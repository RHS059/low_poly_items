"""Fifty waterfront, winter-service and outdoor-event props, metres, Z-up.

Muted municipal finishes, readable working parts, and individually constructed
silhouettes.  Every factory bakes its parts into one bottom-centred mesh.
"""
import math
from assetlib import Asset, register


def item(slug, family, size='person'):
    def decorate(fn):
        name = 'b20_' + slug
        def factory():
            a = Asset(name, family, size, style='muted detailed low-poly American city')
            fn(a)
            return a.bottom_center()
        register(name, family, size, factory)
        return factory
    return decorate


def rod(a, p, q, r=.018, m='steel', n=8):
    a.cylinder(p, q, r, m, n)


def disc(a, p, r, h=.025, m='steel', n=12):
    a.cylinder(p, (p[0], p[1], p[2]+h), r, m, n)


def taper(a, x, y, z, w, d, h, tw, td, m):
    v = [(x+sx*ww/2, y+sy*dd/2, zz)
         for ww, dd, zz in ((w,d,z),(tw,td,z+h))
         for sx,sy in ((-1,-1),(1,-1),(1,1),(-1,1))]
    a.mesh(v, [(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)], m)


def wheel(a, x, y, z, r=.15, width=.08):
    rod(a, (x-width/2,y,z), (x+width/2,y,z), r, 'rubber', 12)
    rod(a, (x-width*.56,y,z), (x+width*.56,y,z), r*.46, 'metal', 8)
    rod(a, (x-width*.6,y,z), (x+width*.6,y,z), r*.13, 'dark_metal', 8)


def handle(a, x, y, z, w=.2, h=.12, m='dark_metal'):
    a.tube([(x-w/2,y,z),(x-w/2,y,z+h),(x+w/2,y,z+h),(x+w/2,y,z)], .018, m, 6)


def bolt(a,x,y,z,r=.018):
    disc(a,(x,y,z),r,.012,'silver',6)


def plate(a,x,y,z,w,h,mat='cream'):
    a.box((x,y,z),(w,.008,h),mat)


def grille(a,x,y,z,w,h,n=6):
    a.box((x,y,z),(w,.012,h),'black')
    for i in range(n):
        a.box((x,y-.009,z-h*.43+i*h*.86/(n-1)),(w*.92,.016,.012),'metal')


def feet(a,w,d,z,thick=.04,m='dark_metal'):
    for x in (-w/2,w/2):
        for y in (-d/2,d/2):
            a.box((x,y,z/2),(thick,thick,z),m)
            a.box((x,y,.015),(thick*2,thick*2,.03),'rubber')


def base_bolts(a,w,d,z):
    for x in (-w*.38,w*.38):
        for y in (-d*.38,d*.38):
            bolt(a,x,y,z)


# WATERFRONT — 15
@item('cast_dock_mooring_cleat','waterfront')
def mooring(a):
    a.box((0,0,.028),(.52,.19,.056),'dark_metal')
    base_bolts(a,.52,.19,.056)
    taper(a,0,0,.05,.2,.11,.15,.13,.1,'dark_metal')
    a.beam((-.34,0,.24),(.34,0,.24),.08,.1,'dark_metal')
    a.beam((-.34,0,.24),(-.4,0,.28),.068,.075,'dark_metal')
    a.beam((.34,0,.24),(.4,0,.28),.068,.075,'dark_metal')


@item('lifering_emergency_stand','waterfront')
def lifering(a):
    a.box((0,0,.05),(.5,.4,.1),'concrete')
    a.box((0,.07,.91),(.07,.07,1.72),'dark_metal')
    a.box((0,.08,1.84),(.55,.05,.28),'white')
    plate(a,0,.05,1.85,.4,.07,'red')
    a.torus((0,-.01,1.16),.29,.068,'orange',axis='y',segments=16,sides=6)
    for t in (0,math.pi/2,math.pi,3*math.pi/2):
        x,z=.29*math.cos(t),1.16+.29*math.sin(t)
        a.box((x,-.065,z),(.12,.035,.075),'white',rot=(0,-t,0))
    a.torus((0,-.04,1.16),.395,.009,'cream',axis='y',segments=16,sides=5)
    a.box((0,.04,.63),(.17,.12,.19),'red')
    handle(a,0,-.035,.69,.09,.065,'silver')
    base_bolts(a,.5,.4,.1)


@item('dock_swim_ladder','waterfront')
def ladder(a):
    for x in (-.28,.28):
        a.tube([(x,.45,1.72),(x,.45,1.92),(x,.18,2.12),(x,-.13,2.12),(x,-.27,1.97),(x,-.27,.05)],.032,'steel',8)
        a.box((x,.45,1.58),(.15,.16,.04),'dark_metal')
        bolt(a,x,.45,1.6)
    for z in (.18,.5,.82,1.14,1.46):
        a.box((0,-.25,z),(.57,.15,.035),'metal')
        for y in (-.295,-.25,-.205):
            a.box((0,y,z+.021),(.47,.007,.008),'dark_metal')


@item('three_level_kayak_storage_rack','waterfront','large')
def kayakrack(a):
    for x in (-1.05,1.05):
        a.box((x,0,.06),(.15,1.65,.12),'wood_dark')
        a.box((x,0,1.13),(.11,.11,2.2),'wood_dark')
        for z in (.45,1.12,1.79):
            a.box((x,0,z),(.09,1.48,.08),'teal')
            for y in (-.59,.59):
                a.box((x,y,z+.045),(.1,.25,.02),'rubber')
                rod(a,(x,y*.8,z-.24),(x,y,z),.023,'metal')
        for y in (-.53,.53):
            a.beam((x,0,.64),(x,y,.14),.065,.06,'wood_dark')
    for z in (.14,2.08):
        a.box((0,.035,z),(2.2,.07,.075),'wood_dark')
    a.beam((-1.05,.08,.22),(1.05,.08,2.04),.05,.04,'metal')
    plate(a,0,-.006,2.08,.35,.055,'cream')


@item('marina_gear_handcart','waterfront')
def dockcart(a):
    a.box((0,0,.34),(.85,1.18,.09),'teal')
    for x in (-.39,.39):
        a.box((x,0,.53),(.055,1.18,.35),'teal')
    for y in (-.56,.56):
        a.box((0,y,.53),(.8,.05,.35),'teal')
    for x in (-.32,.32):
        for y in (-.39,.39):
            rod(a,(x,y,.15),(x,y,.3),.035,'steel')
            wheel(a,x,y,.145,.14,.075)
    for x in (-.36,.36):
        rod(a,(x,.5,.57),(x,.7,1.07),.026,'steel')
    rod(a,(-.36,.7,1.07),(.36,.7,1.07),.035,'rubber')
    for y in (-.4,-.2,0,.2,.4):
        a.box((0,y,.391),(.69,.009,.006),'dark_metal')


@item('boat_launch_hand_winch_pedestal','waterfront')
def winch(a):
    a.box((0,0,.04),(.54,.5,.08),'steel')
    base_bolts(a,.54,.5,.08)
    a.beam((0,0,.1),(0,.18,.97),.14,.13,'metal')
    for x in (-.16,.16):
        a.box((x,.18,1.03),(.035,.34,.38),'steel')
    rod(a,(-.19,.18,1.04),(.19,.18,1.04),.12,'dark_metal',12)
    for x in (-.18,.18):
        rod(a,(x-.015,.18,1.04),(x+.015,.18,1.04),.185,'metal',12)
    rod(a,(-.12,.18,1.04),(.12,.18,1.04),.145,'brown',12)
    a.beam((.22,.18,1.04),(.22,.36,1.28),.026,.035,'steel')
    rod(a,(.21,.36,1.28),(.36,.36,1.28),.035,'rubber')
    rod(a,(0,.05,1.08),(0,-.5,1.08),.012,'brown',6)
    a.torus((0,-.55,1.08),.05,.012,'steel',axis='x',segments=8,sides=5,arc=4.8)


@item('roller_boat_launch_cradle','waterfront','large')
def cradle(a):
    for x in (-.59,.59):
        a.box((x,0,.18),(.1,2.8,.14),'steel')
        for y in (-1.2,1.2):
            a.box((x,y,.07),(.32,.27,.14),'concrete')
    for y in (-1.05,-.35,.35,1.05):
        a.box((0,y,.22),(1.28,.075,.08),'metal')
        for s in (-1,1):
            p=(s*.12,y,.37);q=(s*.56,y,.51)
            rod(a,p,q,.087,'rubber',8)
            a.beam((s*.34,y,.23),(s*.34,y,.44),.06,.045,'steel')


@item('modular_floating_dock_section','waterfront','large')
def pontoon(a):
    for x in (-.65,.65):
        taper(a,x,0,.04,.67,2.58,.4,.82,2.7,'black')
    for x in (-.83,.83):
        a.box((x,0,.49),(.12,2.9,.17),'wood_dark')
    for j in range(14):
        y=-1.37+j*.21
        a.box((0,y,.59),(1.76,.196,.075),'wood_light' if j%4==0 else 'wood')
        for x in (-.78,.78): bolt(a,x,y,.629,.011)
    for y in (-1.46,1.46):
        a.box((0,y,.51),(1.8,.08,.15),'wood_dark')
    for x in (-.65,.65):
        a.box((x,1.54,.53),(.12,.17,.04),'steel')
        bolt(a,x,1.58,.55)


@item('hinged_marina_gangway','waterfront','large')
def gangway(a):
    for x in (-.57,.57):
        a.beam((x,-1.9,.12),(x,1.9,.65),.1,.15,'metal')
        for y in (-1.75,-.58,.58,1.75):
            z=.385+y*.53/3.8
            rod(a,(x,y,z),(x,y,z+1.03),.026,'steel')
        for h in (.52,1.02):
            rod(a,(x,-1.85,.13+h),(x,1.85,.65+h),.026,'steel')
    for i in range(23):
        y=-1.81+i*.165;z=.385+y*.53/3.8
        a.box((0,y,z),(1.11,.14,.034),'metal',rot=(math.atan(.53/3.8),0,0))
    rod(a,(-.66,-1.94,.12),(.66,-1.94,.12),.075,'dark_metal')
    for x in (-.43,.43): wheel(a,x,1.81,.55,.13,.075)


@item('marina_shore_power_pedestal','waterfront')
def shorepower(a):
    a.box((0,0,.05),(.43,.36,.1),'concrete')
    a.box((0,0,.7),(.29,.24,1.25),'cream')
    a.box((0,0,1.32),(.34,.29,.065),'navy')
    plate(a,0,-.126,1.11,.21,.2,'dark_metal')
    plate(a,0,-.135,1.13,.14,.11,'light')
    for x in (-.07,.07):
        rod(a,(x,-.125,.78),(x,-.17,.78),.052,'black',8)
        a.box((x,-.166,.83),(.107,.025,.018),'metal')
    grille(a,0,-.127,.38,.19,.19,5)
    plate(a,0,-.13,.99,.16,.025,'navy')
    base_bolts(a,.43,.36,.1)


@item('marina_sewage_pumpout_station','waterfront')
def pumpout(a):
    a.box((0,0,.075),(.8,.64,.15),'concrete')
    a.box((-.12,0,.62),(.46,.53,1.05),'teal')
    a.box((-.12,0,1.19),(.49,.56,.1),'cream')
    plate(a,-.12,-.269,.99,.31,.16,'cream')
    grille(a,-.12,-.274,.37,.31,.22,6)
    rod(a,(.17,0,.91),(.32,0,.91),.05,'steel')
    for z in (.53,.61,.69):
        a.torus((.3,0,z),.25,.035,'rubber',segments=12,sides=6)
    a.tube([(.48,0,.68),(.6,-.16,.68),(.59,-.33,.36)],.035,'rubber',8)
    rod(a,(.59,-.33,.35),(.59,-.33,.18),.055,'steel')
    a.box((.64,-.33,.31),(.13,.06,.03),'red')


@item('dock_corner_rubber_fender','waterfront')
def cornerfender(a):
    a.box((0,.045,.31),(.6,.1,.62),'metal')
    a.box((.255,.27,.31),(.09,.54,.62),'metal')
    for z in (.1,.3,.5):
        a.beam((-.3,-.04,z),(.3,-.04,z),.14,.12,'rubber')
        a.beam((.3,-.04,z),(.3,.54,z),.14,.12,'rubber')
    for x in (-.23,.21):
        for z in (.06,.57):
            rod(a,(x,-.023,z),(x,-.042,z),.022,'silver',6)


@item('dock_piling_protective_sleeve','waterfront')
def piling(a):
    rod(a,(0,0,0),(0,0,1.55),.2,'wood_dark',10)
    rod(a,(0,0,.16),(0,0,1.33),.234,'rubber',10)
    for z in (.24,.68,1.14):
        a.torus((0,0,z),.232,.032,'rubber',segments=10,sides=5)
    a.cone((0,0,1.55),(0,0,1.72),.24,'white',10)
    for z in (.23,1.15):
        rod(a,(0,-.259,z),(0,-.279,z),.023,'steel',6)


@item('channel_marker_buoy','waterfront')
def buoy(a):
    a.cylinder((0,0,.12),(0,0,.55),.45,'green',12,radius2=.39)
    a.cylinder((0,0,.02),(0,0,.12),.22,'dark_metal',12,radius2=.45)
    a.cylinder((0,0,.55),(0,0,.85),.39,'green',12,radius2=.2)
    rod(a,(0,0,.85),(0,0,1.62),.08,'green')
    a.box((0,0,1.4),(.33,.06,.43),'green')
    plate(a,0,-.035,1.4,.16,.27,'white')
    a.box((0,-.042,1.4),(.052,.012,.18),'green')
    disc(a,(0,0,1.66),.12,.04,'dark_metal')
    disc(a,(0,0,1.7),.07,.11,'light')
    a.torus((0,0,.92),.072,.018,'steel',axis='y',segments=10,sides=5)


@item('fishing_line_recycling_tube','waterfront')
def linebin(a):
    a.box((0,0,.04),(.34,.32,.08),'concrete')
    a.box((0,.065,.72),(.065,.065,1.38),'wood_dark')
    rod(a,(0,-.045,.35),(0,-.045,1.17),.11,'white',10)
    disc(a,(0,-.045,.33),.125,.045,'white',10)
    rod(a,(0,-.045,1.15),(0,-.19,1.28),.11,'white',10)
    rod(a,(0,-.21,1.285),(0,-.232,1.285),.079,'black',10)
    for z in (.53,.97):
        a.torus((0,-.045,z),.112,.012,'metal',segments=10,sides=4)
    plate(a,0,-.156,.78,.14,.2,'blue')
    plate(a,0,-.163,.81,.1,.025,'white')


# WINTER — 15
@item('municipal_salt_grit_bunker','winter_equipment')
def saltbin(a):
    taper(a,0,0,.07,.88,.6,.66,1.05,.75,'yellow')
    a.box((0,0,.78),(1.11,.8,.105),'dark_metal',rot=(.06,0,0))
    for x in (-.4,.4):
        a.box((x,0,.045),(.11,.61,.09),'black')
    handle(a,0,-.417,.74,.25,.055,'black')
    plate(a,0,-.353,.46,.38,.18,'cream')
    for x in (-.3,.3):
        a.box((x,.39,.74),(.13,.06,.09),'metal')
    for x in (-.43,.43):
        a.box((x,-.349,.42),(.024,.024,.4),'yellow')


@item('wide_push_snow_shovel','winter_equipment','handheld')
def snowshovel(a):
    a.box((0,0,.16),(.68,.07,.31),'navy',rot=(-.2,0,0))
    a.box((0,-.04,.028),(.69,.12,.035),'steel')
    for x in (-.29,-.145,0,.145,.29):
        a.box((x,.042,.18),(.018,.018,.25),'dark_metal',rot=(-.2,0,0))
    rod(a,(0,.04,.18),(0,.47,1.31),.019,'wood_light',8)
    a.tube([(-.1,.47,1.31),(-.1,.5,1.46),(.1,.5,1.46),(.1,.47,1.31)],.019,'dark_metal',6)
    rod(a,(-.1,.47,1.31),(.1,.47,1.31),.018,'dark_metal',6)


@item('wheeled_snow_scoop','winter_equipment')
def snowscoop(a):
    a.box((0,-.12,.1),(.8,.66,.07),'navy',rot=(.11,0,0))
    a.box((0,.21,.28),(.8,.07,.4),'navy',rot=(-.25,0,0))
    for x in (-.38,.38):
        a.box((x,-.05,.21),(.04,.63,.26),'navy')
        wheel(a,x,.3,.18,.18,.08)
        rod(a,(x,.3,.3),(x,.71,1.05),.025,'metal')
    rod(a,(-.38,.71,1.05),(.38,.71,1.05),.033,'rubber')
    a.box((0,-.47,.04),(.83,.08,.035),'steel')


@item('two_stage_walkbehind_snowblower','winter_equipment')
def snowblower(a):
    a.box((0,.1,.31),(.54,.7,.21),'dark_metal')
    for x in (-.36,.36): wheel(a,x,.23,.26,.26,.16)
    a.box((0,.07,.56),(.42,.44,.3),'red')
    a.box((0,.13,.755),(.32,.33,.09),'black')
    grille(a,0,-.161,.57,.31,.18,5)
    for x in (-.33,.33):
        a.box((x,-.45,.27),(.045,.48,.48),'red')
    a.box((0,-.25,.3),(.69,.065,.5),'red')
    a.box((0,-.5,.057),(.72,.43,.044),'steel')
    rod(a,(-.34,-.46,.25),(.34,-.46,.25),.042,'steel')
    for x in (-.22,-.08,.08,.22):
        a.torus((x,-.46,.25),.15,.028,'dark_metal',axis='x',segments=8,sides=4)
    rod(a,(0,-.2,.52),(0,-.2,.96),.095,'red')
    a.box((0,-.28,1.04),(.2,.3,.17),'red',rot=(-.35,0,0))
    a.box((0,-.434,1.08),(.14,.012,.12),'black',rot=(-.35,0,0))
    for x in (-.26,.26):
        rod(a,(x,.3,.49),(x,.8,1.12),.024,'metal')
        rod(a,(x,.8,1.12),(x,1.02,1.12),.031,'rubber')
    a.box((0,.78,1.07),(.56,.19,.045),'black')
    rod(a,(.1,.77,1.09),(.1,.75,1.23),.012,'steel')
    a.sphere((.1,.75,1.23),.029,'black',8,3)


@item('sidewalk_broadcast_salt_spreader','winter_equipment')
def spreader(a):
    taper(a,0,0,.44,.19,.18,.47,.62,.53,'yellow')
    a.box((0,0,.93),(.65,.56,.045),'black')
    rod(a,(-.39,0,.2),(.39,0,.2),.025,'metal')
    for x in (-.34,.34):
        wheel(a,x,0,.2,.2,.1)
        rod(a,(x*.65,0,.3),(x*.65,.46,1.02),.02,'steel')
    rod(a,(-.23,.46,1.02),(.23,.46,1.02),.027,'rubber')
    rod(a,(0,0,.18),(0,0,.46),.028,'metal')
    disc(a,(0,0,.32),.2,.023,'metal',10)
    for t in (0,math.pi/2,math.pi,3*math.pi/2):
        a.box((.1*math.cos(t),.1*math.sin(t),.35),(.18,.018,.04),'metal',rot=t)
    rod(a,(0,.07,.48),(0,.42,.98),.007,'black',5)


@item('reflective_driveway_snow_marker','winter_equipment')
def snowmarker(a):
    a.cone((0,0,.08),(0,0,0),.022,'steel',6)
    rod(a,(0,0,.08),(0,0,1.53),.015,'orange',6)
    rod(a,(0,0,1.23),(0,0,1.44),.019,'white',6)
    a.sphere((0,0,1.55),(.055,.024,.055),'orange',8,3)
    rod(a,(0,-.026,1.55),(0,-.032,1.55),.04,'white',8)


@item('sidewalk_ice_chopper','winter_equipment','handheld')
def icechopper(a):
    taper(a,0,0,0,.19,.018,.14,.1,.045,'steel')
    a.box((0,0,.02),(.2,.025,.025),'dark_metal')
    rod(a,(0,0,.14),(0,0,.28),.028,'metal')
    rod(a,(0,0,.26),(0,0,1.37),.016,'wood_light')
    rod(a,(0,0,1.19),(0,0,1.42),.022,'rubber')
    a.torus((0,0,1.42),.026,.008,'black',segments=8,sides=4)


@item('telescopic_roof_snow_rake','winter_equipment','handheld')
def roofrake(a):
    a.box((0,0,.2),(.66,.055,.4),'navy')
    a.box((0,.03,.4),(.69,.05,.035),'metal')
    rod(a,(0,.04,.24),(0,.33,.27),.018,'steel')
    for x in (-.25,.25):
        rod(a,(x,.03,.23),(0,.3,.27),.012,'metal',6)
    rod(a,(0,.31,.27),(0,.58,1.58),.018,'steel')
    rod(a,(0,.58,1.58),(0,.85,2.94),.015,'steel')
    rod(a,(0,.565,1.5),(0,.585,1.6),.025,'black')
    rod(a,(0,.8,2.67),(0,.87,3.0),.021,'rubber')


@item('winter_maintenance_storage_locker','winter_equipment')
def snowlocker(a):
    a.box((0,0,.07),(.88,.58,.14),'dark_metal')
    a.box((0,.25,.97),(.84,.045,1.8),'green')
    for x in (-.41,.41): a.box((x,0,.97),(.045,.55,1.8),'green')
    a.box((0,0,1.89),(.9,.61,.07),'green')
    a.box((0,-.275,.98),(.78,.04,1.72),'green')
    grille(a,0,-.3,1.6,.6,.24,6)
    plate(a,0,-.304,1.13,.38,.15,'cream')
    handle(a,.25,-.33,.78,.07,.18,'silver')
    for z in (.32,1.61): a.box((-.36,-.3,z),(.045,.04,.16),'metal')
    a.box((0,-.3,.33),(.62,.027,.018),'dark_metal')


@item('snowplow_blade_storage_dolly','winter_equipment','large')
def plowdolly(a):
    for x in (-.83,.83):
        a.box((x,0,.14),(.12,.8,.1),'dark_metal')
        for y in (-.32,.32): wheel(a,x,y,.085,.08,.055)
    a.box((0,.19,.19),(1.82,.1,.1),'dark_metal')
    for i in range(5):
        z=.23+i*.145;y=-.25+.05*(i-2)**2
        a.box((0,y,z),(2.12,.065,.17),'yellow',rot=(.18*(i-2),0,0))
    a.box((0,-.048,.175),(2.16,.055,.09),'steel')
    for x in (-.82,0,.82):
        a.beam((x,.23,.24),(x,.24,.87),.055,.06,'dark_metal')
    for x in (-.37,.37):
        a.beam((x,.2,.42),(x,.69,.35),.1,.09,'dark_metal')
        rod(a,(x,.25,.65),(x,.62,.43),.045,'metal')


@item('brine_mixing_service_cart','winter_equipment')
def brinecart(a):
    a.box((0,0,.24),(.72,.83,.08),'dark_metal')
    for x in (-.32,.32):
        for y in (-.31,.31): wheel(a,x,y,.13,.13,.07)
    rod(a,(0,0,.29),(0,0,1.01),.29,'cream',12)
    disc(a,(0,0,1.01),.3,.05,'navy')
    disc(a,(.07,0,1.06),.07,.04,'black')
    plate(a,0,-.294,.7,.23,.19,'blue')
    for z in (.39,.86): a.torus((0,0,z),.296,.018,'steel',segments=12,sides=4)
    a.box((.37,0,.43),(.22,.29,.21),'teal')
    a.tube([(.34,0,.44),(.48,-.25,.44),(.41,-.37,.82),(0,-.32,.93)],.018,'rubber',6)
    for x in (-.3,.3): rod(a,(x,.36,.3),(x,.47,1.11),.023,'steel')
    rod(a,(-.3,.47,1.11),(.3,.47,1.11),.03,'rubber')


@item('towable_ice_grit_sledge','winter_equipment')
def gritsledge(a):
    for x in (-.31,.31):
        a.beam((x,-.53,.05),(x,.4,.05),.075,.055,'steel')
        a.beam((x,-.53,.05),(x,-.66,.2),.075,.055,'steel')
    taper(a,0,0,.12,.62,.78,.37,.76,.93,'navy')
    a.box((0,0,.5),(.71,.88,.025),'sand')
    for x in (-.31,.31): rod(a,(x,-.44,.4),(x,-1.03,.58),.02,'steel')
    rod(a,(-.31,-1.03,.58),(.31,-1.03,.58),.028,'rubber')
    for x in (-.3,.3):
        for y in (-.35,.35): bolt(a,x,y,.505,.012)


@item('snow_boot_brush_station','winter_equipment')
def bootbrush(a):
    a.box((0,0,.045),(.7,.46,.09),'concrete')
    a.box((0,0,.12),(.46,.29,.07),'dark_metal')
    for x in (-.22,.22):
        a.box((x,0,.215),(.08,.28,.14),'wood_dark')
        for j in range(7):
            a.box((x*.77,-.115+j*.038,.22),(.07,.022,.095),'brown')
    for i in range(6):
        a.box((-.135+i*.054,0,.177),(.03,.25,.055),'brown')
    for x in (-.32,.32):
        rod(a,(x,.17,.05),(x,.17,1.0),.026,'dark_metal')
    rod(a,(-.32,.17,1.0),(.32,.17,1.0),.028,'dark_metal')


@item('bagged_road_salt_pallet','winter_equipment')
def saltpallet(a):
    for x in (-.42,0,.42): a.box((x,0,.09),(.12,.85,.16),'wood_dark')
    for y in (-.38,-.19,0,.19,.38): a.box((0,y,.2),(1.05,.13,.065),'wood')
    for level in range(3):
        for x in (-.255,.255):
            for y in (-.215,.215):
                z=.255+level*.19
                taper(a,x,y,z,.4,.32,.045,.46,.38,'cream')
                taper(a,x,y,z+.045,.46,.38,.12,.4,.32,'cream')
                a.box((x,y,z+.169),(.18,.29,.008),'blue')
                a.box((x,y,z+.176),(.12,.025,.006),'white')
    for x in (-.45,.45): a.box((x,0,.52),(.025,.83,.58),'white')


@item('heated_walkway_mat_controller','winter_equipment','large')
def heatmat(a):
    a.box((0,-.15,.018),(.94,2.12,.036),'rubber')
    for y in [i*.16-.98 for i in range(12)]:
        a.box((0,y,.041),(.88,.016,.012),'dark_metal')
    for x in (-.445,.445): a.box((x,-.15,.046),(.022,2.08,.014),'yellow')
    a.box((.71,.65,.035),(.35,.4,.07),'concrete')
    a.box((.71,.65,.59),(.055,.055,1.05),'metal')
    a.box((.71,.63,.9),(.24,.15,.32),'dark_metal')
    plate(a,.71,.548,.96,.15,.085,'glass')
    rod(a,(.71,.549,.84),(.71,.529,.84),.025,'red',8)
    a.tube([(.43,.68,.06),(.63,.85,.07),(.81,.8,.25),(.81,.63,.74)],.013,'black',6)


# OUTDOOR EVENTS — 20
@item('pop_up_event_canopy','outdoor_event','large')
def canopy(a):
    for x in (-1.4,1.4):
        for y in (-1.4,1.4):
            rod(a,(x,y,.04),(x,y,2.22),.023,'steel')
            a.box((x,y,.023),(.14,.14,.046),'dark_metal')
            a.box((x,y,1.68),(.065,.065,.14),'black')
    taper(a,0,0,2.2,3.03,3.03,.63,.03,.03,'cream')
    for x in (-1.5,1.5): a.box((x,0,2.15),(.035,3.03,.18),'cream')
    for y in (-1.5,1.5): a.box((0,y,2.15),(3.03,.035,.18),'cream')
    for y in (-1.4,1.4):
        for s in (-1,1):
            rod(a,(s*1.4,y,1.93),(0,y,2.24),.014,'metal',6)
            rod(a,(s*1.4,y,2.24),(0,y,1.93),.014,'metal',6)


@item('pagoda_festival_marquee','outdoor_event','large')
def pagoda(a):
    for x in (-1.9,1.9):
        for y in (-1.9,1.9):
            a.box((x,y,1.25),(.11,.11,2.5),'white')
            a.box((x,y,.04),(.3,.3,.08),'metal')
    taper(a,0,0,2.5,4.1,4.1,.37,2.0,2.0,'cream')
    taper(a,0,0,2.87,2,2,.45,.7,.7,'cream')
    taper(a,0,0,3.32,.7,.7,.72,.03,.03,'cream')
    a.sphere((0,0,4.08),.065,'gold',8,3)
    for x in (-2.02,2.02): a.box((x,0,2.4),(.035,4.06,.2),'navy')
    for y in (-2.02,2.02): a.box((0,y,2.4),(4.06,.035,.2),'navy')
    for x in (-1.88,1.88):
        a.box((x,0,1.33),(.035,3.71,2.12),'cream')
        for y in (-1.15,0,1.15):
            a.box((x*1.011,y,1.42),(.025,.84,.84),'glass')
            a.box((x*1.021,y,1.42),(.021,.035,.83),'cream')
    a.box((0,1.88,1.33),(3.71,.035,2.12),'cream')


@item('portable_festival_restroom','outdoor_event')
def toilet(a):
    a.box((0,0,.075),(1.12,1.13,.15),'black')
    a.box((0,.51,1.14),(1.04,.055,2.07),'teal')
    for x in (-.5,.5):
        a.box((x,0,1.14),(.06,1.04,2.07),'teal')
        for y in (-.31,0,.31): a.box((x*1.045,y,1.11),(.028,.035,1.7),'teal')
    a.box((0,-.5,1.12),(.97,.075,2.03),'teal')
    a.box((0,-.545,1.12),(.79,.025,1.86),'navy')
    taper(a,0,0,2.15,1.12,1.13,.17,.94,.96,'cream')
    grille(a,0,-.565,1.86,.57,.13,4)
    plate(a,0,-.563,1.57,.26,.27,'white')
    handle(a,.29,-.581,.94,.06,.16,'steel')
    plate(a,.26,-.601,1.17,.08,.04,'green')
    for z in (.53,1.65): a.box((-.385,-.57,z),(.05,.04,.15),'metal')
    rod(a,(.38,.4,1.9),(.38,.4,2.41),.045,'black')
    disc(a,(.38,.4,2.4),.075,.035,'black')


@item('portable_outdoor_shower_cubicle','outdoor_event')
def shower(a):
    a.box((0,0,.09),(1.18,1.22,.18),'dark_metal')
    for x in (-.53,.53):
        a.box((x,0,1.25),(.075,1.13,2.18),'cream')
    a.box((0,.54,1.25),(1.11,.075,2.18),'cream')
    a.box((0,0,2.36),(1.19,1.2,.1),'teal')
    rod(a,(-.5,-.51,2.18),(.5,-.51,2.18),.023,'steel')
    for i in range(9):
        x=-.44+i*.11;y=-.54+(.035 if i%2 else 0)
        a.box((x,y,1.2),(.12,.03,1.85),'teal')
        a.torus((x,-.51,2.13),.043,.007,'steel',axis='x',segments=8,sides=4)
    for y in (-.43,-.22,0,.22,.43): a.box((0,y,.2),(.99,.13,.03),'wood')
    rod(a,(0,.45,1.03),(0,.45,2.12),.018,'steel')
    rod(a,(0,.45,2.12),(0,.23,2.12),.018,'steel')
    disc(a,(0,.23,2.05),.08,.025,'steel',10)
    a.box((0,.49,2.51),(.59,.43,.24),'black')
    plate(a,0,-.617,2.34,.36,.06,'white')


@item('dual_pump_handwash_station','outdoor_event')
def handwash(a):
    taper(a,0,0,.06,.82,.66,.73,.74,.58,'cream')
    for x in (-.2,.2):
        a.box((x,-.07,.84),(.35,.41,.12),'teal')
        a.box((x,-.1,.906),(.27,.3,.012),'dark_metal')
        a.box((x,-.1,.913),(.22,.25,.008),'metal')
        a.tube([(x,.1,.88),(x,.1,1.09),(x,-.04,1.09),(x,-.04,1.04)],.015,'steel',6)
        a.box((x,-.31,.11),(.18,.13,.04),'dark_metal',rot=(.14,0,0))
    a.box((0,.24,1.07),(.79,.07,.49),'teal')
    a.box((0,.192,1.14),(.2,.08,.24),'cream')
    a.box((0,.138,1.12),(.12,.03,.05),'black')
    plate(a,0,.195,.99,.1,.04,'blue')
    disc(a,(.24,.17,.8),.055,.03,'black')


@item('retractable_belt_queue_stanchion','outdoor_event')
def stanchion(a):
    a.cylinder((0,0,.01),(0,0,.075),.19,'black',12,radius2=.14)
    rod(a,(0,0,.075),(0,0,.89),.035,'steel',10)
    rod(a,(0,0,.86),(0,0,1.02),.06,'black',10)
    a.box((.275,0,.96),(.45,.02,.075),'navy')
    a.box((.51,0,.96),(.025,.05,.095),'black')
    disc(a,(0,0,1.02),.064,.017,'dark_metal',10)


@item('festival_ticket_inspection_podium','outdoor_event')
def ticketpodium(a):
    a.box((0,0,.04),(.66,.51,.08),'black')
    taper(a,0,0,.08,.5,.39,.88,.57,.45,'navy')
    a.box((0,0,1.0),(.76,.58,.065),'wood_dark')
    plate(a,0,-.226,.71,.4,.14,'cream')
    a.box((.17,0,1.08),(.19,.27,.12),'black',rot=(.12,0,0))
    a.box((.17,-.025,1.153),(.12,.13,.012),'glass',rot=(.12,0,0))
    a.box((-.19,.11,1.085),(.17,.14,.12),'cream')
    a.box((-.19,.1,1.15),(.11,.015,.01),'black')
    for x in (-.21,.21):
        a.box((x,-.226,.38),(.014,.018,.53),'metal')


@item('pa_loudspeaker_on_tripod','outdoor_event')
def loudspeaker(a):
    rod(a,(0,0,.12),(0,0,1.72),.033,'dark_metal')
    for t in (0,2.0944,4.1888):
        x,y=.56*math.cos(t),.56*math.sin(t)
        rod(a,(0,0,.62),(x,y,.055),.023,'dark_metal')
        a.box((x,y,.033),(.11,.075,.045),'rubber',rot=t)
    a.box((0,0,1.93),(.45,.34,.68),'black')
    plate(a,0,-.176,1.93,.38,.59,'dark_metal')
    rod(a,(0,-.181,1.81),(0,-.19,1.81),.137,'black',12)
    a.torus((0,-.195,1.81),.126,.009,'metal',axis='y',segments=12,sides=4)
    a.box((0,-.19,2.13),(.25,.013,.105),'black')
    for x in (-.218,.218): a.box((x,0,1.98),(.025,.14,.19),'dark_metal')
    a.box((0,.183,1.8),(.12,.026,.13),'metal')


@item('stage_floor_monitor_wedge','outdoor_event')
def monitor(a):
    # Trapezoidal side profile extruded across its width.
    v=[(x,y,z) for x in (-.29,.29) for y,z in ((-.28,.035),(.24,.035),(.24,.4),(.13,.4))]
    a.mesh(v,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'black')
    a.box((0,-.058,.237),(.51,.52,.018),'dark_metal',rot=(.735,0,0))
    rod(a,(0,-.105,.25),(0,-.12,.266),.14,'black',12)
    for x in (-.22,.22):
        for y in (-.17,.17): a.box((x,y,.02),(.08,.08,.04),'rubber')
    a.box((.294,.045,.16),(.014,.13,.08),'metal')
    a.box((.303,.045,.16),(.013,.09,.04),'black')


@item('wheeled_audio_flight_case','outdoor_event')
def flightcase(a):
    a.box((0,0,.48),(.83,.55,.66),'black')
    for x in (-.41,.41):
        for y in (-.27,.27): a.box((x,y,.49),(.028,.028,.69),'silver')
    for z in (.155,.68,.815):
        for y in (-.28,.28): a.box((0,y,z),(.85,.025,.025),'silver')
        for x in (-.42,.42): a.box((x,0,z),(.025,.55,.025),'silver')
    for x in (-.31,.31):
        for y in (-.18,.18):
            rod(a,(x,y,.09),(x,y,.15),.018,'metal')
            wheel(a,x,y,.069,.065,.045)
    for x in (-.24,.24):
        a.box((x,-.296,.67),(.065,.027,.12),'metal')
        a.box((x,-.317,.67),(.025,.025,.064),'dark_metal')
    handle(a,0,-.3,.42,.22,.09,'silver')
    plate(a,0,-.299,.31,.22,.09,'cream')


@item('portable_audio_mixing_console','outdoor_event')
def mixing(a):
    for x in (-.45,.45):
        a.beam((x,-.29,.04),(x,.25,.85),.04,.05,'dark_metal')
        a.beam((x,.29,.04),(x,-.25,.85),.04,.05,'dark_metal')
        rod(a,(x,-.31,.04),(x,.31,.04),.025,'rubber')
    a.box((0,0,.9),(1.05,.66,.13),'black',rot=(.12,0,0))
    a.box((0,0,.973),(.95,.6,.02),'dark_metal',rot=(.12,0,0))
    for i in range(10):
        x=-.41+i*.077
        for j in range(3):
            y=.03+j*.08
            disc(a,(x,y,.98+y*.12),.014,.022,'metal' if j else 'navy',6)
        a.box((x,-.16,.967),(.008,.18,.011),'black',rot=(.12,0,0))
        a.box((x,-.22+(i%3)*.05,.988),(.035,.032,.018),'white')
    a.box((.385,.12,1.005),(.14,.2,.012),'glass',rot=(.12,0,0))
    for x in (-.51,.51): a.box((x,0,.94),(.045,.68,.14),'wood_dark',rot=(.12,0,0))


@item('modular_stage_riser','outdoor_event','large')
def stage(a):
    a.box((0,0,.72),(2.4,1.22,.09),'black')
    for y in (-.59,.59): a.box((0,y,.657),(2.4,.035,.06),'silver')
    for x in (-1.18,1.18): a.box((x,0,.657),(.035,1.18,.06),'silver')
    feet(a,2.18,1.0,.66,.065,'metal')
    for y in (-.5,.5):
        a.beam((-1.09,y,.2),(1.09,y,.61),.03,.028,'metal')
        a.beam((1.09,y,.2),(-1.09,y,.61),.03,.028,'metal')
    for x in (-1.09,1.09):
        for y in (-.5,.5):
            disc(a,(x,y,.03),.09,.018,'dark_metal',8)
            rod(a,(x,y,.04),(x,y,.14),.025,'silver')


@item('portable_stage_stair_module','outdoor_event')
def stagestairs(a):
    for i in range(4):
        y=-.54+i*.34;z=.18+i*.18
        a.box((0,y,z),(.98,.34,.07),'black')
        a.box((0,y-.162,z+.042),(.95,.035,.012),'yellow')
        for x in (-.43,.43):
            a.box((x,y,z/2),(.045,.045,z),'metal')
    for x in (-.48,.48):
        a.beam((x,-.68,.06),(x,.64,.7),.06,.075,'metal')
        for y,z in ((-.58,.19),(.52,.73)):
            rod(a,(x,y,z),(x,y,z+.86),.024,'metal')
        rod(a,(x,-.68,.99),(x,.64,1.57),.026,'metal')


@item('event_lighting_truss_goalpost','outdoor_event','large')
def truss(a):
    for x in (-1.7,1.7):
        a.box((x,0,.025),(.74,.72,.05),'dark_metal')
        for dx in (-.13,.13):
            for y in (-.13,.13): rod(a,(x+dx,y,.05),(x+dx,y,3.0),.025,'silver')
        for k in range(6):
            z=.13+k*.46
            for y in (-.13,.13):
                rod(a,(x-.13,y,z),(x+.13,y,z+.43),.014,'silver',6)
            for dx in (-.13,.13):
                rod(a,(x+dx,-.13,z),(x+dx,.13,z+.43),.014,'silver',6)
    for y in (-.13,.13):
        for z in (2.74,3.0): rod(a,(-1.7,y,z),(1.7,y,z),.025,'silver')
        for k in range(8):
            x=-1.7+k*.425
            rod(a,(x,y,2.74),(x+.425,y,3.0),.014,'silver',6)
    for x in (-1.05,0,1.05):
        a.box((x,0,2.62),(.25,.24,.13),'black')
        rod(a,(x,0,2.47),(x,-.09,2.29),.1,'black',10)
        rod(a,(x,-.09,2.287),(x,-.1,2.265),.084,'light',10)
        rod(a,(x,0,2.71),(x,0,2.59),.025,'dark_metal')


@item('folding_banquet_service_table','outdoor_event','large')
def banquet(a):
    a.box((0,0,.74),(1.82,.76,.065),'cream')
    a.box((0,0,.699),(1.7,.66,.025),'dark_metal')
    for x in (-.63,.63):
        for y in (-.27,.27):
            rod(a,(x,y,.71),(x*.91,y*1.08,.045),.024,'steel')
            a.box((x*.91,y*1.08,.03),(.07,.07,.055),'rubber')
        rod(a,(x,-.28,.18),(x,.28,.18),.017,'steel')
        rod(a,(x,0,.42),(x*.38,0,.7),.014,'metal',6)
    a.box((0,0,.779),(.008,.72,.005),'metal')


@item('interlocking_portable_dance_floor','outdoor_event','large')
def dancefloor(a):
    a.box((0,0,.025),(2.5,2.5,.05),'dark_metal')
    for ix in range(4):
        for iy in range(4):
            x=-.93+ix*.62;y=-.93+iy*.62
            for j in range(4):
                if (ix+iy)%2:
                    a.box((x-.225+j*.15,y,.067),(.143,.596,.04),'wood' if j%2 else 'wood_light')
                else:
                    a.box((x,y-.225+j*.15,.067),(.596,.143,.04),'wood' if j%2 else 'wood_light')
    for x in (-1.27,1.27): a.box((x,0,.047),(.055,2.6,.045),'silver')
    for y in (-1.27,1.27): a.box((0,y,.047),(2.6,.055,.045),'silver')
    for x in (-.84,0,.84): a.box((x,1.309,.029),(.09,.042,.023),'metal')


@item('outdoor_speaking_lectern','outdoor_event')
def lectern(a):
    a.box((0,0,.035),(.61,.46,.07),'dark_metal')
    for x in (-.22,.22): a.beam((x,.06,.07),(x,.09,1.05),.065,.07,'wood_dark')
    a.box((0,-.02,.7),(.45,.04,.66),'wood')
    a.box((0,0,1.1),(.65,.47,.055),'wood_dark',rot=(.16,0,0))
    a.box((0,-.228,1.098),(.65,.026,.065),'wood_dark')
    plate(a,0,-.047,.8,.25,.2,'navy')
    a.tube([(.23,.13,1.15),(.23,.14,1.38),(.12,0,1.46)],.012,'black',6)
    rod(a,(.12,0,1.46),(.08,-.055,1.46),.021,'black',8)


@item('five_channel_event_cable_ramp','outdoor_event')
def cableramp(a):
    # Chamfered cross section and separate lift-up lid.
    taper(a,0,0,0,1.02,.6,.08,1.02,.33,'rubber')
    a.box((0,0,.086),(.97,.26,.026),'yellow')
    for x in (-.38,-.19,0,.19,.38):
        a.box((x,0,.102),(.04,.24,.007),'dark_metal')
    for x in (-.45,-.22,0,.22,.45):
        a.box((x,.159,.072),(.1,.036,.022),'black')
    for y in (-.17,0,.17):
        a.box((.535,y,.038),(.06,.067,.045),'rubber')
    for x in (-.38,-.18,.02,.22,.42):
        a.box((x,-.232,.042),(.11,.013,.01),'dark_metal',rot=(.2,0,0))


@item('event_tent_ballast_water_tank','outdoor_event')
def ballast(a):
    taper(a,0,0,.035,.69,.68,.72,.62,.61,'cream')
    for x in (-.3,.3): a.box((x,0,.04),(.12,.69,.08),'black')
    for z in (.22,.42,.62):
        for y in (-.325,.325): a.box((0,y,z),(.64,.026,.047),'cream')
    disc(a,(.13,0,.755),.09,.025,'black',10)
    a.box((-.22,0,.4),(.045,.65,.74),'dark_metal')
    rod(a,(-.23,.0,.73),(-.23,.0,.98),.031,'metal')
    a.torus((-.23,0,.98),.07,.018,'steel',axis='y',segments=10,sides=5)
    handle(a,.12,-.318,.56,.18,.075,'cream')
    rod(a,(.15,-.327,.12),(.15,-.38,.12),.035,'black',8)


@item('outdoor_event_misting_fan','outdoor_event')
def mistfan(a):
    a.box((0,0,.08),(.57,.5,.16),'dark_metal')
    taper(a,0,0,.16,.47,.42,.53,.42,.38,'cream')
    disc(a,(.12,.07,.69),.055,.025,'black',8)
    rod(a,(0,.08,.69),(0,.08,1.49),.034,'metal')
    rod(a,(0,-.02,1.67),(0,.21,1.67),.07,'black',10)
    a.torus((0,-.045,1.67),.36,.022,'dark_metal',axis='y',segments=16,sides=5)
    a.torus((0,.13,1.67),.36,.018,'dark_metal',axis='y',segments=16,sides=5)
    for t in [i*math.pi/4 for i in range(8)]:
        x,z=.355*math.cos(t),1.67+.355*math.sin(t)
        rod(a,(x,-.045,z),(x,.13,z),.012,'metal',6)
        rod(a,(0,-.058,1.67),(x,-.045,z),.009,'metal',5)
    for t in (0,2.0944,4.1888):
        a.box((.16*math.cos(t),.01,1.67+.16*math.sin(t)),(.28,.026,.095),'metal',rot=(0,-t,0))
    a.tube([(.15,.11,.7),(.14,.15,1.44),(.25,.1,1.7)],.01,'black',5)
    for t in (0,math.pi/2,math.pi,3*math.pi/2):
        x,z=.35*math.cos(t),1.67+.35*math.sin(t)
        rod(a,(x,-.055,z),(x,-.08,z),.015,'gold',6)
