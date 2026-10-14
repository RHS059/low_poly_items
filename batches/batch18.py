"""Outdoor lighting and decorative civic fixtures, authored at real metre scale.
Fifty distinct silhouettes with restrained metal, stone, glass and warm lenses.
"""
import math
from assetlib import Asset, register

D='dark_metal'
M='metal'
S='steel'
K='black'
L='light'
G='glass'
C='concrete'
W='cream'


def fixture(category,size='person'):
    def decorate(fn):
        def make():
            a=Asset(fn.__name__,category,size)
            fn(a)
            return a.bottom_center()
        make.__name__=fn.__name__
        register(fn.__name__,category,size,make)
        return make
    return decorate


def rod(a,p,q,r,mat=D,n=8,r2=None):
    a.cylinder(p,q,r,mat=mat,sides=n,radius2=r2)
def disk(a,p,r,h,mat=D,n=12):
    rod(a,(p[0],p[1],p[2]-h/2),(p[0],p[1],p[2]+h/2),r,mat,n)
def box(a,p,s,mat=D,rot=None): a.box(p,s,mat=mat,rot=rot)
def tube(a,pts,r,mat=D,n=8): a.tube(pts,r,mat,n)
def ball(a,p,r,mat=L): a.sphere(p,r,mat,segments=10,rings=5)
def ring(a,p,r,t=.016,mat=D,axis='z',n=12):
    a.torus(p,r,t,mat,axis=axis,segments=n,sides=5)
def anchor(a,r=.22):
    disk(a,(0,0,.045),r,.09,C)
    disk(a,(0,0,.105),r*.76,.04,D,8)
    for x,y in ((.56,0),(-.56,0),(0,.56),(0,-.56)):
        rod(a,(x*r,y*r,.126),(x*r,y*r,.15),.018,S,6)
def pole(a,h=5,r=.085,ornate=False):
    anchor(a,max(.20,r*2.2))
    rod(a,(0,0,.13),(0,0,h),r,D,10,r*.62)
    box(a,(0,-r*.95,.52),(.085,.018,.26),M)
    if ornate:
        rod(a,(0,0,.15),(0,0,.46),r*1.65,D,10,r*1.3)
        for z,rr in ((.17,r*1.85),(.46,r*1.35),(.66,r*1.12),(h-.13,r*1.1)):
            disk(a,(0,0,z),rr,.035,D,10)
def lensbox(a,p,w=.6,d=.3,h=.12):
    box(a,p,(w,d,h),D)
    box(a,(p[0],p[1],p[2]-h*.51),(w*.84,d*.8,.018),L)
    for x in (-.25,.25):
        box(a,(p[0]+x*w,p[1],p[2]+h*.5),(.026,d*.72,.02),M)
def lantern(a,p,r=.23,h=.6):
    x,y,z=p
    rod(a,(x,y,z),(x,y,z+h*.70),r*.67,G,4,r*.96)
    for i in range(4):
        t=i*math.pi/2
        tube(a,[(x+r*.67*math.cos(t),y+r*.67*math.sin(t),z),(x+r*.96*math.cos(t),y+r*.96*math.sin(t),z+h*.70)],.016,D,5)
    disk(a,(x,y,z-.016),r*.84,.05,D,4)
    disk(a,(x,y,z+h*.71),r*1.12,.055,D,4)
    a.cone((x,y,z+h*.735),(x,y,z+h),r*1.15,D,sides=4)
    ball(a,(x,y,z+h+.025),.038,D)
    rod(a,(x,y,z+.06),(x,y,z+h*.57),.038,L,6)
def dome(a,p,r=.3):
    x,y,z=p
    rod(a,(x,y,z),(x,y,z+.13),r,D,12,r*.38)
    disk(a,(x,y,z-.01),r,.032,D)
    disk(a,(x,y,z-.032),r*.79,.014,L)
def mount(a,p=(0,0,.2),w=.14,h=.3):
    x,y,z=p
    box(a,(x,y,z),(w,.035,h),D)
    for dz in (-h*.36,h*.36):
        rod(a,(x,y-.022,z+dz),(x,y-.036,z+dz),.014,S,6)
def roof(a,p,w,d,rise):
    x,y,z=p
    # Solid pitched cover with outward winding.
    vs=[(x-w/2,y-d/2,z),(x+w/2,y-d/2,z),(x+w/2,y+d/2,z),(x-w/2,y+d/2,z),(x,y-d/2,z+rise),(x,y+d/2,z+rise)]
    a.mesh(vs,[(3,2,1,0),(0,1,4),(1,2,5,4),(2,3,5),(3,0,4,5)],D)
def clockface(a,x,y,z,r=.47,back=False):
    sign=-1 if back else 1
    rod(a,(x,y,z),(x,y+sign*.026,z),r,W,16)
    ring(a,(x,y+sign*.025,z),r,.028,D,'y',16)
    for i in range(12):
        t=i*math.tau/12
        p=(x+math.sin(t)*r*.83,y+sign*.045,z+math.cos(t)*r*.83)
        q=(x+math.sin(t)*r*.70,y+sign*.045,z+math.cos(t)*r*.70)
        a.beam(p,q,.022,.009,D)
    a.beam((x,y+sign*.053,z),(x-r*.40,y+sign*.053,z+r*.24),.032,.012,D)
    a.beam((x,y+sign*.065,z),(x+r*.13,y+sign*.065,z+r*.59),.022,.012,D)
    rod(a,(x,y+sign*.052,z),(x,y+sign*.076,z),.042,D,8)


@fixture('street_lighting','large')
def b18_cobrahead_roadway_lamp(a):
    pole(a,7.1,.12)
    tube(a,[(0,0,6.6),(.48,0,7.07),(1.18,0,7.32),(1.72,0,7.32)],.065,M)
    a.sphere((1.9,0,7.3),(.48,.24,.15),M,segments=10,rings=4)
    a.sphere((1.98,0,7.19),(.33,.18,.08),L,segments=10,rings=3)
    box(a,(1.70,0,7.37),(.14,.15,.045),D)

@fixture('street_lighting','large')
def b18_flat_led_roadway_lamp(a):
    pole(a,6.5,.10)
    a.beam((0,0,6.42),(1.5,0,6.7),.095,.08,D)
    lensbox(a,(1.63,0,6.72),.78,.30,.11)
    for x in (1.45,1.65,1.85):
        box(a,(x,0,6.65),(.115,.19,.012),L)
    a.beam((0,0,6.13),(.66,0,6.54),.032,.04,M)

@fixture('street_lighting','large')
def b18_double_arm_boulevard_light(a):
    pole(a,7.2,.12)
    for s in (-1,1):
        tube(a,[(0,0,6.84),(s*.45,0,7.32),(s*1.15,0,7.42),(s*1.62,0,7.42)],.07,D)
        lensbox(a,(s*1.76,0,7.39),.74,.34,.16)
    disk(a,(0,0,7.19),.16,.12,D)

@fixture('street_lighting','large')
def b18_historic_teardrop_streetlight(a):
    pole(a,5.5,.105,True)
    tube(a,[(0,0,5.32),(.28,0,5.85),(.66,0,6.03),(1.04,0,5.90),(1.22,0,5.62),(1.22,0,5.45)],.052,D)
    a.sphere((1.22,0,5.16),(.21,.21,.31),G,segments=10,rings=5)
    dome(a,(1.22,0,5.43),.28)
    a.cone((1.22,0,4.98),(1.22,0,4.79),.16,D,8)
    tube(a,[(0,0,5.08),(.43,0,5.54),(.88,0,5.59)],.022,D)

@fixture('street_lighting','large')
def b18_gooseneck_industrial_post_light(a):
    pole(a,4.5,.09)
    tube(a,[(0,0,4.34),(0,0,4.84),(.18,0,5.06),(.57,0,5.06),(.79,0,4.85),(.79,0,4.66)],.042,D)
    dome(a,(.79,0,4.44),.42)
    rod(a,(.79,0,4.54),(.79,0,4.72),.12,D,10)
    ball(a,(.79,0,4.4),.075,L)

@fixture('park_lighting','large')
def b18_acorn_globe_park_lamp(a):
    pole(a,3.25,.09,True)
    disk(a,(0,0,3.27),.19,.09,D)
    a.sphere((0,0,3.63),(.25,.25,.36),G,segments=10,rings=5)
    disk(a,(0,0,3.88),.17,.045,D)
    a.cone((0,0,3.9),(0,0,4.05),.18,D,10)
    ball(a,(0,0,4.08),.045,D)
    for t in (0,math.pi/2,math.pi,3*math.pi/2):
        tube(a,[(.10*math.cos(t),.10*math.sin(t),3.30),(.245*math.cos(t),.245*math.sin(t),3.61),(.14*math.cos(t),.14*math.sin(t),3.89)],.012,D,5)

@fixture('park_lighting','large')
def b18_schoolhouse_globe_lamp(a):
    pole(a,3.1,.073,True)
    rod(a,(0,0,3.07),(0,0,3.34),.14,D,10,.18)
    rod(a,(0,0,3.34),(0,0,3.54),.21,W,12,.31)
    rod(a,(0,0,3.54),(0,0,3.71),.31,W,12,.20)
    a.cone((0,0,3.71),(0,0,3.78),.20,W,12)
    disk(a,(0,0,3.34),.225,.035,D)

@fixture('plaza_lighting','large')
def b18_four_lantern_plaza_standard(a):
    pole(a,3.6,.115,True)
    for t in (0,math.pi/2,math.pi,3*math.pi/2):
        x,y=.62*math.cos(t),.62*math.sin(t)
        tube(a,[(0,0,3.19),(x*.62,y*.62,3.27),(x,y,3.59)],.036,D)
        lantern(a,(x,y,3.57),.20,.54)
    ball(a,(0,0,3.79),.10,'gold')

@fixture('park_lighting','large')
def b18_tapered_lantern_avenue_lamp(a):
    pole(a,3.2,.095,True)
    lantern(a,(0,0,3.19),.32,.91)
    for z in (3.32,3.65):
        disk(a,(0,0,z),.085,.035,D,6)

@fixture('street_lighting','large')
def b18_solar_panel_street_lamp(a):
    pole(a,5.6,.11)
    a.beam((0,0,5.12),(1.12,0,5.35),.10,.10,D)
    lensbox(a,(1.30,0,5.34),.68,.39,.12)
    box(a,(0,.11,5.55),(.24,.21,.45),M)
    box(a,(0,0,5.98),(1.2,.84,.06),S,rot=(.30,0,0))
    for x in (-.39,0,.39):
        for y in (-.22,.16):
            box(a,(x,y,6.03+y*.30),(.36,.33,.012),'navy',rot=(.30,0,0))
    a.beam((0,0,5.5),(0,.30,5.99),.06,.07,D)

@fixture('promenade_lighting','large')
def b18_rectangular_frame_promenade_light(a):
    anchor(a,.25)
    box(a,(0,0,2.18),(.16,.23,4.12),D)
    box(a,(.42,0,4.18),(1.0,.23,.16),D)
    box(a,(.84,0,3.56),(.16,.23,1.38),D)
    box(a,(.75,0,3.61),(.021,.16,1.14),L)
    box(a,(0,-.124,.49),(.10,.014,.30),M)

@fixture('suspended_street_lighting','large')
def b18_catenary_lighting_span(a):
    # Two fixed architectural standards support three suspended roadway fixtures.
    for x in (-3.8,3.8):
        box(a,(x,0,.10),(.44,.44,.20),C)
        rod(a,(x,0,.18),(x,0,5.0),.085,D,8,.052)
        disk(a,(x,0,5.0),.09,.035,S)
    pts=[(-3.8,0,4.9),(-2.2,0,4.65),(0,0,4.52),(2.2,0,4.65),(3.8,0,4.9)]
    tube(a,pts,.012,K,5)
    for x,z in ((-2.2,4.65),(0,4.52),(2.2,4.65)):
        rod(a,(x,0,z),(x,0,z-.22),.015,D,6)
        lensbox(a,(x,0,z-.27),.59,.35,.10)

@fixture('area_lighting','large')
def b18_stadium_floodlight_mast(a):
    pole(a,8.4,.19)
    for z in (7.55,8.18):
        box(a,(0,0,z),(2.30,.12,.13),D)
        for x in (-.82,0,.82):
            box(a,(x,.08,z+.11),(.57,.28,.47),M,rot=(.32,0,0))
            box(a,(x,-.08,z+.08),(.49,.035,.36),L,rot=(.32,0,0))
            for dx in (-.28,.28): rod(a,(x+dx,0,z),(x+dx,.14,z+.20),.025,D,6)
    for z in (1.8,2.4,3,3.6,4.2,4.8,5.4,6,6.6):
        rod(a,(-.24,0,z),(.24,0,z),.019,S,6)
    box(a,(0,0,.74),(.31,.28,.42),D)

@fixture('parking_lighting','large')
def b18_twin_shoebox_parking_lamp(a):
    anchor(a,.28)
    box(a,(0,0,3.6),(.15,.15,7.0),D)
    for s in (-1,1):
        box(a,(s*.32,0,6.93),(.62,.10,.13),D)
        lensbox(a,(s*.71,0,6.96),.58,.57,.23)
        box(a,(s*.71,0,7.10),(.43,.42,.04),M)
    box(a,(0,-.083,.55),(.10,.014,.32),M)

@fixture('park_lighting','large')
def b18_shielded_mushroom_posttop(a):
    pole(a,3.0,.075)
    disk(a,(0,0,3.1),.28,.05,D)
    rod(a,(0,0,3.10),(0,0,3.31),.12,L,10,.20)
    for i in range(4):
        t=i*math.pi/2
        rod(a,(.23*math.cos(t),.23*math.sin(t),3.12),(.23*math.cos(t),.23*math.sin(t),3.36),.018,D,6)
    rod(a,(0,0,3.35),(0,0,3.46),.45,D,12,.11)
    disk(a,(0,0,3.35),.46,.035,D)

@fixture('bollard_lighting')
def b18_louvered_cylinder_light_bollard(a):
    anchor(a,.18)
    rod(a,(0,0,.11),(0,0,.67),.125,D,12)
    rod(a,(0,0,.65),(0,0,.94),.105,L,10)
    for z in (.66,.74,.82,.9,.97): disk(a,(0,0,z),.145,.033,D)
    a.cone((0,0,.986),(0,0,1.04),.145,D,12)

@fixture('bollard_lighting')
def b18_recessed_square_light_bollard(a):
    box(a,(0,0,.06),(.28,.28,.12),C)
    box(a,(0,0,.52),(.17,.17,.93),D)
    box(a,(0,-.088,.76),(.125,.018,.30),K)
    box(a,(0,-.101,.86),(.095,.009,.06),L)
    box(a,(0,-.15,.66),(.17,.14,.026),D)
    box(a,(0,0,1.0),(.19,.19,.035),M)

@fixture('path_lighting')
def b18_conical_path_lamp(a):
    disk(a,(0,0,.025),.12,.05,D,8)
    rod(a,(0,0,.04),(0,0,.8),.026,D,8)
    a.cone((0,0,.77),(0,0,1.02),.27,D,10)
    disk(a,(0,0,.731),.22,.014,L,10)
    disk(a,(0,0,.75),.28,.025,D,10)

@fixture('garden_lighting')
def b18_shepherd_hook_lantern_light(a):
    disk(a,(0,0,.025),.12,.05,C,8)
    tube(a,[(0,0,.02),(0,0,1.6),(.08,0,1.8),(.29,0,1.86),(.48,0,1.7),(.48,0,1.61)],.026,D,7)
    ring(a,(.48,0,1.57),.065,.009,D,'y',8)
    lantern(a,(.48,0,1.08),.17,.43)
    rod(a,(0,0,.12),(.14,0,.02),.019,D,6)

@fixture('landscape_lighting','handheld')
def b18_low_mushroom_landscape_light(a):
    disk(a,(0,0,.015),.07,.03,D,8)
    rod(a,(0,0,.03),(0,0,.25),.022,D,6)
    rod(a,(0,0,.23),(0,0,.29),.095,L,8)
    rod(a,(0,0,.29),(0,0,.355),.18,D,10,.05)
    disk(a,(0,0,.286),.184,.016,D,10)

@fixture('landscape_lighting','handheld')
def b18_ground_stake_spotlight(a):
    a.cone((0,0,.16),(0,0,0),.025,D,6)
    rod(a,(0,0,.12),(0,0,.23),.017,D,6)
    rod(a,(0,0,.24),(0,-.15,.34),.065,D,10)
    rod(a,(0,-.145,.335),(0,-.162,.347),.056,L,10)
    for x in (-.055,.055): rod(a,(x,0,.19),(x,0,.26),.014,M,6)
    rod(a,(-.075,0,.23),(.075,0,.23),.014,S,6)

@fixture('landscape_lighting','handheld')
def b18_flush_inground_uplight(a):
    disk(a,(0,0,.035),.135,.07,K,12)
    disk(a,(0,0,.078),.15,.016,S,12)
    disk(a,(0,0,.089),.117,.009,G,12)
    disk(a,(0,0,.095),.078,.005,L,10)
    for t in (0,math.tau/3,2*math.tau/3):
        disk(a,(.133*math.cos(t),.133*math.sin(t),.089),.009,.004,D,6)

@fixture('step_lighting','handheld')
def b18_recessed_brick_step_light(a):
    box(a,(0,0,.055),(.26,.065,.11),D)
    box(a,(0,-.038,.056),(.23,.009,.083),M)
    box(a,(0,-.044,.054),(.19,.008,.052),L)
    for z in (.043,.061,.079): box(a,(0,-.052,z),(.202,.014,.012),D)
    for x in (-.109,.109): rod(a,(x,-.044,.055),(x,-.052,.055),.007,S,6)

@fixture('wall_lighting','handheld')
def b18_round_bulkhead_wall_light(a):
    rod(a,(0,0,.15),(0,-.065,.15),.145,D,12)
    rod(a,(0,-.066,.15),(0,-.105,.15),.116,L,12,.103)
    ring(a,(0,-.102,.15),.115,.012,D,'y',12)
    for x in (-.056,.056):
        rod(a,(x,-.115,.058),(x,-.115,.242),.008,D,6)
    rod(a,(-.108,-.114,.15),(.108,-.114,.15),.009,D,6)

@fixture('wall_lighting','handheld')
def b18_rectangular_caged_wall_light(a):
    box(a,(0,0,.18),(.18,.062,.36),D)
    box(a,(0,-.044,.18),(.13,.05,.29),L)
    for x in (-.086,.086): box(a,(x,-.084,.18),(.015,.018,.33),D)
    for z in (.04,.12,.24,.32): box(a,(0,-.084,z),(.18,.018,.013),D)
    for x in (-.029,.029): box(a,(x,-.088,.18),(.012,.012,.30),D)

@fixture('wall_lighting')
def b18_coach_house_wall_lantern(a):
    mount(a,(0,0,.39),.18,.44)
    tube(a,[(0,-.02,.51),(0,-.28,.66),(0,-.43,.58)],.027,D,7)
    lantern(a,(0,-.43,.08),.20,.50)
    ring(a,(0,-.43,.63),.07,.014,D,'y',10)

@fixture('wall_lighting','handheld')
def b18_modern_cube_downlight(a):
    mount(a,(0,0,.135),.15,.21)
    box(a,(0,-.115,.14),(.22,.21,.24),D)
    box(a,(0,-.125,.017),(.17,.15,.012),K)
    box(a,(0,-.125,.009),(.125,.12,.008),L)
    box(a,(0,-.23,.23),(.20,.012,.025),M)

@fixture('wall_lighting','handheld')
def b18_cylindrical_up_down_sconce(a):
    mount(a,(0,0,.19),.10,.20)
    rod(a,(0,-.11,.045),(0,-.11,.355),.073,D,12)
    for z in (.04,.36):
        disk(a,(0,-.11,z),.075,.02,M,12)
        disk(a,(0,-.11,z+(.014 if z>.2 else -.014)),.056,.008,L,10)

@fixture('security_lighting')
def b18_twin_motion_sensor_security_light(a):
    mount(a,(0,0,.27),.16,.22)
    for s in (-1,1):
        tube(a,[(0,-.03,.29),(s*.15,-.11,.31),(s*.22,-.14,.37)],.022,D,6)
        rod(a,(s*.22,-.11,.40),(s*.29,-.24,.39),.105,D,10,.125)
        rod(a,(s*.29,-.24,.39),(s*.30,-.251,.39),.106,L,10)
    box(a,(0,-.085,.15),(.105,.11,.12),W)
    a.sphere((0,-.147,.15),(.043,.020,.042),G,segments=8,rings=3)

@fixture('security_lighting')
def b18_yoke_mounted_rectangular_floodlight(a):
    box(a,(0,0,.027),(.22,.18,.054),D)
    for x in (-.25,.25):
        box(a,(x,0,.24),(.045,.10,.42),D)
        rod(a,(x-.025,0,.37),(x+.025,0,.37),.032,S,8)
    box(a,(0,0,.37),(.46,.17,.34),D,rot=(.2,0,0))
    box(a,(0,-.105,.355),(.405,.028,.27),L,rot=(.2,0,0))
    for x in (-.15,0,.15): box(a,(x,.1,.4),(.025,.08,.26),M,rot=(.2,0,0))

@fixture('wall_lighting')
def b18_barn_gooseneck_wall_light(a):
    mount(a,(0,0,.38),.18,.40)
    tube(a,[(0,-.03,.44),(0,-.16,.64),(0,-.43,.71),(0,-.68,.59),(0,-.68,.42)],.03,D,8)
    dome(a,(0,-.68,.23),.34)
    rod(a,(0,-.68,.32),(0,-.68,.45),.09,D,10)
    ball(a,(0,-.68,.22),.064,L)

@fixture('canopy_lighting')
def b18_linear_canopy_strip_light(a):
    box(a,(0,0,.14),(1.30,.12,.10),D)
    box(a,(0,0,.084),(1.24,.08,.015),L)
    for x in (-.48,.48):
        box(a,(x,0,.23),(.07,.15,.08),S)
        rod(a,(x,-.05,.22),(x,-.05,.29),.01,D,6)
    for x in (-.63,.63): box(a,(x,0,.13),(.04,.14,.13),M)

@fixture('awning_lighting')
def b18_angled_awning_wash_light(a):
    for x in (-.45,.45):
        mount(a,(x,0,.12),.10,.21)
        a.beam((x,-.02,.13),(x,-.37,.27),.035,.04,D)
    box(a,(0,-.41,.28),(1.14,.14,.12),D,rot=(-.55,0,0))
    box(a,(0,-.475,.31),(1.05,.012,.075),L,rot=(-.55,0,0))
    for x in (-.55,.55): rod(a,(x-.015,-.41,.28),(x+.015,-.41,.28),.073,M,8)

@fixture('hanging_lighting')
def b18_industrial_pendant_light(a):
    disk(a,(0,0,1.10),.105,.025,D,10)
    rod(a,(0,0,.44),(0,0,1.09),.014,K,6)
    rod(a,(0,0,.32),(0,0,.45),.079,D,10)
    rod(a,(0,0,.10),(0,0,.33),.30,D,12,.079)
    disk(a,(0,0,.097),.305,.028,D,12)
    disk(a,(0,0,.08),.255,.015,L,12)
    for i in range(4):
        t=i*math.pi/2
        tube(a,[(.26*math.cos(t),.26*math.sin(t),.1),(.18*math.cos(t),.18*math.sin(t),.012),(0,0,.006)],.012,D,5)

@fixture('hanging_lighting','large')
def b18_festoon_bulb_cable(a):
    pts=[]
    for i in range(11):
        x=-2.5+i*.5;z=.62+.08*x*x;pts.append((x,0,z))
    tube(a,pts,.008,K,5)
    for x,y,z in pts[1:-1]:
        rod(a,(x,0,z),(x,0,z-.09),.015,K,6)
        rod(a,(x,0,z-.07),(x,0,z-.13),.028,D,8)
        a.sphere((x,0,z-.173),(.052,.052,.07),L,segments=8,rings=4)
    for p in (pts[0],pts[-1]): ring(a,p,.033,.008,S,'y',8)

@fixture('illuminated_civic_fixture')
def b18_backlit_address_pedestal(a):
    box(a,(0,0,.065),(.50,.26,.13),C)
    for x in (-.19,.19): box(a,(x,0,.61),(.065,.09,1.0),D)
    box(a,(0,0,.99),(.64,.13,.38),D)
    box(a,(0,-.073,.99),(.55,.014,.28),L)
    # Geometric address 124, separate visible strokes.
    box(a,(-.18,-.087,.99),(.025,.01,.19),D)
    for z in (.895,.99,1.085): box(a,(-.025,-.087,z),(.10,.01,.021),D)
    for x,z in ((.014,1.04),(-.064,.94)):
        box(a,(x,-.087,z),(.021,.01,.075),D)
    for x,z,h in ((.16,.99,.19),(.08,1.04,.09)):
        box(a,(x,-.087,z),(.023,.01,h),D)
    box(a,(.12,-.087,.99),(.11,.01,.021),D)
    box(a,(0,0,1.205),(.69,.17,.045),D)

@fixture('civic_clock','large')
def b18_four_face_town_clock(a):
    pole(a,3.0,.16,True)
    box(a,(0,0,3.51),(1.02,1.02,1.05),D)
    # Four independently modelled clock dials.
    clockface(a,0,-.522,3.54,.43,True)
    clockface(a,0,.522,3.54,.43,False)
    for s in (-1,1):
        sub=Asset('clock_side')
        clockface(sub,0,s*.522,3.54,.43,s<0)
        sub.rotate((0,0,math.pi/2))
        a.mesh(sub.vertices,sub.faces,sub.face_materials)
    roof(a,(0,0,4.07),1.28,1.28,.28)
    ball(a,(0,0,4.43),.075,'gold')
    box(a,(0,0,2.99),(1.12,1.12,.10),D)

@fixture('civic_clock','large')
def b18_double_face_sidewalk_clock(a):
    pole(a,2.78,.09,True)
    rod(a,(0,-.12,3.23),(0,.12,3.23),.54,D,16)
    clockface(a,0,-.128,3.23,.47,True)
    clockface(a,0,.128,3.23,.47,False)
    disk(a,(0,0,3.78),.10,.075,D,8)
    ball(a,(0,0,3.86),.055,'gold')
    for s in (-1,1): tube(a,[(0,0,2.61),(s*.26,0,2.74),(s*.44,0,2.98)],.025,D,6)

@fixture('civic_sundial')
def b18_stone_pedestal_sundial(a):
    box(a,(0,0,.09),(.60,.60,.18),C)
    rod(a,(0,0,.18),(0,0,.84),.21,'concrete_light',8,.17)
    disk(a,(0,0,.90),.34,.12,C,12)
    disk(a,(0,0,.972),.285,.024,'gold',16)
    # Thick triangular gnomon, points to celestial pole.
    a.mesh([(-.02,-.18,.99),(-.02,.18,.99),(-.02,.18,1.25),(.02,-.18,.99),(.02,.18,.99),(.02,.18,1.25)],[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],D)
    for i in range(12):
        t=i*math.tau/12
        a.beam((.23*math.cos(t),.23*math.sin(t),.989),(.265*math.cos(t),.265*math.sin(t),.989),.009,.006,D)

@fixture('civic_flag_fixture','large')
def b18_angled_building_flagpole(a):
    mount(a,(0,0,.24),.21,.46)
    rod(a,(0,-.02,.18),(0,-1.80,2.26),.025,S,10)
    ball(a,(0,-1.83,2.30),.049,'gold')
    # A hanging municipal pennant attached along an angled upper edge.
    vs=[(-.010,-.68,.97),(-.010,-1.64,2.09),(-.010,-1.69,.86),(-.010,-.92,.21),(.01,-.68,.97),(.01,-1.64,2.09),(.01,-1.69,.86),(.01,-.92,.21)]
    a.mesh(vs,[(3,2,1,0),(4,5,6,7),(1,5,4,0),(2,6,5,1),(3,7,6,2),(0,4,7,3)],'navy')
    rod(a,(-.016,-1.22,1.06),(.016,-1.22,1.06),.18,'gold',8)
    rod(a,(-.020,-1.22,1.06),(.020,-1.22,1.06),.12,'cream',8)

@fixture('civic_flag_fixture','large')
def b18_american_flag_civic_pole(a):
    anchor(a,.28)
    rod(a,(0,0,.12),(0,0,6.2),.058,S,12,.025)
    ball(a,(0,0,6.24),.065,'gold')
    rod(a,(.06,0,.6),(.06,0,6.16),.006,W,5)
    rod(a,(-.07,0,.89),(.10,0,.89),.015,S,6)
    # Thirteen raised cloth bands; fly edge has a restrained folded silhouette.
    xs=(.075,.58,1.08,1.58);ys=(0,.05,-.045,.08)
    for row in range(13):
        z=5.96-row*.073
        for j in range(3):
            x0,x1=xs[j],xs[j+1];y0,y1=ys[j],ys[j+1]
            vs=[(x0,y0-.006,z-.071),(x1,y1-.006,z-.071),(x1,y1+.006,z-.071),(x0,y0+.006,z-.071),(x0,y0-.006,z),(x1,y1-.006,z),(x1,y1+.006,z),(x0,y0+.006,z)]
            a.mesh(vs,[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],'red' if row%2==0 else 'white')
    for x0,x1,y0,y1 in ((.075,.58,0,.05),(.58,.659,.05,.03578)):
        vs=[(x0,y0-.016,5.451),(x1,y1-.016,5.451),(x1,y1-.006,5.451),(x0,y0-.006,5.451),(x0,y0-.016,5.963),(x1,y1-.016,5.963),(x1,y1-.006,5.963),(x0,y0-.006,5.963)]
        a.mesh(vs,[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],'navy')
    for row in range(9):
        count=6 if row%2==0 else 5
        for j in range(count):
            x=.12+j*.089+(.0445 if row%2 else 0)
            yy=(x-.075)*(.05/.505) if x<=.58 else .05-(x-.58)*.18
            tilt=math.atan(.05/.505) if x<=.58 else math.atan(-.18)
            box(a,(x,yy-.020,5.925-row*.052),(.017,.006,.017),'white',rot=(0,0,tilt))

@fixture('civic_banner','large')
def b18_single_banner_street_standard(a):
    pole(a,4.1,.076)
    for z in (2.11,3.70): rod(a,(0,0,z),(.82,0,z),.025,D,8)
    box(a,(.42,0,2.91),(.69,.014,1.50),'teal')
    box(a,(.42,-.012,3.39),(.44,.008,.11),W)
    for z,w in ((3.16,.26),(2.94,.38),(2.72,.26)):
        box(a,(.42,-.012,z),(w,.008,.055),W)
    ball(a,(0,0,4.17),.065,'gold')

@fixture('civic_banner','large')
def b18_twin_vertical_banner_gateway(a):
    anchor(a,.26)
    box(a,(0,0,2.28),(.17,.17,4.32),D)
    box(a,(0,0,4.40),(2.00,.11,.10),D)
    for s in (-1,1):
        box(a,(s*.59,0,3.41),(.68,.014,1.89),'navy')
        box(a,(s*.59,-.01,3.91),(.47,.009,.28),'cream')
        for z in (3.42,3.23,3.04): box(a,(s*.59,-.01,z),(.40,.009,.035),'cream')
        x=s*.59
        a.mesh([(x-.34,-.007,2.47),(x+.34,-.007,2.47),(x,-.007,2.23),(x-.34,.007,2.47),(x+.34,.007,2.47),(x,.007,2.23)],[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],'navy')
        rod(a,(s*.95,0,4.33),(s*.95,0,4.5),.026,'gold',8)

@fixture('civic_hanging_fixture','large')
def b18_ornamental_hanging_basket_standard(a):
    pole(a,2.85,.09,True)
    for s in (-1,1):
        tube(a,[(0,0,2.68),(s*.30,0,3.03),(s*.65,0,3.03),(s*.89,0,2.84),(s*.89,0,2.70)],.027,D,7)
        ring(a,(s*.45,0,2.76),.13,.014,D,'y',10)
        for dx,dy in ((-.21,0),(.21,0),(0,.21)):
            rod(a,(s*.89,0,2.7),(s*.89+dx,dy,2.12),.006,D,5)
        rod(a,(s*.89,0,1.89),(s*.89,0,2.13),.14,'terracotta',10,.25)
        disk(a,(s*.89,0,2.12),.255,.055,D,10)
        disk(a,(s*.89,0,2.148),.219,.008,'soil',10)
    ball(a,(0,0,2.96),.075,'gold')

@fixture('civic_monument','large')
def b18_granite_civic_obelisk(a):
    box(a,(0,0,.10),(1.3,1.3,.20),C)
    box(a,(0,0,.27),(1.06,1.06,.14),'concrete_light')
    box(a,(0,0,.66),(.83,.83,.65),C)
    rod(a,(0,0,.985),(0,0,3.2),.53,'concrete_light',4,.31)
    a.cone((0,0,3.2),(0,0,3.78),.31,'concrete_light',4)
    box(a,(0,-.423,.66),(.50,.018,.34),'gold')
    for z,w in ((.76,.31),(.68,.36),(.60,.29),(.54,.17)):
        box(a,(0,-.435,z),(w,.007,.015),'brown')

@fixture('public_art','large')
def b18_interlocking_steel_ribbon_sculpture(a):
    box(a,(0,0,.12),(1.8,1.38,.24),C)
    pts=[(-.48,-.2,.24),(-.64,-.2,1.14),(-.23,-.2,2.20),(.56,-.2,2.75),(.86,-.2,2.03),(.32,-.2,1.28),(-.30,-.2,.93)]
    for p,q in zip(pts,pts[1:]): a.beam(p,q,.16,.26,'steel')
    pts=[(.40,.15,.24),(.73,.15,.9),(.48,.15,1.66),(-.28,.15,2.45),(-.75,.15,2.04),(-.70,.15,1.27),(-.25,.15,.87)]
    for p,q in zip(pts,pts[1:]): a.beam(p,q,.16,.26,'brown')
    box(a,(.61,-.54,.28),(.33,.13,.06),'gold')

@fixture('civic_memorial')
def b18_sloped_memorial_plaque_pedestal(a):
    box(a,(0,0,.07),(.87,.57,.14),C)
    # Monument's sloping presentation surface is solid stone.
    vs=[(-.32,-.18,.14),(.32,-.18,.14),(.32,.18,.14),(-.32,.18,.14),(-.32,-.18,.70),(.32,-.18,.70),(.32,.18,1.02),(-.32,.18,1.02)]
    a.mesh(vs,[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],'concrete_light')
    box(a,(0,0,.883),(.55,.43,.022),'gold',rot=(.727,0,0))
    for y,w in ((-.12,.37),(-.05,.43),(.02,.39),(.09,.33)):
        box(a,(0,y*.75,.902+y*.666),(w,.012,.007),'brown',rot=(.727,0,0))
    for x in (-.238,.238):
        for y in (-.13,.13): ball(a,(x,y,.902+y*.89),.012,D)

@fixture('civic_marker')
def b18_carved_boundary_milestone(a):
    box(a,(0,0,.07),(.56,.45,.14),C)
    box(a,(0,0,.49),(.40,.31,.76),'concrete_light')
    roof(a,(0,0,.87),.43,.34,.12)
    box(a,(0,-.161,.58),(.29,.01,.33),C)
    # Deep inset crest and two geometric inscription rows.
    rod(a,(0,-.17,.63),(0,-.186,.63),.085,'gold',6)
    box(a,(0,-.178,.49),(.19,.006,.02),D)
    box(a,(0,-.178,.44),(.13,.006,.018),D)

@fixture('civic_weather_fixture','large')
def b18_directional_weather_vane_column(a):
    pole(a,2.1,.065,True)
    ball(a,(0,0,2.27),.15,'gold')
    rod(a,(0,0,2.26),(0,0,2.9),.026,D,8)
    for p,q in (((-.64,0,2.38),(.64,0,2.38)),((0,-.64,2.38),(0,.64,2.38))): rod(a,p,q,.015,D,6)
    for x,y in ((-.63,0),(.63,0),(0,-.63),(0,.63)):
        rod(a,(x,y,2.36),(x,y,2.55),.014,D,6)
        ball(a,(x,y,2.56),.036,'gold')
    rod(a,(-.66,0,2.78),(.62,0,2.78),.024,'gold',6)
    a.cone((.52,0,2.78),(.90,0,2.78),.12,'gold',4)
    box(a,(-.56,0,2.79),(.32,.022,.24),'gold')
    box(a,(-.69,0,2.79),(.03,.034,.27),D)

@fixture('civic_monument','large')
def b18_civic_bell_memorial(a):
    box(a,(0,0,.10),(1.55,.90,.20),C)
    for x in (-.56,.56):
        box(a,(x,0,1.20),(.16,.22,2.18),D)
        box(a,(x,0,.25),(.28,.34,.10),D)
        for y in (-.10,.1): rod(a,(x,y,.30),(x,y,.32),.026,S,6)
    box(a,(0,0,2.28),(1.39,.24,.19),'wood_dark')
    rod(a,(0,0,1.93),(0,0,2.27),.052,D,8)
    rod(a,(0,0,1.41),(0,0,1.72),.40,'gold',12,.22)
    rod(a,(0,0,1.72),(0,0,1.95),.22,'gold',12,.11)
    disk(a,(0,0,1.41),.45,.08,'gold',12)
    disk(a,(0,0,1.365),.345,.013,D,12)
    rod(a,(0,0,1.31),(0,0,1.53),.034,D,8)
    ball(a,(0,0,1.30),.073,'gold')
    tube(a,[(.10,0,2.18),(.27,0,1.9),(.34,0,1.24),(.38,0,.5)],.012,'cream',6)
    box(a,(0,-.455,.24),(.56,.019,.22),'gold')
    for z,w in ((.30,.36),(.24,.43),(.18,.29)): box(a,(0,-.468,z),(w,.007,.016),'brown')
