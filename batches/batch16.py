"""Fifty original handheld food, beverage, packaging and sidewalk litter props.
Metres; muted, readable, logo-free forms with deliberately low export budgets.
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
    a.sphere(p,1,m,segments=n,rings=rings,scale=s)


def taperbox(a,z,h,w0,d0,w1,d1,m='paper'):
    vs=[(-w0/2,-d0/2,z),(w0/2,-d0/2,z),(w0/2,d0/2,z),(-w0/2,d0/2,z),(-w1/2,-d1/2,z+h),(w1/2,-d1/2,z+h),(w1/2,d1/2,z+h),(-w1/2,d1/2,z+h)]
    a.mesh(vs,[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],m)


def tray(a,w,d,h,m='paper'):
    box(a,(0,0,.003),(w,d,.006),m)
    for x in (-w/2,w/2): box(a,(x,0,h/2),(.005,d,h),m)
    for y in (-d/2,d/2): box(a,(0,y,h/2),(w,.005,h),m)


def pouch(a,w,h,d,m='paper'):
    # Plump four-sided packet, pinched at both heat-sealed ends.
    vs=[(-w/2,-.003,0),(w/2,-.003,0),(w/2,.003,0),(-w/2,.003,0),(-w*.56,-d/2,h*.48),(w*.56,-d/2,h*.48),(w*.56,d/2,h*.48),(-w*.56,d/2,h*.48),(-w/2,-.003,h),(w/2,-.003,h),(w/2,.003,h),(-w/2,.003,h)]
    fs=[(3,2,1,0),(8,9,10,11)]+[(j*4+i,j*4+(i+1)%4,(j+1)*4+(i+1)%4,(j+1)*4+i) for j in range(2) for i in range(4)]
    a.mesh(vs,fs,m)
    box(a,(0,0,.004),(w,.008,.008),m)
    box(a,(0,0,h-.004),(w,.008,.008),m)


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
    lathe(a,[(.028,0),(.033,.009),(.033,.113),(.028,.120)],'red',12)
    disk(a,.122,.029,.004,'silver',12)
    disk(a,.003,.029,.004,'silver',12)
    box(a,(0,.008,.125),(.013,.022,.002),'dark_metal')
    ring(a,(0,-.005,.128),.008,.002,'silver',n=8)


@item('crushed_soda_can')
def crushed(a):
    n=10
    specs=[(.029,0,0),(.035,.020,.30),(.023,.040,-.15),(.033,.059,.24)]
    vs=[]
    for j,(r,z,phase) in enumerate(specs):
        for i in range(n):
            t=i*math.tau/n+phase
            rr=r*(.73 if (i+j)%4==0 else 1)
            vs.append((rr*math.cos(t),rr*math.sin(t),z+.004*math.sin(i*2+j)))
    fs=[tuple(reversed(range(n))),tuple(range(3*n,4*n))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(3) for i in range(n)]
    a.mesh(vs,fs,['silver','silver']+['blue']*(3*n))
    box(a,(.007,0,.066),(.014,.019,.003),'silver',rot=(.2,.2,.2))


@item('ribbed_water_bottle')
def water(a):
    lathe(a,[(.027,0),(.032,.010),(.032,.117),(.024,.141),(.012,.154),(.012,.166)],'glass',10)
    for z in (.025,.045,.116): ring(a,(0,0,z),.032,.002,'glass')
    lathe(a,[(.033,.055),(.033,.096)],'paper')
    lathe(a,[(.013,.162),(.014,.180)],'blue')


@item('longneck_glass_bottle')
def glass_bottle(a):
    lathe(a,[(.028,0),(.031,.012),(.031,.125),(.014,.164),(.012,.221)],'green',10)
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
    box(a,(0,-.019,.079),(.062,.002,.062),'teal')
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
    for y in (-.018,.018): ball(a,(0,y,.041),(.089,.022,.026),'wood_light',10,3)
    rod(a,(-.073,0,.061),(.073,0,.061),.015,'brick',8)
    a.tube([(-.065,0,.078),(-.035,-.006,.078),(-.008,.006,.078),(.022,-.005,.078),(.055,.004,.078)],.0025,'yellow',5)


@item('street_taco_in_wrapper')
def taco(a):
    box(a,(0,0,.003),(.17,.115,.006),'paper',rot=.14)
    # Standing folded tortilla and visible filling along its mouth.
    a.mesh([(-.065,-.026,.006),(.065,-.026,.006),(.082,-.018,.053),(.057,-.018,.083),(-.057,-.018,.083),(-.082,-.018,.053),(-.065,.026,.006),(.065,.026,.006),(.082,.018,.053),(.057,.018,.083),(-.057,.018,.083),(-.082,.018,.053)],[(5,4,3,2,1,0),(6,7,8,9,10,11),(0,1,7,6),(1,2,8,7),(2,3,9,8),(3,4,10,9),(4,5,11,10),(5,0,6,11)],'wood_light')
    for i in range(6):
        ball(a,(-.050+i*.020,0,.080),(.014,.014,.009),'foliage' if i%2 else 'brick',6,3)


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
    ball(a,(0,0,.055),(.036,.036,.021),'cream',10,3)
    a.beam((.019,.008,.050),(.038,.018,.126),.011,.003,'wood_light')
    ball(a,(.039,.019,.128),(.012,.006,.012),'wood_light',6,3)


@item('waffle_ice_cream_cone')
def cone(a):
    a.cone((0,0,.100),(0,0,0),.036,'wood_light',10)
    ring(a,(0,0,.099),.034,.003,'brown')
    ball(a,(0,0,.120),(.044,.044,.040),'cream',10,4)
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
    box(a,(0,-.032,.105),(.101,.004,.067),'navy')
    ball(a,(0,-.035,.108),(.031,.004,.019),'wood_light',8,3)


@item('soft_street_pretzel')
def pretzel(a):
    # A characteristic three-loop pretzel, laid flat on a small deli sheet.
    box(a,(0,0,.002),(.17,.15,.004),'paper',rot=.10)
    path=[(-.046,-.050,.018),(.051,.031,.018),(.055,.058,.018),(.022,.067,.018),(.005,.046,.018),(0,.012,.020),(-.006,.046,.018),(-.023,.067,.018),(-.055,.057,.018),(-.058,.028,.018),(.044,-.050,.018)]
    a.tube(path,.010,'wood_light',6)
    for x,y in [(-.043,.040),(.044,.041),(0,.010),(-.024,-.027),(.026,-.024)]: box(a,(x,y,.029),(.004,.006,.003),'white',rot=.40)


@item('popcorn_carton')
def popcorn(a):
    taperbox(a,0,.137,.065,.056,.095,.079,'paper')
    for x in (-.030,0,.030): box(a,(x,-.040,.094),(.012,.002,.085),'brick',rot=(.07,0,0))
    for x,y,z in [(-.031,-.021,.140),(0,-.020,.145),(.031,-.020,.142),(-.023,.010,.150),(.009,.011,.150),(.032,.014,.143)]: ball(a,(x,y,z),(.019,.018,.018),'cream',6,3)


@item('paper_takeaway_bag')
def takeaway_bag(a):
    taperbox(a,0,.204,.136,.074,.140,.080,'wood_light')
    box(a,(0,0,.205),(.140,.080,.008),'brown')
    for y in (-.027,.027):
        a.tube([(-.037,y,.206),(-.037,y,.270),(.037,y,.270),(.037,y,.206)],.003,'cream',6)
    box(a,(0,-.042,.113),(.074,.002,.057),'paper')
    box(a,(0,-.0435,.111),(.037,.001,.014),'wood_dark')


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
    rod(a,(0,0,.012),(0,0,.047),.012,'wood_light',6,r2=.008)
    # Three tapered curved peel flaps laid outward from the short stem.
    for theta in (0,2.15,4.3):
        c,s=math.cos(theta),math.sin(theta)
        coords=[(0,-.011,.015),(.035,-.017,.010),(.090,-.012,.007),(.111,0,.018),(.090,.012,.007),(.035,.017,.010),(0,.011,.015)]
        top=[(x*c-y*s,x*s+y*c,z+.003) for x,y,z in coords]
        low=[(x*c-y*s,x*s+y*c,z) for x,y,z in coords]
        n=len(coords)
        a.mesh(low+top,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],'yellow')
    disk(a,.049,.009,.004,'brown',6)


@item('discarded_apple_core')
def apple_core(a):
    lathe(a,[(.022,0),(.026,.008),(.012,.025),(.011,.049),(.025,.064),(.026,.073)],'cream',8)
    disk(a,.005,.025,.007,'brick',8)
    disk(a,.075,.025,.007,'brick',8)
    rod(a,(0,0,.078),(.006,.001,.098),.003,'wood_dark',6)
    for z in (.028,.043): ball(a,(.011,0,z),(.002,.004,.005),'brown',6,3)


@item('triangular_sandwich_half')
def sandwich(a):
    points=[(-.065,-.055),(.065,-.055),(-.065,.075)]
    a.prism(points,0,.014,'wood_light')
    a.prism([(-.059,-.049),(.055,-.049),(-.059,.065)],.014,.018,'cream')
    a.prism(points,.018,.024,'foliage_dark')
    a.prism([(-.063,-.053),(.062,-.053),(-.063,.070)],.024,.031,'pink')
    a.prism(points,.031,.036,'yellow')
    a.prism(points,.036,.050,'wood_light')
    a.prism([(-.059,-.049),(.055,-.049),(-.059,.065)],.050,.052,'cream')


@item('broken_chocolate_chip_cookie')
def cookie(a):
    a.prism([(-.038,-.017),(-.018,-.036),(.011,-.039),(.038,-.019),(.039,.012),(.018,.035),(-.007,.038),(.002,.015),(-.019,.017),(-.023,.001),(-.038,.006)],0,.009,'wood_light')
    for x,y in [(-.018,-.014),(.005,-.019),(.023,-.007),(.019,.017),(-.005,.025)]: box(a,(x,y,.011),(.007,.006,.004),'wood_dark',rot=.30)
    a.prism([(-.055,.017),(-.036,.019),(-.044,.039)],.001,.009,'wood_light')


@item('crumpled_food_wrapper')
def food_wrapper(a):
    # Uneven, triangulated sheet; both sides have an outward winding.
    vs=[(-.10,-.07,.012),(0,-.08,0),(.09,-.06,.019),(-.11,0,.028),(0,0,.023),(.10,.005,.006),(-.08,.075,.008),(.005,.069,.026),(.082,.075,.015)]
    triangles=[(0,1,4),(0,4,3),(1,2,5),(1,5,4),(3,4,7),(3,7,6),(4,5,8),(4,8,7)]
    a.mesh(vs+[(x,y,z+.001) for x,y,z in vs],[tuple(reversed(t)) for t in triangles]+[tuple(i+9 for i in t) for t in triangles],['silver']*8+['paper']*8)
    box(a,(.015,.012,.025),(.050,.012,.001),'brick',rot=(.08,.04,.2))


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
    ball(a,(0,0,.022),(.041,.035,.021),'paper',7,3)
    box(a,(-.019,-.013,.023),(.038,.044,.002),'white',rot=(.15,.40,.35))
    box(a,(.017,.009,.038),(.040,.024,.002),'paper',rot=(-.22,-.36,-.5))
    box(a,(.004,-.020,.035),(.042,.022,.002),'cream',rot=(.36,.14,.7))


@item('disposable_plastic_fork')
def fork(a):
    a.prism([(-.006,-.09),(.006,-.09),(.006,.019),(.017,.030),(.017,.049),(-.017,.049),(-.017,.030),(-.006,.019)],0,.003,'white')
    for x in (-.0135,-.0045,.0045,.0135): box(a,(x,.065,.0015),(.005,.039,.003),'white')


@item('disposable_plastic_spoon')
def spoon(a):
    box(a,(0,-.036,.003),(.012,.122,.005),'cream')
    ball(a,(0,.045,.006),(.023,.036,.006),'cream',10,3)
    ball(a,(0,.045,.0085),(.018,.030,.003),'paper',10,3)


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
    box(a,(0,0,.003),(.173,.115,.006),'silver')
    for x in (-.091,.091): box(a,(x,0,.025),(.005,.127,.046),'silver',rot=(0,-.13 if x<0 else .13,0))
    for y in (-.064,.064): box(a,(0,y,.025),(.183,.005,.046),'silver',rot=(.13 if y<0 else -.13,0,0))
    for x in (-.094,.094): rod(a,(x,-.067,.047),(x,.067,.047),.003,'steel',6)
    for y in (-.067,.067): rod(a,(-.094,y,.047),(.094,y,.047),.003,'steel',6)
    for x in (-.068,-.034,0,.034,.068): box(a,(x,-.067,.027),(.005,.004,.033),'steel')


@item('ketchup_sachet')
def ketchup(a):
    pouch(a,.038,.076,.010,'brick')
    box(a,(0,-.006,.037),(.026,.0015,.030),'paper')
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
    box(a,(0,-.043,.020),(.070,.195,.040),'cream')
    ball(a,(0,.093,.026),(.031,.124,.025),'wood_light',10,4)
    for y in (.031,.075,.119,.163): box(a,(0,y,.050),(.040,.005,.002),'cream',rot=.45)
    box(a,(0,-.052,.041),(.041,.067,.002),'wood_dark')
    box(a,(0,.054,.020),(.074,.006,.042),'paper')


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
