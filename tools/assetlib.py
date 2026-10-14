"""Deterministic low-poly mesh construction. Metres, +Z up, right-handed.
All parts become one mesh per asset. Materials are shared by palette name.
"""
from __future__ import annotations
import math
from dataclasses import dataclass

PALETTE = {
 'asphalt':('#30363c',0.0,.92), 'concrete':('#a6aaa8',0.0,.88),
 'concrete_light':('#d4d1c8',0.0,.85), 'metal':('#73818b',.65,.43),
 'steel':('#aab6be',.75,.35), 'dark_metal':('#303e46',.7,.44),
 'black':('#172127',.1,.7), 'rubber':('#242b30',0,.95),
 'white':('#eeeae0',0,.62), 'red':('#c43b38',.08,.58),
 'orange':('#ed8539',0,.6), 'yellow':('#efbc46',.05,.56),
 'green':('#386c50',.1,.65), 'blue':('#34688d',.15,.56),
 'navy':('#223f57',.12,.63), 'teal':('#397b7c',.1,.57),
 'wood':('#a97647',0,.85), 'wood_dark':('#684d35',0,.9),
 'wood_light':('#c69b64',0,.83), 'brick':('#98624c',0,.9),
 'terracotta':('#bc7854',0,.85), 'sand':('#c7b795',0,.97),
 'soil':('#584e3e',0,1), 'foliage':('#548254',0,.9),
 'foliage_dark':('#315a43',0,.95), 'foliage_light':('#82a668',0,.9),
 'glass':('#88b5c3',.25,.23), 'water':('#518ca3',.15,.28),
 'cream':('#dfd3b1',0,.83), 'brown':('#806049',0,.86),
 'purple':('#775b85',0,.69), 'pink':('#c78288',0,.66),
 'silver':('#cad0d1',.8,.31), 'gold':('#be9744',.7,.35),
 'light':('#ffe4a3',0,.4), 'paper':('#dedbcf',0,.93),
}
ALIASES={'metal_dark':'dark_metal','dark_steel':'dark_metal','cardboard':'cream','gray':'concrete','grey':'concrete','iron':'dark_metal','aluminum':'silver','aluminium':'silver','plastic':'blue','bark':'wood_dark','leaves':'foliage','leaf':'foliage','stone':'concrete','chrome':'silver','tan':'sand','safety_orange':'orange','safety_yellow':'yellow','traffic_red':'red','traffic_green':'green'}
REGISTRY={}
LIMITS={'handheld':999,'person':5000,'large':10000}

def material(name):
 name=ALIASES.get(name,name)
 if name not in PALETTE: raise ValueError(f'Unknown palette material {name!r}')
 return name

def register(name,category,size_class,factory):
 if name in REGISTRY: raise ValueError(f'Duplicate asset {name}')
 if size_class not in LIMITS: raise ValueError(size_class)
 REGISTRY[name]={'name':name,'category':category,'size_class':size_class,'factory':factory}

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,s): return tuple(x*s for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(v):
 l=math.sqrt(dot(v,v))
 return mul(v,1/l) if l>1e-12 else (0,0,1)
def frame(axis):
 w=unit(axis); u=unit(cross((0,0,1) if abs(w[2])<.99 else (0,1,0),w)); return u,cross(w,u),w

def rotate(v,rot):
 if isinstance(rot,(int,float)): rot=(0,0,rot)
 x,y,z=v
 for i,a in enumerate(rot):
  c,s=math.cos(a),math.sin(a)
  if i==0: y,z=y*c-z*s,y*s+z*c
  elif i==1: x,z=x*c+z*s,-x*s+z*c
  else: x,y=x*c-y*s,x*s+y*c
 return x,y,z

class Asset:
 def __init__(self,name,category='misc',size_class='person',**metadata):
  self.name=name; self.category=category; self.size_class=size_class
  self.vertices=[]; self.faces=[]; self.face_materials=[]; self.metadata=metadata
 @property
 def verts(self): return self.vertices
 def mesh(self,vertices,faces,mat='metal'):
  offset=len(self.vertices); self.vertices.extend(tuple(float(c) for c in v) for v in vertices)
  self.faces.extend(tuple(i+offset for i in f) for f in faces)
  if isinstance(mat,(list,tuple)): self.face_materials.extend(material(m) for m in mat)
  else: self.face_materials.extend([material(mat)]*len(faces))
  return self
 def box(self,center,size,mat='metal',rot=None,rotation=None):
  x,y,z=(s/2 for s in size)
  vs=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]
  r=rotation if rotation is not None else rot
  if r is not None: vs=[rotate(v,r) for v in vs]
  return self.mesh([add(v,center) for v in vs],[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],mat)
 def cylinder(self,p1,p2,radius,mat='metal',sides=8,radius2=None,cap=True,**kwargs):
  r2=radius if radius2 is None else radius2
  if abs(r2)<1e-12: return self.cone(p1,p2,radius,mat,sides)
  if abs(radius)<1e-12: return self.cone(p2,p1,r2,mat,sides)
  u,v,w=frame(sub(p2,p1)); vs=[]
  for p,r in ((p1,radius),(p2,r2)):
   for i in range(sides):
    th=2*math.pi*i/sides; vs.append(add(p,add(mul(u,r*math.cos(th)),mul(v,r*math.sin(th)))))
  fs=[(i,(i+1)%sides,(i+1)%sides+sides,i+sides) for i in range(sides)]
  if cap: fs += [tuple(reversed(range(sides))),tuple(range(sides,2*sides))]
  return self.mesh(vs,fs,mat)
 def cone(self,p1,p2,radius,mat='metal',sides=8,radius2=0):
  if radius2: return self.cylinder(p1,p2,radius,mat,sides,radius2)
  u,v,w=frame(sub(p2,p1)); vs=[add(p1,add(mul(u,radius*math.cos(2*math.pi*i/sides)),mul(v,radius*math.sin(2*math.pi*i/sides)))) for i in range(sides)]+[p2]
  return self.mesh(vs,[(i,(i+1)%sides,sides) for i in range(sides)]+[tuple(reversed(range(sides)))],mat)
 def sphere(self,center,radius,mat='metal',segments=8,rings=4,scale=None):
  scales=scale or ((radius,radius,radius) if isinstance(radius,(float,int)) else radius)
  vs=[(0,0,-1)]
  for j in range(1,rings):
   lat=-math.pi/2+math.pi*j/rings
   vs.extend((math.cos(lat)*math.cos(2*math.pi*i/segments),math.cos(lat)*math.sin(2*math.pi*i/segments),math.sin(lat)) for i in range(segments))
  top=len(vs);vs.append((0,0,1));fs=[]
  fs.extend((0,1+(i+1)%segments,1+i) for i in range(segments))
  for j in range(rings-2):
   k=1+j*segments;fs.extend((k+i,k+(i+1)%segments,k+(i+1)%segments+segments,k+i+segments) for i in range(segments))
  k=1+(rings-2)*segments;fs.extend((k+i,k+(i+1)%segments,top) for i in range(segments))
  return self.mesh([add(center,tuple(c*s for c,s in zip(v,scales))) for v in vs],fs,mat)
 def torus(self,center,major_radius,minor_radius,mat='metal',axis='z',segments=12,sides=6,arc=2*math.pi):
  ax={'x':(1,0,0),'y':(0,1,0),'z':(0,0,1)}.get(axis,axis) if isinstance(axis,str) else axis
  u,v,w=frame(ax);vs=[];closed=abs(arc-2*math.pi)<1e-8;n=segments if closed else segments+1
  for i in range(n):
   th=arc*i/segments; radial=add(mul(u,math.cos(th)),mul(v,math.sin(th)))
   for j in range(sides):
    ph=2*math.pi*j/sides;vs.append(add(center,add(mul(radial,major_radius+minor_radius*math.cos(ph)),mul(w,minor_radius*math.sin(ph)))))
  fs=[]
  for i in range(segments):
   for j in range(sides): fs.append((i*sides+j,((i+1)%n)*sides+j,((i+1)%n)*sides+(j+1)%sides,i*sides+(j+1)%sides))
  if not closed: fs += [tuple(reversed(range(sides))),tuple(range((n-1)*sides,n*sides))]
  return self.mesh(vs,fs,mat)
 def prism(self,points,zmin,zmax,mat='metal'):
  n=len(points);vs=[(x,y,z) for z in (zmin,zmax) for x,y in points]
  return self.mesh(vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat)
 def beam(self,p1,p2,width,depth=None,mat='metal'):
  depth=width if depth is None else depth;u,v,w=frame(sub(p2,p1))
  vs=[add(p,add(mul(u,sx*width/2),mul(v,sy*depth/2))) for p in (p1,p2) for sx,sy in ((-1,-1),(1,-1),(1,1),(-1,1))]
  return self.mesh(vs,[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],mat)
 def tube(self,points,radius,mat='metal',sides=6):
  for p1,p2 in zip(points,points[1:]): self.cylinder(p1,p2,radius,mat,sides)
  return self
 def translate(self,offset): self.vertices=[add(v,offset) for v in self.vertices];return self
 def scale(self,scale):
  s=(scale,)*3 if isinstance(scale,(int,float)) else scale
  self.vertices=[tuple(c*k for c,k in zip(v,s)) for v in self.vertices];return self
 def rotate(self,rotation): self.vertices=[rotate(v,rotation) for v in self.vertices];return self
 def bottom_center(self):
  lo=[min(v[i] for v in self.vertices) for i in range(3)];hi=[max(v[i] for v in self.vertices) for i in range(3)]
  self.translate((-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]));return self
 def bounds(self): return ([min(v[i] for v in self.vertices) for i in range(3)],[max(v[i] for v in self.vertices) for i in range(3)])
 def validate(self):
  if not self.vertices or not self.faces: raise ValueError(f'{self.name}: empty mesh')
  if len(self.vertices)>LIMITS[self.size_class]: raise ValueError(f'{self.name}: {len(self.vertices)} vertices exceeds {LIMITS[self.size_class]}')
  if len(self.faces)!=len(self.face_materials): raise ValueError('Material count mismatch')
  if any(not all(math.isfinite(c) for c in v) for v in self.vertices): raise ValueError('Nonfinite coordinates')
  if any(len(set(f))<3 for f in self.faces): raise ValueError('Degenerate face')
  for i,f in enumerate(self.faces):
   if any(k<0 or k>=len(self.vertices) for k in f): raise ValueError(f'Face {i}: invalid index')
   area=(0,0,0);p=self.vertices[f[0]]
   for j in range(1,len(f)-1): area=add(area,cross(sub(self.vertices[f[j]],p),sub(self.vertices[f[j+1]],p)))
   if dot(area,area)<1e-22: raise ValueError(f'Face {i}: zero area')
  return True
