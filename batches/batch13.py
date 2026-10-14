"""Fifty original road, pedestrian-access and urban transit modules.

Pavements are modelled as usable construction sections, with real joints,
curb profiles, tactile surfaces and rail hardware rather than texture decals.
Integral handrails belong to the bridges and stairs, never standalone fences.
"""
import math
from assetlib import Asset, register

C='concrete'; L='concrete_light'; M='dark_metal'; S='steel'
Y='yellow'; A='asphalt'; W='wood_dark'; B='brick'

def box(a,p,s,m=C): a.box(p,s,m)
def beam(a,p,q,w=.06,d=None,m=M): a.beam(p,q,w,d,m)
def rod(a,p,q,r=.024,m=S,n=8): a.cylinder(p,q,r,m,n)
def slab(a,w,d,h=.15,z=0,m=C): box(a,(0,0,z+h/2),(w,d,h),m)
def slope(a,x0,x1,y0,y1,h0,h1,base=0,m=C):
    # CCW rectangular prism with a genuinely sloping, planar top.
    v=[(x0,y0,base),(x1,y0,base),(x1,y1,base),(x0,y1,base),
       (x0,y0,h0),(x1,y0,h0),(x1,y1,h1),(x0,y1,h1)]
    a.mesh(v,[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],m)
def tactile(a,x,y,z,w=1.0,d=.55,mat=Y):
    box(a,(x,y,z+.012),(w,d,.024),mat)
    nx=max(2,int(w/.105)); ny=max(2,int(d/.105))
    for i in range(nx):
        for j in range(ny):
            px=x-w/2+(i+.5)*w/nx; py=y-d/2+(j+.5)*d/ny
            a.cylinder((px,py,z+.024),(px,py,z+.034),.025,mat,6,radius2=.018)
def joints(a,w,d,z,nx=2,ny=2,m=M):
    for i in range(1,nx): box(a,(-w/2+w*i/nx,0,z+.001),( .009,d,.002),m)
    for j in range(1,ny): box(a,(0,-d/2+d*j/ny,z+.001),(w,.009,.002),m)
def curb(a,x,y,length=2.0,z=0,mat=L):
    # Chamfered 150 mm exposed curb, 180 mm wide.
    pts=[(y-.10,z),(y+.10,z),(y+.10,z+.22),(y-.055,z+.22),(y-.10,z+.175)]
    v=[(xx,yy,zz) for xx in (x-length/2,x+length/2) for yy,zz in pts]
    n=len(pts); fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    fs += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    a.mesh(v,fs,mat)
def curved_band(a,cx,cy,r0,r1,t0,t1,z0,z1,segments=10,mat=C):
    for i in range(segments):
        t=t0+(t1-t0)*i/segments; u=t0+(t1-t0)*(i+1)/segments
        a.prism([(cx+r0*math.cos(t),cy+r0*math.sin(t)),
                 (cx+r1*math.cos(t),cy+r1*math.sin(t)),
                 (cx+r1*math.cos(u),cy+r1*math.sin(u)),
                 (cx+r0*math.cos(u),cy+r0*math.sin(u))],z0,z1,mat)
def handrail(a,pts,posts=True,m=S):
    top=[(x,y,z+.98) for x,y,z in pts]
    a.tube(top,.025,m,8)
    a.tube([(x,y,z+.48) for x,y,z in pts],.018,m,6)
    if posts:
        for x,y,z in pts:
            rod(a,(x,y,z),(x,y,z+.99),.025,m)
            box(a,(x,y,z+.012),(.11,.11,.025),m)
def stair(a,width=1.7,n=7,run=.28,rise=.17,x=0,y=0,z=0,m=C,nosing=True):
    for i in range(n):
        cy=y+(i+.5)*run; h=(i+1)*rise
        box(a,(x,cy,z+h/2),(width,run,h),m)
        if nosing: box(a,(x,y+i*run+.023,z+h+.002),(width-.05,.046,.006),Y)
def rail(a,pts):
    # Three separate sections reproduce a standard rail's head, web and foot.
    for p,q in zip(pts,pts[1:]):
        for dz,w,h,mat in ((.028,.14,.04,M),(.083,.044,.105,M),(.145,.074,.042,S)):
            beam(a,(p[0],p[1],p[2]+dz),(q[0],q[1],q[2]+dz),w,h,mat)
def ties(a,length=3.6,gauge=1.435,z=.10,mat=W,count=7):
    for i in range(count):
        y=-length/2+(i+.5)*length/count
        box(a,(0,y,z+.08),(gauge+.85,.21,.16),mat)
        for x in (-gauge/2,gauge/2):
            box(a,(x,y,z+.172),(.24,.23,.024),M)
            for dx in (-.083,.083):
                box(a,(x+dx,y,z+.199),(.045,.07,.03),S)
def new(name,cat='pedestrian_infrastructure',size='large'):
    return Asset('b13_'+name,cat,size)
def finish(a): return a.bottom_center()

def b13_scored_concrete_sidewalk_bay():
    a=new('scored_concrete_sidewalk_bay'); slab(a,2.5,3.4,.15)
    joints(a,2.5,3.4,.15,2,3)
    curb(a,0,-1.58,2.5,0)
    box(a,(0,-1.46,.153),(2.46,.06,.008),L)
    return finish(a)

def b13_radius_sidewalk_corner():
    a=new('radius_sidewalk_corner')
    a.prism([(0,0),(2.15,0)]+[(2.15*math.cos(i*math.pi/20),2.15*math.sin(i*math.pi/20)) for i in range(1,11)],0,.17,C)
    curved_band(a,0,0,2.13,2.32,0,math.pi/2,0,.24,10,L)
    for th in (math.pi/6,math.pi/3): beam(a,(.45*math.cos(th),.45*math.sin(th),.174),(2.1*math.cos(th),2.1*math.sin(th),.174),.008,.006,M)
    return finish(a)

def b13_reentrant_sidewalk_corner():
    a=new('reentrant_sidewalk_corner')
    for x,y,w,d in ((0,-.75,3,1.5),(-.75,.75,1.5,1.5)):
        box(a,(x,y,.085),(w,d,.17),C)
    curb(a,.75,.08,1.5)
    for i in range(3):
        box(a,(-.08,.25+i*.5,.11),(.20,.49,.22),L)
    joints(a,3,1.5,.17,3,1)
    return finish(a)

def b13_flared_accessible_curb_ramp():
    a=new('flared_accessible_curb_ramp')
    slope(a,-.75,.75,-.85,.85,.035,.21)
    # Side flares are full-volume wedges rising laterally toward the sidewalk.
    for s in (-1,1):
        x0=.75*s; x1=1.6*s
        v=[(x0,-.85,0),(x1,-.85,0),(x1,.85,0),(x0,.85,0),
           (x0,-.85,.035),(x1,-.85,.21),(x1,.85,.21),(x0,.85,.21)]
        fs=[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6),(4,6,7)]
        a.mesh(v,fs if s>0 else [tuple(reversed(f)) for f in fs],C)
    tactile(a,0,-.60,.062,1.35,.4)
    box(a,(0,.99,.105),(3.2,.28,.21),C)
    return finish(a)

def b13_dual_direction_corner_ramps():
    a=new('dual_direction_corner_ramps')
    slab(a,1.7,1.7,.22)
    slope(a,-.75,.75,-2.1,-.85,.035,.22)
    tactile(a,0,-1.85,.072,1.3,.32)
    # Perpendicular branch assembled in its own coordinates then rotated.
    b=Asset('branch'); slope(b,-.75,.75,-2.1,-.85,.035,.22);tactile(b,0,-1.85,.072,1.3,.32)
    b.rotate(math.pi/2); a.mesh(b.vertices,b.faces,b.face_materials)
    curb(a,0,.81,1.7)
    box(a,(-.80,0,.12),(.15,1.7,.24),L)
    joints(a,1.55,1.55,.22,2,2)
    return finish(a)

def b13_parallel_depressed_curb_ramp():
    a=new('parallel_depressed_curb_ramp')
    box(a,(0,0,.025),(1.45,1.4,.05),C)
    for s in (-1,1):
        b=Asset('slope'); slope(b,-.70,.70,0,1.6,.05,.23);b.rotate(s*math.pi/2);b.translate((-s*.725,0,0));a.mesh(b.vertices,b.faces,b.face_materials)
    tactile(a,0,-.48,.05,1.28,.38)
    box(a,(0,.76,.16),(4.65,.15,.32),L)
    return finish(a)

def b13_residential_driveway_apron():
    a=new('residential_driveway_apron','road_surface')
    slope(a,-1.8,1.8,-1.2,1.1,.025,.22)
    for x in (-.6,.6): beam(a,(x,-1.16,.031),(x,1.06,.22),.009,.006,M)
    for x in (-2.04,2.04): curb(a,x,.95,.45)
    box(a,(0,1.23,.11),(4.5,.26,.22),C)
    return finish(a)

def b13_reinforced_alley_sidewalk_crossover():
    a=new('reinforced_alley_sidewalk_crossover','road_surface')
    slab(a,4.2,2.5,.23);joints(a,4.2,2.5,.23,3,2)
    for y in (-1.1,1.1): box(a,(0,y,.237),(4.18,.12,.012),L)
    for x in (-2.0,2.0): box(a,(x,0,.255),(.16,2.5,.05),L)
    for i in range(7): box(a,(-1.8+i*.6,0,.232),(.05,1.9,.004),C)
    return finish(a)

def b13_truncated_dome_warning_panel():
    a=new('truncated_dome_warning_panel','accessible_paving','person')
    slab(a,1.22,.65,.06);tactile(a,0,0,.06,1.2,.63,'terracotta')
    for x in (-.56,.56):
        for y in (-.265,.265): rod(a,(x,y,.087),(x,y,.091),.015,M,6)
    return finish(a)

def b13_directional_ribbed_guidance_paving():
    a=new('directional_ribbed_guidance_paving','accessible_paving','person')
    slab(a,.72,1.6,.065,m=L)
    for x in (-.27,-.135,0,.135,.27):
        for y in (-.405,.405): box(a,(x,y,.077),(.056,.74,.024),'terracotta')
    box(a,(0,0,.066),(.71,.009,.003),M)
    return finish(a)

def b13_zebra_crossing_road_section():
    a=new('zebra_crossing_road_section','road_surface')
    slab(a,4.6,3.2,.14,0,A)
    for i in range(6): box(a,(-1.9+i*.76,0,.144),(.39,2.8,.008),'white')
    for y in (-1.51,1.51): box(a,(0,y,.08),(4.6,.15,.18),C)
    return finish(a)

def b13_ladder_crossing_road_section():
    a=new('ladder_crossing_road_section','road_surface')
    slab(a,4.5,2.8,.12,0,A)
    for y in (-1.12,1.12): box(a,(0,y,.125),(4.2,.16,.01),'white')
    for x in (-1.7,-.85,0,.85,1.7): box(a,(x,0,.125),(.36,2.09,.01),'white')
    box(a,(0,-1.34,.121),(4.45,.015,.003),M)
    return finish(a)

def b13_raised_pedestrian_crossing_table():
    a=new('raised_pedestrian_crossing_table','road_surface')
    slab(a,4.8,2.25,.26,0,C)
    slope(a,-2.4,2.4,-2.05,-1.125,.065,.26,0,A)
    slope(a,-2.4,2.4,1.125,2.05,.26,.065,0,A)
    for x in (-1.8,-.9,0,.9,1.8): box(a,(x,0,.264),(.44,1.95,.008),'white')
    for y in (-1.02,1.02): box(a,(0,y,.264),(4.78,.065,.008),L)
    return finish(a)

def b13_pedestrian_median_refuge_island():
    a=new('pedestrian_median_refuge_island')
    slab(a,2.0,4.4,.07,0,C)
    for s in (-1,1):
        pts=[(-1,s*.64),(1,s*.64),(1,s*1.65),(.48,s*2.2),(-.48,s*2.2),(-1,s*1.65)]
        if s<0:pts.reverse()
        a.prism(pts,.07,.25,L)
    for x in (-.68,.68): tactile(a,x,0,.07,.45,1.08)
    box(a,(0,0,.073),(.009,1.24,.006),M)
    return finish(a)

def b13_curb_extension_bulbout():
    a=new('curb_extension_bulbout')
    pts=[(-2,-1.1),(1.15,-1.1),(1.78,-.70),(2,-.1),(1.78,.70),(1.15,1.1),(-2,1.1)]
    a.prism(pts,0,.18,C)
    for p,q in zip(pts,pts[1:]): beam(a,(p[0],p[1],.19),(q[0],q[1],.19),.14,.12,L)
    for x in (-.8,.4):box(a,(x,0,.183),(.009,2.10,.006),M)
    return finish(a)

def b13_bus_bulb_boarding_pad():
    a=new('bus_bulb_boarding_pad','transit_platform')
    a.prism([(-2.6,-.9),(2.6,-.9),(2.6,.42),(1.95,1),(-1.95,1),(-2.6,.42)],0,.24,C)
    for i in range(5): curb(a,-2.08+i*1.04,-.87,1.02,.04)
    tactile(a,-1.5,-.45,.24,1.42,.45)
    box(a,(.76,.03,.243),(.012,1.74,.006),M)
    box(a,(-.39,.03,.243),(.012,1.74,.006),M)
    return finish(a)

def b13_cycletrack_driveway_crossing():
    a=new('cycletrack_driveway_crossing','road_surface')
    slab(a,3.8,3.6,.12,0,A)
    box(a,(0,0,.157),(1.62,3.6,.074),'green')
    for x in (-1.08,1.08):
        b=Asset('w');slope(b,-1.8,1.8,-.29,.29,.12,.194);b.rotate(math.pi/2 if x<0 else -math.pi/2);b.translate((x,0,0));a.mesh(b.vertices,b.faces,b.face_materials)
    for y in (-1.43,-.69,.05,.79,1.53):
        for x in (-.70,.70):box(a,(x,y,.198),(.055,.38,.008),'white')
    return finish(a)

def b13_raised_neighborhood_intersection():
    a=new('raised_neighborhood_intersection','road_surface')
    slab(a,4,4,.24,0,B);joints(a,4,4,.24,8,8)
    for rot in (0,math.pi/2,math.pi,3*math.pi/2):
        b=Asset('apron');slope(b,-2,2,-3,-2,.04,.24,0,A);b.rotate(rot);a.mesh(b.vertices,b.faces,b.face_materials)
    for x in (-1.8,1.8):box(a,(x,0,.245),(.09,3.6,.01),L)
    for y in (-1.8,1.8):box(a,(0,y,.245),(3.6,.09,.01),L)
    return finish(a)

def b13_crowned_cobblestone_alley():
    a=new('crowned_cobblestone_alley','road_surface')
    slab(a,2.8,3.3,.09,0,M)
    for j in range(11):
        for i in range(8):
            x=-1.225+i*.35; y=-1.5+j*.30
            z=.12+.055*(1-abs(x)/1.4)
            box(a,(x,y,z),(.33,.275,.10),C if (i+j)%3 else L)
    for x in (-1.42,1.42):box(a,(x,0,.135),(.12,3.3,.27),L)
    return finish(a)

def b13_basketweave_brick_sidewalk_panel():
    a=new('basketweave_brick_sidewalk_panel','pedestrian_infrastructure')
    slab(a,2.25,2.25,.09,0,'sand')
    for i in range(5):
        for j in range(5):
            x=-.8+i*.4;y=-.8+j*.4
            for s in (-1,1):
                if (i+j)%2:box(a,(x+s*.10,y,.112),(.185,.385,.044),B)
                else:box(a,(x,y+s*.10,.112),(.385,.185,.044),B)
    for x in (-1.07,1.07):box(a,(x,0,.12),(.11,2.25,.06),L)
    for y in (-1.07,1.07):box(a,(0,y,.12),(2.02,.11,.06),L)
    return finish(a)

def b13_granite_curb_sett_course():
    a=new('granite_curb_sett_course','curb','person')
    for i in range(3):
        curb(a,-.81+i*.81,0,.80,0,C)
        for j in range(3):box(a,(-1.09+i*.81+j*.27,-.29,.038),(.255,.32,.076),L)
    return finish(a)

def b13_rolled_concrete_gutter_curb():
    a=new('rolled_concrete_gutter_curb','curb','person')
    # Curved transverse apron section approximated with five planar strips.
    profile=[(-.48,.035),(-.25,.035),(-.10,.045),(.02,.10),(.11,.175),(.22,.195),(.36,.195)]
    for (y0,z0),(y1,z1) in zip(profile,profile[1:]):slope(a,-1.2,1.2,y0,y1,z0,z1,0,L)
    for x in (-.40,.40):box(a,(x,-.365,.037),(.006,.20,.004),M)
    return finish(a)

def b13_permeable_concrete_grid_paving():
    a=new('permeable_concrete_grid_paving','road_surface')
    slab(a,2.4,2.4,.09,0,'sand')
    for i in range(7):
        p=-1.2+i*.4
        box(a,(p,0,.13),(.074,2.4,.10),C)
        box(a,(0,p,.13),(2.4,.074,.10),C)
    for i in range(6):
        for j in range(6):box(a,(-1+i*.4,-1+j*.4,.104),(.29,.29,.03),'soil')
    return finish(a)

def b13_bridge_approach_settlement_slab():
    a=new('bridge_approach_settlement_slab','road_surface')
    slope(a,-2.5,2.5,-1.6,1.6,.16,.27,0,C)
    for x in (-2.37,2.37):
        beam(a,(x,-1.6,.27),(x,1.6,.38),.24,.22,L)
    for x in (-1.20,1.20):beam(a,(x,-1.53,.167),(x,1.53,.272),.012,.006,M)
    box(a,(0,1.47,.271),(4.72,.035,.007),M)
    for x in (-.06,.06):beam(a,(x,-1.55,.166),(x,1.4,.267),.045,.004,Y)
    return finish(a)

def b13_road_bridge_finger_expansion_joint():
    a=new('road_bridge_finger_expansion_joint','road_joint')
    for y in (-.46,.46):
        box(a,(0,y,.07),(3.6,.52,.14),C)
        box(a,(0,y*.74,.151),(3.6,.29,.04),S)
    box(a,(0,0,.09),(3.6,.54,.06),'rubber')
    for i in range(23):
        x=-1.65+i*.15;s=1 if i%2 else -1
        box(a,(x,s*.085,.156),(.097,.45,.05),S)
    for i in range(9):
        for y in (-.43,.43):rod(a,(-1.6+i*.4,y,.174),(-1.6+i*.4,y,.187),.023,M,6)
    return finish(a)

def b13_sidewalk_sliding_expansion_cover():
    a=new('sidewalk_sliding_expansion_cover','road_joint','person')
    for y in (-.25,.25): box(a,(0,y,.055),(1.8,.31,.11),C)
    box(a,(0,0,.119),(1.8,.31,.035),S)
    for i in range(15):box(a,(-.84+i*.12,0,.14),(.034,.25,.014),M)
    for x in (-.77,0,.77):
        for y in (-.12,.12):rod(a,(x,y,.138),(x,y,.148),.016,S,6)
    return finish(a)

def b13_embedded_grooved_streetcar_track():
    a=new('embedded_grooved_streetcar_track','rail_track')
    slab(a,2.7,3.6,.13,0,C);joints(a,2.7,3.6,.13,2,3)
    for x in (-.7175,.7175):
        box(a,(x,0,.132),(.19,3.6,.024),M)
        box(a,(x-.04,0,.15),(.065,3.6,.034),S)
        box(a,(x+.053,0,.15),(.03,3.6,.034),S)
    return finish(a)

def b13_curved_streetcar_track_segment():
    a=new('curved_streetcar_track_segment','rail_track')
    t0=-.34;t1=.34
    curved_band(a,-6,0,4.6,7.4,t0,t1,0,.14,12,C)
    for r in (5.2825,6.7175):
        for rr,w,z,mat in ((r,.17,.149,M),(r-.036,.065,.17,S),(r+.053,.025,.17,S)):
            curved_band(a,-6,0,rr-w/2,rr+w/2,t0,t1,.14,z,12,mat)
    return finish(a)

def b13_timber_grade_rail_crossing():
    a=new('timber_grade_rail_crossing','rail_track')
    ties(a,3.4); rail(a,[(-.7175,-1.7,.27),(-.7175,1.7,.27)]); rail(a,[(.7175,-1.7,.27),(.7175,1.7,.27)])
    for x in (-1.14,-.91,-.48,-.24,0,.24,.48,.91,1.14):
        box(a,(x,0,.365),(.217,2.65,.12),W)
        for y in (-1.13,1.13):rod(a,(x,y,.426),(x,y,.431),.022,M,6)
    return finish(a)

def b13_rubber_panel_rail_crossing():
    a=new('rubber_panel_rail_crossing','rail_track')
    slab(a,3.6,3.2,.18,0,A)
    for x in (-1.225,0,1.225):
        for y in (-1.06,0,1.06):
            w=1.23 if x==0 else .79
            box(a,(x,y,.235),(w,1.04,.11),'rubber')
            for off in (-.34,-.17,0,.17,.34):box(a,(x+off,y,.294),(.02,.95,.008),M)
    for x in (-.7175,.7175):rail(a,[(x,-1.6,.14),(x,1.6,.14)])
    return finish(a)

def b13_ballasted_commuter_rail_track():
    a=new('ballasted_commuter_rail_track','rail_track')
    a.prism([(-1.65,-2),(1.65,-2),(1.65,2),(-1.65,2)],0,.15,C)
    ties(a,3.8,z=.13,count=8)
    for x in (-.7175,.7175):rail(a,[(x,-2,.30),(x,2,.30)])
    for i in range(28):
        x=(-1 if i%2 else 1)*(1.17+(i%4)*.12);y=-1.83+(i//2)*.28
        a.sphere((x,y,.168),.08,C,segments=5,rings=2,scale=(.105,.076,.055))
    return finish(a)

def b13_urban_rail_turnout_frog():
    a=new('urban_rail_turnout_frog','rail_track')
    slab(a,3.7,4.6,.12,0,C)
    for i in range(9):box(a,(.12,-2.1+i*.52,.21),(3.4,.20,.18),W)
    for x in (-.7175,.7175):rail(a,[(x,-2.3,.31),(x,2.3,.31)])
    for x in (-.7175,.7175):rail(a,[(x,-2.3,.31),(x+.10,-.9,.31),(x+.38,.50,.31),(x+.93,2.3,.31)])
    for x in (-.57,.58):rail(a,[(x,-.45,.31),(x,.70,.31)])
    for y in (-1.8,-1.4):box(a,(.10,y,.325),(1.77,.07,.075),S)
    return finish(a)

def b13_center_island_light_rail_platform():
    a=new('center_island_light_rail_platform','transit_platform')
    a.prism([(-1.4,-2.7),(1.4,-2.7),(1.4,2.05),(.93,2.7),(-.93,2.7),(-1.4,2.05)],0,.42,C)
    for x in (-1.15,1.15):
        for y in (-1.84,-.60,.64):tactile(a,x,y,.42,.40,1.15)
    joints(a,1.8,5.15,.42,2,5)
    for x in (-1.41,1.41):box(a,(x,-.32,.30),(.03,4.7,.17),M)
    return finish(a)

def b13_low_station_platform_with_access_ramp():
    a=new('low_station_platform_with_access_ramp','transit_platform')
    box(a,(0,.8,.19),(2.5,3.4,.38),C)
    slope(a,-1.25,1.25,-2.5,-.9,.035,.38)
    for y in (-.24,.88,2.0):tactile(a,-.97,y,.38,.42,1.04)
    for y in (-.80,.25,1.3,2.4):box(a,(0,y,.383),(2.4,.009,.006),M)
    handrail(a,[(1.16,-2.3,.073),(1.16,-.9,.38),(1.16,1.0,.38),(1.16,2.35,.38)])
    return finish(a)

def b13_elevated_commuter_platform_end():
    a=new('elevated_commuter_platform_end','transit_platform')
    for x in (-.83,.83):
        for y in (-1.5,1.5):box(a,(x,y,.55),(.44,.46,1.1),C)
    for x in (-.83,.83):box(a,(x,0,1.07),(.38,4.5,.40),C)
    box(a,(0,0,1.31),(2.7,4.7,.24),C)
    for y in (-1.7,-.56,.56,1.7):tactile(a,-1.08,y,1.43,.44,1.08)
    handrail(a,[(1.25,-2.2,1.43),(1.25,0,1.43),(1.25,2.2,1.43)])
    handrail(a,[(-1.25,2.2,1.43),(0,2.2,1.43),(1.25,2.2,1.43)])
    return finish(a)

def b13_subway_sidewalk_stair_entrance():
    a=new('subway_sidewalk_stair_entrance','transit_entrance')
    stair(a,1.8,9,.29,.18,y=-1.3)
    for x in (-1.02,1.02):
        box(a,(x,0,.94),(.23,3.1,1.88),C)
        box(a,(x,0,1.90),(.29,3.2,.08),L)
        handrail(a,[(x,-1.45,1.94),(x,0,1.94),(x,1.45,1.94)],m='green')
    box(a,(0,1.48,1.72),(1.8,.30,.20),C)
    tactile(a,0,1.49,1.82,1.65,.25)
    handrail(a,[(-.78,-1.18,.18),(-.78,0,.91),(-.78,1.18,1.62)])
    return finish(a)

def b13_sunken_transit_ramp_entrance():
    a=new('sunken_transit_ramp_entrance','transit_entrance')
    slope(a,-1.10,1.10,-2.65,2.65,.06,.65)
    for x in (-1.24,1.24):
        box(a,(x,0,.45),(.27,5.5,.90),C)
        box(a,(x,0,.925),(.33,5.6,.05),L)
        handrail(a,[(x,-2.65,.95),(x,0,.95),(x,2.65,.95)],m='green')
    for y in (-1.7,0,1.7):beam(a,(-1.08,y,.06+(y+2.65)*.59/5.3),(1.08,y,.06+(y+2.65)*.59/5.3),.009,.009,M)
    tactile(a,0,2.38,.63,1.85,.33)
    return finish(a)

def b13_transit_elevator_headhouse():
    a=new('transit_elevator_headhouse','transit_entrance')
    slab(a,2.25,2.05,.17)
    for x in (-.98,.98):
        for y in (-.88,.88):box(a,(x,y,1.58),(.15,.15,2.83),M)
    for x in (-.97,.97):
        box(a,(x,0,1.6),(.025,1.62,2.66),'glass')
        for z in (.56,1.62,2.8):box(a,(x,0,z),(.075,1.72,.06),S)
    box(a,(0,.87,1.62),(1.85,.03,2.72),'glass')
    for x in (-.445,.445):
        box(a,(x,-.90,1.29),(.86,.07,2.15),S)
        box(a,(x,-.947,1.49),(.69,.018,1.56),'glass')
    box(a,(0,-.9,2.68),(1.84,.15,.46),M)
    box(a,(0,0,3.06),(2.34,2.11,.17),M)
    box(a,(0,-1.00,.19),(1.76,.19,.04),S)
    box(a,(.85,-.975,1.08),(.11,.045,.24),M)
    rod(a,(.85,-1.008,1.1),(.85,-1.015,1.1),.02,S)
    return finish(a)

def b13_subway_entry_escalator():
    a=new('subway_entry_escalator','transit_entrance')
    stair(a,1.0,10,.27,.16,y=-1.35,m=M,nosing=False)
    for i in range(10):
        for x in (-.40,-.30,-.20,-.10,0,.10,.20,.30,.40):
            box(a,(x,-1.35+(i+.5)*.27,(i+1)*.16+.005),(.016,.23,.01),S)
        box(a,(0,-1.35+i*.27+.02,(i+1)*.16+.007),(.97,.036,.014),Y)
    for x in (-.66,.66):
        beam(a,(x,-1.35,.24),(x,1.35,1.84),.20,.39,S)
        beam(a,(x,-1.45,.98),(x,1.45,2.70),.08,.09,'rubber')
        for y,z in ((-1.25,.20),(0,.97),(1.25,1.72)):
            box(a,(x,y,z+.45),(.045,.17,.8),'glass')
    for y,z in ((-1.51,.06),(1.50,1.59)):box(a,(0,y,z),(1.38,.34,.12),S)
    return finish(a)

def b13_streetcar_cut_stone_tunnel_portal():
    a=new('streetcar_cut_stone_tunnel_portal','transit_structure')
    # Clear arched opening: the arch comprises radial voussoirs.
    for x in (-2.15,2.15):
        box(a,(x,0,1.05),(.68,1.0,2.10),C)
        box(a,(x,-.08,.13),(.95,1.22,.26),L)
        for z in (.7,1.4,2.03):box(a,(x,-.505,z),(.67,.016,.018),M)
    ri=1.82;ro=2.49
    for i in range(12):
        t=i*math.pi/12;u=(i+1)*math.pi/12
        vs=[(r*math.cos(th),y,2.1+r*math.sin(th)) for y in (-.5,.5) for r,th in ((ri,t),(ro,t),(ro,u),(ri,u))]
        a.mesh(vs,[(0,1,2,3),(7,6,5,4),(4,5,1,0),(5,6,2,1),(6,7,3,2),(7,4,0,3)],L if i%2 else C)
    for x in (-.7175,.7175):rail(a,[(x,-.8,0),(x,.8,0)])
    return finish(a)

def b13_timber_creek_pedestrian_bridge():
    a=new('timber_creek_pedestrian_bridge','pedestrian_bridge')
    for x in (-.65,.65):box(a,(x,0,.20),(.18,4.1,.30),W)
    for i in range(23):box(a,(0,-1.98+i*.18,.385),(1.67,.166,.07),'wood')
    for x in (-.80,.80):
        for y in (-1.88,-.65,.65,1.88):box(a,(x,y,.91),(.105,.105,1.17),W)
        for z in (.77,1.48):box(a,(x,0,z),(.10,4.13,.09),'wood')
        for y in (-1.27,0,1.27):beam(a,(x,y-.50,.59),(x,y+.50,1.40),.064,.075,W)
    for x in (-.65,.65):
        for y in (-1.8,1.8):box(a,(x,y,.07),(.5,.5,.14),C)
    return finish(a)

def b13_steel_through_truss_footbridge():
    a=new('steel_through_truss_footbridge','pedestrian_bridge')
    box(a,(0,0,.26),(1.75,5.2,.12),M)
    for i in range(31):box(a,(0,-2.5+i/6,.33),(1.65,.11,.035),S)
    for x in (-.88,.88):
        for z in (.22,1.48):box(a,(x,0,z),(.13,5.4,.13),'green')
        for i in range(5):
            y=-2.6+i*1.3
            box(a,(x,y,.85),(.12,.12,1.25),'green')
            if i<4:beam(a,(x,y,.26),(x,y+1.3,1.48),.085,.085,'green')
        handrail(a,[(x,-2.63,.35),(x,0,.35),(x,2.63,.35)],False,S)
    for y in (-2.4,2.4):box(a,(0,y,.08),(2.1,.44,.16),C)
    return finish(a)

def b13_concrete_arch_pedestrian_bridge():
    a=new('concrete_arch_pedestrian_bridge','pedestrian_bridge')
    # Eight deck sections follow a shallow camber; open undersides remain visible.
    points=[(-2.4,.28),(-1.8,.48),(-1.2,.64),(-.6,.74),(0,.78),(.6,.74),(1.2,.64),(1.8,.48),(2.4,.28)]
    for (y,z),(yy,zz) in zip(points,points[1:]):
        for x in (-.70,.70):beam(a,(x,y,z-.13),(x,yy,zz-.13),.25,.32,C)
        v=[(-.86,y,z-.13),(.86,y,z-.13),(.86,yy,zz-.13),(-.86,yy,zz-.13),
           (-.86,y,z),(.86,y,z),(.86,yy,zz),(-.86,yy,zz)]
        a.mesh(v,[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],C)
    # Stout end abutments leave the cambered bridge's underside visibly open.
    for y in (-2.2,2.2):box(a,(0,y,.10),(1.95,.65,.20),L)
    for x in (-.84,.84):handrail(a,[(x,y,z) for y,z in points],m=S)
    return finish(a)

def b13_city_steps_with_bicycle_gutter():
    a=new('city_steps_with_bicycle_gutter','pedestrian_stair')
    stair(a,1.8,9,.29,.165,y=-1.30)
    slope(a,.97,1.22,-1.30,1.31,.04,1.53,0,S)
    for x in (.98,1.23):beam(a,(x,-1.30,.13),(x,1.31,1.62),.04,.11,M)
    handrail(a,[(-.82,-1.15,.165),(-.82,0,.85),(-.82,1.17,1.485)])
    box(a,(0,1.52,1.375),(2.6,.42,.22),C)
    return finish(a)

def b13_switchback_accessibility_ramp():
    a=new('switchback_accessibility_ramp','accessible_ramp')
    slope(a,-1.39,-.14,-2.1,1.9,.055,.43)
    slope(a,.14,1.39,-2.1,1.9,.805,.43)
    box(a,(0,2.4,.215),(2.78,1.0,.43),C)
    for x in (-1.30,-.20):handrail(a,[(x,-2.05,.06),(x,0,.255),(x,1.86,.43)])
    for x in (.20,1.30):handrail(a,[(x,-2.05,.80),(x,0,.607),(x,1.86,.43)])
    handrail(a,[(-1.3,2.82,.43),(0,2.82,.43),(1.3,2.82,.43)])
    box(a,(0,0,.27),(.12,4.1,.54),C)
    return finish(a)

def b13_quarter_turn_pedestrian_stair():
    a=new('quarter_turn_pedestrian_stair','pedestrian_stair')
    stair(a,1.5,5,.29,.17,x=-.72,y=-2.0)
    box(a,(-.72,.205,.425),(1.5,1.51,.85),C)
    b=Asset('turn');stair(b,1.5,5,.29,.17,y=0,z=.85);b.rotate(-math.pi/2);b.translate((.03,.205,0));a.mesh(b.vertices,b.faces,b.face_materials)
    handrail(a,[(-1.38,-1.86,.17),(-1.38,-.60,.85),(-1.38,.82,.85),(-.1,.82,.85),(1.41,.82,1.70)])
    handrail(a,[(-.03,-1.85,.17),(-.03,-.6,.85)])
    return finish(a)

def b13_open_steel_transit_access_stair():
    a=new('open_steel_transit_access_stair','pedestrian_stair')
    for i in range(11):
        y=-1.75+i*.30;z=.18+i*.18
        box(a,(0,y,z),(1.55,.28,.06),S)
        for k in range(5):box(a,(0,y-.10+k*.05,z+.032),(1.49,.012,.008),M)
    for x in (-.73,.73):
        beam(a,(x,-1.91,.065),(x,1.46,2.05),.11,.22,M)
        handrail(a,[(x,-1.8,.18),(x,-.2,1.14),(x,1.3,1.98)])
        box(a,(x,1.85,1.05),(.13,.13,2.1),M)
        box(a,(x,1.85,.027),(.31,.31,.054),S)
    box(a,(0,1.82,2.055),(1.55,.87,.09),S)
    handrail(a,[(-.74,2.22,2.10),(0,2.22,2.10),(.74,2.22,2.10)])
    return finish(a)

def b13_portable_rail_boarding_ramp():
    a=new('portable_rail_boarding_ramp','transit_access','person')
    slope(a,-.48,.48,-1.00,1.00,.045,.24,0,S)
    for x in (-.49,.49):beam(a,(x,-1.0,.09),(x,1.0,.285),.055,.10,Y)
    for i in range(13):
        y=-.91+i*.15;z=.045+(y+1)*.195/2
        box(a,(0,y,z+.01),(.88,.022,.012),M)
    for x in (-.35,.35):rod(a,(x,.92,.06),(x,.92,.18),.067,'rubber',10)
    for y in (-.48,.48):
        a.tube([(-.505,y-.10,.13),(-.63,y-.10,.13),(-.63,y+.10,.13),(-.505,y+.10,.13)],.016,M,6)
    return finish(a)

def b13_hinged_platform_gap_bridge():
    a=new('hinged_platform_gap_bridge','transit_access','person')
    box(a,(0,.39,.28),(1.30,.77,.56),C)
    box(a,(0,-.235,.58),(1.1,.63,.06),S)
    rod(a,(-.60,.085,.595),(.60,.085,.595),.034,M,10)
    for x in (-.40,-.20,0,.20,.40):box(a,(x,-.235,.614),(.045,.57,.008),M)
    for x in (-.565,.565):box(a,(x,-.235,.62),(.04,.63,.08),Y)
    for x in (-.43,.43):beam(a,(x,.10,.20),(x,-.41,.545),.045,.06,M)
    box(a,(0,.40,.57),(1.10,.37,.02),Y)
    return finish(a)

def b13_pedestrian_underpass_box_section():
    a=new('pedestrian_underpass_box_section','transit_structure')
    slab(a,3.9,2.5,.22)
    for x in (-1.78,1.78):
        box(a,(x,0,1.55),(.34,2.5,2.67),C)
        box(a,(x,0,2.86),(.53,2.65,.17),L)
    box(a,(0,0,3.02),(3.95,2.7,.27),C)
    for x in (-1.46,1.46):box(a,(x,0,.32),(.29,2.5,.20),L)
    for y in (-.8,0,.8):box(a,(0,y,.223),(2.57,.009,.006),M)
    for x in (-1.58,1.58):
        rod(a,(x,-1.2,1.22),(x,1.2,1.22),.026,S)
        for y in (-.95,.95):rod(a,(x,y,1.22),(x*1.08,y,1.13),.018,S)
    return finish(a)

_FACTORIES=[
    b13_scored_concrete_sidewalk_bay,b13_radius_sidewalk_corner,b13_reentrant_sidewalk_corner,
    b13_flared_accessible_curb_ramp,b13_dual_direction_corner_ramps,b13_parallel_depressed_curb_ramp,
    b13_residential_driveway_apron,b13_reinforced_alley_sidewalk_crossover,b13_truncated_dome_warning_panel,
    b13_directional_ribbed_guidance_paving,b13_zebra_crossing_road_section,b13_ladder_crossing_road_section,
    b13_raised_pedestrian_crossing_table,b13_pedestrian_median_refuge_island,b13_curb_extension_bulbout,
    b13_bus_bulb_boarding_pad,b13_cycletrack_driveway_crossing,b13_raised_neighborhood_intersection,
    b13_crowned_cobblestone_alley,b13_basketweave_brick_sidewalk_panel,b13_granite_curb_sett_course,
    b13_rolled_concrete_gutter_curb,b13_permeable_concrete_grid_paving,b13_bridge_approach_settlement_slab,
    b13_road_bridge_finger_expansion_joint,b13_sidewalk_sliding_expansion_cover,b13_embedded_grooved_streetcar_track,
    b13_curved_streetcar_track_segment,b13_timber_grade_rail_crossing,b13_rubber_panel_rail_crossing,
    b13_ballasted_commuter_rail_track,b13_urban_rail_turnout_frog,b13_center_island_light_rail_platform,
    b13_low_station_platform_with_access_ramp,b13_elevated_commuter_platform_end,b13_subway_sidewalk_stair_entrance,
    b13_sunken_transit_ramp_entrance,b13_transit_elevator_headhouse,b13_subway_entry_escalator,
    b13_streetcar_cut_stone_tunnel_portal,b13_timber_creek_pedestrian_bridge,b13_steel_through_truss_footbridge,
    b13_concrete_arch_pedestrian_bridge,b13_city_steps_with_bicycle_gutter,b13_switchback_accessibility_ramp,
    b13_quarter_turn_pedestrian_stair,b13_open_steel_transit_access_stair,b13_portable_rail_boarding_ramp,
    b13_hinged_platform_gap_bridge,b13_pedestrian_underpass_box_section,
]
assert len(_FACTORIES)==50
for _f in _FACTORIES:
    _a=_f()
    register(_f.__name__,_a.category,_a.size_class,_f)
