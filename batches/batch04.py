"""Fifty purpose-built outdoor refuse, recycling, and street-cleaning props."""
from math import cos, sin, pi
from assetlib import Asset, register

CATEGORY = 'waste_recycling_street_cleaning'
NAMES = []

def item(slug, size='person'):
    def deco(build):
        name = 'b04_' + slug
        def factory():
            a = Asset(name, CATEGORY, size)
            build(a)
            return a.bottom_center()
        register(name, CATEGORY, size, factory)
        NAMES.append(name)
        return factory
    return deco

def box(a, c, s, m='metal', rot=None):
    a.box(c, s, mat=m, rot=rot)

def rod(a, p, q, r=.018, m='metal', sides=8):
    a.cylinder(p, q, r, mat=m, sides=sides)

def wheel(a, x, y, z, r=.14, w=.08):
    rod(a, (x,y-w/2,z), (x,y+w/2,z), r, 'rubber', 10)
    rod(a, (x,y-w/2-.003,z), (x,y+w/2+.003,z), r*.38, 'steel', 8)

def cross_wheel(a, x, y, z, r=.14, w=.08):
    rod(a, (x-w/2,y,z), (x+w/2,y,z), r, 'rubber', 10)
    rod(a, (x-w/2-.003,y,z), (x+w/2+.003,y,z), r*.38, 'steel', 8)

def ring(a, z, r, m='dark_metal', center=(0,0)):
    a.torus((center[0],center[1],z), r, .022, mat=m, segments=12,sides=4)

def handle(a, x, y, z, width=.3, depth=.1, mat='dark_metal'):
    rod(a,(x-width/2,y,z),(x-width/2,y+depth,z),.018,mat)
    rod(a,(x+width/2,y,z),(x+width/2,y+depth,z),.018,mat)
    rod(a,(x-width/2,y+depth,z),(x+width/2,y+depth,z),.018,mat)

def hollow_box(a, w,d,h,m='green',z=.0,t=.04):
    box(a,(0,0,z+t/2),(w,d,t),m)
    box(a,(0,-d/2+t/2,z+h/2),(w,t,h),m)
    box(a,(0,d/2-t/2,z+h/2),(w,t,h),m)
    box(a,(-w/2+t/2,0,z+h/2),(t,d,h),m)
    box(a,(w/2-t/2,0,z+h/2),(t,d,h),m)

def bag(a,x=0,y=0,z=0,r=.27,h=.63,m='black'):
    a.sphere((x,y,z+h*.44),1,mat=m,segments=7,rings=4,scale=(r,r*.83,h*.44))
    a.cone((x,y,z+h*.74),(x+.025,y,z+h*.94),r*.48,mat=m,sides=7,radius2=r*.12)
    rod(a,(x+.025,y,z+h*.92),(x+.025,y,z+h*.96),r*.16,'white',6)
    a.cone((x+.025,y,z+h*.95),(x+.08,y,z+h*1.05),r*.28,mat=m,sides=5)

def cart(a, w=.62,d=.7,h=1.02,m='black',lid='black',open_lid=False):
    # Tapered injection-molded body, raised front ribs, and full-width pull handle.
    z=.14
    verts=[(-w*.40,-d*.39,z),(w*.40,-d*.39,z),(w*.40,d*.39,z),(-w*.40,d*.39,z),
           (-w/2,-d/2,h),(w/2,-d/2,h),(w/2,d/2,h),(-w/2,d/2,h)]
    a.mesh(verts,[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],m)
    for x in (-w*.29,w*.29):
        a.beam((x,-d*.395,z+.1),(x,-d*.505,h-.12),.035,.025,mat=m)
    cross_wheel(a,-w*.45,d*.36,.14,.14,.085)
    cross_wheel(a,w*.45,d*.36,.14,.14,.085)
    rod(a,(-w*.42,d*.36,.14),(w*.42,d*.36,.14),.025,'metal')
    handle(a,0,d*.43,h-.03,w*.68,.12)
    if open_lid:
        box(a,(0,d*.44,h+d*.48),(w+.04,.05,d),'black',rot=(.25,0,0))
        box(a,(0,0,h+.006),(w*.84,d*.8,.012),'black')
    else:
        box(a,(0,0,h+.03),(w+.055,d+.06,.06),lid)
        box(a,(0,-d*.45,h+.065),(w*.35,.09,.04),lid)
    box(a,(0,-d*.505,h*.65),(w*.37,.012,h*.18),'white')

def dumpster(a,w=2.0,d=1.12,h=1.25,m='green',lid=True,wheels=True):
    hollow_box(a,w,d,h,m,z=.2,t=.07)
    box(a,(0,0,.23),(w+.12,d+.1,.11),'dark_metal')
    for x in (-w*.37,w*.37):
        box(a,(x,-d/2-.025,.2+h/2),(.065,.05,h-.05),m)
        box(a,(x,d/2+.025,.2+h/2),(.065,.05,h-.05),m)
    for y in (-d/2-.025,d/2+.025):
        box(a,(0,y,h+.18),(w+.1,.07,.1),'dark_metal')
    if lid:
        for x in (-w*.25,w*.25):
            box(a,(x,0,h+.25),(w*.48,d+.11,.08),'black')
            box(a,(x,-d*.45,h+.305),(.2,.12,.06),'dark_metal')
            for yy in (-d*.22,d*.15):
                box(a,(x,yy,h+.3),(w*.39,.035,.025),'dark_metal')
    if wheels:
        for x in (-w*.39,w*.39):
            for y in (-d*.34,d*.34): wheel(a,x,y,.14,.14,.085)

def recycle_mark(a,x,y,z,scale=.12):
    # Three simple arrows embossed on the front panel, readable at game distance.
    for angle in (0,2*pi/3,4*pi/3):
        xx=x+sin(angle)*scale*.6; zz=z+cos(angle)*scale*.6
        box(a,(xx,y,zz),(scale*.7,.015,scale*.16),'green',rot=(0,angle,0))
        box(a,(xx+cos(angle)*scale*.25,y-.001,zz-sin(angle)*scale*.25),
            (scale*.3,.02,scale*.32),'green',rot=(0,angle+pi/4,0))

@item('slatted_park_litter_bin')
def build(a):
    rod(a,(0,0,.07),(0,0,.88),.265,'black',12)
    for i in range(12):
        t=2*pi*i/12
        box(a,(.284*cos(t),.284*sin(t),.46),(.052,.10,.78),'wood',rot=t)
    ring(a,.12,.299);ring(a,.80,.299)
    a.cone((0,0,.89),(0,0,.99),.33,'dark_metal',12,radius2=.25)
    rod(a,(0,0,.991),(0,0,.999),.19,'black',12)
    ring(a,.995,.21)

@item('wire_mesh_street_basket')
def build(a):
    rod(a,(0,0,.03),(0,0,.08),.3,'dark_metal',12)
    for i in range(14):
        t=i*2*pi/14
        rod(a,(.28*cos(t),.28*sin(t),.07),(.35*cos(t),.35*sin(t),.84),.011,'metal',5)
    for z in (.15,.32,.49,.66,.83): ring(a,z,.28+.07*(z/.84),'metal')
    box(a,(0,-.326,.48),(.25,.016,.18),'green')

@item('hooded_side_entry_street_bin')
def build(a):
    rod(a,(0,0,.06),(0,0,.80),.30,'green',12)
    ring(a,.08,.31);ring(a,.78,.31)
    for x in (-.24,.24): box(a,(x,0,.95),(.08,.43,.30),'green')
    a.sphere((0,0,1.08),1,'green',12,4,scale=(.34,.34,.15))
    box(a,(0,0,.87),(.39,.4,.025),'black')
    box(a,(0,-.3,.43),(.20,.017,.23),'white')

@item('square_concrete_park_receptacle')
def build(a):
    hollow_box(a,.64,.64,.82,'concrete',t=.10)
    box(a,(0,0,.04),(.7,.7,.08),'concrete_light')
    box(a,(0,0,.84),(.73,.73,.08),'dark_metal')
    box(a,(0,0,.887),(.38,.38,.015),'black')
    for x in (-.20,0,.20): box(a,(x,-.325,.45),(.018,.01,.52),'concrete_light')

@item('solar_compacting_public_bin')
def build(a):
    box(a,(0,0,.70),(.64,.61,1.35),'dark_metal')
    box(a,(0,-.315,.60),(.53,.035,.91),'green')
    box(a,(0,-.344,1.10),(.43,.08,.24),'black')
    rod(a,(-.16,-.395,1.05),(.16,-.395,1.05),.022,'steel')
    box(a,(0,0,1.405),(.69,.68,.06),'metal',rot=(.09,0,0))
    box(a,(0,0,1.44),(.61,.58,.02),'navy',rot=(.09,0,0))
    for x in (-.2,0,.2): box(a,(x,0,1.456),(.009,.56,.008),'steel',rot=(.09,0,0))
    for y in (-.18,0,.18): box(a,(0,y,1.456+y*.09),(.59,.009,.008),'steel')
    box(a,(.22,-.339,.9),(.02,.02,.10),'silver')
    box(a,(-.2,-.345,1.28),(.04,.012,.025),'foliage_light')

@item('dual_stream_transit_bin_station','large')
def build(a):
    box(a,(0,0,.075),(1.43,.64,.15),'dark_metal')
    for x,m in ((-.36,'blue'),(.36,'black')):
        box(a,(x,0,.62),(.65,.59,1.08),m)
        a.cone((x,0,1.16),(x,0,1.28),.43,'dark_metal',4,radius2=.32)
        rod(a,(x,0,1.282),(x,0,1.294),.15,'black',10)
        box(a,(x,-.304,.78),(.4,.014,.20),'white')
    rod(a,(-.68,.26,.12),(-.68,.26,1.70),.028,'metal')
    rod(a,(.68,.26,.12),(.68,.26,1.70),.028,'metal')
    box(a,(0,.26,1.63),(1.38,.07,.26),'green')
    recycle_mark(a,-.36,-.315,.79,.11)

@item('cigarette_butt_disposal_tower')
def build(a):
    a.cone((0,0,.02),(0,0,.40),.19,'black',10,radius2=.085)
    rod(a,(0,0,.35),(0,0,1.04),.065,'dark_metal',10)
    a.sphere((0,0,1.055),.095,'dark_metal',10,4)
    box(a,(0,-.091,1.06),(.058,.009,.045),'black')
    rod(a,(0,0,.015),(0,0,.04),.205,'dark_metal',10)
    box(a,(0,-.066,.80),(.042,.01,.11),'yellow')

@item('dog_waste_bag_and_bin_station')
def build(a):
    box(a,(0,.12,.87),(.065,.065,1.74),'dark_metal')
    box(a,(0,.10,1.59),(.38,.055,.35),'green')
    box(a,(0,-.015,1.22),(.32,.20,.27),'green')
    box(a,(0,-.12,1.18),(.20,.014,.065),'black')
    box(a,(.035,-.133,1.13),(.12,.014,.11),'paper')
    rod(a,(0,-.13,.18),(0,-.13,.66),.225,'green',10)
    a.cone((0,-.13,.66),(0,-.13,.73),.25,'dark_metal',10,radius2=.205)
    rod(a,(0,-.13,.731),(0,-.13,.737),.15,'black',10)
    box(a,(0,.12,.035),(.33,.30,.07),'concrete')

@item('bear_resistant_trail_refuse_bin')
def build(a):
    box(a,(0,0,.57),(.84,.77,1.10),'brown')
    box(a,(0,0,1.16),(.95,.83,.13),'wood_dark',rot=(.12,0,0))
    box(a,(0,-.404,.98),(.50,.08,.21),'black')
    box(a,(0,-.465,1.01),(.22,.05,.06),'metal')
    for x in (-.35,.35):
        box(a,(x,-.403,.48),(.055,.04,.78),'wood_dark')
        box(a,(x,0,.04),(.12,1.0,.08),'dark_metal')
    box(a,(.30,-.45,.84),(.05,.04,.11),'silver')

@item('perforated_steel_drum_bin')
def build(a):
    rod(a,(0,0,.04),(0,0,.88),.285,'metal',12)
    for z in (.1,.82):ring(a,z,.29,'dark_metal')
    for i in range(12):
        t=2*pi*i/12
        for z in (.27,.44,.61):
            box(a,(.286*cos(t),.286*sin(t),z),(.007,.065,.075),'black',rot=t)
    rod(a,(0,0,.881),(0,0,.89),.245,'black',12)

@item('round_household_trash_can')
def build(a):
    a.cylinder((0,0,.035),(0,0,.66),.23,'black',12,radius2=.27)
    for i in range(10):
        t=i*2*pi/10;rod(a,(.233*cos(t),.233*sin(t),.12),(.26*cos(t),.26*sin(t),.60),.012,'dark_metal',5)
    a.cone((0,0,.67),(0,0,.72),.295,'dark_metal',12,radius2=.23)
    handle(a,0,-.05,.743,.19,.10)
    for x in (-.28,.28):box(a,(x,0,.58),(.075,.14,.055),'dark_metal')

@item('household_lidded_refuse_cart')
def build(a):cart(a)

@item('oversize_blue_recycling_cart')
def build(a):
    cart(a,.71,.82,1.12,'blue','blue')
    recycle_mark(a,0,-.416,.73,.15)
    for x in (-.22,0,.22):box(a,(x,0,1.188),(.035,.56,.025),'navy')

@item('open_yard_waste_cart')
def build(a):
    cart(a,.61,.68,1.00,'green','green',True)
    for x,y,z in ((-.13,-.1,1.03),(.1,.03,1.06),(.02,-.13,1.16)):
        a.sphere((x,y,z),.17,'foliage',7,3,scale=(.20,.16,.14))
    for x in (-.17,.12):rod(a,(x,0,.97),(x+.07,-.12,1.32),.023,'wood_dark',6)

@item('small_food_scrap_curb_cart')
def build(a):
    cart(a,.42,.49,.70,'brown','green')
    box(a,(0,-.25,.72),(.18,.10,.065),'dark_metal')
    rod(a,(-.14,.25,.68),(-.14,.32,.96),.022,'dark_metal')
    rod(a,(.14,.25,.68),(.14,.32,.96),.022,'dark_metal')
    rod(a,(-.14,.32,.96),(.14,.32,.96),.025,'black')

@item('galvanized_ash_can')
def build(a):
    a.cylinder((0,0,.02),(0,0,.49),.19,'silver',12,radius2=.23)
    for z in (.1,.22,.36):ring(a,z,.19+z*.08,'steel')
    a.cone((0,0,.50),(0,0,.56),.25,'steel',12,radius2=.15)
    handle(a,0,-.045,.575,.11,.09,'dark_metal')
    for x in (-.238,.238):a.torus((x,0,.40),.07,.012,'dark_metal',axis='x',segments=8,sides=4,arc=pi)

@item('wire_leaf_collection_cage')
def build(a):
    for i in range(12):
        t=i*2*pi/12;rod(a,(.43*cos(t),.43*sin(t),.02),(.43*cos(t),.43*sin(t),.89),.009,'steel',4)
    for z in (.04,.20,.38,.56,.74,.89):
        a.torus((0,0,z),.43,.009,'metal',segments=12,sides=4)
    for x,y in ((-.16,-.1),(.16,-.06),(0,.15)):
        a.sphere((x,y,.2),1,'foliage_dark',7,3,scale=(.25,.22,.22))

@item('folded_top_paper_leaf_sack','handheld')
def build(a):
    a.mesh([(-.19,-.14,0),(.19,-.14,0),(.19,.14,0),(-.19,.14,0),
            (-.22,-.15,.58),(.22,-.15,.58),(.22,.15,.58),(-.22,.15,.58),
            (-.19,0,.74),(.19,0,.74)],
           [(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),
            (4,5,9,8),(5,6,9),(6,7,8,9),(7,4,8)],'wood_light')
    box(a,(0,-.015,.73),(.39,.05,.065),'brown')
    box(a,(0,-.154,.34),(.24,.008,.24),'green')
    for z in (.30,.36,.42):box(a,(0,-.161,z),(.16,.005,.018),'cream')

@item('tied_black_refuse_sack','handheld')
def build(a):bag(a)

@item('clear_sack_of_recyclables','handheld')
def build(a):
    # Stylized blue translucent-looking shell and visible protruding recyclables.
    a.sphere((0,0,.24),1,'glass',7,3,scale=(.26,.22,.24))
    a.cone((0,0,.40),(0,0,.59),.13,'glass',7,radius2=.024)
    box(a,(.10,-.15,.31),(.15,.07,.24),'paper',rot=(0,.18,.12))
    rod(a,(-.10,-.17,.17),(-.10,-.17,.33),.048,'silver',6)
    rod(a,(.13,.03,.42),(.13,.03,.53),.052,'blue',6)
    rod(a,(.13,.03,.52),(.13,.03,.60),.022,'blue',6)
    rod(a,(0,0,.565),(0,0,.59),.036,'white',6)

@item('rear_load_rolling_dumpster','large')
def build(a):
    dumpster(a)
    box(a,(0,-.605,.80),(.66,.022,.33),'white')
    for x in (-1.07,1.07):rod(a,(x,-.40,.97),(x,.40,.97),.035,'dark_metal')

@item('cardboard_dumpster_with_slot','large')
def build(a):
    dumpster(a,2.25,1.32,1.45,'blue',False)
    box(a,(0,0,1.68),(2.38,1.4,.10),'navy',rot=(.15,0,0))
    box(a,(0,-.714,1.40),(1.55,.08,.24),'black')
    box(a,(0,-.768,1.28),(1.64,.17,.06),'metal')
    box(a,(0,-.68,.86),(.8,.02,.34),'white')
    recycle_mark(a,0,-.706,.87,.22)

@item('front_load_commercial_dumpster','large')
def build(a):
    dumpster(a,2.35,1.72,1.65,'green',True,False)
    for x in (-1.23,1.23):
        box(a,(x,0,1.1),(.22,1.32,.29),'green')
        box(a,(x,-.673,1.1),(.14,.018,.18),'black')
        box(a,(x,0,.83),(.13,1.2,.08),'dark_metal')
    for x in (-.90,.90):box(a,(x,0,.12),(.17,1.82,.16),'dark_metal')
    box(a,(0,-.882,.88),(.7,.023,.37),'white')

@item('restaurant_used_grease_container')
def build(a):
    box(a,(0,0,.54),(.82,.69,.88),'black')
    for x in (-.32,.32):
        cross_wheel(a,x,.22,.13,.13)
        box(a,(x,-.24,.12),(.075,.075,.24),'dark_metal')
    box(a,(0,0,1.01),(.87,.74,.08),'dark_metal')
    box(a,(0,-.01,1.075),(.43,.47,.045),'black')
    handle(a,0,-.10,1.10,.22,.15,'metal')
    box(a,(.30,-.06,1.07),(.08,.10,.14),'metal')
    box(a,(0,-.351,.64),(.49,.015,.26),'yellow')
    box(a,(0,-.361,.64),(.32,.014,.035),'black')
    rod(a,(0,.36,.80),(0,.52,.88),.025,'dark_metal')

@item('construction_rolloff_container','large')
def build(a):
    hollow_box(a,5.5,2.20,1.75,'orange',z=.28,t=.095)
    for y in (-1.16,1.16):
        box(a,(0,y,2.02),(5.64,.13,.15),'orange')
        box(a,(0,y,.36),(5.64,.11,.17),'wood_dark')
        for x in (-2.4,-1.6,-.8,0,.8,1.6,2.4):
            box(a,(x,y,1.15),(.13,.11,1.65),'orange')
    for y in (-.73,.73):box(a,(0,y,.15),(5.6,.15,.18),'dark_metal')
    for y in (-.86,.86):wheel(a,2.40,y,.20,.20,.15)
    for z in (.65,1.4):box(a,(2.82,0,z),(.11,2.11,.09),'dark_metal')
    rod(a,(-2.85,-.33,.47),(-2.85,.33,.47),.065,'dark_metal')
    box(a,(0,-1.225,1.3),(1.14,.014,.48),'white')

@item('compact_open_debris_skip','large')
def build(a):
    # Splayed ends and low loading lip distinguish a contractor skip from a dumpster.
    a.mesh([(-1.1,-.7,.20),(1.1,-.7,.20),(1.1,.7,.20),(-1.1,.7,.20),
            (-1.6,-.87,1.1),(1.6,-.87,1.1),(1.6,.87,1.1),(-1.6,.87,1.1)],
           [(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'yellow')
    for y in (-.88,.88):
        box(a,(0,y,1.1),(3.24,.085,.09),'dark_metal')
        for x in (-.8,0,.8):box(a,(x,y,.75),(.09,.07,.62),'yellow')
    for x in (-1.3,1.3):
        rod(a,(x,-.98,.90),(x,.98,.90),.045,'dark_metal')
    for y in (-.5,.5):box(a,(0,y,.12),(2.3,.12,.2),'dark_metal')
    for x,y in ((-.7,-.2),(.2,.18),(.7,-.25)):
        box(a,(x,y,.42),(.62,.36,.22),'concrete',rot=(0,.22,x))

@item('clothing_donation_dropbox','large')
def build(a):
    box(a,(0,0,.93),(1.24,1.08,1.81),'blue')
    box(a,(0,0,1.89),(1.35,1.18,.13),'navy',rot=(.10,0,0))
    box(a,(0,-.555,1.40),(.91,.035,.45),'black')
    box(a,(0,-.635,1.33),(.93,.18,.10),'blue',rot=(.2,0,0))
    rod(a,(-.32,-.742,1.4),(.32,-.742,1.4),.023,'silver')
    box(a,(0,-.555,.65),(1.00,.04,.88),'navy')
    box(a,(0,-.586,.85),(.69,.02,.34),'white')
    box(a,(.43,-.587,.65),(.04,.025,.14),'metal')
    for x in (-.50,.50):box(a,(x,0,.06),(.10,1.16,.12),'dark_metal')

@item('igloo_glass_bottle_recycling_bank','large')
def build(a):
    rod(a,(0,0,.03),(0,0,.17),.88,'dark_metal',12)
    rod(a,(0,0,.15),(0,0,.83),.84,'green',12)
    a.sphere((0,0,.83),1,'green',12,6,scale=(.84,.84,.72))
    rod(a,(0,-.87,1.01),(0,-.73,1.01),.205,'dark_metal',10)
    rod(a,(0,-.884,1.01),(0,-.872,1.01),.154,'black',10)
    box(a,(0,-.828,.53),(.43,.045,.28),'white')
    a.torus((0,0,1.65),.11,.027,'metal',axis='y',segments=8,sides=4)

@item('three_hole_public_recycling_sorter','large')
def build(a):
    box(a,(0,0,.56),(1.66,.64,1.04),'metal')
    for x,m in ((-.54,'blue'),(0,'green'),(.54,'yellow')):
        box(a,(x,-.33,.55),(.51,.04,.95),m)
        box(a,(x,0,1.105),(.54,.68,.07),'dark_metal')
        rod(a,(x,-.04,1.142),(x,-.04,1.154),.16,'black',10)
        box(a,(x,-.358,.83),(.27,.015,.14),'white')
        box(a,(x+.20,-.364,.51),(.025,.012,.09),'steel')
    box(a,(0,0,.04),(1.77,.7,.08),'black')

@item('used_motor_oil_collection_tank','large')
def build(a):
    rod(a,(-.65,0,.72),(.65,0,.72),.48,'dark_metal',12)
    for x in (-.49,.49):
        box(a,(x,0,.23),(.14,.78,.40),'green')
        a.torus((x,0,.72),.487,.025,'metal',axis='x',segments=12,sides=4)
    rod(a,(.22,0,1.14),(.22,0,1.37),.085,'metal',8)
    a.cone((.22,0,1.36),(.22,0,1.52),.09,'metal',10,radius2=.26)
    rod(a,(.22,0,1.522),(.22,0,1.533),.22,'black',10)
    box(a,(-.20,-.46,.74),(.58,.028,.30),'yellow')
    rod(a,(.64,-.12,.57),(.86,-.12,.57),.046,'metal')
    rod(a,(.86,-.12,.57),(.86,-.12,.39),.046,'metal')
    box(a,(.76,-.12,.66),(.16,.05,.035),'red')

@item('flattened_cardboard_tied_stack','handheld')
def build(a):
    for i in range(7):
        box(a,((i%3-1)*.018,(i%2)*.015,.015+i*.027),(.62-(i%2)*.07,.44,.021),'wood_light',rot=(i%3-1)*.035)
    for x in (-.18,.18):
        box(a,(x,0,.207),(.014,.49,.009),'cream')
        box(a,(x,-.242,.112),(.014,.009,.19),'cream')
        box(a,(x,.242,.112),(.014,.009,.19),'cream')
    box(a,(0,0,.209),(.63,.016,.008),'cream')

@item('twine_bound_newspaper_bundle','handheld')
def build(a):
    box(a,(0,0,.105),(.40,.29,.21),'paper')
    for z in (.035,.065,.095,.125,.155,.185):box(a,(0,-.147,z),(.40,.006,.007),'concrete')
    for x in (-.09,.09):
        box(a,(x,0,.214),(.009,.30,.008),'wood_dark')
        box(a,(x,-.151,.105),(.009,.009,.215),'wood_dark')
        box(a,(x,.151,.105),(.009,.009,.215),'wood_dark')
    box(a,(0,0,.216),(.41,.009,.007),'wood_dark')
    for y in (-.085,-.045,.015,.045):box(a,(0,y,.213),(.27,.013,.003),'concrete')

@item('compressed_aluminum_can_bale')
def build(a):
    box(a,(0,0,.29),(.67,.57,.56),'silver')
    for row in range(3):
        for col in range(5):
            x=-.26+col*.13;z=.11+row*.18
            a.cylinder((x,-.31,z),(x,-.345,z),.07,['red','blue','silver','green','silver'][col],6,radius2=.05)
    for x in (-.25,0,.25):
        for y in (-.17,.10):
            a.cylinder((x,y,.574),(x+.015,y,.603),.088,'silver',7,radius2=.064)
            box(a,(x,y,.609),(.035,.016,.008),'dark_metal')
    for x in (-.21,.21):
        box(a,(x,0,.58),(.018,.60,.012),'dark_metal')
        box(a,(x,-.354,.29),(.018,.012,.58),'dark_metal')

@item('baled_plastic_bottles')
def build(a):
    box(a,(0,0,.29),(.72,.54,.55),'glass')
    for row in range(3):
        for col in range(5):
            x=-.29+col*.145;z=.1+row*.18
            a.sphere((x,-.287,z),1,['glass','white','blue'][col%3],6,3,scale=(.071,.055,.085))
    for x in (-.17,.16):
        for y in (-.19,0,.19):
            a.sphere((x,y,.586),1,'glass',6,3,scale=(.11,.064,.034))
            rod(a,(x+.085,y,.59),(x+.14,y,.59),.018,'white',6)
    for x in (-.24,.24):
        box(a,(x,0,.58),(.014,.59,.012),'metal')
        box(a,(x,-.347,.29),(.014,.012,.58),'metal')

@item('three_bag_yard_clippings_pile')
def build(a):
    bag(a,-.19,-.12,0,.27,.62,'green')
    bag(a,.21,.11,0,.24,.52,'black')
    bag(a,-.23,.26,.05,.22,.55,'green')
    a.sphere((.12,-.29,.065),1,'foliage_dark',7,3,scale=(.22,.12,.06))

@item('curbside_tied_brush_bundle')
def build(a):
    for i,(y,z) in enumerate(((-.18,.10),(-.08,.15),(.04,.11),(.17,.13),(-.06,.23),(.10,.24))):
        rod(a,(-.64+i*.04,y,z),(.66-i*.03,y+.025,z+.03),.035,'wood_dark',6)
        rod(a,(.18,y,z),(.48,y+.18,z+.18),.018,'wood',5)
        rod(a,(-.13,y,z),(-.37,y-.13,z+.15),.013,'wood',5)
    for x in (-.3,.3):a.torus((x,0,.19),.215,.012,'cream',axis='x',segments=8,sides=4)

@item('discarded_tire_stack')
def build(a):
    for i in range(3):
        a.torus(((i%2)*.045,0,.105+i*.19),.25,.102,'rubber',segments=12,sides=6)
    for i in range(12):
        t=i*pi/6;box(a,(.356*cos(t),.356*sin(t),.48),(.01,.05,.10),'black',rot=t)

@item('curbside_discarded_mattress','large')
def build(a):
    box(a,(0,0,.18),(1.02,1.96,.34),'cream')
    for z in (.06,.29):
        box(a,(0,-.982,z),(1.03,.018,.021),'paper')
        box(a,(0,.982,z),(1.03,.018,.021),'paper')
        box(a,(-.512,0,z),(.018,1.96,.021),'paper')
        box(a,(.512,0,z),(.018,1.96,.021),'paper')
    for x in (-.34,0,.34):
        for y in (-.71,-.24,.24,.71):
            rod(a,(x,y,.35),(x,y,.359),.035,'brown',6)
    for y in (-.5,.5):handle(a,.516,y,.18,.15,.04,'wood_light')

@item('bulky_pickup_worn_armchair')
def build(a):
    box(a,(0,0,.28),(.86,.83,.33),'brown')
    box(a,(0,.29,.70),(.86,.25,.72),'brown',rot=(-.10,0,0))
    for x in (-.36,.36):box(a,(x,0,.54),(.19,.82,.40),'brown')
    box(a,(0,-.07,.48),(.51,.59,.18),'wood_light')
    box(a,(0,.172,.78),(.51,.07,.48),'wood_light',rot=(-.10,0,0))
    for x in (-.31,.31):
        for y in (-.28,.28):box(a,(x,y,.08),(.075,.075,.16),'wood_dark')
    box(a,(.358,-.24,.752),(.11,.23,.018),'cream')
    box(a,(-.1,-.23,.584),(.14,.13,.013),'brown',rot=.25)

@item('broken_pallet_scrap_stack','large')
def build(a):
    for z,dx in ((.0,0),(.15,.08)):
        for y in (-.4,0,.4):box(a,(dx,y,z+.06),(1.15,.10,.12),'wood_dark')
        for x in (-.49,-.25,0,.25,.49):box(a,(x+dx,0,z+.14),(.16,.96,.05),'wood')
    box(a,(.0,.03,.36),(1.18,.13,.055),'wood_light',rot=.5)
    box(a,(-.10,-.15,.39),(.78,.12,.045),'wood',rot=-.37)
    box(a,(.29,.15,.39),(.42,.15,.065),'wood_light',rot=.82)
    for x in (-.48,.02,.5):
        for y in (-.4,.4):rod(a,(x,y,.316),(x,y,.322),.009,'dark_metal',5)

@item('outdoor_janitor_pushcart')
def build(a):
    box(a,(0,0,.24),(1.02,.59,.10),'blue')
    for x in (-.38,.38):
        for y in (-.22,.22):wheel(a,x,y,.13,.11,.06)
    for x in (-.36,.20):
        for y in (-.22,.22):rod(a,(x,y,.28),(x,y,.98),.022,'metal')
    box(a,(-.13,0,.67),(.63,.53,.06),'blue')
    box(a,(-.13,0,.99),(.63,.53,.06),'blue')
    bag(a,.43,0,.25,.22,.70,'yellow')
    rod(a,(.45,-.24,.94),(.45,.24,.94),.025,'dark_metal')
    for y in (-.22,.22):rod(a,(-.40,y,.88),(-.59,y,1.14),.023,'dark_metal')
    rod(a,(-.59,-.22,1.14),(-.59,.22,1.14),.027,'dark_metal')
    a.cylinder((-.18,0,1.03),(-.18,0,1.22),.12,'green',8,radius2=.15)

@item('trigger_litter_picker_tongs','handheld')
def build(a):
    rod(a,(0,0,.16),(0,0,.98),.012,'silver',6)
    box(a,(0,0,1.00),(.055,.042,.13),'orange')
    box(a,(.052,0,1.027),(.075,.033,.028),'black',rot=(0,.35,0))
    rod(a,(0,0,.18),(-.065,0,.07),.014,'orange',6)
    rod(a,(0,0,.18),(.065,0,.07),.014,'orange',6)
    box(a,(-.065,0,.04),(.035,.06,.085),'black',rot=(0,-.30,0))
    box(a,(.065,0,.04),(.035,.06,.085),'black',rot=(0,.30,0))

@item('upright_lobby_dustpan','handheld')
def build(a):
    a.prism([(-.16,-.17),(.16,-.17),(.14,.11),(-.14,.11)],.01,.055,'black')
    box(a,(0,.10,.14),(.28,.035,.19),'black')
    for x in (-.148,.148):box(a,(x,-.015,.10),(.025,.22,.10),'black')
    rod(a,(0,.11,.14),(0,.11,.94),.013,'silver',6)
    box(a,(0,.11,.99),(.035,.045,.16),'blue')
    box(a,(0,-.17,.038),(.33,.025,.022),'rubber')

@item('wide_street_push_broom','handheld')
def build(a):
    box(a,(0,0,.105),(.57,.11,.055),'wood')
    for x in (-.24,-.16,-.08,0,.08,.16,.24):
        box(a,(x,0,.047),(.062,.095,.072),'brown')
    rod(a,(0,.015,.135),(0,.30,1.41),.017,'wood_light',8)
    rod(a,(0,.275,1.3),(0,.31,1.45),.021,'green',8)
    rod(a,(-.17,.02,.15),(0,.08,.38),.010,'metal',6)
    rod(a,(.17,.02,.15),(0,.08,.38),.010,'metal',6)

@item('handheld_litter_collection_hoop_bag','handheld')
def build(a):
    a.cylinder((0,0,.05),(0,0,.61),.18,'black',8,radius2=.24)
    rod(a,(0,0,.612),(0,0,.619),.215,'black',8)
    a.torus((0,0,.62),.235,.020,'orange',segments=10,sides=4)
    handle(a,0,.21,.64,.16,.11,'black')
    box(a,(0,-.205,.36),(.19,.018,.16),'white')

@item('two_wheel_refuse_bin_dolly')
def build(a):
    box(a,(0,-.14,.07),(.48,.40,.09),'dark_metal')
    for x in (-.19,.19):rod(a,(x,.075,.09),(x,.075,1.20),.021,'metal')
    for z in (.36,.69,1.07):rod(a,(-.19,.075,z),(.19,.075,z),.018,'metal')
    rod(a,(-.19,.075,1.20),(.19,.075,1.20),.027,'black')
    cross_wheel(a,-.28,.09,.15,.15,.09);cross_wheel(a,.28,.09,.15,.15,.09)
    rod(a,(-.30,.09,.15),(.30,.09,.15),.027,'dark_metal')
    box(a,(0,-.07,.57),(.38,.045,.12),'orange')

@item('walk_behind_parking_lot_sweeper')
def build(a):
    box(a,(0,0,.33),(.79,.58,.39),'orange')
    box(a,(.21,0,.55),(.34,.53,.14),'dark_metal')
    box(a,(-.24,0,.30),(.33,.65,.28),'orange',rot=(0,-.15,0))
    for y in (-.32,.32):wheel(a,.20,y,.20,.20,.1)
    rod(a,(-.25,-.32,.11),(-.25,.32,.11),.09,'black',12)
    for y in (-.38,.38):
        rod(a,(-.34,y,.06),(-.34,y,.11),.20,'brown',10)
        rod(a,(-.34,y,.11),(-.34,y,.15),.11,'dark_metal',10)
    for y in (-.24,.24):rod(a,(.24,y,.45),(.72,y,1.01),.022,'metal')
    rod(a,(.72,-.24,1.01),(.72,.24,1.01),.029,'black')
    box(a,(.2,-.301,.37),(.27,.012,.12),'white')

@item('towable_leaf_vacuum','large')
def build(a):
    box(a,(0,0,.39),(1.44,.90,.15),'dark_metal')
    for y in (-.56,.56):wheel(a,0,y,.33,.33,.18)
    box(a,(.12,0,.80),(1.04,.79,.71),'yellow')
    box(a,(.13,0,1.22),(.84,.70,.15),'yellow',rot=(0,.13,0))
    rod(a,(-.58,-.06,.72),(-.75,-.06,.72),.25,'black',12)
    a.tube([(-.75,-.06,.72),(-.98,-.16,.58),(-1.1,-.42,.25),(-1.18,-.72,.14)],.105,'black',10)
    for z in (.66,.82,.98):box(a,(.22,-.407,z),(.6,.022,.04),'black')
    a.beam((.65,0,.35),(1.35,0,.29),.085,.1,'dark_metal')
    a.torus((1.40,0,.29),.08,.02,'steel',segments=8,sides=4)
    box(a,(-.28,.31,1.36),(.27,.22,.54),'yellow')
    box(a,(-.25,.53,1.58),(.27,.52,.16),'yellow')
    box(a,(-.25,.80,1.55),(.20,.028,.11),'black')

@item('compact_municipal_street_sweeper','large')
def build(a):
    box(a,(0,0,.51),(2.72,1.14,.23),'dark_metal')
    for x in (-.88,.88):
        for y in (-.59,.59):wheel(a,x,y,.38,.34,.20)
    box(a,(.63,0,1.07),(1.24,1.10,.92),'white')
    box(a,(.71,0,1.59),(1.08,1.08,.16),'white')
    box(a,(-.74,0,1.22),(.97,1.07,1.20),'yellow')
    box(a,(-.76,0,1.91),(1.14,1.16,.12),'yellow')
    box(a,(-1.245,0,1.44),(.025,.94,.56),'glass')
    for y in (-.548,.548):
        box(a,(-.76,y,1.45),(.80,.022,.61),'glass')
        box(a,(-.78,y,.92),(.83,.027,.28),'yellow')
        box(a,(-.45,y*1.08,1.23),(.11,.045,.03),'dark_metal')
    box(a,(-1.35,0,.66),(.15,1.20,.18),'black')
    for y in (-.4,.4):box(a,(-1.431,y,.81),(.028,.20,.14),'light')
    for y in (-.74,.74):
        rod(a,(-.49,y,.06),(-.49,y,.17),.30,'brown',12)
        rod(a,(-.49,y,.18),(-.49,y,.23),.20,'dark_metal',10)
        rod(a,(-.42,y*.62,.45),(-.49,y,.23),.05,'metal')
    for z in (.99,1.10,1.21):box(a,(.65,-.56,z),(.73,.025,.035),'dark_metal')
    rod(a,(-.42,0,2.0),(-.42,0,2.13),.09,'orange',8)
    box(a,(1.27,0,1.23),(.14,.74,.30),'dark_metal')
    for y in (-.42,.42):box(a,(1.41,y,.91),(.045,.12,.13),'red')

@item('street_cleaning_water_hose_cart')
def build(a):
    box(a,(0,0,.24),(.89,.63,.11),'dark_metal')
    for x in (-.3,.3):
        for y in (-.29,.29):wheel(a,x,y,.16,.14,.065)
    rod(a,(-.29,0,.67),(.29,0,.67),.31,'blue',12)
    for x in (-.22,.22):
        a.torus((x,0,.67),.318,.023,'metal',axis='x',segments=10,sides=4)
        box(a,(x,0,.38),(.08,.49,.18),'metal')
    rod(a,(.04,0,.96),(.04,0,1.05),.075,'dark_metal',8)
    rod(a,(.04,0,1.05),(.04,0,1.07),.105,'black',8)
    for x in (-.08,.015,.10):a.torus((x,-.39,.63),.21,.033,'green',axis='x',segments=10,sides=5)
    rod(a,(-.11,-.39,.63),(.15,-.39,.63),.045,'metal')
    for y in (-.25,.25):rod(a,(.34,y,.34),(.57,y,1.09),.022,'metal')
    rod(a,(.57,-.25,1.09),(.57,.25,1.09),.029,'black')
    rod(a,(.20,-.33,.50),(.43,-.40,.29),.016,'green')
    rod(a,(.43,-.40,.29),(.53,-.42,.25),.024,'gold')

assert len(NAMES) == 50, f'Expected exactly 50 batch04 assets, got {len(NAMES)}'
