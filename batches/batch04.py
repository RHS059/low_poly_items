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
    # Rounded tire shoulders, sidewall, steel hub and recessed axle.
    n=12 if r>=.2 else 10;vs=[]
    for dy,rr in ((-.5*w,r*.84),(-.35*w,r),( .35*w,r),(.5*w,r*.84)):
        vs += [(x+rr*cos(j*2*pi/n),y+dy,z+rr*sin(j*2*pi/n)) for j in range(n)]
    fs=[(k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j) for k in range(3) for j in range(n)]
    fs += [tuple(reversed(range(n))),tuple(range(3*n,4*n))];a.mesh(vs,fs,'rubber')
    rod(a,(x,y-w*.51,z),(x,y+w*.51,z),r*.52,'steel',n)
    for sign in (-1,1):
        rod(a,(x,y+sign*w*.514,z),(x,y+sign*w*.55,z),r*.24,'dark_metal',8)
        if r>=.2:
            for j in range(5):
                t=j*2*pi/5
                rod(a,(x+r*.36*cos(t),y+sign*w*.52,z+r*.36*sin(t)),(x+r*.36*cos(t),y+sign*w*.56,z+r*.36*sin(t)),r*.043,'silver',6)

def cross_wheel(a, x, y, z, r=.14, w=.08):
    tmp=Asset('wheel');wheel(tmp,0,0,0,r,w)
    a.mesh([(x+yy,y-xx,z+zz) for xx,yy,zz in tmp.vertices],tmp.faces,tmp.face_materials)


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

def xz_shell(a,points,y0,y1,m):
    n=len(points);vs=[(x,y,z) for y in (y0,y1) for x,z in points]
    a.mesh(vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],m)

def cushion(a,c,size,m='brown',sag=.025):
    # Upholstery rolls inward at each seam instead of ending in a perfect cube.
    x,y,z=c;w,d,h=size;vs=[]
    for zz,fw,fd in ((-h*.5,.89,.89),(-h*.31,1,1),(h*.28,1,1),(h*.5,.88,.88)):
        rr=min(w,d)*.12
        pts=[(-w*.5+rr,-d*.5),(w*.5-rr,-d*.5),(w*.5,-d*.5+rr),(w*.5,d*.5-rr),(w*.5-rr,d*.5),(-w*.5+rr,d*.5),(-w*.5,d*.5-rr),(-w*.5,-d*.5+rr)]
        vs += [(x+xx*fw,y+yy*fd,z+zz) for xx,yy in pts]
    vs.append((x,y,z+h*.5-sag));fs=[(k*8+j,k*8+(j+1)%8,(k+1)*8+(j+1)%8,(k+1)*8+j) for k in range(3) for j in range(8)]
    fs += [tuple(reversed(range(8)))]+[(24+j,24+(j+1)%8,32) for j in range(8)]
    a.mesh(vs,fs,m)

def open_lid(a,c,w,d,z,opening=.18,m='dark_metal',n=12):
    # Rectangular outside edge, actual circular aperture and inner wall.
    x,y=c;vs=[]
    for layer in range(4):
        for j in range(n):
            t=j*2*pi/n;co=cos(t);si=sin(t)
            outer=min(w/2/max(abs(co),1e-6),d/2/max(abs(si),1e-6))
            rr=outer if layer==0 else opening+.024 if layer==1 else opening
            zz=z-.03 if layer==0 else z+.025 if layer==1 else z+.012 if layer==2 else z-.13
            vs.append((x+rr*co,y+rr*si,zz))
    a.mesh(vs,[(k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j) for k in range(3) for j in range(n)],m)
    rod(a,(x,y,z-.19),(x,y,z-.18),opening*.97,'black',n)

def brush(a,x,y,z,r=.25):
    a.cone((x,y,z),(x,y,z+.10),r,'brown',12,radius2=r*.7)
    rod(a,(x,y,z+.105),(x,y,z+.14),r*.62,'dark_metal',12)
    rod(a,(x,y,z+.14),(x,y,z+.23),r*.18,'metal',8)
    for j in range(16):
        t=j*2*pi/16
        rod(a,(x+r*.74*cos(t),y+r*.74*sin(t),z+.077),(x+r*.98*cos(t),y+r*.98*sin(t),z+.009),.012,'wood_dark',5)

def bag(a,x=0,y=0,z=0,r=.27,h=.63,m='black'):
    # Asymmetric packed sack with vertical creases that gather at its tied neck.
    n=10;vs=[]
    for k,(zh,rr) in enumerate(((.02,.48),(.14,.86),(.39,1),(.65,.88),(.79,.52),(.89,.11))):
        for j in range(n):
            t=j*2*pi/n;fac=1+.10*sin(j*2.4+k*.65)+(.055 if j%2 else -.055)
            vs.append((x+r*rr*cos(t)*fac+.02*sin(k),y+r*.84*rr*sin(t)*fac,z+h*zh))
    fs=[(k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j) for k in range(5) for j in range(n)]
    fs += [tuple(reversed(range(n))),tuple(range(5*n,6*n))];a.mesh(vs,fs,m)
    rod(a,(x-.015,y,z+h*.883),(x-.015,y,z+h*.916),r*.13,'white',6)
    a.cone((x-.015,y,z+h*.913),(x+.06,y+.014,z+h*1.025),r*.27,mat=m,sides=5)

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
    for x in (-w*.30,w*.30):
        rod(a,(x-.05,d*.45,h),(x+.05,d*.45,h),.036,lid,8)
    for sign in (-1,1):
        box(a,(sign*w*.49,0,h*.76),(.036,d*.24,.06),m)
    if not open_lid:
        for x in (-w*.32,w*.32):box(a,(x,0,h+.068),(.045,d*.74,.025),lid)

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
            for y in (-d*.34,d*.34):
                wheel(a,x,y,.14,.14,.085)
                for dy in (-.058,.058):box(a,(x,y+dy,.22),(.10,.02,.19),'metal')
                rod(a,(x,y,.28),(x,y,.34),.041,'metal',8)
    if lid:
        rod(a,(-w*.46,d*.51,h+.24),(w*.46,d*.51,h+.24),.027,'metal',8)
        for x in (-w*.34,0,w*.34):box(a,(x,d*.51,h+.19),(.12,.07,.14),m)

def recycle_mark(a,x,y,z,scale=.12):
    # Three simple arrows embossed on the front panel, readable at game distance.
    for angle in (0,2*pi/3,4*pi/3):
        xx=x+sin(angle)*scale*.6; zz=z+cos(angle)*scale*.6
        box(a,(xx,y,zz),(scale*.7,.015,scale*.16),'green',rot=(0,angle,0))
        box(a,(xx+cos(angle)*scale*.25,y-.001,zz-sin(angle)*scale*.25),
            (scale*.3,.02,scale*.32),'green',rot=(0,angle+pi/4,0))

@item('slatted_park_litter_bin')
def build(a):
    rod(a,(0,0,.07),(0,0,.81),.255,'black',12)
    for i in range(12):
        t=2*pi*i/12
        box(a,(.284*cos(t),.284*sin(t),.46),(.052,.10,.78),'wood',rot=t)
    ring(a,.12,.299);ring(a,.80,.299)
    a.cylinder((0,0,.89),(0,0,.99),.33,'dark_metal',12,radius2=.25,cap=False)
    a.cylinder((0,0,.80),(0,0,.99),.23,'dark_metal',12,cap=False)
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
    hollow_box(a,.64,.64,.82,'concrete',t=.07)
    box(a,(0,0,.04),(.7,.7,.08),'concrete_light')
    for y in (-.283,.283):box(a,(0,y,.85),(.73,.164,.08),'dark_metal')
    for x in (-.283,.283):box(a,(x,0,.85),(.164,.40,.08),'dark_metal')
    box(a,(0,0,.68),(.49,.49,.02),'black')
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
        start=len(a.vertices);hollow_box(a,.65,.59,1.08,m,z=.08,t=.035)
        for vi in range(start,len(a.vertices)):
            vx,vy,vz=a.vertices[vi];a.vertices[vi]=(vx+x,vy,vz)
        open_lid(a,(x,0),.67,.61,1.25,.145)
        box(a,(x,-.305,.52),(.56,.035,.85),m)
        for z in (.30,.90):box(a,(x-.26,-.33,z),(.04,.03,.07),'metal')
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
    # Open slots are geometry: separate webs and hoop bands surround a dark liner.
    rod(a,(0,0,.04),(0,0,.08),.285,'metal',12)
    rod(a,(0,0,.08),(0,0,.72),.24,'black',12)
    for j in range(12):
        t=j*2*pi/12;q=(j+1)*2*pi/12
        for z0,z1 in ((.08,.19),(.29,.36),(.46,.53),(.63,.72),(.82,.87)):
            p=[(.285*cos(t),.285*sin(t),z0),(.285*cos(q),.285*sin(q),z0),(.285*cos(q),.285*sin(q),z1),(.285*cos(t),.285*sin(t),z1)]
            a.mesh(p,[(0,1,2,3)],'metal')
        a.beam((.28*cos(t),.28*sin(t),.08),(.28*cos(t),.28*sin(t),.87),.055,.018,'metal')
    ring(a,.09,.286,'dark_metal');ring(a,.86,.286,'dark_metal')
    a.torus((0,0,.877),.265,.020,'steel',segments=12,sides=4)

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
    bag(a,0,0,0,.26,.56,'glass')
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
    # Splayed steel shell has an actual wall thickness and open interior.
    outer=[(-1.1,-.7,.20),(1.1,-.7,.20),(1.1,.7,.20),(-1.1,.7,.20),(-1.6,-.87,1.1),(1.6,-.87,1.1),(1.6,.87,1.1),(-1.6,.87,1.1)]
    inner=[(-1.07,-.66,.26),(1.07,-.66,.26),(1.07,.66,.26),(-1.07,.66,.26),(-1.54,-.82,1.1),(1.54,-.82,1.1),(1.54,.82,1.1),(-1.54,.82,1.1)]
    fs=[(0,3,2,1),(8,9,10,11)]
    for i in range(4):
        j=(i+1)%4
        fs += [(i,j,j+4,i+4),(i+8,i+12,j+12,j+8),(i+4,j+4,j+12,i+12)]
    a.mesh(outer+inner,fs,'yellow')
    for sign in (-1,1):
        y=sign*.88
        box(a,(0,y,1.115),(3.24,.085,.08),'dark_metal')
        for x in (-.8,0,.8):
            a.beam((x,sign*.741,.32),(x,sign*.88,1.06),.075,.045,'yellow')
        for x in (-1.3,1.3):
            box(a,(x,sign*.867,.88),(.15,.07,.18),'dark_metal')
            rod(a,(x,sign*.885,.90),(x,sign*.985,.90),.055,'dark_metal',8)
    for x in (-1.59,1.59):box(a,(x,0,1.115),(.085,1.79,.08),'dark_metal')
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
    hollow_box(a,1.66,.64,1.04,'metal',z=.04,t=.035)
    for x in (-.27,.27):box(a,(x,0,.52),(.028,.58,.92),'dark_metal')
    for x,m in ((-.54,'blue'),(0,'green'),(.54,'yellow')):
        box(a,(x,-.33,.55),(.51,.04,.95),m)
        open_lid(a,(x,0),.54,.68,1.12,.15)
        for z in (.28,.86):box(a,(x-.22,-.36,z),(.028,.025,.07),'metal')
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
    # Compressed flattened cartons with staggered creases and partly folded flaps.
    for i in range(7):
        dx=(i%3-1)*.013;dy=(i%2)*.012;z=.01+i*.017
        pts=[(-.31+dx,-.21+dy),(.27+dx,-.22+dy),(.31+dx,-.16+dy),(.30+dx,.21+dy),(-.26+dx,.22+dy),(-.31+dx,.17+dy)]
        a.prism(pts,z,z+.012,'wood_light' if i%3 else 'cream')
        box(a,(dx,-.216+dy,z+.006),(.40,.007,.003),'brown')
    a.mesh([(-.29,-.20,.126),(-.09,-.20,.126),(-.09,.20,.126),(-.29,.20,.14)],[(0,1,2,3)],'wood_light')
    a.mesh([(.10,-.20,.126),(.29,-.19,.146),(.29,.20,.137),(.10,.20,.126)],[(0,1,2,3)],'wood_light')
    for x in (-.18,.18):
        a.tube([(x,-.237,.006),(x,-.238,.139),(x,0,.143),(x,.238,.139),(x,.238,.005)],.005,'cream',4)
    rod(a,(-.32,0,.146),(.32,0,.146),.005,'cream',4)

@item('twine_bound_newspaper_bundle','handheld')
def build(a):
    # Seven slightly buckled folded sections, with compressed edges under twine.
    for j in range(7):
        x=(j%3-1)*.008;y=(j%2)*.008;z=.015+j*.029
        pts=[(-.20+x,-.142+y),(-.04+x,-.151+y),(.19+x,-.143+y),(.20+x,.128+y),(.01+x,.145+y),(-.20+x,.132+y)]
        a.prism(pts,z,z+.024,'paper' if j%3 else 'white')
    for x in (-.09,.09):a.tube([(x,-.155,.015),(x,-.157,.211),(x,0,.214),(x,.155,.211),(x,.155,.01)],.004,'wood_dark',4)
    rod(a,(-.20,0,.219),(.20,0,.219),.004,'wood_dark',4)
    for y in (-.095,-.067,-.039,.025,.048):box(a,(.024,y,.215),(.23,.009,.003),'concrete')

@item('compressed_aluminum_can_bale')
def build(a):
    # Compressed crushed cans form every exposed side; the inner packing is hidden.
    cushion(a,(0,0,.29),(.58,.47,.53),'silver',.016)
    for side in (-1,1):
        for row in range(4):
            for col in range(5):
                x=-.28+col*.139+(row%2)*.012;z=.083+row*.137
                a.sphere((x,side*(.237+.016*sin(row+col)),z),1,['silver','red','silver','blue','green'][col],6,3,scale=(.076,.058,.077))
                if side<0 and (row+col)%2==0:rod(a,(x,-.295,z),(x,-.301,z),.035,'dark_metal',6)
    for side in (-1,1):
        for row in range(3):
            for col in range(3):
                a.sphere((side*.30,(col-1)*.16,.10+row*.17),1,'silver',6,3,scale=(.048,.082,.083))
    for x in (-.22,0,.22):
        for y in (-.16,.02,.16):
            a.sphere((x,y,.564+.013*sin(x*10+y)),1,'silver',6,3,scale=(.095,.076,.045))
    for x in (-.21,.21):
        a.tube([(x,-.31,.03),(x,-.32,.55),(x,-.21,.605),(x,.22,.60),(x,.31,.54),(x,.31,.03)],.009,'dark_metal',4)

@item('baled_plastic_bottles')
def build(a):
    cushion(a,(0,0,.29),(.63,.45,.52),'glass',.015)
    for side in (-1,1):
        for row in range(3):
            for col in range(5):
                x=-.29+col*.145+sin(row*2+col)*.012;z=.105+row*.18
                a.sphere((x,side*.25,z),1,['glass','white','glass','blue','glass'][col],6,3,scale=(.075,.056,.084))
                if (row+col)%2==0:rod(a,(x+.021,side*.269,z+.058),(x+.037,side*.284,z+.093),.019,'white',6)
    for side in (-1,1):
        for row in range(3):
            for col in range(3):a.sphere((side*.335,(col-1)*.16,.12+row*.17),1,'glass',6,3,scale=(.045,.077,.081))
    for x in (-.19,.03,.22):
        for y in (-.16,.02,.16):
            a.sphere((x,y,.563),1,'glass',6,3,scale=(.092,.070,.041))
            rod(a,(x+.066,y,.58),(x+.105,y,.595),.016,'white',6)
    for x in (-.23,.23):a.tube([(x,-.316,.025),(x,-.326,.55),(x,-.20,.61),(x,.20,.61),(x,.318,.54),(x,.318,.025)],.008,'metal',4)

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
    cushion(a,(0,0,.17),(1.02,1.96,.31),'cream',.028)
    # Piping follows the rounded corners; quilting dips inward at each button.
    pts=[(-.40,-.97),(.40,-.97),(.51,-.87),(.51,.87),(.40,.97),(-.40,.97),(-.51,.87),(-.51,-.87)]
    for z in (.055,.29):a.tube([(x,y,z) for x,y in pts+[pts[0]]],.009,'paper',6)
    for x in (-.31,0,.31):
        for y in (-.68,-.23,.23,.68):
            zz=.325-.028*(1-max(abs(x)/.448,abs(y)/.862))
            rod(a,(x,y,zz+.001),(x,y,zz+.005),.017,'wood_light',8)
    for y in (-.50,.50):
        a.tube([(.502,y-.10,.14),(.535,y-.10,.18),(.535,y+.10,.18),(.502,y+.10,.14)],.013,'wood_light',6)

@item('bulky_pickup_worn_armchair')
def build(a):
    cushion(a,(0,0,.28),(.87,.84,.28),'brown',.005)
    for x in (-.31,.31):
        for y in (-.28,.28):a.cone((x,y,.015),(x*.95,y,.17),.045,'wood_dark',5,radius2=.031)
    # The reclining back and separate cushions follow a soft, compressed silhouette.
    start=len(a.vertices);cushion(a,(0,.30,.72),(.85,.23,.75),'brown',.005)
    for i in range(start,len(a.vertices)):
        x,y,z=a.vertices[i];a.vertices[i]=(x,y+(z-.72)*.10,z)
    cushion(a,(0,-.075,.48),(.54,.60,.18),'wood_light',.037)
    start=len(a.vertices);cushion(a,(0,.17,.77),(.55,.105,.48),'wood_light',.012)
    for i in range(start,len(a.vertices)):
        x,y,z=a.vertices[i];a.vertices[i]=(x,y+(z-.77)*.10,z)
    for sign in (-1,1):
        cushion(a,(sign*.36,-.012,.56),(.22,.78,.39),'brown',.008)
        a.tube([(sign*.39,-.37,.70),(sign*.39,-.30,.753),(sign*.39,.27,.755)],.008,'wood_dark',6)
    a.tube([(-.24,-.34,.526),(0,-.36,.52),(.24,-.34,.526)],.007,'wood_dark',6)
    for x in (-.14,.14):rod(a,(x,.101,.80),(x,.092,.80),.016,'brown',6)
    a.mesh([(.30,-.30,.748),(.39,-.32,.753),(.405,-.16,.754),(.34,-.10,.747),(.31,-.19,.749)],[(0,1,2,3,4)],'cream')
    a.mesh([(-.19,-.24,.554),(-.09,-.28,.55),(-.04,-.18,.55),(-.14,-.13,.554)],[(0,1,2,3)],'brown')

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
    a.cylinder((0,0,.05),(0,0,.61),.18,'black',10,radius2=.24,cap=False)
    rod(a,(0,0,.05),(0,0,.062),.18,'black',10)
    a.cylinder((0,0,.07),(0,0,.605),.168,'black',10,radius2=.224,cap=False)
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
    profile=[(-.47,.17),(-.47,.39),(-.32,.53),(.10,.56),(.32,.45),(.38,.20)]
    xz_shell(a,profile,-.29,.29,'orange')
    xz_shell(a,[(-.37,.43),(-.26,.54),(.05,.565),(.11,.52)],-.26,.26,'dark_metal')
    for y in (-.32,.32):wheel(a,.20,y,.20,.20,.1)
    rod(a,(-.25,-.29,.115),(-.25,.29,.115),.10,'black',12)
    for y in (-.37,.37):
        brush(a,-.37,y,.03,.18)
        rod(a,(-.20,y*.62,.30),(-.37,y,.23),.024,'metal',8)
    for y in (-.24,.24):
        rod(a,(.24,y,.45),(.72,y,1.01),.022,'metal')
        rod(a,(.23,y-.014,.43),(.23,y+.014,.43),.039,'dark_metal',8)
    rod(a,(.72,-.24,1.01),(.72,.24,1.01),.029,'black')
    handle(a,-.12,-.04,.57,.22,.09,'black')
    for y in (-.307,.307):
        box(a,(-.27,y,.34),(.065,.027,.11),'metal')
        for x in (-.04,.035,.11):box(a,(x,y,.41),(.045,.013,.03),'dark_metal')
    rod(a,(.33,-.27,.43),(.68,-.27,.92),.008,'black',6)
    box(a,(.2,-.307,.29),(.20,.012,.075),'white')

@item('towable_leaf_vacuum','large')
def build(a):
    for y in (-.39,.39):box(a,(0,y,.39),(1.48,.09,.14),'dark_metal')
    for x in (-.61,.59):box(a,(x,0,.39),(.10,.88,.14),'dark_metal')
    for y in (-.56,.56):wheel(a,0,y,.33,.33,.18)
    xz_shell(a,[(-.30,.47),(.61,.47),(.61,.91),(.46,1.10),(-.19,1.10),(-.30,.95)],-.35,.35,'yellow')
    # Centrifugal blower scroll, intake flange and ribbed hose.
    rod(a,(-.42,-.34,.88),(-.42,.34,.88),.34,'yellow',12)
    rod(a,(-.42,-.39,.88),(-.42,-.35,.88),.255,'dark_metal',12)
    hose=[(-.42,-.41,.88),(-.64,-.63,.77),(-.87,-.75,.48),(-1.12,-.82,.20)]
    a.tube(hose,.12,'black',10)
    for i in range(12):
        t=i/11;xx=-.64-.48*t;yy=-.63-.19*t;zz=.77-.57*t
        a.torus((xx,yy,zz),.121,.010,'dark_metal',axis=(-.48,-.19,-.57),segments=10,sides=4)
    a.cone((-1.12,-.82,.20),(-1.27,-.86,.12),.13,'dark_metal',10,radius2=.17)
    for sign in (-1,1):
        y=sign*.359
        box(a,(.23,y,.78),(.54,.025,.47),'yellow')
        for z in (.67,.75,.83,.91):box(a,(.24,y+sign*.017,z),(.39,.015,.025),'black')
        box(a,(.45,y+sign*.025,.57),(.04,.025,.09),'metal')
        a.beam((-.37,sign*.55,.57),(-.22,sign*.55,.72),.23,.035,'yellow')
        box(a,(0,sign*.55,.725),(.46,.23,.035),'yellow')
        a.beam((.22,sign*.55,.72),(.36,sign*.55,.57),.23,.035,'yellow')
    # Square discharge chute has a diagonal elbow and a visible open mouth.
    xz_shell(a,[(-.56,1.00),(-.28,1.0),(-.28,1.55),(-.48,1.73),(-.75,1.73),(-.75,1.51),(-.56,1.51)],.15,.40,'yellow')
    box(a,(-.76,.275,1.615),(.018,.17,.15),'black')
    for y in (-.35,.35):a.beam((.53,y,.38),(1.30,0,.28),.085,.10,'dark_metal')
    box(a,(1.37,0,.30),(.24,.13,.11),'metal')
    a.sphere((1.49,0,.285),1,'metal',8,4,scale=(.10,.066,.055))
    box(a,(1.35,0,.375),(.13,.035,.035),'dark_metal')
    rod(a,(1.03,.16,.07),(1.03,.16,.41),.028,'metal',8)
    box(a,(1.03,.16,.05),(.20,.16,.04),'dark_metal')
    rod(a,(.32,.14,1.11),(.32,.14,1.30),.035,'dark_metal',8)
    rod(a,(.32,.14,1.30),(.43,.14,1.30),.035,'dark_metal',8)

@item('compact_municipal_street_sweeper','large')
def build(a):
    box(a,(0,0,.48),(2.72,1.06,.20),'dark_metal')
    for x in (-.88,.88):
        for y in (-.59,.59):wheel(a,x,y,.36,.33,.20)
    # Cab slopes at the windshield and turns beneath the nose; hopper tapers aft.
    cab=[(-1.34,.63),(-1.39,1.02),(-1.14,1.86),(-.43,1.91),(-.23,1.77),(-.23,.63)]
    xz_shell(a,cab,-.535,.535,'yellow')
    xz_shell(a,[(-1.16,1.87),(-.44,1.92),(-.21,1.81),(-.21,1.92),(-1.20,1.99)],-.58,.58,'yellow')
    # Windshield is truly raked; rubber seals and center divider follow its plane.
    wind=[(-1.376,-.46,1.095),(-1.376,.46,1.095),(-1.166,.46,1.806),(-1.166,-.46,1.806)]
    a.mesh(wind,[(0,1,2,3)],'glass')
    a.tube(wind+[wind[0]],.019,'dark_metal',6)
    rod(a,(-1.38,0,1.10),(-1.17,0,1.81),.014,'dark_metal',6)
    rod(a,(-1.377,-.16,1.10),(-1.283,.27,1.44),.012,'black',6)
    for sign in (-1,1):
        yy=sign*.548
        xz_shell(a,[(-1.25,1.05),(-1.04,1.81),(-.46,1.85),(-.30,1.73),(-.30,1.05)],yy,yy+sign*.007,'dark_metal')
        xz_shell(a,[(-1.18,1.12),(-1.00,1.75),(-.70,1.78),(-.70,1.12)],yy+sign*.012,yy+sign*.018,'glass')
        xz_shell(a,[(-.66,1.12),(-.66,1.79),(-.47,1.79),(-.36,1.69),(-.36,1.12)],yy+sign*.012,yy+sign*.018,'glass')
        box(a,(-.72,yy,.90),(.79,.025,.23),'yellow')
        box(a,(-.38,yy+sign*.03,1.02),(.14,.025,.034),'dark_metal')
        for zz in (.91,1.61):box(a,(-1.075,yy+sign*.02,zz),(.038,.032,.082),'metal')
        a.tube([(-.49,yy,1.64),(-.49,sign*.73,1.72),(-.66,sign*.77,1.72)],.018,'dark_metal',6)
        box(a,(-.70,sign*.775,1.65),(.11,.07,.22),'black')
        box(a,(-.47,sign*.63,.64),(.36,.21,.035),'metal')
        for xx in (-.56,-.45,-.34):box(a,(xx,sign*.64,.665),(.018,.14,.007),'dark_metal')
    xz_shell(a,[(-.10,.65),(1.24,.65),(1.36,1.32),(1.15,1.68),(.19,1.68),(-.10,1.44)],-.54,.54,'white')
    for sign in (-1,1):
        yy=sign*.556
        xz_shell(a,[(.24,.85),(1.13,.85),(1.20,1.35),(1.06,1.52),(.24,1.52)],yy,yy+sign*.018,'concrete_light')
        for zz in (1.01,1.10,1.19,1.28):box(a,(.67,yy+sign*.024,zz),(.66,.015,.031),'dark_metal')
        for xx in (.25,1.11):box(a,(xx,yy+sign*.033,.94),(.045,.025,.08),'metal')
        # Mudguard arches clear the tire silhouette.
        for xx in (-.88,.88):
            pts=[(xx+.39*cos(j*pi/6),yy+sign*.05,.36+.39*sin(j*pi/6)) for j in range(7)]
            a.tube(pts,.038,'yellow' if xx<0 else 'white',6)
    box(a,(-1.40,0,.66),(.15,1.17,.14),'black')
    for y in (-.41,.41):
        box(a,(-1.481,y,.87),(.03,.19,.14),'dark_metal')
        box(a,(-1.498,y,.87),(.017,.14,.093),'light')
    for y in (-.78,.78):
        brush(a,-.50,y,.018,.29)
        a.tube([(-.25,y*.59,.44),(-.37,y*.83,.33),(-.50,y,.25)],.035,'metal',8)
        a.tube([(-.16,y*.62,.63),(-.22,y*.76,.43),(-.48,y,.28)],.018,'black',6)
    # Central suction shoe and duct connect the brushes to the hopper.
    box(a,(-.13,0,.15),(.39,.68,.13),'dark_metal')
    a.tube([(-.10,0,.22),(.03,0,.52),(.16,0,.78)],.12,'black',10)
    rod(a,(.28,.28,1.68),(.28,.28,1.90),.048,'dark_metal',10)
    rod(a,(.28,.28,1.90),(.41,.28,1.90),.048,'dark_metal',10)
    rod(a,(-.67,0,1.99),(-.67,0,2.06),.09,'dark_metal',10)
    a.cone((-.67,0,2.06),(-.67,0,2.18),.08,'orange',10,radius2=.063)
    box(a,(1.39,0,.77),(.11,1.09,.16),'dark_metal')
    for y in (-.41,.41):box(a,(1.453,y,.94),(.032,.14,.16),'red')
    box(a,(1.45,0,1.22),(.025,.57,.32),'dark_metal')
    for y in (-.20,-.10,0,.10,.20):box(a,(1.468,y,1.22),(.02,.025,.26),'metal')

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
