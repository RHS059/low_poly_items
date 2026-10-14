"""Fifty original American residential yard and garden furnishings.

Muted, functional low-poly construction: open vessels, useful hardware,
structural supports and recognisable domestic proportions.  No vegetation.
"""
import math
from assetlib import Asset, register

M = 'dark_metal'
S = 'steel'
W = 'wood'
D = 'wood_dark'
K = 'black'


def item(slug, size='person'):
    def decorate(fn):
        def factory():
            a = Asset('b11_' + slug, 'residential_yard_garden', size)
            fn(a)
            return a.bottom_center()
        factory.__name__ = 'b11_' + slug
        register('b11_' + slug, 'residential_yard_garden', size, factory)
        return factory
    return decorate


def box(a, p, s, m=M, rot=None):
    a.box(p, s, mat=m, rot=rot)


def rod(a, p, q, r=.025, m=M, n=8, r2=None):
    a.cylinder(p, q, r, mat=m, sides=n, radius2=r2)


def beam(a, p, q, w=.05, d=None, m=W):
    a.beam(p, q, w, depth=d, mat=m)


def ring(a, p, r, t=.015, m=M, axis='z', n=12):
    a.torus(p, r, t, mat=m, axis=axis, segments=n, sides=4)


def disk(a, x, y, z, r, h=.025, m=M, n=12):
    rod(a, (x, y, z-h/2), (x, y, z+h/2), r, m, n)


def lathe(a, contours, m, n=12, x=0, y=0, caps=True):
    """A solid revolved profile; outer base upward, then inside downward."""
    vs = [(x+r*math.cos(i*math.tau/n), y+r*math.sin(i*math.tau/n), z)
          for r, z in contours for i in range(n)]
    fs = [(j*n+i, j*n+(i+1)%n, (j+1)*n+(i+1)%n, (j+1)*n+i)
          for j in range(len(contours)-1) for i in range(n)]
    if caps:
        fs += [tuple(reversed(range(n))), tuple(range((len(contours)-1)*n, len(contours)*n))]
    a.mesh(vs, fs, mat=m)


def legs(a, w, d, top, bottom=.02, material=M, thick=.045):
    for x in (-w/2, w/2):
        for y in (-d/2, d/2):
            box(a, (x, y, (bottom+top)/2), (thick, thick, top-bottom), material)
            box(a, (x, y, bottom), (thick+.018, thick+.018, .03), K)


def handle(a, x, y, z, w=.32, depth=.08, m=M):
    # Horizontal front-facing pull, with two actual mounting offsets.
    for dx in (-w/2, w/2):
        rod(a, (x+dx, y, z), (x+dx, y-depth, z), .017, m, 6)
    rod(a, (x-w/2, y-depth, z), (x+w/2, y-depth, z), .025, m)


def wheel(a, x, y, z, r=.12, width=.055, axis='y'):
    if axis == 'y':
        rod(a, (x, y-width/2, z), (x, y+width/2, z), r, 'rubber', 12)
        rod(a, (x, y-width*.55, z), (x, y+width*.55, z), r*.44, S, 8)
    else:
        rod(a, (x-width/2, y, z), (x+width/2, y, z), r, 'rubber', 12)
        rod(a, (x-width*.55, y, z), (x+width*.55, y, z), r*.44, S, 8)


def bolts(a, points, axis='z'):
    for x, y, z in points:
        if axis == 'z': rod(a, (x,y,z), (x,y,z+.009), .012, S, 6)
        else: rod(a, (x,y-.007,z), (x,y+.007,z), .012, S, 6)


def slats(a, w, d, z, count=7, m=W, y=0):
    for j in range(count):
        box(a, (0, y-d/2+(j+.5)*d/count, z), (w, d/count-.012, .035), m)


def gable(a, w, d, z, rise, m=D, over=.04):
    # Roof halves are thick sloping boards rather than zero-thickness faces.
    ang=math.atan2(rise, w/2)
    length=math.hypot(w/2, rise)+over
    for side in (-1, 1):
        box(a, (side*w/4, 0, z+rise/2), (length, d+2*over, .04), m,
            rot=(0, side*ang, 0))
    beam(a, (0,-d/2-over,z+rise+.022), (0,d/2+over,z+rise+.022), .04, .045, m)


@item('kettle_charcoal_grill')
def kettle(a):
    lathe(a, [(.16,.56),(.25,.64),(.31,.82),(.31,.86),(.28,.86),(.23,.68)], K, 16)
    lathe(a, [(.31,.875),(.29,.94),(.22,1.025),(.075,1.075)], 'dark_metal', 16)
    handle(a,0,-.12,1.065,.20,.025,S)
    for th in (0, math.tau/3, math.tau*2/3):
        x,y=.23*math.cos(th),.23*math.sin(th)
        rod(a,(x*1.4,y*1.4,.08),(x,y,.65),.021,S)
    wheel(a,-.16,.29,.12,.12);wheel(a,.16,.29,.12,.12)
    rod(a,(-.2,.29,.12),(.2,.29,.12),.02,S)
    disk(a,0,0,.38,.16,.025,S)
    disk(a,.12,0,1.059,.062,.009,S,8)
    for x,y in ((.10,0),(.13,-.02),(.14,.02)):
        disk(a,x,y,1.065,.009,.005,K,6)
    handle(a,0,-.285,.81,.27,.06,S)


@item('three_burner_gas_grill_cart')
def gasgrill(a):
    box(a,(0,0,.42),(.73,.51,.64),M)
    box(a,(0,-.265,.43),(.67,.018,.52),'steel')
    box(a,(0,-.28,.43),(.018,.012,.50),M)
    for x in (-.18,.18): handle(a,x,-.28,.56,.17,.035,M)
    box(a,(0,0,.79),(.85,.59,.10),S)
    box(a,(0,0,.96),(.77,.53,.25),M)
    box(a,(0,.01,1.10),(.68,.47,.055),M)
    handle(a,0,-.282,1.005,.50,.07,S)
    for x in (-.27,0,.27): rod(a,(x,-.31,.78),(x,-.35,.78),.036,K,8)
    for x in (-.60,.60):
        box(a,(x,0,.82),(.31,.51,.045),S)
        beam(a,(x,-.17,.80),(x*.64,-.17,.62),.025,.025,M)
    for x in (-.30,.30):
        for y in (-.20,.20): wheel(a,x,y,.065,.06,.035)
    rod(a,(.0,-.284,1.04),(.0,-.298,1.04),.035,'cream',12)
    box(a,(0,-.306,1.04),(.038,.008,.004),K,rot=(0,-.4,0))


@item('offset_barrel_smoker')
def offset(a):
    rod(a,(-.49,0,.91),(.45,0,.91),.27,M,12)
    rod(a,(.46,0,.75),(.84,0,.75),.185,K,10)
    rod(a,(-.37,.04,1.05),(-.37,.04,1.63),.047,K,8)
    disk(a,-.37,.04,1.65,.077,.025,K,8)
    handle(a,0,-.248,1.01,.38,.09,S)
    handle(a,.69,-.17,.80,.20,.075,S)
    for x in (-.36,.37):
        for y in (-.19,.19): beam(a,(x,y,.12),(x,y,.84),.045,.045,M)
    slats(a,.80,.37,.29,4,M)
    wheel(a,-.35,-.24,.15,.15);wheel(a,-.35,.24,.15,.15)
    rod(a,(-.35,-.28,.15),(-.35,.28,.15),.024,S)
    box(a,(.68,0,.94),(.31,.25,.024),M)
    rod(a,(.30,-.24,1.045),(.30,-.27,1.045),.027,'cream',10)


@item('ceramic_kamado_grill')
def kamado(a):
    lathe(a,[(.19,.35),(.27,.44),(.32,.72),(.31,.85)],'green',16)
    lathe(a,[(.31,.87),(.31,.91),(.27,1.09),(.15,1.20),(.06,1.23)],'green',16)
    ring(a,(0,0,.86),.315,.022,M, n=16)
    lathe(a,[(.058,1.22),(.068,1.25),(.068,1.29)],K,8)
    disk(a,0,0,1.31,.09,.025,M,8)
    handle(a,0,-.30,.91,.24,.09,W)
    box(a,(0,-.255,.48),(.16,.025,.10),M)
    box(a,(0,-.27,.48),(.065,.01,.055),S)
    for x in (-.25,.25):
        for y in (-.22,.22):
            beam(a,(x,y,.08),(x*.73,y*.73,.53),.035,.035,M)
            wheel(a,x,y,.063,.057,.035)
    for x in (-.46,.46):
        for y in (-.15,-.05,.05,.15): box(a,(x,y,.85),(.29,.085,.028),W)
        beam(a,(x,0,.83),(x*.60,0,.66),.025,.025,M)


@item('vertical_cabinet_smoker')
def cabinet_smoker(a):
    legs(a,.43,.40,.26)
    box(a,(0,0,.69),(.53,.47,.91),M)
    box(a,(0,-.245,.75),(.46,.023,.66),K)
    box(a,(0,-.246,.34),(.46,.025,.14),K)
    for z in (.5,1.0): box(a,(-.255,-.257,z),(.034,.038,.08),S)
    rod(a,(.17,-.278,.69),(.17,-.278,.89),.018,S,8)
    for z in (.69,.89):rod(a,(.17,-.23,z),(.17,-.278,z),.015,S,6)
    rod(a,(0,-.265,.97),(0,-.276,.97),.048,'cream',12)
    box(a,(0,-.282,.97),(.052,.01,.005),M,rot=(0,-.5,0))
    rod(a,(.12,.12,1.135),(.12,.12,1.24),.05,K,8)
    disk(a,.12,.12,1.25,.075,.02,M,8)
    for x in (-.14,-.07,0,.07,.14):box(a,(x,-.266,.32),(.04,.008,.009),'metal')
    handle(a,0,-.266,.39,.13,.035,S)


@item('pellet_grill_with_hopper')
def pellet(a):
    rod(a,(-.41,0,.98),(.38,0,.98),.245,M,12)
    legs(a,.62,.36,.90,thick=.042)
    box(a,(-.57,.015,.95),(.30,.39,.43),K)
    box(a,(-.57,.015,1.18),(.33,.42,.035),M)
    box(a,(-.58,-.192,.99),(.15,.012,.08),'metal')
    box(a,(-.61,-.202,1.0),(.058,.005,.034),'navy')
    rod(a,(-.54,-.207,.99),(-.54,-.227,.99),.02,K,8)
    handle(a,.02,-.225,1.07,.38,.08,S)
    rod(a,(.30,.07,1.06),(.30,.07,1.48),.045,K,8)
    a.cone((.30,.07,1.49),(.30,.07,1.54),.08,mat=M,sides=8)
    box(a,(.0,-.38,.89),(.73,.20,.035),W)
    slats(a,.65,.38,.29,4,M)
    wheel(a,.31,-.23,.115,.115);wheel(a,.31,.23,.115,.115)
    box(a,(.16,0,.63),(.12,.12,.17),S)


@item('brick_backyard_barbecue', 'large')
def brick_bbq(a):
    box(a,(0,0,.07),(1.6,.90,.14),'concrete')
    for x in (-.64,.64):
        box(a,(x,0,.64),(.21,.70,1.14),'brick')
        for z in (.23,.40,.57,.74,.91,1.08):box(a,(x,-.36,z),(.215,.007,.012),'sand')
    box(a,(0,.27,.74),(1.10,.18,.92),'brick')
    box(a,(0,0,.59),(1.14,.60,.12),'concrete')
    box(a,(0,0,.66),(.97,.47,.04),K)
    for x in (-.43,-.32,-.21,-.10,.01,.12,.23,.34,.45):rod(a,(x,-.25,.89),(x,.27,.89),.012,S,6)
    for y in (-.22,.23):rod(a,(-.50,y,.88),(.50,y,.88),.016,M,6)
    for x in (-.64,.64):box(a,(x,0,1.23),(.31,.83,.08),'concrete_light')
    box(a,(0,.30,1.23),(1.3,.28,.08),'concrete_light')
    slats(a,.95,.50,.26,4,D)


@item('cast_iron_hibachi', 'handheld')
def hibachi(a):
    for x in (-.25,.25):
        for y in (-.14,.14):box(a,(x,y,.07),(.048,.048,.14),M)
    a.prism([(-.34,-.22),(.34,-.22),(.27,-.15),(-.27,-.15)],.14,.25,K)
    box(a,(0,.18,.205),(.68,.065,.16),K)
    for x in (-.305,.305):box(a,(x,0,.205),(.065,.36,.16),K)
    box(a,(0,0,.14),(.61,.32,.065),M)
    for x in (-.24,-.18,-.12,-.06,0,.06,.12,.18,.24):rod(a,(x,-.18,.29),(x,.18,.29),.013,M,6)
    for x in (-.40,.40):
        rod(a,(x*.8,0,.20),(x,0,.20),.018,M,6)
        rod(a,(x,-.10,.20),(x,.10,.20),.023,W,8)
    for x in (-.16,.16):box(a,(x,-.239,.20),(.16,.012,.055),'metal')


@item('backyard_pizza_oven_cart')
def pizza(a):
    legs(a,.70,.57,.85,thick=.045)
    box(a,(0,0,.84),(.90,.78,.07),S)
    # Recessed black mouth between chamfered oven cheeks and roof.
    box(a,(0,.04,1.04),(.73,.60,.32),M)
    box(a,(0,-.271,1.00),(.49,.019,.19),K)
    box(a,(0,-.31,.906),(.61,.16,.034),'concrete_light')
    box(a,(0,.015,1.23),(.59,.58,.11),M)
    for x in (-.335,.335):box(a,(x,.015,1.178),(.14,.58,.095),M,rot=(0,x/.335*.65,0))
    rod(a,(.0,.17,1.23),(.0,.17,1.73),.062,S,10)
    disk(a,0,.17,1.75,.085,.025,M,10)
    slats(a,.67,.52,.28,4,M)
    for x in (-.35,.35):wheel(a,x,.29,.083,.078,.035)
    handle(a,0,-.32,1.11,.22,.045,S)
    box(a,(.43,0,.87),(.10,.65,.026),W)


@item('steel_fire_bowl')
def firebowl(a):
    lathe(a,[(.22,.21),(.37,.30),(.51,.43),(.50,.46),(.46,.44),(.32,.29),(.20,.26)],M,16)
    for th in (0,math.tau/3,math.tau*2/3):
        rod(a,(.40*math.cos(th),.40*math.sin(th),.025),(.25*math.cos(th),.25*math.sin(th),.26),.035,M,8)
    for x in (-.48,.48):
        ring(a,(x,0,.41),.07,.015,M,axis='x',n=8)
    for y in (-.15,-.05,.05,.15):rod(a,(-.25,y,.30),(.25,y,.30),.012,K,6)


@item('square_propane_fire_table')
def firetable(a):
    box(a,(0,0,.28),(.87,.87,.53),'concrete')
    box(a,(0,-.443,.27),(.56,.014,.37),'dark_metal')
    handle(a,.16,-.453,.39,.13,.025,S)
    for y in (-.49,.49):box(a,(0,y,.58),(1.13,.17,.09),'concrete_light')
    for x in (-.49,.49):box(a,(x,0,.58),(.17,.82,.09),'concrete_light')
    box(a,(0,0,.53),(.82,.82,.05),K)
    for x in (-.26,-.13,0,.13,.26):
        for y in (-.23,0,.23):a.sphere((x,y,.58),.056,'concrete',segments=5,rings=3,scale=(.066,.045,.032))
    ring(a,(0,0,.589),.22,.015,S,n=12)


@item('terracotta_chiminea')
def chiminea(a):
    # Broad belly and slender smoke neck, with a layered front mouth.
    lathe(a,[(.22,.02),(.28,.09),(.36,.30),(.34,.49),(.23,.68),(.13,.83),(.105,1.15),(.13,1.20)],'terracotta',12)
    box(a,(0,-.338,.36),(.28,.025,.22),K)
    for x in (-.16,.16):beam(a,(x,-.35,.24),(x*.8,-.34,.47),.035,.04,'brick')
    beam(a,(-.13,-.34,.47),(0,-.325,.53),.035,.04,'brick')
    beam(a,(0,-.325,.53),(.13,-.34,.47),.035,.04,'brick')
    box(a,(0,-.353,.24),(.36,.07,.045),'brick')
    disk(a,0,0,1.206,.094,.012,K,12)
    ring(a,(0,0,1.19),.123,.023,'terracotta')


@item('covered_firewood_rack')
def log_rack(a):
    for x in (-.63,.63):
        for y in (-.25,.25):box(a,(x,y,.71),(.05,.05,1.42),M)
        rod(a,(x,-.25,.15),(x,.25,.15),.028,M)
        rod(a,(x,-.25,1.10),(x,.25,1.10),.025,M)
    for y in (-.25,.25):box(a,(0,y,.15),(1.35,.045,.06),M)
    for x in (-.48,-.24,0,.24,.48):box(a,(x,0,.14),(.05,.50,.055),M)
    box(a,(0,0,1.40),(1.47,.69,.045),M,rot=(.10,0,0))
    # Several split logs make capacity and purpose readable.
    for x in (-.44,-.15,.14,.43):
        rod(a,(x,-.25,.28),(x,.23,.28),.11,D,7)
        rod(a,(x,-.261,.28),(x,-.252,.28),.093,'wood_light',7)
    for x in (-.29,0,.29):
        rod(a,(x,-.24,.46),(x,.23,.46),.10,D,6)
        rod(a,(x,-.25,.46),(x,-.242,.46),.083,'wood_light',6)


@item('wheeled_garden_hose_reel')
def hose_cart(a):
    for x in (-.26,.26):
        a.tube([(x,-.26,.03),(x,-.18,.51),(x,.22,.65),(x,.32,1.0)],.025,mat=M,sides=6)
        wheel(a,x,.23,.12,.12,.045,axis='x')
    rod(a,(-.26,.32,1.0),(.26,.32,1.0),.034,K)
    rod(a,(-.31,0,.57),(.31,0,.57),.038,S)
    for x in (-.18,.18):
        rod(a,(x-.015,0,.57),(x+.015,0,.57),.245,'green',12)
        ring(a,(x,0,.57),.217,.019,M,axis='x')
    for x in (-.125,-.075,-.025,.025,.075,.125):ring(a,(x,0,.57),.16,.024,'green',axis='x')
    rod(a,(.30,0,.57),(.30,0,.40),.018,S)
    rod(a,(.30,0,.40),(.41,0,.40),.027,K)
    a.tube([(-.1,-.15,.57),(-.1,-.28,.34),(-.08,-.32,.05),(.27,-.40,.05)],.024,mat='green',sides=6)
    rod(a,(.27,-.40,.05),(.39,-.40,.05),.027,'gold',8)


@item('wall_mounted_hose_reel')
def wall_reel(a):
    box(a,(0,.09,.30),(.34,.075,.53),M)
    for x in (-.13,.13):
        for z in (.075,.52):rod(a,(x,.048,z),(x,.035,z),.018,S,6)
    rod(a,(0,.04,.32),(0,-.17,.32),.035,S)
    for y in (-.10,-.32):
        rod(a,(0,y-.012,.32),(0,y+.012,.32),.25,'green',12)
        ring(a,(0,y,.32),.215,.018,M,axis='y')
    for y in (-.145,-.195,-.245):ring(a,(0,y,.32),.18,.024,'green',axis='y')
    rod(a,(0,-.365,.32),(.13,-.365,.32),.016,S)
    rod(a,(.13,-.365,.32),(.13,-.46,.32),.024,K)
    a.tube([(.15,-.18,.23),(.21,-.19,.10),(.25,-.25,.045)],.023,mat='green',sides=6)
    rod(a,(.25,-.25,.045),(.31,-.28,.045),.025,'gold',8)


@item('hose_saddle_with_coiled_hose')
def hose_saddle(a):
    box(a,(0,.08,.54),(.23,.045,.34),M)
    box(a,(0,-.03,.66),(.34,.23,.035),M)
    box(a,(0,-.15,.70),(.34,.035,.12),M)
    for z in (.43,.65):rod(a,(0,.055,z),(0,.04,z),.02,S,6)
    for y in (-.015,-.065,-.115):
        # Long oval loops are a common simple domestic hose storage form.
        pts=[(.19,y,.59),(.25,y,.48),(.25,y,.20),(.18,y,.08),(-.18,y,.08),(-.25,y,.20),(-.25,y,.48),(-.19,y,.59),(.19,y,.59)]
        a.tube(pts,.021,mat='green',sides=6)
    a.tube([(.18,-.12,.38),(.31,-.14,.24),(.31,-.18,.03)],.021,mat='green',sides=6)
    rod(a,(.31,-.18,.03),(.31,-.23,.07),.025,'gold',8)


@item('barrel_rainwater_collector')
def rainbarrel(a):
    lathe(a,[(.25,.02),(.30,.13),(.32,.51),(.30,.91),(.27,1.0)],'green',12)
    for z in (.15,.86):ring(a,(0,0,z),.304,.019,M)
    disk(a,0,0,1.01,.28,.035,M,12)
    disk(a,0,0,1.034,.13,.014,K,12)
    for x in (-.08,-.04,0,.04,.08):box(a,(x,0,1.043),(.008,.19,.006),S)
    rod(a,(0,-.29,.18),(0,-.39,.18),.024,'gold',8)
    rod(a,(0,-.39,.18),(0,-.39,.12),.023,'gold',8)
    rod(a,(-.05,-.34,.23),(.05,-.34,.23),.015,M,6)
    rod(a,(.22,.12,.90),(.38,.12,.90),.033,S,8)
    box(a,(0,0,.04),(.52,.52,.08),M)


@item('slim_wall_rainwater_tank')
def slim_tank(a):
    box(a,(0,0,.80),(.80,.33,1.60),'sand')
    for z in (.16,.40,.64,.88,1.12,1.36):box(a,(0,-.175,z),(.73,.035,.045),'cream')
    for x in (-.37,.37):box(a,(x,0,.80),(.08,.39,1.64),'sand')
    box(a,(0,0,1.62),(.76,.34,.045),'cream')
    disk(a,-.22,0,1.66,.082,.035,M,10)
    rod(a,(.18,-.18,.18),(.18,-.30,.18),.024,'gold',8)
    rod(a,(.18,-.30,.18),(.18,-.30,.12),.022,'gold',8)
    rod(a,(.13,-.25,.225),(.23,-.25,.225),.012,M,6)
    for x in (-.28,.28):box(a,(x,0,.04),(.23,.50,.08),'concrete')


@item('dual_chamber_compost_tumbler')
def compost_tumbler(a):
    for x in (-.58,.58):
        for y in (-.33,.33):beam(a,(x,y,.025),(x,0,.90),.04,.04,M)
        beam(a,(x,-.33,.055),(x,.33,.055),.04,.04,M)
    rod(a,(-.63,0,.91),(.63,0,.91),.035,S)
    for x in (-.265,.265):
        rod(a,(x-.23,0,.91),(x+.23,0,.91),.39,K,10)
        for y,z in ((-.375,.91),(-.30,1.14),(.30,1.14),(.375,.91)):
            box(a,(x,y,z),(.45,.038,.052),'dark_metal')
        box(a,(x,-.25,1.21),(.32,.18,.027),'green',rot=(.56,0,0))
        handle(a,x,-.29,1.235,.13,.027,S)
        for dz in (-.13,0,.13):box(a,(x,-.375,.91+dz),(.11,.012,.018),'metal')
    rod(a,(.64,0,.91),(.64,0,1.09),.018,S)
    rod(a,(.64,0,1.09),(.74,0,1.09),.025,K)


@item('cedar_compost_bin')
def compost_bin(a):
    for x in (-.5,.5):
        for y in (-.45,.45):box(a,(x,y,.56),(.075,.075,1.12),D)
    for z in (.14,.30,.46,.62,.78,.94):
        for x in (-.50,.50):box(a,(x,0,z),(.042,.94,.13),W)
        box(a,(0,.45,z),(1.02,.042,.13),W)
    for z in (.15,.33,.51):box(a,(0,-.47,z),(1.0,.045,.15),W)
    for x in (-.29,0,.29):box(a,(x,-.48,.40),(.045,.035,.62),D)
    for y in (-.33,-.20,-.07,.06,.19,.32):box(a,(0,y,1.15),(1.13,.10,.035),W)
    for x in (-.35,.35):box(a,(x,0,1.118),(.06,.91,.035),D)
    handle(a,0,-.26,1.19,.23,.015,M)


@item('glazed_garden_cold_frame')
def coldframe(a):
    # A sloped glazing lid atop an empty, open cedar planting frame.
    w,d=1.3,.86
    for y,z,h in ((-.43,.17,.34),(.43,.29,.58)):box(a,(0,y,z),(w,.045,h),W)
    for x in (-.64,.64):
        a.mesh([(x-.025,-.43,0),(x+.025,-.43,0),(x+.025,.43,0),(x-.025,.43,0),
                (x-.025,-.43,.34),(x+.025,-.43,.34),(x+.025,.43,.58),(x-.025,.43,.58)],
               [(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],W)
    angle=math.atan2(.24,.86)
    box(a,(0,0,.48),(1.23,.88,.019),'glass',rot=(angle,0,0))
    for x in (-.63,0,.63):beam(a,(x,-.46,.352),(x,.46,.61),.035,.04,D)
    for y,z in ((-.46,.352),(.46,.61)):box(a,(0,y,z),(1.31,.045,.04),D)
    handle(a,0,-.48,.38,.19,.024,M)
    for x in (-.38,.38):box(a,(x,.43,.607),(.12,.075,.014),S)


@item('elevated_cedar_garden_planter')
def elevated_planter(a):
    legs(a,1.14,.54,.90,material=D,thick=.065)
    for x in (-.57,.57):box(a,(x,0,.84),(.055,.60,.30),W)
    for y in (-.28,.28):
        for z in (.74,.87,.99):box(a,(0,y,z),(1.17,.043,.105),W)
    slats(a,1.10,.50,.70,5,D)
    for y in (-.31,.31):box(a,(0,y,1.054),(1.27,.085,.032),'wood_light')
    for x in (-.60,.60):box(a,(x,0,1.054),(.085,.55,.032),'wood_light')
    slats(a,1.10,.49,.25,4,W)
    for x in (-.53,.53):
        for z in (.77,.99):bolts(a,[(x,-.305,z)],'y')


@item('corrugated_steel_raised_bed')
def raised_bed(a):
    # Rounded-rectangle wall with corrugation bands and a genuinely empty center.
    pts=[]
    for cx,cy,base in ((.53,.23,0),(-.53,.23,math.pi/2),(-.53,-.23,math.pi),(.53,-.23,3*math.pi/2)):
        for j in range(4):
            th=base+j*math.pi/6
            pts.append((cx+.22*math.cos(th),cy+.22*math.sin(th)))
    n=len(pts)
    for layer in range(5):
        z0=.04+layer*.095; z1=z0+.09
        vs=[(x,y,z) for z in (z0,z1) for x,y in pts]
        fs=[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
        # Band is a thin closed wall; reverse inner side and join edge strips.
        inner=[(x*.965,y*.94,z) for z in (z0,z1) for x,y in pts]
        vs+=inner
        fs += [(2*n+i,3*n+i,3*n+(i+1)%n,2*n+(i+1)%n) for i in range(n)]
        fs += [(i,2*n+i,2*n+(i+1)%n,(i+1)%n) for i in range(n)]
        fs += [(n+i,n+(i+1)%n,3*n+(i+1)%n,3*n+i) for i in range(n)]
        a.mesh(vs,fs,'metal' if layer%2 else 'steel')
    for i in range(n):
        p=pts[i];q=pts[(i+1)%n]
        rod(a,(p[0],p[1],.522),(q[0],q[1],.522),.015,M,6)


@item('tiered_empty_planter_stand')
def planter_stand(a):
    for x in (-.38,.38):
        beam(a,(x,-.42,.03),(x,.27,1.08),.05,.05,D)
        beam(a,(x,.36,.03),(x,.27,1.08),.05,.05,D)
    for y,z in ((-.29,.27),(0,.62),(.24,.97)):
        box(a,(0,y,z),(.82,.24,.035),W)
        for yy in (y-.13,y+.13):box(a,(0,yy,z+.08),(.82,.026,.14),W)
        for x in (-.40,.40):box(a,(x,y,z+.08),(.03,.27,.14),W)
    beam(a,(-.38,.31,.42),(.38,.31,.42),.04,.05,D)


@item('half_whiskey_barrel_planter')
def barrel_planter(a):
    lathe(a,[(.25,.02),(.30,.18),(.33,.48),(.295,.50),(.27,.20),(.24,.07)],W,14)
    for z,r in ((.12,.289),(.40,.324)):
        ring(a,(0,0,z),r,.022,M,n=14)
    for i in range(14):
        th=i*math.tau/14
        rod(a,(.255*math.cos(th),.255*math.sin(th),.04),(.330*math.cos(th),.330*math.sin(th),.48),.007,D,4)
    disk(a,0,0,.078,.24,.016,D,14)


@item('tapered_square_patio_planter')
def square_planter(a):
    # Closed thickness and deep visible cavity, not a filled cube.
    rings=[(.20,.02),(.30,.74),(.267,.74),(.171,.09)]
    vs=[(s*x,s*y,z) for s,z in rings for x,y in ((-1,-1),(1,-1),(1,1),(-1,1))]
    fs=[(j*4+i,j*4+(i+1)%4,(j+1)*4+(i+1)%4,(j+1)*4+i) for j in range(3) for i in range(4)]
    fs += [(3,2,1,0),(12,13,14,15)]
    a.mesh(vs,fs,'concrete')
    for y in (-.296,.296):box(a,(0,y,.735),(.61,.04,.05),'concrete_light')
    for x in (-.296,.296):box(a,(x,0,.735),(.04,.55,.05),'concrete_light')
    for x in (-.15,.15):
        for y in (-.15,.15):box(a,(x,y,.017),(.075,.075,.033),K)


@item('window_flower_box_empty')
def window_box(a):
    box(a,(0,0,.13),(1.1,.29,.04),D)
    for y in (-.16,.16):
        for z in (.17,.27):box(a,(0,y,z),(1.18,.035,.085),W)
    for x in (-.57,.57):box(a,(x,0,.225),(.04,.31,.22),W)
    for x in (-.36,.36):
        beam(a,(x,.18,.02),(x,.18,.44),.035,.035,M)
        beam(a,(x,.18,.02),(x,-.17,.12),.028,.028,M)
        beam(a,(x,-.17,.12),(x,-.17,.24),.028,.028,M)
        rod(a,(x,.157,.40),(x,.144,.40),.016,S,6)
    for y in (-.17,.17):box(a,(0,y,.345),(1.23,.05,.028),'wood_light')


@item('hanging_wire_basket_empty', 'handheld')
def hanging_basket(a):
    lathe(a,[(.12,.01),(.22,.09),(.28,.24),(.26,.25),(.20,.115),(.115,.03)],'brown',8)
    for z,r in ((.03,.14),(.13,.245),(.25,.28)):ring(a,(0,0,z),r,.012,M,n=8)
    for i in range(6):
        th=i*math.tau/6
        beam(a,(.12*math.cos(th),.12*math.sin(th),.02),(.28*math.cos(th),.28*math.sin(th),.25),.012,.012,M)
    for th in (0,math.tau/3,math.tau*2/3):
        rod(a,(.27*math.cos(th),.27*math.sin(th),.25),(0,0,.84),.008,M,6)
    a.torus((0,0,.88),.048,.009,mat=M,axis='y',segments=8,sides=4,arc=math.pi*1.65)


@item('garden_potting_bench_with_sink')
def pottingbench(a):
    legs(a,1.16,.54,.92,material=D,thick=.065)
    slats(a,1.22,.55,.28,5,W)
    box(a,(-.29,0,.91),(.72,.65,.06),W)
    for y in (-.285,.285):box(a,(.38,y,.91),(.61,.08,.06),W)
    for x in (.13,.64):box(a,(x,0,.91),(.055,.50,.06),W)
    box(a,(.38,0,.765),(.43,.39,.035),S)
    for x in (.17,.59):box(a,(x,0,.83),(.025,.43,.17),S)
    for y in (-.21,.21):box(a,(.38,y,.83),(.43,.025,.17),S)
    disk(a,.38,0,.787,.027,.007,M,8)
    a.tube([(.38,.26,.94),(.38,.26,1.16),(.38,.16,1.20),(.38,.06,1.16)],.019,mat=S,sides=8)
    for x in (-.58,.58):box(a,(x,.28,1.20),(.055,.055,.58),D)
    for z in (1.06,1.21,1.36):box(a,(0,.30,z),(1.18,.025,.10),W)
    box(a,(0,.22,1.52),(1.32,.28,.04),W)
    for x in (-.40,-.18,.04):rod(a,(x,.25,1.37),(x,.17,1.37),.013,M,6)


@item('wire_tomato_cage')
def tomato_cage(a):
    for z,r in ((.43,.17),(.82,.23),(1.22,.30)):
        ring(a,(0,0,z),r,.009,'metal',n=12)
    for i in range(4):
        th=i*math.tau/4
        rod(a,(.10*math.cos(th),.10*math.sin(th),0),(.30*math.cos(th),.30*math.sin(th),1.28),.009,'metal',6)


@item('a_frame_cucumber_trellis')
def cucumber(a):
    for x in (-.45,.45):
        for side in (-1,1):beam(a,(x,side*.55,.01),(x,0,1.34),.04,.04,W)
    rod(a,(-.54,0,1.34),(.54,0,1.34),.021,M,8)
    for side in (-1,1):
        for z in (.23,.46,.69,.92,1.15):
            y=side*.55*(1-z/1.34)
            beam(a,(-.45,y,z),(.45,y,z),.026,.028,W)
        for x in (-.30,-.15,0,.15,.30):
            beam(a,(x,side*.52,.08),(x,side*.02,1.29),.018,.024,W)
    for x in (-.45,.45):rod(a,(x,-.37,.47),(x,.37,.47),.009,M,6)


@item('fan_climbing_trellis')
def fan_trellis(a):
    for i in range(7):
        x=(i-3)*.205
        beam(a,(x*.10,0,.02),(x,0,1.75-abs(i-3)*.06),.024,.031,W)
    for z,w in ((.63,.45),(1.12,.84),(1.57,1.15)):
        box(a,(0,-.026,z),(w,.028,.043),W)
    box(a,(0,.005,.13),(.07,.045,.26),D)
    for x in (-.31,0,.31):bolts(a,[(x,-.047,1.12)],'y')


@item('garden_obelisk_support')
def obelisk(a):
    for x in (-.31,.31):
        for y in (-.31,.31):beam(a,(x,y,.01),(x*.14,y*.14,1.86),.027,.027,M)
    for z in (.36,.81,1.25,1.61):
        r=.31*(1-z/2.16)
        for y in (-r,r):beam(a,(-r,y,z),(r,y,z),.019,.024,M)
        for x in (-r,r):beam(a,(x,-r,z),(x,r,z),.019,.024,M)
    a.sphere((0,0,1.90),.06,mat=M,segments=8,rings=3)
    a.cone((0,0,1.93),(0,0,2.02),.032,mat=M,sides=8)


@item('pedestal_bird_bath')
def birdbath(a):
    lathe(a,[(.26,.015),(.29,.07),(.20,.14),(.115,.24),(.085,.64),(.15,.73)],'concrete',12)
    lathe(a,[(.12,.71),(.28,.75),(.40,.84),(.39,.88),(.35,.865),(.25,.80),(.11,.79)],'concrete_light',16)
    disk(a,0,0,.800,.23,.012,'water',16)
    ring(a,(0,0,.865),.38,.024,'concrete_light',n=16)


@item('hanging_tube_seed_feeder', 'handheld')
def seed_feeder(a):
    rod(a,(0,0,.12),(0,0,.68),.085,'cream',10)
    for z in (.28,.51):
        rod(a,(0,-.088,z),(0,-.101,z),.031,M,8)
        rod(a,(-.16,-.065,z-.05),(.16,-.065,z-.05),.009,S,6)
        rod(a,(0,.088,z+.06),(0,.101,z+.06),.028,M,8)
        rod(a,(-.14,.065,z+.015),(.14,.065,z+.015),.009,S,6)
    disk(a,0,0,.095,.135,.022,'green',12)
    lathe(a,[(.12,.69),(.15,.705),(.10,.76),(.035,.79)],'green',12)
    a.torus((0,0,.835),.043,.007,mat=S,axis='y',segments=8,sides=4)
    for th in (0,math.pi/2,math.pi,math.pi*1.5):rod(a,(.086*math.cos(th),.086*math.sin(th),.14),(.086*math.cos(th),.086*math.sin(th),.67),.008,S,6)


@item('roofed_platform_bird_feeder')
def platform_feeder(a):
    box(a,(0,0,.81),(.075,.075,1.62),D)
    box(a,(0,0,1.54),(.57,.45,.04),W)
    for x in (-.27,.27):box(a,(x,0,1.59),(.032,.45,.09),W)
    for y in (-.21,.21):box(a,(0,y,1.59),(.52,.032,.09),W)
    for x in (-.23,.23):
        for y in (-.17,.17):box(a,(x,y,1.77),(.032,.032,.40),D)
    gable(a,.64,.52,1.96,.20,'green')
    for x in (-.12,.12):beam(a,(0,0,1.28),(x,0,1.53),.034,.034,D)
    box(a,(0,0,.04),(.27,.27,.08),'concrete')


@item('post_mounted_songbird_house')
def birdhouse(a):
    box(a,(0,0,.74),(.09,.09,1.48),D)
    box(a,(0,0,1.56),(.32,.29,.38),'wood_light')
    a.mesh([(-.16,-.145,1.75),(.16,-.145,1.75),(0,-.145,1.95),(-.16,.145,1.75),(.16,.145,1.75),(0,.145,1.95)],
           [(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],'wood_light')
    gable(a,.40,.37,1.76,.25,D,.02)
    rod(a,(0,-.151,1.67),(0,-.167,1.67),.052,K,12)
    ring(a,(0,-.168,1.67),.054,.008,D,axis='y')
    rod(a,(0,-.17,1.52),(0,-.30,1.52),.012,W,8)
    box(a,(0,0,1.355),(.38,.35,.035),D)
    box(a,(0,0,.035),(.20,.20,.07),'concrete')


@item('pole_mounted_bat_house')
def bat_house(a):
    box(a,(0,.05,1.12),(.085,.085,2.24),D)
    box(a,(0,0,2.06),(.42,.14,.65),D)
    box(a,(0,-.085,2.13),(.43,.03,.54),W)
    box(a,(0,-.065,2.415),(.49,.22,.045),M,rot=(.10,0,0))
    box(a,(0,-.084,1.79),(.36,.025,.18),D)
    for z in (1.73,1.77,1.81,1.85):box(a,(0,-.101,z),(.35,.009,.008),'wood_light')
    for x in (-.14,0,.14):box(a,(x,-.062,1.87),(.021,.065,.10),K)
    for x in (-.17,.17):bolts(a,[(x,-.108,2.30),(x,-.108,1.94)],'y')
    box(a,(0,.05,.045),(.24,.24,.09),'concrete')


@item('cedar_backyard_dog_house')
def doghouse(a):
    box(a,(0,0,.10),(.95,1.14,.20),D)
    for x in (-.43,.43):box(a,(x,0,.48),(.085,1.03,.67),W)
    box(a,(0,.48,.48),(.83,.08,.67),W)
    for x in (-.33,.33):box(a,(x,-.48,.46),(.22,.065,.65),W)
    box(a,(0,-.48,.76),(.45,.07,.16),W)
    a.mesh([(-.47,-.52,.80),(.47,-.52,.80),(0,-.52,1.16),(-.47,.52,.80),(.47,.52,.80),(0,.52,1.16)],
           [(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],W)
    gable(a,1.12,1.23,.81,.42,M,.025)
    for x in (-.225,.225):box(a,(x,-.526,.44),(.045,.032,.59),'wood_light')
    box(a,(0,-.526,.73),(.46,.032,.048),'wood_light')
    for z in (.25,.39,.53,.67):
        for x in (-.355,.355):box(a,(x,-.519,z),(.18,.009,.009),D)
        for x in (-.477,.477):box(a,(x,0,z),(.009,1.02,.009),D)


@item('raised_backyard_rabbit_hutch')
def rabbit_hutch(a):
    legs(a,1.14,.57,.72,material=D,thick=.06)
    box(a,(0,0,.65),(1.25,.66,.06),W)
    box(a,(0,.29,.99),(1.22,.05,.66),W)
    box(a,(.37,0,.99),(.48,.63,.66),W)
    for x in (-.59,.12):
        for y in (-.29,.29):box(a,(x,y,1.0),(.038,.038,.67),D)
    for z in (.69,1.28):box(a,(-.23,-.30,z),(.73,.045,.045),D)
    for x in (-.54,-.43,-.32,-.21,-.10,.01,.10):rod(a,(x,-.307,.72),(x,-.307,1.26),.005,'metal',4)
    for z in (.78,.88,.98,1.08,1.18):rod(a,(-.56,-.307,z),(.10,-.307,z),.005,'metal',4)
    box(a,(.37,-.331,1.0),(.37,.035,.52),'wood_light')
    box(a,(.21,-.356,1.0),(.07,.02,.025),M)
    box(a,(0,0,1.34),(1.41,.80,.055),M,rot=(-.08,0,0))
    box(a,(-.20,-.37,.63),(.64,.15,.038),S)
    box(a,(-.20,-.40,.62),(.20,.025,.025),M)


@item('adirondack_garden_chair')
def adirondack(a):
    # Broad flat arms, reclining back and low sloping seat.
    for x in (-.28,.28):
        box(a,(x,-.25,.29),(.06,.065,.58),D)
        beam(a,(x,.51,.035),(x,-.29,.39),.065,.09,W)
        beam(a,(x,.10,.38),(x,.40,1.04),.05,.06,D)
        box(a,(x,-.015,.61),(.16,.75,.055),W)
    for y in (-.27,-.16,-.05,.06,.17):
        box(a,(0,y,.385-(y+.27)*.15),(.59,.09,.035),W,rot=(-.14,0,0))
    for i in range(6):
        x=(i-2.5)*.092
        ztop=1.10-.16*abs(x)/.24
        beam(a,(x,.17,.40),(x,.44,ztop),.077,.036,W)
    beam(a,(-.27,.35,.84),(.27,.35,.84),.055,.06,D)
    for x in (-.28,.28):bolts(a,[(x,-.20,.643),(x,.22,.643)])


@item('woven_patio_armchair')
def woven_chair(a):
    legs(a,.48,.46,.47,thick=.035)
    box(a,(0,0,.43),(.58,.56,.09),D)
    box(a,(0,-.02,.50),(.53,.49,.09),'cream')
    box(a,(0,.265,.73),(.57,.065,.49),D,rot=(-.12,0,0))
    box(a,(0,.219,.75),(.48,.055,.33),'cream',rot=(-.12,0,0))
    for x in (-.285,.285):
        box(a,(x,-.015,.64),(.048,.53,.055),D)
        for y in (-.22,.20):box(a,(x,y,.55),(.038,.04,.22),D)
        for z in (.48,.54,.60):box(a,(x,0,z),(.032,.46,.014),'brown')
        for y in (-.15,-.05,.05,.15):box(a,(x,y,.55),(.035,.014,.20),'wood_light')
    for x in (-.20,-.10,0,.10,.20):box(a,(x,.307,.73),(.012,.013,.41),'wood_light',rot=(-.12,0,0))


@item('adjustable_patio_chaise')
def chaise(a):
    for x in (-.31,.31):
        beam(a,(x,-.81,.33),(x,.24,.33),.032,.045,M)
        beam(a,(x,.24,.33),(x,.77,.88),.032,.045,M)
        for y in (-.60,.15):beam(a,(x,y,.03),(x,y,.33),.035,.035,M)
        beam(a,(x,.23,.18),(x,.61,.68),.026,.026,M)
    for y in (-.75,-.59,-.43,-.27,-.11,.05,.21):box(a,(0,y,.355),(.62,.13,.029),'cream')
    for k in range(5):
        y=.31+k*.10;z=.405+k*.104
        box(a,(0,y,z),(.62,.123,.028),'cream',rot=(.80,0,0))
    for x in (-.31,.31):wheel(a,x,.34,.095,.085,.035,axis='x')
    box(a,(0,.66,.825),(.49,.22,.06),'sand',rot=(.8,0,0))


@item('round_patio_dining_table')
def round_table(a):
    disk(a,0,0,.75,.58,.05,M,16)
    disk(a,0,0,.78,.535,.013,'glass',16)
    ring(a,(0,0,.79),.552,.025,M,n=16)
    # Central umbrella grommet makes this clearly a patio dining table.
    disk(a,0,0,.793,.039,.014,K,10)
    ring(a,(0,0,.802),.039,.01,S,n=10)
    for th in (0,math.pi/2,math.pi,math.pi*1.5):
        x,y=math.cos(th),math.sin(th)
        beam(a,(x*.47,y*.47,.025),(x*.12,y*.12,.72),.038,.055,M)
    ring(a,(0,0,.30),.25,.020,M)


@item('rectangular_cedar_patio_table')
def rect_table(a):
    slats(a,1.55,.80,.76,7,W)
    for x in (-.63,.63):
        beam(a,(x,-.40,.03),(x,.20,.69),.075,.075,D)
        beam(a,(x,.40,.03),(x,-.20,.69),.075,.075,D)
        box(a,(x,0,.70),(.08,.71,.10),D)
    beam(a,(-.65,0,.31),(.65,0,.31),.075,.075,D)
    for x in (-.63,.63):
        for y in (-.29,.29):bolts(a,[(x,y,.785)])
    box(a,(0,0,.775),(.068,.068,.014),M)
    disk(a,0,0,.787,.022,.008,K,8)


@item('patio_cushioned_ottoman')
def ottoman(a):
    legs(a,.53,.45,.31,material=D,thick=.045)
    box(a,(0,0,.29),(.64,.55,.22),D)
    for z in (.20,.25,.30,.35):
        for y in (-.28,.28):box(a,(0,y,z),(.61,.014,.014),'brown')
        for x in (-.325,.325):box(a,(x,0,z),(.014,.54,.014),'brown')
    box(a,(0,0,.44),(.65,.56,.12),'sand')
    for y in (-.26,.26):box(a,(0,y,.46),(.61,.012,.013),'cream')
    for x in (-.30,.30):box(a,(x,0,.46),(.012,.52,.013),'cream')


@item('outdoor_deck_storage_box')
def storagebox(a):
    box(a,(0,0,.33),(1.22,.56,.59),'sand')
    for y in (-.29,.29):
        for z in (.12,.23,.34,.45,.56):box(a,(0,y,z),(1.16,.022,.082),'cream')
    for x in (-.59,.59):box(a,(x,-.308,.33),(.06,.021,.55),'sand')
    box(a,(0,0,.66),(1.29,.63,.065),'cream')
    for x in (-.42,.42):box(a,(x,.293,.64),(.10,.04,.035),M)
    box(a,(0,-.33,.56),(.14,.037,.053),M)
    box(a,(0,-.35,.56),(.088,.008,.023),K)
    for x in (-.58,.58):
        for y in (-.23,.23):box(a,(x,y,.032),(.10,.10,.064),M)


@item('backyard_porch_swing_frame', 'large')
def porch_swing(a):
    for x in (-1.1,1.1):
        for y in (-.71,.71):beam(a,(x,y,.03),(x,0,2.05),.075,.075,M)
        beam(a,(x,-.46,.73),(x,.46,.73),.045,.05,M)
    beam(a,(-1.21,0,2.07),(1.21,0,2.07),.095,.09,M)
    for x in (-.72,.72):
        for y in (-.25,.25):rod(a,(x,y,.65),(x,0,1.99),.009,S,6)
    slats(a,1.52,.55,.59,5,W)
    for z in (.78,.93,1.08):box(a,(0,.28,z),(1.52,.04,.115),W,rot=(-.10,0,0))
    for x in (-.73,.73):
        beam(a,(x,.24,.53),(x,.31,1.14),.045,.055,D)
        beam(a,(x,-.25,.53),(x,.29,.53),.045,.055,D)
        box(a,(x,-.02,.84),(.10,.62,.045),W)
        beam(a,(x,-.22,.60),(x,-.22,.84),.035,.045,D)
    for x in (-1.1,1.1):
        for y in (-.71,.71):box(a,(x,y,.04),(.18,.16,.08),K)


@item('freestanding_hammock_and_stand','large')
def hammock(a):
    for x in (-1.17,1.17):rod(a,(x,-.62,.07),(x,.62,.07),.055,M,8)
    rod(a,(-1.20,0,.12),(1.20,0,.12),.060,M,8)
    for side in (-1,1):
        rod(a,(side*.99,0,.12),(side*1.66,0,1.23),.055,M,8)
        rod(a,(side*1.66,0,1.23),(side*1.39,0,1.10),.011,S,6)
        rod(a,(side*1.24,-.43,.96),(side*1.24,.43,.96),.027,W,8)
        for y in (-.39,-.26,-.13,0,.13,.26,.39):rod(a,(side*1.39,0,1.10),(side*1.24,y,.96),.006,'cream',6)
    # Five broad cloth bands follow a catenary-like low-poly sag.
    xs=[-1.24,-.85,-.43,0,.43,.85,1.24]
    zs=[.96,.64,.46,.40,.46,.64,.96]
    for j in range(6):
        y0=-.42+j*.14;y1=y0+.135
        for k in range(6):
            a.mesh([(xs[k],y0,zs[k]),(xs[k+1],y0,zs[k+1]),(xs[k+1],y1,zs[k+1]),(xs[k],y1,zs[k])],[(0,1,2,3)],'cream' if j%2 else 'sand')
    for y in (-.425,.425):
        a.tube([(x,y,z+.007) for x,z in zip(xs,zs)],.010,mat='cream',sides=6)


@item('rotary_backyard_clothesline','large')
def rotary(a):
    rod(a,(0,0,.02),(0,0,2.12),.038,S,8)
    lathe(a,[(.075,.01),(.075,.11),(.042,.19)],'concrete',8)
    rod(a,(0,0,1.33),(0,0,1.52),.065,M,8)
    disk(a,0,0,2.0,.09,.065,M,8)
    endpoints=[]
    for th in (math.pi/4,3*math.pi/4,5*math.pi/4,7*math.pi/4):
        x,y=math.cos(th),math.sin(th)
        rod(a,(0,0,1.99),(x*1.35,y*1.35,2.04),.018,S,6)
        rod(a,(0,0,1.46),(x*.77,y*.77,2.02),.014,S,6)
        endpoints.append((x,y))
    for r in (.36,.63,.90,1.17,1.34):
        for i in range(4):
            p,q=endpoints[i],endpoints[(i+1)%4]
            rod(a,(p[0]*r,p[1]*r,2.01),(q[0]*r,q[1]*r,2.01),.0045,'cream',5)
    rod(a,(0,0,2.12),(0,0,2.16),.052,M,8)
