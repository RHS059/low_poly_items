"""Fifty purpose-built outdoor utility props for a midsized American city.

All dimensions are meters.  Every asset rests at z=0, with compact, readable
hardware and open grille construction rather than texture-dependent details.
"""
from math import cos, sin, pi, atan2
from assetlib import Asset, register

# Palette names are deliberately centralized for consistent utility finishes.
STEEL = 'steel'
DARK = 'dark_metal'
IRON = 'dark_metal'
RED = 'red'
YELLOW = 'yellow'
GREEN = 'green'
GRAY = 'metal'
CONCRETE = 'concrete'
WOOD = 'wood'
BLACK = 'black'
WHITE = 'white'
BLUE = 'blue'
BRASS = 'gold'
RUBBER = 'rubber'


def prop(name, category, size='person'):
    def wrap(builder):
        def factory():
            a = Asset('b05_' + name, category, size_class=size)
            builder(a)
            return a
        factory.__name__ = 'b05_' + name
        register(factory.__name__, category, size, factory)
        return factory
    return wrap


def tube(a, p, q, r, mat=STEEL, n=8):
    a.cylinder(p, q, r, mat=mat, sides=n)


def disc(a, x, y, z, r, thick=.025, mat=STEEL, n=12):
    tube(a, (x,y,z), (x,y,z+thick), r, mat, n)


def rod_path(a, points, r, mat=STEEL, n=8):
    for p,q in zip(points, points[1:]):
        tube(a,p,q,r,mat,n)


def bolts(a, z, radius, count=6, bolt=.018, mat=DARK, x=0, y=0):
    for i in range(count):
        t=2*pi*i/count
        disc(a,x+radius*cos(t),y+radius*sin(t),z,bolt,.024,mat,6)


def feet(a, x, y, z, sx, sy, mat=STEEL):
    for xx in (-sx/2,sx/2):
        for yy in (-sy/2,sy/2):
            a.box((x+xx,y+yy,z/2),(.11,.11,z),mat=mat)


def handle(a,x,y,z,width=.12,mat=STEEL):
    rod_path(a,[(x-width/2,y,z),(x-width/2,y-.04,z),(x+width/2,y-.04,z),(x+width/2,y,z)],.012,mat,6)


def grille(a,x,y,z,width,height,count=8,mat=DARK):
    # Recessed coil/plenum behind folded, pitched weather louvers.
    a.box((x,y+.034,z),(width,.018,height),mat=BLACK)
    for j in range(count):
        zz=z-height/2+height*(j+.5)/count
        a.box((x,y-.008,zz),(width,.046,min(.029,height/count*.56)),mat=mat,rot=(.42,0,0))


def panel(a,x,y,z,width,height,mat=GREEN):
    a.box((x,y+.010,z),(width+.015,.02,height+.016),mat=DARK)
    a.box((x,y-.009,z),(width-.013,.026,height-.014),mat=mat)
    handle(a,x+width*.31,y-.036,z)
    for zz in (z-height*.32,z+height*.32):
        a.box((x-width*.46,y-.028,zz),(.04,.018,.085),mat=STEEL)
        tube(a,(x-width*.465,y-.045,zz-.046),(x-width*.465,y-.045,zz+.046),.012,STEEL,6)
    tube(a,(x+width*.31,y-.043,z-.075),(x+width*.31,y-.052,z-.075),.015,DARK,6)


def flange(a,p,q,r,mat=STEEL):
    tube(a,p,q,r,mat,12)


def insulator(a,x,y,z,mat=WHITE):
    tube(a,(x,y,z),(x,y,z+.23),.042,STEEL)
    for zz in (z+.08,z+.135,z+.19):
        disc(a,x,y,zz,.088,.024,mat,10)


def fan_top(a,x,y,z,r,mat=DARK):
    # Recess, swept blades and a separate wire guard read as a working fan.
    disc(a,x,y,z-.060,r*.98,.012,BLACK,16)
    annulus(a,(x,y,z-.053),r,r*.91,.075,GRAY,16)
    for i in range(5):
        t=2*pi*i/5
        pts=[(.06,-.025),(.12,-.055),(r*.86,-.085),(r*.92,.015),(.13,.075),(.055,.030)]
        a.prism([(x+u*cos(t)-v*sin(t),y+u*sin(t)+v*cos(t)) for u,v in pts],z-.023,z-.013,STEEL)
    disc(a,x,y,z-.022,.070,.054,GRAY,10)
    for i in range(8):
        t=i*pi/4
        tube(a,(x+.065*cos(t),y+.065*sin(t),z+.048),(x+(r-.015)*cos(t),y+(r-.015)*sin(t),z+.048),.007,mat,4)
    for rr in (r*.45,r*.7,r*.94):
        a.torus((x,y,z+.045),rr,.007,mat=mat,segments=16,sides=4)


def annulus(a, center, outer, inner, depth, mat=STEEL, n=16, axis='z'):
    x,y,z=center
    def point(r,t,d):
        return (x+r*cos(t),y+d,z+r*sin(t)) if axis=='y' else (x+r*cos(t),y+r*sin(t),z+d)
    vs=[point(r,2*pi*i/n,d) for d,r in ((0,outer),(depth,outer),(0,inner),(depth,inner)) for i in range(n)]
    fs=[]
    for i in range(n):
        j=(i+1)%n
        fs.extend(((i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)))
    a.mesh(vs,fs,mat)


def formed_round(a, rings, mat=GRAY, n=16, center=(0,0)):
    # Open-ended sheet-metal surface; rings are (height, radius).
    x,y=center
    vs=[(x+r*cos(2*pi*i/n),y+r*sin(2*pi*i/n),z) for z,r in rings for i in range(n)]
    fs=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(rings)-1) for i in range(n)]
    a.mesh(vs,fs,mat)


def grate_surround(a,w,d,h,thick=.065):
    # Cast curb around a visible recess, no full-height solid hidden below slots.
    a.box((0,0,.02),(w,d,.04),mat=BLACK)
    for x in (-w/2+thick/2,w/2-thick/2):
        a.box((x,0,h/2),(thick,d,h),mat=CONCRETE)
    for y in (-d/2+thick/2,d/2-thick/2):
        a.box((0,y,h/2),(w-2*thick,thick,h),mat=CONCRETE)


def aperture_panel(a,center,bounds,r,z0,z1,mat=GRAY,axis='z'):
    # A rectangular sheet with a real circular hole, including its inside wall.
    cx,cy=center;x0,x1,y0,y1=bounds
    angles=sorted(set([i*2*pi/16 for i in range(16)]+[atan2(y-cy,x-cx)%(2*pi) for x in (x0,x1) for y in (y0,y1)]))
    inner=[];outer=[]
    for t in angles:
        dx,dy=cos(t),sin(t)
        tx=((x1-cx) if dx>0 else (x0-cx))/dx if abs(dx)>1e-10 else 1e9
        ty=((y1-cy) if dy>0 else (y0-cy))/dy if abs(dy)>1e-10 else 1e9
        length=min(tx,ty)
        inner.append((cx+r*dx,cy+r*dy));outer.append((cx+length*dx,cy+length*dy))
    def point(p,z):return (p[0],z,p[1]) if axis=='y' else (p[0],p[1],z)
    vs=[point(p,z) for z,ring in ((z0,outer),(z1,outer),(z0,inner),(z1,inner)) for p in ring]
    n=len(angles);fs=[]
    for i in range(n):
        j=(i+1)%n
        fs.extend(((i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)))
    a.mesh(vs,fs,mat)


def coil_face(a,x,y,z,w,h,mat=DARK):
    grille(a,x,y,z,w,h,12,mat)
    for xx in (x-w/2-.016,x+w/2+.016):
        a.box((xx,y-.021,z),(.028,.046,h+.045),mat=GRAY)


def safety_plate(a,x,y,z,w=.11,h=.10):
    a.box((x,y,z),(w,.006,h),mat=YELLOW)
    a.box((x,y-.005,z+.015),(.014,.006,h*.43),mat=BLACK)
    a.box((x,y-.005,z-h*.29),(.017,.006,.015),mat=BLACK)


@prop('classic_fire_hydrant','utilities_fire_water')
def classic_hydrant(a):
    disc(a,0,0,0,.24,.07,IRON)
    disc(a,0,0,.07,.17,.06,RED)
    tube(a,(0,0,.13),(0,0,.74),.132,RED,10)
    disc(a,0,0,.29,.17,.045,RED)
    bolts(a,.34,.139,6,.018)
    disc(a,0,0,.76,.175,.045,RED)
    a.sphere((0,0,.81),.17,mat=RED,segments=10,rings=4)
    disc(a,0,0,.96,.042,.04,IRON,5)
    for sign in (-1,1):
        tube(a,(sign*.08,0,.62),(sign*.27,0,.62),.074,RED)
        tube(a,(sign*.27,0,.62),(sign*.31,0,.62),.088,IRON,8)
        tube(a,(sign*.31,0,.62),(sign*.34,0,.62),.027,STEEL,5)
    tube(a,(0,-.09,.54),(0,-.235,.54),.10,RED)
    tube(a,(0,-.235,.54),(0,-.275,.54),.115,IRON,10)
    tube(a,(0,-.275,.54),(0,-.30,.54),.034,STEEL,5)
    rod_path(a,[(-.28,-.03,.57),(-.23,-.12,.43),(-.08,-.19,.42),(0,-.23,.48)],.009,DARK,5)


@prop('breakaway_barrel_hydrant','utilities_fire_water')
def breakaway_hydrant(a):
    disc(a,0,0,0,.20,.07,STEEL)
    tube(a,(0,0,.07),(0,0,.91),.112,YELLOW,10)
    for z in (.17,.42,.91):
        disc(a,0,0,z,.147,.04,YELLOW)
    bolts(a,.22,.129,8,.016)
    disc(a,0,0,.95,.14,.07,STEEL,10)
    a.sphere((0,0,1.01),.112,mat=STEEL,segments=10,rings=3)
    disc(a,0,0,1.11,.035,.04,BRASS,5)
    for sign in (-1,1):
        tube(a,(0,0,.80),(sign*.24,0,.80),.065,YELLOW)
        tube(a,(sign*.24,0,.80),(sign*.29,0,.80),.085,STEEL)
    tube(a,(0,-.08,.61),(0,-.24,.61),.095,YELLOW)
    tube(a,(0,-.24,.61),(0,-.28,.61),.11,STEEL,10)
    a.box((0,.14,.35),(.10,.025,.13),mat=WHITE)
    tube(a,(.105,.03,1.02),(.105,.03,1.63),.008,STEEL,5)
    a.box((.105,.03,1.60),(.08,.016,.13),mat=BLUE)


@prop('siamese_fire_department_connection','utilities_fire_water')
def fire_connection(a):
    disc(a,0,0,0,.15,.045,STEEL)
    tube(a,(0,0,.03),(0,0,.72),.075,RED)
    tube(a,(-.23,0,.72),(.23,0,.72),.07,RED)
    for x in (-.23,.23):
        tube(a,(x,0,.72),(x,-.17,.77),.061,BRASS)
        tube(a,(x,-.17,.77),(x,-.205,.78),.082,BRASS,10)
        a.box((x,-.22,.78),(.13,.02,.025),mat=STEEL)
        rod_path(a,[(x,-.20,.71),(x,-.20,.55),(x*.55,-.12,.55),(x*.4,-.06,.67)],.008,DARK,5)
    a.box((0,-.082,.49),(.20,.02,.10),mat=WHITE)


@prop('post_indicator_valve','utilities_fire_water')
def indicator_valve(a):
    disc(a,0,0,0,.16,.06,IRON)
    tube(a,(0,0,.06),(0,0,.93),.075,RED)
    a.box((0,0,.74),(.18,.15,.28),mat=RED)
    a.box((0,-.083,.78),(.115,.015,.067),mat=BLACK)
    a.box((0,-.094,.78),(.085,.007,.036),mat=WHITE)
    disc(a,0,0,.99,.10,.04,RED)
    tube(a,(0,0,1.03),(0,0,1.10),.025,STEEL,6)
    a.box((.11,0,1.1),(.30,.045,.035),mat=STEEL)
    a.box((.22,0,1.13),(.035,.045,.10),mat=STEEL)
    tube(a,(-.13,.045,.25),(-.13,.045,.96),.021,DARK,6)


@prop('backflow_preventer_assembly','utilities_fire_water','large')
def backflow(a):
    for x in (-.6,.6):
        a.box((x,0,.08),(.32,.36,.16),mat=CONCRETE)
        tube(a,(x,0,.16),(x,0,.88),.075,BLUE)
        disc(a,x,0,.31,.12,.05,STEEL)
    tube(a,(-.6,0,.88),(.6,0,.88),.087,BLUE)
    for x in (-.38,.38):
        tube(a,(x-.06,0,.88),(x+.06,0,.88),.14,STEEL,10)
        tube(a,(x,0,.9),(x,0,1.12),.024,BRASS)
        a.torus((x,0,1.16),.13,.015,mat=RED,segments=10,sides=5)
        for ang in (0,pi/2):
            tube(a,(x-.12*cos(ang),-.12*sin(ang),1.16),(x+.12*cos(ang),.12*sin(ang),1.16),.012,RED,5)
    a.box((0,0,.86),(.40,.23,.23),mat=BLUE)
    disc(a,0,0,.975,.12,.05,STEEL)
    tube(a,(0,-.06,.80),(0,-.06,.56),.045,BRASS)
    tube(a,(0,-.06,.56),(0,-.2,.51),.05,BRASS)
    tube(a,(.13,-.08,.95),(.13,-.18,1.07),.013,BRASS,6)
    tube(a,(.13,-.18,1.07),(.13,-.205,1.07),.05,WHITE,12)


@prop('wall_fire_hose_connection','utilities_fire_water')
def wall_connection(a):
    a.box((0,.04,.30),(.64,.08,.60),mat=CONCRETE)
    a.box((0,-.015,.35),(.50,.035,.18),mat=RED)
    for x in (-.17,0,.17):
        tube(a,(x,-.04,.27),(x,-.17,.20),.05,BRASS)
        tube(a,(x,-.17,.20),(x,-.205,.18),.067,BRASS,10)
        tube(a,(x-.055,-.22,.18),(x+.055,-.22,.18),.012,STEEL,6)
    a.box((0,-.04,.50),(.36,.025,.055),mat=WHITE)


@prop('padmount_transformer','utilities_electrical','large')
def pad_transformer(a):
    a.box((0,0,.10),(1.70,1.38,.20),mat=CONCRETE)
    a.box((0,.08,.71),(1.38,1.04,1.02),mat=GREEN)
    a.box((0,.08,1.24),(1.45,1.12,.085),mat=GREEN)
    for x in (-.35,.35):
        panel(a,x,-.455,.74,.66,.90)
    a.box((0,-.489,.76),(.03,.025,.96),mat=DARK)
    safety_plate(a,-.36,-.485,.98,.14,.14)
    for x in (-.58,.58):
        a.box((x,.07,1.30),(.08,.22,.09),mat=STEEL)
    for y in (-.15,.02,.19,.36):
        a.box((.711,y,.70),(.06,.09,.72),mat=GREEN)


@prop('polemount_transformer_can','utilities_electrical')
def pole_transformer(a):
    disc(a,0,0,.04,.30,.75,GRAY,12)
    disc(a,0,0,.0,.32,.045,STEEL,12)
    disc(a,0,0,.79,.33,.045,GRAY,12)
    for z in (.20,.66):
        a.box((0,.31,z),(.42,.10,.08),mat=STEEL)
        a.box((0,.40,z),(.12,.14,.12),mat=STEEL)
    insulator(a,-.13,0,.83)
    insulator(a,.13,0,.83)
    for z in (.28,.43,.58):
        tube(a,(-.30,0,z),(-.39,0,z),.032,BLACK)
        tube(a,(-.39,0,z),(-.42,0,z),.043,WHITE)
    safety_plate(a,0,-.303,.52,.12,.15)


@prop('three_phase_transformer_rack','utilities_electrical','large')
def transformer_rack(a):
    for x in (-.95,.95):
        a.box((x,0,.10),(.35,.64,.20),mat=CONCRETE)
        a.box((x,0,.78),(.11,.11,1.35),mat=STEEL)
    for z in (.40,1.00):
        a.box((0,0,z),(2.15,.17,.12),mat=STEEL)
    for x in (-.64,0,.64):
        disc(a,x,-.10,.52,.25,.69,GRAY,12)
        disc(a,x,-.10,1.21,.275,.045,STEEL,12)
        insulator(a,x-.09,-.10,1.255)
        insulator(a,x+.09,-.10,1.255)
        for z in (.70,.87):
            tube(a,(x,-.33,z),(x,-.42,z),.025,BLACK,6)
        safety_plate(a,x,-.355,1.02,.09,.10)
    for x in (-.64,0):
        rod_path(a,[(x+.09,-.10,1.47),(x+.28,-.10,1.64),(x+.55,-.10,1.47)],.012,DARK,6)


@prop('streetlight_control_cabinet','utilities_electrical')
def streetlight_cabinet(a):
    a.box((0,0,.09),(.66,.48,.18),mat=CONCRETE)
    a.box((0,0,.66),(.52,.35,1.02),mat=GRAY)
    a.box((0,0,1.20),(.58,.41,.07),mat=STEEL)
    panel(a,0,-.19,.69,.46,.91,GRAY)
    grille(a,0,-.218,.40,.34,.18,5,STEEL)
    disc(a,0,0,1.245,.045,.06,BLACK,8)
    a.sphere((0,0,1.31),.05,mat=BLUE,segments=8,rings=3)
    safety_plate(a,0,-.218,.93)
    for x in (-.16,.16):
        tube(a,(x,.08,.18),(x,.08,.02),.025,STEEL)


@prop('traffic_signal_controller_cabinet','utilities_electrical','large')
def signal_controller(a):
    a.box((0,0,.14),(1.0,.78,.28),mat=CONCRETE)
    a.box((0,0,.98),(.88,.66,1.40),mat=STEEL)
    a.box((0,0,1.72),(.96,.75,.08),mat=GRAY)
    panel(a,0,-.35,.98,.80,1.30,GRAY)
    grille(a,-.18,-.379,.55,.30,.23,6,STEEL)
    a.box((.15,-.38,1.13),(.025,.035,.22),mat=DARK)
    a.box((.17,-.399,1.08),(.035,.025,.035),mat=BLACK)
    a.box((0,-.377,1.49),(.24,.012,.06),mat=WHITE)
    for z in (.48,1.43):
        a.box((-.415,-.366,z),(.035,.043,.10),mat=STEEL)
    for y in (-.20,.20):
        a.box((.455,y,.85),(.025,.12,.035),mat=DARK)


@prop('telephone_distribution_pedestal','utilities_electrical')
def telecom_pedestal(a):
    a.box((0,0,.055),(.36,.30,.11),mat=CONCRETE)
    a.box((0,0,.51),(.24,.22,.93),mat=GREEN)
    a.box((0,0,1.0),(.29,.265,.08),mat=GREEN)
    a.box((0,-.115,.56),(.20,.015,.76),mat=GREEN)
    a.box((0,-.13,.78),(.08,.014,.045),mat=WHITE)
    tube(a,(0,-.137,.35),(0,-.149,.35),.018,STEEL,6)
    for z in (.86,.91):
        a.box((0,-.135,z),(.13,.018,.015),mat=DARK)


@prop('fiber_distribution_cabinet','utilities_electrical')
def fiber_cabinet(a):
    a.box((0,0,.11),(.85,.60,.22),mat=CONCRETE)
    a.box((0,0,.79),(.73,.48,1.14),mat=GREEN)
    a.box((0,0,1.40),(.82,.56,.09),mat=GREEN)
    panel(a,0,-.263,.80,.65,1.02,GREEN)
    a.box((.22,-.293,.79),(.045,.025,.22),mat=BLACK)
    a.box((0,-.291,1.19),(.19,.008,.055),mat=WHITE)
    for x in (-.20,.20):
        a.box((x,0,.24),(.08,.32,.06),mat=DARK)
    for z in (.65,.76,.87):
        a.box((.38,0,z),(.025,.24,.035),mat=STEEL)


@prop('coax_cable_junction_pedestal','utilities_electrical')
def cable_pedestal(a):
    disc(a,0,0,0,.20,.07,CONCRETE,8)
    disc(a,0,0,.05,.145,.74,GREEN,8)
    disc(a,0,0,.79,.16,.055,GREEN,8)
    a.sphere((0,0,.83),.145,mat=GREEN,segments=8,rings=3)
    a.box((0,-.143,.46),(.105,.017,.27),mat=GREEN)
    tube(a,(0,-.155,.34),(0,-.175,.34),.018,STEEL,6)
    a.box((0,-.15,.65),(.09,.012,.04),mat=WHITE)


@prop('four_meter_service_bank','utilities_electrical','large')
def meter_bank(a):
    for x in (-.56,.56):
        a.box((x,0,.70),(.06,.06,1.40),mat=STEEL)
        a.box((x,0,.035),(.25,.25,.07),mat=CONCRETE)
    a.box((0,0,.80),(1.30,.22,.98),mat=GRAY)
    for x in (-.46,-.15,.15,.46):
        tube(a,(x,-.125,1.03),(x,-.195,1.03),.115,STEEL,12)
        tube(a,(x,-.195,1.03),(x,-.21,1.03),.096,WHITE,12)
        a.box((x,-.225,1.04),(.095,.018,.035),mat=BLACK)
        a.box((x,-.13,.67),(.22,.045,.27),mat=GRAY)
        a.box((x+.057,-.16,.66),(.025,.025,.09),mat=BLACK)
        tube(a,(x,.02,.31),(x,.02,.10),.025,STEEL)
    a.box((0,0,1.33),(1.36,.28,.06),mat=STEEL)


@prop('outdoor_fused_disconnect','utilities_electrical')
def disconnect(a):
    a.box((0,.06,.63),(.075,.08,1.26),mat=STEEL)
    a.box((0,0,.73),(.40,.25,.68),mat=GRAY)
    panel(a,0,-.143,.73,.35,.60,GRAY)
    a.box((.232,-.02,.88),(.055,.08,.15),mat=BLACK)
    tube(a,(.23,-.02,.91),(.23,-.02,1.04),.018,RED,6)
    a.box((0,0,1.09),(.46,.31,.045),mat=STEEL)
    safety_plate(a,0,-.171,.87)
    tube(a,(-.09,.02,.39),(-.09,.02,.05),.022,STEEL)
    tube(a,(.09,.02,.39),(.09,.02,.05),.022,STEEL)
    a.box((0,.07,.025),(.30,.30,.05),mat=CONCRETE)


@prop('utility_meter_pedestal','utilities_electrical')
def meter_pedestal(a):
    a.box((0,0,.08),(.44,.38,.16),mat=CONCRETE)
    a.box((0,0,.73),(.28,.22,1.22),mat=GRAY)
    a.box((0,0,1.15),(.38,.27,.49),mat=GRAY)
    tube(a,(0,-.145,1.20),(0,-.22,1.20),.125,STEEL,12)
    tube(a,(0,-.22,1.20),(0,-.233,1.20),.108,WHITE,12)
    a.box((0,-.245,1.22),(.12,.008,.039),mat=BLACK)
    a.box((0,-.132,.67),(.21,.025,.34),mat=GRAY)
    a.box((.06,-.152,.67),(.02,.025,.09),mat=BLACK)
    a.box((0,0,1.42),(.43,.31,.05),mat=STEEL)


@prop('generator_transfer_switch','utilities_electrical')
def transfer_switch(a):
    feet(a,0,0,.25,.48,.28)
    a.box((0,0,.68),(.65,.42,.88),mat=GRAY)
    a.box((0,0,1.15),(.72,.49,.07),mat=STEEL)
    panel(a,0,-.23,.71,.58,.77,GRAY)
    a.box((-.14,-.254,.84),(.16,.024,.11),mat=BLACK)
    a.box((-.14,-.27,.85),(.12,.01,.06),mat=BLUE)
    tube(a,(.11,-.252,.85),(.11,-.284,.85),.047,BLACK,10)
    a.box((.11,-.294,.86),(.022,.025,.072),mat=RED)
    grille(a,-.04,-.255,.49,.34,.14,4,STEEL)
    safety_plate(a,.17,-.258,.53,.09,.11)
    for x in (-.16,.16):
        tube(a,(x,.05,.24),(x,.05,.01),.035,DARK)


@prop('wood_distribution_power_pole','utilities_poles','large')
def wood_pole(a):
    a.cylinder((0,0,0),(0,0,7.8),.16,WOOD,10,radius2=.10)
    a.box((0,0,7.15),(2.45,.13,.17),mat=WOOD)
    for x in (-1.0,0,1.0):
        insulator(a,x,0,7.25)
    for x in (-.9,.9):
        tube(a,(0,.02,6.55),(x,.02,7.11),.027,STEEL,6)
    for z in (1.8,2.25,2.7,3.15,3.6):
        tube(a,(-.14,0,z),(-.31,0,z),.016,STEEL,6)
    a.box((0,-.147,1.5),(.10,.015,.25),mat=YELLOW)
    tube(a,(.145,0,.08),(.145,0,6.3),.019,DARK,6)


@prop('concrete_utility_pole','utilities_poles','large')
def concrete_pole(a):
    a.cylinder((0,0,0),(0,0,7.4),.20,CONCRETE,8,radius2=.115)
    for z in (6.5,7.1):
        a.box((0,0,z),(1.70,.12,.12),mat=STEEL)
        for x in (-.67,.67):
            insulator(a,x,0,z+.07)
    for z in (.55,1.2,1.85,2.5,3.15,3.8,4.45,5.1):
        a.box((0,-.162,z),(.055,.009,.07),mat=DARK)
    a.box((0,-.176,1.45),(.11,.025,.14),mat=WHITE)
    disc(a,0,0,.03,.27,.08,CONCRETE)


@prop('telecom_splice_pole','utilities_poles','large')
def telecom_pole(a):
    a.cylinder((0,0,0),(0,0,6.35),.145,WOOD,10,radius2=.09)
    a.box((0,0,5.65),(1.1,.12,.12),mat=STEEL)
    for x in (-.45,.45):
        tube(a,(x,0,5.66),(x,0,5.88),.032,BLACK)
    tube(a,(.13,0,.08),(.13,0,5.72),.021,BLACK)
    tube(a,(.2,-.07,4.25),(.2,-.07,4.96),.095,BLACK,10)
    for z in (4.31,4.9):
        disc(a,.2,-.07,z,.105,.035,STEEL,10)
    a.torus((0,-.17,5.16),.34,.025,mat=BLACK,axis='y',segments=16,sides=6)
    for z in (4.5,5.18):
        a.box((0,-.16,z),(.33,.045,.06),mat=STEEL)
    a.box((0,-.14,1.4),(.10,.012,.19),mat=YELLOW)


@prop('guyed_corner_power_pole','utilities_poles','large')
def corner_pole(a):
    a.cylinder((0,0,0),(0,0,7.5),.16,WOOD,10,radius2=.10)
    for z in (6.75,7.05):
        a.box((0,0,z),(2.05,.14,.13),mat=WOOD)
        for x in (-.85,.85):
            insulator(a,x,0,z+.08)
    tube(a,(0,.02,6.65),(2.15,.12,.08),.012,STEEL,6)
    tube(a,(1.65,.10,1.62),(2.15,.12,.08),.035,YELLOW,8)
    disc(a,2.15,.12,0,.09,.06,STEEL,8)
    for x in (-.85,.85):
        rod_path(a,[(x,0,7.27),(x,-.18,7.49),(x,-.35,7.18)],.016,DARK,6)
    tube(a,(-.15,0,.02),(-.15,0,5.8),.018,DARK,6)


@prop('overhead_service_mast','utilities_poles','large')
def service_mast(a):
    a.box((0,0,.065),(.40,.40,.13),mat=CONCRETE)
    tube(a,(0,0,.13),(0,0,3.25),.052,STEEL,10)
    rod_path(a,[(0,0,3.22),(0,-.12,3.38),(0,-.28,3.28)],.079,GRAY,8)
    for x in (-.04,0,.04):
        rod_path(a,[(x,-.28,3.25),(x,-.29,3.08),(x,-.43,3.0),(x,-.50,3.11)],.012,BLACK,6)
    a.box((0,-.075,1.47),(.32,.18,.44),mat=GRAY)
    tube(a,(0,-.17,1.5),(0,-.24,1.5),.108,WHITE,12)
    a.box((0,-.25,1.52),(.11,.015,.027),mat=BLACK)
    for z in (.6,2.1):
        a.box((0,.07,z),(.24,.05,.07),mat=STEEL)


@prop('small_cell_network_pole','utilities_poles','large')
def cell_pole(a):
    disc(a,0,0,0,.30,.14,CONCRETE)
    disc(a,0,0,.14,.22,.035,STEEL)
    bolts(a,.18,.18,6,.02)
    a.cylinder((0,0,.18),(0,0,6.5),.135,GRAY,10,radius2=.085)
    tube(a,(0,0,6.5),(0,0,7.22),.19,WHITE,10)
    disc(a,0,0,7.22,.20,.035,GRAY)
    a.box((.20,0,4.7),(.22,.30,.73),mat=WHITE)
    a.box((-.19,0,4.35),(.17,.25,.52),mat=WHITE)
    for z in (4.1,4.9):
        a.box((0,0,z),(.52,.08,.06),mat=STEEL)
    rod_path(a,[(.28,.11,4.4),(.28,.11,3.96),(.1,.11,3.88),(.1,.11,.26)],.018,BLACK,6)
    a.box((0,-.11,.9),(.14,.035,.42),mat=GRAY)


@prop('residential_ac_condenser','utilities_hvac')
def condenser(a):
    a.box((0,0,.05),(.94,.94,.10),mat=CONCRETE)
    feet(a,0,0,.16,.62,.62,DARK)
    a.box((0,0,.18),(.80,.80,.045),mat=GRAY)
    for x in (-.375,.375):
        for y in (-.375,.375):a.box((x,y,.54),(.046,.046,.71),mat=GRAY)
    for y in (-.37,.37):
        coil_face(a,0,y,.53,.68,.59)
    for x in (-.365,.365):
        a.box((x,0,.53),(.018,.68,.60),mat=BLACK)
        for y in (-.28,-.14,0,.14,.28):a.box((x*1.04,y,.53),(.025,.020,.61),mat=DARK)
    for x in (-.365,.365):a.box((x,0,.88),(.09,.82,.055),mat=GRAY)
    for y in (-.365,.365):a.box((0,y,.88),(.64,.09,.055),mat=GRAY)
    fan_top(a,0,0,.91,.335)
    a.box((.285,.41,.45),(.20,.055,.31),mat=GRAY)
    for x,r,m in ((.25,.025,BRASS),(.10,.040,BLACK)):
        rod_path(a,[(x,.42,.28),(x,.54,.28),(x,.60,.20),(x,.60,.07)],r,m)
    for z in (.35,.54):tube(a,(.28,.443,z),(.28,.462,z),.012,STEEL,6)


@prop('mini_split_outdoor_unit','utilities_hvac')
def mini_split(a):
    for x in (-.30,.30):
        a.box((x,0,.045),(.12,.40,.09),mat=STEEL)
        for y in (-.15,.15):disc(a,x,y,.09,.014,.015,DARK,6)
    a.box((0,.12,.415),(.88,.065,.65),mat=WHITE)
    a.box((0,0,.105),(.88,.32,.035),mat=WHITE)
    a.box((0,0,.734),(.92,.35,.038),mat=WHITE)
    for x in (-.428,.425):a.box((x,0,.418),(.028,.32,.61),mat=WHITE)
    # Faceted circular opening cut into a formed front panel.
    aperture_panel(a,(-.12,.425),(-.44,.185,.11,.715),.236,-.173,-.145,WHITE,'y')
    annulus(a,(-.12,-.183,.425),.252,.236,.022,WHITE,16,'y')
    tube(a,(-.12,-.122,.425),(-.12,-.151,.425),.048,GRAY,10)
    for i in range(3):
        t=i*2*pi/3
        pts=[(.035,-.025),(.075,-.071),(.205,-.082),(.221,.009),(.14,.070),(.038,.028)]
        vv=[(-.12+u*cos(t)-v*sin(t),-.151,.425+u*sin(t)+v*cos(t)) for u,v in pts]
        a.mesh(vv,[tuple(range(6))],GRAY)
    for j in range(-4,5):
        zz=j*.047;half=(.23**2-zz**2)**.5
        a.box((-.12,-.190,.425+zz),(half*2,.016,.010),mat=GRAY)
    for x in (-.23,-.12,-.01):a.box((x,-.196,.425),(.009,.014,.41),mat=GRAY)
    a.box((.305,-.163,.416),(.24,.034,.61),mat=WHITE)
    a.box((.29,-.184,.60),(.11,.012,.035),mat=BLUE)
    for z in (.2,.31):
        tube(a,(.44,.04,z),(.515,.04,z),.027,BRASS)
        tube(a,(.51,.04,z),(.51,.04,z+.028),.020,BRASS,6)
    for y in (-.07,.02,.11):a.box((-.445,y,.43),(.012,.02,.43),mat=DARK)


@prop('rooftop_packaged_hvac','utilities_hvac','large')
def rooftop_package(a):
    a.box((0,0,.10),(1.70,1.05,.20),mat=DARK)
    a.box((0,0,.66),(2.10,1.30,1.00),mat=GRAY)
    aperture_panel(a,(-.56,0),(-1.09,-.04,-.69,.69),.408,1.155,1.225,STEEL)
    aperture_panel(a,(.48,0),(-.04,1.09,-.69,.69),.408,1.155,1.225,STEEL)
    fan_top(a,-.56,0,1.23,.42)
    fan_top(a,.48,0,1.23,.42)
    grille(a,-.56,-.665,.65,.72,.75,13,DARK)
    panel(a,.45,-.672,.66,.95,.85,GRAY)
    safety_plate(a,.64,-.70,.84)
    a.box((1.17,0,.60),(.25,.88,.64),mat=STEEL)
    grille(a,1.17,-.457,.60,.18,.53,10,DARK)
    for x in (-.83,.83):
        a.box((x,0,.19),(.12,1.40,.08),mat=STEEL)


@prop('industrial_axial_exhaust_fan','utilities_hvac','large')
def axial_fan(a):
    for x in (-.49,.49):
        a.box((x,0,.05),(.20,.69,.10),mat=STEEL)
        a.beam((x,0,.10),(x*.78,0,.60),.075,.09,STEEL)
        for y in (-.25,.25):disc(a,x,y,.10,.021,.017,DARK,6)
    annulus(a,(0,-.22,.84),.63,.553,.47,GRAY,16,'y')
    for y in (-.245,.25):annulus(a,(0,y,.84),.666,.55,.025,STEEL,16,'y')
    for i in range(6):
        t=2*pi*i/6
        pts=[(.09,-.02),(.20,-.085),(.46,-.10),(.51,.025),(.35,.12),(.11,.065)]
        a.mesh([(u*cos(t)-v*sin(t),-.075,.84+u*sin(t)+v*cos(t)) for u,v in pts],[tuple(range(6))],STEEL)
    tube(a,(0,-.11,.84),(0,.20,.84),.116,GRAY,10)
    for rr in (.31,.49,.60):a.torus((0,-.29,.84),rr,.010,mat=STEEL,axis='y',segments=16,sides=4)
    for i in range(6):
        t=pi*i/6;tube(a,(-.60*cos(t),-.29,.84-.60*sin(t)),(.60*cos(t),-.29,.84+.60*sin(t)),.008,STEEL,4)
    a.box((.49,.14,.96),(.14,.14,.19),mat=DARK)


@prop('wind_turbine_roof_vent','utilities_hvac')
def turbine_vent(a):
    a.box((0,0,.022),(.65,.65,.044),mat=STEEL)
    annulus(a,(0,0,.04),.185,.171,.28,GRAY,12)
    annulus(a,(0,0,.30),.26,.174,.025,STEEL,16)
    disc(a,0,0,.715,.13,.025,STEEL,12)
    # Individual curved louver blades enclose air gaps; no solid sphere inside.
    for i in range(16):
        t=2*pi*i/16;v=[]
        for z,r,tw in ((.325,.23,0),(.44,.30,.10),(.59,.28,.25),(.71,.13,.39)):
            for dt in (0,.32):v.append((r*cos(t+tw+dt),r*sin(t+tw+dt),z))
        a.mesh(v,[(0,1,3,2),(2,3,5,4),(4,5,7,6)],GRAY)
    tube(a,(0,0,.32),(0,0,.73),.018,DARK,6)
    for i in range(3):
        t=2*pi*i/3;tube(a,(0,0,.34),(.22*cos(t),.22*sin(t),.34),.01,STEEL,5)
    a.torus((0,0,.326),.23,.014,STEEL,segments=16,sides=4)


@prop('mushroom_roof_exhaust','utilities_hvac')
def mushroom_vent(a):
    a.box((0,0,.035),(.69,.69,.07),mat=STEEL)
    annulus(a,(0,0,.07),.22,.201,.34,GRAY,12)
    annulus(a,(0,0,.40),.30,.201,.026,DARK,12)
    for i in range(6):
        t=pi*i/3;a.beam((.28*cos(t),.28*sin(t),.40),(.28*cos(t),.28*sin(t),.61),.021,.027,STEEL)
    # Spun, low-domed weather cap with rolled lip and an open underside.
    formed_round(a,[(.56,.43),(.61,.43),(.70,.33),(.745,.16),(.755,.025)],GRAY,16)
    a.torus((0,0,.565),.427,.012,STEEL,segments=16,sides=4)
    disc(a,0,0,.751,.042,.016,STEEL,8)
    for x in (-.25,.25):
        for y in (-.25,.25):disc(a,x,y,.07,.013,.01,DARK,6)


@prop('evaporative_cooler','utilities_hvac')
def evaporative_cooler(a):
    feet(a,0,0,.26,.64,.64,STEEL)
    a.box((0,0,.65),(.90,.90,.78),mat=GREEN)
    a.box((0,0,1.075),(.99,.99,.07),mat=GREEN)
    grille(a,0,-.465,.66,.77,.60,12,STEEL)
    for y in (-.32,-.16,0,.16,.32):
        a.box((.465,y,.67),(.023,.06,.61),mat=DARK)
    a.box((0,.59,.66),(.60,.30,.49),mat=STEEL)
    a.box((0,.78,.66),(.64,.08,.53),mat=STEEL)
    rod_path(a,[(-.43,.20,.50),(-.55,.20,.50),(-.55,.20,.10)],.012,BRASS,6)
    a.box((0,-.463,.34),(.78,.025,.06),mat=STEEL)


@prop('louvered_air_intake_tower','utilities_hvac','large')
def intake_tower(a):
    a.box((0,0,.10),(1.1,1.0,.20),mat=CONCRETE)
    a.box((0,0,1.05),(.80,.70,1.70),mat=GRAY)
    for x in (-.43,.43):
        a.box((x,0,1.15),(.06,.81,1.42),mat=STEEL)
    grille(a,0,-.38,1.18,.77,1.29,15,STEEL)
    for z in (.57,.74,.91,1.08,1.25,1.42,1.59,1.76):
        a.box((0,.38,z),(.76,.09,.055),mat=STEEL)
    a.box((0,0,1.97),(1.04,.96,.14),mat=GRAY)
    a.box((0,0,2.065),(.82,.74,.05),mat=STEEL)


@prop('long_rooftop_air_handler','utilities_hvac','large')
def air_handler(a):
    for x in (-1.15,1.15):
        a.box((x,0,.10),(.18,1.30,.20),mat=STEEL)
    a.box((0,0,.72),(2.90,1.10,1.04),mat=GRAY)
    a.box((0,0,1.28),(3.0,1.19,.08),mat=STEEL)
    for x in (-.99,-.01,.97):
        panel(a,x,-.575,.72,.88,.94,GRAY)
    grille(a,-.99,-.61,.73,.68,.67,12,DARK)
    a.box((1.63,0,.75),(.37,.76,.63),mat=STEEL)
    a.box((1.86,0,.75),(.10,.85,.72),mat=STEEL)
    for x in (-.505,.205):a.box((x,0,1.42),(.030,.73,.20),mat=GRAY)
    for y in (-.35,.35):a.box((-.15,y,1.42),(.68,.030,.20),mat=GRAY)
    aperture_panel(a,(-.15,0),(-.52,.22,-.365,.365),.280,1.495,1.52,GRAY)
    fan_top(a,-.15,0,1.53,.29)
    for x in (-1.4,1.4):
        a.box((x,0,1.36),(.06,.13,.09),mat=STEEL)


@prop('gooseneck_roof_vent','utilities_hvac')
def gooseneck(a):
    a.box((0,0,.03),(.62,.62,.06),mat=STEEL)
    tube(a,(0,0,.05),(0,0,.75),.18,GRAY,12)
    rod_path(a,[(0,0,.75),(0,-.10,.96),(0,-.34,1.02),(0,-.55,.91),(0,-.55,.71)],.18,GRAY,12)
    disc(a,0,-.55,.68,.20,.05,STEEL,12)
    disc(a,0,-.55,.675,.16,.012,BLACK,12)
    for x in (-.10,0,.10):
        a.box((x,-.55,.665),(.014,.25,.015),mat=STEEL)
    disc(a,0,0,.17,.20,.03,STEEL,12)


@prop('water_meter_lid_box','utilities_meters_valves','handheld')
def water_box(a):
    a.box((0,0,.08),(.42,.27,.16),mat=CONCRETE)
    a.box((0,0,.17),(.45,.30,.035),mat=IRON)
    a.box((0,0,.192),(.36,.22,.012),mat=DARK)
    for x in (-.135,-.09,-.045,0,.045,.09,.135):
        a.box((x,0,.204),(.012,.15,.012),mat=IRON)
    a.box((.15,0,.207),(.022,.055,.007),mat=BLACK)
    for x in (-.17,.17):
        disc(a,x,.09,.194,.01,.008,STEEL,6)


@prop('residential_gas_meter','utilities_meters_valves')
def gas_meter(a):
    for x in (-.14,.14):a.box((x,0,.07),(.07,.24,.14),mat=STEEL)
    # Pressed diaphragm body with chamfered shoulders and a bolted split flange.
    outline=[(-.22,-.10),(-.17,-.15),(.17,-.15),(.22,-.10),(.22,.10),(.17,.15),(-.17,.15),(-.22,.10)]
    a.prism(outline,.14,.59,GRAY)
    a.prism([(x*1.045,y*1.06) for x,y in outline],.37,.397,STEEL)
    a.cylinder((0,0,.59),(0,0,.665),.20,GRAY,8,radius2=.16)
    for x in (-.20,.20):
        for y in (-.11,.11):disc(a,x,y,.40,.012,.014,DARK,6)
    a.box((0,-.17,.515),(.28,.055,.145),mat=STEEL)
    a.box((0,-.203,.536),(.21,.012,.059),mat=WHITE)
    for x in (-.075,-.025,.025,.075):a.box((x,-.212,.536),(.031,.008,.036),mat=BLACK)
    for x in (-.13,.13):
        rod_path(a,[(x,0,.65),(x,0,.79),(x*2,0,.79),(x*2,0,.09)],.026,STEEL)
        disc(a,x,0,.684,.044,.037,STEEL,6)
    tube(a,(-.26,0,.61),(-.26,-.07,.61),.080,GRAY,12)
    tube(a,(-.26,-.07,.61),(-.26,-.09,.61),.066,STEEL,12)
    tube(a,(.26,-.055,.45),(.26,.055,.45),.016,BRASS,6)
    a.box((.26,0,.45),(.045,.15,.025),mat=RED)


@prop('gas_pressure_regulator_station','utilities_meters_valves','large')
def gas_regulator(a):
    a.box((0,0,.08),(1.45,.64,.16),mat=CONCRETE)
    for x in (-.53,.53):
        tube(a,(x,0,.16),(x,0,.78),.056,YELLOW)
        disc(a,x,0,.26,.09,.04,STEEL)
    tube(a,(-.53,0,.78),(.53,0,.78),.055,YELLOW)
    for x in (-.34,.34):
        tube(a,(x-.04,0,.78),(x+.04,0,.78),.09,STEEL)
    a.box((0,0,.78),(.27,.22,.21),mat=GRAY)
    disc(a,0,0,.89,.17,.035,GRAY,12)
    a.sphere((0,0,.96),.14,mat=GRAY,segments=10,rings=3)
    tube(a,(0,0,1.07),(0,0,1.17),.025,STEEL)
    tube(a,(0,0,1.17),(0,-.10,1.17),.025,STEEL)
    tube(a,(-.40,0,.83),(-.40,0,.99),.014,BRASS,6)
    tube(a,(-.40,0,.99),(-.40,-.036,.99),.065,WHITE,12)
    a.box((.43,0,.97),(.22,.04,.025),mat=RED)
    tube(a,(.43,0,.82),(.43,0,.97),.02,BRASS)


@prop('curb_stop_valve_cover','utilities_meters_valves','handheld')
def curb_stop(a):
    disc(a,0,0,0,.095,.12,IRON,10)
    disc(a,0,0,.12,.13,.035,IRON,12)
    disc(a,0,0,.157,.105,.014,DARK,12)
    a.box((0,0,.178),(.07,.023,.013),mat=IRON)
    for x in (-.08,.08):
        disc(a,x,0,.17,.009,.007,STEEL,6)


@prop('irrigation_valve_access_box','utilities_meters_valves','handheld')
def irrigation_box(a):
    a.box((0,0,.10),(.50,.34,.20),mat=BLACK)
    a.box((0,0,.21),(.54,.38,.04),mat=GREEN)
    a.box((0,0,.236),(.45,.29,.012),mat=GREEN)
    for y in (-.105,-.07,-.035,0,.035,.07,.105):
        a.box((0,y,.247),(.34,.01,.01),mat=DARK)
    a.box((.18,0,.25),(.045,.05,.012),mat=BLACK)


@prop('water_sampling_station','utilities_meters_valves')
def water_sampler(a):
    a.box((0,0,.07),(.45,.45,.14),mat=CONCRETE)
    tube(a,(0,0,.14),(0,0,1.18),.052,BLUE)
    a.box((0,0,.92),(.27,.24,.48),mat=BLUE)
    panel(a,0,-.135,.93,.23,.40,BLUE)
    a.box((0,0,1.18),(.32,.29,.06),mat=BLUE)
    tube(a,(.13,0,.86),(.25,0,.86),.023,BRASS)
    tube(a,(.25,0,.86),(.25,0,.79),.023,BRASS)
    tube(a,(.18,0,.87),(.18,0,.97),.01,BRASS,6)
    a.box((.18,0,.97),(.11,.027,.018),mat=RED)
    a.box((0,-.161,1.05),(.12,.012,.05),mat=WHITE)


@prop('gas_vent_riser','utilities_meters_valves')
def gas_vent(a):
    disc(a,0,0,0,.16,.045,CONCRETE)
    tube(a,(0,0,.045),(0,0,1.85),.04,YELLOW)
    rod_path(a,[(0,0,1.85),(0,-.055,1.97),(0,-.18,2.01),(0,-.29,1.94),(0,-.29,1.81)],.041,YELLOW,8)
    disc(a,0,-.29,1.78,.055,.025,DARK,10)
    for z in (.27,1.61):
        disc(a,0,0,z,.052,.045,STEEL,8)
    a.box((0,-.054,.90),(.09,.02,.22),mat=WHITE)
    a.box((0,-.067,.91),(.018,.01,.11),mat=RED)


@prop('sewer_cleanout_access_cap','utilities_meters_valves','handheld')
def sewer_cleanout(a):
    disc(a,0,0,0,.14,.19,WHITE,10)
    disc(a,0,0,.19,.16,.035,WHITE,10)
    disc(a,0,0,.227,.145,.03,GRAY,10)
    a.box((0,0,.28),(.08,.08,.05),mat=GRAY)
    for z in (.176,.206):
        a.torus((0,0,z),.144,.009,mat=GRAY,segments=10,sides=4)


@prop('sanitary_manhole_cover','utilities_covers_drains')
def sanitary_cover(a):
    disc(a,0,0,0,.43,.06,CONCRETE,16)
    disc(a,0,0,.06,.385,.045,IRON,16)
    disc(a,0,0,.108,.35,.014,DARK,16)
    for yy in (-.24,-.16,-.08,0,.08,.16,.24):
        extent=(.325**2-yy**2)**.5
        a.box((0,yy,.125),(extent*2,.019,.012),mat=IRON)
    for xx in (-.24,-.16,-.08,0,.08,.16,.24):
        extent=(.325**2-xx**2)**.5
        a.box((xx,0,.126),(.019,extent*2,.012),mat=IRON)
    a.torus((0,0,.125),.343,.012,mat=IRON,segments=16,sides=4)
    for x in (-.27,.27):
        a.box((x,0,.141),(.028,.068,.009),mat=BLACK)


@prop('storm_sewer_radial_cover','utilities_covers_drains')
def storm_cover(a):
    annulus(a,(0,0,0),.49,.395,.10,CONCRETE,16)
    annulus(a,(0,0,.10),.433,.375,.045,IRON,16)
    disc(a,0,0,.01,.392,.012,BLACK,16)
    for i in range(16):
        t=2*pi*i/16;a.beam((.10*cos(t),.10*sin(t),.130),(.383*cos(t),.383*sin(t),.130),.019,.035,IRON)
    for rr in (.13,.25,.373):a.torus((0,0,.134),rr,.014,mat=IRON,segments=16,sides=4)
    disc(a,0,0,.116,.11,.034,IRON,10)
    a.box((0,0,.154),(.11,.023,.012),mat=DARK)


@prop('telecom_vault_access_cover','utilities_covers_drains')
def vault_cover(a):
    a.box((0,0,.045),(1.12,.72,.09),mat=CONCRETE)
    a.box((0,0,.10),(1.02,.62,.05),mat=IRON)
    for x in (-.245,.245):
        a.box((x,0,.131),(.475,.54,.018),mat=GRAY)
        for y in (-.20,-.10,0,.10,.20):
            a.box((x,y,.147),(.40,.018,.012),mat=STEEL)
        for yy in (-.17,.17):
            a.box((x,yy,.161),(.10,.03,.012),mat=BLACK)
    a.box((0,0,.143),(.025,.57,.02),mat=DARK)


@prop('curb_inlet_storm_drain','utilities_covers_drains')
def curb_drain(a):
    a.box((0,.11,.035),(1.25,.60,.07),mat=CONCRETE)
    for x in (-.55,.55):a.box((x,.22,.21),(.14,.38,.35),mat=CONCRETE)
    a.box((0,.40,.22),(1.10,.06,.36),mat=CONCRETE)
    a.box((0,.19,.422),(1.25,.51,.07),mat=CONCRETE)
    a.box((0,.32,.18),(.96,.024,.22),mat=BLACK)
    for x in (-.43,-.215,0,.215,.43):a.box((x,.025,.22),(.028,.07,.28),mat=IRON)
    for z in (.08,.355):a.box((0,.021,z),(.98,.07,.034),mat=IRON)
    for x in (-.45,.45):disc(a,x,.19,.46,.017,.010,IRON,6)


@prop('linear_trench_drain','utilities_covers_drains')
def trench_drain(a):
    grate_surround(a,1.56,.33,.16,.046)
    for y in (-.12,.12):a.box((0,y,.173),(1.48,.027,.030),mat=IRON)
    for i in range(21):a.box((-.70+i*.07,0,.170),(.023,.235,.034),mat=IRON)
    for x in (-.73,.73):a.box((x,0,.173),(.026,.26,.032),mat=IRON)
    for x in (-.49,.49):a.box((x,0,.135),(.042,.235,.025),mat=IRON)


@prop('square_catch_basin_grate','utilities_covers_drains')
def catch_basin(a):
    grate_surround(a,.84,.84,.18,.075)
    for y in (-.35,.35):a.box((0,y,.198),(.75,.05,.045),mat=IRON)
    for x in (-.35,.35):a.box((x,0,.198),(.05,.75,.045),mat=IRON)
    for i in range(9):a.box((-.28+i*.07,0,.195),(.026,.68,.043),mat=IRON)
    for y in (-.20,.20):a.box((0,y,.166),(.68,.026,.026),mat=IRON)
    for y in (-.34,.34):
        for x in (-.28,.28):disc(a,x,y,.222,.015,.007,STEEL,6)


@prop('round_landscape_area_drain','utilities_covers_drains','handheld')
def area_drain(a):
    annulus(a,(0,0,0),.19,.171,.09,BLACK,12)
    annulus(a,(0,0,.09),.22,.172,.031,GREEN,12)
    for i in range(6):
        t=pi*i/6;a.beam((-.175*cos(t),-.175*sin(t),.117),(.175*cos(t),.175*sin(t),.117),.014,.023,GREEN)
    disc(a,0,0,.106,.041,.025,GREEN,8)


@prop('double_panel_sump_grate','utilities_covers_drains')
def sump_grate(a):
    grate_surround(a,1.22,.78,.16,.055)
    for x in (-.55,0,.55):a.box((x,0,.179),(.041,.68,.04),mat=IRON)
    for y in (-.32,.32):a.box((0,y,.179),(1.12,.039,.04),mat=IRON)
    for x in (-.275,.275):
        for j in range(8):a.box((x,-.265+j*.075,.180),(.49,.025,.04),mat=IRON)
        for yy in (-.22,.22):
            for dx in (-.042,.042):a.box((x+dx,yy,.198),(.014,.021,.029),mat=STEEL)
            a.box((x,yy,.216),(.095,.020,.014),mat=STEEL)
