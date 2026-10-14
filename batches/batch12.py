"""Fifty architectural exterior components for an American city kit.

Units are metres.  Front faces point toward -Y.  Narrow trim, rebates,
hardware and structural members are deliberately modeled rather than painted.
"""
from assetlib import Asset, register
import math


CATEGORY = 'exterior_building_components'


def model(name, size='person'):
    return Asset('b12_' + name, CATEGORY, size,
                 style='muted realistic low-poly', orientation='front -Y')


def finish(a):
    return a.bottom_center()


def entry(name, size='person'):
    def decorate(fn):
        register('b12_' + name, CATEGORY, size, fn)
        return fn
    return decorate


def xz_prism(a, pts, y0, y1, mat):
    """Counterclockwise x/z polygon extruded along Y."""
    n = len(pts)
    v = [(x, y0, z) for x, z in pts] + [(x, y1, z) for x, z in pts]
    f = [tuple(range(n)), tuple(reversed(range(n, 2*n)))]
    f += [(i, n+i, n+(i+1)%n, (i+1)%n) for i in range(n)]
    a.mesh(v, f, mat)


def yz_prism(a, pts, x0, x1, mat):
    n = len(pts)
    # A CCW y/z polygon has +X normal, so the first cap is reversed.
    v = [(x0, y, z) for y, z in pts] + [(x1, y, z) for y, z in pts]
    f = [tuple(reversed(range(n))), tuple(range(n, 2*n))]
    f += [(i, (i+1)%n, n+(i+1)%n, n+i) for i in range(n)]
    a.mesh(v, f, mat)


def frame(a, w, h, z=0, y=0, t=.075, d=.15, mat='white', sill=True, x=0):
    for side in (-1, 1):
        a.box((x+side*(w+t)/2, y, z+h/2), (t, d, h+2*t), mat)
    a.box((x, y, z+h+t/2), (w, d, t), mat)
    if sill:
        a.box((x, y-.035, z-t/2), (w+2*t, d+.09, t), mat)


def pane(a, x, z, w, h, y=0, mat='glass'):
    a.box((x, y, z), (w, .025, h), mat)


def inset_panel(a, x, z, w, h, y=-.065, mat='wood_dark', trim='wood'):
    a.box((x, y, z), (w, .022, h), mat)
    for sx in (-1, 1):
        a.box((x+sx*(w/2-.019), y-.012, z), (.038, .022, h), trim)
    for sz in (-1, 1):
        a.box((x, y-.012, z+sz*(h/2-.019)), (w-.076, .022, .038), trim)


def knob(a, x, z, y=-.1, mat='gold'):
    a.cylinder((x, y+.03, z), (x, y-.015, z), .035, mat, 8)
    a.sphere((x, y-.027, z), .033, mat, 8, 3)


def pull(a, x, z, y=-.12, h=.28, mat='steel'):
    for sz in (-1, 1):
        a.cylinder((x, y+.055, z+sz*h/2), (x, y, z+sz*h/2), .013, mat, 6)
    a.cylinder((x, y, z-h/2), (x, y, z+h/2), .016, mat, 6)


def hinges(a, x, zs, y=-.065, mat='dark_metal'):
    for z in zs:
        a.box((x-.014, y, z), (.055, .014, .09), mat)
        a.cylinder((x, y-.012, z-.045), (x, y-.012, z+.045), .011, mat, 6)


def grille(a, w, h, z=0, y=-.07, cols=3, rows=2, mat='white', x=0):
    for i in range(1, cols):
        a.box((x-w/2+w*i/cols, y, z+h/2), (.025, .035, h), mat)
    for i in range(1, rows):
        a.box((x, y, z+h*i/rows), (w, .035, .025), mat)


def rail(a, p, q, h=.95, count=6, mat='dark_metal', bars=True):
    a.beam((p[0], p[1], p[2]+h), (q[0], q[1], q[2]+h), .045, .035, mat)
    a.beam((p[0], p[1], p[2]+.16), (q[0], q[1], q[2]+.16), .027, .025, mat)
    for i in range(count+1):
        t=i/count
        x=p[0]+t*(q[0]-p[0]); y=p[1]+t*(q[1]-p[1]); z=p[2]+t*(q[2]-p[2])
        a.box((x,y,z+h/2), (.03,.03,h), mat)
    if bars:
        a.beam((p[0],p[1],p[2]+.51), (q[0],q[1],q[2]+.51), .024,.021,mat)


def bolts(a, xs, y, zs, mat='steel'):
    for x in xs:
        for z in zs:
            a.cylinder((x,y,z), (x,y-.009,z), .012,mat,6)


def treads(a, w, count, run, rise, mat='concrete', start_y=0, start_z=0):
    for i in range(count):
        z=start_z+(i+1)*rise
        a.box((0,start_y+(i+.5)*run,z/2), (w,run,z), mat)
        a.box((0,start_y+(i+.5)*run-.015,z+.012), (w+.035,run+.025,.024), 'concrete_light')


@entry('six_panel_front_door')
def six_panel_front_door():
    a=model('six_panel_front_door'); w=.91; h=2.03
    a.box((0,0,h/2),(w,.085,h),'wood')
    frame(a,w,h,t=.085,d=.19,mat='cream')
    for z,ph in ((.38,.53),(1.04,.55),(1.70,.42)):
        for x in (-.205,.205): inset_panel(a,x,z,.32,ph)
    knob(a,.34,.98); hinges(a,-.445,[.27,1.02,1.78])
    a.box((0,-.06,.095),(.79,.018,.115),'gold')
    return finish(a)


@entry('commercial_glass_entry')
def commercial_glass_entry():
    a=model('commercial_glass_entry'); frame(a,1.02,2.2,t=.065,mat='dark_metal')
    pane(a,0,1.17,.87,1.93)
    for x in (-.48,.48): a.box((x,-.015,1.1),(.06,.07,2.18),'silver')
    for z,h in ((.08,.16),(2.16,.08)):
        a.box((0,-.015,z),(.9,.07,h),'silver')
    pull(a,.34,1.06,h=.42)
    a.box((.22,.015,2.09),(.3,.07,.075),'dark_metal')
    a.beam((.17,-.005,2.075),(.38,-.11,2.075),.022,mat='steel')
    a.box((0,-.05,.19),(.87,.025,.16),'metal')
    return finish(a)


@entry('double_steel_service_door','large')
def double_steel_service_door():
    a=model('double_steel_service_door','large'); frame(a,1.84,2.1,t=.085,mat='concrete_light')
    for x in (-.46,.46):
        a.box((x,0,1.05),(.905,.11,2.1),'metal')
        a.box((x,-.068,.25),(.76,.018,.33),'steel')
        a.box((x,-.065,1.65),(.27,.018,.29),'dark_metal')
        pane(a,x,1.65,.225,.245,-.08)
        a.box((x,-.11,1.04),(.71,.045,.055),'dark_metal')
        for dx in (-.29,.29): a.box((x+dx,-.08,1.04),(.055,.08,.085),'steel')
    hinges(a,-.91,[.2,1.05,1.9]); hinges(a,.91,[.2,1.05,1.9])
    a.box((0,-.07,1.05),(.026,.03,2.1),'dark_metal')
    return finish(a)


@entry('roll_up_storefront_shutter','large')
def roll_up_storefront_shutter():
    a=model('roll_up_storefront_shutter','large'); w=3.2;h=2.65
    for x in (-w/2-.06,w/2+.06): a.box((x,.04,h/2),(.12,.17,h),'dark_metal')
    for i in range(27):
        a.box((0,0,.048+i*.097),(w,.055,.085),'metal')
        a.box((0,-.033,.011+i*.097),(w,.016,.011),'steel')
    a.box((0,-.01,.045),(w,.095,.075),'dark_metal')
    a.box((0,.055,h+.19),(w+.24,.42,.36),'metal')
    for x in (-1.48,1.48): a.box((x,-.165,h+.19),(.04,.024,.32),'steel')
    a.box((0,-.064,.14),(.15,.028,.07),'dark_metal')
    return finish(a)


@entry('sectional_residential_garage','large')
def sectional_residential_garage():
    a=model('sectional_residential_garage','large'); w=2.65;h=2.2
    frame(a,w,h,t=.105,d=.2,mat='cream')
    for row in range(4):
        z=.272+row*.55
        a.box((0,0,z),(w,.08,.537),'white')
        for x in (-.91,0,.91):
            if row==3:
                a.box((x,-.047,z),(.69,.02,.3),'dark_metal');pane(a,x,z,.63,.245,-.063)
                grille(a,.63,.245,z-.1225,-.085,cols=2,rows=1,x=x)
            else: inset_panel(a,x,z,.72,.36,-.052,'concrete_light','white')
    a.box((0,-.085,.66),(.2,.045,.035),'black')
    a.box((0,-.045,.026),(w,.04,.044),'rubber')
    return finish(a)


@entry('carriage_house_garage_doors','large')
def carriage_house_garage_doors():
    a=model('carriage_house_garage_doors','large'); frame(a,2.5,2.32,t=.12,mat='cream')
    for side in (-1,1):
        x=side*.627
        a.box((x,0,1.16),(1.235,.105,2.32),'wood')
        for j in range(5): a.box((x-.49+j*.245,-.059,.88),(.225,.025,1.7),'wood_dark')
        for z in (.13,1.60): a.box((x,-.085,z),(1.13,.052,.1),'wood_light')
        a.beam((x-side*.52,-.09,.19),(x+side*.52,-.09,1.55),.085,.036,'wood_light')
        pane(a,x,1.98,.99,.43,-.065);grille(a,.99,.43,1.765,-.087,cols=3,rows=1,mat='wood_light',x=x)
        for z in (.33,1.4):
            a.box((side*.93,-.108,z),(.49,.025,.055),'dark_metal')
            bolts(a,[side*.76,side*1.1],-.124,[z],'dark_metal')
        pull(a,side*.10,1.06,h=.22,mat='dark_metal')
    return finish(a)


@entry('sloped_cellar_bulkhead','large')
def sloped_cellar_bulkhead():
    a=model('sloped_cellar_bulkhead','large')
    for x0,x1 in ((-.77,-.65),(.65,.77)):
        yz_prism(a,[(-.9,0),(.9,0),(.9,.98),(-.9,.22)],x0,x1,'concrete')
    a.box((0,.84,.48),(1.4,.12,.96),'concrete')
    slope=math.atan2(.76,1.8)
    for x in (-.325,.325):
        a.box((x,0,.65),(.635,1.96,.055),'dark_metal',rot=(slope,0,0))
        for dy in (-.59,.55): a.box((x,dy,.65+dy*.422),(.56,.07,.033),'metal',rot=(slope,0,0))
    a.beam((0,-.9,.27),(0,.9,1.03),.032,.03,'metal')
    a.cylinder((-.08,-.5,.47),(-.08,-.33,.54),.018,'steel',6)
    a.box((0,-.96,.06),(1.55,.13,.12),'concrete_light')
    return finish(a)


@entry('revolving_glass_entry','large')
def revolving_glass_entry():
    a=model('revolving_glass_entry','large');r=1.04;h=2.35
    a.cylinder((0,0,0),(0,0,.065),r+.08,'dark_metal',16)
    a.cylinder((0,0,h),(0,0,h+.14),r+.08,'metal',16)
    for deg in (0,30,60,120,150,180,210,240,300,330):
        th=math.radians(deg);x=r*math.cos(th);y=r*math.sin(th)
        a.box((x,y,h/2),(.045,.045,h),'silver')
    for start in (0,120,180,300):
        for deg in range(start,start+60,20):
            th=math.radians(deg+10);ch=2*r*math.sin(math.radians(10))
            a.box((r*math.cos(th),r*math.sin(th),h/2),(.02,ch,h-.08),'glass',rot=th)
    a.cylinder((0,0,.065),(0,0,h),.055,'steel',8)
    for deg in (0,120,240):
        th=math.radians(deg); x=.48*math.cos(th);y=.48*math.sin(th)
        a.box((x,y,1.19),(.92,.025,2.2),'glass',rot=th)
        for z in (.09,1.10,2.29): a.box((x,y,z),(.98,.04,.045),'silver',rot=th)
    return finish(a)


@entry('sliding_patio_door','large')
def sliding_patio_door():
    a=model('sliding_patio_door','large');frame(a,2.0,2.13,t=.075,d=.18,mat='white')
    for x,y in ((-.49,.025),(.49,-.04)):
        pane(a,x,1.075,.86,1.98,y)
        for dx in (-.455,.455): a.box((x+dx,y-.027,1.065),(.065,.075,2.13),'white')
        for z in (.045,2.085): a.box((x,y-.027,z),(.91,.075,.09),'white')
    for y in (-.09,0,.09): a.box((0,y,-.04),(2.12,.022,.035),'silver')
    pull(a,.085,1.04,-.13,.32,'white')
    return finish(a)


@entry('screen_storm_door')
def screen_storm_door():
    a=model('screen_storm_door');frame(a,.9,2.04,t=.045,d=.065,mat='cream')
    a.box((0,.014,1.17),(.8,.012,1.62),'dark_metal')
    for x in (-.414,.414):a.box((x,-.016,1.02),(.072,.045,2.04),'white')
    for z,hh in ((.15,.3),(.83,.095),(1.96,.16)):
        a.box((0,-.025,z),(.78,.045,hh),'white')
    for i in range(12):a.box((-.36+i*.065,-.003,1.43),(.008,.009,1.02),'metal')
    for i in range(12):a.box((0,-.009,.92+i*.087),(.79,.009,.008),'metal')
    a.box((.29,-.072,.94),(.034,.065,.16),'black')
    hinges(a,-.442,[.24,1,1.77]);return finish(a)


@entry('arched_wood_entry')
def arched_wood_entry():
    a=model('arched_wood_entry');r=.51; spring=1.79
    pts=[(-r,0),(r,0),(r,spring)]+[(r*math.cos(i*math.pi/12),spring+r*math.sin(i*math.pi/12)) for i in range(1,13)]
    xz_prism(a,pts,-.035,.055,'wood_dark')
    for x in (-.565,.565):a.box((x,0,.90),(.11,.2,1.80),'concrete_light')
    for i in range(12):
        th=(i+.5)*math.pi/12
        a.box((.565*math.cos(th),0,spring+.565*math.sin(th)),(.15,.20,.115),'concrete_light',rot=(0,math.pi/2-th,0))
    for x in (-.235,.235):inset_panel(a,x,.71,.36,1.1,-.067,'wood','wood_light')
    pane(a,0,1.69,.72,.34,-.054);grille(a,.72,.34,1.52,-.079,cols=3,rows=1,mat='wood')
    knob(a,.37,1.04,mat='dark_metal');hinges(a,-.49,[.22,1.09,1.69]);return finish(a)


@entry('sidelight_transom_entry','large')
def sidelight_transom_entry():
    a=model('sidelight_transom_entry','large');frame(a,1.72,2.5,t=.085,d=.21,mat='cream')
    a.box((0,0,1.02),(.9,.09,2.04),'navy')
    for x in (-.69,.69):
        pane(a,x,1.12,.29,1.8);frame(a,.29,1.8,.22,-.01,.035,.09,'white',True,x)
        grille(a,.29,1.8,.22,-.064,cols=1,rows=4,mat='white',x=x)
    a.box((0,-.01,2.1),(1.72,.13,.12),'white');pane(a,0,2.34,1.65,.34)
    grille(a,1.65,.34,2.17,-.067,cols=5,rows=1)
    inset_panel(a,0,.51,.7,.71,-.061,'navy','white')
    pane(a,0,1.45,.64,.77,-.05);grille(a,.64,.77,1.065,-.075,cols=2,rows=3)
    knob(a,.35,.98,mat='gold');return finish(a)


@entry('basement_hopper_window')
def basement_hopper_window():
    a=model('basement_hopper_window');frame(a,1.18,.52,t=.085,d=.28,mat='concrete')
    pane(a,0,.285,1.08,.42,.012)
    for x in (-.555,.555):a.box((x,-.034,.26),(.045,.07,.49),'metal')
    for z in (.025,.49):a.box((0,-.034,z),(1.11,.07,.045),'metal')
    a.box((0,-.089,.43),(.13,.055,.026),'black')
    for x in (-.40,.40):a.cylinder((x-.035,-.065,.025),(x+.035,-.065,.025),.018,'steel',6)
    a.box((0,-.15,-.08),(1.43,.47,.065),'concrete_light')
    return finish(a)


@entry('double_hung_sash_window')
def double_hung_sash_window():
    a=model('double_hung_sash_window');frame(a,.91,1.52,t=.09,d=.18,mat='cream')
    for z,y in ((.385,-.027),(1.14,.018)):
        pane(a,0,z,.79,.675,y)
        for x in (-.415,.415):a.box((x,y-.028,z),(.05,.055,.735),'white')
        for dz in (-.35,.35):a.box((0,y-.032,z+dz),(.83,.06,.055),'white')
        grille(a,.78,.65,z-.325,y-.046,cols=2,rows=2)
    a.box((0,-.03,.76),(.91,.115,.054),'white')
    a.box((0,-.095,.77),(.10,.03,.034),'gold')
    a.box((0,-.07,-.135),(1.05,.09,.11),'cream')
    return finish(a)


@entry('open_casement_window')
def open_casement_window():
    a=model('open_casement_window');frame(a,1.2,1.4,t=.08,d=.17,mat='white')
    pane(a,.305,.70,.53,1.29,.015)
    a.box((0,-.017,.7),(.055,.09,1.4),'white')
    # Left sash pivots outward forty degrees from its jamb.
    pivot=(-.6,-.035);th=-.62
    def xy(local):return (pivot[0]+local*math.cos(th),pivot[1]+local*math.sin(th))
    x,y=xy(.29);a.box((x,y,.7),(.52,.025,1.28),'glass',rot=th)
    for u in (0,.58):
        xx,yy=xy(u);a.box((xx,yy,.7),(.047,.075,1.4),'white',rot=th)
    for z in (.025,1.375):a.box((x,y,z),(.58,.075,.05),'white',rot=th)
    for u in (.23,.4):
        xx,yy=xy(u);a.beam((-.53,-.025,.09),(xx,yy,.09),.018,.016,'steel')
    a.box((.3,-.046,.7),(.53,.03,.03),'white');return finish(a)


@entry('projecting_bay_window','large')
def projecting_bay_window():
    a=model('projecting_bay_window','large')
    footprint=[(-1.25,.0),(-.83,-.65),(.83,-.65),(1.25,0)]
    a.prism(footprint,0,.14,'concrete_light');a.prism(footprint,1.65,1.77,'cream')
    for p,q in zip(footprint,footprint[1:]):
        dx=q[0]-p[0];dy=q[1]-p[1];ln=math.hypot(dx,dy);ang=math.atan2(dy,dx)
        x=(p[0]+q[0])/2;y=(p[1]+q[1])/2
        a.box((x,y,.92),(ln-.08,.025,1.32),'glass',rot=ang)
        for z in (.22,.91,1.60):a.beam((p[0],p[1],z),(q[0],q[1],z),.056,.06,'white')
        a.box((x,y,.92),(.045,.08,1.4),'white',rot=ang)
    for x,y in footprint:a.box((x,y,.91),(.075,.075,1.55),'white')
    a.box((0,-.31,1.83),(2.64,.85,.09),'dark_metal')
    for x in (-.72,.72):a.beam((x,-.06,.02),(x,-.57,.3),.10,.11,'wood_dark')
    return finish(a)


@entry('industrial_steel_grid_window','large')
def industrial_steel_grid_window():
    a=model('industrial_steel_grid_window','large');frame(a,2.42,1.84,t=.08,d=.16,mat='brick')
    pane(a,0,.92,2.4,1.82,.018)
    for x in (-1.19,1.19):a.box((x,-.02,.92),(.045,.075,1.84),'dark_metal')
    for z in (.02,1.82):a.box((0,-.02,z),(2.42,.075,.04),'dark_metal')
    grille(a,2.4,1.8,.02,-.027,cols=6,rows=4,mat='dark_metal')
    a.box((0,-.061,.91),(.82,.037,.027),'metal')
    a.box((0,-.082,.76),(.11,.04,.02),'steel')
    a.box((0,-.09,-.08),(2.66,.36,.12),'concrete_light')
    return finish(a)


@entry('glass_block_window_panel')
def glass_block_window_panel():
    a=model('glass_block_window_panel');frame(a,1.14,1.14,t=.065,d=.18,mat='concrete_light')
    for i in range(6):
        for j in range(6):
            x=-.475+i*.19;z=.095+j*.19
            a.box((x,0,z),(.177,.105,.177),'glass')
            a.box((x,-.058,z),(.135,.018,.135),'silver' if (i+j)%8==0 else 'glass')
    for i in range(7):
        a.box((-.57+i*.19,.018,.57),(.011,.13,1.14),'cream')
        a.box((0,.018,i*.19),(1.14,.13,.011),'cream')
    return finish(a)


@entry('round_attic_window')
def round_attic_window():
    a=model('round_attic_window');a.cylinder((0,.045,.59),(0,-.015,.59),.49,'glass',16)
    a.torus((0,-.01,.59),.54,.068,'cream',axis='y',segments=16,sides=4)
    a.torus((0,-.045,.59),.484,.018,'white',axis='y',segments=16,sides=4)
    a.box((0,-.066,.59),(.945,.04,.035),'white');a.box((0,-.066,.59),(.035,.04,.945),'white')
    for d in (-1,1):a.beam((-.34,-.055,.59+d*.34),(.34,-.055,.59-d*.34),.022,.025,'white')
    return finish(a)


@entry('gable_dormer_window','large')
def gable_dormer_window():
    a=model('gable_dormer_window','large')
    for side in (-1,1):
        a.box((side*.58,.32,.66),(.1,.7,1.32),'cream')
        for z in (.2,.4,.6,.8,1.,1.2):a.box((side*.635,.32,z),(.025,.71,.025),'white')
    xz_prism(a,[(-.66,1.28),(.66,1.28),(0,1.81)],-.08,.07,'cream')
    frame(a,.92,1.10,.12,-.055,.055,.12,'white')
    pane(a,0,.67,.91,1.09,-.066);grille(a,.89,1.08,.13,-.094,cols=2,rows=3)
    slope=math.atan2(.55,.72)
    for side in (-1,1):
        a.box((side*.37,.25,1.59),(.96,1.08,.085),'asphalt',rot=(0,side*slope,0))
        a.beam((side*.74,-.29,1.35),(0,-.29,1.87),.065,.06,'white')
    a.box((0,.25,1.9),(.12,1.08,.055),'dark_metal')
    return finish(a)


@entry('louvered_window_shutters')
def louvered_window_shutters():
    a=model('louvered_window_shutters')
    for x in (-.38,.38):
        for dx in (-.24,.24):a.box((x+dx,0,.79),(.065,.07,1.58),'green')
        for z in (.045,.79,1.535):a.box((x,0,z),(.48,.07,.075),'green')
        for i in range(18):
            z=.13+i*.075
            a.box((x,-.005,z),(.43,.072,.022),'green',rot=(.45,0,0))
        for z in (.23,1.35):a.box((x-.26,-.046,z),(.09,.02,.07),'dark_metal')
    return finish(a)


@entry('board_and_batten_shutters')
def board_and_batten_shutters():
    a=model('board_and_batten_shutters')
    for x in (-.36,.36):
        for dx in (-.175,0,.175):a.box((x+dx,0,.7),(.163,.052,1.4),'wood_dark')
        for z in (.27,1.13):a.box((x,-.047,z),(.56,.042,.09),'wood')
        a.beam((x-.23,-.071,.32),(x+.23,-.071,1.08),.055,.03,'wood')
        for z in (.27,1.13):bolts(a,[x-.19,x+.19],-.073,[z],'black')
        for z in (.2,1.22):a.box((x-.28,-.065,z),(.1,.045,.06),'dark_metal')
    return finish(a)


@entry('canvas_wedge_shop_awning','large')
def canvas_wedge_shop_awning():
    a=model('canvas_wedge_shop_awning','large');ang=math.atan2(.65,1.15)
    for i in range(10):
        x=-1.35+i*.3
        a.box((x,-.58,.50),(.3,1.34,.035),'green' if i%2==0 else 'cream',rot=(ang,0,0))
        a.box((x,-1.17,.14),(.3,.037,.24),'green' if i%2==0 else 'cream')
    for side in (-1,1):
        yz_prism(a,[(-1.16,.27),(0,.92),(0,.27)],side*1.48-.017,side*1.48+.017,'green')
        a.beam((side*1.45,-1.16,.25),(side*1.45,0,.88),.035,mat='dark_metal')
    a.box((0,.015,.89),(3.1,.08,.1),'dark_metal');a.box((0,-1.17,.27),(3.02,.045,.04),'dark_metal')
    return finish(a)


@entry('barrel_entrance_awning','large')
def barrel_entrance_awning():
    a=model('barrel_entrance_awning','large');r=.93
    for i in range(10):
        t0=math.pi*i/10;t1=math.pi*(i+1)/10
        x0=r*math.cos(t0);x1=r*math.cos(t1);z0=.18+r*math.sin(t0);z1=.18+r*math.sin(t1)
        a.beam((x0,-.45,z0),(x1,-.45,z1),.93,.033,'navy' if i%2==0 else 'cream')
        a.beam((x0,-.91,z0),(x1,-.91,z1),.026,.03,'dark_metal')
    for x in (-.93,.93):a.box((x,-.45,.09),(.05,.93,.18),'navy')
    a.box((0,.035,.1),(1.99,.09,.11),'dark_metal')
    for x in (-.85,.85):a.beam((x,0,.0),(x,-.86,.14),.032,mat='steel')
    return finish(a)


@entry('suspended_glass_entry_canopy','large')
def suspended_glass_entry_canopy():
    a=model('suspended_glass_entry_canopy','large')
    for x in (-.88,0,.88):
        a.box((x,-.68,.23),(.83,1.37,.035),'glass',rot=(.055,0,0))
    for x in (-1.33,-.45,.45,1.33):a.beam((x,.01,.27),(x,-1.4,.19),.038,.048,'silver')
    a.box((0,.035,.28),(2.76,.11,.11),'metal')
    a.box((0,-1.4,.19),(2.76,.045,.065),'silver')
    for x in (-1.07,1.07):
        a.cylinder((x,0,1.10),(x,-1.27,.22),.017,'steel',6)
        for y,z in ((0,1.10),(-1.27,.22)):
            a.box((x,y,z),(.13,.052,.075),'metal')
    return finish(a)


@entry('standing_seam_metal_canopy','large')
def standing_seam_metal_canopy():
    a=model('standing_seam_metal_canopy','large');ang=.18
    a.box((0,-.66,.65),(3.25,1.38,.055),'dark_metal',rot=(ang,0,0))
    for i in range(9):a.box((-1.56+i*.39,-.66,.69),(.023,1.4,.046),'metal',rot=(ang,0,0))
    a.box((0,-1.37,.48),(3.33,.075,.18),'dark_metal')
    for x in (-1.37,1.37):
        a.beam((x,0,.69),(x,-1.3,.45),.065,.05,'dark_metal')
        a.beam((x,0,.02),(x,-1.19,.45),.058,.05,'dark_metal')
        a.box((x,.025,.37),(.15,.06,.74),'metal')
    return finish(a)


@entry('gabled_entry_portico','large')
def gabled_entry_portico():
    a=model('gabled_entry_portico','large')
    for x in (-.94,.94):
        a.box((x,-1.02,1.17),(.13,.13,2.34),'white')
        for z in (.10,2.24):a.box((x,-1.02,z),(.22,.22,.16),'cream')
    a.box((0,-1.02,2.33),(2.22,.17,.19),'cream')
    xz_prism(a,[(-1.1,2.41),(1.1,2.41),(0,3.02)],-1.1,-.98,'white')
    slope=math.atan2(.65,1.17)
    for s in (-1,1):
        a.box((s*.585,-.53,2.73),(1.36,1.35,.095),'asphalt',rot=(0,s*slope,0))
        a.beam((s*1.18,-1.22,2.41),(0,-1.22,3.08),.075,.09,'cream')
    a.box((0,-.53,3.095),(.1,1.38,.055),'dark_metal')
    return finish(a)


@entry('retractable_shop_awning','large')
def retractable_shop_awning():
    a=model('retractable_shop_awning','large');ang=.16
    a.cylinder((-1.72,.03,.74),(1.72,.03,.74),.085,'metal',10)
    for i in range(12):a.box((-1.54+i*.28,-.85,.6),(.28,1.72,.025),'cream' if i%3 else 'brown',rot=(ang,0,0))
    a.box((0,-1.73,.45),(3.48,.06,.065),'white')
    for i in range(12):a.box((-1.54+i*.28,-1.74,.35),(.28,.022,.17),'cream' if i%3 else 'brown')
    for x in (-1.35,1.35):
        a.beam((x,0,.69),(x-.19,-.86,.38),.046,.03,'white')
        a.beam((x-.19,-.86,.38),(x,-1.7,.43),.046,.03,'white')
        a.cylinder((x-.19,-.86,.36),(x-.19,-.86,.41),.055,'metal',8)
        a.box((x,.07,.7),(.17,.12,.24),'dark_metal')
    return finish(a)


@entry('three_step_front_stoop','large')
def three_step_front_stoop():
    a=model('three_step_front_stoop','large');treads(a,1.6,3,.31,.17)
    a.box((0,1.26,.255),(1.6,.66,.51),'concrete')
    a.box((0,1.26,.525),(1.66,.68,.03),'concrete_light')
    for x in (-.75,.75):
        rail(a,(x,.18,.17),(x,.80,.51),.86,3,'dark_metal',False)
        rail(a,(x,.8,.51),(x,1.52,.51),.86,3,'dark_metal',False)
    return finish(a)


@entry('brownstone_entry_stair','large')
def brownstone_entry_stair():
    a=model('brownstone_entry_stair','large');treads(a,1.48,7,.28,.175,'brick')
    a.box((0,2.37,.6125),(1.48,.82,1.225),'brick')
    a.box((0,2.37,1.25),(1.59,.9,.06),'sand')
    for x in (-.88,.88):
        for i in range(7):a.box((x,(i+.5)*.28,(i+1)*.175/2),(.23,.28,(i+1)*.175+.16),'brown')
        rail(a,(x,.12,.34),(x,1.83,1.40),.8,9,'dark_metal')
        rail(a,(x,1.83,1.40),(x,2.73,1.40),.8,4,'dark_metal')
        a.box((x,.06,.44),(.3,.3,.88),'sand')
        a.box((x,.06,.94),(.36,.36,.11),'sand')
    return finish(a)


@entry('side_entry_stair_landing','large')
def side_entry_stair_landing():
    a=model('side_entry_stair_landing','large');treads(a,1.15,5,.28,.18)
    a.box((.55,1.96,.45),(2.25,1.12,.9),'concrete')
    a.box((.55,1.96,.925),(2.31,1.18,.05),'concrete_light')
    rail(a,(-.54,.16,.18),(-.54,1.27,.9),.92,6)
    rail(a,(-.54,1.27,.9),(-.54,2.45,.9),.92,5)
    rail(a,(-.54,2.45,.9),(1.62,2.45,.9),.92,10)
    rail(a,(.55,1.40,.9),(1.62,1.40,.9),.92,5)
    return finish(a)


@entry('raised_loading_dock_platform','large')
def raised_loading_dock_platform():
    a=model('raised_loading_dock_platform','large')
    a.box((0,0,.54),(3.5,1.8,1.08),'concrete');a.box((0,-.03,1.10),(3.59,1.88,.09),'concrete_light')
    for x in (-1.32,1.32):
        a.box((x,-.964,.65),(.23,.17,.55),'rubber')
        for z in (.47,.66,.84):a.box((x,-1.055,z),(.19,.025,.018),'black')
    a.box((0,-.953,.995),(2.4,.04,.15),'yellow')
    for x in (-.95,-.45,.05,.55,1.05):a.box((x,-.98,.995),(.11,.008,.155),'black',rot=(0,.27,0))
    a.box((0,-.32,1.154),(1.65,1.08,.025),'dark_metal')
    for i in range(9):a.box((-.72+i*.18,-.32,1.171),(.035,.94,.008),'metal')
    return finish(a)


@entry('loading_dock_door_seal','large')
def loading_dock_door_seal():
    a=model('loading_dock_door_seal','large');w=2.55;h=2.85
    for x in (-w/2-.13,w/2+.13):
        a.box((x,0,h/2),(.28,.43,h),'rubber')
        a.box((x,.23,h/2),(.34,.045,h+.05),'dark_metal')
        for i in range(14):a.box((x,-.223,.10+i*.20),(.29,.025,.022),'black')
        a.box((x,-.238,1.14),(.07,.012,1.85),'cream')
    a.box((0,0,h+.17),(w+.55,.43,.34),'rubber')
    for x in (-1.12,-.56,0,.56,1.12):a.box((x,-.23,h+.17),(.024,.021,.34),'black')
    for x in (-1.46,1.46):bolts(a,[x],-.245,[.2,1.4,2.65],'steel')
    return finish(a)


@entry('fire_escape_landing','large')
def fire_escape_landing():
    a=model('fire_escape_landing','large')
    for x in (-1.05,1.05):a.box((x,0,.18),(.095,1.2,.17),'dark_metal')
    for y in (-.57,.57):a.box((0,y,.18),(2.18,.09,.17),'dark_metal')
    for i in range(18):a.box((-.98+i*.115,0,.285),(.034,1.11,.03),'metal')
    for y in (-.38,0,.38):a.box((0,y,.263),(2.06,.018,.025),'dark_metal')
    rail(a,(-1.03,-.54,.30),(1.03,-.54,.30),1.02,13,'dark_metal',False)
    for x in (-1.03,1.03):
        rail(a,(x,-.54,.30),(x,.55,.30),1.02,7,'dark_metal',False)
        a.beam((x,.58,.03),(x,-.5,.2),.055,.065,'dark_metal')
        a.box((x,.61,.4),(.14,.06,.72),'dark_metal')
    return finish(a)


@entry('fire_escape_stair_flight','large')
def fire_escape_stair_flight():
    a=model('fire_escape_stair_flight','large');n=11;run=.235;rise=.19;w=.84
    for x in (-.47,.47):
        a.beam((x,-.07,.02),(x,n*run+.08,n*rise),.085,.16,'dark_metal')
        rail(a,(x,.12,.19),(x,(n-.5)*run,n*rise),.92,10,'dark_metal',False)
    for i in range(n):
        y=(i+.5)*run;z=(i+1)*rise
        for j in range(5):a.box((0,y-.09+j*.043,z),(w,.023,.035),'metal')
        a.box((0,y-.117,z-.02),(w,.027,.064),'dark_metal')
    return finish(a)


@entry('fire_escape_drop_ladder','large')
def fire_escape_drop_ladder():
    a=model('fire_escape_drop_ladder','large')
    for x in (-.29,.29):
        a.box((x,0,1.48),(.055,.06,2.96),'dark_metal')
        a.box((x,.10,2.51),(.1,.25,.1),'metal')
        a.cylinder((x,-.06,2.55),(x,.21,2.55),.043,'steel',8)
    for i in range(11):a.cylinder((-.29,-.01,.12+i*.267),(.29,-.01,.12+i*.267),.024,'metal',8)
    a.box((0,.33,2.84),(.84,.54,.075),'dark_metal')
    for x in (-.4,.4):rail(a,(x,.12,2.87),(x,.59,2.87),.84,3,'dark_metal',False)
    a.cylinder((.4,.05,2.53),(.4,.05,2.73),.025,'steel',8)
    return finish(a)


@entry('cantilever_apartment_balcony','large')
def cantilever_apartment_balcony():
    a=model('cantilever_apartment_balcony','large')
    a.box((0,0,.21),(2.75,1.3,.22),'concrete');a.box((0,0,.34),(2.79,1.34,.055),'concrete_light')
    rail(a,(-1.32,-.59,.38),(1.32,-.59,.38),1.06,14,'dark_metal',False)
    for x in (-1.32,1.32):rail(a,(x,-.59,.38),(x,.57,.38),1.06,6,'dark_metal',False)
    for x in (-.9,.9):
        a.beam((x,.56,.04),(x,-.53,.16),.08,.15,'dark_metal')
        a.box((x,.59,.13),(.19,.08,.26),'metal')
    return finish(a)


@entry('ornamental_juliet_balcony')
def ornamental_juliet_balcony():
    a=model('ornamental_juliet_balcony');w=1.55
    for z in (.10,.97):a.box((0,-.17,z),(w,.055,.06),'dark_metal')
    for x in (-.74,.74):
        a.box((x,-.17,.54),(.052,.052,1.08),'dark_metal')
        for z in (.12,.98):a.beam((x,-.17,z),(x,.08,z),.04,mat='dark_metal')
    for i in range(9):
        x=-.64+i*.16
        a.box((x,-.17,.53),(.019,.022,.85),'dark_metal')
    for x in (-.47,0,.47):
        a.torus((x,-.17,.57),.17,.012,'dark_metal',axis='y',segments=10,sides=5)
        a.box((x,-.17,.31),(.06,.029,.06),'dark_metal',rot=(0,math.pi/4,0))
    return finish(a)


@entry('open_rooftop_access_hatch')
def open_rooftop_access_hatch():
    a=model('open_rooftop_access_hatch');w=.86;d=1.05
    for x in (-w/2,w/2):a.box((x,0,.19),(.065,d,.38),'metal')
    for y in (-d/2,d/2):a.box((0,y,.19),(w+.065,.065,.38),'metal')
    a.box((0,.71,.93),(.99,.075,1.2),'concrete_light',rot=(.35,0,0))
    a.box((0,.674,.925),(.84,.06,1.05),'metal',rot=(.35,0,0))
    for x in (-.32,.32):
        a.cylinder((x,.49,.39),(x,.53,.49),.037,'steel',8)
    a.beam((.39,-.15,.3),(.39,.55,1.25),.024,.018,'steel')
    a.box((0,.47,1.35),(.22,.06,.032),'dark_metal')
    return finish(a)


@entry('curb_mounted_skylight')
def curb_mounted_skylight():
    a=model('curb_mounted_skylight')
    for x in (-.59,.59):a.box((x,0,.17),(.095,1.62,.34),'dark_metal')
    for y in (-.76,.76):a.box((0,y,.17),(1.26,.1,.34),'dark_metal')
    a.box((0,0,.38),(1.09,1.42,.04),'glass',rot=(.06,0,0))
    for x in (-.58,.58):a.box((x,0,.40),(.065,1.57,.07),'silver',rot=(.06,0,0))
    for y in (-.76,.76):a.box((0,y,.40+y*.06),(1.22,.065,.07),'silver')
    a.box((0,0,.419),(.043,1.45,.045),'silver',rot=(.06,0,0))
    for x in (-.66,.66):a.box((x,0,.045),(.15,1.78,.035),'metal')
    for y in (-.86,.86):a.box((0,y,.045),(1.45,.15,.035),'metal')
    return finish(a)


@entry('sawtooth_roof_glazing_module','large')
def sawtooth_roof_glazing_module():
    a=model('sawtooth_roof_glazing_module','large')
    for x0,x1 in ((-1.58,-1.52),(1.52,1.58)):
        yz_prism(a,[(-.65,0),(.65,0),(.35,1.02)],x0,x1,'metal')
    a.box((0,.485,.535),(3.08,.07,1.075),'glass',rot=(.29,0,0))
    for x in (-1.54,-.77,0,.77,1.54):a.beam((x,.65,.02),(x,.35,1.055),.045,.05,'silver')
    for z,y in ((.045,.642),(1.04,.353)):
        a.box((0,y,z),(3.18,.055,.065),'silver')
    a.box((0,-.16,.52),(3.16,1.45,.065),'asphalt',rot=(.8,0,0))
    a.box((0,.32,1.078),(3.24,.17,.05),'dark_metal')
    return finish(a)


@entry('parapet_coping_corner','large')
def parapet_coping_corner():
    a=model('parapet_coping_corner','large')
    a.box((0,0,.40),(2.4,.34,.8),'brick');a.box((1.03,.69,.4),(.34,1.04,.8),'brick')
    for row in range(5):
        z=.06+row*.15
        a.box((0,-.175,z),(2.4,.01,.013),'cream')
        for i in range(8):
            x=-1.16+i*.30+(.15 if row%2 else 0)
            if x<1.17:a.box((x,-.18,z+.071),(.01,.01,.13),'cream')
        a.box((.855,.69,z),(.01,1.04,.013),'cream')
    a.box((0,0,.84),(2.52,.47,.1),'concrete_light');a.box((1.03,.73,.84),(.47,1.13,.1),'concrete_light')
    for x in (-.62,.05,.72):a.box((x,-.243,.84),(.012,.007,.1),'concrete')
    return finish(a)


@entry('dentil_cornice_section','large')
def dentil_cornice_section():
    a=model('dentil_cornice_section','large')
    for y,z,d,h in ((.08,.13,.20,.26),(.005,.31,.35,.09),(-.04,.45,.43,.08),(-.065,.59,.50,.12)):
        a.box((0,y,z),(2.8,d,h),'cream')
    for i in range(14):a.box((-1.3+i*.2,-.15,.365),(.09,.19,.12),'concrete_light')
    for x in (-1.18,-.59,0,.59,1.18):
        a.box((x,-.08,.165),(.14,.26,.26),'cream')
        a.beam((x,-.08,.03),(x,-.21,.25),.13,.08,'cream')
    a.box((0,-.07,.682),(2.93,.57,.07),'concrete_light')
    return finish(a)


@entry('brick_arch_window_lintel')
def brick_arch_window_lintel():
    a=model('brick_arch_window_lintel');r=.68
    for i in range(15):
        t0=i*math.pi/15+.012;t1=(i+1)*math.pi/15-.012
        pts=[(r*math.cos(t0),r*math.sin(t0)),((r+.22)*math.cos(t0),(r+.22)*math.sin(t0)),((r+.22)*math.cos(t1),(r+.22)*math.sin(t1)),(r*math.cos(t1),r*math.sin(t1))]
        xz_prism(a,pts,-.13,.13,'brick')
    # Enlarged limestone keystone and spring blocks.
    xz_prism(a,[(-.073,.62),(.073,.62),(.12,.96),(-.12,.96)],-.17,.17,'sand')
    for s in (-1,1):a.box((s*.79,0,-.065),(.29,.32,.13),'sand')
    return finish(a)


@entry('limestone_window_surround')
def limestone_window_surround():
    a=model('limestone_window_surround');w=1.12;h=1.63
    for x in (-.65,.65):
        for i in range(4):a.box((x,0,.20+i*.41),(.18,.25,.39),'concrete_light')
        a.box((x,-.092,.82),(.065,.085,1.65),'cream')
    a.box((0,-.015,1.73),(1.53,.33,.2),'concrete_light')
    a.box((0,-.06,1.88),(1.65,.40,.095),'cream')
    a.box((0,-.1,-.06),(1.58,.48,.13),'concrete_light')
    for x in (-.47,.47):a.box((x,-.03,-.2),(.17,.25,.17),'cream')
    xz_prism(a,[(-.07,1.65),(.07,1.65),(.13,1.85),(-.13,1.85)],-.21,-.08,'sand')
    return finish(a)


@entry('classical_entry_pediment','large')
def classical_entry_pediment():
    a=model('classical_entry_pediment','large')
    for x in (-.84,.84):
        a.box((x,0,1.12),(.20,.21,2.24),'cream')
        for dx in (-.052,0,.052):a.box((x+dx,-.116,1.2),(.023,.02,1.8),'concrete_light')
        for z,h,w in ((.10,.2,.32),(2.22,.14,.33),(2.34,.08,.39)):
            a.box((x,-.025,z),(w,.30,h),'concrete_light')
    a.box((0,0,2.43),(2.14,.34,.14),'cream')
    xz_prism(a,[(-1.06,2.53),(1.06,2.53),(0,3.01)],-.16,.12,'cream')
    for s in (-1,1):a.beam((s*1.14,-.18,2.52),(0,-.18,3.07),.085,.09,'concrete_light')
    a.box((0,-.12,2.54),(2.31,.46,.085),'concrete_light')
    return finish(a)


@entry('masonry_chimney_stack','large')
def masonry_chimney_stack():
    a=model('masonry_chimney_stack','large')
    a.box((0,0,.74),(.82,.62,1.48),'brick')
    for row in range(10):
        z=.065+row*.143
        for y in (-.315,.315):
            a.box((0,y,z),(.825,.008,.012),'cream')
            for x in ((-.20,.2) if row%2 else (-.4,0,.4)):
                a.box((x,y,z+.068),(.011,.008,.12),'cream')
        for x in (-.415,.415):a.box((x,0,z),(.008,.62,.012),'cream')
    a.box((0,0,1.50),(.98,.78,.12),'concrete_light')
    for x in (-.2,.2):
        for yy in (-.16,.16):a.box((x,yy,1.68),(.26,.055,.27),'terracotta')
        for xx in (x-.13,x+.13):a.box((xx,0,1.68),(.055,.28,.27),'terracotta')
    a.box((0,0,.035),(.99,.81,.07),'dark_metal')
    return finish(a)


@entry('rooftop_stair_headhouse','large')
def rooftop_stair_headhouse():
    a=model('rooftop_stair_headhouse','large')
    a.box((0,.25,1.2),(1.66,1.85,2.4),'brick')
    a.box((0,-.703,1.02),(.92,.10,2.04),'metal')
    frame(a,.94,2.06,0,-.715,.065,.15,'concrete_light')
    a.box((0,-.786,.26),(.8,.02,.35),'steel');knob(a,.35,1.05,-.8,'steel')
    a.box((0,-.78,1.69),(.29,.018,.26),'black');pane(a,0,1.69,.24,.21,-.795)
    a.box((0,.25,2.46),(1.9,2.10,.16),'dark_metal',rot=(.045,0,0))
    for z in (.38,.78,1.18,1.58,1.98,2.32):
        for x in (-.842,.842):a.box((x,.25,z),(.014,1.83,.018),'cream')
    a.box((0,-.92,.055),(1.16,.45,.11),'concrete_light')
    return finish(a)


@entry('entrance_threshold_ramp','large')
def entrance_threshold_ramp():
    a=model('entrance_threshold_ramp','large')
    yz_prism(a,[(-1.35,0),(1.15,0),(1.15,.24),(.55,.24),(-1.35,.025)],-.67,.67,'metal')
    for i in range(17):
        y=-1.27+i*.11;z=.028+(y+1.35)*.215/1.9
        a.box((0,y,z+.008),(1.29,.018,.012),'dark_metal')
    for x in (-.67,.67):
        a.beam((x,-1.31,.045),(x,.55,.265),.045,.055,'dark_metal')
        a.box((x,.85,.27),(.045,.60,.08),'dark_metal')
    a.box((0,.84,.25),(1.28,.54,.026),'metal')
    for x in (-.55,.55):bolts(a,[x],1.158,[.13],'steel')
    return finish(a)


@entry('foundation_crawlspace_hatch')
def foundation_crawlspace_hatch():
    a=model('foundation_crawlspace_hatch');frame(a,.92,.67,t=.08,d=.2,mat='concrete')
    a.box((0,-.035,.335),(.88,.065,.63),'dark_metal')
    for i in range(5):a.box((-.34+i*.17,-.077,.335),(.143,.025,.54),'wood_dark')
    for z in (.13,.54):a.box((0,-.10,z),(.82,.04,.06),'metal')
    a.beam((-.36,-.125,.16),(.36,-.125,.51),.04,.026,'metal')
    for z in (.13,.54):
        a.box((-.4,-.125,z),(.18,.02,.085),'dark_metal')
        bolts(a,[-.45,-.35],-.139,[z],'steel')
    pull(a,.31,.33,-.145,.14,'steel')
    a.box((.41,-.137,.33),(.12,.02,.047),'steel')
    a.torus((.405,-.166,.302),.025,.008,'gold',axis='y',segments=8,sides=4)
    a.box((.405,-.165,.276),(.052,.033,.041),'gold')
    return finish(a)
