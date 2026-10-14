"""Fifty distinct roadside, traffic-control, and parking props; metres, Z up."""
import math
from assetlib import Asset, register

# Common front face is -Y. Vector strokes provide legible markings without fonts.
METAL='metal'; DARK='dark_metal'; WHITE='white'; BLACK='black'; RED='red'
YELLOW='yellow'; ORANGE='orange'; BLUE='blue'; GREEN='green'; CONCRETE='concrete'; RUBBER='rubber'; GLASS='glass'

def asset(n,cat='traffic',size='person'):
    return Asset('b02_'+n,cat,size_class=size)

def rod(a,p,q,r=.018,mat=METAL,sides=8): a.cylinder(p,q,r,mat=mat,sides=sides)
def box(a,p,s,mat=METAL): a.box(p,s,mat=mat)
def face_stroke(a,pts,y=-.061,mat=BLACK,width=.014):
    for p,q in zip(pts,pts[1:]): rod(a,(p[0],y,p[1]),(q[0],y,q[1]),width,mat,4)
def ring(a,x,z,r,y=-.064,mat=BLACK,width=.016):
    pts=[(x+math.cos(i*math.tau/20)*r,z+math.sin(i*math.tau/20)*r) for i in range(21)]
    face_stroke(a,pts,y,mat,width)
def pole(a,height=2.5,x=0,y=.035,r=.028,base=True):
    rod(a,(x,y,.025),(x,y,height),r,METAL)
    if base:
        box(a,(x,y,.026),(.18,.18,.052),DARK)
        for dx in (-.06,.06):
            for dy in (-.06,.06): rod(a,(x+dx,y+dy,.051),(x+dx,y+dy,.063),.012,METAL,6)
def plate(a,x,z,w,h,mat=WHITE,y=0):
    corner=min(.035,w*.08,h*.08)
    pts=[(x-w/2+corner,z-h/2),(x+w/2-corner,z-h/2),(x+w/2,z-h/2+corner),(x+w/2,z+h/2-corner),(x+w/2-corner,z+h/2),(x-w/2+corner,z+h/2),(x-w/2,z+h/2-corner),(x-w/2,z-h/2+corner)]
    profile(a,pts,y+.015,y-.031,METAL)
    profile(a,[(x+(xx-x)*(.976),z+(zz-z)*(.976)) for xx,zz in pts],y-.032,y-.044,mat)
    # A stamped sign bolts through two rear saddles, so it is not floating on a pole.
    for zz in (z-h*.32,z+h*.32):
        box(a,(x,y+.027,zz),(min(w*.65,.24),.045,.035),DARK)
        rod(a,(x,y-.045,zz),(x,y-.053,zz),.009,METAL,6)
def profile(a,points,yback,yfront,mat):
    area=sum(points[i][0]*points[(i+1)%len(points)][1]-points[(i+1)%len(points)][0]*points[i][1] for i in range(len(points)))
    if area<0: points=list(reversed(points))
    n=len(points); vs=[(x,y,z) for y in (yback,yfront) for x,z in points]
    a.mesh(vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat=mat)
def poly_plate(a,z,r,sides,mat=YELLOW,y=0):
    angle=math.pi/8 if sides==8 else 0
    pts=[(r*math.cos(angle+i*math.tau/sides),z+r*math.sin(angle+i*math.tau/sides)) for i in range(sides)]
    if sides==5: pts=[(-r*.86,z-r*.72),(r*.86,z-r*.72),(r*.86,z+r*.22),(0,z+r),(-r*.86,z+r*.22)]
    profile(a,pts,y+.01,y-.033,METAL)
    profile(a,[(x*.95,z+(zz-z)*.95) for x,zz in pts],y-.034,y-.043,mat)
def arrow(a,x,z,w=.38,h=.22,y=-.063,mat=BLACK,direction=1):
    face_stroke(a,[(x-direction*w/2,z),(x+direction*w/2,z)],y,mat,.025)
    face_stroke(a,[(x+direction*(w/2-h/2),z+h/2),(x+direction*w/2,z),(x+direction*(w/2-h/2),z-h/2)],y,mat,.028)

# Simple uppercase engineering lettering, each glyph is real low-poly mesh.
FONT={
 'A':[[(0,0),(.5,1),(1,0)],[(.23,.43),(.77,.43)]],
 'B':[[(0,0),(0,1),(.7,1),(1,.75),(.65,.5),(0,.5)],[(.65,.5),(1,.25),(.7,0),(0,0)]],
 'C':[[(1,.95),(.25,1),(0,.75),(0,.25),(.25,0),(1,.05)]],
 'D':[[(0,0),(0,1),(.65,1),(1,.75),(1,.25),(.65,0),(0,0)]],
 'E':[[(1,1),(0,1),(0,0),(1,0)],[(0,.5),(.8,.5)]],
 'F':[[(0,0),(0,1),(1,1)],[(0,.5),(.8,.5)]],
 'G':[[(1,.95),(.25,1),(0,.75),(0,.25),(.25,0),(1,.05),(1,.5),(.6,.5)]],
 'K':[[(0,0),(0,1)],[(1,1),(0,.45),(1,0)]],
 'V':[[(0,1),(.5,0),(1,1)]],
 'H':[[(0,0),(0,1)],[(1,0),(1,1)],[(0,.5),(1,.5)]],
 'I':[[('.5',0),('.5',1)]],
 'L':[[(0,1),(0,0),(1,0)]],
 'M':[[(0,0),(0,1),(.5,.5),(1,1),(1,0)]],
 'N':[[(0,0),(0,1),(1,0),(1,1)]],
 'O':[[(.2,0),(0,.2),(0,.8),(.2,1),(.8,1),(1,.8),(1,.2),(.8,0),(.2,0)]],
 'P':[[(0,0),(0,1),(.8,1),(1,.8),(1,.6),(.8,.5),(0,.5)]],
 'R':[[(0,0),(0,1),(.8,1),(1,.8),(1,.6),(.8,.5),(0,.5)],[(.5,.5),(1,0)]],
 'S':[[(1,1),(.2,1),(0,.8),(.2,.5),(.8,.5),(1,.2),(.8,0),(0,0)]],
 'T':[[(0,1),(1,1)],[(.5,1),(.5,0)]],
 'U':[[(0,1),(0,.2),(.2,0),(.8,0),(1,.2),(1,1)]],
 'W':[[(0,1),(.2,0),(.5,.5),(.8,0),(1,1)]],
 'X':[[(0,0),(1,1)],[(0,1),(1,0)]],
 'Y':[[(0,1),(.5,.5),(1,1)],[(.5,.5),(.5,0)]],
 '2':[[(0,.8),(.2,1),(.8,1),(1,.8),(1,.65),(0,0),(1,0)]],
 '5':[[(1,1),(0,1),(0,.5),(.8,.5),(1,.3),(1,.1),(.8,0),(0,0)]],
 '0':[[(.2,0),(0,.2),(0,.8),(.2,1),(.8,1),(1,.8),(1,.2),(.8,0),(.2,0)]],
 '8':[[(.2,.5),(0,.7),(0,.85),(.2,1),(.8,1),(1,.85),(1,.7),(.8,.5),(.2,.5),(0,.3),(0,.15),(.2,0),(.8,0),(1,.15),(1,.3),(.8,.5)]],
 '3':[[(0,1),(.8,1),(1,.8),(.7,.5),(1,.2),(.8,0),(0,0)],[(.3,.5),(.7,.5)]],
 '6':[[(.9,1),(.3,1),(0,.7),(0,.2),(.2,0),(.8,0),(1,.2),(1,.4),(.8,.6),(0,.6)]],
 '4':[[(.8,0),(.8,1),(0,.3),(1,.3)]],
 '1':[[('.2',.8),('.5',1),('.5',0)],[(.1,0),(.9,0)]],
 '-':[[(0,.5),(1,.5)]],
}
def text(a,s,x,z,w,h,y=-.066,mat=BLACK,stroke=.007):
    spacing=1.35; charw=w/(max(1,len(s))*spacing-.35)
    for i,ch in enumerate(s):
        for line in FONT.get(ch,[]):
            face_stroke(a,[(x-w/2+i*charw*spacing+float(px)*charw,z-h/2+float(pz)*h) for px,pz in line],y,mat,stroke)
def person(a,x,z,scale=1,y=-.065,mat=BLACK,walking=True):
    rod(a,(x,y,z+.20*scale),(x,y-.003,z+.20*scale),.054*scale,mat,8)
    face_stroke(a,[(x,z+.115*scale),(x-.03*scale,z-.02*scale),(x+.065*scale,z-.15*scale)],y,mat,.031*scale)
    face_stroke(a,[(x-.025*scale,z-.005*scale),(x-.12*scale,z-.145*scale)],y,mat,.025*scale)
    face_stroke(a,[(x-.005*scale,z+.08*scale),(x-.10*scale,z+.015*scale),(x-.17*scale,z+.015*scale)],y,mat,.022*scale)
    face_stroke(a,[(x,z+.08*scale),(x+.09*scale,z+.025*scale)],y,mat,.023*scale)
def sign_base(n,shape='rect',mat=WHITE,w=.65,h=.85,z=2.0):
    a=asset(n,'signage'); pole(a,z+.36)
    if shape=='rect': plate(a,0,z,w,h,mat)
    else:
        poly_plate(a,z,w/2,shape,mat)
        for zz in (z-w*.22,z+w*.22):
            box(a,(0,.031,zz),(.15,.045,.035),DARK)
            rod(a,(0,-.044,zz),(0,-.052,zz),.009,METAL,6)
    return a


def stop_sign():
    a=sign_base('stop_sign',8,RED,w=.78,z=2.08)
    text(a,'STOP',0,2.08,.55,.18,mat=WHITE,stroke=.012)
    return a

def yield_sign():
    a=asset('yield_sign','signage'); pole(a,2.44)
    profile(a,[(-.41,2.37),(.41,2.37),(0,1.66)],.025,-.032,RED)
    profile(a,[(-.30,2.30),(.30,2.30),(0,1.78)],-.033,-.045,WHITE)
    text(a,'YIELD',0,2.19,.40,.095,stroke=.006)
    return a

def speed_limit():
    a=sign_base('speed_limit_25',w=.66,h=.88,z=2.05)
    text(a,'SPEED',0,2.34,.48,.095,stroke=.006)
    text(a,'LIMIT',0,2.18,.43,.095,stroke=.006)
    text(a,'25',0,1.91,.35,.27,stroke=.014)
    return a

def one_way():
    a=sign_base('one_way_arrow',w=1.04,h=.39,z=2.15,mat=BLACK)
    arrow(a,0,2.15,.77,.24,mat=WHITE)
    return a

def do_not_enter():
    a=sign_base('do_not_enter',12,RED,w=.74,z=2.10)
    box(a,(0,-.062,2.10),(.52,.018,.15),WHITE)
    text(a,'DO NOT',0,2.30,.45,.078,mat=WHITE,stroke=.005)
    text(a,'ENTER',0,1.90,.40,.078,mat=WHITE,stroke=.005)
    return a

def wrong_way():
    a=sign_base('wrong_way',w=.80,h=.52,z=2.05,mat=RED)
    text(a,'WRONG',0,2.16,.60,.12,mat=WHITE,stroke=.009)
    text(a,'WAY',0,1.94,.42,.12,mat=WHITE,stroke=.009)
    return a

def no_left_turn():
    a=sign_base('no_left_turn',w=.70,h=.75,z=2.08)
    face_stroke(a,[(.13,1.84),(.13,2.14),(-.15,2.14)],mat=BLACK,width=.035)
    face_stroke(a,[(-.02,2.27),(-.15,2.14),(-.02,2.02)],width=.025)
    ring(a,0,2.08,.27,mat=RED,width=.026)
    face_stroke(a,[(-.2,2.30),(.2,1.86)],-.079,RED,.024)
    return a

def no_u_turn():
    a=sign_base('no_u_turn',w=.70,h=.75,z=2.08)
    face_stroke(a,[(.13,1.88),(.13,2.20),(.07,2.26),(-.07,2.26),(-.13,2.20),(-.13,1.99)],width=.027)
    face_stroke(a,[(-.23,2.09),(-.13,1.98),(-.03,2.09)],width=.025)
    ring(a,0,2.08,.275,mat=RED,width=.024)
    face_stroke(a,[(-.21,2.29),(.21,1.87)],-.079,RED,.024)
    return a

def pedestrian_crossing():
    a=sign_base('pedestrian_crossing',4,YELLOW,w=1.00,z=2.10)
    person(a,0,2.11,1)
    for zz in (1.87,1.82): box(a,(0,-.065,zz),(.36,.01,.015),BLACK)
    return a

def school_crossing():
    a=sign_base('school_crossing',5,YELLOW,w=.93,z=2.07)
    person(a,-.12,2.06,.80); person(a,.16,2.04,.61)
    face_stroke(a,[(-.055,2.08),(.10,2.08)],width=.015)
    box(a,(.24,-.065,2.035),(.07,.014,.09),BLACK)
    return a

def bike_route():
    a=sign_base('bike_route',w=.69,h=.74,z=2.08,mat=GREEN)
    ring(a,-.17,2.09,.095,mat=WHITE,width=.009); ring(a,.17,2.09,.095,mat=WHITE,width=.009)
    face_stroke(a,[(-.17,2.09),(-.06,2.25),(.06,2.09),(-.17,2.09),(.12,2.24),(.17,2.09)],mat=WHITE,width=.01)
    face_stroke(a,[(.12,2.24),(.09,2.30),(.17,2.30)],mat=WHITE,width=.01)
    text(a,'BIKE',0,1.86,.39,.09,mat=WHITE,stroke=.006)
    return a

def railroad_crossbuck():
    a=asset('railroad_crossbuck','signage'); pole(a,2.87)
    for angle,word in ((-.58,'RAILROAD'),(.58,'CROSSING')):
        a.box((0,-.018,2.35),(1.65,.075,.19),mat=WHITE,rot=(0,angle,0))
        # Transform glyph vertices together into the diagonal blade plane.
        start=len(a.vertices)
        text(a,word,0,0,1.43,.098,y=-.07,stroke=.007)
        for i in range(start,len(a.vertices)):
            x,y,z=a.vertices[i]; a.vertices[i]=(x*math.cos(angle)+z*math.sin(angle),y,z*math.cos(angle)-x*math.sin(angle)+2.35)
    return a

def street_name_pair():
    a=asset('street_name_pair','signage'); pole(a,2.95)
    plate(a,0,2.80,1.20,.23,GREEN)
    text(a,'MAIN ST',0,2.80,1.00,.10,mat=WHITE,stroke=.008)
    # Perpendicular second street blade with edge stripes.
    box(a,(0,.02,2.52),(.065,1.12,.23),GREEN)
    for zz in (2.42,2.62): box(a,(-.039,.02,zz),(.016,1.06,.018),WHITE)
    return a

def parking_sign():
    a=sign_base('public_parking_sign',w=.62,h=.73,z=2.12,mat=BLUE)
    text(a,'P',0,2.16,.23,.39,mat=WHITE,stroke=.024)
    arrow(a,0,1.88,.32,.14,mat=WHITE)
    return a

def accessible_sign():
    a=sign_base('accessible_parking_sign',w=.62,h=.78,z=2.10,mat=BLUE)
    rod(a,(0,-.065,2.32),(0,-.073,2.32),.044,WHITE,8)
    ring(a,-.04,1.99,.135,mat=WHITE,width=.016)
    face_stroke(a,[(0,2.23),(.015,2.06),(.14,2.06),(.19,1.93),(.25,1.93)],mat=WHITE,width=.019)
    face_stroke(a,[(.005,2.15),(.15,2.15)],mat=WHITE,width=.015)
    return a

def no_parking_sign():
    a=sign_base('no_parking_sign',w=.62,h=.80,z=2.10)
    text(a,'P',0,2.16,.19,.30,stroke=.022)
    ring(a,0,2.16,.24,mat=RED,width=.024)
    face_stroke(a,[(-.18,2.34),(.18,1.98)],-.079,RED,.024)
    arrow(a,0,1.82,.37,.13,mat=RED)
    return a

def bus_stop_sign():
    a=sign_base('bus_stop_sign',w=.49,h=.86,z=2.12,mat=BLUE)
    box(a,(0,-.063,2.24),(.27,.018,.28),WHITE)
    box(a,(0,-.078,2.28),(.22,.016,.12),BLUE)
    for xx in (-.085,.085):
        box(a,(xx,-.077,2.08),(.047,.02,.08),WHITE)
        rod(a,(xx,-.086,2.18),(xx,-.094,2.18),.025,BLUE,8)
    text(a,'BUS',0,1.88,.29,.10,mat=WHITE,stroke=.008)
    return a

def interstate_direction():
    a=asset('interstate_80_direction','signage'); pole(a,2.62)
    # Interstate shield has a notched crown, rounded shoulders and tapered foot.
    shield=[(-.34,2.46),(-.23,2.50),(0,2.46),(.23,2.50),(.34,2.46),(.32,2.10),(.21,1.95),(0,1.86),(-.21,1.95),(-.32,2.10)]
    profile(a,shield,.03,-.038,WHITE)
    profile(a,[(x*.92,2.2+(z-2.2)*.92) for x,z in shield],-.039,-.047,BLUE)
    profile(a,[(-.302,2.445),(-.21,2.469),(0,2.433),(.21,2.469),(.302,2.445),(.297,2.355),(-.297,2.355)],-.048,-.055,RED)
    text(a,'80',0,2.20,.39,.25,mat=WHITE,stroke=.013)
    plate(a,0,1.63,.66,.25,GREEN); arrow(a,0,1.63,.40,.14,mat=WHITE)
    return a

def detour_sign():
    a=sign_base('construction_detour_sign',4,ORANGE,w=1.04,z=1.66)
    text(a,'DETOUR',0,1.77,.54,.105,stroke=.009)
    arrow(a,0,1.55,.40,.15)
    # Weighted work-zone stand.
    box(a,(0,.035,.065),(.84,.50,.13),RUBBER)
    return a

def road_closed_barricade():
    a=asset('road_closed_barricade','traffic','large')
    for x in (-1.05,1.05):
        for y in (-.35,.35): rod(a,(x,y,.05),(x,0,1.32),.038,METAL,6)
        box(a,(x,0,.08),(.18,.85,.08),DARK)
    for z in (.45,.80,1.15):
        box(a,(0,0,z),(2.48,.075,.20),WHITE)
        for i in range(8): face_stroke(a,[(-1.16+i*.32,z-.095),(-1.04+i*.32,z+.095)],-.047,ORANGE,.049)
    plate(a,0,1.53,1.50,.47,WHITE)
    text(a,'ROAD',0,1.65,.64,.12,stroke=.01)
    text(a,'CLOSED',0,1.43,.93,.12,stroke=.01)
    return a


def lamp_housing(a,x,y,z,axis='vertical',scale=1,backplate=True):
    if axis=='vertical': dims=(.33*scale,.29*scale,.99*scale)
    else: dims=(.99*scale,.29*scale,.33*scale)
    if backplate: box(a,(x,y+.07,z),(dims[0]+.12*scale,.045*scale,dims[2]+.12*scale),DARK)
    box(a,(x,y,z),dims,YELLOW)
    for i,mat in enumerate((RED,YELLOW,GREEN)):
        lx=x+(i-1)*.31*scale if axis=='horizontal' else x
        lz=z+(1-i)*.31*scale if axis=='vertical' else z
        rod(a,(lx,y-.15*scale,lz),(lx,y-.23*scale,lz),.131*scale,BLACK,12)
        rod(a,(lx,y-.236*scale,lz),(lx,y-.243*scale,lz),.105*scale,mat,12)
        # Rolled semicircular visor shelters the lens above and at both sides.
        vs=[];steps=8
        for yy,rr in ((y-.16*scale,.145*scale),(y-.38*scale,.145*scale),(y-.38*scale,.133*scale),(y-.16*scale,.133*scale)):
            for j in range(steps+1):
                th=math.pi*j/steps;vs.append((lx+rr*math.cos(th),yy,lz+rr*math.sin(th)))
        fs=[(k*9+j,k*9+j+1,(k+1)*9+j+1,(k+1)*9+j) for k in range(3) for j in range(8)]
        fs += [(0,9,18,27),(8,35,26,17)];a.mesh(vs,fs,DARK)
        for dx in (-.145,.145):
            rod(a,(lx+dx*scale,y-.149*scale,lz),(lx+dx*scale,y-.16*scale,lz),.014*scale,METAL,6)
        box(a,(lx,y+.153*scale,lz),(.25*scale,.024*scale,.255*scale),DARK)
    for sign in (-1,1):
        pz=z+sign*(dims[2]*.5+.04*scale)
        rod(a,(x,y+.11,pz),(x,y+.25,pz),.036*scale,DARK,8)

def vertical_signal():
    a=asset('vertical_traffic_signal','traffic')
    pole(a,3.2,r=.055); rod(a,(0,.05,2.75),(.37,.05,2.75),.038)
    lamp_housing(a,.40,-.04,2.64)
    return a

def horizontal_signal():
    a=asset('horizontal_traffic_signal','traffic')
    pole(a,2.60,r=.058); rod(a,(0,.06,2.48),(.46,.06,2.48),.035)
    lamp_housing(a,.50,-.03,2.48,'horizontal')
    return a

def mast_arm_signal():
    a=asset('mast_arm_traffic_signal','traffic','large')
    pole(a,5.9,x=-2.5,r=.095)
    rod(a,(-2.5,.035,5.75),(-2.15,.035,6.05),.08)
    rod(a,(-2.15,.035,6.05),(2.7,.035,6.05),.065)
    for x in (-.15,2.1):
        rod(a,(x,.035,6.02),(x,.035,5.38),.035)
        lamp_housing(a,x,-.06,4.91,scale=1.13)
    box(a,(-2.5,.035,.2),(.36,.36,.4),METAL)
    return a

def pedestrian_signal():
    a=asset('pedestrian_walk_signal','traffic')
    pole(a,2.55,r=.055)
    box(a,(.33,0,2.12),(.61,.34,.61),YELLOW)
    box(a,(.33,-.183,2.12),(.52,.029,.52),BLACK)
    person(a,.34,2.07,.86,y=-.213,mat=WHITE)
    box(a,(.33,-.10,2.46),(.70,.57,.055),DARK)
    rod(a,(0,.03,2.14),(.20,.03,2.14),.034)
    box(a,(-.07,-.06,1.12),(.13,.14,.24),YELLOW)
    rod(a,(-.07,-.14,1.12),(-.07,-.16,1.12),.039,BLACK,12)
    return a

def flashing_beacon():
    a=asset('flashing_school_beacon','traffic')
    pole(a,2.74,r=.044)
    plate(a,0,1.89,.64,.78,YELLOW)
    text(a,'SCHOOL',0,2.08,.51,.085,stroke=.005)
    text(a,'25',0,1.82,.31,.23,stroke=.013)
    for z in (1.31,2.50):
        box(a,(0,-.03,z),(.35,.23,.35),BLACK)
        rod(a,(0,-.15,z),(0,-.20,z),.129,YELLOW,12)
        box(a,(0,-.20,z+.17),(.40,.22,.03),DARK)
    return a

def railroad_gate():
    a=asset('railroad_crossing_gate','traffic','large')
    box(a,(0,0,.50),(.55,.49,1.0),METAL)
    rod(a,(0,-.3,.97),(0,.3,.97),.18,DARK,12)
    box(a,(1.72,-.32,.99),(3.8,.15,.14),WHITE)
    for x in (.35,1.1,1.85,2.6,3.35): box(a,(x,-.405,.99),(.30,.018,.14),RED)
    pole(a,2.52,x=-.05,y=.15,r=.065,base=False)
    rod(a,(-.74,.10,2.15),(.64,.10,2.15),.04)
    for x in (-.51,.42):
        rod(a,(x,.06,2.15),(x,-.04,2.15),.245,BLACK,12)
        rod(a,(x,-.05,2.15),(x,-.09,2.15),.15,RED,12)
        box(a,(x,-.11,2.40),(.43,.35,.035),BLACK)
    rod(a,(-.05,.15,2.59),(-.05,.15,2.70),.11,BLACK,10)
    return a

def traffic_camera():
    a=asset('traffic_camera_pole','traffic')
    pole(a,3.28,r=.055)
    rod(a,(0,.05,3.12),(.52,.05,3.12),.04)
    box(a,(.52,-.03,3.12),(.29,.61,.26),WHITE)
    box(a,(.52,-.29,3.15),(.36,.36,.055),METAL)
    rod(a,(.52,-.35,3.105),(.52,-.41,3.105),.084,BLACK,12)
    rod(a,(.52,-.415,3.105),(.52,-.422,3.105),.055,GLASS,12)
    box(a,(0,.07,1.41),(.32,.27,.46),METAL)
    box(a,(0,-.074,1.41),(.275,.025,.40),DARK)
    rod(a,(.52,-.03,2.95),(.52,-.03,3.01),.046,DARK,8)
    a.tube([(.42,.20,3.02),(.19,.21,2.98),(.01,.11,2.81),(.01,.11,1.64)],.015,BLACK,6)
    for z in (1.28,1.53):box(a,(-.145,-.077,z),(.032,.035,.04),METAL)
    return a

def traffic_cabinet():
    a=asset('traffic_control_cabinet','traffic')
    box(a,(0,0,.065),(.81,.56,.13),CONCRETE)
    box(a,(0,0,.77),(.72,.46,1.41),METAL)
    box(a,(0,0,1.51),(.79,.53,.07),DARK)
    box(a,(0,-.245,.79),(.65,.027,1.26),WHITE)
    for z in [ .26+i*.054 for i in range(7) ]: box(a,(0,-.266,z),(.49,.020,.025),DARK)
    for z in (.34,1.2): box(a,(-.32,-.265,z),(.033,.04,.11),METAL)
    box(a,(.25,-.28,.85),(.027,.055,.16),DARK)
    rod(a,(.25,-.31,.70),(.25,-.325,.70),.022,BLACK,8)
    return a


def meter_head(a,x,z,y=0):
    box(a,(x,y,z),(.23,.19,.34),METAL)
    rod(a,(x,y-.095,z+.17),(x,y+.095,z+.17),.115,METAL,8)
    box(a,(x,y-.105,z+.08),(.17,.014,.12),BLACK)
    box(a,(x,y-.115,z+.08),(.12,.008,.063),GREEN)
    box(a,(x+.058,y-.118,z-.045),(.052,.016,.008),BLACK)
    rod(a,(x-.043,y-.12,z-.06),(x-.043,y-.16,z-.06),.036,DARK,8)
    face_stroke(a,[(x-.04,z-.06),(x-.04,z-.025)],y-.17,WHITE,.008)
    box(a,(x,y-.102,z-.13),(.13,.017,.026),DARK)
    box(a,(x,y+.102,z-.015),(.19,.022,.255),DARK)
    rod(a,(x,y+.115,z-.05),(x,y+.125,z-.05),.019,METAL,8)
    for dx in (-.083,.083):rod(a,(x+dx,y-.111,z-.12),(x+dx,y-.121,z-.12),.008,METAL,6)

def single_meter():
    a=asset('single_parking_meter','parking'); pole(a,1.35,r=.039)
    meter_head(a,0,1.40); return a

def dual_meter():
    a=asset('dual_parking_meter','parking'); pole(a,1.23,r=.045)
    rod(a,(-.23,.02,1.21),(.23,.02,1.21),.042)
    meter_head(a,-.23,1.41); meter_head(a,.23,1.41)
    box(a,(0,.02,.89),(.14,.13,.25),DARK)
    return a

def pay_station():
    a=asset('parking_pay_station','parking')
    box(a,(0,0,.045),(.59,.40,.09),DARK)
    box(a,(0,0,.84),(.46,.30,1.60),DARK)
    box(a,(0,-.164,1.04),(.39,.025,.93),METAL)
    box(a,(0,-.185,1.28),(.29,.022,.23),BLACK)
    box(a,(0,-.201,1.28),(.245,.010,.178),BLUE)
    for x in (-.065,0,.065):
        for z in (.91,.97,1.03): box(a,(x,-.197,z),(.043,.018,.035),BLACK)
    box(a,(0,-.2,.76),(.22,.016,.055),BLACK)
    box(a,(.125,-.20,1.10),(.055,.015,.012),BLACK)
    box(a,(0,0,1.71),(.62,.53,.055),BLACK)
    for x in (-.20,0,.20): box(a,(x,-.005,1.742),(.16,.43,.014),BLUE)
    text(a,'P',0,.48,.15,.24,y=-.17,mat=WHITE,stroke=.015)
    return a

def gate_arm():
    a=asset('parking_gate_arm','parking','large')
    box(a,(0,0,.59),(.48,.44,1.18),YELLOW)
    box(a,(0,0,1.21),(.54,.49,.08),DARK)
    rod(a,(0,-.23,1.04),(0,-.36,1.04),.14,METAL,12)
    box(a,(1.72,-.34,1.04),(3.65,.11,.13),WHITE)
    for x in (.42,1.17,1.92,2.67,3.42): box(a,(x,-.402,1.04),(.33,.018,.13),RED)
    rod(a,(-.12,-.231,.90),(-.12,-.25,.90),.04,BLACK,8)
    box(a,(0,-.23,.41),(.37,.02,.60),YELLOW)
    return a

def ticket_dispenser():
    a=asset('parking_ticket_dispenser','parking')
    box(a,(0,0,.04),(.58,.53,.08),METAL)
    box(a,(0,0,.58),(.34,.32,1.09),YELLOW)
    box(a,(0,-.06,1.23),(.56,.43,.56),YELLOW)
    box(a,(0,-.288,1.24),(.47,.023,.43),BLACK)
    box(a,(-.07,-.306,1.31),(.24,.018,.12),GREEN)
    rod(a,(.145,-.30,1.19),(.145,-.32,1.19),.052,WHITE,10)
    box(a,(-.07,-.31,1.12),(.22,.026,.042),METAL)
    box(a,(-.07,-.35,1.10),(.18,.09,.007),WHITE)
    box(a,(0,-.095,1.55),(.65,.59,.07),DARK)
    return a

def concrete_wheel_stop():
    a=asset('concrete_wheel_stop','parking','person')
    yz=[(-.14,0),(.14,0),(.14,.045),(.084,.165),(-.084,.165),(-.14,.045)]
    n=len(yz);vs=[(x,y,z) for x in (-.84,.84) for y,z in yz]
    a.mesh(vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],CONCRETE)
    for x in (-.52,.52):
        rod(a,(x,0,.163),(x,0,.17),.032,DARK,8)
        rod(a,(x,0,.169),(x,0,.186),.014,METAL,6)
    for x in (-.65,.65):a.box((x,-.116,.095),(.15,.014,.065),YELLOW,rot=(-.43,0,0))
    return a

def rubber_parking_curb():
    a=asset('rubber_parking_curb','parking','person')
    for j in range(3):
        cx=(j-1)*.47
        pts=[(cx-.23,0),(cx+.23,0),(cx+.23,.047),(cx+.18,.125),(cx-.18,.125),(cx-.23,.047)]
        profile(a,pts,.13,-.13,RUBBER)
        box(a,(cx,-.136,.075),(.23,.014,.055),YELLOW)
        for xx in (cx-.16,cx+.16):rod(a,(xx,0,.125),(xx,0,.132),.022,DARK,8)
    return a

def steel_bollard():
    a=asset('steel_safety_bollard','parking')
    rod(a,(0,0,.03),(0,0,1.04),.086,YELLOW,10)
    a.sphere((0,0,1.04),.086,mat=YELLOW,segments=10,rings=3)
    rod(a,(0,0,.70),(0,0,.83),.088,WHITE,10)
    box(a,(0,0,.035),(.30,.30,.07),DARK)
    for x in (-.1,.1):
        for y in (-.1,.1): rod(a,(x,y,.07),(x,y,.088),.023,METAL,6)
    return a

def removable_bollard():
    a=asset('removable_locking_bollard','parking')
    box(a,(0,0,.48),(.12,.12,.93),WHITE)
    for z in (.40,.75): box(a,(0,0,z),(.126,.126,.14),RED)
    box(a,(0,0,.035),(.22,.22,.07),METAL)
    rod(a,(-.047,0,.95),(-.047,0,1.04),.012,DARK,6)
    rod(a,(.047,0,.95),(.047,0,1.04),.012,DARK,6)
    rod(a,(-.047,0,1.04),(.047,0,1.04),.012,DARK,6)
    box(a,(0,-.075,.16),(.071,.035,.074),METAL)
    rod(a,(0,-.096,.16),(0,-.101,.16),.014,BLACK,6)
    return a

def delineator():
    a=asset('flexible_lane_delineator','traffic')
    rod(a,(0,0,.04),(0,0,.92),.038,ORANGE,8)
    rod(a,(0,0,.52),(0,0,.66),.040,WHITE,8)
    rod(a,(0,0,.76),(0,0,.89),.040,WHITE,8)
    rod(a,(0,0,.015),(0,0,.065),.14,ORANGE,8)
    for x in (-.10,.10): rod(a,(x,0,.067),(x,0,.077),.017,DARK,6)
    return a

def traffic_cone():
    a=asset('traffic_cone','traffic','handheld')
    box(a,(0,0,.035),(.39,.39,.07),RUBBER)
    # Continuous frusta preserve the familiar tapered silhouette and reflective bands.
    for z0,z1,mat in ((.07,.30,ORANGE),(.30,.40,WHITE),(.40,.51,ORANGE),(.51,.61,WHITE),(.61,.70,ORANGE)):
        r0=.16-(z0-.07)*.20; r1=.16-(z1-.07)*.20
        a.cylinder((0,0,z0),(0,0,z1),r0,mat=mat,sides=8,radius2=r1)
    rod(a,(0,0,.701),(0,0,.708),.025,BLACK,8)
    return a

def traffic_barrel():
    a=asset('construction_traffic_barrel','traffic')
    rod(a,(0,0,.02),(0,0,.11),.37,RUBBER,10)
    for i in range(8):
        z=.11+i*.115; r=.29-i*.007
        rod(a,(0,0,z),(0,0,z+.117),r,ORANGE if i%2==0 else WHITE,10)
    box(a,(0,0,1.06),(.20,.08,.09),ORANGE)
    box(a,(0,0,1.10),(.115,.085,.025),BLACK)
    rod(a,(0,0,1.14),(0,0,1.19),.045,DARK,8)
    a.sphere((0,0,1.24),.080,mat=YELLOW,segments=8,rings=3)
    return a

def jersey_barrier():
    a=asset('concrete_jersey_barrier','traffic','large')
    cross=[(-.33,0),(.33,0),(.33,.17),(.17,.49),(.115,.86),(-.115,.86),(-.17,.49),(-.33,.17)]
    vs=[(x,y,z) for x in (-1.175,1.175) for y,z in cross]; n=len(cross)
    a.mesh(vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat=CONCRETE)
    for x in (-.74,.74):
        box(a,(x,0,.875),(.16,.09,.05),DARK)
        box(a,(x,-.14,.66),(.11,.014,.17),WHITE)
    return a

def water_barrier():
    a=asset('plastic_water_barrier','traffic','large')
    yz=[(-.29,0),(.29,0),(.29,.16),(.17,.30),(.12,.88),(.09,.94),(-.09,.94),(-.12,.88),(-.17,.30),(-.29,.16)]
    n=len(yz);vs=[(x,y,z) for x in (-.88,.88) for y,z in yz]
    a.mesh(vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],ORANGE)
    for x in (-.61,0,.61):
        for sign in (-1,1):
            a.box((x,sign*.150,.58),(.28,.026,.22),WHITE,rot=(sign*.08,0,0))
            box(a,(x,sign*.22,.23),(.31,.04,.10),ORANGE)
    rod(a,(.52,0,.94),(.52,0,.975),.08,BLACK,10)
    # Interleaved end knuckles allow units to pin together.
    for x in (-.94,.94):
        for z in ((.22,.57) if x<0 else (.39,.74)):
            rod(a,(x,0,z-.06),(x,0,z+.06),.085,ORANGE,8)
            rod(a,(x,0,z+.061),(x,0,z+.067),.025,BLACK,8)
    rod(a,(-.67,-.294,.10),(-.67,-.31,.10),.039,BLACK,8)
    return a

def sawhorse_barricade():
    a=asset('striped_sawhorse_barricade','traffic')
    for x in (-.56,.56):
        for y in (-.30,.30): rod(a,(x,y,.025),(x,0,.94),.035,METAL,4)
        rod(a,(x,-.21,.28),(x,.21,.28),.018,METAL,4)
    for z in (.62,.96):
        box(a,(0,0,z),(1.40,.066,.23),WHITE)
        for i in range(5): face_stroke(a,[(-.63+i*.29,z-.102),(-.49+i*.29,z+.102)],-.042,ORANGE,.045)
    rod(a,(.47,0,1.09),(.47,0,1.15),.035,DARK,8)
    a.sphere((.47,0,1.21),.081,mat=YELLOW,segments=8,rings=3)
    return a

def sidewalk_aframe():
    a=asset('sidewalk_closed_a_frame','traffic')
    for x in (-.37,.37):
        for y in (-.29,.29): rod(a,(x,y,.045),(x,0,1.13),.032,ORANGE,4)
    plate(a,0,.73,.74,.62,WHITE,y=-.10)
    text(a,'SIDEWALK',0,.91,.63,.075,y=-.163,stroke=.005)
    text(a,'CLOSED',0,.73,.56,.09,y=-.163,stroke=.006)
    arrow(a,0,.52,.34,.14,y=-.163)
    box(a,(0,0,1.13),(.85,.13,.10),ORANGE)
    box(a,(0,0,1.15),(.23,.15,.052),BLACK)
    return a

def warning_triangle():
    a=asset('folding_warning_triangle','traffic','handheld')
    face_stroke(a,[(-.32,.065),(0,.63),(.32,.065),(-.32,.065)],0,RED,.038)
    face_stroke(a,[(-.23,.115),(0,.51),(.23,.115),(-.23,.115)],-.01,ORANGE,.018)
    for s in (-1,1): rod(a,(0,-.18,.02),(s*.29,.12,.035),.018,BLACK,4)
    return a

def cable_ramp():
    a=asset('cable_protector_ramp','traffic','handheld')
    yz=[(-.25,0),(.25,0),(.25,.014),(.12,.10),(-.12,.10),(-.25,.014)]
    n=len(yz);vs=[(x,y,z) for x in (-.49,.49) for y,z in yz]
    a.mesh(vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],RUBBER)
    box(a,(0,0,.105),(.92,.19,.018),YELLOW)
    for x in (-.34,-.17,0,.17,.34):box(a,(x,0,.117),(.045,.19,.01),BLACK)
    rod(a,(-.42,.10,.106),(.42,.10,.106),.012,METAL,6)
    for x in (-.495,.495):
        for y in (-.07,.07):rod(a,(x-.006,y,.043),(x+.006,y,.043),.025,BLACK,6)
    return a

def speed_hump():
    a=asset('modular_speed_hump','traffic','large')
    # Continuous arched section, separately bolted modules; no staircase blocks.
    yz=[(-.42,0),(.42,0),(.42,.018),(.31,.054),(.16,.086),(0,.10),(-.16,.086),(-.31,.054),(-.42,.018)]
    for j in range(5):
        x=(j-2)*.35;n=len(yz);vs=[(xx,y,z) for xx in (x-.171,x+.171) for y,z in yz]
        a.mesh(vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],YELLOW if j%2==0 else RUBBER)
        for y in (-.29,.29):
            rod(a,(x,y,.06),(x,y,.066),.032,DARK,8)
            rod(a,(x,y,.065),(x,y,.075),.015,METAL,6)
    return a

def convex_mirror():
    a=asset('convex_traffic_mirror','traffic')
    pole(a,2.43,r=.038)
    rod(a,(0,.03,2.24),(.30,.03,2.24),.022)
    rod(a,(.32,.08,2.25),(.32,-.028,2.25),.36,ORANGE,16)
    # Shallow faceted dome produces a truly convex reflective face.
    a.sphere((.32,-.033,2.25),1,mat=GLASS,segments=16,rings=8,scale=(.316,.073,.316))
    face_stroke(a,[(.11,2.18),(.18,2.36),(.29,2.45)],-.106,WHITE,.022)
    return a

def portable_message_board():
    a=asset('portable_arrow_message_board','traffic','large')
    for y in (-.42,.42):box(a,(0,y,.39),(1.75,.07,.11),DARK)
    for x in (-.80,0,.80):box(a,(x,0,.39),(.075,.91,.11),DARK)
    box(a,(.30,.08,.54),(.72,.66,.27),ORANGE)
    box(a,(.30,.08,.691),(.75,.69,.035),DARK)
    rod(a,(-.25,-.63,.29),(-.25,.63,.29),.055,METAL,8)
    for sign in (-1,1):
        y=sign*.56
        a.torus((-.25,y,.29),.215,.073,RUBBER,axis='y',segments=12,sides=6)
        rod(a,(-.25,y-.073,.29),(-.25,y+.073,.29),.135,METAL,12)
        rod(a,(-.25,y+sign*.075,.29),(-.25,y+sign*.09,.29),.05,DARK,8)
        for j in range(5):
            t=j*math.tau/5;rod(a,(-.25+.088*math.cos(t),y+sign*.077,.29+.088*math.sin(t)),(-.25+.088*math.cos(t),y+sign*.087,.29+.088*math.sin(t)),.012,METAL,6)
        # Folded mudguard has sloping leading and trailing edges.
        a.beam((-.61,y,.43),(-.47,y,.61),.21,.035,ORANGE)
        box(a,(-.25,y,.615),(.46,.21,.035),ORANGE)
        a.beam((-.03,y,.61),(.11,y,.43),.21,.035,ORANGE)
        for x in (-.75,.75):
            box(a,(x,y,.32),(.07,.07,.32),METAL)
            box(a,(x,y,.13),(.17,.17,.025),DARK)
    rod(a,(0,0,.43),(0,0,2.10),.075,METAL,8)
    rod(a,(0,.22,.51),(0,.03,1.61),.035,DARK,8)
    box(a,(0,0,2.02),(2.48,.22,1.18),BLACK)
    box(a,(0,0,2.64),(2.62,.29,.06),ORANGE)
    for z in (1.48,2.56):box(a,(0,.135,z),(2.38,.05,.05),DARK)
    for x in (-1.13,0,1.13):box(a,(x,.14,2.02),(.05,.06,1.10),DARK)
    points=[(-.86+i*.215,2.02) for i in range(9)]
    points += [(.43,2.45),(.645,2.235),(.645,1.805),(.43,1.59)]
    for x,z in points:
        rod(a,(x,-.12,z),(x,-.151,z),.071,DARK,8)
        rod(a,(x,-.154,z),(x,-.165,z),.053,YELLOW,8)
    for x in (-.66,.66):a.beam((x,.37,.38),(0,1.50,.30),.085,.10,DARK)
    box(a,(0,1.55,.31),(.12,.25,.12),METAL)
    a.sphere((0,1.69,.31),1,METAL,8,4,scale=(.065,.13,.063))
    box(a,(0,1.55,.39),(.04,.15,.04),DARK)
    rod(a,(.16,1.13,.06),(.16,1.13,.46),.024,METAL,8)
    box(a,(.16,1.13,.04),(.19,.17,.035),DARK)
    return a

def clearance_gantry():
    a=asset('parking_height_clearance_gantry','parking','large')
    for x in (-2.12,2.12):
        pole(a,3.0,x=x,r=.075)
        rod(a,(x,0,.35),(x,0,.80),.08,YELLOW,8)
    rod(a,(-2.12,0,3.0),(2.12,0,3.0),.075,YELLOW,8)
    for x in (-1.35,1.35): rod(a,(x,0,3.0),(x,0,2.64),.012,METAL,6)
    rod(a,(-1.81,0,2.59),(1.81,0,2.59),.071,YELLOW,8)
    for x in (-1.50,-.9,.9,1.5): rod(a,(x-.13,0,2.59),(x+.13,0,2.59),.074,BLACK,8)
    plate(a,0,2.96,1.50,.34,YELLOW)
    text(a,'8 FT',0,2.96,.82,.16,stroke=.012)
    return a

FACTORIES=[stop_sign,yield_sign,speed_limit,one_way,do_not_enter,wrong_way,no_left_turn,no_u_turn,pedestrian_crossing,school_crossing,bike_route,railroad_crossbuck,street_name_pair,parking_sign,accessible_sign,no_parking_sign,bus_stop_sign,interstate_direction,detour_sign,road_closed_barricade,vertical_signal,horizontal_signal,mast_arm_signal,pedestrian_signal,flashing_beacon,railroad_gate,traffic_camera,traffic_cabinet,single_meter,dual_meter,pay_station,gate_arm,ticket_dispenser,concrete_wheel_stop,rubber_parking_curb,steel_bollard,removable_bollard,delineator,traffic_cone,traffic_barrel,jersey_barrier,water_barrier,sawhorse_barricade,sidewalk_aframe,warning_triangle,cable_ramp,speed_hump,convex_mirror,portable_message_board,clearance_gantry]
for _factory in FACTORIES:
    _sample=_factory()
    register(_sample.name,_sample.category,_sample.size_class,_factory)
assert len(FACTORIES)==50
