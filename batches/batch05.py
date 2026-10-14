"""Fifty purpose-built outdoor utility props for a midsized American city.

All dimensions are meters.  Every asset rests at z=0, with compact, readable
hardware and open grille construction rather than texture-dependent details.
"""
from math import cos, sin, pi
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
    # Recessed backing plus thin horizontal slats on the front (-Y) face.
    a.box((x,y+.012,z),(width,.018,height),mat=BLACK)
    for j in range(count):
        zz=z-height/2+height*(j+.5)/count
        a.box((x,y-.008,zz),(width,.035,.018),mat=mat)


def panel(a,x,y,z,width,height,mat=GREEN):
    a.box((x,y,z),(width,.035,height),mat=mat)
    handle(a,x+width*.31,y-.026,z)
    for zz in (z-height*.32,z+height*.32):
        a.box((x-width*.46,y-.025,zz),(.035,.022,.085),mat=STEEL)


def flange(a,p,q,r,mat=STEEL):
    tube(a,p,q,r,mat,12)


def insulator(a,x,y,z,mat=WHITE):
    tube(a,(x,y,z),(x,y,z+.23),.042,STEEL)
    for zz in (z+.08,z+.135,z+.19):
        disc(a,x,y,zz,.088,.024,mat,10)


def fan_top(a,x,y,z,r,mat=DARK):
    disc(a,x,y,z,r,.024,BLACK,16)
    disc(a,x,y,z+.034,.07,.04,STEEL,10)
    for i in range(8):
        t=i*pi/4
        tube(a,(x+.065*cos(t),y+.065*sin(t),z+.06),(x+(r-.015)*cos(t),y+(r-.015)*sin(t),z+.06),.012,mat,5)
    for rr in (r*.45,r*.7,r*.94):
        a.torus((x,y,z+.055),rr,.009,mat=mat,segments=16,sides=4)


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
    tube(a,(0,0,0),(0,0,7.8),.14,WOOD,10)
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
    tube(a,(0,0,0),(0,0,7.4),.16,CONCRETE,8)
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
    tube(a,(0,0,0),(0,0,6.35),.13,WOOD,10)
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
    tube(a,(0,0,0),(0,0,7.5),.145,WOOD,10)
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
    tube(a,(0,0,.18),(0,0,6.5),.105,GRAY,10)
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
    a.box((0,0,.055),(.92,.92,.11),mat=CONCRETE)
    feet(a,0,0,.17,.62,.62,DARK)
    a.box((0,0,.52),(.76,.76,.70),mat=GRAY)
    grille(a,0,-.388,.52,.65,.57,13,DARK)
    for y in (-.26,-.13,0,.13,.26):
        a.box((.389,y,.52),(.024,.035,.56),mat=DARK)
    a.box((0,0,.89),(.82,.82,.055),mat=GRAY)
    fan_top(a,0,0,.92,.31)
    rod_path(a,[(.25,.40,.27),(.25,.56,.27),(.25,.56,.06)],.025,BRASS)
    rod_path(a,[(.10,.40,.27),(.10,.53,.27),(.10,.53,.06)],.042,BLACK)


@prop('mini_split_outdoor_unit','utilities_hvac')
def mini_split(a):
    for x in (-.29,.29):
        a.box((x,0,.06),(.10,.38,.12),mat=STEEL)
    a.box((0,0,.41),(.88,.32,.61),mat=WHITE)
    tube(a,(-.13,-.17,.42),(-.13,-.192,.42),.24,BLACK,16)
    tube(a,(-.13,-.192,.42),(-.13,-.215,.42),.048,GRAY,10)
    for j in range(-4,5):
        z=.42+j*.047
        half=(.23**2-(j*.047)**2)**.5
        a.box((-.13,-.219,z),(half*2,.017,.011),mat=GRAY)
    a.box((.30,-.169,.41),(.19,.018,.50),mat=WHITE)
    a.box((.29,-.184,.58),(.11,.012,.035),mat=BLUE)
    for z in (.20,.31):
        tube(a,(.44,.04,z),(.52,.04,z),.027,BRASS)
    a.box((0,0,.733),(.92,.35,.035),mat=WHITE)


@prop('rooftop_packaged_hvac','utilities_hvac','large')
def rooftop_package(a):
    a.box((0,0,.10),(1.70,1.05,.20),mat=DARK)
    a.box((0,0,.66),(2.10,1.30,1.00),mat=GRAY)
    a.box((0,0,1.19),(2.18,1.38,.07),mat=STEEL)
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
    for x in (-.50,.50):
        a.box((x,0,.09),(.20,.68,.18),mat=STEEL)
        a.box((x,0,.43),(.08,.11,.60),mat=STEEL)
    tube(a,(0,-.21,.89),(0,.24,.89),.66,GRAY,16)
    tube(a,(0,-.225,.89),(0,-.245,.89),.56,BLACK,16)
    for i in range(8):
        ang=2*pi*i/8
        tube(a,(.11*cos(ang),-.29,.89+.11*sin(ang)),(.51*cos(ang+.20),-.29,.89+.51*sin(ang+.20)),.065,STEEL,5)
    tube(a,(0,-.25,.89),(0,-.36,.89),.12,GRAY,10)
    for rr in (.31,.49,.60):
        a.torus((0,-.37,.89),rr,.012,mat=STEEL,axis='y',segments=16,sides=4)
    for i in range(6):
        ang=pi*i/6
        tube(a,(-.60*cos(ang),-.38,.89-.60*sin(ang)),(.60*cos(ang),-.38,.89+.60*sin(ang)),.012,STEEL,4)


@prop('wind_turbine_roof_vent','utilities_hvac')
def turbine_vent(a):
    a.box((0,0,.025),(.62,.62,.05),mat=STEEL)
    tube(a,(0,0,.05),(0,0,.37),.18,GRAY,12)
    disc(a,0,0,.33,.27,.035,STEEL,12)
    a.sphere((0,0,.53),.30,mat=GRAY,segments=12,rings=4)
    disc(a,0,0,.78,.09,.025,STEEL,10)
    for i in range(12):
        t=i*pi/6
        rod_path(a,[(.235*cos(t),.235*sin(t),.36),(.303*cos(t+.16),.303*sin(t+.16),.51),(.24*cos(t+.32),.24*sin(t+.32),.69)],.012,STEEL,5)


@prop('mushroom_roof_exhaust','utilities_hvac')
def mushroom_vent(a):
    a.box((0,0,.04),(.68,.68,.08),mat=STEEL)
    tube(a,(0,0,.08),(0,0,.44),.22,GRAY,12)
    disc(a,0,0,.40,.34,.035,DARK,12)
    for i in range(6):
        t=i*pi/3
        tube(a,(.28*cos(t),.28*sin(t),.40),(.28*cos(t),.28*sin(t),.60),.016,STEEL,5)
    disc(a,0,0,.60,.43,.07,GRAY,12)
    a.sphere((0,0,.65),.39,mat=GRAY,segments=12,rings=3)
    disc(a,0,0,.98,.06,.02,STEEL,8)


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
    a.box((-.15,0,1.42),(.74,.73,.20),mat=GRAY)
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
    feet(a,0,0,.15,.26,.14,STEEL)
    a.box((0,0,.39),(.43,.25,.48),mat=GRAY)
    a.box((0,0,.65),(.38,.24,.05),mat=STEEL)
    a.box((0,-.143,.52),(.25,.047,.14),mat=STEEL)
    a.box((0,-.171,.54),(.20,.012,.06),mat=WHITE)
    for x in (-.075,-.025,.025,.075):
        tube(a,(x,-.18,.54),(x,-.184,.54),.017,BLACK,8)
    for x in (-.13,.13):
        rod_path(a,[(x,0,.67),(x,0,.80),(x*2,0,.80),(x*2,0,.15)],.026,STEEL)
    tube(a,(-.26,0,.62),(-.26,-.05,.62),.074,GRAY,10)
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
    disc(a,0,0,0,.49,.055,CONCRETE,16)
    disc(a,0,0,.055,.43,.035,IRON,16)
    disc(a,0,0,.09,.394,.014,BLACK,16)
    for i in range(16):
        t=2*pi*i/16
        tube(a,(.12*cos(t),.12*sin(t),.115),(.38*cos(t),.38*sin(t),.115),.014,IRON,4)
    for rr in (.13,.25,.38):
        a.torus((0,0,.117),rr,.015,mat=IRON,segments=16,sides=4)
    disc(a,0,0,.108,.11,.02,IRON,10)
    a.box((0,0,.132),(.11,.024,.012),mat=DARK)


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
    a.box((0,.25,.20),(1.20,.36,.40),mat=CONCRETE)
    a.box((0,-.06,.04),(1.22,.42,.08),mat=CONCRETE)
    a.box((0,.06,.20),(.95,.025,.24),mat=BLACK)
    for x in (-.43,-.215,0,.215,.43):
        a.box((x,.025,.20),(.035,.055,.24),mat=IRON)
    a.box((0,.018,.32),(.97,.07,.045),mat=IRON)
    a.box((0,.018,.08),(.97,.07,.045),mat=IRON)
    a.box((0,.235,.415),(1.22,.41,.04),mat=CONCRETE)


@prop('linear_trench_drain','utilities_covers_drains')
def trench_drain(a):
    a.box((0,0,.065),(1.55,.30,.13),mat=CONCRETE)
    a.box((0,0,.137),(1.48,.235,.018),mat=BLACK)
    for y in (-.115,.115):
        a.box((0,y,.154),(1.50,.025,.026),mat=IRON)
    for i in range(21):
        a.box((-.70+i*.07,0,.155),(.024,.235,.028),mat=IRON)
    for x in (-.73,.73):
        a.box((x,0,.157),(.04,.26,.025),mat=IRON)


@prop('square_catch_basin_grate','utilities_covers_drains')
def catch_basin(a):
    a.box((0,0,.065),(.82,.82,.13),mat=CONCRETE)
    a.box((0,0,.136),(.68,.68,.018),mat=BLACK)
    for y in (-.35,.35):
        a.box((0,y,.159),(.75,.05,.04),mat=IRON)
    for x in (-.35,.35):
        a.box((x,0,.159),(.05,.75,.04),mat=IRON)
    for i in range(9):
        a.box((-.28+i*.07,0,.16),(.026,.68,.04),mat=IRON)
    for y in (-.20,.20):
        a.box((0,y,.156),(.68,.026,.04),mat=IRON)


@prop('round_landscape_area_drain','utilities_covers_drains','handheld')
def area_drain(a):
    disc(a,0,0,0,.19,.09,BLACK,12)
    disc(a,0,0,.09,.22,.025,GREEN,12)
    disc(a,0,0,.115,.18,.012,BLACK,12)
    a.torus((0,0,.13),.19,.018,mat=GREEN,segments=12,sides=4)
    for i in range(6):
        t=pi*i/6
        tube(a,(-.175*cos(t),-.175*sin(t),.137),(.175*cos(t),.175*sin(t),.137),.012,GREEN,4)
    disc(a,0,0,.135,.048,.015,GREEN,10)


@prop('double_panel_sump_grate','utilities_covers_drains')
def sump_grate(a):
    a.box((0,0,.055),(1.20,.76,.11),mat=CONCRETE)
    a.box((0,0,.12),(1.08,.64,.02),mat=BLACK)
    for x in (-.55,0,.55):
        a.box((x,0,.145),(.045,.68,.04),mat=IRON)
    for y in (-.32,.32):
        a.box((0,y,.145),(1.12,.045,.04),mat=IRON)
    for x in (-.275,.275):
        for j in range(8):
            a.box((x,-.265+j*.075,.148),(.49,.027,.04),mat=IRON)
        for yy in (-.22,.22):
            a.box((x,yy,.172),(.095,.045,.015),mat=STEEL)
