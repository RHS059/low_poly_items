"""Fifty crafted low-poly American mail, delivery, cargo and logistics props."""
import math
from assetlib import Asset, register

CAT='mail_delivery_cargo'
M='dark_metal'; S='steel'; W='wood'; WD='wood_dark'; K='rubber'

def shell(a,p,size,mat,edge=.035):
    """Formed enclosure with broad rolled corners and distinct edge shoulders."""
    x,y,z=p;w,d,h=size;e=min(edge,w*.22,d*.22,h*.25)
    vs=[]
    for zz,inset in ((z-h/2,e*.5),(z-h/2+e,0),(z+h/2-e,0),(z+h/2,e*.65)):
        hw=w/2-inset;hd=d/2-inset;c=min(e,hw*.35,hd*.35)
        vs += [(x+xx,y+yy,zz) for xx,yy in ((-hw+c,-hd),(hw-c,-hd),(hw,-hd+c),(hw,hd-c),(hw-c,hd),(-hw+c,hd),(-hw,hd-c),(-hw,-hd+c))]
    fs=[tuple(reversed(range(8))),tuple(range(24,32))]
    fs += [(k*8+j,k*8+(j+1)%8,(k+1)*8+(j+1)%8,(k+1)*8+j) for k in range(3) for j in range(8)]
    a.mesh(vs,fs,mat)


def fabric(a,p,size,mat='cream',open_top=False):
    """Twelve-sided bulged textile volume; open hampers include inside walls."""
    x,y,z=p;w,d,h=size
    outline=[(-.38,-.48),(0,-.52),(.38,-.48),(.48,-.32),(.52,0),(.48,.32),(.38,.48),(0,.52),(-.38,.48),(-.48,.32),(-.52,0),(-.48,-.32)]
    rings=[(-.5,.78),(-.05,1.0),(.5,.85 if not open_top else .97)]
    vs=[(x+px*w*sc,y+py*d*sc,z+zz*h) for zz,sc in rings for px,py in outline]
    fs=[tuple(reversed(range(12)))]
    fs += [(k*12+j,k*12+(j+1)%12,(k+1)*12+(j+1)%12,(k+1)*12+j) for k in range(2) for j in range(12)]
    if not open_top:fs.append(tuple(range(24,36)))
    else:
        vs += [(x+px*w*.89,y+py*d*.89,z+h*.47) for px,py in outline]
        vs += [(x+px*w*.70,y+py*d*.70,z-h*.39) for px,py in outline]
        fs += [(24+j,24+(j+1)%12,36+(j+1)%12,36+j) for j in range(12)]
        fs += [(36+j,36+(j+1)%12,48+(j+1)%12,48+j) for j in range(12)]
        fs.append(tuple(range(48,60)))
    a.mesh(vs,fs,mat)


def fork_blade(a,x,y0,y1,z,w,h,mat):
    """A tapered forged toe with clipped nose corners, not a rectangular bar."""
    c=min(.035,w*.20);tip=min(.16,(y1-y0)*.18)
    plan=[(-w/2+c,y0),(w/2-c,y0),(w/2,y0+tip),(w/2,y1),(-w/2,y1),(-w/2,y0+tip)]
    vs=[(x+xx,yy,z) for xx,yy in plan]+[(x+xx,yy,z+(h*.38 if yy==y0 else h)) for xx,yy in plan]
    a.mesh(vs,[(5,4,3,2,1,0),(6,7,8,9,10,11)]+[(j,(j+1)%6,(j+1)%6+6,j+6) for j in range(6)],mat)


def b(a,p,s,m=M,rot=None): a.box(p,s,m,rot=rot)
def r(a,p,q,t=.025,m=M,n=8): a.cylinder(p,q,t,m,n)
def line(a,points,t=.02,m=M): a.tube(points,t,m,sides=6)
def bolt(a,p,axis='y'):
    v={'x':(.006,0,0),'y':(0,.006,0),'z':(0,0,.006)}[axis]
    r(a,tuple(p[i]-v[i] for i in range(3)),tuple(p[i]+v[i] for i in range(3)),.012,S,6)
def handle(a,x,y,z,w=.16,m=M):
    line(a,[(x-w/2,y+.035,z),(x-w/2,y,z),(x+w/2,y,z),(x+w/2,y+.035,z)],.014,m)
def wheel(a,x,y,z,radius=.10,width=.055):
    # A shouldered industrial tyre; separate recessed hub and axle ends.
    vs=[]
    for xx,rr in ((x-width/2,radius*.83),(x-width*.30,radius),(x+width*.30,radius),(x+width/2,radius*.83)):
        vs.extend((xx,y+rr*math.cos(j*math.tau/10),z+rr*math.sin(j*math.tau/10)) for j in range(10))
    fs=[tuple(reversed(range(10))),tuple(range(30,40))]+[(k*10+j,k*10+(j+1)%10,(k+1)*10+(j+1)%10,(k+1)*10+j) for k in range(3) for j in range(10)]
    a.mesh(vs,fs,K)
    r(a,(x-width*.54,y,z),(x+width*.54,y,z),radius*.47,S,8)
    r(a,(x-width*.59,y,z),(x+width*.59,y,z),radius*.17,M,6)
def caster(a,x,y,z=.10,radius=.08):
    wheel(a,x,y,z,radius,.045)
    b(a,(x,y,z+radius),(.055,.10,.045),S)
    b(a,(x,y-.017,z+.05),(.067,.033,.09),M)
def label(a,x,y,z,w=.15,h=.08,m='paper'):
    b(a,(x,y,z),(w,.008,h),m)
    for i in range(3): b(a,(x-w*.12,y-.006,z+h*(.22-i*.22)),(w*.55,.003,.006),M)
def latch(a,x,y,z):
    b(a,(x,y,z),(.045,.016,.095),S);b(a,(x,y-.012,z-.01),(.026,.015,.032),M)
def hinge(a,x,y,z,h=.09): r(a,(x,y,z-h/2),(x,y,z+h/2),.013,S,6)
def feet(a,w,d,z=.07):
    for x in (-w/2,w/2):
        for y in (-d/2,d/2): b(a,(x,y,z/2),(.095,.095,z),M)
def extrude(a,pts,y0,y1,m):
    n=len(pts);vs=[(x,y,z) for y in (y0,y1) for x,z in pts]
    fs=[tuple(range(n)),tuple(reversed(range(n,2*n)))]
    fs += [(i,i+n,(i+1)%n+n,(i+1)%n) for i in range(n)]
    a.mesh(vs,fs,m)
def arch(a,x,y,z,w,d,h,m):
    rad=w/2; spring=z+h-rad
    pts=[(x-rad,z),(x+rad,z)]+[(x+rad*math.cos(t*math.pi/6),spring+rad*math.sin(t*math.pi/6)) for t in range(7)]
    extrude(a,pts,y-d/2,y+d/2,m)
def pallet(a,w=1.2,d=1.,z=0,plastic=False):
    if plastic:
        for x in (-w*.4,0,w*.4):
            for y in (-d*.4,0,d*.4): b(a,(x,y,z+.07),(.16,.16,.14),M)
        for y in (-d*.4,0,d*.4): b(a,(0,y,z+.025),(w,.12,.05),M)
        for i in range(7): b(a,(-w/2+(i+.5)*w/7,0,z+.165),(w/7-.025,d,.055),'blue')
        for y in (-d*.46,d*.46):b(a,(0,y,z+.13),(w,.07,.05),'blue')
    else:
        for x in (-w*.38,0,w*.38):
            # Raised stringer web leaves two functional fork-entry notches.
            b(a,(x,0,z+.123),(.09,d,.054),WD)
            for yy in (-d*.43,0,d*.43):b(a,(x,yy,z+.063),(.09,d*.14,.067),WD)
        for y in (-d*.39,0,d*.39): b(a,(0,y,z+.026),(w,.12,.05),W)
        for i in range(6):
            x=-w/2+(i+.5)*w/6
            b(a,(x,0,z+.175),(w/6-.023,d,.045),'wood_light' if i%2 else W)
            for y in (-d*.36,d*.36): b(a,(x,y,z+.201),(.015,.014,.004),M)
def carton(a,x,y,z,w,d,h):
    shell(a,(x,y,z+h/2),(w,d,h),'cream',min(w,d,h)*.025)
    b(a,(x,y,z+h+.003),(.042,d+.006,.006),'sand')
    b(a,(x,y-d/2-.004,z+h*.52),(.042,.007,h),'sand')
    label(a,x+w*.2,y-d/2-.011,z+h*.6,w*.26,h*.22)
def band(a,x,y,z,w,d,h,axis='x'):
    if axis=='x':
        b(a,(x,y,z+h/2),(.033,d+.015,h+.012),M)
        b(a,(x,y,z+h+.009),(.046,d+.025,.012),M)
    else:
        for yy in (y-d/2-.009,y+d/2+.009):b(a,(x,yy,z+h/2),(w,.015,.03),M)
        for xx in (x-w/2-.009,x+w/2+.009):b(a,(xx,y,z+h/2),(.015,d,.03),M)
def drum(a,x,y,z,rad=.28,h=.87,m='navy'):
    rings=[(.018,.955),(.04,1.),(.085,1.),(.115,.972),(.27,.972),(.29,1.018),(.32,.972),(.68,.972),(.71,1.018),(.74,.972),(.90,.972),(.955,1.),(.982,.955)]
    vs=[(x+rad*rr*math.cos(j*math.tau/12),y+rad*rr*math.sin(j*math.tau/12),z+zz*h) for zz,rr in rings for j in range(12)]
    fs=[tuple(reversed(range(12))),tuple(range((len(rings)-1)*12,len(rings)*12))]
    fs += [(k*12+j,k*12+(j+1)%12,(k+1)*12+(j+1)%12,(k+1)*12+j) for k in range(len(rings)-1) for j in range(12)]
    a.mesh(vs,fs,m)
    r(a,(x+rad*.45,y,z+h-.028),(x+rad*.45,y,z+h+.003),.035,S,8)
def deck_cart(a,w,d,z=.23,m='navy'):
    shell(a,(0,0,z),(w,d,.065),m,.024)
    for x in (-w*.4,w*.4):
        for y in (-d*.39,d*.39):caster(a,x,y,.095,.078)
def register_asset(name,size='person'):
    def deco(fn):
        def make():
            a=Asset('b14_'+name,CAT,size);fn(a);return a.bottom_center()
        register('b14_'+name,CAT,size,make)
        return make
    return deco

@register_asset('curbside_arched_mailbox')
def mailbox(a):
    b(a,(0,.05,.60),(.10,.10,1.20),WD);b(a,(0,.03,1.12),(.48,.12,.09),W)
    arch(a,0,0,1.16,.31,.56,.34,'navy')
    arch(a,0,-.287,1.173,.282,.025,.311,'metal')
    b(a,(0,-.313,1.39),(.08,.04,.025),S)
    r(a,(-.12,-.306,1.19),(.12,-.306,1.19),.012,S)
    b(a,(.165,.05,1.45),(.019,.19,.025),'red');b(a,(.166,.12,1.50),(.02,.075,.095),'red')
    label(a,0,-.324,1.28,.12,.055)

@register_asset('wall_letterbox_with_flap','handheld')
def wall_mail(a):
    shell(a,(0,0,.22),(.34,.15,.44),'green',.018)
    b(a,(0,-.092,.34),(.30,.032,.087),M,(-.20,0,0))
    b(a,(0,-.083,.15),(.285,.02,.21),'green');latch(a,0,-.10,.22)
    for x in (-.145,.145): bolt(a,(x,-.08,.38))
    b(a,(0,0,.455),(.375,.19,.035),M)

@register_asset('curbside_cluster_mail_station')
def cluster_mail(a):
    b(a,(0,0,.065),(.58,.46,.13),M);b(a,(0,0,.52),(.19,.19,.88),S)
    shell(a,(0,0,1.27),(1.10,.47,.74),'metal',.027)
    for row in range(4):
        for col in range(4):
            x=(col-1.5)*.259;z=.96+row*.175
            b(a,(x,-.243,z),(.247,.025,.161),S)
            b(a,(x+.085,-.259,z),(.026,.012,.024),M)
            label(a,x-.049,-.260,z,.063,.026)
    b(a,(0,0,1.666),(1.16,.52,.04),M)

@register_asset('recessed_apartment_mail_wall')
def wall_bank(a):
    b(a,(0,0,.68),(1.26,.17,1.36),M)
    for col in range(3):
        for row in range(3):
            x=(col-1)*.40;z=.235+row*.44
            b(a,(x,-.095,z),(.38,.033,.414),'brown')
            b(a,(x,-.116,z+.107),(.265,.015,.027),K)
            label(a,x,-.120,z+.036,.12,.038)
            r(a,(x+.117,-.12,z-.115),(x+.117,-.133,z-.115),.02,S,8)
    for x in (-.6,.6):bolt(a,(x,-.095,1.30))

@register_asset('electronic_parcel_locker')
def locker(a):
    feet(a,1.9,.59,.12);shell(a,(0,0,1.09),(2.05,.70,1.96),'navy',.035)
    for x,w,rows in ((-.73,.52,3),(-.13,.52,4),(.64,.86,2)):
        h=1.79/rows
        for i in range(rows):
            z=.20+h*(i+.5);b(a,(x,-.364,z),(w,.029,h-.026),'metal')
            handle(a,x+w*.30,-.393,z,.07)
            label(a,x-w*.25,-.384,z+h*.28,.064,.032)
    b(a,(.21,-.411,1.33),(.22,.068,.32),M);b(a,(.21,-.448,1.39),(.165,.008,.155),'glass')
    b(a,(.21,-.449,1.24),(.11,.009,.025),S)
    b(a,(0,0,2.10),(2.16,.80,.065),M)

@register_asset('postal_collection_drop_box')
def collection(a):
    for x in (-.24,.24):
        for y in (-.20,.20):b(a,(x,y,.20),(.07,.07,.40),M)
    arch(a,0,0,.32,.64,.57,1.08,'navy')
    b(a,(0,-.296,1.13),(.48,.035,.17),M)
    b(a,(0,-.334,1.115),(.43,.078,.04),S)
    b(a,(0,-.295,.69),(.49,.026,.49),'navy');hinge(a,-.21,-.316,.67,.25);latch(a,.18,-.326,.70)
    label(a,0,-.318,.91,.22,.12);b(a,(0,-.308,.47),(.27,.012,.046),'white')

@register_asset('drive_through_mail_chute')
def drive_chute(a):
    b(a,(0,0,.065),(.57,.49,.13),M);shell(a,(0,0,.78),(.51,.48,1.43),'navy',.037)
    b(a,(0,-.18,1.42),(.68,.90,.24),'navy',(.16,0,0))
    b(a,(0,-.626,1.45),(.56,.035,.11),K)
    b(a,(0,-.65,1.52),(.68,.12,.045),S)
    b(a,(0,-.251,.69),(.41,.028,.66),'metal');latch(a,.14,-.28,.80)
    label(a,0,-.26,1.13,.25,.12)

@register_asset('building_mail_slot','handheld')
def slot(a):
    b(a,(0,0,.13),(.38,.055,.26),'brick')
    b(a,(0,-.033,.13),(.32,.025,.13),S)
    b(a,(0,-.049,.128),(.269,.012,.064),M)
    b(a,(0,-.061,.146),(.276,.018,.064),'metal',(-.2,0,0))
    for x in (-.142,.142):bolt(a,(x,-.052,.13))

@register_asset('postal_relay_storage_box')
def relay(a):
    feet(a,.60,.49,.23);arch(a,0,0,.20,.75,.62,1.14,'green')
    b(a,(0,-.324,.70),(.62,.03,.74),'green')
    for z in (.43,.98):hinge(a,-.28,-.347,z,.12)
    handle(a,.21,-.368,.83,.09);latch(a,.21,-.35,.65)
    label(a,0,-.351,1.08,.26,.086)

@register_asset('home_delivery_lock_chest')
def chest(a):
    feet(a,.65,.48,.08);shell(a,(0,0,.43),(.76,.60,.70),'brown',.035)
    b(a,(0,0,.81),(.82,.67,.08),'dark_metal',(.075,0,0))
    for x in (-.27,.27):b(a,(x,.31,.79),(.11,.035,.075),S)
    latch(a,0,-.33,.74);handle(a,0,-.35,.47,.20)
    for x in (-.31,.31):b(a,(x,-.307,.42),(.021,.015,.59),M)
    label(a,0,-.31,.60,.20,.07)

@register_asset('mail_sack_sorting_stand')
def sack_stand(a):
    for x in (-.25,.25):
        for y in (-.20,.20):
            r(a,(x,y,0),(x,y,1.0),.025,S)
        r(a,(x,-.20,.07),(x,.20,.07),.025,S)
    fabric(a,(0,0,.51),(.46,.36,.78),'sand',True)
    for y in (-.20,.20):r(a,(-.25,y,1.),(.25,y,1.),.022,S)
    for x in (-.25,.25):r(a,(x,-.20,1.),(x,.20,1.),.022,S)
    for x in (-.16,.16):line(a,[(x,-.17,.86),(x,-.205,1.02),(x,-.20,.93)],.014,WD)
    label(a,0,-.196,.51,.19,.09)

@register_asset('postal_carrier_satchel','handheld')
def satchel(a):
    fabric(a,(0,0,.145),(.38,.14,.29),'navy')
    b(a,(0,-.078,.22),(.40,.025,.15),'blue',(-.05,0,0))
    b(a,(0,-.094,.10),(.15,.025,.085),'blue')
    for x in (-.17,.17):line(a,[(x,0,.28),(x,.012,.50),(x*.7,.005,.57)],.018,WD)
    line(a,[(-.119,.005,.57),(.119,.005,.57)],.018,WD)
    for x in (-.13,.13):latch(a,x,-.10,.16)
    label(a,0,-.102,.24,.18,.055)

@register_asset('mobile_letter_sorting_cubbies')
def cubbies(a):
    deck_cart(a,1.08,.55,.24,'metal')
    b(a,(0,.23,1.02),(1.04,.035,1.52),'brown')
    for x in (-.52,.52):b(a,(x,0,1.02),(.035,.50,1.52),W)
    for row in range(5):b(a,(0,0,.32+row*.29),(1.04,.50,.025),'wood_light')
    b(a,(0,0,1.77),(1.08,.53,.04),W)
    for x in (-.26,0,.26):b(a,(x,0,1.04),(.02,.49,1.44),W)
    for col,row in ((0,0),(2,1),(1,2),(3,3),(0,3),(2,4)):
        b(a,(-.39+col*.26,-.03,.35+row*.29),(.21,.35,.055),'paper')
    line(a,[(-.57,-.19,1.1),(-.68,-.19,1.1),(-.68,.19,1.1),(-.57,.19,1.1)],.021,M)

@register_asset('postal_rolling_canvas_hamper')
def hamper(a):
    deck_cart(a,.78,.62,.23,'metal')
    for x in (-.38,.38):
        for y in (-.30,.30):r(a,(x,y,.23),(x,y,1.03),.023,S)
    fabric(a,(0,0,.61),(.72,.55,.69),'cream',True)
    for y in (-.31,.31):r(a,(-.39,y,1.01),(.39,y,1.01),.025,S)
    for x in (-.39,.39):r(a,(x,-.31,1.01),(x,.31,1.01),.025,S)
    line(a,[(-.30,.31,.88),(-.30,.44,1.11),(.30,.44,1.11),(.30,.31,.88)],.025,M)
    label(a,0,-.292,.62,.28,.13)
    for x in (-.28,.28):
        for y in (-.30,.30):
            a.beam((x,y*.85,.925),(x,y,1.026),.045,.014,'sand')
            a.beam((x,y,1.026),(x,y*.89,.94),.045,.014,'sand')

@register_asset('parcel_hand_truck')
def handtruck(a):
    for x in (-.19,.19):
        line(a,[(x,0,.14),(x,0,1.12),(x,.13,1.27),(x,.23,1.27)],.027,'blue')
        wheel(a,x*1.45,.075,.15,.15,.065)
    for z in (.22,.55,.88):b(a,(0,0,z),(.42,.045,.055),'blue')
    b(a,(0,-.18,.058),(.48,.40,.04),'metal')
    r(a,(-.29,.075,.15),(.29,.075,.15),.03,S)
    for x in (-.19,.19):r(a,(x,.12,1.27),(x,.235,1.27),.037,K)

@register_asset('stair_climbing_appliance_dolly')
def stair_dolly(a):
    for x in (-.22,.22):
        r(a,(x,0,.17),(x,0,1.38),.030,'orange')
        line(a,[(x,0,1.32),(x,.20,1.48),(x*.55,.22,1.48)],.03,M)
    for z in (.30,.75,1.2):b(a,(0,0,z),(.48,.052,.073),'orange')
    b(a,(0,-.18,.07),(.56,.40,.055),S)
    for x in (-.33,.33):
        for t in range(3):
            ang=math.tau*t/3; yy=.09+.14*math.sin(ang);zz=.25+.14*math.cos(ang)
            r(a,(x,.09,.25),(x,yy,zz),.035,M,6);wheel(a,x,yy,zz,.095,.048)
    for z in (.53,.94):b(a,(0,-.055,z),(.47,.035,.07),K)
    b(a,(0,-.07,.72),(.37,.016,.045),WD);b(a,(.20,-.075,.72),(.045,.033,.07),S)

@register_asset('folding_platform_delivery_cart')
def flatcart(a):
    deck_cart(a,.62,.92,.235,'blue')
    b(a,(0,0,.275),(.57,.86,.024),K)
    line(a,[(-.245,.35,.26),(-.245,.35,.91),(.245,.35,.91),(.245,.35,.26)],.028,S)
    r(a,(-.22,.35,.91),(.22,.35,.91),.039,K)
    for x in (-.25,.25):b(a,(x,.35,.32),(.065,.08,.14),M);bolt(a,(x,.305,.32))

@register_asset('wire_cage_roll_container')
def rollcage(a):
    deck_cart(a,.80,.70,.25,'metal')
    for x in (-.39,.39):
        for y in (-.34,.34):r(a,(x,y,.27),(x,y,1.80),.024,S)
    for z in (.45,.85,1.25,1.79):
        for y in (-.34,.34):r(a,(-.39,y,z),(.39,y,z),.013,S,6)
        for x in (-.39,.39):r(a,(x,-.34,z),(x,.34,z),.013,S,6)
    for x in (-.26,-.13,0,.13,.26):
        for y in (-.34,.34):r(a,(x,y,.28),(x,y,1.79),.009,S,6)
    for y in (-.20,-.07,.07,.20):
        for x in (-.39,.39):r(a,(x,y,.28),(x,y,1.79),.009,S,6)
    latch(a,.30,-.367,1.03);hinge(a,-.39,-.358,.56,.15);hinge(a,-.39,-.358,1.44,.15)

@register_asset('manual_pallet_jack')
def palletjack(a):
    for x in (-.22,.22):
        fork_blade(a,x,-.865,.265,.063,.17,.095,'yellow')
        wheel(a,x,-.73,.07,.07,.10)
    shell(a,(0,.31,.17),(.61,.26,.22),'yellow',.05)
    r(a,(0,.32,.10),(0,.32,.43),.075,M,10)
    for x in (-.11,.11):wheel(a,x,.32,.125,.125,.072)
    r(a,(0,.32,.37),(0,.62,1.13),.036,M)
    line(a,[(-.17,.61,1.11),(-.17,.65,1.26),(.17,.65,1.26),(.17,.61,1.11),(-.17,.61,1.11)],.027,K)
    b(a,(0,.605,1.06),(.07,.06,.10),S)

@register_asset('warehouse_counterbalance_forklift','large')
def forklift(a):
    shell(a,(0,.18,.49),(1.04,1.42,.51),'yellow',.115)
    shell(a,(0,.78,.64),(1.01,.31,.65),'yellow',.12)
    b(a,(0,.91,.87),(.79,.05,.29),M)
    for x in (-.54,.54):
        for y in (-.43,.61):wheel(a,x,y,.29,.29,.15)
    shell(a,(0,.08,.82),(.45,.46,.13),K,.045);b(a,(0,.29,1.03),(.46,.11,.44),K,(-.12,0,0))
    for x in (-.46,.46):
        for y in (-.49,.53):b(a,(x,y,1.38),(.056,.056,1.34),M)
    for x in (-.50,.50):b(a,(x,.03,2.07),(.055,1.19,.07),M)
    for y in (-.54,.60):b(a,(0,y,2.07),(1.05,.055,.07),M)
    for x in (-.36,-.12,.12,.36):b(a,(x,.03,2.11),(.048,1.12,.035),S)
    for x in (-.35,.35):b(a,(x,-.67,1.14),(.12,.14,2.06),M)
    for z in (.32,1.35,2.13):b(a,(0,-.67,z),(.77,.11,.08),S)
    r(a,(0,-.71,.36),(0,-.71,1.75),.044,S,8)
    b(a,(0,-.80,.59),(.94,.08,.39),M)
    for x in (-.28,.28):
        b(a,(x,-.84,.38),(.10,.09,.68),M);fork_blade(a,x,-1.885,-.815,.0325,.13,.085,M)
    r(a,(.10,-.29,.74),(.10,-.38,1.20),.022,S)
    a.torus((.10,-.38,1.22),.14,.018,K,axis=(0,-.5,1),segments=10,sides=5)
    for x in (-.40,.40):b(a,(x,-.54,1.82),(.12,.10,.10),'light')
    r(a,(.35,.38,2.10),(.35,.38,2.22),.057,'orange',8)
    # Tilt cylinders, telescoping mast channels and load carriage rollers.
    for x in (-.35,.35):
        r(a,(x,-.23,.49),(x,-.63,.92),.045,M,8)
        r(a,(x,-.50,.78),(x,-.67,.97),.024,S,8)
        for yy in (-.598,-.742):b(a,(x,yy,1.14),(.15,.025,2.04),S)
        for zz in (.66,1.65):r(a,(x-.072,-.67,zz),(x+.072,-.67,zz),.062,M,10)
    # Rear-mounted LPG bottle, valve and straps clear the driver's seat.
    r(a,(-.34,.64,1.10),(.34,.64,1.10),.145,'concrete_light',12)
    for x in (-.22,.22):a.torus((x,.64,1.10),.151,.014,M,axis='x',segments=12,sides=4)
    r(a,(.34,.64,1.10),(.42,.64,1.10),.035,S,8)
    for zz in (.43,.52,.61):b(a,(0,.945,zz),(.66,.018,.028),M)
    for x in (-.30,.30):
        b(a,(x,-.34,.79),(.14,.19,.025),M,rot=(.20,0,0))
        r(a,(x,.18,.88),(x,.11,1.07),.009,S,6)
        r(a,(x,.10,1.065),(x,.10,1.10),.022,K,8)


@register_asset('empty_wood_shipping_pallet')
def woodpallet(a):pallet(a)

@register_asset('rackable_plastic_pallet')
def plasticpallet(a):pallet(a,plastic=True)

@register_asset('pallet_carton_stack')
def cartons(a):
    pallet(a)
    for k in range(3):
        for x in (-.29,.29):
            for y in (-.24,.24):carton(a,x,y,.20+k*.30,.55,.44,.28)
    for x in (-.32,.32):
        for y in (-.465,.465):b(a,(x,y,.66),(.025,.018,.93),M)
        b(a,(x,0,1.126),(.025,.96,.015),M)

@register_asset('pallet_four_chemical_drums')
def drumload(a):
    pallet(a,1.30,1.30)
    for x in (-.315,.315):
        for y in (-.315,.315):drum(a,x,y,.20,.29,.87,'navy')
    for z in (.44,.88):
        for y in (-.621,.621):b(a,(0,y,z),(1.22,.02,.035),M)
        for x in (-.621,.621):b(a,(x,0,z),(.02,1.22,.035),M)
    label(a,-.315,-.619,.70,.16,.19,'yellow')

@register_asset('pallet_bagged_mortar')
def cement(a):
    pallet(a)
    for z in range(5):
        for x in (-.29,.29):
            for y in (-.235,.235):
                fabric(a,(x,y,.285+z*.145),(.54,.43,.125),'sand')
                b(a,(x,y-.228,.285+z*.145),(.27,.009,.052),'paper')
                b(a,(x,y,.353+z*.145),(.32,.30,.008),'cream')
    for x in (-.36,.36):
        b(a,(x,0,.955),(.025,.96,.012),M)
        for y in (-.47,.47):b(a,(x,y,.58),(.025,.012,.75),M)

@register_asset('pallet_strapped_masonry_bricks')
def bricks(a):
    pallet(a,1.04,.86)
    for row in range(5):
        for xx in range(4):
            for yy in range(3):b(a,(-.36+xx*.24,-.27+yy*.27,.25+row*.11),(.224,.254,.10),'brick' if (row+xx)%3 else 'terracotta')
    for x in (-.25,.25):
        b(a,(x,0,.75),(.028,.85,.012),M)
        for y in (-.417,.417):b(a,(x,y,.48),(.028,.012,.56),M)

@register_asset('pallet_lumber_bundle')
def lumber(a):
    pallet(a,1.1,2.4)
    for row in range(4):
        for x in (-.40,-.20,0,.20,.40):b(a,(x,0,.25+row*.10),(.18,2.33,.083),'wood_light' if row%2 else W)
    for y in (-.75,.75):
        b(a,(0,y,.605),(1.01,.035,.015),M)
        for x in (-.505,.505):b(a,(x,y,.40),(.015,.035,.41),M)
        b(a,(0,y,.205),(1.04,.08,.045),WD)

@register_asset('skidded_steel_pipe_bundle')
def pipes(a):
    for y in (-.78,.78):b(a,(0,y,.07),(1.20,.14,.14),W)
    for row,n in ((0,5),(1,4),(2,3)):
        for i in range(n):
            x=(i-(n-1)/2)*.215;z=.25+row*.18
            r(a,(x,-1.09,z),(x,1.09,z),.102,'metal',8)
            r(a,(x,-1.104,z),(x,-1.098,z),.078,M,8)
            r(a,(x,1.098,z),(x,1.104,z),.078,M,8)
    for y in (-.69,.69):
        line(a,[(-.57,y,.15),(-.55,y,.33),(-.34,y,.68),(.34,y,.68),(.55,y,.33),(.57,y,.15),(-.57,y,.15)],.014,K)

@register_asset('wooden_cable_reel_on_skid')
def reel(a):
    pallet(a,1.10,.94)
    for x in (-.39,.39):
        r(a,(x-.035,0,.71),(x+.035,0,.71),.50,W,12)
        r(a,(x-.04,0,.71),(x+.04,0,.71),.12,WD,10)
        for t in range(6):
            ang=t*math.tau/6
            r(a,(x-.046,.36*math.sin(ang),.71+.36*math.cos(ang)),(x+.046,.36*math.sin(ang),.71+.36*math.cos(ang)),.022,S,6)
    r(a,(-.355,0,.71),(.355,0,.71),.39,K,12)
    for x in (-.26,-.13,0,.13,.26):a.torus((x,0,.71),.39,.018,M,axis='x',segments=12,sides=4)
    for y in (-.38,.38):b(a,(0,y,.24),(.88,.15,.08),WD)

@register_asset('ibc_tote_with_valve')
def ibc(a):
    pallet(a,1.2,1.,plastic=True)
    shell(a,(0,0,.69),(1.01,.83,.99),'cream',.105)
    for x in (-.53,.53):
        for y in (-.43,.43):r(a,(x,y,.22),(x,y,1.23),.02,S,6)
    for z in (.30,.62,.93,1.21):
        line(a,[(-.54,-.44,z),(.54,-.44,z),(.54,.44,z),(-.54,.44,z),(-.54,-.44,z)],.018,S)
    for x in (-.35,-.18,0,.18,.35):
        for y in (-.44,.44):r(a,(x,y,.27),(x,y,1.21),.012,S,6)
    for y in (-.28,0,.28):
        for x in (-.54,.54):r(a,(x,y,.27),(x,y,1.21),.012,S,6)
    r(a,(0,0,1.18),(0,0,1.27),.11,M,10)
    r(a,(0,-.43,.30),(0,-.56,.30),.049,M,8)
    b(a,(0,-.57,.34),(.12,.028,.026),'red');label(a,.24,-.452,.78,.24,.20)

@register_asset('braced_wood_shipping_crate')
def crate(a):
    for x in (-.36,.36):b(a,(x,0,.06),(.14,.81,.12),WD)
    b(a,(0,0,.58),(.92,.80,.97),W)
    for y in (-.412,.412):
        for x in (-.36,.36):b(a,(x,y,.60),(.095,.035,1.01),'wood_light')
        for z in (.18,1.015):b(a,(0,y,z),(.92,.035,.095),'wood_light')
        a.beam((-.34,y,.24),(.34,y,.94),.09,.035,WD)
    for x in (-.474,.474):
        for y in (-.29,.29):b(a,(x,y,.60),(.028,.09,1.01),'wood_light')
    for y in (-.27,.27):b(a,(0,y,1.08),(.96,.07,.04),WD)
    label(a,-.15,-.436,.72,.26,.19)

@register_asset('open_slatted_parts_crate')
def opencrate(a):
    b(a,(0,0,.045),(.73,.52,.09),WD)
    for x in (-.34,.34):
        for y in (-.235,.235):b(a,(x,y,.28),(.048,.048,.53),W)
    for z in (.14,.27,.40):
        for y in (-.245,.245):b(a,(0,y,z),(.74,.035,.095),'wood_light')
        for x in (-.355,.355):b(a,(x,0,z),(.035,.46,.095),W)
    for y in (-.245,.245):
        for x in (-.265,.265):b(a,(x,y,.51),(.20,.035,.075),W)
        b(a,(0,y,.55),(.74,.04,.025),W)
    for x in (-.355,.355):b(a,(x,0,.52),(.038,.47,.085),W)

@register_asset('reinforced_shipping_flight_case')
def flightcase(a):
    b(a,(0,0,.33),(.84,.48,.63),'navy')
    for z in (.045,.45,.625):
        for y in (-.246,.246):b(a,(0,y,z),(.86,.024,.028),S)
        for x in (-.426,.426):b(a,(x,0,z),(.024,.50,.028),S)
    for x in (-.425,.425):
        for y in (-.244,.244):b(a,(x,y,.33),(.032,.032,.63),S)
    for x in (-.25,.25):latch(a,x,-.264,.45)
    handle(a,0,-.292,.28,.22)
    for x in (-.35,.35):
        for y in (-.20,.20):b(a,(x,y,.022),(.09,.08,.044),M)
    label(a,0,-.25,.54,.21,.072)

@register_asset('capped_triangular_shipping_tube','handheld')
def mailing_tube(a):
    extrude(a,[(-.11,0),(.11,0),(0,.19)],-.43,.43,'cream')
    extrude(a,[(-.115,-.004),(.115,-.004),(0,.20)],-.44,-.41,WD)
    extrude(a,[(-.115,-.004),(.115,-.004),(0,.20)],.41,.44,WD)
    b(a,(0,-.005,.101),(.068,.24,.009),'paper',rot=(0,math.pi/3,0))
    for yy in (-.22,.22):b(a,(0,yy,.006),(.22,.024,.012),'sand')

@register_asset('insulated_medical_shipping_chest')
def coldchest(a):
    shell(a,(0,0,.25),(.59,.42,.46),'cream',.035);shell(a,(0,0,.50),(.63,.45,.07),'white',.025)
    for x in (-.30,.30):
        line(a,[(x,-.11,.39),(x*1.12,-.11,.31),(x*1.12,.11,.31),(x,.11,.39)],.022,'blue')
    for x in (-.19,.19):latch(a,x,-.232,.45)
    b(a,(0,-.222,.25),(.21,.015,.16),'blue')
    b(a,(0,-.234,.25),(.10,.012,.035),'white');b(a,(0,-.234,.25),(.035,.012,.10),'white')
    for y in (-.16,.16):b(a,(0,y,.024),(.49,.06,.048),M)

@register_asset('steel_shipping_drum')
def single_drum(a):
    drum(a,0,0,0,.285,.87,'green')
    label(a,0,-.287,.48,.20,.23,'cream')
    r(a,(-.12,.02,.843),(-.12,.02,.885),.021,S,8)

@register_asset('stackable_attached_lid_delivery_tote')
def tote(a):
    shell(a,(0,0,.19),(.62,.42,.35),'blue',.042)
    b(a,(0,0,.382),(.66,.455,.045),'navy')
    for x in (-.16,.16):b(a,(x,0,.410),(.304,.445,.016),'metal')
    for x in (-.27,-.09,.09,.27):
        for y in (-.216,.216):b(a,(x,y,.19),(.025,.022,.30),'navy')
    for y in (-.230,.230):b(a,(0,y,.32),(.20,.014,.046),M)
    for x in (-.31,.31):b(a,(x,0,.31),(.014,.16,.042),M)
    label(a,.10,-.234,.21,.14,.08)

@register_asset('skidded_wrapped_appliance')
def appliance(a):
    pallet(a,.83,.79)
    shell(a,(0,0,1.03),(.68,.62,1.64),'white',.06)
    b(a,(0,-.322,1.11),(.62,.022,1.47),'paper')
    for x in (-.35,.35):
        for y in (-.323,.323):b(a,(x,y,1.03),(.05,.047,1.69),'sand')
    for z in (.55,1.48):
        for y in (-.351,.351):b(a,(0,y,z),(.72,.018,.043),M)
        for x in (-.372,.372):b(a,(x,0,z),(.018,.71,.043),M)
    b(a,(0,0,1.885),(.75,.69,.05),'cream')
    label(a,0,-.34,1.45,.28,.20)
    b(a,(.18,-.35,.82),(.038,.035,.28),'sand')

@register_asset('bulk_fertilizer_sack_on_pallet')
def bulkbag(a):
    pallet(a,1.10,1.10)
    # Filled woven sack has soft shoulder folds and a cinched crown.
    fabric(a,(0,0,.68),(1.0,1.0,.96),'cream')
    for x in (-.40,.40):
        for y in (-.40,.40):line(a,[(x,y,.85),(x,y,1.26),(x*.70,y*.70,1.31),(x*.70,y*.70,1.11)],.024,'sand')
    r(a,(0,0,1.12),(0,0,1.29),.09,'paper',8)
    r(a,(0,0,1.20),(0,0,1.23),.095,WD,8)
    label(a,0,-.522,.60,.33,.25)

@register_asset('cargo_net_secured_mixed_freight')
def netload(a):
    pallet(a,1.2,1.)
    carton(a,-.28,0,.20,.52,.82,.52);carton(a,.29,-.20,.20,.48,.40,.79);carton(a,.29,.25,.20,.48,.44,.41)
    carton(a,-.28,.06,.72,.45,.60,.28)
    for x in (-.49,-.25,0,.25,.49):
        line(a,[(x,-.51,.19),(x,-.49,.85),(x,-.31,1.08),(x,.31,1.08),(x,.49,.85),(x,.51,.19)],.009,WD)
    for y in (-.38,-.19,0,.19,.38):
        line(a,[(-.59,y,.19),(-.56,y,.84),(-.40,y,1.09),(.40,y,1.09),(.56,y,.84),(.59,y,.19)],.009,WD)
    for x in (-.52,.52):
        for y in (-.46,.46):b(a,(x,y,.24),(.045,.045,.075),M)

@register_asset('twenty_foot_freight_container','large')
def container(a):
    b(a,(0,0,1.28),(2.44,6.06,2.56),'navy')
    for x in (-1.22,1.22):
        for y in (-3.03,3.03):b(a,(x,y,1.28),(.10,.11,2.56),M)
    for z in (.07,2.50):
        for x in (-1.23,1.23):b(a,(x,0,z),(.08,6.05,.10),M)
        for y in (-3.04,3.04):b(a,(0,y,z),(2.47,.10,.10),M)
    for i in range(24):
        y=-2.86+i*.248
        for side in (-1,1):
            vs=[(side*(1.239+lift),y+yy,z) for z in (.12,2.46) for yy,lift in ((-.09,0),(-.035,.029),(.035,.029),(.09,0))]
            a.mesh(vs,[(j,j+1,j+5,j+4) for j in range(3)],'blue')
        vs=[(x,y+yy,2.572+lift) for x in (-1.15,1.15) for yy,lift in ((-.09,0),(-.035,.029),(.035,.029),(.09,0))]
        a.mesh(vs,[(j,j+1,j+5,j+4) for j in range(3)],'blue')
    for x in (-.595,.595):
        b(a,(x,-3.091,1.29),(1.14,.03,2.35),'metal')
        for xx in (x-.36,x+.36):
            r(a,(xx,-3.126,.17),(xx,-3.126,2.40),.022,S)
            handle(a,xx,-3.16,1.07,.16)
        for z in (.46,1.28,2.14):hinge(a,x+(.54 if x>0 else -.54),-3.12,z,.15)
    label(a,-.64,-3.121,2.13,.51,.17)
    for x in (-1.23,1.23):
        for y in (-3.04,3.04):
            for z in (.07,2.49):b(a,(x,y,z),(.14,.15,.13),S)

@register_asset('loading_dock_laminated_bumpers')
def bumpers(a):
    for x in (-.66,.66):
        b(a,(x,.02,.36),(.34,.11,.72),M)
        for i in range(7):b(a,(x,-.076,.09+i*.092),(.29,.17,.077),K)
        for xx in (x-.20,x+.20):
            b(a,(xx,.015,.36),(.065,.13,.72),'metal')
            for z in (.14,.59):bolt(a,(xx,-.06,z))
    b(a,(0,.105,.36),(1.85,.07,.76),'concrete')

@register_asset('mobile_yard_loading_ramp','large')
def ramp(a):
    # Sloped ramp surface, side curbs, axle and telescoping support legs.
    vs=[(-1.,-2.3,.06),(1.,-2.3,.06),(1.,2.3,1.12),(-1.,2.3,1.12),(-1.,-2.3,.16),(1.,-2.3,.16),(1.,2.3,1.22),(-1.,2.3,1.22)]
    a.mesh(vs,[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],M)
    for x in (-.97,.97):a.beam((x,-2.28,.22),(x,2.28,1.28),.07,.14,'yellow')
    for i in range(23):
        y=-2.2+i*.195;z=.16+(y+2.3)/4.6*1.06
        b(a,(0,y,z+.014),(1.86,.035,.025),S,rot=(math.atan(1.06/4.6),0,0))
    r(a,(-1.17,.8,.40),(1.17,.8,.40),.05,M)
    for x in (-1.14,1.14):wheel(a,x,.8,.4,.30,.13)
    for x in (-.73,.73):
        r(a,(x,1.65,.045),(x,1.65,1.02),.045,S)
        b(a,(x,1.65,.035),(.30,.31,.07),M)
    b(a,(0,2.42,1.215),(1.9,.32,.045),S)

@register_asset('recessed_hydraulic_dock_leveler','large')
def dockleveler(a):
    b(a,(0,0,.095),(2.12,2.48,.19),M)
    for x in (-1.01,1.01):b(a,(x,0,.23),(.11,2.48,.35),'yellow')
    a.beam((-.92,-1.16,.25),(-.92,1.13,.69),.11,.12,M)
    a.beam((.92,-1.16,.25),(.92,1.13,.69),.11,.12,M)
    b(a,(0,0,.53),(1.88,2.36,.12),'steel',rot=(.19,0,0))
    b(a,(0,1.36,.74),(1.90,.50,.055),'metal')
    r(a,(-.95,1.13,.715),(.95,1.13,.715),.032,M)
    r(a,(0,-.65,.16),(0,.58,.53),.074,'yellow');r(a,(0,.52,.51),(0,.96,.64),.04,S)
    for y in (-.92,-.55,-.18,.19,.56,.93):b(a,(0,y,.599+y*.19),(1.77,.025,.012),M,rot=(.19,0,0))

@register_asset('truck_tail_liftgate_assembly','large')
def liftgate(a):
    for x in (-.72,.72):
        b(a,(x,.45,.75),(.13,.14,1.48),M)
        a.beam((x,.45,.80),(x,-.44,.21),.09,.08,M)
        a.beam((x,.43,1.21),(x,-.42,.61),.08,.075,S)
        r(a,(x,.45,.25),(x,-.05,.63),.055,M)
        r(a,(x,-.05,.63),(x,-.27,.83),.031,S)
    b(a,(0,.44,1.39),(1.77,.15,.17),M)
    b(a,(0,-.72,.16),(1.94,1.45,.14),'metal')
    for x in (-.82,-.62,-.42,-.22,0,.22,.42,.62,.82):b(a,(x,-.72,.239),(.032,1.34,.015),S)
    b(a,(0,-1.465,.205),(1.96,.07,.07),'yellow')
    for x in (-.77,.77):r(a,(x,-.40,.23),(x,-.40,.65),.032,M)
    b(a,(.91,.37,1.02),(.11,.14,.23),'black')
    for z in (.97,1.06):r(a,(.91,.293,z),(.91,.283,z),.018,'green' if z>1 else 'red',8)

@register_asset('floor_pallet_weighing_scale')
def floorscale(a):
    b(a,(0,0,.08),(1.24,1.24,.16),M)
    b(a,(0,0,.17),(1.19,1.19,.035),S)
    for x in (-.52,.52):
        for y in (-.52,.52):b(a,(x,y,.02),(.09,.09,.04),K)
    r(a,(.70,.46,0),(.70,.46,1.23),.032,M)
    b(a,(.70,.43,1.26),(.38,.17,.20),'metal',rot=(.12,0,0))
    b(a,(.67,.331,1.28),(.22,.015,.09),'black')
    for x in (.59,.65,.71):b(a,(x,.321,1.28),(.032,.006,.052),'green')
    for x in (.79,.84):b(a,(x,.326,1.23),(.03,.018,.025),K)
    for y in (-.48,.48):b(a,(0,y,.192),(.84,.015,.009),M)

@register_asset('countertop_parcel_postage_scale','handheld')
def postagescale(a):
    shell(a,(0,0,.07),(.39,.30,.14),'metal',.025)
    b(a,(0,.035,.165),(.41,.29,.04),S)
    b(a,(0,-.13,.074),(.35,.11,.055),M,rot=(-.22,0,0))
    b(a,(-.053,-.181,.09),(.155,.015,.054),'black')
    for x in (-.10,-.053,-.006):b(a,(x,-.191,.09),(.025,.008,.036),'green')
    for x in (.065,.105,.145):b(a,(x,-.181,.085),(.025,.018,.023),'cream')
    for x in (-.15,.15):
        for y in (-.10,.10):b(a,(x,y,.012),(.045,.045,.024),K)

@register_asset('handheld_stretch_wrap_dispenser','handheld')
def wraptool(a):
    r(a,(0,0,.13),(0,0,.55),.095,'paper',12)
    for z in (.13,.55):r(a,(0,0,z-.014),(0,0,z+.014),.114,M,10)
    r(a,(0,0,.025),(0,0,.65),.021,S,8)
    r(a,(0,0,0),(0,0,.11),.034,K,8)
    r(a,(0,0,.59),(0,0,.70),.034,K,8)
    b(a,(.105,0,.35),(.017,.16,.40),'white')

@register_asset('strapping_reel_and_tensioner_cart')
def strapcart(a):
    for x in (-.25,.25):wheel(a,x,.1,.13,.13,.052)
    r(a,(-.29,.1,.13),(.29,.1,.13),.03,S)
    line(a,[(-.23,.1,.15),(-.23,.1,.90),(.23,.1,.90),(.23,.1,.15)],.023,'blue')
    for x in (-.27,.27):r(a,(x-.02,.08,.46),(x+.02,.08,.46),.27,M,12)
    r(a,(-.25,.08,.46),(.25,.08,.46),.23,K,12)
    r(a,(-.30,.08,.46),(.30,.08,.46),.04,S)
    b(a,(0,-.26,.11),(.56,.40,.045),'blue')
    b(a,(0,-.23,.27),(.46,.24,.05),'metal')
    b(a,(.07,-.23,.32),(.21,.13,.085),M)
    line(a,[(.03,-.23,.35),(.02,-.23,.47),(.17,-.23,.48)],.023,S)
    line(a,[(-.12,.04,.45),(-.12,-.23,.29),(-.12,-.36,.13)],.01,K)

@register_asset('expandable_roller_conveyor','large')
def conveyor(a):
    for y in (-1.2,0,1.2):
        for x in (-.38,.38):
            caster(a,x,y,.09,.075);r(a,(x,y,.18),(x,y,.82),.025,M)
    for x in (-.37,.37):
        for i in range(6):
            y=-1.42+i*.475
            a.beam((x,y,.48),(x,y+.475,.79),.03,.022,S)
            a.beam((x,y,.79),(x,y+.475,.48),.03,.022,S)
            bolt(a,(x,y,.79),axis='x')
    for i in range(18):
        y=-1.38+i*.162
        r(a,(-.38,y,.87),(.38,y,.87),.047,S,8)
        for x in (-.40,.40):r(a,(x-.015,y,.87),(x+.015,y,.87),.018,M,6)
    for x in (-.42,.42):r(a,(x,-1.42,.85),(x,1.42,.85),.018,M,6)
    for x in (-.36,.36):line(a,[(x,1.4,.84),(x,1.50,1.02)],.022,'yellow')
