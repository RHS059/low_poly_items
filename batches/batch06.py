"""Fifty portable maintenance tools. Metres; hard-face budget < 1,000 each."""
import math
from assetlib import Asset, register

CAT = 'hand_tools_and_portable_construction_tools'

def asset(name):
    return Asset('b06_' + name, CAT, 'handheld')

def finish(a):
    a.bottom_center()
    a.validate()
    assert sum(map(len, a.faces)) < 1000, (a.name, sum(map(len, a.faces)))
    return a

def poly(a, points, depth, mat='steel', y=0):
    """CCW X/Z silhouette, extruded across Y, including concave profiles."""
    points = list(points)
    if sum(points[i][0]*points[(i+1)%len(points)][1] - points[(i+1)%len(points)][0]*points[i][1] for i in range(len(points))) < 0:
        points.reverse()
    n = len(points)
    vs = [(x, y-depth/2, z) for x,z in points] + [(x,y+depth/2,z) for x,z in points]
    def cross2(p,q,r):
        return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    # Explicit ear clipping preserves the real negative spaces of curved grips,
    # square blades and wrench jaws even in simple fan-based catalog viewers.
    ids=list(range(n)); tris=[]
    while len(ids)>3:
        for k,i in enumerate(ids):
            h,j=ids[k-1],ids[(k+1)%len(ids)]
            p,q,r=points[h],points[i],points[j]
            if cross2(p,q,r)<=1e-14: continue
            if any(cross2(p,q,points[t])>=-1e-14 and cross2(q,r,points[t])>=-1e-14 and cross2(r,p,points[t])>=-1e-14 for t in ids if t not in (h,i,j)): continue
            tris.append((h,i,j));ids.pop(k);break
        else: raise ValueError('Untriangulatable tool silhouette')
    tris.append(tuple(ids))
    fs = tris + [tuple(i+n for i in reversed(t)) for t in tris]
    fs += [(i, i+n, (i+1)%n+n, (i+1)%n) for i in range(n)]
    a.mesh(vs,fs,mat)

def ring(a, center, outer, inner, depth, mat='steel', n=8, axis='y'):
    # Four rings joined explicitly: real open hole, no black painted substitute.
    x,y,z = center
    def pt(r,t,h):
        u,v=r*math.cos(t),r*math.sin(t)
        return (x+u,y+h,z+v) if axis=='y' else ((x+h,y+u,z+v) if axis=='x' else (x+u,y+v,z+h))
    vs=[]
    for h,r in [(-depth/2,outer),(depth/2,outer),(-depth/2,inner),(depth/2,inner)]:
        vs += [pt(r,2*math.pi*i/n,h) for i in range(n)]
    fs=[]
    for i in range(n):
        j=(i+1)%n
        fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
    if axis == 'y': fs = [tuple(reversed(f)) for f in fs]
    a.mesh(vs,fs,mat)

def bolt(a, x,z, r=.007, depth=.03, y=0, mat='silver'):
    a.cylinder((x,y-depth/2,z),(x,y+depth/2,z),r,mat,sides=6)

def grip(a,p1,p2,r=.017,mat='rubber',sides=8):
    # One connected octagonal grip with a palm swell and end chamfers.
    from assetlib import frame, sub, add, mul
    u,v,w=frame(sub(p2,p1));length=math.dist(p1,p2)
    rings=[(0,.80),(.07,1.0),(.40,1.07),(.83,.96),(1,.76)]
    vs=[]
    for t,sc in rings:
        c=add(p1,mul(w,length*t))
        for i in range(sides):
            th=2*math.pi*i/sides
            vs.append(add(c,add(mul(u,r*sc*math.cos(th)),mul(v,r*.85*sc*math.sin(th)))))
    fs=[tuple(reversed(range(sides))),tuple(range((len(rings)-1)*sides,len(rings)*sides))]
    fs += [(j*sides+i,j*sides+(i+1)%sides,(j+1)*sides+(i+1)%sides,(j+1)*sides+i) for j in range(len(rings)-1) for i in range(sides)]
    a.mesh(vs,fs,mat)


def ribs(a,zs,x=0,y=0,w=.035,d=.029,mat='dark_metal'):
    for z in zs: a.box((x,y,z),(w,d,.004),mat)

def handle_poly(a,points,depth=.025,mat='rubber'):
    poly(a,points,depth,mat)

def tooth_strip(a,x0,x1,z,step,depth=.002,down=.009,y=0):
    n=max(1,round((x1-x0)/step))
    for i in range(n):
        x=x0+(x1-x0)*i/n
        poly(a,[(x,z),(x+(x1-x0)/n*.55,z-down),(x+(x1-x0)/n,z)],depth,'steel',y)

def hammer_handle(a,zmax=.29,mat='wood'):
    grip(a,(0,0,.009),(0,0,zmax),.015,mat,8)
    a.cylinder((0,0,.002),(0,0,.020),.014,'wood_dark' if mat=='wood' else 'rubber',8,radius2=.017)
    a.box((0,0,zmax-.005),(.025,.026,.014),'dark_metal')


def claw_hammer():
    a=asset('claw_hammer'); hammer_handle(a,.295)
    a.box((-.013,0,.309),(.071,.039,.042),'dark_metal')
    a.cylinder((-.078,0,.309),(-.039,0,.309),.019,'steel',8,radius2=.016)
    a.cylinder((-.084,0,.309),(-.077,0,.309),.022,'silver',8)
    for y in [-.013,.013]:
        poly(a,[(.018,.297),(.079,.308),(.101,.336),(.053,.329),(.019,.327)],.015,'steel',y)
    a.box((0,-.0205,.315),(.023,.003,.014),'metal')
    return finish(a)

def ball_peen_hammer():
    a=asset('ball_peen_hammer');hammer_handle(a,.265)
    a.box((0,0,.28),(.049,.036,.039),'metal')
    a.cylinder((-.057,0,.28),(-.024,0,.28),.020,'steel',8)
    a.cylinder((.022,0,.28),(.047,0,.28),.011,'dark_metal',8)
    a.sphere((.052,0,.28),.021,'steel',8,3)
    return finish(a)

def rubber_mallet():
    a=asset('rubber_mallet');hammer_handle(a,.26)
    a.cylinder((-.07,0,.281),(.07,0,.281),.039,'rubber',10)
    a.cylinder((-.073,0,.281),(-.064,0,.281),.040,'black',10)
    a.cylinder((.064,0,.281),(.073,0,.281),.040,'black',10)
    a.box((0,-.036,.281),(.033,.006,.021),'dark_metal')
    return finish(a)

def club_hammer():
    a=asset('club_hammer');hammer_handle(a,.237,'teal')
    grip(a,(0,0,.015),(0,0,.13),.018)
    poly(a,[(-.073,.229),(.073,.229),(.083,.239),(.083,.284),(.073,.294),(-.073,.294),(-.083,.284),(-.083,.239)],.050,'dark_metal')
    a.box((-.081,0,.261),(.008,.052,.047),'steel');a.box((.081,0,.261),(.008,.052,.047),'steel')
    return finish(a)

def hatchet():
    a=asset('hatchet')
    poly(a,[(-.012,.01),(.013,.005),(.023,.043),(.016,.25),(.009,.335),(-.014,.334),(-.007,.20),(-.017,.044)],.026,'wood')
    a.box((0,0,.3),(.035,.041,.066),'dark_metal')
    poly(a,[(.01,.283),(.085,.258),(.118,.269),(.103,.35),(.077,.359),(.014,.332)],.023,'metal')
    poly(a,[(.089,.263),(.118,.269),(.103,.35),(.083,.355)],.010,'silver')
    a.box((-.027,0,.309),(.029,.035,.032),'steel')
    a.cylinder((0,-.015,.036),(0,.015,.036),.006,'wood_dark',8)
    return finish(a)

def cold_chisel():
    a=asset('cold_chisel')
    a.cylinder((0,0,.035),(0,0,.202),.011,'dark_metal',6)
    poly(a,[(-.019,0),(.019,0),(.011,.039),(-.011,.039)],.007,'steel')
    a.cylinder((0,0,.18),(0,0,.208),.013,'metal',6)
    a.cylinder((0,0,.207),(0,0,.213),.015,'steel',8)
    return finish(a)

def masonry_bolster():
    a=asset('masonry_bolster')
    poly(a,[(-.056,0),(.056,0),(.042,.065),(.013,.115),(-.013,.115),(-.042,.065)],.012,'steel')
    a.box((0,0,.003),(.112,.006,.006),'silver')
    a.cylinder((0,0,.08),(0,0,.225),.012,'dark_metal',6)
    a.cylinder((0,0,.12),(0,0,.215),.022,'teal',8)
    a.cylinder((0,0,.113),(0,0,.126),.042,'rubber',8)
    a.cylinder((0,0,.222),(0,0,.23),.018,'steel',8)
    return finish(a)

def crowbar():
    a=asset('crowbar')
    a.tube([(0,0,.065),(0,0,.56),(.014,0,.595),(.055,0,.614),(.083,0,.602),(.089,0,.576)],.012,'dark_metal',6)
    poly(a,[(-.016,0),(.014,0),(.012,.080),(-.010,.085)],.010,'steel')
    a.box((.089,0,.569),(.026,.034,.012),'steel')
    return finish(a)

def flat_nail_pull_bar():
    a=asset('flat_nail_pull_bar')
    poly(a,[(-.018,.025),(.011,.009),(.015,.018),(-.008,.044),(-.007,.254),(.010,.279),(.052,.288),(.054,.302),(-.005,.3),(-.021,.267)],.015,'dark_metal')
    for y in [-.010,.010]: poly(a,[(.031,.286),(.061,.284),(.067,.291),(.034,.304)],.010,'steel',y)
    a.box((-.003,0,.015),(.047,.012,.009),'steel',rot=(0,-.55,0))
    return finish(a)

# Wrenches, socket tools and keys ---------------------------------------------
def adjustable_wrench():
    a=asset('adjustable_wrench')
    poly(a,[(-.011,.036),(.011,.036),(.019,.146),(.029,.190),(.025,.221),(-.013,.222),(-.024,.187),(-.015,.15)],.017,'metal')
    # Fixed hooked jaw, open slot, movable jaw and exposed knurled adjuster.
    poly(a,[(-.023,.19),(-.047,.222),(-.042,.255),(-.014,.262),(-.012,.248),(-.026,.243),(-.025,.222),(-.010,.211)],.020,'steel')
    poly(a,[(.014,.2),(.025,.212),(.033,.25),(.021,.255),(.009,.221)],.021,'steel')
    a.box((.003,-.011,.218),(.025,.007,.020),'dark_metal')
    a.cylinder((-.009,-.015,.218),(.014,-.015,.218),.009,'metal',8)
    for x in [-.006,0,.006,.012]: a.box((x,-.023,.218),(.002,.003,.014),'steel')
    ring(a,(0,0,.025),.017,.007,.019,'steel',10)
    return finish(a)

def combination_wrench():
    a=asset('combination_wrench')
    a.box((0,0,.11),(.018,.009,.16),'steel')
    a.box((0,-.005,.113),(.009,.003,.111),'metal')
    ring(a,(0,0,.024),.024,.014,.011,'steel',8)
    poly(a,[(-.010,.18),(.012,.18),(.032,.204),(.026,.235),(.011,.235),(.016,.208),(-.009,.199),(-.025,.221),(-.036,.212)],.011,'steel')
    return finish(a)

def pipe_wrench():
    a=asset('pipe_wrench')
    poly(a,[(-.012,.009),(.013,.009),(.014,.198),(.025,.229),(.005,.25),(-.025,.237),(-.021,.197)],.027,'brick')
    a.box((-.011,0,.267),(.020,.022,.086),'steel')
    poly(a,[(-.023,.288),(.041,.288),(.046,.308),(-.023,.316)],.031,'dark_metal')
    a.box((.022,0,.239),(.044,.030,.023),'dark_metal')
    for x in [0,.008,.016,.024,.032]:
        a.box((x,0,.283),(.003,.032,.008),'steel')
        a.box((x,0,.253),(.003,.032,.006),'steel')
    a.cylinder((-.015,-.024,.234),(-.015,.024,.234),.020,'dark_metal',8)
    a.box((0,-.016,.088),(.012,.005,.123),'dark_metal')
    return finish(a)

def socket_ratchet():
    a=asset('socket_ratchet')
    a.beam((0,0,.03),(0,0,.199),.019,.010,'steel')
    grip(a,(0,0,.02),(0,0,.10),.017)
    a.cylinder((0,-.011,.219),(0,.012,.219),.025,'metal',10)
    a.cylinder((0,-.023,.219),(0,-.011,.219),.015,'steel',8)
    a.box((0,.021,.219),(.014,.026,.014),'steel')
    ring(a,(0,.04,.219),.022,.014,.028,'silver',8)
    a.box((.009,-.015,.234),(.018,.007,.007),'black',rot=(0,.3,0))
    return finish(a)

def torque_wrench():
    a=asset('torque_wrench')
    a.cylinder((0,0,.097),(0,0,.393),.011,'steel',8)
    grip(a,(0,0,.01),(0,0,.117),.023)
    a.cylinder((0,0,.107),(0,0,.14),.020,'metal',10)
    for z in [.018,.035,.052,.069,.086]: a.cylinder((0,0,z),(0,0,z+.004),.024,'dark_metal',8)
    a.cylinder((0,-.012,.410),(0,.011,.410),.025,'metal',10)
    a.box((0,.022,.410),(.014,.025,.014),'steel')
    for z in [.18,.20,.22,.24]: a.box((.008,-.008,z),(.007,.004,.002),'black')
    return finish(a)

def hex_key():
    a=asset('hex_key')
    a.cylinder((0,0,.008),(0,0,.174),.0058,'dark_metal',6)
    a.cylinder((0,0,.174),(.052,0,.174),.0058,'dark_metal',6)
    a.cylinder((.049,0,.174),(.055,0,.174),.0055,'steel',6)
    a.cylinder((0,0,.004),(0,0,.011),.0054,'steel',6)
    return finish(a)

def folding_hex_key_set():
    a=asset('folding_hex_key_set')
    for y in [-.019,.019]:
        poly(a,[(-.025,.015),(.025,.015),(.03,.03),(.03,.097),(.021,.111),(-.021,.111),(-.03,.095),(-.03,.03)],.006,'navy',y)
    for z in [.03,.093]: bolt(a,0,z,.008,.049,mat='steel')
    for i in range(4):
        y=-.012+i*.008
        a.cylinder((-.011,y,.039),(-.011,y,.086),.0036,'metal',6)
    for i,(x,z) in enumerate([(.082,.032),(.066,.070),(.040,.121)]):
        y=-.008+i*.008
        a.cylinder((0,y,.031),(x,y,z),.0036+i*.0005,'steel',6)
        a.cylinder((x,y,z),(x+.013,y,z+.008),.0036+i*.0005,'steel',6)
    return finish(a)

# Cutting and gripping pliers -------------------------------------------------
def bolt_cutters():
    a=asset('bolt_cutters')
    for s in [-1,1]:
        a.beam((s*.095,0,.017),(s*.036,0,.493),.022,.023,'brick')
        grip(a,(s*.095,0,.01),(s*.079,0,.16),.022)
        poly(a,[(s*x,z) for x,z in ([(-.016,.486),(.03,.478),(.068,.54),(.039,.584),(.009,.568)] if s==1 else reversed([(-.016,.486),(.03,.478),(.068,.54),(.039,.584),(.009,.568)]))],.019,'metal',s*.013)
        poly(a,[(s*x,z) for x,z in ([(.009,.551),(.050,.575),(.037,.645),(.005,.658),(0,.612)] if s==1 else reversed([(.009,.551),(.050,.575),(.037,.645),(.005,.658),(0,.612)]))],.033,'dark_metal')
        a.beam((s*.009,0,.611),(s*.006,0,.650),.008,.035,'steel')
        bolt(a,s*.028,.545,.013,.057)
    bolt(a,0,.579,.012,.041)
    return finish(a)

def combination_pliers():
    a=asset('combination_pliers')
    for s in [-1,1]:
        a.beam((s*.037,0,.015),(s*.009,0,.125),.014,.014,'steel');grip(a,(s*.037,0,.012),(s*.014,0,.101),.015,'teal',6)
        a.beam((s*.013,0,.10),(-s*.012,0,.154),.014,.018,'steel')
        poly(a,[(s*x,z) for x,z in ([(.007,.14),(.025,.16),(.022,.197),(.007,.197),(.004,.174)] if s==1 else reversed([(.007,.14),(.025,.16),(.022,.197),(.007,.197),(.004,.174)]))],.018,'metal')
        for z in [.171,.18,.19]: a.box((s*.006,0,z),(.005,.020,.003),'steel')
    bolt(a,0,.139,.012,.028)
    return finish(a)

def needle_nose_pliers():
    a=asset('needle_nose_pliers')
    for s in [-1,1]:
        a.beam((s*.035,0,.012),(s*.009,0,.105),.013,.014,'steel');grip(a,(s*.035,0,.012),(s*.016,0,.090),.014,'rubber',6)
        a.beam((s*.011,0,.078),(-s*.008,0,.132),.014,.017,'steel')
        poly(a,[(s*x,z) for x,z in ([(.004,.122),(.018,.133),(.005,.207),(.001,.208)] if s==1 else reversed([(.004,.122),(.018,.133),(.005,.207),(.001,.208)]))],.011,'steel')
        for z in [.15,.165,.18]:a.box((s*.004,0,z),(.003,.013,.002),'dark_metal')
    bolt(a,0,.123,.010,.028)
    return finish(a)

def locking_pliers():
    a=asset('locking_pliers')
    poly(a,[(-.027,.007),(-.013,.004),(-.004,.121),(-.019,.162),(-.029,.157),(-.017,.12)],.016,'metal')
    poly(a,[(.038,.02),(.045,.036),(.023,.12),(.009,.153),(-.004,.135),(.013,.099)],.019,'steel')
    poly(a,[(-.019,.139),(-.032,.179),(-.025,.207),(.008,.209),(.011,.196),(-.013,.19),(-.009,.166)],.022,'metal')
    poly(a,[(.013,.135),(.034,.163),(.030,.19),(.008,.191),(.009,.177),(.018,.173),(-.001,.154)],.022,'steel')
    a.beam((-.019,0,.040),(.022,0,.117),.010,.009,'dark_metal')
    a.beam((.013,-.017,.074),(.035,-.017,.04),.009,.007,'steel')
    a.cylinder((-.024,0,-.012),(-.024,0,.027),.006,'steel',8)
    a.cylinder((-.024,0,-.015),(-.024,0,-.004),.012,'metal',8)
    bolt(a,-.006,.147,.008,.030);bolt(a,.02,.118,.006,.030)
    for x in [-.010,0,.01]:a.box((x,0,.194),(.003,.024,.004),'dark_metal')
    return finish(a)

def wire_stripper():
    a=asset('wire_stripper')
    for sign in (-1,1):
        a.beam((sign*.04,0,.012),(sign*.011,0,.121),.012,.012,'steel')
        grip(a,(sign*.04,0,.01),(sign*.018,0,.092),.015,'navy',6)
        # Semicircular notches are empty geometry, each size cuts a real bite.
        edge=[(.002,.126)]
        for z,r in ((.140,.006),(.155,.005),(.169,.004),(.182,.003)):
            edge.extend([(.002,z-r),(.002+r*.8,z-r*.6),(.002+r,z),(.002+r*.8,z+r*.6),(.002,z+r)])
        pts=edge+[(.005,.198),(.024,.184),(.020,.135)]
        poly(a,[(sign*x,z) for x,z in pts],.010,'metal')
    bolt(a,0,.121,.010,.028)
    a.tube([(-.018,0,.081),(-.009,0,.074),(.008,0,.078),(.018,0,.09)],.002,'steel',4)
    return finish(a)


def aviation_snips():
    a=asset('aviation_snips')
    for s in [-1,1]:
        a.beam((s*.039,0,.015),(s*.017,0,.114),.015,.014,'steel');grip(a,(s*.039,0,.012),(s*.020,0,.096),.017,'green' if s==1 else 'rubber',6)
        a.beam((s*.018,0,.092),(-s*.008,0,.152),.020,.015,'metal')
    poly(a,[(-.013,.136),(.012,.157),(.01,.199),(-.011,.236),(-.022,.242),(-.008,.19)],.010,'steel',-.007)
    poly(a,[(-.009,.148),(.018,.147),(.03,.18),(-.008,.235),(-.001,.186)],.010,'metal',.007)
    bolt(a,0,.14,.012,.029);bolt(a,.006,.177,.009,.029)
    a.box((.02,-.017,.119),(.027,.005,.009),'steel',rot=(0,.4,0))
    return finish(a)

# Screwdrivers, marking and measuring ----------------------------------------
def flat_screwdriver():
    a=asset('flat_screwdriver')
    a.cylinder((0,0,.10),(0,0,.269),.004,'steel',8)
    poly(a,[(-.008,.27),(.008,.27),(.004,.25),(-.004,.25)],.002,'silver')
    a.cylinder((0,0,.017),(0,0,.112),.018,'teal',8,radius2=.013)
    a.cylinder((0,0,.009),(0,0,.024),.021,'rubber',8)
    for x in [-.014,.014]:a.box((x,-.008,.064),(.007,.011,.065),'rubber')
    a.cylinder((0,0,.108),(0,0,.12),.010,'dark_metal',8)
    return finish(a)

def stubby_phillips_screwdriver():
    a=asset('stubby_phillips_screwdriver')
    a.cylinder((0,0,.009),(0,0,.047),.026,'rubber',10,radius2=.022)
    a.cylinder((0,0,.047),(0,0,.059),.022,'navy',10,radius2=.012)
    a.cylinder((0,0,.059),(0,0,.093),.004,'steel',8)
    poly(a,[(-.004,.086),(.004,.086),(.001,.103),(-.001,.103)],.002,'silver')
    a.cylinder((0,0,.085),(0,0,.097),.003,'steel',4,radius2=.001)
    for x in [-.023,.023]:a.box((x,0,.029),(.006,.016,.024),'navy')
    a.cylinder((0,0,.003),(0,0,.01),.018,'dark_metal',8)
    return finish(a)

def utility_knife():
    a=asset('utility_knife')
    poly(a,[(-.021,0),(.021,0),(.026,.025),(.021,.139),(.014,.167),(-.019,.152),(-.028,.031)],.023,'metal')
    poly(a,[(-.018,.032),(.020,.032),(.017,.125),(-.016,.123)],.026,'rubber')
    a.box((0,-.015,.107),(.008,.005,.076),'black')
    a.box((0,-.020,.124),(.016,.009,.022),'teal')
    poly(a,[(-.013,.158),(.013,.17),(.013,.206),(-.013,.183)],.0018,'steel')
    a.box((0,.014,.044),(.012,.003,.044),'steel')
    bolt(a,0,.019,.005,.026)
    return finish(a)

def retractable_tape_measure():
    a=asset('retractable_tape_measure')
    poly(a,[(-.04,.006),(.033,.006),(.048,.021),(.048,.062),(.028,.082),(-.029,.082),(-.045,.064),(-.048,.026)],.034,'navy')
    a.cylinder((0,-.020,.045),(0,-.024,.045),.028,'rubber',10)
    a.cylinder((0,-.024,.045),(0,-.026,.045),.019,'metal',8)
    a.box((.015,0,.080),(.026,.035,.009),'rubber')
    a.box((.123,0,.022),(.155,.019,.0015),'cream')
    a.box((.202,0,.015),(.004,.024,.018),'steel')
    for i in range(11):a.box((.058+i*.012,-.005,.023),(.001,.008 if i%2 else .013,.001),'black')
    a.box((-.003,.024,.047),(.030,.012,.027),'steel')
    return finish(a)

def carpenters_square():
    a=asset('carpenters_square')
    poly(a,[(0,0),(.24,0),(.24,.029),(.033,.029),(.033,.40),(0,.40)],.003,'steel')
    for z in [.055,.085,.115,.145,.175,.205,.235,.265,.295,.325,.355,.385]:a.box((.009,-.002,z),(.013,.001,.0015),'black')
    for x in [.055,.085,.115,.145,.175,.205,.235]:a.box((x,-.002,.009),(.0015,.001,.012),'black')
    return finish(a)

def spirit_level():
    a=asset('spirit_level')
    # Open I-section beam with separate vial windows.
    for z in [.006,.05]:a.box((0,0,z),(.60,.028,.010),'metal')
    for x,w in [(-.252,.088),(-.131,.114),(.131,.114),(.252,.088)]:a.box((x,0,.028),(w,.008,.038),'teal')
    for x in [-.295,.295]:a.box((x,0,.028),(.018,.036,.064),'rubber')
    for x in [-.185,0,.185]:
        a.box((x,0,.028),(.046,.012,.012),'glass',rot=(0,0 if x==0 else (math.pi/2 if x<0 else math.pi/4),0))
        for dx in [-.012,.012]:a.box((x+dx,-.007,.026),(.002,.002,.012),'black')
        a.box((x-.004,-.007,.026),(.008,.002,.008),'light')
    return finish(a)

def chalk_line_reel():
    a=asset('chalk_line_reel')
    poly(a,[(-.027,.012),(.027,.012),(.042,.052),(.032,.094),(0,.115),(-.032,.094),(-.042,.052)],.031,'brick')
    a.cylinder((0,-.019,.053),(0,-.023,.053),.027,'dark_metal',10)
    a.beam((0,-.027,.053),(.024,-.027,.072),.009,.006,'steel')
    a.cylinder((.025,-.027,.073),(.025,-.040,.073),.009,'rubber',8)
    a.cylinder((0,0,.109),(0,0,.127),.009,'metal',8)
    a.cylinder((0,0,.126),(0,0,.26),.0012,'white',4)
    a.box((0,0,.257),(.014,.003,.014),'steel')
    a.box((.008,0,.252),(.004,.017,.005),'steel')
    return finish(a)

def plumb_bob():
    a=asset('plumb_bob')
    a.cone((0,0,.052),(0,0,0),.024,'gold',8)
    a.cylinder((0,0,.052),(0,0,.084),.024,'gold',8,radius2=.015)
    a.cylinder((0,0,.083),(0,0,.096),.009,'steel',8)
    a.cylinder((0,0,.095),(0,0,.259),.001,'white',4)
    a.cylinder((-.032,0,.267),(.032,0,.267),.011,'wood',8)
    a.cylinder((-.025,0,.267),(-.020,0,.267),.018,'wood_dark',8)
    a.cylinder((.020,0,.267),(.025,0,.267),.018,'wood_dark',8)
    a.cylinder((-.018,0,.267),(.018,0,.267),.012,'white',8)
    return finish(a)

# Saws, planes and finishing tools --------------------------------------------
def handsaw():
    a=asset('handsaw')
    poly(a,[(-.23,.014),(.17,.014),(.191,.099),(-.23,.055)],.002,'steel')
    tooth_strip(a,-.229,.170,.014,.020,.002,.009)
    # Hollow pistol grip assembled from four shaped strips.
    poly(a,[(.157,.074),(.176,.04),(.211,.018),(.222,.03),(.186,.063),(.178,.089)],.025,'wood')
    poly(a,[(.211,.018),(.249,.02),(.27,.089),(.254,.098),(.235,.04),(.217,.038)],.025,'wood')
    poly(a,[(.178,.084),(.254,.084),(.259,.11),(.183,.117)],.025,'wood')
    bolt(a,.178,.092,.005,.029);bolt(a,.226,.101,.005,.029)
    return finish(a)

def hacksaw():
    a=asset('hacksaw')
    a.tube([(-.18,0,.031),(-.18,0,.125),(-.162,0,.145),(.144,0,.145),(.167,0,.11),(.168,0,.028)],.009,'metal',6)
    a.box((-.006,0,.03),(.357,.0015,.014),'steel')
    tooth_strip(a,-.179,.167,.023,.028,.0015,.004)
    poly(a,[(.156,.089),(.181,.090),(.223,.033),(.21,.005),(.19,.018),(.15,.069)],.025,'rubber')
    a.cylinder((-.182,-.015,.031),(-.182,.015,.031),.010,'steel',6)
    a.cylinder((.17,-.016,.031),(.17,.016,.031),.007,'steel',6)
    a.box((-.193,0,.028),(.018,.041,.006),'dark_metal')
    return finish(a)

def coping_saw():
    a=asset('coping_saw')
    a.tube([(-.075,0,.018),(-.103,0,.05),(-.105,0,.155),(-.084,0,.181),(.088,0,.181),(.108,0,.159),(.107,0,.052),(.08,0,.02)],.005,'steel',6)
    a.box((0,0,.02),(.16,.0012,.005),'dark_metal')
    a.cylinder((.072,0,.02),(.129,0,.02),.004,'steel',6)
    a.cylinder((.122,0,.02),(.231,0,.02),.019,'wood',8,radius2=.012)
    a.cylinder((.12,0,.02),(.135,0,.02),.013,'metal',8)
    a.cylinder((-.080,-.009,.02),(-.080,.009,.02),.009,'metal',6)
    return finish(a)

def hand_plane():
    a=asset('hand_plane')
    a.box((0,0,.006),(.25,.057,.012),'steel')
    for y in [-.027,.027]:poly(a,[(-.115,.009),(.121,.009),(.105,.038),(-.101,.038)],.009,'dark_metal',y)
    a.box((-.03,0,.057),(.032,.043,.073),'metal',rot=(0,-.52,0))
    a.box((-.043,0,.078),(.012,.031,.05),'steel',rot=(0,-.52,0))
    a.cylinder((-.091,0,.026),(-.091,0,.070),.017,'wood',8,radius2=.022)
    a.sphere((-.091,0,.074),(.023,.023,.013),'wood',8,3)
    poly(a,[(.044,.018),(.067,.018),(.080,.070),(.074,.089),(.061,.071)],.021,'wood')
    poly(a,[(.074,.080),(.085,.085),(.103,.110),(.093,.121),(.071,.116),(.057,.098)],.023,'wood')
    poly(a,[(.044,.018),(.042,.070),(.057,.103),(.069,.104),(.055,.069),(.056,.02)],.021,'wood')
    a.cylinder((.002,0,.048),(.025,0,.064),.013,'gold',8)
    a.box((-.02,0,.112),(.008,.032,.008),'dark_metal')
    return finish(a)

def wood_rasp():
    a=asset('wood_rasp')
    a.cylinder((0,0,.01),(0,0,.113),.019,'wood',8,radius2=.013)
    a.cylinder((0,0,.105),(0,0,.121),.014,'metal',8)
    poly(a,[(-.012,.119),(.012,.119),(.014,.307),(0,.335),(-.014,.307)],.008,'metal')
    for i in range(10):
        for x in (-.007,.005):
            z=.138+i*.017+(0.006 if x>0 else 0)
            poly(a,[(x-.003,z),(x+.003,z),(x+.001,z+.006)],.003,'steel',-.006)
    return finish(a)

def masonry_trowel():
    a=asset('masonry_trowel')
    # Rhomboid broad blade lies horizontally; raised bent shank and wood grip.
    a.prism([(-.07,-.047),(.067,-.06),(.164,0),(.067,.06),(-.07,.047)],0,.004,'steel')
    a.tube([(-.043,0,.004),(-.043,0,.045),(-.012,0,.071),(-.025,0,.096)],.006,'dark_metal',6)
    a.cylinder((-.026,0,.096),(-.143,0,.096),.020,'wood',8,radius2=.015)
    a.cylinder((-.03,0,.096),(-.047,0,.096),.017,'metal',8)
    return finish(a)

def pointing_trowel():
    a=asset('pointing_trowel')
    a.prism([(-.054,-.03),(.132,0),(-.054,.03)],0,.0025,'steel')
    a.tube([(-.018,0,.003),(-.041,0,.036),(-.041,0,.063)],.005,'metal',6)
    a.cylinder((-.023,0,.071),(-.124,0,.071),.016,'rubber',8,radius2=.013)
    a.cylinder((-.021,0,.071),(-.041,0,.071),.012,'teal',8)
    a.box((-.083,0,.087),(.055,.010,.004),'teal')
    return finish(a)

def plastering_float():
    a=asset('plastering_float')
    a.box((0,0,.009),(.285,.123,.018),'wood_light')
    a.box((0,0,.002),(.29,.127,.004),'rubber')
    for x in [-.06,.06]:a.beam((x,0,.018),(x,0,.052),.018,.024,'dark_metal')
    a.cylinder((-.083,0,.055),(.083,0,.055),.018,'wood',8)
    for x in [-.11,.11]:a.cylinder((x,0,.017),(x,0,.02),.006,'metal',6)
    return finish(a)

def caulking_gun():
    a=asset('caulking_gun')
    # Cartridge barrel, open frame rails, toothed plunger rod and squeeze trigger.
    a.cylinder((-.123,0,.105),(.09,0,.105),.025,'cream',10)
    for y in [-.029,.029]:a.box((-.014,y,.10),(.246,.007,.018),'brick')
    ring(a,(-.129,0,.105),.031,.023,.014,'brick',8,'x')
    ring(a,(.102,0,.105),.031,.021,.014,'brick',8,'x')
    a.cone((.104,0,.105),(.184,0,.105),.017,'white',8)
    a.cylinder((-.232,0,.105),(-.123,0,.105),.004,'steel',6)
    a.tube([(-.232,0,.105),(-.25,0,.11),(-.261,0,.099),(-.253,0,.085)],.004,'steel',6)
    poly(a,[(-.136,.095),(-.101,.079),(-.122,.008),(-.15,.008),(-.144,.055)],.024,'brick')
    poly(a,[(-.099,.077),(-.075,.068),(-.088,.026),(-.107,.019),(-.097,.06)],.012,'steel')
    bolt(a,-.113,.077,.006,.03)
    return finish(a)

def rivet_gun():
    a=asset('rivet_gun')
    poly(a,[(-.021,.077),(.034,.076),(.047,.142),(.034,.177),(-.021,.177)],.029,'metal')
    a.cylinder((-.021,0,.162),(-.062,0,.162),.008,'steel',8)
    a.cylinder((-.064,0,.162),(-.071,0,.162),.005,'dark_metal',6)
    a.beam((-.013,0,.105),(-.039,0,.008),.016,.016,'metal');grip(a,(-.039,0,.010),(-.021,0,.083),.017,'navy',6)
    a.beam((.014,0,.112),(.061,0,.012),.014,.014,'steel');grip(a,(.061,0,.012),(.032,0,.076),.017,'rubber',6)
    a.beam((.02,0,.12),(.045,0,.064),.020,.017,'steel')
    bolt(a,.008,.125,.009,.037)
    for x,z in [(-.01,.154),(.025,.154),(.018,.086)]:bolt(a,x,z,.004,.032)
    return finish(a)

# Portable power tools -------------------------------------------------------
def drill_body(a, short=False, hammer=False):
    # Motor points along +X; batteries low, anatomically tilted pistol grip.
    z=.235 if not hammer else .25
    length=.127 if short else .184
    a.cylinder((-length/2,0,z),(length/2,0,z),.044,'teal',10,radius2=.034)
    a.cylinder((-length/2-.010,0,z),(-length/2+.011,0,z),.043,'rubber',10)
    poly(a,[(-.054,.059),(.007,.059),(.036,.194),(-.007,.218),(-.028,.166)],.049,'teal')
    poly(a,[(-.046,.074),(-.013,.074),(.007,.158),(-.023,.18)],.053,'rubber')
    poly(a,[(-.081,.01),(-.073,.005),(.026,.005),(.031,.014),(.031,.050),(.022,.059),(-.075,.059),(-.081,.051)],.079,'rubber')
    a.box((-.025,0,.060),(.089,.071,.011),'dark_metal')
    a.box((.022,-.003,.179),(.022,.048,.023),'black')
    a.box((-.041,-.042,.034),(.054,.004,.017),'teal')
    for x in [-length*.36,-length*.24,-length*.12]:a.box((x,-.041,z+.001),(.006,.007,.027),'black')
    for y in (-.04,.04):a.box((.011,y,.048),(.018,.008,.015),'teal')
    a.box((-.025,.039,.067),(.045,.006,.011),'metal')
    return z,length

def cordless_drill():
    a=asset('cordless_drill');z,l=drill_body(a)
    a.cylinder((.082,0,z),(.108,0,z),.036,'dark_metal',10)
    a.cylinder((.106,0,z),(.150,0,z),.026,'rubber',10,radius2=.021)
    a.cylinder((.150,0,z),(.166,0,z),.015,'steel',8)
    a.cylinder((.165,0,z),(.228,0,z),.0038,'metal',6)
    for x in [.182,.197,.212]: a.box((x,0,z),(.01,.009,.003),'steel',rot=(.4,.5,0))
    a.box((.035,0,.279),(.035,.021,.009),'rubber')
    return finish(a)

def impact_driver():
    a=asset('impact_driver');z,l=drill_body(a,True)
    a.cylinder((.052,0,z),(.082,0,z),.033,'metal',8,radius2=.026)
    a.cylinder((.080,0,z),(.10,0,z),.018,'dark_metal',8)
    a.cylinder((.099,0,z),(.124,0,z),.010,'steel',8)
    a.cylinder((.12,0,z),(.172,0,z),.0045,'dark_metal',6)
    a.cone((.172,0,z),(.182,0,z),.0045,'steel',6)
    for y in [-.023,.023]:a.box((.083,y,z),(.006,.009,.009),'light')
    a.box((-.073,-.045,.076),(.025,.008,.044),'steel')
    return finish(a)

def angle_grinder():
    a=asset('angle_grinder')
    a.cylinder((-.126,0,.095),(.051,0,.095),.034,'teal',10,radius2=.041)
    a.cylinder((-.160,0,.095),(-.119,0,.095),.033,'rubber',8,radius2=.029)
    a.box((-.032,0,.13),(.045,.022,.012),'black')
    a.box((.076,0,.086),(.064,.067,.045),'metal')
    a.cylinder((.085,0,.066),(.085,0,.038),.013,'steel',8)
    a.cylinder((.085,0,.028),(.085,0,.033),.065,'dark_metal',16)
    a.cylinder((.085,0,.023),(.085,0,.034),.016,'steel',8)
    # Half-disc guard with real open front.
    arc=[(.085+.074*math.cos(t),.074*math.sin(t)) for t in [math.pi/2+i*math.pi/8 for i in range(9)]]
    for p,q in zip(arc,arc[1:]):a.beam((p[0],p[1],.036),(q[0],q[1],.036),.006,.022,'black')
    a.cylinder((.044,.018,.096),(.044,.061,.096),.009,'steel',6)
    grip(a,(.044,.056,.096),(.044,.152,.096),.018)
    for x in [-.13,-.117,-.104]:a.box((x,-.031,.09),(.006,.005,.027),'black')
    a.tube([(-.159,0,.095),(-.183,0,.082),(-.18,-.025,.056)],.005,'rubber',6)
    return finish(a)

def circular_saw():
    a=asset('circular_saw')
    a.box((0,.031,.018),(.279,.085,.009),'steel')
    a.box((0,-.065,.018),(.279,.017,.009),'steel')
    for x in (-.132,.132):a.box((x,-.032,.018),(.015,.055,.009),'steel')
    teeth=[]
    for i in range(16):
        t=2*math.pi*i/16
        teeth.extend([(.021+.087*math.cos(t),.115+.087*math.sin(t)),(.021+.095*math.cos(t+.10),.115+.095*math.sin(t+.10))])
    poly(a,teeth,.004,'metal',-.042)
    a.cylinder((.021,-.052,.115),(.021,-.04,.115),.015,'dark_metal',8)
    poly(a,[(-.079,.116),(-.072,.173),(-.028,.211),(.034,.219),(.095,.192),(.121,.14),(.123,.118)],.036,'teal',-.020)
    a.cylinder((.01,.009,.112),(.01,.095,.112),.047,'teal',10)
    a.cylinder((.01,.085,.112),(.01,.102,.112),.039,'rubber',10)
    # Arch handle built around its open center.
    a.beam((-.099,.045,.075),(-.095,.045,.201),.027,.030,'rubber')
    a.beam((-.093,.045,.20),(.001,.045,.243),.027,.031,'rubber')
    a.beam((.001,.045,.24),(.063,.045,.191),.025,.029,'teal')
    a.box((-.056,.045,.205),(.026,.033,.014),'black')
    a.box((.10,.057,.038),(.027,.026,.033),'metal')
    return finish(a)

def jigsaw():
    a=asset('jigsaw')
    for y in (-.030,.030):a.box((.01,y,.007),(.175,.014,.012),'steel')
    a.box((-.056,0,.007),(.043,.047,.012),'steel')
    a.box((.079,0,.007),(.025,.047,.012),'steel')
    poly(a,[(-.063,.046),(.053,.046),(.064,.148),(.049,.182),(-.041,.185),(-.070,.15)],.068,'teal')
    a.box((.019,0,.040),(.012,.046,.036),'metal')
    poly(a,[(.015,-.032),(.022,-.032),(.024,-.021),(.02,-.016),(.024,-.009),(.02,-.004),(.024,.003),(.02,.008),(.023,.016),(.023,.048),(.015,.048)],.002,'steel')
    a.cylinder((.006,-.011,.026),(.006,.011,.026),.008,'dark_metal',6)
    for s in [-1,1]:a.cylinder((.035,s*.024,.024),(.044,s*.024,.077),.003,'steel',6)
    a.beam((-.064,0,.157),(-.075,0,.233),.029,.036,'rubber')
    a.beam((-.075,0,.233),(.034,0,.23),.029,.036,'rubber')
    a.beam((.034,0,.231),(.054,0,.176),.028,.036,'teal')
    a.box((.008,0,.214),(.027,.031,.010),'black')
    for z in [.108,.12,.132,.144]:a.box((-.034,-.035,z),(.04,.005,.004),'black')
    a.cylinder((-.087,0,.092),(-.060,0,.092),.017,'rubber',8)
    return finish(a)

def reciprocating_saw():
    a=asset('reciprocating_saw')
    poly(a,[(-.14,.10),(.115,.10),(.153,.128),(.146,.183),(.076,.202),(-.11,.189)],.063,'teal')
    a.box((.13,0,.150),(.078,.069,.076),'rubber')
    a.box((.181,0,.149),(.012,.082,.092),'steel')
    poly(a,[(.172,.145),(.38,.137),(.415,.147),(.397,.168),(.177,.170)],.0025,'steel')
    tooth_strip(a,.194,.39,.140,.022,.0025,.006)
    # Rear D grip with battery under it.
    a.beam((-.117,0,.177),(-.192,0,.166),.03,.039,'rubber')
    a.beam((-.192,0,.166),(-.192,0,.064),.03,.039,'rubber')
    a.beam((-.192,0,.064),(-.105,0,.1),.03,.039,'teal')
    a.box((-.168,0,.043),(.099,.08,.049),'rubber')
    a.box((-.175,0,.135),(.01,.034,.037),'black')
    for x in [-.084,-.066,-.048]:a.box((x,-.034,.145),(.007,.005,.038),'black')
    return finish(a)

def rotary_hammer():
    a=asset('rotary_hammer')
    a.cylinder((-.101,0,.173),(.087,0,.173),.046,'teal',10)
    a.cylinder((.074,0,.173),(.129,0,.173),.034,'rubber',10)
    a.cylinder((.129,0,.173),(.148,0,.173),.023,'metal',8)
    a.cylinder((.144,0,.173),(.32,0,.173),.007,'steel',6)
    for x in [.21,.239,.268,.298]:a.box((x,0,.173),(.015,.018,.006),'metal',rot=(.6,.45,0))
    a.box((-.021,0,.112),(.123,.075,.08),'teal')
    a.beam((-.117,0,.178),(-.162,0,.167),.033,.04,'rubber')
    a.beam((-.162,0,.167),(-.161,0,.048),.035,.04,'rubber')
    a.beam((-.161,0,.048),(-.063,0,.085),.028,.035,'teal')
    a.box((-.142,0,.128),(.012,.039,.035),'black')
    a.cylinder((.06,0,.17),(.06,-.066,.17),.013,'metal',8)
    grip(a,(.06,-.061,.17),(.06,-.159,.17),.022)
    a.cylinder((.05,-.049,.214),(.308,-.049,.214),.0035,'steel',6)
    a.cylinder((-.034,-.04,.117),(-.034,-.046,.117),.019,'black',8)
    return finish(a)

def orbital_sander():
    a=asset('orbital_sander')
    a.cylinder((0,0,.004),(0,0,.017),.063,'rubber',12)
    a.cylinder((0,0,.017),(0,0,.039),.058,'dark_metal',12,radius2=.048)
    a.cylinder((0,0,.039),(0,0,.112),.044,'teal',10,radius2=.039)
    a.sphere((-.002,0,.117),(.059,.047,.026),'rubber',10,3)
    a.box((.037,0,.12),(.024,.025,.013),'teal')
    a.cylinder((-.042,0,.054),(-.076,0,.054),.016,'dark_metal',8)
    a.box((-.12,0,.057),(.108,.05,.044),'navy')
    a.box((-.165,0,.057),(.008,.048,.039),'rubber')
    for x in [-.026,-.012,.002,.016,.03]:a.box((x,-.041,.068),(.006,.005,.022),'black')
    return finish(a)

def heat_gun():
    a=asset('heat_gun')
    a.cylinder((-.072,0,.208),(.087,0,.208),.045,'navy',10,radius2=.032)
    a.cylinder((.081,0,.208),(.145,0,.208),.027,'metal',10,radius2=.024)
    ring(a,(.147,0,.208),.025,.019,.012,'steel',10,'x')
    a.cylinder((.127,0,.208),(.14,0,.208),.018,'black',10)
    poly(a,[(-.031,.015),(.008,.015),(.039,.167),(-.003,.192),(-.014,.143)],.043,'navy')
    poly(a,[(-.029,.031),(-.002,.031),(.015,.12),(-.012,.15)],.047,'rubber')
    a.box((.019,0,.126),(.014,.043,.03),'black')
    a.box((-.016,0,.012),(.085,.052,.017),'rubber')
    a.cylinder((-.085,0,.208),(-.069,0,.208),.041,'rubber',10)
    for z in [.19,.202,.214,.226]:a.box((-.06,-.041,z),(.036,.005,.003),'black')
    a.tube([(-.031,0,.013),(-.059,0,.003),(-.074,-.014,.021)],.004,'rubber',6)
    return finish(a)

def pruning_secateurs():
    a=asset('pruning_secateurs')
    for s in [-1,1]:
        poly(a,[(s*x,z) for x,z in ([(.029,.007),(.045,.014),(.039,.068),(.016,.116),(-.002,.1),(.023,.057)] if s==1 else reversed([(.029,.007),(.045,.014),(.039,.068),(.016,.116),(-.002,.1),(.023,.057)]))],.019,'brick' if s==1 else 'rubber')
    poly(a,[(-.009,.099),(.017,.118),(.028,.151),(.017,.183),(-.012,.196),(-.008,.176),(.007,.154),(.001,.134),(-.02,.12)],.007,'steel',-.005)
    poly(a,[(-.014,.107),(-.034,.142),(-.033,.171),(-.012,.193),(-.021,.164),(-.017,.145),(.009,.123)],.009,'dark_metal',.006)
    bolt(a,0,.12,.011,.028)
    a.tube([(-.021,0,.078),(-.012,0,.061),(.002,0,.059),(.017,0,.076)],.0025,'steel',4)
    a.box((.014,-.014,.103),(.025,.005,.007),'steel',rot=(0,.3,0))
    return finish(a)

FACTORIES = [claw_hammer, ball_peen_hammer, rubber_mallet, club_hammer, hatchet,
    cold_chisel, masonry_bolster, crowbar, flat_nail_pull_bar, adjustable_wrench,
    combination_wrench, pipe_wrench, socket_ratchet, torque_wrench, hex_key,
    folding_hex_key_set, bolt_cutters, combination_pliers, needle_nose_pliers,
    locking_pliers, wire_stripper, aviation_snips, flat_screwdriver,
    stubby_phillips_screwdriver, utility_knife, retractable_tape_measure,
    carpenters_square, spirit_level, chalk_line_reel, plumb_bob, handsaw, hacksaw,
    coping_saw, hand_plane, wood_rasp, masonry_trowel, pointing_trowel,
    plastering_float, caulking_gun, rivet_gun, cordless_drill, impact_driver,
    angle_grinder, circular_saw, jigsaw, reciprocating_saw, rotary_hammer,
    orbital_sander, heat_gun, pruning_secateurs]
assert len(FACTORIES) == 50
for factory in FACTORIES:
    register('b06_' + factory.__name__, CAT, 'handheld', factory)
