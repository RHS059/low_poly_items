"""Fifty modular building parts. Metres, 1 m planning grid, 3 m wall height.
All origins remain bottom-centred. See BUILDING_KIT.md for placement sockets.
"""
from assetlib import Asset,register


def item(name,category,size='large'):
 def deco(fn):
  def factory():
   a=Asset('b21_'+name,category,size);fn(a);return a.bottom_center()
  register('b21_'+name,category,size,factory);return factory
 return deco


def box(a,x,y,z,w,d,h,m):a.box((x,y,z),(w,d,h),m)
def wall(a,w,mat='cream',opening=None):
 # Bands are contiguous wall sections, never coplanar surface overlays.
 def fill(x,width,z0,z1):
  cuts=sorted(set([z0,z1]+[z for z in (.11,2.93) if z0<z<z1]))
  for lo,hi in zip(cuts,cuts[1:]):
   material='concrete' if hi<=.11001 or lo>=2.92999 else mat
   box(a,x,0,(lo+hi)/2,width,.2,hi-lo,material)
 if opening:
  ow,sill,oh=opening;j=(w-ow)/2
  for sign in (-1,1):fill(sign*(ow/2+j/2),j,0,3)
  if sill:fill(0,ow,0,sill)
  fill(0,ow,sill+oh,3)
  for sign in (-1,1):box(a,sign*(ow/2+.016),0,sill+oh/2,.032,.204,oh,'concrete')
  box(a,0,0,sill+oh+.016,ow+.064,.204,.032,'concrete')
 else:fill(0,w,0,3)

for w in (1,2,4):
 @item(f'wall_solid_{w}m','building_walls')
 def solid(a,w=w):wall(a,w)
for w in (2,4):
 @item(f'wall_door_opening_{w}m','building_walls')
 def doorwall(a,w=w):wall(a,w,opening=(1,0,2.2))
for w,ow in [(2,1),(4,2)]:
 @item(f'wall_window_opening_{w}m','building_walls')
 def windowwall(a,w=w,ow=ow):wall(a,w,opening=(ow,.9,1.4))
@item('wall_double_door_opening_4m','building_walls')
def doublewall(a):wall(a,4,opening=(2,0,2.2))
@item('wall_storefront_opening_4m','building_walls')
def storefrontwall(a):wall(a,4,'brick',opening=(3.6,0,2.6))
@item('wall_corner_1m','building_walls')
def corner(a):
 box(a,0,-.4,1.5,1,.2,3,'cream');box(a,-.4,.1,1.5,.2,.8,3,'cream')
@item('wall_t_junction_1m','building_walls')
def tjunction(a):
 box(a,0,-.4,1.5,1,.2,3,'cream');box(a,0,.1,1.5,.2,.8,3,'cream')
@item('wall_end_pier','building_walls','person')
def pier(a):
 box(a,0,0,1.5,.2,.2,3,'concrete')
 for z in (.06,2.94):box(a,0,0,z,.22,.22,.12,'stone')

# Floor top surfaces are at +0.2 m from each source origin.
for w,d in [(1,1),(2,2),(4,4),(2,4),(4,8)]:
 @item(f'floor_concrete_{w}x{d}m','building_floors')
 def floor(a,w=w,d=d):
  box(a,0,0,.0925,w,d,.185,'concrete');box(a,0,0,.1925,w-.004,d-.004,.015,'stone')
for w,d in [(2,2),(4,4),(2,4)]:
 @item(f'floor_timber_{w}x{d}m','building_floors')
 def timber(a,w=w,d=d):
  box(a,0,0,.085,w,d,.17,'wood_dark')
  n=round(w/.2)
  for i in range(n):box(a,-w/2+(i+.5)*w/n,0,.185,w/n-.003,d,.03,'wood' if i%3 else 'wood_light')
@item('floor_stairwell_opening_4x4m','building_floors')
def stairfloor(a):
 for x in (-1.25,1.25):box(a,x,0,.1,1.5,4,.2,'concrete')
 for y in (-1.5,1.5):box(a,0,y,.1,1,1,.2,'concrete')
@item('floor_edge_fascia_4m','building_floors')
def fascia(a):
 box(a,0,0,.1,4,.2,.2,'concrete');box(a,0,-.101,.1,4,.006,.12,'stone')

for w,d in [(1,1),(2,2),(4,4),(2,4)]:
 @item(f'ceiling_plain_{w}x{d}m','building_ceilings')
 def ceiling(a,w=w,d=d):
  box(a,0,0,.0575,w,d,.085,'concrete');box(a,0,0,.0075,w-.002,d-.002,.015,'cream')
for w in (2,4):
 @item(f'ceiling_suspended_grid_{w}m','building_ceilings')
 def suspended(a,w=w):
  n=w
  for x in range(n):
   for y in range(n):box(a,-w/2+x+.5,-w/2+y+.5,.038,.976,.976,.05,'cream')
  for i in range(n+1):
   p=-w/2+i;bar=.024
   if i==0:p+=.006;bar=.012
   if i==n:p-=.006;bar=.012
   box(a,p,0,.01,bar,w,.02,'steel');box(a,0,p,.01,w,bar,.02,'steel')
@item('ceiling_exposed_beams_4x4m','building_ceilings')
def beamceiling(a):
 box(a,0,0,.18,4,4,.04,'wood_dark')
 for x in (-1.5,-.5,.5,1.5):box(a,x,0,.08,.12,4,.16,'wood')
@item('ceiling_service_hatch_2x2m','building_ceilings')
def hatch(a):
 for x in (-.65,.65):box(a,x,0,.05,.7,2,.1,'cream')
 for y in (-.65,.65):box(a,0,y,.05,.6,.7,.1,'cream')
 box(a,0,0,.045,.574,.574,.07,'steel');box(a,.2,-.005,.008,.06,.02,.008,'black')

# Leaf width 0.9 and jamb outer width 1.0 fit the 1 m door opening.
def doorframe(a,w=1,h=2.2,mat='wood_dark'):
 for x in (-w/2+.025,w/2-.025):box(a,x,0,h/2,.05,.16,h,mat)
 box(a,0,0,h-.025,w,.16,.05,mat)
 for sy in (-1,1):
  for x in (-w/2+.024,w/2-.024):box(a,x,sy*.083,h/2,.046,.01,h,mat)
def leaf(a,w=.9,h=2.13,mat='wood',glass=False,x=0):
 if glass:
  for xx in (-w/2+.045,w/2-.045):box(a,x+xx,0,h/2,.09,.045,h,mat)
  for z in (.08,h-.05,h*.43):box(a,x,0,z,w,.045,.085,mat)
  
  for z0,z1 in [(.115,h*.43-.035),(h*.43+.035,h-.085)]:box(a,x,0,(z0+z1)/2,w-.17,.012,z1-z0,'glass')
 else:
  box(a,x,0,h/2,w,.04,h,mat)
  for sy in (-1,1):
   if mat=='steel':
    box(a,x,sy*.025,.16,w-.08,.01,.25,'silver')
    for z in (.4,.46,.52,.58):box(a,x,sy*.025,z,w*.58,.012,.025,'dark_metal')
   elif mat=='cream':
    for xx in (-w*.23,w*.23):
     for z,hh in [(h*.25,h*.32),(h*.69,h*.4)]:box(a,x+xx,sy*.024,z,w*.34,.008,hh,'cream')
   else:
    for z,hh in [(h*.25,h*.32),(h*.69,h*.4)]:box(a,x,sy*.023,z,w-.18,.006,hh,'wood_dark')
 for sy in (-1,1):
  box(a,x+w*.36,sy*.03,h*.48,.035,.025,.16,'steel');a.beam((x+w*.36,sy*.055,h*.51),(x+w*.2,sy*.055,h*.51),.018,.018,'silver')
 for z in (.22,h*.5,h-.22):a.cylinder((x-w/2,-.028,z-.045),(x-w/2,-.028,z+.045),.016,'steel',8)
for name,mat,glass in [('wood_panel','wood',False),('painted_panel','cream',False),('steel_service','steel',False),('glazed_entry','dark_metal',True)]:
 @item('door_'+name,'building_doors','person')
 def doormodule(a,mat=mat,glass=glass):doorframe(a);leaf(a,mat=mat,glass=glass)
@item('door_empty_frame_1m','building_doors','person')
def emptyframe(a):doorframe(a)
@item('door_double_glazed_2m','building_doors','person')
def doubledoor(a):
 doorframe(a,2)
 for x in (-.475,.475):
  start=len(a.vertices);face_start=len(a.faces);leaf(a,.946,mat='dark_metal',glass=True,x=x)
  if x>0:
   a.vertices[start:]=[(2*x-vx,vy,vz) for vx,vy,vz in a.vertices[start:]]
   a.faces[face_start:]=[tuple(reversed(f)) for f in a.faces[face_start:]]
@item('door_double_steel_2m','building_doors','person')
def doublesteel(a):
 doorframe(a,2,2.2,'steel')
 for x in (-.475,.475):
  start=len(a.vertices);face_start=len(a.faces);leaf(a,.946,mat='steel',x=x)
  if x>0:
   a.vertices[start:]=[(2*x-vx,vy,vz) for vx,vy,vz in a.vertices[start:]]
   a.faces[face_start:]=[tuple(reversed(f)) for f in a.faces[face_start:]]
@item('door_leaf_wood_900mm','building_doors','person')
def bareleaf(a):leaf(a)
@item('door_leaf_glass_900mm','building_doors','person')
def bareglass(a):leaf(a,mat='dark_metal',glass=True)
@item('door_storefront_3_6m','building_doors','large')
def storedoor(a):
 doorframe(a,3.6,2.6,'dark_metal')
 for x in (-1.25,1.25):
  box(a,x,0,1.3,1,.018,2.52,'glass');box(a,x,0,.025,1,.05,.05,'dark_metal')
  for xx in (x-.5,x+.5):box(a,xx,0,1.3,.04,.05,2.6,'dark_metal')
 leaf(a,1.45,2.542,'dark_metal',True)

# Window modules fit matching rough openings, with genuine recessed glazing.
def window(a,w=1,h=1.4,style='fixed',mat='cream'):
 for x in (-w/2+.035,w/2-.035):box(a,x,0,h/2,.07,.14,h,mat)
 for z in (.035,h-.035):box(a,0,0,z,w,.14,.07,mat)
 cols=2 if style in ['slider','paired','storefront'] else 1
 rows=2 if style in ['sash','cross'] else 1
 if style=='cross':cols=2
 iw=w-.14;ih=h-.14
 for i in range(cols):
  for j in range(rows):
   x=-iw/2+(i+.5)*iw/cols;z=.07+(j+.5)*ih/rows
   box(a,x,.012 if i%2 else 0,z,iw/cols+.01,.018,ih/rows+.01,'glass')
 for i in range(1,cols):box(a,-iw/2+i*iw/cols,0,h/2,.045,.07,h-.14,mat)
 for j in range(1,rows):box(a,0,0,.07+j*ih/rows,w-.14,.07,.045,mat)
 if style in ['sash','slider']:
  box(a,0,-.048,h/2,.08,.024,.018,'steel')
for name,w,h,style in [('fixed_1m',1,1.4,'fixed'),('fixed_2m',2,1.4,'fixed'),('double_hung_1m',1,1.4,'sash'),('sliding_2m',2,1.4,'slider'),('cross_mullion_1m',1,1.4,'cross'),('paired_2m',2,1.4,'paired'),('clerestory_2m',2,.6,'fixed'),('shopfront_3_6m',3.6,2.6,'storefront')]:
 @item('window_'+name,'building_windows','person' if w<=2 else 'large')
 def win(a,w=w,h=h,style=style):window(a,w,h,style)
@item('window_sill_1m','building_windows','person')
def sill(a):box(a,0,0,.035,1,.26,.07,'stone')
@item('window_sill_2m','building_windows','person')
def sill2(a):box(a,0,0,.035,2,.26,.07,'stone')
