"""Fifty original handheld food, beverage, packaging and sidewalk litter props.
Metres; muted, readable, logo-free forms with measured handheld export budgets.
"""
import math
from assetlib import Asset, register


def item(slug):
    def decorate(fn):
        def factory():
            a = Asset('b16_' + slug, 'food_drinks_packaging_litter', 'handheld')
            fn(a)
            return a.bottom_center()
        register('b16_' + slug, 'food_drinks_packaging_litter', 'handheld', factory)
        return factory
    return decorate


def box(a,p,s,m='paper',rot=None):
    a.box(p,s,m,rot=rot)


def rod(a,p,q,r,m='paper',n=8,r2=None):
    a.cylinder(p,q,r,m,sides=n,radius2=r2)


def disk(a,z,r,h=.004,m='paper',n=10,x=0,y=0):
    rod(a,(x,y,z-h/2),(x,y,z+h/2),r,m,n)


def lathe(a,profile,m='paper',n=10):
    vs=[(r*math.cos(i*math.tau/n),r*math.sin(i*math.tau/n),z) for r,z in profile for i in range(n)]
    fs=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(profile)-1) for i in range(n)]
    fs += [tuple(reversed(range(n))),tuple(range((len(profile)-1)*n,len(profile)*n))]
    a.mesh(vs,fs,m)


def ring(a,p,r,t,m='paper',axis='z',n=10):
    a.torus(p,r,t,m,axis=axis,segments=n,sides=4)


def ball(a,p,s,m='cream',n=8,rings=3):
    a.sphere(p,1,m,segments=max(9,n),rings=max(4,rings),scale=s)


def _rect(w,d,c=.09):
    x=w/2;y=d/2;k=min(w,d)*c
    return [(-x+k,-y),(x-k,-y),(x,-y+k),(x,y-k),(x-k,y),(-x+k,y),(-x,y-k),(-x,-y+k)]

def taperbox(a,z,h,w0,d0,w1,d1,m='paper'):
    # Eight-sided carton section: four folded corner returns, not a cuboid.
    vs=[(x,y,zz) for w,d,zz in ((w0,d0,z),(w1,d1,z+h)) for x,y in _rect(w,d)]
    a.mesh(vs,[tuple(reversed(range(8))),tuple(range(8,16))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)],m)

def tray(a,w,d,h,m='paper'):
    # Folded food boat with sloping walls, clipped corners, and an open cavity.
    rings=[[(x,y,z) for x,y in _rect(ww,dd,.13)] for ww,dd,z in
           ((w*.81,d*.74,0),(w,d,h),(w-.004,d-.004,h),(w*.81-.004,d*.74-.004,.003))]
    vs=[p for ring in rings for p in ring];fs=[]
    for j in range(3):fs += [(j*8+i,j*8+(i+1)%8,(j+1)*8+(i+1)%8,(j+1)*8+i) for i in range(8)]
    fs += [tuple(reversed(range(8))),tuple(range(24,32))]
    a.mesh(vs,fs,m)

def _pouch_depth(t,d):
    rows=((0,.06),(.12,.32),(.45,.50),(.78,.43),(1,.06))
    for (t0,d0),(t1,d1) in zip(rows,rows[1:]):
        if t<=t1:return d*(d0+(d1-d0)*(t-t0)/(t1-t0))
    return d*.06

def pouch(a,w,h,d,m='paper'):
    # A rounded gusseted packet with a broad pillow face and flat heat seals.
    vs=[]
    for t,scale in ((0,.92),(.12,1.01),(.45,1.06),(.78,1.01),(1,.92)):
        half=_pouch_depth(t,d);xx=w*scale/2
        plan=[(-xx*.80,-half),(xx*.80,-half),(xx,-half*.53),(xx,half*.53),
              (xx*.8,half),(-xx*.8,half),(-xx,half*.53),(-xx,-half*.53)]
        vs += [(x,y,h*t) for x,y in plan]
    fs=[tuple(reversed(range(8))),tuple(range(32,40))]
    fs += [(j*8+i,j*8+(i+1)%8,(j+1)*8+(i+1)%8,(j+1)*8+i) for j in range(4) for i in range(8)]
    a.mesh(vs,fs,m)
    for zz in (.003,h-.003):box(a,(0,0,zz),(w*.92,.009,.006),m)
    for j in range(5):
        xx=(j-2)*w*.15
        box(a,(xx,-d*.06-.0006,.005),(.001,.001,.007),m)

def pouch_label(a,w,h,d,z0,z1,mat):
    ts=sorted(set([z0,z1]+[t for t in (.12,.45,.78) if z0<t<z1]))
    vs=[(x,-_pouch_depth(t,d)-.0006,h*t) for t in ts for x in (-w*.38,w*.38)]
    a.mesh(vs,[(j*2,j*2+1,j*2+3,j*2+2) for j in range(len(ts)-1)],mat)

def sweep(a,points,r,mat='wood_light',sides=6):
    # Continuous tube avoids the conspicuous cylinder caps at bread bends.
    vs=[]
    for j,p in enumerate(points):
        prev=points[max(0,j-1)];nxt=points[min(len(points)-1,j+1)]
        dx=nxt[0]-prev[0];dy=nxt[1]-prev[1];le=max(math.hypot(dx,dy),1e-9)
        for i in range(sides):
            th=i*math.tau/sides
            vs.append((p[0]-dy/le*r*math.cos(th),p[1]+dx/le*r*math.cos(th),p[2]+r*math.sin(th)))
    fs=[tuple(reversed(range(sides))),tuple(range((len(points)-1)*sides,len(points)*sides))]
    fs += [(j*sides+i,j*sides+(i+1)%sides,(j+1)*sides+(i+1)%sides,(j+1)*sides+i) for j in range(len(points)-1) for i in range(sides)]
    a.mesh(vs,fs,mat)

def _folded_sheet(a,w,d,mat='paper',crumple=False):
    n=6;vs=[]
    for j in range(n):
        for i in range(n):
            x=(i/(n-1)-.5)*w;y=(j/(n-1)-.5)*d
            wave=math.sin(i*1.7+j*.93)
            z=.004+abs(wave)*(.013 if not crumple else .024)+.007*math.sin(j*2.1-i*.6)
            if crumple:
                x+=.012*math.sin(j*1.3+i*.4);y+=.009*math.cos(i*1.8+j*.5)
            vs.append((x,y,z))
    fs=[]
    for j in range(n-1):
        for i in range(n-1):
            q=j*n+i;fs += [(q,q+1,q+n+1),(q,q+n+1,q+n)]
    a.mesh(vs+[(x,y,z-.0007) for x,y,z in vs],fs+[tuple(k+n*n for k in reversed(f)) for f in fs],mat)

def strokes(a,x,y,z,width=.05,lines=3,m='concrete'):
    for i in range(lines): box(a,(x,y+i*.009,z),(width*(1-.11*i),.0025,.0008),m)


@item('takeaway_coffee_cup')
def coffee(a):
    lathe(a,[(.028,0),(.030,.010),(.043,.105)],'paper')
    lathe(a,[(.034,.037),(.040,.075)],'wood_light')
    lathe(a,[(.043,.104),(.046,.108),(.046,.114),(.039,.117),(.036,.124)],'white')
    box(a,(0,-.025,.125),(.019,.009,.002),'dark_metal')


@item('fountain_drink_with_straw')
def fountain(a):
    lathe(a,[(.035,0),(.049,.150)],'white')
    lathe(a,[(.041,.059),(.045,.112)],'red')
    disk(a,.152,.052,.006,'white')
    rod(a,(0,0,.15),(.011,0,.225),.003,'cream',6)
    rod(a,(.011,0,.225),(.030,0,.239),.003,'cream',6)


@item('aluminum_soda_can')
def can(a):
    lathe(a,[(.026,0),(.030,.003),(.033,.011),(.033,.105),(.031,.115),(.028,.120)],'red',12)
    disk(a,.122,.029,.004,'silver',12)
    disk(a,.003,.029,.004,'silver',12)
    box(a,(0,.008,.125),(.013,.022,.002),'dark_metal')
    ring(a,(0,-.005,.128),.008,.002,'silver',n=8)


@item('crushed_soda_can')
def crushed(a):
    n=12;vs=[]
    # Intact rolled end rims contrast with strongly dented, twisted side walls.
    for j,(r,z) in enumerate(((.028,0),(.031,.010),(.022,.027),(.032,.042),(.027,.057),(.028,.063))):
        for i in range(n):
            t=i*math.tau/n;dent=(.78+.20*math.sin(t*3+j*.9)) if j in (2,3) else 1
            vs.append((r*dent*math.cos(t)+(.004 if j==3 else 0),r*dent*math.sin(t),z+(.004*math.cos(t) if j>3 else .002*math.sin(t*2+j))))
    fs=[tuple(reversed(range(n))),tuple(range(5*n,6*n))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(5) for i in range(n)]
    a.mesh(vs,fs,['silver','silver']+['blue']*(5*n))
    lid=Asset('rolled rim');ring(lid,(0,0,0),.028,.0015,'silver',n=12)
    ring(lid,(0,-.004,.002),.007,.0017,'silver',n=8)
    box(lid,(0,.010,.001),(.011,.012,.001),'dark_metal')
    lid.rotate((0,-.14,0)).translate((0,0,.064));a.mesh(lid.vertices,lid.faces,lid.face_materials)


@item('ribbed_water_bottle')
def water(a):
    lathe(a,[(.025,0),(.030,.006),(.032,.018),(.033,.023),(.033,.027),(.031,.031),(.031,.040),(.033,.044),(.033,.048),(.031,.052),(.032,.104),(.034,.114),(.032,.120),(.026,.139),(.016,.151),(.012,.157),(.012,.167)],'glass',10)
    lathe(a,[(.033,.055),(.033,.096)],'paper')
    lathe(a,[(.013,.162),(.014,.180)],'blue')


@item('longneck_glass_bottle')
def glass_bottle(a):
    lathe(a,[(.027,0),(.030,.006),(.031,.016),(.031,.117),(.029,.131),(.024,.143),(.016,.159),(.012,.179),(.012,.213),(.015,.216),(.015,.221)],'green',10)
    lathe(a,[(.032,.041),(.032,.099)],'cream')
    disk(a,.222,.015,.009,'gold')
    box(a,(0,-.0325,.070),(.023,.001,.025),'wood_dark')


@item('square_juice_bottle')
def juice_bottle(a):
    taperbox(a,0,.118,.061,.048,.065,.052,'orange')
    taperbox(a,.118,.030,.065,.052,.025,.023,'orange')
    rod(a,(0,0,.148),(0,0,.169),.014,'white',8)
    box(a,(0,-.027,.069),(.052,.002,.057),'cream')
    box(a,(0,-.0285,.069),(.019,.001,.023),'foliage_dark')


@item('gable_top_milk_carton')
def milk(a):
    box(a,(0,0,.088),(.071,.071,.176),'white')
    a.mesh([(-.0355,-.0355,.176),(.0355,-.0355,.176),(.0355,.0355,.176),(-.0355,.0355,.176),(-.0355,0,.213),(.0355,0,.213)],[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4),(3,2,1,0)],'paper')
    box(a,(0,0,.219),(.071,.006,.012),'white')
    box(a,(0,-.0365,.075),(.061,.002,.070),'blue')
    rod(a,(.018,-.017,.197),(.018,-.023,.203),.010,'white',8)


@item('juice_box_with_straw')
def juice_box(a):
    box(a,(0,0,.053),(.060,.039,.106),'cream')
    box(a,(0,-.0205,.053),(.050,.002,.080),'orange')
    box(a,(0,0,.109),(.061,.040,.006),'paper')
    rod(a,(.017,.006,.112),(.017,.006,.151),.0022,'white',6)
    rod(a,(.017,.006,.151),(.005,.006,.165),.0022,'white',6)
    box(a,(-.013,-.022,.060),(.013,.001,.029),'green')


@item('foil_drink_pouch')
def drink_pouch(a):
    pouch(a,.089,.145,.035,'silver')
    pouch_label(a,.089,.145,.035,.33,.75,'teal')
    rod(a,(.021,0,.143),(.030,0,.191),.0025,'orange',6)


@item('closed_pizza_box')
def pizza_box(a):
    box(a,(0,0,.024),(.35,.35,.048),'cream')
    box(a,(0,0,.050),(.354,.354,.005),'paper')
    box(a,(0,-.179,.043),(.065,.005,.020),'wood_light')
    for x in (-.11,.11): box(a,(x,-.176,.025),(.025,.001,.006),'brown')
    box(a,(0,0,.053),(.17,.022,.001),'brick',rot=.35)


@item('pizza_slice_in_triangle_tray')
def pizza_slice(a):
    pts=[(-.085,.115),(.085,.115),(0,-.14)]
    a.prism(pts,0,.004,'paper')
    a.prism([(-.075,.099),(.075,.099),(0,-.126)],.005,.013,'cream')
    a.prism([(-.067,.082),(.067,.082),(0,-.118)],.013,.019,'yellow')
    rod(a,(-.074,.098,.019),(.074,.098,.019),.010,'wood_light',8)
    for x,y in [(-.030,.058),(.030,.058),(0,.010),(0,-.055)]: disk(a,.021,.014,.003,'brick',8,x,y)


@item('burger_clamshell')
def burger_box(a):
    taperbox(a,0,.035,.100,.100,.120,.120,'cream')
    box(a,(0,0,.037),(.126,.126,.005),'paper')
    taperbox(a,.040,.050,.120,.120,.093,.093,'cream')
    box(a,(0,-.064,.039),(.025,.008,.012),'paper')
    box(a,(0,.061,.041),(.071,.011,.014),'wood_light')


@item('french_fry_carton')
def fries(a):
    taperbox(a,0,.077,.045,.031,.075,.043,'brick')
    box(a,(0,0,.079),(.069,.036,.005),'brown')
    for i,(x,y,h) in enumerate([(-.024,0,.072),(-.012,.009,.084),(0,.010,.068),(.014,.007,.080),(.024,-.004,.062),(-.015,-.010,.063),(.005,-.010,.075)]):
        box(a,(x,y,.070+h/2),(.009,.009,h),'wood_light',rot=(.035*(i%3-1),.06*(i%2),.08*(i%3-1)))
    box(a,(0,-.024,.045),(.025,.003,.018),'cream')


@item('hotdog_in_paper_boat')
def hotdog(a):
    tray(a,.195,.075,.021)
    for y in (-.018,.018):ball(a,(0,y,.038),(.089,.023,.028),'wood_light',12,4)
    b=Asset('sausage')
    lathe(b,[(.004,-.078),(.012,-.072),(.015,-.061),(.015,.061),(.012,.072),(.004,.078)],'brick',10)
    b.rotate((0,math.pi/2,0)).translate((0,0,.058));a.mesh(b.vertices,b.faces,b.face_materials)
    sweep(a,[(-.065,0,.074),(-.045,-.004,.074),(-.024,.005,.074),(-.003,-.004,.074),(.019,.004,.074),(.041,-.004,.074),(.062,0,.074)],.002,'yellow',4)


@item('street_taco_in_wrapper')
def taco(a):
    box(a,(0,0,.002),(.17,.115,.003),'paper',rot=.14)
    vs=[];nx=7;nt=7
    for k in range(2):
        for i in range(nx):
            x=-.078+.156*i/(nx-1);h=.074*math.sqrt(max(.04,1-(x/.081)**2))
            for j in range(nt):
                th=math.pi*j/(nt-1)
                vs.append((x,-(.029-k*.002)*math.cos(th),.005+h*(1-math.sin(th))+k*.0015))
    fs=[];mats=[];off=nx*nt
    for k in range(2):
        for i in range(nx-1):
            for j in range(nt-1):
                q=k*off+i*nt+j;fs.append((q,q+1,q+nt+1,q+nt));mats.append('wood_light' if k==0 else 'cream')
    for i in range(nx-1):
        for j in (0,nt-1):
            q=i*nt+j;fs.append((q,q+nt,q+nt+off,q+off));mats.append('wood_light')
    a.mesh(vs,fs,mats)
    for i in range(5):
        a.sphere((-.049+i*.024,0,.067),(.015,.017,.009),'foliage' if i%2 else 'brick',segments=7,rings=3)
    for i in range(3):box(a,(-.035+i*.031,-.004,.077),(.024,.007,.002),'yellow',rot=.25-i*.23)


@item('folded_takeout_carton')
def takeout(a):
    taperbox(a,0,.090,.065,.058,.088,.077,'paper')
    box(a,(0,-.010,.093),(.090,.057,.006),'white',rot=(.12,0,0))
    box(a,(0,.020,.095),(.088,.038,.005),'white',rot=(-.15,0,0))
    a.tube([(-.047,0,.060),(-.049,0,.144),(.049,0,.144),(.047,0,.060)],.0017,'steel',6)
    box(a,(0,-.041,.043),(.041,.002,.029),'brick')


@item('lidded_salad_bowl')
def salad(a):
    lathe(a,[(.051,0),(.078,.045),(.078,.049),(.072,.049),(.048,.007)],'black',12)
    disk(a,.046,.070,.007,'foliage',10)
    for x,y in [(-.025,0),(.026,.013),(.005,-.029)]: disk(a,.052,.012,.004,'brick',6,x,y)
    lathe(a,[(.080,.050),(.080,.056),(.061,.076)],'glass',12)


@item('lidded_soup_cup')
def soup(a):
    lathe(a,[(.043,0),(.052,.078)],'cream')
    disk(a,.080,.055,.006,'paper')
    disk(a,.085,.048,.005,'white')
    for x in (-.009,.009): disk(a,.088,.002,.001,'brown',6,x,0)
    box(a,(0,-.051,.045),(.041,.002,.024),'terracotta')


@item('ice_cream_cup_with_spoon')
def ice_cream_cup(a):
    lathe(a,[(.029,0),(.041,.050)],'paper')
    ring(a,(0,0,.051),.040,.003,'white')
    ball(a,(0,0,.055),(.036,.036,.021),'cream',12,5)
    a.beam((.019,.008,.050),(.038,.018,.126),.011,.003,'wood_light')
    ball(a,(.039,.019,.128),(.007,.003,.016),'wood_light',8,4)


@item('waffle_ice_cream_cone')
def cone(a):
    a.cone((0,0,.100),(0,0,0),.036,'wood_light',10)
    ring(a,(0,0,.099),.034,.003,'brown')
    ball(a,(0,0,.120),(.044,.044,.040),'cream',12,5)
    for z,r in [(.041,.014),(.062,.022),(.082,.029)]: ring(a,(0,0,z),r,.0015,'brown',n=10)


@item('donut_in_open_paper_bag')
def donut_bag(a):
    box(a,(0,0,.004),(.13,.12,.008),'cream')
    box(a,(0,.040,.044),(.13,.040,.080),'cream',rot=(-.13,0,0))
    for x in (-.061,.061): box(a,(x,-.018,.023),(.006,.080,.040),'paper')
    a.torus((0,-.024,.026),.031,.015,'wood_light',segments=12,sides=6)
    a.torus((0,-.024,.031),.031,.013,'brown',segments=12,sides=4)


@item('sealed_potato_chip_bag')
def chip_bag(a):
    pouch(a,.125,.202,.060,'cream')
    pouch_label(a,.125,.202,.060,.36,.69,'navy')
    ball(a,(0,-.032,.108),(.027,.004,.017),'wood_light',8,3)


@item('soft_street_pretzel')
def pretzel(a):
    box(a,(0,0,.002),(.17,.15,.003),'paper',rot=.10)
    knots=[(-.033,-.030,.022),(.003,.011,.026),(.037,.049,.019),(.057,.042,.019),(.066,.015,.019),(.049,-.035,.019),(0,-.056,.019),(-.049,-.035,.019),(-.066,.013,.019),(-.057,.044,.019),(-.035,.049,.019),(.006,.008,.017),(.035,-.030,.019)]
    points=[]
    for j in range(len(knots)-1):
        p0,p1,p2,p3=[knots[max(0,min(len(knots)-1,k))] for k in (j-1,j,j+1,j+2)]
        for t in (0,.5):
            points.append(tuple(.5*((2*p1[k])+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t*t*t) for k in range(3)))
    points.append(knots[-1]);sweep(a,points,.010,'wood_light',6)
    for x,y in [(-.054,.028),(.052,.029),(0,-.054),(-.036,-.043),(.036,-.043)]:box(a,(x,y,.029),(.004,.005,.002),'white',rot=.40)


@item('popcorn_carton')
def popcorn(a):
    taperbox(a,0,.137,.065,.056,.095,.079,'paper')
    for x in (-.030,0,.030):box(a,(x,-.040,.094),(.012,.002,.085),'brick',rot=(.07,0,0))
    for k,(x,y,z) in enumerate([(-.031,-.021,.126),(0,-.020,.132),(.031,-.020,.128),(-.023,.010,.137),(.009,.011,.136),(.032,.014,.128)]):
        n=8;vs=[]
        for j,(r,zz) in enumerate(((.007,0),(.018,.007),(.015,.021),(.005,.027))):
            for i in range(n):
                t=i*math.tau/n;rr=r*(1+.22*math.sin(3*t+k*.7+j*.45))
                vs.append((x+rr*math.cos(t),y+rr*math.sin(t),z+zz+.0025*math.cos(t*3+j)))
        a.mesh(vs,[tuple(reversed(range(n))),tuple(range(3*n,4*n))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(3) for i in range(n)],'cream')
        if k in (1,3,4):a.mesh([(x-.002,y-.002,z+.027),(x+.003,y-.001,z+.027),(x,y+.002,z+.027)],[(0,1,2)],'wood_light')


@item('paper_takeaway_bag')
def takeaway_bag(a):
    bottom=[(x,y,0) for x,y in _rect(.136,.074,.12)]
    top=[(x,y,.205+(.003 if i%3==0 else -.001)) for i,(x,y) in enumerate(_rect(.14,.08,.12))]
    inner=[(x*.977,y*.960,z-.006) for x,y,z in top]
    a.mesh(bottom+top+inner,[tuple(reversed(range(8)))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]+[(i+8,(i+1)%8+8,(i+1)%8+16,i+16) for i in range(8)],'wood_light')
    # The open top exposes the brown inner gussets instead of a solid lid.
    a.mesh(inner+[(x*.96,y*.94,.012) for x,y,z in bottom],[(i,i+8,(i+1)%8+8,(i+1)%8) for i in range(8)]+[tuple(range(8,16))],'brown')
    for y in (-.027,.027):
        pts=[(-.037,y,.198),(-.037,y,.244),(-.026,y,.266),(0,y,.271),(.026,y,.266),(.037,y,.244),(.037,y,.198)]
        a.tube(pts,.0027,'cream',sides=5)
    box(a,(0,-.0408,.113),(.074,.001,.057),'paper')
    box(a,(0,-.0417,.111),(.037,.0008,.014),'wood_dark')


@item('molded_four_cup_carrier')
def cup_carrier(a):
    box(a,(0,0,.008),(.176,.176,.016),'sand')
    for x in (-.046,.046):
        for y in (-.046,.046):
            # Four true recesses, created as open annular walls.
            b=Asset('tmp')
            lathe(b,[(.036,.013),(.041,.039),(.036,.041),(.032,.019)],'sand',8)
            b.translate((x,y,0));a.mesh(b.vertices,b.faces,b.face_materials)
    box(a,(0,0,.023),(.032,.032,.040),'sand')


@item('six_egg_carton')
def egg_carton(a):
    taperbox(a,0,.034,.139,.086,.156,.101,'sand')
    box(a,(0,0,.037),(.160,.105,.007),'cream')
    taperbox(a,.040,.028,.154,.101,.137,.084,'sand')
    for x in (-.047,0,.047):
        for y in (-.024,.024): ball(a,(x,y,.065),(.023,.022,.013),'sand',6,3)
    box(a,(0,-.053,.037),(.033,.008,.017),'cream')


@item('discarded_banana_peel')
def banana(a):
    rod(a,(0,0,.029),(0,0,.056),.009,'wood_light',8,r2=.006)
    for theta in (0,2.15,4.3):
        c,ss=math.cos(theta),math.sin(theta);vs=[]
        for zz in (0,.002):
            for x,w,z in ((0,.008,.040),(.027,.017,.017),(.056,.018,.007),(.088,.012,.011),(.110,.001,.028)):
                for t in (-1,0,1):
                    y=w*t;vs.append((x*c-y*ss,x*ss+y*c,z+zz-.003*(1-t*t)))
        fs=[];ms=[]
        for k in range(2):
            for i in range(4):
                for j in range(2):
                    q=k*15+i*3+j;fs.append((q,q+1,q+4,q+3));ms.append('yellow' if k==0 else 'cream')
        for i in range(4):
            for j in (0,2):q=i*3+j;fs.append((q,q+3,q+18,q+15));ms.append('yellow')
        a.mesh(vs,fs,ms)
    disk(a,.057,.006,.003,'brown',8)


@item('discarded_apple_core')
def apple_core(a):
    n=12;vs=[]
    profile=((.013,.002),(.024,.007),(.029,.015),(.014,.028),(.010,.041),(.017,.054),(.027,.063),(.019,.071))
    for j,(r,z) in enumerate(profile):
        for i in range(n):
            t=i*math.tau/n;rr=r*(1+.07*math.sin(t*3)+.045*math.cos(t*5+j*.6))
            vs.append((rr*math.cos(t)+.002*math.sin(j*.8),rr*math.sin(t),z+.0015*math.cos(t*3+j*.5)))
    vs += [(0,0,0),(0,0,.067)];fs=[];ms=[]
    for j in range(len(profile)-1):
        for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i));ms.append('brick' if j in (0,1,6) else 'cream')
    for i in range(n):
        fs.append((i,(i+1)%n,96));ms.append('brick')
        fs.append((84+i,84+(i+1)%n,97));ms.append('brick')
    a.mesh(vs,fs,ms)
    rod(a,(0,0,.066),(.004,.002,.091),.0025,'wood_dark',6,r2=.0018)
    for z in (.030,.043):a.sphere((.012,-.003,z),(.002,.0035,.004),'brown',segments=6,rings=3)


@item('triangular_sandwich_half')
def sandwich(a):
    outline=[(-.059,-.055),(.059,-.055),(.063,-.051),(-.060,.072),(-.065,.067),(-.065,-.049)]
    for base in (0,.037):
        n=len(outline)
        vs=[(x*sc,y*sc,base+z) for sc,z in ((.98,0),(1,.006),(.98,.014)) for x,y in outline]
        fs=[tuple(reversed(range(n))),tuple(range(2*n,3*n))]
        ms=['cream','cream']
        for j in range(2):
            for i in range(n):
                fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i));ms.append('wood_light' if i!=2 else 'cream')
        a.mesh(vs,fs,ms)
    leaves=[(-.062,-.056),(.057,-.056),(.064,-.044),(.043,-.025),(.032,-.024),(.020,-.004),(.003,.009),(-.011,.031),(-.028,.040),(-.042,.060),(-.067,.074),(-.063,.045)]
    a.prism(leaves,.017,.021,'foliage_dark')
    a.prism([(-.063,-.054),(.062,-.051),(.033,-.022),(.023,-.014),(-.022,.039),(-.062,.072)],.023,.029,'pink')
    a.prism([(-.062,-.056),(.059,-.056),(.060,-.048),(-.066,.074)],.030,.034,'yellow')
    # A second ruffled leaf peeks past the filling along the cut face.
    a.prism([(-.058,-.052),(.058,-.052),(.044,-.030),(.013,.001),(.006,.014),(-.039,.057),(-.065,.067)],.034,.037,'foliage')


@item('broken_chocolate_chip_cookie')
def cookie(a):
    outline=[(-.038,-.017),(-.018,-.036),(.011,-.039),(.038,-.019),(.039,.012),(.018,.035),(-.007,.038),(.002,.015),(-.019,.017),(-.023,.001),(-.038,.006)]
    n=len(outline);vs=[(x*sc,y*sc,z) for sc,z in ((.95,0),(1,.005),(.93,.011)) for x,y in outline]
    a.mesh(vs,[tuple(reversed(range(n))),tuple(range(2*n,3*n))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(2) for i in range(n)],'wood_light')
    for x,y in [(-.018,-.014),(.005,-.019),(.023,-.007),(.019,.017),(-.005,.025)]:
        a.sphere((x,y,.011),(.0047,.0037,.0028),'wood_dark',segments=6,rings=3)
    a.prism([(-.055,.017),(-.036,.019),(-.044,.039)],.001,.009,'wood_light')
    for x,y in [(-.035,.035),(-.026,.024),(-.050,.014)]:a.sphere((x,y,.003),(.0028,.002,.0025),'cream',segments=5,rings=3)


@item('crumpled_food_wrapper')
def food_wrapper(a):
    start=len(a.faces);_folded_sheet(a,.21,.15,'paper')
    # Printed ink belongs to the folded paper faces, never a hovering label.
    for i in (22,23,24,25):a.face_materials[start+i]='brick' 


@item('rolled_newspaper')
def rolled_news(a):
    rod(a,(-.135,0,.032),(.135,0,.032),.031,'paper',10)
    for x in (-.132,.132): ring(a,(x,0,.032),.021,.002,'concrete',axis='x')
    rod(a,(-.014,0,.032),(.014,0,.032),.032,'brown',10)
    for x in (-.093,-.065,.061,.088): box(a,(x,0,.063),(.014,.029,.001),'concrete')


@item('folded_newspaper')
def folded_news(a):
    box(a,(0,0,.004),(.215,.155,.008),'paper')
    box(a,(0,0,.009),(.212,.153,.003),'white',rot=(.008,0,.02))
    box(a,(0,.046,.012),(.185,.022,.001),'dark_metal')
    for x in (-.070,0,.070): strokes(a,x,-.054,.013,.055,7)
    box(a,(-.059,-.009,.014),(.061,.038,.001),'concrete')


@item('curled_receipt_litter')
def receipt(a):
    # Continuous six-segment curling paper strip, with thin rectangular cross-sections.
    path=[(-.092,.018),(-.070,.008),(-.032,.001),(.014,.003),(.053,.015),(.077,.036),(.079,.055)]
    vs=[(x,y,z+t) for x,z in path for y,t in [(-.029,0),(.029,0),(.029,.0008),(-.029,.0008)]]
    fs=[(3,2,1,0),tuple(range((len(path)-1)*4,len(path)*4))]
    fs += [(4*j+i,4*j+(i+1)%4,4*(j+1)+(i+1)%4,4*(j+1)+i) for j in range(len(path)-1) for i in range(4)]
    a.mesh(vs,fs,'paper')
    for x in (-.026,-.015,-.004,.007): box(a,(x,0,.005),(.002,.037,.0008),'concrete')


@item('crumpled_paper_napkin')
def napkin(a):
    _folded_sheet(a,.105,.087,'paper',True)


@item('disposable_plastic_fork')
def fork(a):
    a.prism([(-.006,-.09),(.006,-.09),(.006,.019),(.017,.030),(.017,.049),(-.017,.049),(-.017,.030),(-.006,.019)],0,.003,'white')
    for x in (-.0135,-.0045,.0045,.0135): box(a,(x,.065,.0015),(.005,.039,.003),'white')


@item('disposable_plastic_spoon')
def spoon(a):
    a.prism([(-.004,-.098),(.004,-.098),(.006,-.087),(.006,.023),(-.006,.023),(-.006,-.087)],0,.004,'cream')
    n=12;vs=[]
    for xx,yy,z in ((.023,.036,.010),(.019,.031,.006),(.008,.013,.004)):
        vs += [(xx*math.cos(i*math.tau/n),.045+yy*math.sin(i*math.tau/n),z) for i in range(n)]
    vs.append((0,.045,.004));fs=[]
    for j in range(2):fs += [(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for i in range(n)]
    fs += [(24+i,24+(i+1)%n,36) for i in range(n)]
    # Concave upper bowl and a thin closed underside, rather than overlaid blobs.
    below=[(x,y,z-.002) for x,y,z in vs];base=len(vs)
    a.mesh(vs+below,fs+[tuple(base+i for i in reversed(f)) for f in fs]+[(i,(i+1)%n,base+(i+1)%n,base+i) for i in range(n)],'cream')


@item('serrated_takeout_knife')
def knife(a):
    a.prism([(-.006,-.099),(.006,-.099),(.008,-.004),(.017,.035),(.016,.071),(.009,.082),(-.006,.077)],0,.004,'white')
    for y in (.008,.020,.032,.044,.056): a.prism([(.013,y),(.020,y+.003),(.014,y+.007)],0,.004,'white')
    for x in (-.003,.003): box(a,(x,-.054,.0045),(.001,.065,.001),'paper')


@item('chopsticks_in_paper_sleeve')
def chopsticks(a):
    box(a,(0,-.039,.006),(.037,.173,.012),'paper')
    for x in (-.008,.008): rod(a,(x,-.106,.007),(x,.128,.007),.003,'wood_light',6,r2=.002)
    box(a,(0,-.038,.0125),(.026,.054,.001),'brick')
    for y in (-.054,-.041,-.028): box(a,(0,y,.0135),(.017,.004,.001),'paper')


@item('fluted_paper_plate')
def plate(a):
    lathe(a,[(.073,0),(.091,.009),(.100,.020),(.103,.021),(.099,.024),(.087,.014),(.071,.006)],'paper',16)
    for i in range(12):
        t=i*math.tau/12
        rod(a,(.087*math.cos(t),.087*math.sin(t),.015),(.100*math.cos(t),.100*math.sin(t),.024),.0008,'cream',4)


@item('rectangular_foil_takeaway_pan')
def foil_pan(a):
    def plan(w,d):
        pts=[];r=.013
        for cx,cy,start in ((w/2-r,d/2-r,0),(-w/2+r,d/2-r,math.pi/2),(-w/2+r,-d/2+r,math.pi),(w/2-r,-d/2+r,math.pi*1.5)):
            for j in range(4):
                th=start+j*math.pi/6;pts.append((cx+r*math.cos(th),cy+r*math.sin(th)))
        return pts
    rows=[[(x,y,z) for x,y in plan(w,d)] for w,d,z in ((.171,.111,0),(.191,.134,.046),(.197,.140,.049),(.191,.134,.050),(.181,.124,.044),(.162,.102,.006))]
    n=16;vs=[p for row in rows for p in row];fs=[]
    for j in range(5):fs += [(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for i in range(n)]
    fs += [tuple(reversed(range(n))),tuple(range(5*n,6*n))]
    a.mesh(vs,fs,'silver')
    for sy in (-1,1):
        for x in (-.063,-.042,-.021,0,.021,.042,.063):
            a.beam((x,sy*.056,.009),(x,sy*.067,.044),.0022,.0013,'steel')
    for sx in (-1,1):
        for y in (-.033,0,.033):a.beam((sx*.086,y,.009),(sx*.096,y,.044),.0022,.0013,'steel')


@item('ketchup_sachet')
def ketchup(a):
    pouch(a,.038,.076,.010,'brick')
    pouch_label(a,.038,.076,.010,.28,.70,'paper')
    for x in (-.011,0,.011): box(a,(x,0,.004),(.002,.010,.006),'terracotta')


@item('torn_sugar_packet')
def sugar(a):
    # Low open sachet with a jagged mouth and sugar mound.
    a.prism([(-.042,-.022),(.035,-.022),(.041,-.012),(.035,-.005),(.042,.005),(.035,.014),(.040,.022),(-.042,.022)],0,.002,'white')
    box(a,(-.006,0,.004),(.051,.039,.004),'paper')
    box(a,(-.009,0,.0065),(.028,.017,.001),'blue')
    ball(a,(.050,.002,.004),(.023,.020,.005),'white',8,3)
    for x,y in [(.070,-.019),(.079,.010),(.058,.030)]: box(a,(x,y,.002),(.003,.003,.003),'white')


@item('baguette_in_paper_sleeve')
def baguette(a):
    # Crimped paper sleeve has a real open mouth around the bread.
    section=[(-.034,.004),(-.035,.031),(-.024,.046),(.024,.046),(.035,.031),(.034,.004)]
    vs=[(x,y,z) for y in (-.140,.056) for x,z in section]
    a.mesh(vs,[tuple(reversed(range(6)))]+[(i,(i+1)%6,(i+1)%6+6,i+6) for i in range(6)],'cream')
    inner=[(x*.95,.056,z*.96+.001) for x,z in section]
    a.mesh(vs[6:]+inner,[(i,(i+1)%6,(i+1)%6+6,i+6) for i in range(6)],'paper')
    ball(a,(0,.087,.026),(.031,.130,.026),'wood_light',12,4)
    for y in (.070,.111,.151,.187):
        z=.026+.026*math.sqrt(max(0,1-((y-.087)/.130)**2))
        a.beam((-.016,y-.007,z),(.016,y+.007,z),.004,.001,'cream')
    box(a,(0,-.052,.047),(.039,.061,.001),'wood_dark')


@item('discarded_six_pack_rings')
def sixpack(a):
    for x in (-.060,0,.060):
        for y in (-.032,.032): ring(a,(x,y,.002),.028,.002,'cream',n=8)
    for x in (-.030,.030): box(a,(x,0,.002),(.008,.064,.004),'cream')
    for x in (-.060,0,.060): box(a,(x,0,.002),(.014,.008,.004),'cream')


@item('discarded_crown_bottle_cap')
def bottle_cap(a):
    # Flared alternating crown skirt and closed embossed top.
    n=16
    vs=[]
    for z,r in [(0,.016),(.006,.013),(.009,.013)]:
        for i in range(n):
            rr=r*(1.0 if i%2==0 or z>0 else .87)
            vs.append((rr*math.cos(i*math.tau/n),rr*math.sin(i*math.tau/n),z))
    a.mesh(vs,[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]+[(n+i,n+(i+1)%n,2*n+(i+1)%n,2*n+i) for i in range(n)]+[tuple(reversed(range(n))),tuple(range(2*n,3*n))],'gold')
    disk(a,.010,.009,.002,'cream',10)


@item('discarded_bottle_cork')
def cork(a):
    rod(a,(-.023,0,.011),(.023,0,.011),.011,'wood_light',10)
    for x,y,z in [(-.012,-.006,.020),(0,.003,.022),(.011,-.005,.020)]: box(a,(x,y,z),(.004,.002,.001),'wood_dark',rot=.2)
    ring(a,(.022,0,.011),.007,.001,'brown',axis='x',n=8)


@item('partly_eaten_ice_pop')
def ice_pop(a):
    box(a,(0,-.039,.005),(.013,.133,.005),'wood_light')
    outline=[(-.031,-.024),(.031,-.024),(.031,.069),(.021,.078),(.011,.070),(.005,.081),(-.007,.077),(-.016,.086),(-.028,.076),(-.031,.062)]
    a.prism(outline,.006,.022,'terracotta')
    box(a,(0,.022,.023),(.006,.071,.0015),'orange')
