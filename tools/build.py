#!/usr/bin/env python3
"""Build all registered assets in Blender 4.2+ and export individual binary glTF.
Run with Blender's bundled Python or a Python 3.11 environment with bpy==4.2.0.
"""
from pathlib import Path
import argparse, contextlib, importlib.util, json, math, os, sys, time, hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
from assetlib import REGISTRY, PALETTE, LIMITS
ROOT=Path(__file__).resolve().parents[1]

def load_batches(batch=None):
 for path in sorted((ROOT/'batches').glob('batch*.py')):
  if batch and path.stem!=batch and path.stem.replace('batch','b')!=batch: continue
  spec=importlib.util.spec_from_file_location(path.stem,path); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 return REGISTRY

def srgb_to_linear(x): return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4

def palette_entry(key):
 h,metal,rough=PALETTE[key];h=h.lstrip('#')
 return {'name':key,'base_color_srgb': '#'+h,'base_color_linear':[srgb_to_linear(int(h[i:i+2],16)/255) for i in (0,2,4)]+[1.0],'metallic':metal,'roughness':rough}

def make_materials(bpy):
 result={}
 for name in PALETTE:
  d=palette_entry(name);m=bpy.data.materials.new(name);m.use_nodes=True
  m.diffuse_color=d['base_color_linear'];m.metallic=d['metallic'];m.roughness=d['roughness']
  p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=d['base_color_linear'];p.inputs['Metallic'].default_value=d['metallic'];p.inputs['Roughness'].default_value=d['roughness']
  m['palette_id']=name;m['srgb_hex']=d['base_color_srgb'];result[name]=m
 return result

def create_object(bpy,bmesh,a,mats,coll):
 mesh=bpy.data.meshes.new(a.name+'_mesh');mesh.from_pydata(a.vertices,[],a.faces);mesh.update()
 bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
 keys=sorted(set(a.face_materials))
 for key in keys:mesh.materials.append(mats[key])
 for poly,key in zip(mesh.polygons,a.face_materials):poly.material_index=keys.index(key);poly.use_smooth=False
 mesh.validate(verbose=False);mesh.update()
 obj=bpy.data.objects.new(a.name,mesh);coll.objects.link(obj);obj.location=(0,0,0)
 obj['category']=a.category;obj['size_class']=a.size_class;obj['vertex_limit']=LIMITS[a.size_class];obj['units']='meters';obj['pivot']='bottom center';obj['source']='Original procedural geometry'
 obj.asset_mark();obj.asset_data.description=f'{a.name.replace("_"," ")} | {a.category} | {a.size_class} | metre scale, bottom-center origin'
 return obj

def bevel_candidate(bpy,obj,limit):
 """Bake a restrained one-segment bevel only when the budget can support it."""
 width=min(.008,.015*min(d for d in obj.dimensions if d>1e-6))
 mod=obj.modifiers.new('Narrow hard-edge chamfer','BEVEL');mod.width=width;mod.segments=1;mod.limit_method='ANGLE';mod.angle_limit=math.radians(55);mod.use_clamp_overlap=True
 depsgraph=bpy.context.evaluated_depsgraph_get();depsgraph.update()
 candidate=bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph),depsgraph=depsgraph)
 obj.modifiers.remove(mod)
 # Clamped bevels can create microscopic collapsed edges at primitive junctions.
 # Dissolve those before both budget checks and export, preserving materials.
 import bmesh
 bm=bmesh.new();bm.from_mesh(candidate);bmesh.ops.dissolve_degenerate(bm,dist=1e-6,edges=list(bm.edges));bm.to_mesh(candidate);bm.free()
 # Flat normals can create one exported vertex per face corner. This conservative
 # bound prevents the chamfer from consuming a model's actual runtime vertex cap.
 if len(candidate.vertices)>limit or len(candidate.loops)>limit:
  bpy.data.meshes.remove(candidate);return False
 old=obj.data;obj.data=candidate;bpy.data.meshes.remove(old);candidate.name=obj.name+'_mesh'
 for p in candidate.polygons:p.use_smooth=False
 obj['bevel_width_m']=width;obj['bevel_segments']=1
 return True

def scene_setup(bpy):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 src=bpy.context.scene;src.name='Assets at World Origin';src.unit_settings.system='METRIC';src.unit_settings.scale_length=1
 return src

def add_overview(bpy,objects,asset_colls):
 from mathutils import Vector,Quaternion
 overview=bpy.data.scenes.new('Overview');overview.unit_settings.system='METRIC'
 grid=bpy.data.collections.new('Overview Collection Instances');overview.collection.children.link(grid)
 cols=25;spacing=12
 for i,obj in enumerate(objects):
  empty=bpy.data.objects.new('Preview '+obj.name,None);empty.instance_type='COLLECTION';empty.instance_collection=asset_colls[obj.name]
  empty.location=((i%cols)*spacing,-(i//cols)*spacing,0);factor=min(1,9/max(max(obj.dimensions),.001));empty.scale=(factor,)*3;empty['source_asset']=obj.name;grid.objects.link(empty)
 overview.world=bpy.data.worlds.new('Overview World');overview.world.color=(.15,.15,.15)
 bpy.context.window.scene=overview
 for screen in bpy.data.screens:
  for area in screen.areas:
   if area.type=='VIEW_3D':
    sp=area.spaces.active;sp.shading.type='SOLID';sp.shading.color_type='MATERIAL';sp.shading.light='STUDIO';sp.shading.show_shadows=True;sp.shading.show_cavity=True;sp.overlay.show_floor=False;sp.overlay.show_axis_x=False;sp.overlay.show_axis_y=False
    sp.region_3d.view_distance=80;sp.region_3d.view_location=(48,-35,0);sp.region_3d.view_rotation=Quaternion((.880,.279,.115,.364));sp.region_3d.view_perspective='ORTHO'
 return overview

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--batch');parser.add_argument('--expected',type=int,default=1000);parser.add_argument('--partial',action='store_true');parser.add_argument('--skip-export',action='store_true');parser.add_argument('--no-bevel',action='store_true');parser.add_argument('--flat-without-normals',action='store_true',help='Use glTF prescribed flat normals generated by the consumer; useful for vertex budgets.');args=parser.parse_args()
 load_batches(args.batch)
 if len(REGISTRY)!=args.expected and not args.partial:raise SystemExit(f'Expected {args.expected} registrations, got {len(REGISTRY)}. Use --partial for development.')
 import bpy,bmesh
 from validate import read_glb
 start=time.time();source=scene_setup(bpy);mats=make_materials(bpy);objects=[];categories={};asset_colls={};manifest=[];errors=[]
 (ROOT/'exports').mkdir(exist_ok=True)
 # Only whole-registry builds may remove obsolete generated filenames.
 if not args.batch:
  for stale in (ROOT/'exports').glob('*.glb'):
   if stale.stem not in REGISTRY:stale.unlink()
 for i,(name,row) in enumerate(sorted(REGISTRY.items())):
  try:
   a=row['factory']();a.name=name;a.category=row['category'];a.size_class=row['size_class'];a.bottom_center();a.validate()
   category=categories.get(a.category)
   if category is None:category=bpy.data.collections.new(a.category);source.collection.children.link(category);categories[a.category]=category
   coll=bpy.data.collections.new(name);category.children.link(coll);asset_colls[name]=coll
   obj=create_object(bpy,bmesh,a,mats,coll);objects.append(obj);bpy.context.view_layer.update()
   beveled=False if args.no_bevel else bevel_candidate(bpy,obj,LIMITS[a.size_class])
   mesh=obj.data;mesh.calc_loop_triangles();lo=[min(v.co[j] for v in mesh.vertices) for j in range(3)];hi=[max(v.co[j] for v in mesh.vertices) for j in range(3)]
   # The pivot is defined from the final evaluated mesh, including chamfers.
   shift=((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2])
   for v in mesh.vertices:
    for j in range(3):v.co[j]-=shift[j]
   lo=[x-shift[j] for j,x in enumerate(lo)];hi=[x-shift[j] for j,x in enumerate(hi)]
   mesh.update();mesh.calc_loop_triangles();dest=ROOT/'exports'/f'{name}.glb'
   if not args.skip_export:
    obj.select_set(True);bpy.context.view_layer.objects.active=obj
    # Official Blender exporter; flat split normals are preserved by default.
    with open(os.devnull,'w') as quiet,contextlib.redirect_stdout(quiet):
     bpy.ops.export_scene.gltf(filepath=str(dest),export_format='GLB',use_selection=True,export_materials='EXPORT',export_extras=True,export_cameras=False,export_lights=False,export_animations=False,export_yup=True,export_normals=not args.flat_without_normals)
    obj.select_set(False)
   glb=read_glb(dest) if dest.exists() else None
   glb_vertices=sum(glb['accessors'][p['attributes']['POSITION']]['count'] for m in glb['meshes'] for p in m['primitives']) if glb else None
   entry={'name':name,'category':a.category,'size_class':a.size_class,'authored_vertices':len(a.vertices),'source_vertices':len(mesh.vertices),'export_vertices':glb_vertices,'polygons':len(mesh.polygons),'triangles':len(mesh.loop_triangles),'vertex_limit':LIMITS[a.size_class],'dimensions_m':[round(y-x,6) for x,y in zip(lo,hi)],'bounds_min':[round(v,8) for v in lo],'bounds_max':[round(v,8) for v in hi],'origin':[0,0,0],'materials':sorted(set(a.face_materials)),'beveled':beveled,'glb':f'exports/{name}.glb','source_geometry_sha256':hashlib.sha256(json.dumps([a.vertices,a.faces],separators=(',',':')).encode()).hexdigest()}
   if glb_vertices is not None and glb_vertices>LIMITS[a.size_class]:errors.append(f'{name}: GLB {glb_vertices} > {LIMITS[a.size_class]}')
   manifest.append(entry)
   if (i+1)%25==0:print(f'Built {i+1}/{len(REGISTRY)} in {time.time()-start:.1f}s',flush=True)
  except Exception as exc:errors.append(f'{name}: {type(exc).__name__}: {exc}');print('ERROR',errors[-1],flush=True);raise
 add_overview(bpy,objects,asset_colls)
 bpy.context.scene['asset_count']=len(objects);bpy.context.scene['readme']='Switch to Assets at World Origin for original meshes. Overview contains collection instances only.'
 bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'city_items.blend'),compress=True)
 report={'schema_version':1,'asset_count':len(manifest),'blender_version':bpy.app.version_string,'units':'meters','blend_up_axis':'Z','glb_up_axis':'Y','glb_normals':'flat split normals' if not args.flat_without_normals else 'omitted: consumer must generate flat normals per glTF 2.0','assets':manifest,'build_errors':errors}
 (ROOT/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'materials.json').write_text(json.dumps([palette_entry(n) for n in PALETTE],indent=2)+'\n')
 print(f'Built {len(manifest)} assets, {len(errors)} errors; {time.time()-start:.1f}s',flush=True)
 if errors:
  print('\n'.join(errors));return 1
 return 0
if __name__=='__main__':
 # bpy's pip wheel can crash during CPython module teardown after scene creation.
 # Exit only after all synchronous Blender saves and JSON writes have completed.
 import traceback
 try: status=main()
 except Exception:
  traceback.print_exc();status=1
 sys.stdout.flush();sys.stderr.flush();os._exit(status)
