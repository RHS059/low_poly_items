#!/usr/bin/env python3
"""Validate actual GLB payloads and independently reopen the authored .blend.
Use Python+bpy for full checks; --skip-blend is available for GLB-only CI.
"""
from pathlib import Path
import argparse, collections, hashlib, json, math, struct, sys
ROOT=Path(__file__).resolve().parents[1]

def triangle_is_degenerate(a,b,c):
 u=[b[k]-a[k] for k in range(3)];v=[c[k]-a[k] for k in range(3)]
 n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
 return sum(x*x for x in n)<1e-22

def read_glb(path,with_binary=False):
 raw=Path(path).read_bytes()
 if len(raw)<20 or raw[:4]!=b'glTF':raise ValueError(f'{path}: not GLB')
 version,total=struct.unpack_from('<II',raw,4)
 if version!=2 or total!=len(raw):raise ValueError(f'{path}: invalid GLB header')
 pos=12;doc=None;binary=b''
 while pos<len(raw):
  length,kind=struct.unpack_from('<II',raw,pos);pos+=8;payload=raw[pos:pos+length];pos+=length
  if kind==0x4e4f534a:doc=json.loads(payload)
  elif kind==0x004e4942:binary=payload
 if pos!=len(raw) or doc is None:raise ValueError(f'{path}: invalid chunks')
 return (doc,binary) if with_binary else doc

def accessor_values(doc,binary,idx):
 a=doc['accessors'][idx];view=doc['bufferViews'][a['bufferView']]
 codes={5120:'b',5121:'B',5122:'h',5123:'H',5125:'I',5126:'f'};width={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]
 fmt='<'+codes[a['componentType']]*width;size=struct.calcsize(fmt);stride=view.get('byteStride',size);offset=view.get('byteOffset',0)+a.get('byteOffset',0)
 return [struct.unpack_from(fmt,binary,offset+i*stride) for i in range(a['count'])]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--expected',type=int,default=1000);ap.add_argument('--skip-blend',action='store_true');args=ap.parse_args()
 data=json.loads((ROOT/'manifest.json').read_text());rows=data['assets'];errors=[];warnings=[];material_defs={};file_hashes={};geometry_hashes=collections.defaultdict(list)
 if len(rows)!=args.expected:errors.append(f'Expected {args.expected} assets, found {len(rows)}')
 names={r['name'] for r in rows}
 if len(names)!=len(rows):errors.append('Duplicate asset names')
 glbs=list((ROOT/'exports').glob('*.glb'))
 if {p.stem for p in glbs}!=names:errors.append('GLB filenames do not exactly match manifest names')
 triangle_total=0;max_ratio=0
 for row in rows:
  path=ROOT/row['glb'];doc,binary=read_glb(path,True);verts=0;tris=0;coords=[];degenerate=0
  if len(doc.get('meshes',[]))!=1:errors.append(f'{row["name"]}: expected one mesh')
  for mesh in doc.get('meshes',[]):
   for p in mesh['primitives']:
    pos=accessor_values(doc,binary,p['attributes']['POSITION']);verts+=len(pos);coords.extend(pos)
    indices=accessor_values(doc,binary,p['indices']);tris+=len(indices)//3
    if len(indices)%3 or any(i[0]>=len(pos) for i in indices):errors.append(f'{row["name"]}: invalid triangle indices')
    else:
     for i in range(0,len(indices),3):
      if triangle_is_degenerate(*(pos[indices[i+j][0]] for j in range(3))):degenerate+=1
    if any(not all(math.isfinite(c) for c in v) for v in pos):errors.append(f'{row["name"]}: nonfinite position')
  if verts!=row['export_vertices']:errors.append(f'{row["name"]}: stale manifest vertex count')
  if degenerate:errors.append(f'{row["name"]}: {degenerate} degenerate exported triangles')
  if verts>row['vertex_limit'] or row['source_vertices']>row['vertex_limit']:errors.append(f'{row["name"]}: vertex limit exceeded ({row["source_vertices"]}/{verts}>{row["vertex_limit"]})')
  if coords:
   lo=[min(v[i] for v in coords) for i in range(3)];hi=[max(v[i] for v in coords) for i in range(3)]
   # glTF Y is up, Blender Z maps to Y, Blender +Y maps to glTF -Z.
   if abs(lo[1])>1e-4 or abs(lo[0]+hi[0])>1e-4 or abs(lo[2]+hi[2])>1e-4:errors.append(f'{row["name"]}: GLB origin not bottom center')
  for node in doc.get('nodes',[]):
   if 'mesh' in node and (node.get('translation',[0,0,0])!=[0,0,0] or node.get('scale',[1,1,1])!=[1,1,1]):errors.append(f'{row["name"]}: nonidentity node transform')
  for mat in doc.get('materials',[]):
   name=mat['name'];fingerprint=json.dumps({k:v for k,v in mat.items() if k!='extras'},sort_keys=True)
   if name in material_defs and material_defs[name]!=fingerprint:errors.append(f'{row["name"]}: inconsistent shared material {name}')
   material_defs[name]=fingerprint
  if any('uri' in x for x in doc.get('buffers',[])+doc.get('images',[])):errors.append(f'{row["name"]}: external GLB dependencies')
  file_hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest();triangle_total+=tris;max_ratio=max(max_ratio,verts/max(row['source_vertices'],1));geometry_hashes[row['source_geometry_sha256']].append(row['name'])
 for names_for_hash in geometry_hashes.values():
  if len(names_for_hash)>1:errors.append('Identical source geometry: '+', '.join(names_for_hash))
 blend_checked=False
 if not args.skip_blend:
  import bpy
  bpy.ops.wm.open_mainfile(filepath=str(ROOT/'city_items.blend'))
  source_meshes=[o for o in bpy.data.objects if o.type=='MESH'];blend_checked=True
  if len(source_meshes)!=args.expected:errors.append(f'Blend contains {len(source_meshes)} meshes, expected {args.expected}')
  if {o.name for o in source_meshes}!={r['name'] for r in rows}:errors.append('Blend mesh names mismatch')
  for obj in source_meshes:
   if obj.location.length>1e-7 or obj.rotation_euler.to_quaternion().angle>1e-7 or max(abs(v-1) for v in obj.scale)>1e-7:errors.append(f'{obj.name}: source transform is not identity')
   lo=[min(v.co[i] for v in obj.data.vertices) for i in range(3)];hi=[max(v.co[i] for v in obj.data.vertices) for i in range(3)]
   if abs(lo[2])>1e-5 or abs(lo[0]+hi[0])>1e-5 or abs(lo[1]+hi[1])>1e-5:errors.append(f'{obj.name}: blend pivot not bottom center')
   obj.data.calc_loop_triangles()
   degenerate=sum(triangle_is_degenerate(*(obj.data.vertices[i].co for i in t.vertices)) for t in obj.data.loop_triangles)
   if degenerate:errors.append(f'{obj.name}: {degenerate} degenerate Blender triangles')
  if len(bpy.data.materials)!=len(material_defs):warnings.append(f'Blend has {len(bpy.data.materials)} palette materials; GLBs use {len(material_defs)}')
 report={'passed':not errors,'asset_count':len(rows),'glb_count':len(glbs),'blend_checked':blend_checked,'shared_materials_used':len(material_defs),'total_export_triangles':triangle_total,'maximum_export_to_source_vertex_ratio':round(max_ratio,4),'size_classes':dict(collections.Counter(r['size_class'] for r in rows)),'source_vertices':{'min':min(r['source_vertices'] for r in rows),'max':max(r['source_vertices'] for r in rows),'total':sum(r['source_vertices'] for r in rows)},'export_vertices':{'min':min(r['export_vertices'] for r in rows),'max':max(r['export_vertices'] for r in rows),'total':sum(r['export_vertices'] for r in rows)},'errors':errors,'warnings':warnings}
 (ROOT/'validation_report.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'SHA256SUMS').write_text(''.join(f'{v}  {k}\n' for k,v in sorted(file_hashes.items()))+f'{hashlib.sha256((ROOT/"city_items.blend").read_bytes()).hexdigest()}  city_items.blend\n')
 print(json.dumps(report,indent=2));return bool(errors)
if __name__=='__main__':sys.exit(main())
