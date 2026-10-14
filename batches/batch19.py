"""Fifty practical American property-boundary assets; metres, bottom centered.

Open meshes are actual rods/lattice, never opaque stand-ins.  Rail joinery,
hinge barrels, latch hardware, post caps and foundations are deliberately
chunky enough to survive a low-poly city-kit camera distance.
"""
from assetlib import Asset, register
import math

CAT = 'fences_gates_boundaries'


def asset(name, large=False):
    return Asset('b19_' + name, CAT, 'large' if large else 'person',
                 style='muted crafted low-poly', units='metres')


def rod(a, p, q, r=.018, mat='dark_metal', sides=6):
    a.cylinder(p, q, r, mat, sides)


def poly(a, pts, y=0, thick=.05, mat='wood'):
    # Points run counter-clockwise in the x/z plane, as viewed from -Y.
    if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(pts,pts[1:]+pts[:1])) < 0:
        pts = list(reversed(pts))
    n = len(pts)
    vs = [(x, y-thick/2, z) for x,z in pts] + [(x, y+thick/2, z) for x,z in pts]
    fs = [tuple(range(n)), tuple(reversed(range(n,2*n)))]
    fs += [(i,n+i,n+(i+1)%n,(i+1)%n) for i in range(n)]
    a.mesh(vs,fs,mat)


def post(a, x, h, mat='wood_dark', w=.12, y=0, cap=True, foot=True):
    a.box((x,y,h/2),(w,w,h),mat)
    if foot:
        a.box((x,y,.06),(w+.10,w+.10,.12),'concrete')
    if cap:
        a.box((x,y,h+.018),(w+.025,w+.025,.036),mat)
        rr=w*.5+.012
        a.mesh([(x-rr,y-rr,h+.036),(x+rr,y-rr,h+.036),(x+rr,y+rr,h+.036),(x-rr,y+rr,h+.036),(x,y,h+.093)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(3,2,1,0)],mat)
    if mat in ('dark_metal','green'):
        a.box((x,y,.125),(w+.04,w+.04,.035),mat)
        for dx in (-.065,.065):
            for dy in (-.065,.065):rod(a,(x+dx,y+dy,.09),(x+dx,y+dy,.105),.008,'steel',6)


def pipepost(a,x,h,y=0,r=.045,mat='steel',foot=True):
    rod(a,(x,y,.03),(x,y,h),r,mat,8)
    a.cylinder((x,y,h),(x,y,h+.028),r*1.16,mat,8)
    if foot:
        a.box((x,y,.045),(.20,.20,.09),'concrete')
    for z in (.28,h-.15):
        a.cylinder((x,y,z-.02),(x,y,z+.02),r*1.22,mat,8)
        a.box((x-r*1.05,y-.012,z),(.07,.035,.044),mat)
        rod(a,(x-r*1.05,y-.031,z),(x-r*1.05,y-.047,z),.011,'dark_metal',6)


def rails(a,w,zs,mat='wood_dark',depth=.07,height=.10,y=.03):
    for z in zs:
        a.box((0,y,z),(w,depth,height),mat)
        if mat.startswith('wood'):
            for x in (-w/2+.09,w/2-.09):
                rod(a,(x,y-depth/2-.004,z),(x,y-depth/2-.014,z),.012,'dark_metal',6)


def picket(a,x,z1,z2,w=.13,mat='wood_light',y=-.04,style='point'):
    if style=='point':
        pts=[(x-w/2,z1),(x+w/2,z1),(x+w/2,z2-.12),(x,z2),(x-w/2,z2-.12)]
    elif style=='dog':
        pts=[(x-w/2,z1),(x+w/2,z1),(x+w/2,z2-.045),(x+w/2-.035,z2),(x-w/2+.035,z2),(x-w/2,z2-.045)]
    else:
        pts=[(x-w/2,z1),(x+w/2,z1),(x+w/2,z2),(x-w/2,z2)]
    poly(a,pts,y,.045,mat)


def wood_frame(a,w,h,mat='wood_dark',brace=False,y=0):
    a.box((-w/2,y,h/2+.10),(.08,.10,h),mat)
    a.box((w/2,y,h/2+.10),(.08,.10,h),mat)
    rails(a,w,[.20,h],mat,.10,.12,y)
    if brace:
        a.beam((-w/2+.05,y+.07,.26),(w/2-.05,y+.07,h-.06),.095,.05,mat)


def metal_frame(a,w,h,bottom=.12,mat='dark_metal',y=0,r=.029):
    for x in [-w/2,w/2]: rod(a,(x,y,bottom),(x,y,h),r,mat)
    for z in [bottom,h]: rod(a,(-w/2,y,z),(w/2,y,z),r,mat)


def hardware(a,w,h,mat='dark_metal',left=True,y=-.11,strap=False):
    x=-w/2 if left else w/2
    for z in [.32,h-.27]:
        rod(a,(x,y,z-.07),(x,y,z+.07),.033,mat,8)
        rod(a,(x,y,z+.071),(x,y,z+.095),.018,'steel',6)
        direction=-1 if left else 1
        a.box((x+direction*.074,y+.012,z),(.13,.035,.10),mat)
        rod(a,(x+direction*.112,y-.01,z),(x+direction*.112,y-.033,z),.017,'steel',6)
        a.box((x+( .14 if left else -.14),y+.012,z),(.27,.028,.047),mat)
        if strap:
            for xx in [x+(.07 if left else -.07),x+(.24 if left else -.24)]:
                rod(a,(xx,y-.025,z),(xx,y-.041,z),.016,'steel',6)
    x=w/2-.12 if left else -w/2+.12
    z=h*.58
    a.box((x,y-.008,z),(.10,.035,.15),mat)
    rod(a,(x,y-.07,z-.035),(x,y-.07,z+.07),.017,mat)
    a.box((x+.09,y-.03,z+.08),(.22,.035,.035),mat)
    a.box((x+.21,y+.003,z+.06),(.055,.065,.09),mat)
    rod(a,(x,y-.041,z-.045),(x,y-.058,z-.045),.012,'steel',6)


def meshgrid(a,w,h,bottom=.15,spacing=.25,y=0,mat='steel',radius=.008):
    for i in range(1,int(w/spacing)+1):
        x=-w/2+i*w/(int(w/spacing)+1)
        rod(a,(x,y,bottom),(x,y,h),radius,mat,4)
    for i in range(1,int((h-bottom)/spacing)+1):
        z=bottom+i*(h-bottom)/(int((h-bottom)/spacing)+1)
        rod(a,(-w/2,y,z),(w/2,y,z),radius,mat,4)


def diamond(a,w,h,bottom=.12,y=0,spacing=.27,mat='steel',radius=.007):
    # Clip each diagonal family to the actual rectangular fence opening.
    for s in [-1,1]:
        c=-w/2-h
        while c <= w/2+h:
            pts=[]
            for x in [-w/2,w/2]:
                z=s*x+c
                if bottom-1e-8 <= z <= h+1e-8: pts.append((x,y,z))
            for z in [bottom,h]:
                x=(z-c)/s
                if -w/2-1e-8 <= x <= w/2+1e-8: pts.append((x,y,z))
            unique=[]
            for p in pts:
                if not any(sum((u-v)**2 for u,v in zip(p,q))<1e-12 for q in unique): unique.append(p)
            if len(unique)==2: rod(a,unique[0],unique[1],radius,mat,4)
            c += spacing


def iron_infill(a,w,h,bottom=.15,n=11,spears=False,arched=False,y=0):
    rails(a,w,[bottom+.12,h-.16],'dark_metal',.038,.04,y)
    for i in range(n):
        x=-w/2+(i+.5)*w/n
        top=h+(.28*(1-(2*x/w)**2) if arched else 0)
        a.box((x,y,(bottom+top)/2),(.032,.032,top-bottom),'dark_metal')
        if spears:
            poly(a,[(x-.045,top),(x,top+.13),(x+.045,top),(x,top-.055)],y,.026,'dark_metal')


def brickwork(a,w,h,depth=.27,x0=0,y=0,mat='brick',course=.18):
    # Visible mortar joints with alternating bond; separated closed bricks.
    rows=int(h/course)
    for j in range(rows):
        x=-w/2+x0
        first=.23 if j%2 else .46
        while x < w/2+x0-.005:
            span=min(first,w/2+x0-x)
            if span>.02: a.box((x+span/2,y,(j+.5)*course),(span-.012,depth,course-.014),mat)
            x+=span; first=.46
    a.box((x0,y,rows*course+.04),(w+.04,depth+.07,.08),'concrete_light')


def finish(a):
    return a.bottom_center()


def gothic_picket_fence():
    a=asset('gothic_picket_fence'); w=2.4
    for x in [-w/2,w/2]: post(a,x,1.13,'wood_dark')
    rails(a,w,[.29,.77])
    for i in range(13): picket(a,-1.10+i*2.20/12,.09,1.09)
    return finish(a)


def dogear_stockade_fence():
    a=asset('dogear_stockade_fence'); w=2.4
    for x in [-w/2,w/2]: post(a,x,1.78)
    rails(a,w,[.32,.90,1.49])
    for i in range(16): picket(a,-1.125+i*.15,.08,1.83,.143,'wood',style='dog')
    return finish(a)


def shadowbox_privacy_fence():
    a=asset('shadowbox_privacy_fence'); w=2.4
    for x in [-w/2,w/2]: post(a,x,1.82)
    rails(a,w,[.34,1.0,1.62],depth=.11)
    for i in range(17): picket(a,-1.12+i*.14,.10,1.78,.19,'wood_light' if i%2 else 'wood',y=-.09 if i%2 else .11,style='flat')
    return finish(a)


def board_batten_fence():
    a=asset('board_batten_fence'); w=2.4
    for x in [-1.2,1.2]: post(a,x,1.88)
    for i in range(10): picket(a,-1.08+i*.24,.12,1.79,.236,'wood',style='flat')
    for i in range(9): a.box((-.96+i*.24,-.079,.955),(.053,.04,1.67),'wood_dark')
    rails(a,w,[.14,1.82],'wood_dark',.17,.075)
    return finish(a)


def horizontal_cedar_slat_fence():
    a=asset('horizontal_cedar_slat_fence')
    for x in [-1.22,0,1.22]: post(a,x,1.80,'dark_metal',.065)
    for i in range(12): a.box((0,-.06,.18+i*.138),(2.45,.05,.105),'wood_light' if i%3==0 else 'wood')
    return finish(a)


def basketweave_timber_fence():
    a=asset('basketweave_timber_fence')
    for x in [-1.2,0,1.2]: post(a,x,1.6,'wood_dark',.10)
    for i in range(8):
        y=.075 if i%2 else -.075; z=.18+i*.18
        a.beam((-1.14,-y,z),(0,y,z),.042,.14,'wood')
        a.beam((0,y,z),(1.14,-y,z),.042,.14,'wood')
    rails(a,2.4,[1.62],'wood_dark',.13,.065)
    return finish(a)


def split_rail_fence():
    a=asset('split_rail_fence')
    for x in [-1.45,1.45]: post(a,x,1.32,'wood_dark',.17,cap=False)
    for i,z in enumerate([.36,.77,1.14]):
        a.cylinder((-1.47,0,z), (1.47,0,z+.025*(i-1)), .071,'wood',5)
        for x in [-1.46,1.46]: a.box((x,-.085,z),(.065,.02,.10),'wood_dark')
    return finish(a)


def crossbuck_ranch_fence():
    a=asset('crossbuck_ranch_fence')
    for x in [-1.4,1.4]: post(a,x,1.28,'white',.15)
    rails(a,2.8,[.27,1.10],'white',.075,.12)
    a.beam((-1.32,-.04,.32),(1.32,-.04,1.06),.09,.05,'white')
    a.beam((-1.32,.025,1.06),(1.32,.025,.32),.09,.05,'white')
    return finish(a)


def ranch_wire_fence():
    a=asset('ranch_wire_fence')
    for x in [-1.5,1.5]: post(a,x,1.22,'wood_dark',.14,cap=False)
    rails(a,3,[1.10],'wood',.07,.14)
    meshgrid(a,2.95,.98,.12,.28,-.03,'steel',.007)
    return finish(a)


def cedar_lattice_top_fence():
    a=asset('cedar_lattice_top_fence')
    for x in [-1.2,1.2]: post(a,x,1.93)
    for i in range(15): picket(a,-1.12+i*.16,.10,1.35,.152,'wood',style='flat')
    rails(a,2.4,[.20,1.35,1.85],'wood_dark',.085,.08)
    diamond(a,2.28,1.81,1.39,-.012,.22,'wood_light',.019)
    return finish(a)


def scalloped_vinyl_fence():
    a=asset('scalloped_vinyl_fence')
    for x in [-1.2,1.2]: post(a,x,1.20,'white',.13)
    rails(a,2.4,[.27,.73],'white',.07,.085)
    for i in range(13):
        x=-1.1+i*2.2/12; h=.91+.25*(x/1.1)**2
        picket(a,x,.1,h,.105,'white',style='flat')
        a.box((x,-.04,h+.012),(.12,.06,.025),'white')
    return finish(a)


def tongue_groove_vinyl_fence():
    a=asset('tongue_groove_vinyl_fence')
    for x in [-1.2,1.2]: post(a,x,1.9,'cream',.14)
    for i in range(13): a.box((-1.10+i*2.2/12,0,.95),(.178,.065,1.54),'white')
    rails(a,2.35,[.17,1.73],'cream',.115,.12)
    return finish(a)


def aluminum_spear_fence():
    a=asset('aluminum_spear_fence')
    for x in [-1.2,1.2]: post(a,x,1.55,'dark_metal',.075)
    iron_infill(a,2.3,1.43,.10,13,True)
    rails(a,2.3,[1.12],'dark_metal',.045,.035)
    return finish(a)


def flat_top_pool_fence():
    a=asset('flat_top_pool_fence')
    for x in [-1.2,1.2]: post(a,x,1.35,'dark_metal',.07)
    rails(a,2.4,[.12,1.31],'dark_metal',.047,.055)
    for i in range(18): a.box((-1.10+i*2.20/17,0,.715),(.022,.022,1.15),'dark_metal')
    return finish(a)


def ornamental_iron_fence():
    a=asset('ornamental_iron_fence')
    for x in [-1.25,1.25]: post(a,x,1.65,'dark_metal',.085)
    iron_infill(a,2.4,1.50,.1,13,True)
    rails(a,2.4,[1.12],'dark_metal',.037,.037)
    for i in range(6):
        x=-1.0+i*.40
        a.torus((x,0,1.23),.095,.014,'dark_metal',axis='y',segments=10,sides=4)
    return finish(a)


def residential_chainlink_fence():
    a=asset('residential_chainlink_fence')
    for x in [-1.3,1.3]: pipepost(a,x,1.28)
    rod(a,(-1.3,0,1.24),(1.3,0,1.24),.023,'steel')
    rod(a,(-1.3,0,.12),(1.3,0,.12),.009,'steel',4)
    diamond(a,2.53,1.2,.12,spacing=.21)
    for x in [-1.24,1.24]: rod(a,(x,-.018,.12),(x,-.018,1.22),.012,'steel',4)
    return finish(a)


def security_chainlink_fence():
    a=asset('security_chainlink_fence',True)
    for x in [-1.5,1.5]:
        pipepost(a,x,2.08)
        rod(a,(x,0,2.05),(x,-.30,2.39),.024,'steel')
    rod(a,(-1.5,0,2.04),(1.5,0,2.04),.026,'steel')
    diamond(a,2.93,2.0,.10,spacing=.24)
    for f in [.30,.65,1.0]:
        rod(a,(-1.5,-.30*f,2.05+.34*f),(1.5,-.30*f,2.05+.34*f),.008,'steel',4)
    return finish(a)


def welded_mesh_security_fence():
    a=asset('welded_mesh_security_fence')
    for x in [-1.3,1.3]: post(a,x,1.86,'green',.065)
    meshgrid(a,2.52,1.81,.10,.19,0,'green',.009)
    for z in [.45,1.38]:
        rod(a,(-1.26,-.055,z),(1.26,-.055,z),.011,'green',4)
        for x in [-1.22,1.22]: a.box((x,0,z),(.10,.055,.06),'dark_metal')
    return finish(a)


def corrugated_panel(a,w,h,z,y=0):
    points=[];waves=max(5,round(w/.24))
    for i in range(waves):
        for f,offset in ((0,-.024),(.22,-.024),(.50,.024),(.72,.024)):
            points.append((-w/2+(i+f)*w/waves,y+offset))
    points.append((w/2,y-.024))
    outline=points+[(x,yy+.008) for x,yy in reversed(points)]
    a.prism(outline,z-h/2,z+h/2,'metal')
    for zz in (z-h*.38,z+h*.38):
        for i in range(waves):
            x=-w/2+(i+.62)*w/waves
            rod(a,(x,y-.03,zz),(x,y-.044,zz),.009,'steel',6)

def corrugated_metal_boundary():
    a=asset('corrugated_metal_boundary')
    for x in [-1.2,1.2]: post(a,x,1.9,'dark_metal',.075)
    rails(a,2.4,[.16,.94,1.73],'dark_metal',.055,.07,.09)
    corrugated_panel(a,2.37,1.65,.95)
    rails(a,2.4,[1.80],'metal',.12,.05)
    return finish(a)


def capped_brick_boundary_wall():
    a=asset('capped_brick_boundary_wall')
    brickwork(a,2.8,1.10)
    for x in [-1.45,1.45]:
        a.box((x,0,.65),(.38,.40,1.30),'brick')
        for z in [.20,.42,.64,.86,1.08]: a.box((x,-.205,z),(.385,.018,.024),'sand')
        a.box((x,0,1.34),(.46,.48,.08),'concrete_light')
    return finish(a)


def dry_stone_boundary_wall():
    a=asset('dry_stone_boundary_wall')
    for j in range(4):
        for i in range(7):
            x=-1.35+(i+.5)*.39+(.09 if j%2 else -.03)
            poly(a,[(x-.19,j*.22+.02),(x+.19,j*.22),(x+.20,j*.22+.16),(x+.07,j*.22+.24),(x-.16,j*.22+.20)],0,.42-.035*j,'concrete' if (i+j)%3 else 'sand')
    for i in range(8): a.box((-1.30+i*.375,0,.94),(.35,.44,.10),'concrete_light',rot=(0,.06*(-1)**i,0))
    return finish(a)


def concrete_block_boundary_wall():
    a=asset('concrete_block_boundary_wall')
    brickwork(a,2.8,1.25,.30,mat='concrete',course=.25)
    for x in [-1.5,1.5]:
        a.box((x,0,.70),(.33,.34,1.4),'concrete')
        a.box((x,0,1.43),(.40,.41,.08),'concrete_light')
    a.box((0,0,.045),(3.30,.48,.09),'concrete')
    return finish(a)


def gabion_boundary_wall():
    a=asset('gabion_boundary_wall')
    # Large faceted stones inside a genuinely open, two-sided cage.
    for k in range(2):
        for j in range(3):
            for i in range(7):
                a.sphere((-1.10+i*.365+(.04 if j%2 else 0),-.15+k*.30,.15+j*.29),.19,'concrete' if (i+j+k)%3 else 'sand',segments=5,rings=3,scale=(.20,.18,.18))
    for y in [-.34,.34]:
        meshgrid(a,2.65,.98,.03,.30,y,'dark_metal',.011)
        for x in [-1.34,1.34]: rod(a,(x,y,.025),(x,y,1.0),.018,'dark_metal',4)
        for z in [.025,1.0]: rod(a,(-1.34,y,z),(1.34,y,z),.017,'dark_metal',4)
    for x in [-1.34,-.67,0,.67,1.34]:
        for z in [.025,1.0]: rod(a,(x,-.34,z),(x,.34,z),.012,'dark_metal',4)
    return finish(a)


def retaining_wall_corner():
    a=asset('retaining_wall_corner')
    for j in range(4):
        for i in range(5): a.box((-1.2+i*.48,.04*j,j*.22+.11),(.465,.36,.205),'concrete')
        for i in range(1,4): a.box((-1.2+.04*j,i*.48,j*.22+.11),(.36,.465,.205),'concrete')
    a.box((-.24,.12,.92),(2.46,.44,.09),'concrete_light')
    a.box((-1.08,.97,.92),(.44,1.76,.09),'concrete_light')
    return finish(a)


def precast_concrete_fence():
    a=asset('precast_concrete_fence')
    for x in [-1.3,1.3]:
        post(a,x,1.92,'concrete',.19,cap=False)
        a.box((x,0,1.95),(.23,.23,.09),'concrete_light')
    for i in range(5):
        a.box((0,0,.22+i*.34),(2.55,.13,.32),'concrete_light')
        a.box((0,-.075,.22+i*.34),(2.32,.025,.20),'concrete')
    return finish(a)


def picket_garden_gate():
    a=asset('picket_garden_gate'); w=1.06
    for x in [-.67,.67]: post(a,x,1.22,'wood_dark',.13)
    wood_frame(a,w,.93,brace=True)
    for i in range(7): picket(a,-.45+i*.15,.10,1.14,.115)
    hardware(a,w,1.05,strap=True)
    return finish(a)


def stockade_service_gate():
    a=asset('stockade_service_gate'); w=1.12
    for x in [-.72,.72]: post(a,x,1.90,'wood_dark',.14)
    wood_frame(a,w,1.62,brace=True,y=.055)
    for i in range(8): picket(a,-.49+i*.14,.10,1.81,.136,'wood',style='dog')
    hardware(a,w,1.80,strap=True)
    a.box((.46,-.14,1.17),(.10,.07,.035),'steel')
    return finish(a)


def double_crossbuck_driveway_gate():
    a=asset('double_crossbuck_driveway_gate',True)
    for x in [-2.08,2.08]: post(a,x,1.33,'white',.18)
    for side in [-1,1]:
        c=side*1.0; w=1.88
        for z in [.28,1.10]: a.box((c,0,z),(w,.07,.13),'white')
        for x in [c-w/2,c+w/2]: a.box((x,0,.69),(.12,.09,.95),'white')
        a.beam((c-w/2,-.02,.31),(c+w/2,-.02,1.07),.085,.05,'white')
        a.beam((c-w/2,.04,1.07),(c+w/2,.04,.31),.085,.05,'white')
        for z in [.30,1.05]: rod(a,(side*1.96,-.08,z-.07),(side*1.96,-.08,z+.07),.035,'dark_metal')
    a.box((0,-.085,.91),(.30,.05,.05),'dark_metal')
    rod(a,(.09,-.07,.04),(.09,-.07,.54),.015,'dark_metal')
    return finish(a)


def split_rail_field_gate():
    a=asset('split_rail_field_gate')
    for x in [-1.45,1.45]: post(a,x,1.40,'wood_dark',.19,cap=False)
    for x in [-1.28,1.28]: a.box((x,0,.70),(.11,.09,1.12),'wood')
    for z in [.24,.58,.92,1.22]: a.box((0,0,z),(2.62,.07,.095),'wood')
    a.beam((-1.25,.06,.27),(1.25,.06,1.19),.10,.04,'wood_dark')
    hardware(a,2.62,1.26,strap=True)
    return finish(a)


def vinyl_pedestrian_gate():
    a=asset('vinyl_pedestrian_gate')
    for x in [-.68,.68]: post(a,x,1.35,'white',.14)
    wood_frame(a,1.04,1.12,'white')
    for i in range(6):
        x=-.425+i*.17
        picket(a,x,.13,1.19+.13*(1-(x/.5)**2),.11,'white',style='flat')
    hardware(a,1.04,1.25,'dark_metal')
    return finish(a)


def arched_wrought_iron_gate():
    a=asset('arched_wrought_iron_gate')
    for x in [-.76,.76]: post(a,x,1.84,'dark_metal',.11)
    for x in [-.61,.61]: rod(a,(x,0,.13),(x,0,1.62),.03)
    rod(a,(-.61,0,.13),(.61,0,.13),.03)
    pts=[(-.61+i*1.22/8,0,1.60+.28*math.sin(math.pi*i/8)) for i in range(9)]
    a.tube(pts,.027,'dark_metal',6)
    for i in range(8):
        x=-.535+i*1.07/7; h=1.6+.28*math.cos(math.pi*x/1.22)
        rod(a,(x,0,.16),(x,0,h),.014)
    for x in [-.30,.30]: a.torus((x,0,.84),.20,.017,'dark_metal',axis='y',segments=12,sides=4)
    hardware(a,1.22,1.61)
    return finish(a)


def self_closing_pool_gate():
    a=asset('self_closing_pool_gate')
    for x in [-.66,.66]: post(a,x,1.4,'dark_metal',.075)
    metal_frame(a,1.05,1.34)
    for i in range(8): a.box((-.445+i*.127,0,.73),(.022,.022,1.19),'dark_metal')
    hardware(a,1.05,1.30)
    rod(a,(-.57,-.06,.36),(-.57,-.06,.58),.05,'dark_metal')
    a.box((.57,-.07,1.48),(.065,.06,.19),'dark_metal')
    a.box((.57,-.07,1.59),(.10,.075,.04),'black')
    return finish(a)


def aluminum_double_drive_gate():
    a=asset('aluminum_double_drive_gate',True)
    for x in [-2.2,2.2]: post(a,x,1.74,'dark_metal',.13)
    for side in [-1,1]:
        c=side*1.06
        for x in [c-1,c+1]: a.box((x,0,.86),(.06,.06,1.45),'dark_metal')
        for z in [.15,1.34,1.55]: a.box((c,0,z),(2.03,.05,.055),'dark_metal')
        for i in range(11):
            x=c-.90+i*.18
            a.box((x,0,.89),(.028,.028,1.49),'dark_metal')
            poly(a,[(x-.04,1.62),(x,1.76),(x+.04,1.62)],0,.026,'dark_metal')
        for z in [.34,1.32]: rod(a,(side*2.08,-.05,z-.08),(side*2.08,-.05,z+.08),.035)
    a.box((0,-.07,.95),(.20,.05,.055),'dark_metal')
    rod(a,(.10,0,.02),(.10,0,.66),.014)
    return finish(a)


def chainlink_walk_gate():
    a=asset('chainlink_walk_gate')
    for x in [-.72,.72]: pipepost(a,x,1.57)
    metal_frame(a,1.20,1.5,mat='steel')
    diamond(a,1.14,1.46,.16,spacing=.21)
    hardware(a,1.20,1.47,'steel')
    a.box((.68,-.02,.89),(.09,.08,.19),'steel')
    return finish(a)


def chainlink_double_vehicle_gate():
    a=asset('chainlink_double_vehicle_gate',True)
    for x in [-2.15,2.15]: pipepost(a,x,1.90,r=.063)
    for side in [-1,1]:
        b=Asset('temporary')
        metal_frame(b,1.98,1.81,mat='steel')
        diamond(b,1.92,1.76,.17,spacing=.245)
        b.beam((-.94,.03,.19),(.94,.03,1.75),.025,.025,'steel')
        b.translate((side*1.035,0,0)); a.mesh(b.vertices,b.faces,b.face_materials)
        for z in [.35,1.55]: rod(a,(side*2.05,-.04,z-.075),(side*2.05,-.04,z+.075),.037,'steel')
    rod(a,(.07,-.05,.01),(.07,-.05,.75),.016,'steel')
    a.box((0,-.045,.98),(.26,.04,.05),'steel')
    return finish(a)


def cantilever_security_slide_gate():
    a=asset('cantilever_security_slide_gate',True)
    for x in [-2.30,-1.35,2.30]: pipepost(a,x,2.13,r=.065)
    metal_frame(a,4.35,2.06,.23,'steel')
    diamond(a,4.25,2.0,.28,spacing=.28)
    for x in [-.72,.72]: rod(a,(x,0,.23),(x,0,2.06),.035,'steel')
    for x in [-2.3,-1.35]:
        for z in [.38,1.88]:
            a.box((x,.04,z),(.22,.22,.10),'dark_metal')
            a.cylinder((x,-.10,z),(x,-.20,z),.083,'rubber',8)
    a.box((-1.7,.27,.20),(.44,.32,.4),'dark_metal')
    a.box((-1.7,.095,.21),(.36,.025,.29),'metal')
    for xx in (-1.86,-1.54):rod(a,(xx,.078,.21),(xx,.066,.21),.01,'steel',6)
    for xx in [-1.9+i*.10 for i in range(39)]:a.box((xx,-.062,.34),(.033,.032,.064),'metal')
    a.box((0,-.044,.33),(4.40,.035,.038),'dark_metal')
    return finish(a)


def welded_mesh_industrial_gate():
    a=asset('welded_mesh_industrial_gate')
    for x in [-.91,.91]: post(a,x,2.08,'green',.10)
    metal_frame(a,1.56,1.98,.14,'green',r=.038)
    meshgrid(a,1.48,1.91,.21,.18,0,'green',.009)
    rails(a,1.56,[1.03],'green',.06,.07)
    a.box((.60,-.045,1.02),(.25,.045,.33),'green')
    hardware(a,1.56,1.95)
    return finish(a)


def sliding_timber_driveway_gate():
    a=asset('sliding_timber_driveway_gate',True)
    for x in [-2.13,2.13]: post(a,x,1.86,'dark_metal',.12)
    a.box((0,0,.055),(4.75,.045,.04),'steel')
    wood_frame(a,3.95,1.6,'dark_metal',y=.035)
    for i in range(10): a.box((0,-.045,.30+i*.145),(3.88,.06,.115),'wood')
    for x in [-1.45,1.45]:
        a.cylinder((x,-.07,.12),(x,.07,.12),.095,'dark_metal',10)
        a.box((x,0,.22),(.18,.14,.11),'dark_metal')
    a.box((-2.20,.25,.20),(.32,.35,.40),'dark_metal')
    a.box((-2.20,.06,.21),(.26,.025,.30),'metal')
    a.box((0,.065,.24),(4.03,.035,.043),'metal')
    for xx in [-1.85+i*.10 for i in range(38)]:a.box((xx,.072,.25),(.026,.040,.057),'dark_metal')
    rod(a,(1.72,-.13,.74),(1.72,-.13,1.02),.019,'steel')
    return finish(a)


def corrugated_utility_yard_gate():
    a=asset('corrugated_utility_yard_gate')
    for x in [-.89,.89]: post(a,x,1.93,'dark_metal',.105)
    wood_frame(a,1.50,1.67,'dark_metal',brace=True,y=.09)
    corrugated_panel(a,1.48,1.68,.99)
    rails(a,1.54,[.14,1.84],'dark_metal',.10,.055)
    hardware(a,1.50,1.83,strap=True)
    a.box((.48,-.10,1.1),(.20,.04,.20),'dark_metal')
    return finish(a)


def lattice_trellis_gate():
    a=asset('lattice_trellis_gate')
    for x in [-.79,.79]: post(a,x,1.86,'wood_dark',.14)
    wood_frame(a,1.26,1.63,'wood_dark')
    diamond(a,1.15,1.58,.24,-.03,.22,'wood_light',.024)
    rails(a,1.3,[.19,1.70],'wood',.09,.09)
    hardware(a,1.26,1.73,strap=True)
    return finish(a)


def brick_pier_garden_gate():
    a=asset('brick_pier_garden_gate')
    for x in [-.93,.93]:
        brickwork(a,.45,1.44,.43,x0=x)
        a.box((x,0,1.53),(.54,.53,.10),'concrete_light')
    metal_frame(a,1.28,1.25,r=.025)
    iron_infill(a,1.22,1.23,.14,7,True)
    for x in [-.38,0,.38]: a.torus((x,0,.68),.11,.016,'dark_metal',axis='y',segments=10,sides=4)
    hardware(a,1.28,1.3)
    return finish(a)


def stone_pier_driveway_entry():
    a=asset('stone_pier_driveway_entry',True)
    for x in [-2.08,2.08]:
        for j in range(6):
            a.box((x+(.015 if j%2 else -.015),0,.14+j*.27),(.48,.50,.255),'concrete' if j%2 else 'sand')
            a.box((x,-.258,.14+j*.27),(.025,.02,.255),'concrete_light')
        a.box((x,0,1.67),(.62,.64,.11),'concrete_light')
        a.sphere((x,0,1.84),.14,'concrete_light',segments=8,rings=4)
    for side in [-1,1]:
        c=side*.91
        for z in [.18,.40,1.43]: a.box((c,0,z),(1.71,.045,.055),'dark_metal')
        for i in range(9):
            x=c-.76+i*.19; top=1.42+.2*(1-abs(x)/1.72)
            rod(a,(x,0,.18),(x,0,top),.019)
            a.cone((x,0,top),(x,0,top+.10),.038,'dark_metal',4)
        for z in [.35,1.26]: rod(a,(side*1.79,-.05,z-.07),(side*1.79,-.05,z+.07),.036)
    a.box((0,-.05,.94),(.25,.045,.065),'dark_metal')
    return finish(a)


def accordion_industrial_gate():
    a=asset('accordion_industrial_gate',True)
    for x in [-2.0,2.0]: post(a,x,1.74,'dark_metal',.10)
    for z in [.20,1.53]: rod(a,(-1.91,0,z),(1.91,0,z),.023,'steel')
    for i in range(10):
        x=-1.90+i*.38
        a.beam((x,-.03,.20),(x+.38,-.03,1.53),.035,.025,'metal')
        a.beam((x,.03,1.53),(x+.38,.03,.20),.035,.025,'metal')
        rod(a,(x+.19,-.055,.865),(x+.19,.055,.865),.033,'steel',8)
    for x in [-1.90,0,1.90]:
        a.box((x,0,.16),(.10,.15,.12),'metal')
        a.cylinder((x,-.08,.085),(x,.08,.085),.065,'rubber',8)
    a.box((1.82,-.10,.92),(.12,.045,.19),'dark_metal')
    return finish(a)


def tubular_field_gate():
    a=asset('tubular_field_gate')
    for x in [-1.56,1.56]: post(a,x,1.39,'wood_dark',.19,cap=False)
    metal_frame(a,2.80,1.25,.20,'red',r=.039)
    for z in [.43,.67,.91]: rod(a,(-1.40,0,z),(1.40,0,z),.027,'red')
    for x in [-.49,.49]: rod(a,(x,0,.20),(x,0,1.25),.024,'red')
    hardware(a,2.80,1.23,'steel')
    a.torus((1.47,-.04,.85),.10,.014,'steel',axis='y',segments=10,sides=4,arc=math.pi*1.5)
    return finish(a)


def geometric_metal_screen_gate():
    a=asset('geometric_metal_screen_gate')
    for x in [-.77,.77]: post(a,x,1.92,'dark_metal',.09)
    wood_frame(a,1.30,1.73,'dark_metal')
    # Distinct open asymmetrical rectangles are built from stock, with no plane.
    for x,z,w,h in [(-.29,.57,.56,.73),(.31,.44,.44,.43),(.31,1.13,.44,.86),(-.28,1.43,.58,.52)]:
        for xx in [x-w/2,x+w/2]: a.box((xx,0,z),(.038,.04,h),'metal')
        for zz in [z-h/2,z+h/2]: a.box((x,0,zz),(w,.04,.038),'metal')
    hardware(a,1.30,1.82)
    return finish(a)


def cedar_fence_inside_corner():
    a=asset('cedar_fence_inside_corner')
    for x,y in [(-1.15,0),(1.15,0),(-1.15,1.65)]: post(a,x,1.50,'wood_dark',.13,y=y)
    rails(a,2.3,[.30,1.27],'wood_dark')
    for i in range(13): picket(a,-1.06+i*.175,.11,1.43,.14,'wood',style='dog')
    for z in [.30,1.27]: a.box((-1.15,.825,z),(.07,1.65,.1),'wood_dark')
    for i in range(9): a.box((-1.19,.12+i*.17,.77),(.045,.145,1.32),'wood')
    return finish(a)


def stepped_block_retaining_wall():
    a=asset('stepped_block_retaining_wall',True)
    for col in range(3):
        height=col+2; xc=-1.2+1.2*col
        for j in range(height):
            for i in range(3): a.box((xc-.4+i*.4,.025*j,j*.22+.11),(.385,.38,.205),'concrete')
        a.box((xc,.025*(height-1),height*.22+.045),(1.22,.47,.09),'concrete_light')
    return finish(a)


def timber_post_cable_boundary():
    a=asset('timber_post_cable_boundary')
    for x in [-1.5,0,1.5]:
        post(a,x,1.17,'wood_dark',.14,cap=False)
        for z in [.25,.49,.73,.97]:
            rod(a,(x-.1,0,z),(x+.1,0,z),.024,'steel',6)
    for z in [.25,.49,.73,.97]: rod(a,(-1.52,0,z),(1.52,0,z),.010,'steel',4)
    a.box((0,0,1.19),(3.17,.19,.075),'wood')
    return finish(a)


def garden_boundary_trellis():
    a=asset('garden_boundary_trellis')
    for x in [-1.22,1.22]: post(a,x,2.08,'wood_dark',.11)
    for z in [.17,1.95]: a.box((0,0,z),(2.44,.09,.09),'wood_dark')
    for i in range(9): a.box((-1.08+i*.27,-.025,1.05),(.037,.04,1.77),'wood_light')
    for i in range(7): a.box((0,.019,.28+i*.26),(2.24,.04,.04),'wood')
    for x in [-1.22,1.22]:
        a.box((x,0,.15),(.16,.18,.30),'dark_metal')
        for z in [.075,.21]: rod(a,(x,-.095,z),(x,-.117,z),.025,'steel',6)
    return finish(a)


def timber_sleeper_retaining_wall():
    a=asset('timber_sleeper_retaining_wall')
    for j in range(4):
        a.box((0,j*.035,.115+j*.21),(2.8,.24,.20),'wood_dark')
        for x in [-1.13,1.13]: rod(a,(x,-.129+j*.035,.115+j*.21),(x,-.15+j*.035,.115+j*.21),.022,'black',6)
    for x in [-1.16,1.16]:
        a.box((x,.28,.44),(.17,.17,.88),'wood')
        a.box((x,.68,.13),(.17,1.02,.22),'wood_dark')
    a.box((0,.04,.88),(2.92,.40,.10),'wood')
    return finish(a)


_FACTORIES = [
    gothic_picket_fence, dogear_stockade_fence, shadowbox_privacy_fence,
    board_batten_fence, horizontal_cedar_slat_fence, basketweave_timber_fence,
    split_rail_fence, crossbuck_ranch_fence, ranch_wire_fence,
    cedar_lattice_top_fence, scalloped_vinyl_fence, tongue_groove_vinyl_fence,
    aluminum_spear_fence, flat_top_pool_fence, ornamental_iron_fence,
    residential_chainlink_fence, security_chainlink_fence,
    welded_mesh_security_fence, corrugated_metal_boundary,
    capped_brick_boundary_wall, dry_stone_boundary_wall,
    concrete_block_boundary_wall, gabion_boundary_wall, retaining_wall_corner,
    precast_concrete_fence, picket_garden_gate, stockade_service_gate,
    double_crossbuck_driveway_gate, split_rail_field_gate, vinyl_pedestrian_gate,
    arched_wrought_iron_gate, self_closing_pool_gate, aluminum_double_drive_gate,
    chainlink_walk_gate, chainlink_double_vehicle_gate,
    cantilever_security_slide_gate, welded_mesh_industrial_gate,
    sliding_timber_driveway_gate, corrugated_utility_yard_gate,
    lattice_trellis_gate, brick_pier_garden_gate, stone_pier_driveway_entry,
    accordion_industrial_gate, tubular_field_gate, geometric_metal_screen_gate,
    cedar_fence_inside_corner, stepped_block_retaining_wall,
    timber_post_cable_boundary, garden_boundary_trellis,
    timber_sleeper_retaining_wall,
]
for _fn in _FACTORIES:
    _a = _fn()
    register(_a.name, CAT, _a.size_class, _fn)

