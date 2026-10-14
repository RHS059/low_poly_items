"""Fifty distinct American sidewalk retail and commercial food-service fixtures.
Meter-scale geometry, intentionally restrained finishes, fully modeled hardware.
"""
from math import pi, sin, cos
from assetlib import Asset, register


def prop(name, category='retail_food_service', size='person'):
    def wrap(builder):
        def factory():
            a = Asset('b10_' + name, category, size_class=size)
            builder(a)
            return a.bottom_center()
        factory.__name__ = 'b10_' + name
        register(factory.__name__, category, size, factory)
        return factory
    return wrap


def rod(a, p, q, r=.016, mat='steel', n=8):
    a.cylinder(p, q, r, mat, n)


def disc(a, x,y,z,r,h=.025,mat='steel',n=12):
    rod(a,(x,y,z),(x,y,z+h),r,mat,n)


def legs(a, w,d,h,mat='dark_metal',z=0,r=.023):
    for x in (-w/2,w/2):
        for y in (-d/2,d/2):
            rod(a,(x,y,z),(x,y,z+h),r,mat)
            disc(a,x,y,z,.035,.025,'rubber',8)


def casters(a,w,d,z=.11,r=.075):
    for x in (-w/2,w/2):
        for y in (-d/2,d/2):
            a.box((x,y,z+.055),(.04,.09,.11),'steel')
            rod(a,(x-.026,y,z-.025),(x+.026,y,z-.025),r,'rubber',10)
            rod(a,(x-.032,y,z-.025),(x+.032,y,z-.025),r*.4,'steel',8)


def wheel(a,x,y,z,r=.23):
    rod(a,(x,y-.045,z),(x,y+.045,z),r,'rubber',12)
    rod(a,(x,y-.049,z),(x,y+.049,z),r*.7,'metal',10)
    rod(a,(x,y-.055,z),(x,y+.055,z),.045,'steel',8)


def handle(a,x,y,z,w=.16,mat='steel'):
    a.tube([(x-w/2,y,z),(x-w/2,y-.04,z),(x+w/2,y-.04,z),(x+w/2,y,z)],.012,mat,6)


def grille(a,x,y,z,w,h,n=6):
    a.box((x,y,z),(w,.012,h),'black')
    for i in range(n):
        a.box((x,y-.012,z-h/2+(i+.5)*h/n),(w*.92,.016,.012),'metal')


def sign(a,x,y,z,w,h,mat='cream'):
    a.box((x,y,z),(w,.04,h),'dark_metal')
    a.box((x,y-.026,z),(w-.05,.012,h-.05),mat)


def script(a,x,y,z,w=.3,n=3,mat='cream'):
    for j in range(n):
        a.box((x,y,z-j*.055),(w*(1-.15*(j%2)),.008,.014),mat)


def cabinet(a,w,d,h,z=.15,mat='teal'):
    a.box((0,0,z+h/2),(w,d,h),mat)
    a.box((0,0,z+.035),(w+.035,d+.035,.07),'dark_metal')
    a.box((0,0,z+h+.018),(w+.05,d+.05,.036),'steel')


def framed_panel(a,x,y,z,w,h,mat='glass'):
    a.box((x,y,z),(w,.025,h),'dark_metal')
    a.box((x,y-.018,z),(w-.055,.009,h-.055),mat)


def serving_counter(a,w=1.3,d=.65,h=.92,mat='steel'):
    legs(a,w-.14,d-.14,h-.06,'steel',r=.027)
    a.box((0,0,h),(w,d,.075),mat)
    a.box((0,0,.25),(w-.08,d-.08,.035),'steel')


def pan(a,x,y,z,w,d):
    a.box((x,y,z),(w,d,.025),'dark_metal')
    for xx in (x-w/2,x+w/2): a.box((xx,y,z+.05),(.02,d+.02,.11),'steel')
    for yy in (y-d/2,y+d/2): a.box((x,yy,z+.05),(w,.02,.11),'steel')


def awning(a,w,d,z,mat='cream',x=0,y=0):
    # An eight-panel pitched fabric cover, with a striped, hanging scallop-like valance.
    for side in (-1,1):
        for i in range(4):
            xx=x-w/2+(i+.5)*w/4
            a.box((xx,y+side*d/4,z+.08),(w/4,d*.52,.035),mat if i%2 else 'teal',rot=(side*-.18,0,0))
        for i in range(8):
            a.box((x-w/2+(i+.5)*w/8,y+side*d/2,z-.065),(w/8,.022,.16),mat if i%2 else 'teal')


def tub(a,x,y,z,r,h,mat='steel'):
    rod(a,(x,y,z),(x,y,z+h),r*.75,mat,10)
    a.cylinder((x,y,z),(x,y,z+h),r*.76,mat,10,radius2=r)
    disc(a,x,y,z+h,r,.022,mat,10)
    disc(a,x,y,z+h+.023,r*.82,.004,'black',10)


def crate(a,x,y,z,w=.42,d=.32,h=.23):
    a.box((x,y,z+.025),(w,d,.05),'wood_dark')
    for lev in (.08,h-.025):
        for yy in (y-d/2,y+d/2): a.box((x,yy,z+lev),(w,.025,.055),'wood')
        for xx in (x-w/2,x+w/2): a.box((xx,y,z+lev),(.025,d,.055),'wood')
    for xx in (-1,1):
        for yy in (-1,1): a.box((x+xx*w*.47,y+yy*d*.46,z+h/2),(.027,.027,h),'wood_dark')


@prop('hot_dog_pushcart',size='large')
def hotdog(a):
    cabinet(a,1.35,.64,.48,.40,'steel')
    for y in (-.4,.4): wheel(a,.25,y,.27,.27)
    rod(a,(.25,-.46,.27),(.25,.46,.27),.022,'dark_metal')
    rod(a,(-.52,0,.04),(-.52,0,.43),.025,'steel')
    a.tube([(-.65,-.25,.64),(-.93,-.25,.86),(-.93,.25,.86),(-.65,.25,.64)],.024,'steel',8)
    for x in (-.32,.04):
        a.box((x,0,.94),(.29,.44,.065),'silver')
        handle(a,x,-.04,.991,.12)
    rod(a,(.48,.24,.9),(.48,.24,2.2),.02,'steel')
    a.cone((.48,.24,1.92),(.48,.24,2.21),.88,'cream',12)
    disc(a,.48,.24,2.21,.038,.07,'dark_metal',8)
    a.box((.48,-.1,1.04),(.20,.23,.22),'cream')
    sign(a,0,-.34,.66,.9,.25,'navy');script(a,0,-.369,.72,.62,2)


@prop('sidewalk_coffee_kiosk',size='large')
def coffee(a):
    a.box((0,0,.08),(2.0,1.55,.16),'concrete')
    a.box((0,.68,1.15),(1.86,.12,2.13),'wood_dark')
    for x in (-.91,.91):
        a.box((x,0,1.15),(.1,1.35,2.13),'teal')
        a.box((x,-.66,1.16),(.11,.11,2.15),'dark_metal')
    a.box((0,-.60,.56),(1.75,.12,.93),'wood')
    for x in (-.72,-.48,-.24,0,.24,.48,.72): a.box((x,-.67,.56),(.027,.023,.90),'wood_light')
    a.box((0,-.66,1.05),(2.08,.52,.075),'wood_dark')
    a.box((0,.02,2.25),(2.18,1.73,.12),'dark_metal',rot=(.06,0,0))
    sign(a,0,-.708,1.94,1.42,.31,'black');script(a,0,-.738,2.00,.75,2)
    a.box((-.44,.1,1.22),(.62,.40,.48),'steel');a.box((-.44,-.115,1.25),(.52,.022,.20),'black')
    for x in (-.57,-.30): rod(a,(x,-.13,1.19),(x,-.23,1.19),.022,'steel')
    disc(a,.53,-.6,1.09,.065,.14,'cream',8)
    a.box((.48,.46,1.26),(.47,.025,.48),'black');script(a,.48,.441,1.40,.31,5)


@prop('spiral_snack_vending_machine')
def snack(a):
    cabinet(a,.98,.80,1.78,.10,'navy')
    a.box((-.13,-.415,1.23),(.68,.025,1.20),'black')
    for row in range(4):
        z=.81+row*.26
        a.box((-.13,-.43,z-.11),(.64,.19,.02),'steel')
        for col in range(3):
            x=-.35+col*.22
            a.box((x,-.446,z),(.13,.05,.16),('cream','terracotta','green')[(row+col)%3],rot=(0,0,.05*(col-1)))
            a.torus((x,-.487,z-.065),.041,.007,'metal',axis='y',segments=8,sides=4)
    for x in (-.48,.22): a.box((x,-.454,1.20),(.04,.05,1.25),'steel')
    sign(a,.35,-.43,1.44,.18,.24,'glass')
    for z in (1.15,1.03,.91):
        for x in (.30,.39): a.box((x,-.448,z),(.055,.018,.043),'steel')
    a.box((0,-.447,.34),(.66,.03,.21),'black');a.box((0,-.478,.31),(.61,.02,.08),'dark_metal')
    grille(a,.33,-.43,.55,.18,.17,4)


@prop('bottled_drink_vending_machine')
def drinks(a):
    cabinet(a,1.05,.83,1.76,.09,'green')
    framed_panel(a,-.2,-.43,1.20,.54,1.14,'cream')
    for j in range(3):
        z=.85+j*.29
        rod(a,(-.20,-.46,z),(-.20,-.46,z+.19),.054,'teal',8)
        rod(a,(-.20,-.46,z+.19),(-.20,-.46,z+.235),.022,'white',8)
    for j in range(6):
        z=.74+j*.16
        a.box((.30,-.436,z),(.28,.027,.11),'dark_metal')
        a.box((.25,-.456,z),(.12,.012,.074),('cream','brown','teal')[j%3])
        rod(a,(.39,-.45,z),(.39,-.475,z),.029,'steel',8)
    a.box((0,-.439,.37),(.68,.03,.19),'black')
    a.box((0,-.482,.29),(.72,.11,.035),'steel')
    a.box((.30,-.454,1.74),(.23,.012,.045),'black')
    grille(a,0,-.435,.18,.86,.11,3)


@prop('paid_newspaper_honor_box')
def newspaper(a):
    a.box((0,0,.08),(.58,.48,.16),'dark_metal')
    cabinet(a,.53,.42,.70,.43,'blue')
    a.box((0,0,.31),(.35,.32,.31),'blue')
    framed_panel(a,0,-.225,.78,.43,.46,'paper')
    a.box((-.075,-.246,.84),(.19,.01,.14),'metal');script(a,.04,-.251,.96,.26,2,'navy')
    handle(a,.11,-.25,.68,.12)
    a.box((.14,-.232,1.08),(.12,.027,.035),'black')
    a.box((0,0,1.18),(.61,.49,.09),'blue',rot=(-.10,0,0))


@prop('free_weekly_news_dispenser')
def weekly(a):
    a.box((0,0,.045),(.50,.44,.09),'black')
    a.cylinder((0,0,.09),(0,0,.66),.15,'dark_metal',8,radius2=.12)
    a.box((0,.03,.83),(.49,.38,.37),'green')
    a.box((0,-.172,.82),(.41,.026,.19),'black')
    for i in range(4): a.box((0,-.187,.77+i*.009),(.36,.13,.008),'paper')
    a.box((0,0,1.06),(.58,.49,.13),'green',rot=(-.14,0,0))
    sign(a,0,-.216,1.03,.34,.105,'cream')


@prop('twin_globe_candy_dispenser')
def candy(a):
    disc(a,0,0,0,.28,.06,'dark_metal')
    rod(a,(0,0,.06),(0,0,.75),.045,'steel')
    a.box((0,0,.76),(.56,.22,.065),'dark_metal')
    for x in (-.16,.16):
        a.box((x,0,.89),(.23,.25,.23),'red')
        a.sphere((x,0,1.10),.16,'glass',segments=10,rings=4,scale=(.15,.15,.19))
        disc(a,x,0,1.27,.12,.035,'steel',10)
        rod(a,(x,-.133,.93),(x,-.162,.93),.058,'steel',10)
        a.box((x,-.18,.93),(.11,.026,.018),'dark_metal')
        a.box((x,-.144,.81),(.10,.025,.05),'black')
        for i in range(5):
            t=i*2*pi/5
            a.sphere((x+.084*cos(t),.084*sin(t),1.09),.042,('cream','brown','yellow')[i%3],segments=6,rings=3)


@prop('outdoor_bagged_ice_chest')
def ice_chest(a):
    cabinet(a,1.62,.78,1.18,.12,'white')
    for x in (-.39,.39):
        framed_panel(a,x,-.407,.77,.75,.95,'cream');handle(a,x+.21,-.436,.76,.13)
        for z in (.40,1.10): a.box((x-.32,-.442,z),(.033,.025,.10),'steel')
    a.box((0,0,1.37),(1.75,.86,.09),'steel',rot=(.04,0,0))
    # Simple ice-crystal emblem on each insulated door.
    for x in (-.39,.39):
        for angle in (0,pi/3,-pi/3): a.box((x,-.449,.94),(.28,.012,.018),'blue',rot=(0,angle,0))
    grille(a,0,-.416,.23,1.36,.12,3)


@prop('tiered_sidewalk_produce_stand')
def produce(a):
    for x in (-.61,.61):
        a.beam((x,-.38,0),(x,.25,1.24),.055,mat='wood_dark')
        a.beam((x,.32,0),(x,.32,1.24),.055,mat='wood_dark')
    for row in range(3):
        y=-.27+row*.24;z=.35+row*.35
        a.box((0,y,z),(1.30,.40,.045),'wood_dark')
        for col in range(3):
            x=-.43+col*.43;crate(a,x,y,z+.025,.40,.34,.20)
            for k in range(3): a.sphere((x-.11+k*.11,y,z+.16),.073,('green','terracotta','sand')[row],segments=6,rings=3)
    sign(a,0,.28,1.50,.86,.23,'cream');script(a,0,.251,1.55,.56,2,'wood_dark')
    for x in (-.36,.36): rod(a,(x,.30,1.12),(x,.30,1.50),.015,'steel')


@prop('florist_bucket_sidewalk_display')
def florist(a):
    legs(a,.84,.47,.25,'dark_metal')
    for z,y in ((.26,-.16),(.54,.20)):
        a.box((0,y,z),(1.03,.41,.045),'wood_dark')
        for x in (-.34,0,.34):
            tub(a,x,y,z+.025,.13,.30,'metal')
            for j in range(3):
                xx=x+(j-1)*.07;zz=z+.64+.045*(j%2)
                rod(a,(x,y,z+.22),(xx,y+.02*(j-1),zz),.008,'foliage_dark',5)
                a.sphere((xx,y+.02*(j-1),zz),.065,('cream','terracotta','purple')[j],segments=6,rings=3)
                a.box((x+.04,y,z+.46),(.095,.025,.032),'foliage',rot=(0,.6,0))
    for x in (-.47,.47): rod(a,(x,.21,.02),(x,.21,.54),.023,'dark_metal')


@prop('rolling_sidewalk_garment_rack')
def garment(a):
    casters(a,1.10,.50,.11,.07)
    for x in (-.55,.55):
        rod(a,(x,-.25,.19),(x,.25,.19),.028,'steel')
        rod(a,(x,0,.19),(x,0,1.66),.026,'steel')
    rod(a,(-.58,0,1.66),(.58,0,1.66),.026,'steel')
    for i in range(5):
        x=-.40+i*.20
        a.tube([(x-.075,0,1.43),(x,0,1.56),(x+.075,0,1.43),(x-.075,0,1.43)],.008,'wood_dark',5)
        # Distinct hanging coats with shoulder taper and split sleeve forms.
        a.box((x,0,1.12),(.15,.07,.62),('navy','brown','cream')[i%3])
        for side in (-1,1): a.beam((x+side*.062,0,1.42),(x+side*.115,0,1.14),.06,.07,('navy','brown','cream')[i%3])
    rod(a,(-.55,0,.36),(.55,0,.36),.02,'steel')


@prop('outdoor_bookshop_cart')
def books(a):
    casters(a,.78,.42,.11,.065)
    for x in (-.44,.44): a.box((x,0,.82),(.055,.47,1.29),'wood_dark')
    for z in (.23,.66,1.10):
        a.box((0,0,z),(.94,.48,.045),'wood')
        a.box((0,.22,z+.19),(.87,.025,.40),'wood_dark')
        for i in range(8): a.box((-.35+i*.10,-.005,z+.17),(.066,.27,.28+(.04 if i%3 else 0)),('brown','navy','cream','teal')[i%4],rot=(0,.03*(i%3-1),0))
    sign(a,0,0,1.54,.75,.18,'cream');script(a,0,-.027,1.58,.45,2,'wood_dark')


@prop('bakery_sidewalk_glass_case')
def bakery(a):
    serving_counter(a,1.18,.64,.74,'wood')
    a.box((0,.29,1.14),(1.20,.035,.80),'wood_dark')
    for x in (-.57,.57):
        a.box((x,0,1.14),(.018,.55,.70),'glass')
        for y in (-.27,.27): rod(a,(x,y,.76),(x,y,1.53),.014,'wood_dark',6)
    # Sliding front leaves are parked to the sides, exposing the bread shelves.
    for x in (-.46,.46): a.box((x,-.28,1.17),(.20,.018,.64),'glass',rot=(-.16,0,0))
    rod(a,(-.56,-.33,.88),(.56,-.33,.88),.012,'steel',6)
    a.box((0,.0,1.55),(1.24,.68,.045),'wood_dark')
    for z in (.86,1.14,1.40):
        a.box((0,0,z),(1.08,.48,.024),'steel')
        for x in (-.36,0,.36): a.sphere((x,-.04,z+.045),.08,'sand',segments=8,rings=3,scale=(.13,.07,.05))
    a.box((0,-.337,.75),(1.22,.06,.075),'wood_dark')


@prop('chalkboard_sandwich_a_frame')
def a_frame(a):
    for ysign in (-1,1):
        for x in (-.28,.28): a.beam((x,ysign*.31,.0),(x,0,1.03),.055,.055,'wood_dark')
        a.box((0,ysign*.14,.57),(.57,.025,.75),'wood',rot=(ysign*.285,0,0))
        a.box((0,ysign*.164,.57),(.48,.012,.65),'black',rot=(ysign*.285,0,0))
    rod(a,(-.31,0,1.04),(.31,0,1.04),.025,'steel')
    script(a,0,-.249,.76,.31,5,'cream')
    for x in (-.28,.28): rod(a,(x,-.18,.42),(x,.18,.42),.009,'steel',6)


@prop('restaurant_menu_display_podium')
def menu_podium(a):
    a.box((0,0,.025),(.52,.47,.05),'dark_metal')
    rod(a,(0,.05,.05),(0,.05,1.02),.034,'steel')
    a.box((0,0,1.08),(.58,.43,.045),'dark_metal',rot=(.50,0,0))
    a.box((0,-.016,1.106),(.50,.35,.008),'paper',rot=(.50,0,0))
    a.box((0,-.196,1.006),(.55,.024,.027),'steel')
    rod(a,(.24,.10,1.07),(.24,.10,1.26),.012,'steel',6)
    rod(a,(.24,.10,1.26),(.03,.04,1.30),.017,'dark_metal',6)


@prop('digital_restaurant_menu_totem')
def digital(a):
    a.box((0,0,.04),(.66,.47,.08),'dark_metal')
    a.box((0,0,1.05),(.58,.18,1.96),'dark_metal')
    framed_panel(a,0,-.101,1.29,.50,1.24,'navy')
    for j in range(3):
        z=.95+j*.33
        a.box((-.12,-.129,z),(.14,.007,.18),('sand','wood','cream')[j])
        for k in range(3): a.box((.10,-.133,z+.06-k*.05),(.17,.007,.012),'white')
    a.box((0,-.103,.40),(.22,.012,.035),'steel')
    grille(a,0,.10,.29,.35,.17,4)


@prop('round_bistro_pedestal_table')
def bistro(a):
    for t in (0,2*pi/3,4*pi/3):
        a.beam((0,0,.15),(.34*cos(t),.34*sin(t),.028),.045,.065,'dark_metal')
    rod(a,(0,0,.12),(0,0,.70),.041,'dark_metal')
    disc(a,0,0,.70,.40,.045,'wood_dark',16)
    for y in (-.24,-.12,0,.12,.24):
        w=2*(.375**2-y*y)**.5
        a.box((0,y,.752),(w,.10,.017),'wood')


@prop('woven_metal_cafe_chair')
def cafe_chair(a):
    for x in (-.21,.21):
        rod(a,(x,-.22,.025),(x,-.18,.48),.019,'dark_metal')
        rod(a,(x,.23,.025),(x,.20,.93),.02,'dark_metal')
        rod(a,(x,-.18,.43),(x,.20,.43),.017,'dark_metal')
    for y in (-.13,-.04,.05,.14): a.box((0,y,.455),(.45,.075,.027),'wood')
    for z in (.66,.75,.84): a.box((0,.214,z),(.44,.035,.063),'wood',rot=(-.08,0,0))
    rod(a,(-.22,.21,.92),(.22,.21,.92),.02,'dark_metal')
    rod(a,(-.21,-.19,.24),(.21,-.19,.24),.012,'dark_metal')


@prop('cafe_bar_stool_with_back')
def cafe_stool(a):
    for t in range(4):
        th=pi/4+t*pi/2
        rod(a,(.28*cos(th),.28*sin(th),0),(.19*cos(th),.19*sin(th),.77),.020,'steel')
    a.torus((0,0,.29),.215,.014,'dark_metal',segments=12,sides=5)
    disc(a,0,0,.77,.255,.047,'wood_dark',12)
    for x in (-.16,.16): rod(a,(x,.16,.75),(x,.22,1.15),.018,'steel')
    a.box((0,.22,1.10),(.38,.05,.17),'wood')


@prop('square_cafe_umbrella_table',size='large')
def umbrella_table(a):
    legs(a,.58,.58,.74,'dark_metal')
    a.box((0,0,.76),(.86,.86,.055),'wood_dark')
    for x in (-.30,-.15,0,.15,.30): a.box((x,0,.799),(.13,.82,.018),'wood')
    disc(a,0,0,0,.27,.055,'dark_metal')
    rod(a,(0,0,.04),(0,0,2.17),.025,'wood_dark')
    a.cone((0,0,1.98),(0,0,2.30),1.03,'cream',8)
    for i in range(8):
        t=pi*i/4
        rod(a,(0,0,2.22),(.96*cos(t),.96*sin(t),1.98),.009,'wood_dark',5)
    disc(a,0,0,2.30,.035,.065,'dark_metal',8)


@prop('commercial_flat_top_griddle_cart')
def griddle(a):
    casters(a,1.02,.49,.11)
    serving_counter(a,1.30,.68,.87)
    a.box((0,0,1.01),(1.12,.59,.24),'steel')
    a.box((0,-.01,1.14),(1.04,.53,.025),'dark_metal')
    for x in (-.54,.54): a.box((x,0,1.20),(.025,.60,.16),'steel')
    a.box((0,.29,1.24),(1.12,.025,.23),'steel')
    for x in (-.36,0,.36): rod(a,(x,-.32,1.03),(x,-.35,1.03),.039,'black',10)
    a.box((.72,0,.96),(.32,.64,.04),'steel')
    a.cylinder((0,0,.30),(0,0,.65),.16,'white',10,radius2=.14)
    disc(a,0,0,.65,.075,.035,'steel',8)


@prop('street_vendor_skewer_grill_cart')
def skewers(a):
    for y in (-.34,.34): wheel(a,.38,y,.23,.23)
    legs(a,.85,.42,.71,'dark_metal')
    a.box((0,0,.77),(1.08,.56,.19),'dark_metal')
    a.box((0,0,.875),(.96,.44,.025),'black')
    for x in (-.40,-.27,-.14,0,.14,.27,.40):
        rod(a,(x,-.34,.91),(x,.25,.91),.009,'steel',6)
        rod(a,(x,-.34,.91),(x,-.44,.91),.019,'wood_dark',6)
    for y in (-.26,.26): a.box((0,y,.96),(1.10,.025,.17),'metal')
    a.box((-.68,0,.81),(.29,.52,.025),'wood')
    a.box((0,0,.30),(.83,.42,.03),'metal')
    handle(a,.0,-.30,.74,.23)


@prop('wood_fired_pizza_oven_cart',size='large')
def pizza(a):
    casters(a,1.15,.79,.12,.09)
    legs(a,1.10,.74,.81,'dark_metal',z=.16,r=.035)
    a.box((0,0,.99),(1.36,1.02,.12),'concrete_light')
    a.sphere((0,.12,1.12),.55,'terracotta',segments=12,rings=4,scale=(.60,.49,.52))
    a.box((0,-.32,1.12),(.73,.12,.33),'brick')
    a.box((0,-.39,1.12),(.49,.015,.26),'black')
    rod(a,(.25,.22,1.49),(.25,.22,2.02),.095,'dark_metal',10)
    disc(a,.25,.22,2.01,.14,.033,'steel',10)
    a.box((0,-.52,.98),(1.16,.24,.065),'concrete_light')
    a.box((0,0,.33),(1.14,.78,.045),'wood_dark')
    for x in (-.39,-.13,.13,.39): rod(a,(x,-.28,.40),(x,.29,.40),.085,'wood',8)


@prop('taco_preparation_service_station')
def taco(a):
    cabinet(a,1.45,.72,.78,.12,'steel');casters(a,1.24,.54,.095,.065)
    for x in (-.36,.36): framed_panel(a,x,-.375,.54,.67,.52,'metal');handle(a,x,-.397,.70,.14)
    for x in (-.44,-.14,.16): pan(a,x,.10,.93,.24,.31)
    a.box((.54,-.03,.94),(.26,.56,.055),'cream')
    for x in (-.66,.66): rod(a,(x,.28,.93),(x,.28,1.58),.018,'steel')
    a.box((0,.02,1.58),(1.43,.62,.025),'glass',rot=(-.12,0,0))
    a.box((0,.31,1.43),(1.43,.025,.28),'glass')
    a.box((0,-.40,.91),(1.49,.17,.035),'steel')


@prop('lemonade_stand_with_canopy')
def lemonade(a):
    a.box((0,0,.48),(1.14,.61,.85),'wood')
    for x in (-.49,-.25,0,.25,.49): a.box((x,-.32,.47),(.018,.022,.81),'wood_dark')
    a.box((0,-.05,.93),(1.28,.78,.06),'wood_light')
    for x in (-.57,.57): rod(a,(x,.22,.91),(x,.22,1.92),.025,'wood_dark')
    awning(a,1.43,.88,1.88,'cream')
    sign(a,0,-.337,.60,.87,.26,'cream');script(a,0,-.364,.66,.58,2,'wood_dark')
    for x in (-.28,.27):
        rod(a,(x,0,.97),(x,0,1.25),.105,'glass',10)
        disc(a,x,0,1.25,.11,.025,'steel',10)
        rod(a,(x,-.10,1.05),(x,-.16,1.05),.014,'steel',6)


@prop('shaved_ice_vendor_cart')
def shaved_ice(a):
    cabinet(a,1.08,.63,.61,.26,'teal');casters(a,.88,.47,.15,.095)
    a.box((-.15,0,.96),(.45,.39,.17),'cream')
    rod(a,(-.15,0,1.03),(-.15,0,1.37),.12,'steel',10)
    disc(a,-.15,0,1.37,.17,.05,'teal',10)
    a.box((-.15,-.19,1.09),(.16,.20,.10),'steel',rot=(.25,0,0))
    for x in (.19,.35,.51):
        rod(a,(x,.11,.91),(x,.11,1.12),.042,('brown','terracotta','cream')[int((x-.18)/.16)%3],8)
        rod(a,(x,.11,1.12),(x,.11,1.18),.017,'white',6)
    handle(a,0,-.334,.67,.28)
    a.tube([(-.54,.20,.75),(-.73,.20,.94),(-.73,-.20,.94),(-.54,-.20,.75)],.022,'steel',8)


@prop('popcorn_concession_pushcart')
def popcorn(a):
    for y in (-.38,.38): wheel(a,.25,y,.25,.25)
    legs(a,.78,.49,.67,'dark_metal')
    cabinet(a,.98,.62,.36,.48,'red')
    for x in (-.44,.44):
        for y in (-.26,.26): a.box((x,y,1.16),(.035,.035,.66),'gold')
    a.box((0,.27,1.18),(.87,.015,.61),'glass')
    for x in (-.45,.45): a.box((x,0,1.18),(.015,.50,.61),'glass')
    a.box((0,0,1.50),(1.10,.75,.15),'red')
    a.box((0,0,.87),(.88,.52,.08),'cream')
    disc(a,0,0,1.17,.19,.10,'steel',10)
    disc(a,0,0,1.27,.22,.025,'gold',10)
    rod(a,(0,0,1.30),(0,0,1.46),.015,'steel',6)
    handle(a,0,-.335,.65,.22)


@prop('pretzel_warmer_cart')
def pretzel(a):
    casters(a,.70,.48,.10,.065)
    cabinet(a,.86,.60,.49,.17,'navy')
    for x in (-.40,.40): a.box((x,0,1.05),(.035,.58,.80),'steel')
    a.box((0,.28,1.06),(.77,.018,.76),'glass')
    a.box((0,0,1.47),(.91,.64,.065),'steel')
    rod(a,(0,0,.72),(0,0,1.40),.015,'steel',6)
    for z in (.91,1.22):
        rod(a,(-.29,0,z),(.29,0,z),.014,'steel',6)
        for x in (-.22,.22):
            a.torus((x,-.035,z-.07),.071,.019,'sand',axis='y',segments=10,sides=5)
            a.beam((x-.055,-.04,z-.1),(x+.055,-.04,z-.035),.024,mat='sand')
    framed_panel(a,0,-.318,.44,.67,.24,'cream')


@prop('insulated_ice_cream_pushcart')
def ice_cream(a):
    for y in (-.40,.40): wheel(a,.26,y,.23,.23)
    a.box((0,0,.66),(1.25,.71,.72),'cream')
    a.box((0,0,.32),(1.30,.75,.065),'dark_metal')
    for x in (-.31,.31):
        a.box((x,0,1.035),(.59,.67,.055),'steel');handle(a,x,-.05,1.08,.15)
    a.tube([(-.62,-.29,.76),(-.91,-.29,.94),(-.91,.29,.94),(-.62,.29,.76)],.024,'steel',8)
    rod(a,(-.52,0,.04),(-.52,0,.32),.025,'dark_metal')
    sign(a,0,-.372,.70,.96,.32,'teal');script(a,0,-.40,.79,.62,3)
    a.box((.62,0,.92),(.10,.32,.14),'steel')


@prop('donut_shop_display_counter')
def donuts(a):
    legs(a,1.02,.47,.28,'dark_metal')
    a.box((0,0,.62),(1.16,.59,.71),'wood')
    a.box((0,.27,1.15),(1.17,.045,.38),'wood_dark')
    a.box((0,0,.99),(1.25,.67,.06),'wood_dark')
    for row in range(2):
        y=-.16+row*.29;z=1.045+row*.15
        a.box((0,y,z),(1.05,.25,.025),'steel')
        for x in (-.37,-.12,.13,.38): a.torus((x,y,z+.03),.067,.024,'sand',segments=10,sides=5)
    a.box((0,-.31,1.095),(1.18,.015,.13),'glass',rot=(-.16,0,0))
    for x in (-.58,.58): rod(a,(x,-.31,1.05),(x,-.25,1.48),.014,'steel',6)
    a.box((0,.0,1.50),(1.25,.66,.05),'wood_dark')
    for x in (-.58,.58): rod(a,(x,.24,.99),(x,.24,1.50),.014,'steel',6)


@prop('seafood_crushed_ice_display_table')
def seafood(a):
    serving_counter(a,1.50,.82,.78)
    pan(a,0,0,.83,1.46,.76)
    a.box((0,0,.88),(1.35,.65,.035),'white')
    for x,y in ((-.46,-.15),(-.12,.14),(.25,-.13),(.48,.17)):
        a.sphere((x,y,.93),.1,'metal',segments=8,rings=3,scale=(.18,.065,.045))
        a.cone((x+.15,y,.93),(x+.25,y,.93),.06,'metal',4)
    rod(a,(.62,.28,.31),(.62,.28,.81),.013,'steel',6)
    tub(a,.55,.22,.04,.13,.20,'metal')
    for x in (-.48,.45):
        rod(a,(x,.30,.9),(x,.30,1.14),.008,'steel',5);sign(a,x,.29,1.16,.23,.13,'paper')


@prop('rotating_sunglasses_display')
def sunglasses(a):
    disc(a,0,0,0,.26,.045,'dark_metal')
    rod(a,(0,0,.04),(0,0,1.75),.029,'steel')
    for z in (.59,.85,1.11,1.37):
        a.box((0,0,z),(.43,.12,.035),'steel')
        for x in (-.13,.13):
            for s in (-1,1):
                a.box((x,s*.095,z+.025),(.20,.025,.063),'black')
                for dx in (-.052,.052): a.box((x+dx,s*.113,z+.025),(.081,.008,.043),'navy')
    sign(a,0,0,1.63,.45,.23,'cream');script(a,0,-.027,1.68,.28,2,'dark_metal')


@prop('greeting_card_spinner_rack')
def card_spinner(a):
    disc(a,0,0,0,.28,.045,'dark_metal')
    rod(a,(0,0,.04),(0,0,1.75),.023,'steel')
    for ang in (0,pi/2,pi,3*pi/2):
        for row in range(4):
            z=.54+row*.27
            # Radial thin card pockets make four open faces of a spinner.
            cx=.20*cos(ang);cy=.20*sin(ang)
            a.box((cx,cy,z),(.31,.025,.22),'paper',rot=(0,0,ang+pi/2))
            a.box((cx*1.06,cy*1.06,z-.07),(.34,.02,.075),'metal',rot=(0,0,ang+pi/2))
    disc(a,0,0,1.73,.25,.025,'teal',8)


@prop('sidewalk_clearance_wire_bin')
def sale_bin(a):
    casters(a,.79,.58,.1,.06)
    for x in (-.42,.42):
        for y in (-.32,.32): rod(a,(x,y,.16),(x,y,.99),.016,'steel',6)
    for z in (.47,.68,.96):
        for y in (-.32,.32): rod(a,(-.42,y,z),(.42,y,z),.012,'steel',6)
        for x in (-.42,.42): rod(a,(x,-.32,z),(x,.32,z),.012,'steel',6)
    for x in (-.28,-.14,0,.14,.28):
        for y in (-.32,.32): rod(a,(x,y,.47),(x,y,.96),.008,'metal',5)
        rod(a,(x,-.32,.47),(x,.32,.47),.01,'metal',5)
    for x,y,z in ((-.21,.10,.57),(.15,-.13,.60),(.08,.15,.67)):
        a.box((x,y,z),(.35,.27,.13),('cream' if x<0 else 'navy'),rot=(0,.12,x))
    sign(a,0,-.34,.90,.34,.16,'cream')


@prop('farmers_market_scale_table')
def scale_table(a):
    serving_counter(a,.93,.60,.85,'wood')
    a.box((0,0,.91),(.40,.34,.085),'cream')
    a.box((0,.065,1.09),(.24,.15,.29),'steel')
    rod(a,(0,-.025,1.12),(0,-.07,1.12),.13,'white',12)
    rod(a,(0,-.075,1.12),(.06,-.075,1.17),.006,'black',4)
    disc(a,0,.02,1.25,.04,.04,'steel',8)
    a.box((0,.02,1.31),(.43,.35,.055),'steel')
    for x in (-.41,.41): crate(a,x,0,.87,.22,.40,.16)
    a.box((0,-.32,.58),(.68,.04,.21),'teal');script(a,0,-.345,.64,.43,2)


@prop('bulk_nut_dispenser_stand')
def bulk_nuts(a):
    legs(a,.97,.45,.91,'dark_metal')
    a.box((0,0,.92),(1.10,.56,.055),'wood_dark')
    for x in (-.34,0,.34):
        a.box((x,.05,1.32),(.27,.27,.59),'glass')
        a.box((x,.05,1.64),(.30,.30,.05),'dark_metal')
        a.cone((x,.05,1.11),(x,.05,.99),.135,'steel',8)
        a.box((x,-.11,1.07),(.16,.08,.10),'dark_metal')
        a.box((x,-.18,1.08),(.10,.035,.022),'steel')
        a.box((x,-.096,1.35),(.21,.02,.26),'sand')
        sign(a,x,-.126,1.48,.18,.085,'cream')
    a.box((0,-.23,.86),(1.09,.12,.065),'steel')


@prop('automated_ice_bag_vending_kiosk',size='large')
def ice_vender(a):
    cabinet(a,2.14,1.23,2.17,.08,'white')
    a.box((0,0,2.29),(2.31,1.36,.12),'blue')
    a.box((-.48,-.629,1.04),(.88,.045,.75),'dark_metal')
    a.box((-.48,-.66,.76),(.91,.16,.12),'steel')
    a.box((-.48,-.66,1.25),(.75,.07,.15),'metal',rot=(.20,0,0))
    framed_panel(a,.58,-.633,1.52,.49,.40,'navy');script(a,.58,-.66,1.64,.33,3)
    a.box((.58,-.658,1.19),(.26,.02,.045),'black')
    sign(a,-.30,-.636,1.89,1.08,.29,'blue');script(a,-.30,-.662,1.98,.71,3)
    grille(a,.48,-.64,.54,.70,.38,8)
    for x in (-.81,.81): a.box((x,-.641,.20),(.19,.025,.055),'yellow')


@prop('filtered_water_refill_station')
def water_station(a):
    cabinet(a,.88,.68,1.78,.06,'cream')
    a.box((0,-.357,1.02),(.59,.036,.76),'navy')
    a.box((0,-.48,.68),(.59,.28,.055),'steel')
    for x in (-.20,-.10,0,.10,.20): a.box((x,-.47,.711),(.025,.22,.015),'dark_metal')
    rod(a,(0,-.37,1.35),(0,-.46,1.35),.021,'steel',8)
    rod(a,(0,-.46,1.35),(0,-.46,1.27),.021,'steel',8)
    framed_panel(a,0,-.36,1.64,.54,.23,'teal')
    rod(a,(.31,-.36,1.25),(.31,-.39,1.25),.036,'blue',8)
    a.box((.29,-.363,1.43),(.12,.018,.028),'black')
    grille(a,0,-.36,.27,.65,.25,6)


@prop('sidewalk_photo_booth',size='large')
def photo_booth(a):
    a.box((0,0,.08),(1.29,1.37,.16),'dark_metal')
    a.box((-.54,0,1.10),(.15,1.20,2.08),'navy')
    a.box((.54,.08,1.10),(.15,1.04,2.08),'navy')
    a.box((0,.56,1.10),(1.08,.11,2.08),'dark_metal')
    a.box((0,0,2.15),(1.31,1.38,.13),'navy')
    for i in range(7): a.box((-.42+i*.14,-.54,1.26),(.145,.047,1.55),('brown' if i%2 else 'wood_dark'))
    sign(a,0,-.655,1.99,1.05,.25,'cream');script(a,0,-.681,2.05,.70,2,'navy')
    a.box((.553,-.528,.84),(.14,.06,.39),'steel')
    a.box((.553,-.566,.91),(.085,.015,.033),'black')
    a.box((.553,-.566,.73),(.095,.015,.063),'black')


@prop('farmers_market_canvas_stall',size='large')
def market_stall(a):
    for x in (-1.04,1.04):
        for y in (-.59,.59):
            rod(a,(x,y,0),(x,y,2.15),.025,'steel',8)
            a.box((x,y,.035),(.14,.14,.07),'dark_metal')
    for y in (-.59,.59): rod(a,(-1.04,y,2.08),(1.04,y,2.08),.023,'steel',8)
    awning(a,2.35,1.49,2.22,'cream')
    serving_counter(a,2.11,.72,.91,'wood')
    a.box((0,-.35,.51),(2.05,.027,.74),'cream')
    for x in (-.72,-.24,.24,.72): crate(a,x,.015,.95,.44,.52,.26)
    sign(a,0,-.385,.61,.71,.23,'teal');script(a,0,-.412,.68,.48,2)


@prop('sidewalk_magazine_ladder')
def magazine(a):
    for x in (-.26,.26):
        a.beam((x,-.22,0),(x,.22,1.55),.035,mat='steel')
        a.beam((x,.40,0),(x,.22,1.55),.035,mat='steel')
    for i in range(4):
        z=.34+i*.32;y=-.17+i*.09
        a.box((0,y,z),(.55,.16,.035),'dark_metal')
        a.box((0,y+.05,z+.15),(.50,.025,.29),'metal',rot=(.20,0,0))
        for x in (-.13,.13):
            a.box((x,y+.023,z+.15),(.23,.018,.27),('paper' if i%2 else 'cream'),rot=(.20,0,0))
            a.box((x,y-.003,z+.18),(.16,.009,.11),'navy',rot=(.20,0,0))
        rod(a,(-.26,y-.07,z+.075),(.26,y-.07,z+.075),.009,'steel',6)


@prop('giant_ice_cream_cone_shop_sign')
def cone_sign(a):
    disc(a,0,0,0,.34,.07,'dark_metal',12)
    a.cylinder((0,0,.07),(0,0,1.00),.09,'sand',10,radius2=.31)
    for i in range(10):
        t=2*pi*i/10
        rod(a,(.12*cos(t),.12*sin(t),.20),(.302*cos(t+.45),.302*sin(t+.45),.94),.009,'wood',5)
    a.sphere((0,0,1.17),.37,'cream',segments=12,rings=5,scale=(.38,.38,.34))
    a.sphere((-.025,.015,1.43),.25,'cream',segments=10,rings=4,scale=(.26,.26,.24))
    a.cone((-.025,.015,1.53),(.08,.015,1.80),.19,'cream',10)


@prop('freestanding_barber_pole_sign')
def barber(a):
    disc(a,0,0,0,.25,.05,'dark_metal',12)
    rod(a,(0,0,.05),(0,0,.50),.045,'steel',8)
    disc(a,0,0,.48,.18,.09,'steel',12)
    rod(a,(0,0,.57),(0,0,1.57),.14,'white',12)
    for j in range(7):
        z=.61+j*.135
        # Diagonal wide ribbon panels wrap faceted cylindrical globe.
        for i in range(8):
            t=i*pi/4;t2=(i+1)*pi/4
            vv=[(.142*cos(t),.142*sin(t),z),(.142*cos(t2),.142*sin(t2),z+.07),(.142*cos(t2),.142*sin(t2),z+.12),(.142*cos(t),.142*sin(t),z+.05)]
            a.mesh(vv,[(0,1,2,3)],'red' if j%2 else 'blue')
    disc(a,0,0,1.57,.18,.07,'steel',12)
    a.sphere((0,0,1.70),.14,'white',segments=10,rings=4)


@prop('restaurant_hostess_station')
def hostess(a):
    cabinet(a,.79,.55,.98,.05,'wood_dark')
    a.box((0,0,1.10),(.88,.64,.10),'wood',rot=(.13,0,0))
    a.box((0,-.33,1.08),(.86,.034,.075),'gold')
    sign(a,0,-.288,.74,.51,.18,'cream');script(a,0,-.315,.79,.32,2,'wood_dark')
    a.box((0,.02,1.174),(.34,.26,.017),'black',rot=(.13,0,0))
    a.box((0,.025,1.189),(.29,.21,.008),'paper',rot=(.13,0,0))
    disc(a,.29,-.17,1.18,.057,.03,'gold',10)
    a.sphere((.29,-.17,1.217),.045,'gold',segments=8,rings=3,scale=(.045,.045,.024))


@prop('restaurant_busser_service_cart')
def busser(a):
    casters(a,.67,.42,.10,.06)
    for x in (-.36,.36):
        for y in (-.24,.24): rod(a,(x,y,.17),(x,y,.97),.018,'steel',8)
    for z in (.25,.57,.89):
        a.box((0,0,z),(.78,.53,.035),'steel')
        for y in (-.25,.25): a.box((0,y,z+.04),(.79,.016,.08),'dark_metal')
        for x in (-.38,.38): a.box((x,0,z+.04),(.016,.51,.08),'dark_metal')
    a.tube([(-.36,.24,.92),(-.48,.24,1.08),(-.48,-.24,1.08),(-.36,-.24,.92)],.022,'steel',8)
    pan(a,.03,0,.93,.56,.38)
    for i in range(4): disc(a,-.16,0,.59+i*.016,.135,.013,'white',12)


@prop('outdoor_cafeteria_tray_return_station')
def tray_return(a):
    cabinet(a,1.04,.64,1.03,.05,'wood_dark')
    a.box((0,-.336,.75),(.70,.025,.31),'black')
    a.box((0,-.396,.63),(.75,.17,.055),'steel')
    for x in (-.35,.35):
        a.box((x,-.342,.29),(.32,.025,.37),'wood');handle(a,x,-.365,.39,.14)
    a.box((0,0,1.11),(1.13,.73,.065),'steel')
    a.box((0,0,1.16),(.76,.51,.035),'dark_metal')
    for i in range(4): a.box((0,0,1.18+i*.018),(.62,.42,.015),'brown')
    sign(a,0,.23,1.47,.75,.20,'cream')
    for x in (-.32,.32): rod(a,(x,.25,1.15),(x,.25,1.48),.014,'steel',6)


@prop('sidewalk_condiment_service_station')
def condiments(a):
    cabinet(a,.95,.57,.85,.06,'teal')
    a.box((0,0,.95),(1.06,.67,.055),'steel')
    for x in (-.37,-.12,.13):
        rod(a,(x,.08,.985),(x,.08,1.16),.062,('brown' if x<0 else 'cream'),8)
        rod(a,(x,.08,1.16),(x,.08,1.28),.012,'steel',6)
        rod(a,(x,.08,1.28),(x,-.015,1.28),.012,'steel',6)
    a.box((.36,.05,1.07),(.19,.26,.19),'steel')
    a.box((.36,-.09,1.10),(.13,.02,.075),'paper')
    for x in (-.27,.09): pan(a,x,-.21,.985,.28,.16)
    framed_panel(a,0,-.303,.50,.78,.57,'teal');handle(a,.26,-.329,.62,.12)


@prop('portable_commercial_handwash_sink')
def hand_sink(a):
    casters(a,.56,.47,.105,.07)
    cabinet(a,.70,.62,.81,.18,'steel')
    a.box((0,0,1.02),(.79,.71,.055),'steel')
    a.box((0,-.05,1.055),(.46,.39,.008),'dark_metal')
    for y in (-.27,.17): a.box((0,y,1.075),(.53,.022,.045),'silver')
    for x in (-.265,.265): a.box((x,-.05,1.075),(.022,.44,.045),'silver')
    a.tube([(0,.23,1.05),(0,.23,1.32),(0,.15,1.40),(0,-.02,1.40),(0,-.07,1.33)],.018,'steel',8)
    for x in (-.13,.13):
        rod(a,(x,.23,1.05),(x,.23,1.13),.017,'steel',6)
        a.box((x,.23,1.14),(.09,.025,.019),'dark_metal')
    a.box((0,-.333,.40),(.52,.02,.57),'metal');handle(a,.16,-.356,.56,.12)
    a.box((0,-.38,.20),(.22,.14,.045),'dark_metal')


@prop('commercial_barbecue_smoker_trailer_cart',size='large')
def smoker(a):
    legs(a,1.29,.67,.62,'dark_metal',r=.035)
    for y in (-.43,.43): wheel(a,.42,y,.24,.24)
    rod(a,(-.69,0,.98),(.60,0,.98),.35,'dark_metal',12)
    for x in (-.55,.47):
        a.torus((x,0,.98),.355,.014,'metal',axis='x',segments=12,sides=4)
    a.box((-.06,-.342,1.08),(.95,.032,.36),'dark_metal')
    handle(a,-.06,-.375,1.10,.37)
    rod(a,(-.57,.08,1.17),(-.57,.08,1.92),.055,'black',10)
    disc(a,-.57,.08,1.91,.091,.025,'metal',10)
    a.box((.91,0,.75),(.53,.57,.50),'dark_metal')
    framed_panel(a,.92,-.296,.76,.39,.34,'black');handle(a,.95,-.322,.83,.17)
    grille(a,.90,-.323,.64,.23,.10,3)
    a.box((-.04,-.55,.80),(1.17,.32,.045),'wood_dark')
    a.box((0,0,.24),(1.32,.64,.035),'metal')
    rod(a,(.18,-.352,1.20),(.18,-.388,1.20),.045,'cream',10)


@prop('commercial_rotisserie_display_cabinet')
def rotisserie(a):
    casters(a,.79,.57,.10,.07)
    cabinet(a,.98,.76,.50,.17,'steel')
    a.box((0,.345,1.20),(.98,.06,1.03),'dark_metal')
    for x in (-.46,.46): a.box((x,0,1.20),(.06,.70,1.03),'steel')
    a.box((0,0,1.74),(1.04,.80,.08),'steel')
    for z in (.89,1.18,1.47):
        rod(a,(-.43,0,z),(.43,0,z),.013,'steel',6)
        for x in (-.27,0,.27): a.sphere((x,0,z),.10,'brown',segments=8,rings=3,scale=(.10,.105,.085))
    # Hinged glazed service door rests open to reveal the three spits.
    a.box((.64,-.72,1.21),(.84,.018,.91),'glass',rot=(0,0,-pi/3))
    for z in (.77,1.65): a.box((.64,-.72,z),(.87,.030,.028),'steel',rot=(0,0,-pi/3))
    rod(a,(.43,-.36,.77),(.43,-.36,1.65),.018,'steel',6)
    rod(a,(.83,-1.04,1.10),(.83,-1.04,1.34),.014,'steel',6)
    for x in (-.29,0,.29): rod(a,(x,-.393,.53),(x,-.417,.53),.032,'black',8)
    grille(a,0,-.395,.30,.71,.17,4)
