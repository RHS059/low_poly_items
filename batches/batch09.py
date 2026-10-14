"""Fifty fixed park playground, outdoor gym and sports installations.
Metre scale, structural tube sizes, restrained civic finishes and service details.
"""
from assetlib import Asset, register
import math

CAT = 'playground_fitness_sports'
PI = math.pi

def _asset(name, size='large'):
    return Asset('b09_'+name, CAT, size)

def _rod(a,p,q,r=.035,mat='dark_metal',sides=6):
    a.cylinder(p,q,r,mat,sides=sides)

def _foot(a,x,y,z=0,post=.045,mat='dark_metal'):
    a.box((x,y,z+.035),(.22,.22,.07),mat)
    for dx,dy in ((-.072,-.072),(.072,.072)):
        a.cylinder((x+dx,y+dy,z+.07),(x+dx,y+dy,z+.084),.015,'steel',sides=6)

def _post(a,x,y,h,r=.045,mat='green'):
    _foot(a,x,y,post=r,mat='dark_metal')
    _rod(a,(x,y,.05),(x,y,h),r,mat,8)
    a.sphere((x,y,h),r,mat,segments=8,rings=3)

def _path(a,pts,r=.026,mat='steel',sides=6):
    a.tube(pts,r,mat,sides=sides)

def _rung_ladder(a,x,y,z0,z1,width=.65,rungs=6,lean=.35,mat='dark_metal'):
    for s in (-1,1):
        _rod(a,(x-lean,y+s*width/2,z0),(x,y+s*width/2,z1+.28),.036,mat)
    for j in range(rungs):
        t=(j+1)/(rungs+1)
        xx=x-lean*(1-t);zz=z0+(z1-z0)*t
        _rod(a,(xx,y-width/2,zz),(xx,y+width/2,zz),.027,'steel')

def _rail(a,p,q,height=.75,mat='dark_metal',mid=True):
    _rod(a,p,(p[0],p[1],p[2]+height),.026,mat)
    _rod(a,q,(q[0],q[1],q[2]+height),.026,mat)
    _rod(a,(p[0],p[1],p[2]+height),(q[0],q[1],q[2]+height),.028,mat)
    if mid: _rod(a,(p[0],p[1],p[2]+height*.45),(q[0],q[1],q[2]+height*.45),.022,mat)

def _profile(a,points,width,mat):
    # x,z polygon extruded along y, polygon must be counterclockwise in x,z.
    n=len(points); vs=[(x,y,z) for y in (-width/2,width/2) for x,z in points]
    fs=[tuple(range(n)),tuple(reversed(range(n,2*n)))]
    fs += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    a.mesh(vs,fs,mat)

def _molded_pad(a,center,size,mat='rubber',vertical=False):
    """Beveled perimeter, domed top and narrowed shell underside of a molded pad."""
    w,d,h=size; r=min(w,d)*.14
    outline=[(-w/2+r,-d/2),(w/2-r,-d/2),(w/2,-d/2+r),(w/2,d/2-r),(w/2-r,d/2),(-w/2+r,d/2),(-w/2,d/2-r),(-w/2,-d/2+r)]
    vs=[]
    for fac,z in ((.86,-h/2),(1,0),(.94,h/2)):
        for x,y in outline:
            v=(x*fac,y*fac,z)
            if vertical:v=(z,y*fac,x*fac)
            vs.append(tuple(center[i]+v[i] for i in range(3)))
    fs=[tuple(reversed(range(8))),tuple(range(16,24))]
    for j in range(2):
        for i in range(8):fs.append((j*8+i,j*8+(i+1)%8,(j+1)*8+(i+1)%8,(j+1)*8+i))
    a.mesh(vs,fs,mat)

def _bearing(a,x,y,z,r=.07,width=.12):
    """Actual pivot boss, bush and visible axle end along the horizontal Y axis."""
    _rod(a,(x,y-width/2,z),(x,y+width/2,z),r,'dark_metal',10)
    for side in (-1,1):
        yy=y+side*width/2
        _rod(a,(x,yy,z),(x,yy+side*.013,z),r*.67,'steel',8)
        _rod(a,(x,yy+side*.013,z),(x,yy+side*.023,z),r*.30,'dark_metal',6)

def _slide_bed(a,pts,width=.58,mat='steel'):
    # Continuous folded sheet trough: thickness, upright sides and hemmed edges.
    # Two tangent sections around each corner remove abrupt panel-to-panel kinks.
    path=[pts[0]]
    for i in range(1,len(pts)-1):
        for j,f in ((i-1,.18),(i+1,.18)):
            path.append(tuple(pts[i][k]*(1-f)+pts[j][k]*f for k in range(3)))
    path.append(pts[-1]);section=[(-width/2-.025,.18),(-width/2-.025,-.018),(width/2+.025,-.018),(width/2+.025,.18),(width/2-.012,.18),(width/2-.025,.018),(-width/2+.025,.018),(-width/2+.012,.18)]
    vs=[(x,y+dy,z+dz) for x,y,z in path for dy,dz in section];fs=[];mats=[]
    for j in range(len(path)-1):
        for i in range(8):fs.append((8*j+i,8*j+(i+1)%8,8*(j+1)+(i+1)%8,8*(j+1)+i));mats.append(mat if i in (1,5) else 'teal')
    fs.extend([tuple(reversed(range(8))),tuple(range(8*(len(path)-1),8*len(path)))]);mats+=['steel','steel'];a.mesh(vs,fs,mats)
    for p in (path[1],path[-2]):
        a.box((p[0],p[1],p[2]-.042),(.075,width+.06,.06),'dark_metal')
        for side in (-1,1):_rod(a,(p[0],p[1]+side*(width/2+.02),p[2]+.08),(p[0],p[1]+side*(width/2+.037),p[2]+.08),.018,'steel',6)

def _swing_frame(a,width=3.4,height=2.45,depth=.9):
    for x in (-width/2,width/2):
        for y in (-depth,depth):
            _foot(a,x,y)
            _rod(a,(x,y,.04),(x,0,height),.059,'green',8)
        _rod(a,(x,-depth*.55,height*.45),(x,depth*.55,height*.45),.036,'dark_metal')
    _rod(a,(-width/2-.12,0,height),(width/2+.12,0,height),.068,'dark_metal',8)

def _chain(a,p,q):
    _rod(a,p,q,.009,'steel',4)
    # Spaced connector collars suggest link chain without consuming the budget.
    for t in (.1,.35,.6,.85):
        c=tuple(p[i]+(q[i]-p[i])*t for i in range(3))
        a.torus(c,.015,.005,'steel',axis='y',segments=6,sides=3)

def straight_slide():
    a=_asset('straight_slide')
    for x in (-.42,.42):
        for y in (-.4,.4): _post(a,x,y,1.57,.044,'teal')
    a.box((0,0,1.52),(.94,.86,.11),'dark_metal')
    _rung_ladder(a,-.46,0,.03,1.55,.64,6,.75)
    for y in (-.40,.40): _rail(a,(-.45,y,1.55),(.39,y,1.55),.70,'teal')
    _slide_bed(a,[(.43,0,1.53),(.85,0,1.40),(2.40,0,.22),(2.87,0,.15)])
    _rod(a,(1.25,-.27,.03),(1.25,-.27,1.10),.035)
    _rod(a,(1.25,.27,.03),(1.25,.27,1.10),.035)
    for y in (-.35,.35):
        a.box((0,y,1.55-.12),(.87,.08,.09),'dark_metal')
        _path(a,[(-0.46-.23,y,1.55-.07),(-0.46-.18,y,1.55+.41),(-0.46+.02,y,1.55+.56)],.028,'steel',8)
    return a

def wave_slide():
    a=_asset('wave_slide')
    for x in (-.35,.35):
        for y in (-.40,.40): _post(a,x,y,2.03,.045,'green')
    a.box((0,0,1.97),(.8,.86,.1),'dark_metal')
    _rung_ladder(a,-.40,0,.03,2.0,.62,8,.90)
    for y in (-.40,.40): _rail(a,(-.4,y,2.0),(.35,y,2.0),.66,'green')
    pts=[(.36,0,2.0),(.80,0,1.80),(1.30,0,1.16),(1.85,0,1.02),(2.25,0,.86),(2.70,0,.31),(3.22,0,.17)]
    _slide_bed(a,pts,.62,'steel')
    for x,z in ((1.55,1.06),(2.55,.47)):
        for y in (-.30,.30): _rod(a,(x,y,.03),(x,y,z),.038,'green')
    for y in (-.35,.35):
        a.box((0,y,2.0-.12),(.87,.08,.09),'dark_metal')
        _path(a,[(-0.4-.23,y,2.0-.07),(-0.4-.18,y,2.0+.41),(-0.4+.02,y,2.0+.56)],.028,'steel',8)
    return a

def curved_slide():
    a=_asset('curved_slide')
    _post(a,0,0,2.15,.105,'dark_metal')
    # Wide faceted curved chute built from a swept inner/outer ribbon.
    n=14; vs=[]
    for i in range(n+1):
        th=PI*.15+PI*1.45*i/n; z=2.12-1.87*i/n
        for r,h in ((.69,0),(1.31,0),(.69,.21),(1.31,.21)):
            vs.append((r*math.cos(th),r*math.sin(th),z+h))
    fs=[];mats=[]
    for i in range(n):
        k=i*4;j=k+4
        fs.extend([(k,k+1,j+1,j),(k+2,k,j,j+2),(k+1,k+3,j+3,j+1)])
        mats.extend(['steel','teal','teal'])
    a.mesh(vs,fs,mats)
    a.box((.90,.1,2.12),(.78,.65,.1),'dark_metal')
    _rung_ladder(a,.90,-.22,.03,2.15,.58,8,.80,'dark_metal')
    for th,z in ((PI*.4,1.8),(PI*.9,1.14),(PI*1.4,.5)):
        _rod(a,(0,0,z-.18),(math.cos(th),math.sin(th),z),.045,'dark_metal')
    return a

def double_swing():
    a=_asset('double_swing');_swing_frame(a)
    for x in (-.79,.79):
        vs=[(x+dx,y,.48+zz) for y in (-.115,.115) for dx,zz in ((-.255,.038),(-.16,-.012),(0,-.026),(.16,-.012),(.255,.038))]
        vs += [(xx,yy,zz-.026) for xx,yy,zz in vs]
        fs=[]
        for j in range(4):fs.extend([(j,j+1,j+6,j+5),(j+10,j+15,j+16,j+11)])
        for j in range(4):fs.extend([(j,j+10,j+11,j+1),(j+5,j+6,j+16,j+15)])
        fs.extend([(0,5,15,10),(4,14,19,9)]);a.mesh(vs,fs,'rubber')
        for s in (-1,1):
            _chain(a,(x+s*.24,0,.5),(x+s*.30,0,2.4))
            a.torus((x+s*.30,0,2.42),.042,.010,'steel',axis='y',segments=8,sides=4)
    return a

def bucket_swing():
    a=_asset('toddler_bucket_swing');_swing_frame(a,2.2,2.2,.8)
    a.box((0,0,.6),(.43,.38,.07),'rubber')
    a.box((0,.17,.78),(.43,.045,.35),'rubber')
    for s in (-1,1):
        a.box((s*.20,0,.78),(.045,.38,.35),'rubber')
        _chain(a,(s*.20,0,.94),(s*.28,0,2.15))
    a.box((0,-.17,.90),(.42,.045,.09),'rubber')
    a.box((0,-.17,.70),(.09,.045,.20),'rubber')
    return a

def tire_swing():
    a=_asset('tire_swing');_swing_frame(a,2.9,2.6,1.1)
    a.torus((0,0,.66),.38,.14,'rubber',segments=12,sides=6)
    a.cylinder((0,0,2.40),(0,0,2.57),.07,'steel',sides=8)
    for i in range(3):
        th=2*PI*i/3;x=.39*math.cos(th);y=.39*math.sin(th)
        _chain(a,(x,y,.75),(0,0,2.39))
    for i in range(12):
        th=i*2*PI/12
        a.box((.46*math.cos(th),.46*math.sin(th),.66),(.10,.045,.10),'black',rot=th)
    return a

def monkey_bars():
    a=_asset('monkey_bars')
    for x in (-1.65,1.65):
        for y in (-.50,.50): _post(a,x,y,2.1,.044,'green')
        for z in (.38,.73,1.08,1.43,1.78): _rod(a,(x,-.5,z),(x,.5,z),.027,'steel')
    for y in (-.5,.5): _rod(a,(-1.68,y,2.08),(1.68,y,2.08),.045,'green')
    for x in [-1.3,-.975,-.65,-.325,0,.325,.65,.975,1.3]: _rod(a,(x,-.5,2.08),(x,.5,2.08),.024,'steel')
    return a

def dome_climber():
    a=_asset('dome_climber')
    rings=[]
    for r,z,offset in ((1.5,.07,0),(1.21,.92,PI/8),(.66,1.48,0)):
        rings.append([(r*math.cos(2*PI*i/8+offset),r*math.sin(2*PI*i/8+offset),z) for i in range(8)])
    for ring in rings:
        for i,p in enumerate(ring): _rod(a,p,ring[(i+1)%8],.028,'teal')
    for k in (0,1):
        for i,p in enumerate(rings[k]):
            _rod(a,p,rings[k+1][i],.027,'teal');_rod(a,p,rings[k+1][(i-1)%8],.027,'teal')
    for p in rings[-1]: _rod(a,p,(0,0,1.72),.027,'teal')
    for ring in rings:
        for p in ring: a.sphere(p,.045,'steel',segments=6,rings=3)
    for p in rings[0]: _foot(a,p[0],p[1])
    return a

def climbing_wall():
    a=_asset('climbing_wall')
    for x in (-.87,.87): _post(a,x,0,2.32,.061,'dark_metal')
    for z in (.62,1.48): a.box((0,0,z),(1.68,.12,.82),'wood')
    a.box((0,0,2.02),(1.68,.12,.25),'wood')
    for i in range(16):
        x=-.65+(i%4)*.43+(.10 if (i//4)%2 else 0);z=.35+(i//4)*.49
        a.sphere((x,-.11,z),(.093,.077,.067),('teal','cream','green')[i%3],segments=5,rings=3)
        _rod(a,(x,-.16,z),(x,-.19,z),.012,'steel')
    return a

def rope_pyramid():
    a=_asset('rope_pyramid')
    _post(a,0,0,2.75,.065,'dark_metal')
    top=(0,0,2.68)
    corners=[(-1.32,-1.32,.10),(1.32,-1.32,.10),(1.32,1.32,.10),(-1.32,1.32,.10)]
    for p in corners:
        _foot(a,p[0],p[1]);_rod(a,p,top,.022,'navy')
    for lev in (.22,.44,.66,.82):
        ring=[tuple(p[j]*(1-lev)+top[j]*lev for j in range(3)) for p in corners]
        for i,p in enumerate(ring): _rod(a,p,ring[(i+1)%4],.017,'navy',5)
    for i in range(4):
        p=corners[i];q=corners[(i+1)%4]
        for t in (.25,.5,.75):
            base=tuple(p[j]*(1-t)+q[j]*t for j in range(3))
            _rod(a,base,top,.013,'navy',5)
    a.cone((0,0,2.7),(0,0,2.89),.105,'steel',8)
    return a

def seesaw():
    a=_asset('seesaw')
    for y in (-.25,.25):
        a.beam((-.27,y,.05),(0,y,.60),.10,mat='green')
        a.beam((.27,y,.05),(0,y,.60),.10,mat='green')
        _foot(a,0,y)
    _rod(a,(0,-.34,.62),(0,.34,.62),.10,'steel',8)
    a.box((0,0,.69),(3.25,.19,.14),'wood')
    for x in (-1.34,1.34):
        a.box((x,0,.80),(.40,.37,.065),'teal')
        _path(a,[(x*.76,-.14,.78),(x*.76,-.14,1.02),(x*.76,.14,1.02),(x*.76,.14,.78)],.026,'steel')
        a.cylinder((x,0,.025),(x,0,.23),.16,'rubber',sides=10)
    _bearing(a,0,0,.62,.13,.73)
    for x in (-.16,.16):a.box((x,0,.68),(.06,.28,.12),'dark_metal')
    for x in (-1.34,1.34):
        a.box((x,0,.57),(.26,.18,.04),'dark_metal')
        for y in (-.12,.12):_rod(a,(x,y,.825),(x,y,.844),.014,'steel',6)
    return a

def spring_rocker():
    a=_asset('four_seat_spring_rocker','person')
    a.box((0,0,.045),(.42,.42,.09),'dark_metal')
    pts=[]
    for i in range(49):
        th=6*PI*i/48;pts.append((.12*math.cos(th),.12*math.sin(th),.10+.43*i/48))
    _path(a,pts,.025,'steel',5)
    a.box((0,0,.61),(1.8,.16,.13),'green');a.box((0,0,.61),(.16,1.8,.13),'green')
    for x,y in ((-.76,0),(.76,0),(0,-.76),(0,.76)):
        a.box((x,y,.72),(.32,.32,.075),'wood')
        _rod(a,(x*.67,y*.67,.69),(x*.67,y*.67,.98),.025,'steel')
        _rod(a,(x*.67-.12,y*.67,.98),(x*.67+.12,y*.67,.98),.025,'steel')
    for z in (.09,.54):
        a.cylinder((0,0,z),(0,0,z+.04),.17,'dark_metal',10)
        for x in (-.11,.11):
            for y in (-.11,.11):_rod(a,(x,y,z+.04),(x,y,z+.055),.017,'steel',6)
    for x,y in ((-.76,0),(.76,0),(0,-.76),(0,.76)):
        a.box((x,y,.53),(.20,.22,.04),'dark_metal')
    return a

def merry_go_round():
    a=_asset('merry_go_round')
    a.cylinder((0,0,.06),(0,0,.24),.23,'dark_metal',12)
    a.cylinder((0,0,.24),(0,0,.32),1.13,'teal',16)
    a.torus((0,0,.315),1.09,.034,'steel',segments=16,sides=4)
    for i in range(4):
        th=2*PI*i/4;c=math.cos(th);s=math.sin(th)
        p=(.35*c,.35*s,.32);q=(.98*c,.98*s,.32)
        _rail(a,p,q,.69,'dark_metal',False)
        a.beam((.40*c,.40*s,.335),(1.0*c,1.0*s,.335),.21,.032,'rubber')
    a.cylinder((0,0,.32),(0,0,.95),.065,'dark_metal',8)
    for i in range(8):
        t=PI*i/4
        a.beam((.21*math.cos(t),.21*math.sin(t),.22),(1.02*math.cos(t),1.02*math.sin(t),.22),.048,.08,'dark_metal')
    a.cylinder((0,0,.17),(0,0,.24),.30,'steel',12)
    return a

def balance_beam():
    a=_asset('zigzag_balance_beam')
    pts=[(-1.8,-.32,.43),(-.6,-.32,.43),(.1,.36,.43),(1.6,.36,.43)]
    for p,q in zip(pts,pts[1:]): a.beam(p,q,.15,.16,'wood')
    for p in pts:
        _foot(a,p[0],p[1]);a.box((p[0],p[1],.23),(.11,.11,.40),'green')
    return a

def stepping_logs():
    a=_asset('stepping_log_course')
    for i,h in enumerate((.19,.30,.42,.53,.39,.26)):
        x=(i-2.5)*.52;y=.24*math.sin(i*1.3)
        a.cylinder((x,y,.0),(x,y,h),.19,'wood_dark',sides=10)
        a.cylinder((x,y,h),(x,y,h+.02),.18,'wood_light',sides=10)
        a.torus((x,y,h+.024),.105,.006,'wood',segments=10,sides=3)
    return a

def crawl_tunnel():
    a=_asset('crawl_tunnel')
    for x in (-.76,.76):
        a.box((x,0,.12),(.27,1.20,.24),'wood_dark')
    # Open tube shell, with separate end rim rather than capped cylinders.
    vs=[];n=12
    for x in (-1.03,1.03):
        for r in (.48,.54):
            for i in range(n):
                th=2*PI*i/n;vs.append((x,r*math.cos(th),.70+r*math.sin(th)))
    fs=[]
    for i in range(n):
        j=(i+1)%n
        fs += [(i,j,j+24,i+24),(i+12,i+36,j+36,j+12),(i,i+12,j+12,j),(i+24,j+24,j+36,i+36)]
    a.mesh(vs,[tuple(reversed(f)) for f in fs],'teal')
    for x in (-1.03,1.03): a.torus((x,0,.70),.511,.031,'dark_metal',axis='x',segments=12,sides=4)
    for x in (-.76,.76):
        # Two formed cradle cheeks support the round shell instead of touching it at a single point.
        for y in (-.38,.38):
            a.beam((x,y,.15),(x,y*.91,.38),.12,.09,'dark_metal')
            _rod(a,(x,y,.32),(x+.075,y,.32),.020,'steel',6)
    for x in (-.92,.92):
        for i in range(8):
            t=i*PI/4;_rod(a,(x,.522*math.cos(t),.70+.522*math.sin(t)),(x+(.014 if x>0 else -.014),.522*math.cos(t),.70+.522*math.sin(t)),.013,'steel',6)
    return a

def ring_traverse():
    a=_asset('overhead_ring_traverse')
    for x in (-1.7,1.7):
        for y in (-.5,.5): _post(a,x,y,2.37,.047,'dark_metal')
        _rod(a,(x,-.5,2.34),(x,.5,2.34),.045,'dark_metal')
    _rod(a,(-1.72,0,2.34),(1.72,0,2.34),.06,'green')
    for i in range(7):
        x=-1.4+i*.466
        _rod(a,(x,0,2.32),(x,0,2.01),.011,'steel')
        a.torus((x,0,1.91),.105,.019,'steel',axis='y',segments=10,sides=5)
    for x in (-1.7,1.7):
        for z in (.37,.72,1.07): _rod(a,(x,-.5,z),(x,.5,z),.027,'steel')
    return a

def play_tower():
    a=_asset('roofed_play_tower')
    for x in (-.66,.66):
        for y in (-.66,.66):
            a.box((x,y,1.32),(.105,.105,2.64),'wood_dark');_foot(a,x,y)
    for i in range(8): a.box((-.55+i*.157,0,1.12),(.148,1.38,.09),'wood')
    for y in (-.66,.66):
        a.box((0,y,1.83),(1.39,.065,.095),'green')
        for x in (-.43,-.21,0,.21,.43): a.box((x,y,1.49),(.045,.045,.64),'wood')
    _rail(a,(-.66,-.64,1.16),(-.66,.64,1.16),.66,'green')
    _rung_ladder(a,.70,0,.03,1.15,.64,5,-.67,'dark_metal')
    # Gabled roof with a thin eave profile.
    _profile(a,[(-.83,2.40),(.83,2.40),(.83,2.49),(0,2.96),(-.83,2.49)],1.72,'green')
    for y in (-.88,.88): a.beam((-.84,y,2.49),(0,y,2.96),.055,mat='dark_metal');a.beam((0,y,2.96),(.84,y,2.49),.055,mat='dark_metal')
    for y in (-.64,.64):
        for x in (-.55,.55):a.beam((x,y,2.35),(x*.48,y,2.61),.058,.065,'wood_dark')
    for y in (-.54,.54):a.box((0,y,1.015),(1.43,.10,.13),'wood_dark')
    for x in (-.61,.61):a.box((x,0,1.015),(.11,1.29,.13),'wood_dark')
    return a

def sand_table():
    a=_asset('accessible_sand_table','person')
    for x in (-.65,.65):
        for y in (-.37,.37): _post(a,x,y,.72,.035,'dark_metal')
    a.box((0,0,.68),(1.58,1.00,.09),'green')
    a.box((0,0,.74),(1.43,.85,.065),'sand')
    for y in (-.49,.49): a.box((0,y,.81),(1.61,.09,.22),'green')
    for x in (-.76,.76): a.box((x,0,.81),(.09,.94,.22),'green')
    a.box((0,.38,.79),(.34,.20,.025),'steel')
    a.cylinder((.48,-.24,.77),(.48,-.24,.785),.035,'dark_metal',8)
    for y in (-.41,.41):a.box((0,y,.62),(1.40,.052,.10),'dark_metal')
    for x in (-.70,.70):a.box((x,0,.63),(.052,.88,.08),'dark_metal')
    for x in (-.64,.64):
        for y in (-.37,.37):a.box((x,y,.62),(.08,.08,.11),'steel')
    return a

def activity_panel():
    a=_asset('playground_abacus_panel','person')
    for x in (-.76,.76): _post(a,x,0,1.65,.046,'green')
    for z in (.52,1.54): a.box((0,0,z),(1.52,.14,.105),'wood_dark')
    for z in (.75,1.01,1.27):
        _rod(a,(-.71,0,z),(.71,0,z),.018,'steel')
        for i in range(5):
            x=-.53+i*.21
            a.cylinder((x-.06,0,z),(x+.06,0,z),.10,('teal','cream','wood')[int(round(z*10))%3],sides=8)
    for x in (-.72,.72):
        for z in (.75,1.01,1.27):_rod(a,(x-.025,0,z),(x+.025,0,z),.038,'dark_metal',8)
    return a

def pullup_station():
    a=_asset('three_height_pullup_station')
    for x,h in ((-1.8,1.63),(-.6,2.08),(.6,2.43),(1.8,2.43)): _post(a,x,0,h,.064,'green')
    for x,h in ((-1.2,1.60),(0,2.05),(1.2,2.40)):
        _rod(a,(x-.56,0,h),(x+.56,0,h),.022,'steel')
        _rod(a,(x-.45,0,h),(x-.22,0,h),.027,'rubber');_rod(a,(x+.22,0,h),(x+.45,0,h),.027,'rubber')
    a.box((-.6,-.07,1.13),(.17,.025,.20),'cream')
    return a

def dip_station():
    a=_asset('parallel_dip_station','person')
    for y in (-.31,.31):
        for x in (-.66,.66): _post(a,x,y,1.20,.045,'green')
        _rod(a,(-.89,y,1.19),(.89,y,1.19),.032,'steel')
        _rod(a,(-.48,y,1.19),(.48,y,1.19),.037,'rubber')
    for x in (-.66,.66): _rod(a,(x,-.31,.20),(x,.31,.20),.04,'green')
    return a

def situp_bench():
    a=_asset('incline_situp_bench','person')
    for x,z in ((-.76,.26),(.76,.68)):
        for y in (-.33,.33): _post(a,x,y,z,.038,'green')
    for y in (-.24,0,.24): a.beam((-.90,y,.33),(.91,y,.83),.19,.065,'wood')
    for y in (-.33,.33): a.beam((-.83,y,.27),(.86,y,.73),.045,.08,'dark_metal')
    _rod(a,(.91,0,.77),(.99,0,1.07),.035,'green')
    _rod(a,(.99,-.41,1.07),(.99,.41,1.07),.075,'rubber',8)
    _rod(a,(.75,-.41,.88),(.75,.41,.88),.06,'rubber',8)
    return a

def elliptical():
    a=_asset('outdoor_elliptical','person')
    for x in (-.49,.49): a.box((x,0,.07),(.15,.96,.14),'dark_metal')
    a.box((0,0,.17),(1.22,.22,.17),'green')
    _rod(a,(.43,0,.20),(.38,0,1.44),.065,'green',8)
    a.cylinder((-.43,-.14,.39),(-.43,.14,.39),.26,'green',12)
    for y,offset in ((-.33,0),(.33,.16)):
        _rod(a,(-.42,y,.43),(-.59+offset,y,.27),.035,'steel')
        a.beam((-.59+offset,y,.27),(.62+offset,y,.27),.09,.075,'dark_metal')
        _molded_pad(a,(-.07+offset,y,.33),(.44,.20,.07))
        _path(a,[(.63+offset,y,.26),(.45,y,1.13),(.20,y,1.63),(.03,y,1.67)],.031,'steel')
        _rod(a,(.03,y,1.67),(.20,y,1.63),.039,'rubber')
    a.box((.34,0,1.42),(.16,.32,.18),'cream',rot=(0,-.25,0))
    for y,off in ((-.33,0),(.33,.16)):
        _bearing(a,-.43,y,.39,.10,.13)
        _bearing(a,.45,y,1.13,.058,.10)
        for xx in (-.20+off,.05+off):a.box((xx,y,.37),(.018,.15,.015),'dark_metal')
    a.box((-.39,0,.19),(.34,.32,.06),'dark_metal')
    return a

def air_walker():
    a=_asset('air_walker','person')
    for y in (-.62,.62):
        _post(a,0,y,1.33,.061,'green')
        _rod(a,(0,y-.12,1.08),(0,y+.12,1.08),.092,'steel',8)
    _path(a,[(0,-.62,1.33),(.27,-.48,1.57),(.27,.48,1.57),(0,.62,1.33)],.041,'green')
    for y,s in ((-.31,-1),(.31,1)):
        _rod(a,(0,y,1.12),(s*.23,y,.28),.045,'steel')
        a.box((s*.23,y,.24),(.51,.24,.075),'dark_metal')
        a.box((s*.23,y,.28),(.43,.18,.015),'rubber')
    _rod(a,(.27,-.36,1.57),(.27,.36,1.57),.045,'rubber')
    for y in (-.31,.31):
        _bearing(a,0,y,1.12,.085,.13)
        _rod(a,(0,y,1.12),(0,y*1.9,1.12),.042,'steel',8)
        a.box((0,y,.88),(.14,.10,.11),'green')
    return a

def chest_press():
    a=_asset('seated_chest_press','person')
    _post(a,-.36,0,1.54,.075,'green')
    _molded_pad(a,(.04,0,.48),(.47,.42,.075))
    _molded_pad(a,(-.27,0,.87),(.64,.40,.095),vertical=True)
    a.beam((-.36,0,.14),(.07,0,.43),.085,.10,'green')
    _rod(a,(-.36,-.53,1.44),(-.36,.53,1.44),.060,'dark_metal',8)
    for y in (-.46,.46):
        _path(a,[(-.36,y,1.44),(.35,y,1.19),(.54,y,.89)],.035,'steel')
        _rod(a,(.54,y,.89),(.54,y*.54,.89),.033,'rubber')
        _rod(a,(-.36,y,1.44),(-.67,y,.99),.042,'green')
        a.cylinder((-.67,y-.075,.99),(-.67,y+.075,.99),.13,'dark_metal',10)
    for y in (-.46,.46):
        _bearing(a,-.36,y,1.44,.092,.14)
        _rod(a,(-.42,y,1.19),(-.60,y,.77),.019,'steel',7)
        _rod(a,(-.60,y,.77),(-.52,y,.57),.031,'dark_metal',8)
    a.box((-.33,0,.48),(.13,.38,.075),'green')
    return a

def rowing_station():
    a=_asset('outdoor_rowing_station','person')
    a.box((0,0,.16),(1.65,.14,.16),'green')
    for x in (-.68,.68):
        a.box((x,0,.07),(.14,.83,.14),'dark_metal')
        _rod(a,(x,0,.10),(x,0,.28),.045,'green')
    _molded_pad(a,(-.45,0,.46),(.42,.39,.085))
    _rod(a,(-.45,0,.18),(-.45,0,.42),.055,'green')
    for y in (-.24,.24):
        a.box((.54,y,.34),(.28,.21,.07),'dark_metal',rot=(0,-.30,0))
        _path(a,[(.58,y,.23),(.43,y,.63),(-.01,y*.9,.92)],.033,'steel')
        _rod(a,(-.01,y*.9,.92),(-.24,y*.9,.92),.038,'rubber')
        _rod(a,(.58,y-.045,.23),(.58,y+.045,.23),.080,'dark_metal',8)
    for y in (-.24,.24):
        _bearing(a,.58,y,.23,.10,.13)
        _rod(a,(.48,y,.35),(.11,y,.22),.024,'steel',7)
        _rod(a,(.11,y,.22),(-.09,y,.21),.037,'dark_metal',8)
        for x in (.48,.58):a.box((x,y,.40),(.018,.15,.016),'rubber')
    return a

def leg_press():
    a=_asset('seated_leg_press','person')
    for x in (-.60,.67): a.box((x,0,.07),(.17,.92,.14),'dark_metal')
    a.box((0,0,.15),(1.48,.18,.14),'green')
    _rod(a,(-.61,0,.20),(-.49,0,1.33),.07,'green',8)
    _molded_pad(a,(-.43,0,.86),(.69,.44,.09),vertical=True)
    _molded_pad(a,(-.16,0,.51),(.50,.45,.085))
    _rod(a,(-.16,0,.20),(-.16,0,.48),.06,'green')
    for y in (-.28,.28):
        _rod(a,(.64,y,.20),(.76,y,.87),.043,'steel')
        a.box((.79,y,.84),(.075,.25,.38),'dark_metal',rot=(0,-.22,0))
        _rod(a,(.64,y-.05,.20),(.64,y+.05,.20),.075,'steel')
    for y in (-.28,.28):
        _bearing(a,.64,y,.20,.094,.15)
        _rod(a,(.73,y,.74),(.25,y,.40),.026,'steel',7)
        _rod(a,(.25,y,.40),(.06,y,.29),.043,'dark_metal',8)
        a.box((.82,y,.76),(.028,.18,.055),'rubber')
    return a

def shoulder_wheels():
    a=_asset('shoulder_rotation_wheels','person')
    _post(a,0,0,1.57,.075,'green')
    _rod(a,(-.67,0,1.30),(.67,0,1.30),.045,'green')
    for x in (-.53,.53):
        a.torus((x,-.10,1.30),.32,.023,'steel',axis='y',segments=12,sides=5)
        for i in range(4):
            th=2*PI*i/4
            _rod(a,(x,-.10,1.30),(x+.31*math.cos(th),-.10,1.30+.31*math.sin(th)),.016,'steel')
        _rod(a,(x,-.04,1.30),(x,-.18,1.30),.067,'green',8)
        _rod(a,(x+.26,-.10,1.30),(x+.26,-.24,1.30),.028,'rubber')
    for x in (-.53,.53):_bearing(a,x,-.04,1.30,.080,.13)
    return a

def twist_station():
    a=_asset('triple_twist_disc_station','person')
    _post(a,0,0,1.22,.069,'green')
    for i in range(3):
        th=2*PI*i/3;c=math.cos(th);s=math.sin(th)
        _rod(a,(0,0,.12),(.75*c,.75*s,.12),.07,'green')
        a.cylinder((.75*c,.75*s,.07),(.75*c,.75*s,.19),.29,'dark_metal',12)
        a.cylinder((.75*c,.75*s,.19),(.75*c,.75*s,.215),.26,'rubber',12)
        _path(a,[(0,0,1.18),(.33*c,.33*s,1.22),(.43*c-.20*s,.43*s+.20*c,1.22)],.028,'steel')
        _rod(a,(.43*c-.20*s,.43*s+.20*c,1.22),(.43*c+.20*s,.43*s-.20*c,1.22),.03,'rubber')
    return a

def _basketball_board(a,y=0,z=3.34):
    a.box((0,y,z),(1.80,.09,1.05),'white')
    # White rectangular steel outdoor board, dark edge and shooter target.
    for x in (-.90,.90): a.box((x,y-.055,z),(.034,.025,1.08),'dark_metal')
    for zz in (z-.53,z+.53): a.box((0,y-.055,zz),(1.83,.025,.034),'dark_metal')
    for x in (-.295,.295): a.box((x,y-.061,z-.18),(.023,.015,.43),'red')
    for zz in (z-.39,z+.035): a.box((0,y-.061,zz),(.61,.015,.023),'red')
    a.box((0,y-.155,z-.29),(.16,.24,.12),'red')
    a.torus((0,y-.41,z-.29),.225,.018,'red',segments=12,sides=5)
    for i in range(10):
        th=2*PI*i/10;p=(.225*math.cos(th),y-.41+.225*math.sin(th),z-.30)
        q=(.13*math.cos(th+.28),y-.41+.13*math.sin(th+.28),z-.71)
        _rod(a,p,q,.006,'cream',4)
    a.torus((0,y-.41,z-.71),.13,.006,'cream',segments=10,sides=3)

def basketball_pole():
    a=_asset('basketball_gooseneck_pole')
    _foot(a,0,1.25)
    _path(a,[(0,1.25,.08),(0,1.25,2.75),(0,.98,3.17),(0,.10,3.34)],.092,'dark_metal',8)
    _rod(a,(0,1.25,2.35),(0,.16,3.08),.038,'steel')
    _basketball_board(a)
    a.box((0,1.25,.69),(.28,.26,1.22),'green')
    for x in (-.30,.30):
        a.beam((0,.14,3.16),(x,.07,3.50),.05,.05,'steel')
        a.box((x,.072,3.50),(.11,.032,.18),'dark_metal')
    return a

def basketball_wall():
    a=_asset('wall_mount_basketball_goal')
    _basketball_board(a,0,1.30)
    for x in (-.56,.56):
        a.box((x,1.05,1.17),(.20,.10,1.04),'dark_metal')
        _rod(a,(x,1.04,.75),(x,.05,.89),.041,'steel')
        _rod(a,(x,1.04,1.57),(x,.05,1.60),.041,'steel')
        _rod(a,(x,1.04,.75),(x,.05,1.60),.030,'steel')
        for z in (.78,1.53): _rod(a,(x,1.00,z),(x,.985,z),.022,'steel')
    for x in (-.56,.56):
        a.box((x,.072,1.31),(.10,.05,.70),'steel')
    a.box((0,.10,1.48),(1.21,.07,.07),'steel')
    return a

def _net_panel(a,p,q,height,spacing=.25,mat='cream',rad=.004,sag=0):
    # Upright net panel with individually modeled, nontransparent strands.
    L=math.dist(p,q); count=max(2,int(L/spacing))
    for i in range(count+1):
        t=i/count;x=p[0]*(1-t)+q[0]*t;y=p[1]*(1-t)+q[1]*t;z=p[2]*(1-t)+q[2]*t
        dip=sag*math.sin(PI*t)
        _rod(a,(x,y,z),(x,y,z+height-dip),rad,mat,4)
    rows=max(1,int(height/spacing))
    for i in range(rows+1):
        z=height*i/rows
        if sag and i==rows:
            _path(a,[(p[0],p[1],p[2]+z),((p[0]+q[0])/2,(p[1]+q[1])/2,(p[2]+q[2])/2+z-sag),(q[0],q[1],q[2]+z)],rad*2,mat,4)
        else: _rod(a,(p[0],p[1],p[2]+z),(q[0],q[1],q[2]+z),rad,mat,4)

def tennis_net():
    a=_asset('tennis_net')
    for x in (-6.40,6.40):
        _post(a,x,0,1.10,.053,'green')
        a.box((x,-.075,.91),(.08,.07,.15),'dark_metal')
    _net_panel(a,(-6.38,0,.06),(6.38,0,.06),.98,.23,'dark_metal',.004,.10)
    _path(a,[(-6.4,0,1.065),(0,0,.965),(6.4,0,1.065)],.025,'white',4)
    a.box((0,-.01,.50),(.037,.04,.92),'white')
    return a

def volleyball_net():
    a=_asset('volleyball_net')
    for x in (-5.12,5.12):
        _post(a,x,0,2.57,.058,'dark_metal')
        a.box((x,0,.67),(.19,.19,1.23),'blue')
        _rod(a,(x,0,2.48),(x*1.12,.84,.04),.007,'steel',4)
        _foot(a,x*1.12,.84)
    _net_panel(a,(-4.62,0,1.38),(4.62,0,1.38),1.0,.20,'cream',.0045)
    for z in (1.38,2.38): a.box((0,0,z),(9.25,.025,.045),'white')
    for x in (-4.62,4.62):
        a.box((x,0,1.88),(.045,.025,1.05),'white')
        _rod(a,(x,0,2.25),(x,0,3.12),.010,'red',6)
    return a

def soccer_goal():
    a=_asset('soccer_goal')
    for x in (-3.66,3.66):
        _path(a,[(x,0,.06),(x,0,2.44),(x,1.0,2.28),(x,1.85,.06),(x,0,.06)],.06,'white',8)
    _rod(a,(-3.66,0,2.44),(3.66,0,2.44),.06,'white',8)
    _rod(a,(-3.66,1.85,.06),(3.66,1.85,.06),.043,'white',8)
    # Horizontal net rows follow the inclined back instead of floating at its rear.
    for j in range(10):
        t=j/9; y=1.0+.85*t; z=2.27-2.20*t
        _rod(a,(-3.66,y,z),(3.66,y,z),.004,'cream',4)
    for y in (.25,.50,.75):
        z=2.43-.16*y
        _rod(a,(-3.66,y,z),(3.66,y,z),.004,'cream',4)
    for x in [-3.66+i*.305 for i in range(25)]:
        _path(a,[(x,0,2.43),(x,1.0,2.27),(x,1.85,.07)],.004,'cream',4)
    for side in (-1,1):
        x=side*3.66
        for z in (.42,.84,1.26,1.68,2.10):
            yy=1.85-.85*(z-.07)/2.20
            _rod(a,(x,0,z),(x,yy,z),.004,'cream',4)
    return a

def lacrosse_goal():
    a=_asset('lacrosse_goal')
    for x in (-.915,.915):
        _rod(a,(x,0,.04),(x,0,1.83),.045,'orange',8)
        _rod(a,(x,0,.04),(0,1.83,.04),.037,'orange',8)
        _rod(a,(x,0,1.83),(0,1.83,.04),.015,'dark_metal')
    _rod(a,(-.915,0,1.83),(.915,0,1.83),.045,'orange',8)
    # Both triangular side nets taper into the rear goal point.
    for s in (-1,1):
        for i in range(1,10):
            t=i/10
            _rod(a,(s*.915,0,1.83*t),(s*.915*(1-t),1.83*t,.04),.0045,'cream',4)
            _rod(a,(s*.915*(1-t),1.83*t,1.83*(1-t)),(s*.915*(1-t),1.83*t,.04),.0045,'cream',4)
    for x in [-.915+i*.183 for i in range(11)]: _rod(a,(x,0,1.83),(0,1.83,.04),.0045,'cream',4)
    return a

def baseball_backstop():
    a=_asset('baseball_backstop')
    panels=[((-2.7,0,0),(2.7,0,0)),((-4.2,1.5,0),(-2.7,0,0)),((2.7,0,0),(4.2,1.5,0))]
    posts=[(-4.2,1.5),(-2.7,0),(0,0),(2.7,0),(4.2,1.5)]
    for x,y in posts: _post(a,x,y,3.2,.048,'steel')
    for p,q in panels:
        _net_panel(a,(p[0],p[1],.1),(q[0],q[1],.1),3.05,.28,'dark_metal',.0045)
        _rod(a,(p[0],p[1],3.18),(q[0],q[1],3.18),.034,'steel')
    for x in (-2.7,0,2.7): _rod(a,(x,0,3.18),(x,.92,3.98),.038,'steel')
    _rod(a,(-2.7,.92,3.98),(2.7,.92,3.98),.038,'steel')
    for i in range(19):
        x=-2.7+i*.30;_rod(a,(x,0,3.18),(x,.92,3.98),.0045,'dark_metal',4)
    for t in (.25,.5,.75): _rod(a,(-2.7,.92*t,3.18+.80*t),(2.7,.92*t,3.18+.80*t),.0045,'dark_metal',4)
    return a

def dugout_bench():
    a=_asset('dugout_equipment_bench')
    for x in (-1.65,0,1.65):
        for y in (-.25,.25): _post(a,x,y,.49,.035,'dark_metal')
        _rod(a,(x,.25,.45),(x,.25,1.06),.035,'dark_metal')
    for y in (-.17,0,.17): a.box((0,y,.48),(3.9,.155,.06),'wood')
    for z in (.76,.96): a.box((0,.27,z),(3.9,.07,.16),'wood')
    # Bat shelf and ball cubbies distinguish this from an ordinary park bench.
    a.box((0,.43,1.12),(3.9,.44,.055),'wood_dark')
    for x in (-1.82,-1.20,-.58,.04,.66,1.28,1.90): a.box((x,.44,1.28),(.038,.42,.29),'wood')
    a.box((0,.63,1.28),(3.9,.035,.30),'wood')
    for x in (-1.65,0,1.65):
        for y in (-.17,.17):_rod(a,(x,y,.51),(x,y,.528),.015,'steel',6)
        a.box((x,0,.43),(.055,.47,.055),'dark_metal')
    return a

def scoreboard():
    a=_asset('baseball_scoreboard')
    for x in (-1.16,1.16): _post(a,x,0,2.80,.088,'dark_metal')
    a.box((0,0,2.27),(3.34,.20,1.44),'green')
    for x in (-1.64,1.64): a.box((x,-.12,2.27),(.045,.04,1.46),'steel')
    for z in (1.55,2.99): a.box((0,-.12,z),(3.32,.04,.045),'steel')
    for z in (2.30,2.69):
        a.box((-1.04,-.113,z),(.70,.02,.20),'cream')
        for x in (-.42,.14,.70,1.26):
            a.box((x,-.13,z),(.42,.025,.28),'black')
            # Unlit segmented numerals, robust and readable without text fonts.
            for dz in (-.089,0,.089): a.box((x,-.15,z+dz),(.15,.018,.025),'yellow')
            for dx in (-.075,.075):
                for dz in (-.045,.045): a.box((x+dx,-.15,z+dz),(.021,.018,.077),'yellow')
    for x in (-.66,0,.66):
        a.box((x,-.13,1.84),(.44,.024,.24),'black')
        for dx in (-.11,.0,.11): a.cylinder((x+dx,-.146,1.84),(x+dx,-.16,1.84),.027,'light',8)
    for x in (-1.16,1.16):
        a.box((x,.135,2.27),(.15,.10,1.46),'dark_metal')
        a.box((x,.18,1.53),(.23,.16,.09),'steel')
    a.box((1.18,.13,1.77),(.47,.036,.32),'dark_metal')
    for x in (.99,1.16,1.33):a.box((x,.153,1.77),(.020,.025,.23),'steel')
    return a

def bleachers():
    a=_asset('four_row_bleachers')
    for x in (-1.74,0,1.74):
        a.box((x,.45,.07),(.13,2.78,.14),'dark_metal')
        a.beam((x,-.84,.18),(x,1.53,1.56),.10,.11,'steel')
        for j in range(4):
            y=-.66+j*.65;z=.41+j*.37
            a.box((x,y,z*.5),(.085,.085,z),'steel')
    for j in range(4):
        y=-.66+j*.65;z=.41+j*.37
        a.box((0,y,z),(4.16,.31,.065),'silver')
        a.box((0,y-.29,z-.29),(4.16,.24,.060),'silver')
        a.box((0,y-.155,z-.026),(4.16,.034,.082),'metal')
    for x in (-2.10,2.10):
        _rail(a,(x,-.75,.46),(x,1.40,1.61),.77,'steel')
    _rail(a,(-2.10,1.52,1.53),(2.10,1.52,1.53),.88,'steel')
    for x in (-1.4,-.7,0,.7,1.4): _rod(a,(x,1.52,1.58),(x,1.52,2.38),.017,'steel')
    return a

def umpire_chair():
    a=_asset('tennis_umpire_chair')
    for y in (-.46,.46):
        a.beam((-.75,y,.06),(-.37,y,1.72),.065,.065,'green')
        a.beam((.65,y,.06),(.23,y,1.72),.065,.065,'green')
        _rod(a,(-.66,y,.35),(.43,y,1.40),.023,'steel')
        _rod(a,(.53,y,.35),(-.46,y,1.40),.023,'steel')
        _rail(a,(-.38,y,1.76),(.28,y,1.76),.38,'green',False)
    for z in (.27,.56,.85,1.14,1.43):
        x=.65-.42*z/1.72; _rod(a,(x,-.46,z),(x,.46,z),.026,'steel')
    a.box((-.08,0,1.75),(.66,.97,.075),'wood')
    a.box((-.40,0,2.00),(.075,.94,.42),'wood')
    a.box((.35,0,1.48),(.23,.84,.055),'steel')
    a.box((.37,0,2.02),(.32,.77,.035),'green')
    for y in (-.46,.46):
        for x,z in ((-.42,1.65),(.28,1.65),(.52,.34),(-.64,.34)):
            _rod(a,(x,y-.022,z),(x,y+.026,z),.026,'steel',6)
    return a

def quarter_pipe():
    a=_asset('skate_quarter_pipe')
    pts=[(-1.15,0),(1.35,0),(1.35,1.58),(.89,1.58),(.83,1.42),(.70,1.11),(.46,.77),(.10,.45),(-.35,.22),(-1.15,.10)]
    _profile(a,pts,2.34,'concrete')
    _rod(a,(.91,-1.2,1.61),(.91,1.2,1.61),.033,'steel',8)
    for y in (-1.18,1.18): _rail(a,(.95,y,1.62),(1.34,y,1.62),.94,'dark_metal')
    _rail(a,(1.34,-1.18,1.62),(1.34,1.18,1.62),.94,'dark_metal')
    a.box((1.12,0,1.60),(.43,2.34,.055),'dark_metal')
    for y in (-1.13,1.13):
        for x,z in ((-.80,.13),(.1,.45),(.70,1.11)):
            _rod(a,(x,y,z),(x,y+.014,z),.012,'dark_metal',6)
    return a

def funbox():
    a=_asset('skate_funbox')
    _profile(a,[(-2.6,0),(2.6,0),(2.6,.07),(.65,.73),(-.75,.73),(-2.6,.07)],2.2,'concrete')
    a.box((-.05,.48,.88),(1.44,.38,.30),'concrete_light')
    a.box((-.05,.48,1.04),(1.46,.39,.028),'steel')
    for x in (-.75,.65): a.box((x,-.03,.745),(.035,1.2,.025),'metal')
    for side in (-1,1):
        a.box((-.05,.48+side*.205,.985),(1.48,.022,.10),'steel')
        for x in (-.56,.43):_rod(a,(x,.48+side*.214,.97),(x,.48+side*.23,.97),.014,'dark_metal',6)
    return a

def grind_rail():
    a=_asset('kinked_grind_rail')
    pts=[(-1.90,0,.85),(-.50,0,.85),(.64,0,.42),(1.92,0,.42)]
    for p,q in zip(pts,pts[1:]): a.beam(p,q,.095,.08,'steel')
    for x,h in ((-1.55,.83),(-.50,.83),(.65,.40),(1.61,.40)):
        _foot(a,x,0);a.box((x,0,h/2),(.065,.065,h),'dark_metal')
    for x,h in ((-1.55,.83),(-.50,.83),(.65,.40),(1.61,.40)):
        a.box((x,0,h-.025),(.19,.13,.045),'dark_metal')
    return a

def bowl_corner():
    a=_asset('skate_bowl_corner')
    # Quarter bowl with radial bands and an upper deck; curved profile remains low poly.
    radii=[(.0,0),(.52,.05),(1.02,.25),(1.39,.62),(1.57,1.13),(1.61,1.48),(2.07,1.48)]
    n=8;vs=[]
    # Exclude the center ring and build a nondegenerate fan.
    vs.append((0,0,0))
    for r,z in radii[1:]:
        for i in range(n+1):
            th=PI*i/(2*n);vs.append((r*math.cos(th),r*math.sin(th),z))
    fs=[(0,1+i,2+i) for i in range(n)]
    for k in range(5):
        for i in range(n):
            p=1+k*(n+1)+i;q=p+n+1;fs.append((p,q,q+1,p+1))
    # Close outer wall and side wedge profiles.
    outer=1+5*(n+1);bottom=[]
    for i in range(n+1):
        p=vs[outer+i];bottom.append(len(vs));vs.append((p[0],p[1],0))
    for i in range(n): fs.append((outer+i,bottom[i],bottom[i+1],outer+i+1))
    fs.append(tuple([0]+[1+k*(n+1) for k in range(6)]+[bottom[0]]))
    fs.append(tuple(reversed([0]+[1+k*(n+1)+n for k in range(6)]+[bottom[-1]])))
    fs.append(tuple([0]+list(reversed(bottom))))
    a.mesh(vs,fs,'concrete')
    _path(a,[(1.615*math.cos(PI*i/16),1.615*math.sin(PI*i/16),1.50) for i in range(9)],.03,'steel',6)
    return a

def manual_pad():
    a=_asset('skate_manual_pad')
    a.box((0,0,.20),(2.66,1.32,.40),'concrete')
    for y in (-.655,.655):
        a.box((0,y,.408),(2.70,.05,.035),'steel')
        a.box((0,y,.36),(2.70,.025,.11),'steel')
    # Offset lower entrance step makes the silhouette unlike a generic slab.
    a.box((-1.48,0,.10),(.30,.86,.20),'concrete_light')
    for x in (-.85,0,.85):
        for y in (-.67,.67): _rod(a,(x,y,.36),(x,y*1.013,.36),.018,'dark_metal',6)
    return a

def disc_golf():
    a=_asset('disc_golf_basket','person')
    _post(a,0,0,1.58,.034,'steel')
    a.torus((0,0,.73),.34,.022,'steel',segments=12,sides=5)
    a.torus((0,0,.50),.24,.018,'steel',segments=12,sides=4)
    a.cylinder((0,0,1.43),(0,0,1.52),.30,'yellow',12)
    for i in range(12):
        th=2*PI*i/12;c=math.cos(th);s=math.sin(th)
        _rod(a,(.34*c,.34*s,.73),(.24*c,.24*s,.50),.012,'steel',4)
        _rod(a,(.24*c,.24*s,.50),(0,0,.50),.012,'steel',4)
        _path(a,[(.28*c,.28*s,1.43),(.20*c,.20*s,1.03),(.10*c,.10*s,.81)],.008,'steel',4)
    a.torus((0,0,.81),.10,.014,'steel',segments=12,sides=4)
    a.box((0,0,1.66),(.15,.025,.15),'green')
    for i in range(6):
        t=PI*i/3
        _path(a,[(.19*math.cos(t),.19*math.sin(t),1.43),(.15*math.cos(t+.12),.15*math.sin(t+.12),1.07),(.075*math.cos(t+.2),.075*math.sin(t+.2),.82)],.008,'steel',4)
    return a

def horseshoe_pit():
    a=_asset('horseshoe_pitching_pit')
    a.box((0,0,.035),(1.8,2.20,.07),'sand')
    for x in (-.94,.94): a.box((x,0,.11),(.12,2.40,.22),'wood_dark')
    for y in (-1.14,1.14): a.box((0,y,.11),(1.98,.12,.22),'wood_dark')
    _rod(a,(0,.15,.06),(0,.07,.46),.024,'steel',8)
    for x in (-.91,.91): a.box((x,1.14,.39),(.12,.12,.57),'wood_dark')
    for z in (.30,.52): a.box((0,1.16,z),(1.94,.065,.18),'wood')
    for x in (-.89,.89):
        for y in (-.99,.99):_rod(a,(x,y,.20),(x,y,.23),.020,'steel',6)
    # A pair of recognisable horseshoes supplies the functional sporting context.
    for x,y,t in ((-.39,-.28,.4),(.44,.47,-.8)):
        a.torus((x,y,.095),.095,.017,'steel',segments=8,sides=4,arc=PI*1.4)
    return a

def table_tennis():
    a=_asset('outdoor_table_tennis')
    a.box((0,0,.735),(2.74,1.525,.070),'blue')
    for x in (-1.365,1.365): a.box((x,0,.773),(.021,1.525,.008),'white')
    for y in (-.755,.755): a.box((0,y,.773),(2.74,.021,.008),'white')
    a.box((0,0,.773),(2.74,.015,.008),'white')
    for x in (-.84,.84):
        a.box((x,0,.32),(.19,1.06,.64),'concrete')
        a.box((x,0,.075),(.44,1.33,.15),'concrete')
    # Perforated rigid steel net common at city recreation courts.
    for y in (-.81,.81): _rod(a,(0,y,.75),(0,y,.94),.019,'steel')
    _net_panel(a,(0,-.80,.78),(0,.80,.78),.15,.08,'steel',.005)
    a.box((0,0,.94),(.025,1.65,.022),'white')
    return a

def tetherball():
    a=_asset('tetherball_pole')
    _post(a,0,0,3.06,.042,'steel')
    a.cylinder((0,0,0),(0,0,.08),.24,'concrete',12)
    a.torus((0,0,3.03),.062,.011,'dark_metal',axis='x',segments=8,sides=4)
    _path(a,[(0,0,3.04),(.32,.03,2.42),(.64,.055,1.73)],.008,'cream',4)
    a.sphere((.70,.06,1.62),.125,'yellow',segments=10,rings=5)
    a.torus((.70,.06,1.62),.126,.004,'wood_dark',axis='x',segments=10,sides=3)
    return a

_FACTORIES = [
('straight_slide',straight_slide),('wave_slide',wave_slide),('curved_slide',curved_slide),
('double_swing',double_swing),('toddler_bucket_swing',bucket_swing),('tire_swing',tire_swing),
('monkey_bars',monkey_bars),('dome_climber',dome_climber),('climbing_wall',climbing_wall),('rope_pyramid',rope_pyramid),
('seesaw',seesaw),('four_seat_spring_rocker',spring_rocker),('merry_go_round',merry_go_round),
('zigzag_balance_beam',balance_beam),('stepping_log_course',stepping_logs),('crawl_tunnel',crawl_tunnel),
('overhead_ring_traverse',ring_traverse),('roofed_play_tower',play_tower),('accessible_sand_table',sand_table),('playground_abacus_panel',activity_panel),
('three_height_pullup_station',pullup_station),('parallel_dip_station',dip_station),('incline_situp_bench',situp_bench),
('outdoor_elliptical',elliptical),('air_walker',air_walker),('seated_chest_press',chest_press),('outdoor_rowing_station',rowing_station),
('seated_leg_press',leg_press),('shoulder_rotation_wheels',shoulder_wheels),('triple_twist_disc_station',twist_station),
('basketball_gooseneck_pole',basketball_pole),('wall_mount_basketball_goal',basketball_wall),('tennis_net',tennis_net),
('volleyball_net',volleyball_net),('soccer_goal',soccer_goal),('lacrosse_goal',lacrosse_goal),('baseball_backstop',baseball_backstop),
('dugout_equipment_bench',dugout_bench),('baseball_scoreboard',scoreboard),('four_row_bleachers',bleachers),
('tennis_umpire_chair',umpire_chair),('skate_quarter_pipe',quarter_pipe),('skate_funbox',funbox),('kinked_grind_rail',grind_rail),
('skate_bowl_corner',bowl_corner),('skate_manual_pad',manual_pad),('disc_golf_basket',disc_golf),('horseshoe_pitching_pit',horseshoe_pit),
('outdoor_table_tennis',table_tennis),('tetherball_pole',tetherball),
]

REVIEW_REASONS = {
'straight_slide':'Rebuilt separate chute panels as a continuous formed trough with thickness, hemmed lips and softened transitions; added entrance grab rails and deck mounts.',
'wave_slide':'Rebuilt faceted panel chute as a continuous formed trough, refined transition profile and added entrance grab rails and deck supports.',
'double_swing':'Replaced rigid slab seats with dipped, thickened flexible belt-seat geometry.',
'outdoor_elliptical':'Molded footpads, crank and linkage bearings, anti-slip ribs and drivetrain guard base.',
'air_walker':'Connected swinging arms to bushed pivot axles with mechanical stop housings.',
'seated_chest_press':'Contoured molded seat/back, visible pivot housings and linked resistance struts.',
'outdoor_rowing_station':'Contoured seat, axle bearings, linkage/resistance struts and non-slip footplate ribs.',
'seated_leg_press':'Contoured seat/back shells, axle housings, resistance linkages and footplate heel stops.',
'shoulder_rotation_wheels':'Added visible bearing bushes and axle-end hardware at wheel rotation axes.',
'seesaw':'Added pivot bearing assembly, beam saddle brackets and bumper contact plates.',
'four_seat_spring_rocker':'Added upper/lower spring mounting plates, anchor fasteners and seat supports.',
'merry_go_round':'Added radial deck underframe and center bearing support flange.',
'crawl_tunnel':'Added shaped support cradles and end-rim assembly fasteners.',
'roofed_play_tower':'Added deck joists and diagonal roof support braces.',
'accessible_sand_table':'Added structural tray rim support rails and leg socket brackets.',
'playground_abacus_panel':'Added rod end bearings where the beads slide into frame.',
'basketball_gooseneck_pole':'Added backboard mounting plates and spread support struts.',
'wall_mount_basketball_goal':'Added backboard support rails and mounting connection plates.',
'dugout_equipment_bench':'Added board support brackets and seat fixing heads.',
'baseball_scoreboard':'Added rear support rails, mounting clamps and rear service ventilation panel.',
'disc_golf_basket':'Added the inner catching-chain array distinct from the outer basket wires.',
'horseshoe_pitching_pit':'Added timber assembly bolts and separate horseshoes as functional equipment.',
'tennis_umpire_chair':'Added exposed ladder-frame joint fasteners.',
'kinked_grind_rail':'Added structural saddle plates between posts and grind rail.',
'skate_funbox':'Added wrap-around grind ledge facing and side fixing heads.',
'skate_quarter_pipe':'Added transition-panel fixing points along supported side edges.',
}
REVIEW_RETAIN={
'curved_slide':'Existing swept curved chute, central radial supports, platform and ladder already form a mechanically readable installation.',
'toddler_bucket_swing':'Existing bucket seat leg openings, four sides, chains and braced frame define the appropriate design.',
'tire_swing':'Existing tread blocks, three-point suspension and braced frame already carry specific construction.',
'monkey_bars':'Existing rung spacing, ladder sides, capped posts and anchor plates are appropriately economical.',
'dome_climber':'Existing triangular geodesic tubes, separate node joints and base anchors provide complete structure.',
'climbing_wall':'Existing separate wall panels, staggered faceted handholds and bolts carry the needed detail.',
'rope_pyramid':'Existing nested cable rings, radial ropes and top/base anchors are already functional.',
'zigzag_balance_beam':'Existing beam joints, independent support posts and anchor feet are complete for a simple fixture.',
'stepping_log_course':'Existing height progression, faceted bark, separate cut ends and endgrain rings define the simple object.',
'overhead_ring_traverse':'Existing hanging rings, suspension rods, access rungs and capped supporting structure are sufficient.',
'four_row_bleachers':'Existing stepped footboards, seat lips, diagonal framework and guardrails already resolve construction.',
'three_height_pullup_station':'Existing varied bar heights, grips, capped posts and anchor plates match a simple static installation.',
'parallel_dip_station':'Existing gripped parallel bars, lower ties and anchors provide complete structure.',
'incline_situp_bench':'Existing slatted inclined support frame, paired rollers and post anchors carry the needed form.',
'triple_twist_disc_station':'Existing separate rotating plates, arm supports and handle geometry already resolve the equipment.',
'tennis_net':'Existing net sag, centre strap, winding housings and posts are already structurally specific.',
'volleyball_net':'Existing net mesh, tape borders, antennas, padded posts and guy wires are complete.',
'soccer_goal':'Existing bent rear supports and net following top/back/side geometry provide the required construction.',
'lacrosse_goal':'Existing triangular rear net and frames are complete and appropriately economical.',
'baseball_backstop':'Existing side panels, overhanging top fence, post feet and wire mesh already resolve construction.',
'skate_bowl_corner':'Existing radial curved transition and coping form a correct simple concrete section.',
'skate_manual_pad':'Existing entrance step, wrap-around steel edging and edge fasteners define the simple object.',
'outdoor_table_tennis':'Existing pedestal supports, field markings and perforated rigid net complete the table.',
'tetherball_pole':'Existing swivel ring, rope bend, ball seam and weighted base are complete.'
}
REVIEW={}

# Each registered factory returns final bottom-centered authored geometry.
for _name, _fn in _FACTORIES:
    _size = 'person' if _name in {'four_seat_spring_rocker','accessible_sand_table','playground_abacus_panel','parallel_dip_station','incline_situp_bench','outdoor_elliptical','air_walker','seated_chest_press','outdoor_rowing_station','seated_leg_press','shoulder_rotation_wheels','triple_twist_disc_station','disc_golf_basket'} else 'large'
    REVIEW['b09_'+_name]={'status':'revised' if _name in REVIEW_REASONS else 'retained','reason':REVIEW_REASONS.get(_name,REVIEW_RETAIN.get(_name,'Reviewed silhouette, construction and functional details; no geometry change needed.'))}
    def _factory(fn=_fn):
        return fn().bottom_center()
    register('b09_'+_name,CAT,_size,_factory)
