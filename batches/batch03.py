"""Fifty independently identifiable passenger vehicles and cycles.
X points forward, Z points upward; dimensions are in metres.
Shared construction describes real components, not color-only variants.
"""
from assetlib import Asset, register
import math

CAT = 'passenger_vehicles'

def _triangulate(poly):
    """Ear clipping for the wheel-arch cutouts of the side panels."""
    ids = list(range(len(poly)))
    area = sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in ids)
    if area < 0: ids.reverse()
    out = []
    def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def inside(p,a,b,c):
        return cross(a,b,p) >= -1e-10 and cross(b,c,p) >= -1e-10 and cross(c,a,p) >= -1e-10
    for _ in range(len(poly)*len(poly)):
        if len(ids) <= 3: break
        for k,b in enumerate(ids):
            aa,cc = ids[k-1],ids[(k+1)%len(ids)]
            if cross(poly[aa],poly[b],poly[cc]) <= 1e-10: continue
            if any(inside(poly[q],poly[aa],poly[b],poly[cc]) for q in ids if q not in (aa,b,cc)): continue
            out.append((aa,b,cc)); ids.pop(k); break
        else: raise ValueError('Cannot triangulate body profile')
    if len(ids)==3: out.append(tuple(ids))
    return out

def _profile(a, poly, width, mat):
    n=len(poly)
    vs=[(x,y,z) for y in (-width/2,width/2) for x,z in poly]
    tris=_triangulate(poly)
    faces=list(tris)+[tuple(i+n for i in reversed(t)) for t in tris]
    faces += [(i,i+n,(i+1)%n+n,(i+1)%n) for i in range(n)]
    a.mesh(vs,faces,mat)

def _quad(a, ps, mat): a.mesh(ps,[(0,1,2,3)],mat)

def _auto_wheel(a,x,y,r=.34,width=.22,style='alloy'):
    a.torus((x,y,r),r*.76,r*.24,'rubber',axis='y',segments=12,sides=4)
    a.cylinder((x,y-width*.45,r),(x,y+width*.45,r),r*.61,'dark_metal',sides=12)
    side=1 if y>0 else -1
    a.cylinder((x,y+side*width*.4,r),(x,y+side*width*.51,r),r*.2,'silver',sides=8)
    if style=='classic':
        a.torus((x,y+side*width*.51,r),r*.6,r*.08,'cream',axis='y',segments=12,sides=4)
        a.cylinder((x,y+side*width*.4,r),(x,y+side*width*.53,r),r*.37,'silver',sides=10)
    else:
        for i in range(5):
            th=2*math.pi*i/5
            p=(x+math.cos(th)*r*.18,y+side*width*.53,r+math.sin(th)*r*.18)
            q=(x+math.cos(th)*r*.52,y+side*width*.53,r+math.sin(th)*r*.52)
            a.beam(p,q,r*.105,r*.06,'silver')

def _body(a,L,W,belt,wb,r,paint,style='alloy'):
    floor=r*.79
    p=[(-L/2+.045,floor)]
    for x in (-wb/2,wb/2):
        ar=r+.065
        p.append((x-ar,floor))
        for j in range(7):
            th=math.pi-j*math.pi/6
            p.append((x+ar*math.cos(th),r+ar*math.sin(th)))
        p.append((x+ar,floor))
    p += [(L/2-.045,floor),(L/2,belt*.61),(L/2-.09,belt*.94),(L/2-.45,belt),(-L/2+.38,belt),(-L/2,belt*.9),(-L/2,belt*.6)]
    _profile(a,p,W,paint)
    a.box((0,0,r*.8),(wb,W*.7,.15),'dark_metal')
    for x in (-wb/2,wb/2):
        for y in (-W/2,W/2): _auto_wheel(a,x,y,r,style=style)
    # Raised molded lips trace the upper part of every wheel opening.
    for x in (-wb/2,wb/2):
        for sy in (-1,1):
            pts=[]
            for j in range(7):
                th=math.pi-j*math.pi/6
                pts.append((x+(r+.071)*math.cos(th),sy*(W/2+.005),r+(r+.071)*math.sin(th)))
            a.tube(pts,.025,paint,sides=4)

def _cabin(a,xr,xf,rr,rf,zbase,zroof,W,paint,panes=2,backglass=True):
    wb=W*.965; wr=W*.81
    vs=[(xr,-wb/2,zbase),(xf,-wb/2,zbase),(xf,wb/2,zbase),(xr,wb/2,zbase),
        (rr,-wr/2,zroof),(rf,-wr/2,zroof),(rf,wr/2,zroof),(rr,wr/2,zroof)]
    a.mesh(vs,[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],paint)
    lo=zbase+.085; hi=zroof-.075
    tlo=(lo-zbase)/(zroof-zbase); thi=(hi-zbase)/(zroof-zbase)
    ylo=(wb+(wr-wb)*tlo)/2+.006; yhi=(wb+(wr-wb)*thi)/2+.006
    rlo=xr+(rr-xr)*tlo+.08; rhi=xr+(rr-xr)*thi+.08
    flo=xf+(rf-xf)*tlo-.08; fhi=xf+(rf-xf)*thi-.08
    for s in (-1,1):
        for j in range(panes):
            u0=j/panes;u1=(j+1)/panes; gap=.038 if panes>1 else .0
            _quad(a,[(rlo+(flo-rlo)*u0+gap,s*ylo,lo),(rlo+(flo-rlo)*u1-gap,s*ylo,lo),
                     (rhi+(fhi-rhi)*u1-gap,s*yhi,hi),(rhi+(fhi-rhi)*u0+gap,s*yhi,hi)],'glass')
    def endglass(xbot,xtop,side):
        xb=xbot+(xtop-xbot)*tlo+side*.006
        xt=xbot+(xtop-xbot)*thi+side*.006
        _quad(a,[(xb,-ylo+.1,lo),(xb,ylo-.1,lo),(xt,yhi-.07,hi),(xt,-yhi+.07,hi)],'glass')
    endglass(xf,rf,1)
    if backglass: endglass(xr,rr,-1)

def _details(a,L,W,belt,paint,doors=4,round_lights=False,offroad=False):
    # Small components preserve scale and vehicle orientation.
    for s in (-1,1):
        a.box((L/2+.018,s*W*.33,belt*.76),(.035,W*.23,.125),'light')
        a.box((-L/2-.011,s*W*.37,belt*.72),(.04,W*.16,.16),'red')
        a.box((L/2-.17,s*(W/2+.018),belt*.53),(.15,.024,.065),'orange')
        a.box((L*.10,s*(W/2+.095),belt+.19),(.23,.19,.13),paint)
        a.beam((L*.04,s*W*.47,belt+.10),(L*.08,s*(W/2+.075),belt+.18),.04,mat='dark_metal')
        for x in ((-.54,.53) if doors>=4 else (0.1,)):
            a.box((x,s*(W/2+.012),belt-.13),(.19,.025,.045),'silver')
            a.box((x-.4,s*(W/2+.01),belt*.72),(.009,.015,belt*.4),'dark_metal')
    a.box((L/2+.027,0,belt*.55),(.05,W*.5,.18),'black')
    for j in range(3): a.box((L/2+.057,0,belt*.49+j*.055),(.015,W*.49,.013),'metal')
    for x in (-L/2-.02,L/2+.025):
        a.box((x,0,belt*.37),(.12,W*.89,.12),'dark_metal')
        a.box((x+(.065 if x>0 else -.065),0,belt*.5),(.014,.32,.13),'white')
    if round_lights:
        for y in (-W*.32,W*.32):
            a.cylinder((L/2+.04,y,belt*.78),(L/2+.08,y,belt*.78),.105,'silver',sides=10)
            a.cylinder((L/2+.08,y,belt*.78),(L/2+.09,y,belt*.78),.081,'light',sides=10)
    if offroad:
        for s in (-1,1): a.box((0,s*(W/2+.09),.4),(L*.57,.18,.11),'black')
        a.beam((L/2+.13,-W*.43,.46),(L/2+.13,W*.43,.46),.07,mat='dark_metal')
        for y in (-W*.31,W*.31): a.beam((L/2+.13,y,.45),(L/2+.13,y,.91),.065,mat='dark_metal')

def _rack(a,xr,xf,W,z,paint='dark_metal'):
    for s in (-1,1):
        a.beam((xr,s*W*.32,z),(xf,s*W*.32,z),.055,mat=paint)
        for x in (xr+.14,xf-.14): a.beam((x,s*W*.32,z-.10),(x,s*W*.32,z),.055,mat=paint)
    for x in (xr+.15,xf-.15): a.beam((x,-W*.35,z+.025),(x,W*.35,z+.025),.045,mat=paint)

def _seats(a,x,W,z):
    for s in (-1,1):
        a.box((x,s*W*.22,z),(.42,W*.32,.12),'black')
        a.box((x-.17,s*W*.22,z+.25),(.13,W*.31,.5),'black',rot=(0,-.12,0))
        a.box((x-.2,s*W*.22,z+.54),(.12,W*.19,.16),'black')

def _pickup_bed(a,L,W,belt,cabrear,paint,stepside=False):
    back=-L/2+.08; front=cabrear-.08
    a.box(((back+front)/2,0,belt-.22),(front-back,W*.84,.10),'dark_metal')
    for s in (-1,1):
        a.box(((back+front)/2,s*W*.43,belt+.095),(front-back,.14,.31),paint)
        a.box(((back+front)/2,s*W*.43,belt+.26),(front-back,.16,.045),'black')
    a.box((back,0,belt+.08),(.12,W*.85,.31),paint)
    a.box((back-.063,0,belt+.14),(.015,.29,.06),'black')
    if stepside:
        for s in (-1,1):
            a.box((cabrear-.23,s*W*.58,.41),(.35,.24,.11),'dark_metal')
            a.box((-L*.29,s*W*.55,.88),(1.03,.27,.16),paint)

def _vehicle(name,spec):
    L,W,belt,wb,r,paint,kind,cab=spec
    a=Asset(name,CAT,'large',style='faceted city fleet',forward_axis='+X')
    old=kind in ('classic','stepside','vintage_pickup')
    _body(a,L,W,belt,wb,r,paint,'classic' if old else 'alloy')
    xr,xf,rr,rf,roof,panes=cab
    isopen=kind in ('roadster','convertible')
    if isopen:
        a.box(((xr+xf)/2,0,belt+.013),(xf-xr,W*.79,.045),'black')
        _seats(a, .02 if kind=='roadster' else .3,W,belt+.055)
        if kind=='convertible': _seats(a,-.68,W,belt+.03)
        _cabin(a,xf-.10,xf,rf-.10,rf,belt,roof,W,paint,1,False)
        # A-frame windshield retains an open, roofless passenger compartment.
        for s in (-1,1): a.beam((xf,s*W*.475,belt),(rf,s*W*.395,roof),.055,mat=paint)
        a.beam((rf,-W*.4,roof),(rf,W*.4,roof),.055,mat=paint)
        a.box((xr-.06,0,belt+.07),(.24,W*.76,.15),'black')
        a.torus((.54,-W*.24,belt+.38),.13,.018,'black',axis='x',segments=10,sides=4)
        if kind=='roadster':
            for s in (-1,1): a.tube([(-.46,s*W*.22,belt+.26),(-.46,s*W*.22,belt+.54),(-.68,s*W*.22,belt+.54),(-.68,s*W*.22,belt+.26)],.037,'silver',sides=6)
    else:
        _cabin(a,xr,xf,rr,rf,belt,roof,W,paint,panes)
    doors=2 if kind in ('coupe','muscle','roadster','convertible','micro','jeep','regular_pickup','stepside','vintage_pickup') else 4
    _details(a,L,W,belt,paint,doors,round_lights=old or kind in ('jeep','micro'),offroad=kind in ('jeep','offroad','full_suv'))
    if 'pickup' in kind or kind=='stepside':
        _pickup_bed(a,L,W,belt,xr,paint,kind=='stepside')
        if kind=='electric_pickup':
            for s in (-1,1):
                a.beam((-L/2+.28,s*W*.39,belt+.23),(xr-.08,s*W*.39,roof-.08),.10,.07,paint)
            a.box((L/2+.063,0,belt*.85),(.018,W*.91,.035),'light')
        if kind=='vintage_pickup':
            for s in (-1,1): a.box((.22,s*W*.54,.4),(1.32,.20,.09),'dark_metal')
            a.box((L*.32,0,belt+.065),(L*.23,W*.64,.14),paint)
    if kind in ('wagon','longroof','compact_suv','suv','full_suv','offroad','crossover','coupe_crossover','van','highroof','accessible'):
        _rack(a,rr+.05,rf-.05,W,roof+.105)
    if kind in ('van','highroof','accessible','minivan'):
        for s in (-1,1):
            a.box((-.35,s*(W/2+.015),belt-.03),(1.1,.027,.025),'dark_metal')
            a.box((-.6,s*(W/2+.037),belt-.13),(.23,.04,.045),'silver')
            a.box((-.28,s*(W/2+.06),.34),(1.25,.13,.09),'dark_metal')
    if kind=='highroof':
        a.box((-.2,0,roof+.075),(.42,.45,.13),'white')
        for x in (-.83,.1,.68): a.box((x,0,roof+.018),(.16,W*.61,.025),'metal')
    if kind=='accessible':
        # Folding ramp is stowed upright at the back; wheelchair access sign inset.
        a.box((-L/2-.13,0,.75),(.10,W*.60,.73),'dark_metal')
        for y in (-W*.23,0,W*.23): a.box((-L/2-.185,y,.75),(.025,.028,.69),'silver')
        for s in (-1,1):
            a.box((-.68,s*(W/2+.025),belt*.72),(.22,.02,.24),'blue')
            a.torus((-.68,s*(W/2+.04),belt*.69),.058,.012,'white',axis='y',segments=8,sides=4)
            a.cylinder((-.69,s*(W/2+.041),belt*.75),(-.69,s*(W/2+.041),belt*.84),.013,'white',sides=6)
    if kind in ('jeep','offroad'):
        a.cylinder((-L/2-.15,0,belt),(-L/2-.34,0,belt),r*.91,'rubber',sides=12)
        a.cylinder((-L/2-.35,0,belt),(-L/2-.37,0,belt),r*.49,'silver',sides=8)
        for y in (-W*.32,W*.32): a.cylinder((.42,y,roof+.07),(.47,y,roof+.07),.095,'light',sides=8)
    if kind=='muscle':
        _profile(a,[(L*.16,belt),(L*.18,belt+.14),(L*.31,belt+.14),(L*.36,belt)],W*.24,'black')
        for y in (-.24,.24): a.box((L*.27,y,belt+.008),(L*.31,.13,.015),'cream')
        a.box((-L*.41,0,belt+.20),(.16,W*.77,.07),'black')
        for y in (-W*.28,W*.28): a.box((-L*.41,y,belt+.09),(.08,.08,.2),'black')
    if kind=='coupe':
        for s in (-1,1):
            a.box((-.7,s*(W/2+.02),belt*.81),(.3,.03,.10),'black')
        a.box((-L*.42,0,belt+.18),(.19,W*.69,.05),paint)
    if kind=='fastback':
        a.box((-L*.43,0,belt+.10),(.14,W*.77,.065),'black')
    if kind=='longroof':
        # Side wood inserts and a strapped roof surfboard identify the long wagon.
        for s in (-1,1): a.box((-.45,s*(W/2+.019),belt*.73),(L*.59,.026,.18),'wood')
        _profile(a,[(-1.15,roof+.19),(-.95,roof+.24),(1.18,roof+.24),(1.32,roof+.20),(1.04,roof+.18)],.47,'cream')
        for x in (-.6,.6): a.box((x,0,roof+.249),(.055,.49,.02),'dark_metal')
    if kind=='limousine':
        for s in (-1,1):
            for x in (-1.30,-.35,.6): a.box((x,s*(W/2+.025),belt-.10),(.18,.025,.035),'silver')
            a.box((0,s*(W/2+.016),belt*.61),(L*.81,.019,.045),'silver')
        a.box((0,0,roof+.008),(1.35,W*.48,.015),'glass')
    if kind=='classic':
        a.box((L*.30,0,belt+.048),(L*.26,W*.65,.085),paint)
        for s in (-1,1): a.box((0,s*(W/2+.025),belt*.69),(L*.83,.03,.05),'silver')
        for j in range(7): a.box((L/2+.075,(j-3)*.088,belt*.64),(.025,.022,.31),'silver')
    if kind=='micro':
        a.box((-L/2-.025,0,belt*.73),(.025,W*.69,.038),'silver')
    return a

# L, width, waist, wheelbase, tyre radius, paint, body family,
# cabin rear/front, roof rear/front, roof elevation, side window sections.
AUTOS = [
 ('compact_notchback_sedan',(4.25,1.72,.94,2.51,.31,'blue','sedan',(-1.16,1.24,-.68,.60,1.45,2))),
 ('midsize_sedan',(4.83,1.84,1.00,2.82,.34,'silver','sedan',(-1.35,1.36,-.83,.63,1.51,2))),
 ('fullsize_luxury_sedan',(5.28,1.98,1.04,3.04,.35,'navy','sedan',(-1.53,1.35,-1.05,.74,1.55,3))),
 ('three_door_city_hatchback',(3.65,1.67,.96,2.36,.29,'yellow','hatch',(-1.57,1.04,-1.2,.42,1.5,1))),
 ('five_door_tall_hatchback',(4.06,1.75,1.01,2.55,.31,'teal','hatch',(-1.75,1.21,-1.36,.55,1.63,2))),
 ('two_seat_microcar',(2.64,1.48,.95,1.78,.27,'orange','micro',(-1.12,.83,-.82,.17,1.55,1))),
 ('compact_station_wagon',(4.63,1.79,.99,2.71,.33,'green','wagon',(-2.02,1.27,-1.64,.62,1.53,3))),
 ('longroof_surf_wagon',(5.24,1.92,1.06,3.04,.35,'brown','longroof',(-2.28,1.43,-1.88,.74,1.65,3))),
 ('five_door_fastback',(4.88,1.89,1.01,2.86,.34,'red','fastback',(-2.00,1.44,-.79,.69,1.49,2))),
 ('classic_muscle_coupe',(4.86,1.93,.92,2.77,.34,'orange','muscle',(-1.18,1.20,-.66,.54,1.37,1))),
 ('midengine_sports_coupe',(4.38,1.98,.79,2.64,.32,'yellow','coupe',(-1.32,1.16,-.70,.50,1.19,1))),
 ('two_seat_open_roadster',(3.93,1.72,.82,2.35,.30,'red','roadster',(-.90,1.01,-.40,.50,1.22,1))),
 ('four_seat_convertible',(4.83,1.89,.97,2.80,.33,'cream','convertible',(-1.38,1.22,-.74,.64,1.46,2))),
 ('subcompact_crossover',(4.22,1.80,1.12,2.59,.34,'teal','crossover',(-1.77,1.30,-1.31,.58,1.71,2))),
 ('sport_coupe_crossover',(4.79,1.95,1.18,2.91,.37,'navy','coupe_crossover',(-2.02,1.47,-.74,.66,1.75,2))),
 ('compact_square_suv',(4.51,1.87,1.17,2.69,.36,'green','compact_suv',(-1.93,1.33,-1.69,.77,1.80,3))),
 ('three_row_family_suv',(4.98,1.97,1.20,2.94,.37,'white','suv',(-2.21,1.45,-1.92,.80,1.83,3))),
 ('fullsize_towing_suv',(5.71,2.09,1.34,3.34,.41,'black','full_suv',(-2.58,1.59,-2.20,.99,2.00,3))),
 ('two_door_trail_suv',(3.87,1.80,1.21,2.33,.38,'sand','jeep',(-1.65,.99,-1.40,.58,1.87,1))),
 ('regular_cab_work_pickup',(5.26,1.99,1.22,3.08,.38,'white','regular_pickup',(-.47,1.42,-.30,.91,1.89,1))),
 ('extended_cab_pickup',(5.77,2.00,1.25,3.63,.39,'blue','extended_pickup',(-1.02,1.58,-.75,1.0,1.91,2))),
 ('crew_cab_shortbed_pickup',(5.79,2.07,1.30,3.59,.40,'red','crew_pickup',(-1.42,1.56,-1.15,1.00,1.98,2))),
 ('stepside_sport_pickup',(4.85,1.82,1.09,2.92,.36,'purple','stepside',(-.43,1.29,-.23,.78,1.74,1))),
 ('compact_unibody_pickup',(4.96,1.88,1.18,3.02,.35,'teal','compact_pickup',(-1.10,1.38,-.82,.77,1.78,2))),
 ('angular_electric_pickup',(5.66,2.09,1.30,3.40,.40,'silver','electric_pickup',(-1.10,1.77,-.67,.28,1.99,2))),
 ('family_minivan',(5.11,1.94,1.09,3.09,.34,'blue','minivan',(-2.25,1.67,-1.91,.91,1.84,3))),
 ('fullsize_passenger_van',(5.53,2.04,1.13,3.44,.37,'white','van',(-2.52,1.87,-2.25,1.21,2.15,4))),
 ('highroof_passenger_van',(5.92,2.10,1.29,3.61,.38,'sand','highroof',(-2.73,2.05,-2.58,1.46,2.72,4))),
 ('wheelchair_accessible_van',(5.29,1.98,1.06,3.22,.33,'silver','accessible',(-2.32,1.75,-1.98,1.02,1.97,3))),
 ('stretch_limousine',(7.70,1.98,1.03,5.43,.35,'black','limousine',(-2.51,2.19,-2.02,1.52,1.53,5))),
 ('chrome_trim_classic_sedan',(4.87,1.91,1.10,2.91,.36,'cream','classic',(-1.56,1.20,-.93,.62,1.75,2))),
 ('vintage_farm_pickup',(4.87,1.86,1.19,2.91,.37,'green','vintage_pickup',(-.48,1.19,-.24,.80,1.89,1))),
]

for _suffix,_spec in AUTOS:
    _name='b03_'+_suffix
    register(_name,CAT,'large',lambda n=_name,s=_spec:_vehicle(n,s))

# Cycles use visible structural tubing, cranksets, brake levers and wheel spokes.
def _cycle_wheel(a,x,y,z,r=.34,tire=.027,spokes=8):
    a.torus((x,y,z),r-tire,tire,'rubber',axis='y',segments=12,sides=4)
    a.torus((x,y,z),r-tire*2,.009,'silver',axis='y',segments=12,sides=4)
    a.cylinder((x,y-.075,z),(x,y+.075,z),.035,'dark_metal',sides=6)
    for j in range(spokes):
        th=j*2*math.pi/spokes
        a.cylinder((x,y,z),(x+(r-tire*2.4)*math.cos(th),y,z+(r-tire*2.4)*math.sin(th)),.006,'silver',sides=4)

def _bar(a,p,q,r=.022,mat='blue'): a.cylinder(p,q,r,mat,sides=6)

def _saddle(a,x,z,width=.19):
    _profile(a,[(x-.13,z),(x+.12,z+.018),(x+.13,z+.075),(x-.09,z+.09)],width,'black')

def _crank(a,x,z,r=.105):
    a.cylinder((x,-.035,z),(x,.035,z),r,'dark_metal',sides=10)
    for s in (-1,1):
        px=x+s*.12
        _bar(a,(x,s*.055,z),(px,s*.055,z-s*.045),.014,'silver')
        a.box((px,s*.115,z-s*.045),(.07,.12,.025),'black')

def _handle(a,x,z,width=.53,kind='flat'):
    _bar(a,(x-.10,0,z-.22),(x,0,z),.019,'silver')
    if kind=='drop':
        for s in (-1,1):
            a.tube([(x,0,z),(x,s*width/2,z),(x+.08,s*width/2,z-.1),(x+.04,s*width/2,z-.19),(x-.08,s*width/2,z-.19)],.017,'black',sides=6)
    elif kind=='cruiser':
        for s in (-1,1):
            a.tube([(x,0,z),(x+.06,s*width*.33,z),(x-.17,s*width/2,z-.04)],.02,'silver',sides=6)
            _bar(a,(x-.17,s*width/2,z-.04),(x-.27,s*width/2,z-.04),.025,'black')
    else:
        _bar(a,(x,-width/2,z),(x,width/2,z),.02,'silver')
        for s in (-1,1): _bar(a,(x,s*width*.32,z),(x,s*width*.50,z),.026,'black')
    for s in (-1,1): _bar(a,(x,s*width*.24,z-.02),(x+.05,s*width*.33,z-.08),.009,'dark_metal')

def _fenders(a,xs,r,z,width=.055):
    for x in xs:
        pts=[(x+math.cos(math.pi*j/6)*r,0,z+math.sin(math.pi*j/6)*r) for j in range(7)]
        a.tube(pts,width/2,'metal',sides=4)

def _bike(name,style):
    a=Asset(name,CAT,'person',forward_axis='+X')
    child=style=='child'; bmx=style=='bmx'; folding=style=='folding'
    r=.22 if child or folding else (.255 if bmx else .345)
    rear=-.48 if child else (-.50 if folding else -.56)
    front=.43 if child else (.52 if folding else .56)
    paint={'road':'red','mountain':'green','cruiser':'cream','stepthrough':'teal','folding':'silver','frontloader':'navy','longtail':'orange','child':'purple','bmx':'yellow','tandem':'red','recumbent':'blue','tricycle':'cream'}.get(style,'blue')
    if style=='frontloader': rear=-1.00; front=1.16
    if style=='longtail': rear=-.96
    if style=='tandem': rear=-1.10; front=.98
    if style=='recumbent': return _recumbent(a)
    if style=='tricycle': return _tricycle(a)
    tire=.043 if style in ('mountain','bmx','child') else .027
    for x in (rear,front): _cycle_wheel(a,x,0,r,r,tire)
    seat=(-.23 if style not in ('frontloader','longtail','tandem') else (-.67 if style=='frontloader' else -.28),0,r+.49)
    crank=(seat[0]+.13,0,r-.08)
    head=(front-.17,0,r+.43)
    if style=='frontloader': head=(-.02,0,r+.47)
    if child:
        seat=(-.17,0,.59);head=(.28,0,.55);crank=(-.10,0,.24)
    if folding: seat=(-.18,0,.78);head=(.31,0,.79);crank=(-.05,0,.22)
    if bmx: seat=(-.22,0,.66);head=(.38,0,.72);crank=(-.06,0,.27)
    if style=='tandem':
        seat=(-.70,0,.88);crank=(-.61,0,.28);head=(.78,0,.88)
        frontseat=(.14,0,.91); frontcrank=(.22,0,.28)
        for p,q in [(seat,frontseat),(crank,frontcrank),(frontseat,frontcrank),(frontseat,head),(frontcrank,head),(seat,frontcrank)]: _bar(a,p,q,.022,paint)
        _bar(a,frontseat,(.14,0,1.04),.016,'silver');_saddle(a,.14,1.03)
        _crank(a,.22,.28)
        _handle(a,.25,.98,.48,'flat')
    if style in ('stepthrough','cruiser'):
        a.tube([seat,(seat[0]+.16,0,r+.10),(head[0]-.17,0,r+.14),head],.026,paint,sides=6)
        if style=='cruiser': a.tube([seat,(0,0,r+.36),head],.026,paint,sides=6)
    elif folding:
        _bar(a,(rear,0,r),(head[0]-.02,0,r+.10),.040,paint)
        _bar(a,(head[0]-.02,0,r+.10),head,.029,paint)
        _bar(a,crank,seat,.027,paint)
        a.box((.06,0,r+.1),(.1,.10,.11),'dark_metal')
        a.box((.07,-.09,r+.1),(.13,.035,.027),'silver')
    else:
        for p,q in [(seat,head),(crank,head),(seat,crank)]: _bar(a,p,q,.025 if style=='mountain' else .021,paint)
    for s in (-1,1):
        axle=(rear,s*.035,r)
        for p in (seat,crank): _bar(a,axle,(p[0],s*.03,p[2]),.015,paint)
        forkhead=(front-.09,s*.042,r+.30) if style=='frontloader' else (head[0],s*.042,head[2])
        _bar(a,forkhead,(front,s*.04,r),.021,'silver' if style=='mountain' else paint)
    if style=='frontloader':
        # Extended steering link leaves an obvious front cargo tub between rider and wheel.
        a.box((.48,0,r+.12),(1.06,.61,.11),'wood')
        for s in (-1,1): a.box((.48,s*.32,r+.29),(1.06,.055,.36),'wood')
        for x in (-.05,1.00): a.box((x,0,r+.29),(.06,.61,.36),'wood')
        _bar(a,(head[0],0,head[2]),(head[0],0,r+.68),.021,'silver')
        _bar(a,(-.1,-.18,r-.05),(front-.1,-.18,r-.05),.015,'silver')
        for s in (-1,1): _bar(a,(crank[0],s*.13,r-.03),(front-.09,s*.13,r-.03),.025,paint)
    if style=='mountain':
        _bar(a,(front-.12,-.055,r+.24),(front,-.055,r),.033,'dark_metal')
        _bar(a,(front-.12,.055,r+.24),(front,.055,r),.033,'dark_metal')
        _bar(a,(-.05,0,r+.30),(.17,0,r+.18),.055,'silver')
        a.torus((front,-.081,r),.11,.009,'silver',axis='y',segments=10,sides=4)
    _bar(a,seat,(seat[0],0,seat[2]+.13),.016,'silver');_saddle(a,seat[0],seat[2]+.10)
    _crank(a,crank[0],crank[2],.075 if child else .10)
    # An open chain loop makes the drivetrain legible from the side.
    chain=[(rear,-.065,r+.055),(crank[0],-.065,crank[2]+.095),(crank[0]+.10,-.065,crank[2]),(crank[0],-.065,crank[2]-.095),(rear,-.065,r-.055),(rear-.055,-.065,r),(rear,-.065,r+.055)]
    a.tube(chain,.007,'dark_metal',sides=4)
    hkind='drop' if style=='road' else ('cruiser' if style in ('cruiser','stepthrough') else 'flat')
    hz=head[2]+(.25 if style in ('cruiser','stepthrough','folding','frontloader') else .09)
    _handle(a,head[0]+.10,hz,.42 if child else .57,hkind)
    if style in ('cruiser','stepthrough','longtail','folding'):
        _fenders(a,(rear,front),r+.037,r)
    if style in ('stepthrough','longtail'):
        rx=rear+.10; length=.72 if style=='longtail' else .4
        a.box((rx,0,r+.39),(length,.31,.04),'dark_metal')
        for s in (-1,1):
            _bar(a,(rear,s*.04,r),(rx,s*.15,r+.39),.014,'silver')
            a.box((rx,s*.26,r+.22),(length*.76,.22,.34),'brown' if style=='stepthrough' else 'blue')
        if style=='longtail':
            a.box((rear+.06,0,r+.44),(.60,.26,.09),'black')
            for s in (-1,1): a.tube([(rear-.22,s*.19,r+.41),(rear-.22,s*.19,r+.70),(rear+.32,s*.19,r+.70),(rear+.32,s*.19,r+.41)],.019,'dark_metal',sides=6)
    if style=='child':
        # A pair of training wheels is geometrically distinct from the BMX.
        for s in (-1,1):
            _bar(a,(rear,0,r),(rear-.05,s*.21,.095),.015,'silver')
            _cycle_wheel(a,rear-.05,s*.23,.09,.09,.018,4)
        a.box((head[0]+.05,0,hz-.17),(.14,.21,.13),'pink')
    if style=='bmx':
        for x in (rear,front): _bar(a,(x,-.13,r),(x,.13,r),.023,'silver')
        _bar(a,(head[0]+.1,-.19,hz-.09),(head[0]+.1,.19,hz-.09),.014,paint)
    if style=='cruiser':
        a.cylinder((head[0]+.13,0,hz-.17),(head[0]+.22,0,hz-.17),.055,'light',sides=8)
    # Ground-reaching kickstand, so every model also works as a parked prop.
    _bar(a,(crank[0]-.08,.04,crank[2]),(crank[0]-.22,.20,.02),.013,'dark_metal')
    return a

def _recumbent(a):
    r=.27
    _cycle_wheel(a,-.90,0,r,r,.031)
    for s in (-1,1): _cycle_wheel(a,.45,s*.44,.22,.22,.026)
    _bar(a,(-.9,0,r),(.95,0,.27),.041,'blue')
    _bar(a,(.45,-.44,.22),(.45,.44,.22),.032,'blue')
    _profile(a,[(-.55,.37),(-.10,.34),(.03,.43),(-.15,.51),(-.50,.84),(-.64,.81)],.37,'black')
    _crank(a,.91,.33,.095)
    for s in (-1,1):
        _bar(a,(-.1,s*.23,.32),(.04,s*.28,.57),.02,'silver')
        _bar(a,(.04,s*.28,.57),(.15,s*.28,.63),.025,'black')
    _bar(a,(-.54,0,.67),(-.68,0,1.34),.008,'silver')
    a.mesh([(-.68,0,1.34),(-.39,0,1.27),(-.68,0,1.17)],[(0,1,2)],'orange')
    return a

def _tricycle(a):
    r=.32
    for s in (-1,1): _cycle_wheel(a,-.61,s*.39,r,r,.036)
    _cycle_wheel(a,.62,0,r,r,.035)
    _bar(a,(-.61,-.4,r),(-.61,.4,r),.028,'silver')
    for p,q in [((-.61,0,r),(-.08,0,.28)),((-.08,0,.28),(.42,0,.82)),((-.08,0,.28),(-.23,0,.84)),((-.23,0,.84),(.42,0,.82))]: _bar(a,p,q,.027,'cream')
    for s in (-1,1): _bar(a,(.42,s*.04,.82),(.62,s*.04,r),.021,'cream')
    _bar(a,(-.23,0,.84),(-.23,0,.95),.017,'silver');_saddle(a,-.23,.94,.25)
    _crank(a,-.08,.28);_handle(a,.53,1.1,.65,'cruiser')
    a.box((-.62,0,.64),(.51,.63,.045),'wood')
    for s in (-1,1):
        for z in (.73,.87): a.box((-.62,s*.33,z),(.55,.035,.075),'wood')
    for x in (-.89,-.35):
        for z in (.73,.87): a.box((x,0,z),(.035,.63,.075),'wood')
    return a

def _scooter(name,electric=False):
    a=Asset(name,CAT,'person',forward_axis='+X')
    r=.13 if electric else .095
    for x in (-.43,.45): _cycle_wheel(a,x,0,r,r,.033 if electric else .023,4)
    a.box((-.03,0,r+.015),(.82,.17,.07),'dark_metal' if electric else 'silver')
    a.box((-.07,0,r+.053),(.55,.14,.009),'black')
    _bar(a,(.43,0,r),(.26,0,1.12 if electric else 1.00),.032 if electric else .021,'dark_metal' if electric else 'silver')
    _bar(a,(.40,-.06,r),(.40,.06,r),.025,'silver')
    _handle(a,.29,1.18 if electric else 1.06,.47,'flat')
    _bar(a,(-.12,0,r),(-.20,.12,.02),.011,'dark_metal')
    if electric:
        a.box((.29,0,1.16),(.09,.08,.025),'black')
        a.box((.31,0,.92),(.055,.07,.09),'light')
        a.box((-.44,0,r+.11),(.09,.12,.035),'red')
        a.box((.40,0,.29),(.085,.075,.12),'orange')
    else:
        a.tube([(-.32,0,r+.06),(-.43,0,r+.10),(-.52,0,r+.065)],.04,'silver',sides=4)
    return a

def _moto(name,kind):
    a=Asset(name,CAT,'person',forward_axis='+X')
    scooter=kind=='moped';dirt=kind=='dirt';tour=kind=='touring';sport=kind=='sport'
    r=.23 if scooter else (.34 if dirt else .30)
    rear=-.64 if scooter else -.77; front=.65 if scooter else .78
    paint='teal' if scooter else ('red' if sport else ('navy' if tour else 'orange'))
    for x in (rear,front):
        a.torus((x,0,r),r*.76,r*.24,'rubber',axis='y',segments=12,sides=5)
        a.cylinder((x,-.066,r),(x,.066,r),r*.60,'dark_metal',sides=10)
        for sy in (-1,1):
            a.torus((x,sy*.072,r),r*.52,.016,'silver',axis='y',segments=10,sides=4)
            for j in range(5):
                th=j*2*math.pi/5
                _bar(a,(x,sy*.076,r),(x+math.cos(th)*r*.52,sy*.076,r+math.sin(th)*r*.52),.016,'silver')
    for sy in (-1,1):
        _bar(a,(rear,sy*.08,r),(-.20,sy*.095,.43),.035,'dark_metal')
        _bar(a,(front,sy*.072,r),(.44,sy*.095,.93 if not dirt else 1.10),.035,'silver')
        if dirt:
            _bar(a,(front,sy*.075,r),(.61,sy*.084,.68),.049,'orange')
    if scooter:
        _profile(a,[(-.79,.36),(-.71,.70),(-.32,.79),(-.14,.58),(.22,.32),(.39,.33),(.33,.71),(.43,.92),(.57,.91),(.65,.52),(.50,.27),(-.30,.27)],.40,paint)
        a.box((-.36,0,.78),(.64,.37,.13),'black')
        a.box((.13,0,.36),(.39,.35,.05),'black')
        _handle(a,.49,1.03,.60,'cruiser')
        a.cylinder((.5,0,.98),(.62,0,.98),.10,'light',sides=10)
        _profile(a,[(.58,.49),(.71,.52),(.87,.42),(.81,.38),(.66,.44)],.20,paint)
    else:
        # Open triangulated frame, finned engine and separate petrol tank.
        for sy in (-1,1):
            for p,q in [((-.47,sy*.11,.62),(.44,sy*.11,.89)),((-.47,sy*.11,.62),(-.13,sy*.11,.33)),((-.13,sy*.11,.33),(.44,sy*.11,.89))]: _bar(a,p,q,.031,'dark_metal')
        for z in (.39,.45,.51,.57): a.box((-.04,0,z),(.40,.38,.036),'silver')
        a.cylinder((-.08,-.22,.46),(-.08,.22,.46),.145,'dark_metal',sides=8)
        a.sphere((.10,0,.82 if not dirt else .91),(.34,.22,.19),paint,segments=8,rings=4)
        a.cylinder((.10,0,1.003 if not dirt else 1.093),(.10,0,1.013 if not dirt else 1.103),.045,'silver',sides=8)
        a.box((-.42,0,.83 if not dirt else .99),(.61,.32,.12),'black',rot=(0,.06,0))
        _profile(a,[(-.90,.69),(-.80,.84),(-.30,.86),(-.24,.77)],.32,paint)
        # Swept exhaust and individual foot pegs.
        a.tube([(.08,.20,.47),(.19,.22,.30),(-.19,.25,.24),(-.66,.26,.34)],.04,'silver',sides=6)
        a.cylinder((-.37,.26,.32),(-.79,.26,.40),.075,'silver',sides=8)
        for sy in (-1,1): _bar(a,(-.17,sy*.10,.4),(-.17,sy*.27,.4),.027,'black')
        _handle(a,.49,1.12 if not dirt else 1.25,.64,'flat')
        a.cylinder((.52,0,.93),(.64,0,.93),.115,'light',sides=10)
        _profile(a,[(.49,.58),(.65,.64),(.86,.59),(.96,.49),(.85,.47),(.69,.56)],.21,paint)
    for sy in (-1,1):
        _bar(a,(.49,sy*.24,1.04 if scooter else 1.13),(.42,sy*.40,1.25 if scooter else 1.34),.012,'silver')
        a.box((.42,sy*.41,1.25 if scooter else 1.34),(.11,.09,.04),'dark_metal')
        a.box((rear-.1,sy*.15,.64 if scooter else .75),(.09,.07,.05),'orange')
    a.box((rear-.20,0,.66 if scooter else .76),(.065,.17,.065),'red')
    a.box((rear-.22,0,.52 if scooter else .60),(.025,.18,.13),'white')
    _bar(a,(-.22,0,.33),(-.40,.28,.015),.018,'dark_metal')
    if sport:
        _profile(a,[(.11,.37),(.54,.45),(.67,.87),(.36,1.04),(-.04,.94),(-.22,.57)],.45,paint)
        for sy in (-1,1):
            _quad(a,[(.23,sy*.231,.54),(.49,sy*.231,.62),(.51,sy*.231,.78),(.25,sy*.231,.70)],'black')
        _profile(a,[(.61,.95),(.62,.96),(.35,1.19),(.34,1.18)],.34,'glass')
        a.box((-.61,0,.93),(.32,.27,.11),paint)
    if tour:
        _profile(a,[(.65,.97),(.67,.975),(.36,1.45),(.34,1.445)],.61,'glass')
        for sy in (-1,1):
            a.box((-.65,sy*.31,.60),(.62,.27,.38),paint)
            a.box((-.65,sy*.31,.81),(.65,.28,.055),'black')
        a.box((-.83,0,1.02),(.42,.56,.28),paint)
        a.box((-.81,0,1.18),(.44,.58,.065),'black')
        a.box((-.67,0,.98),(.10,.30,.22),'black')
    if dirt:
        # High clearance narrow guards, long fork and number plate.
        _profile(a,[(.37,.97),(.56,1.01),(1.03,.89),(.97,.84),(.59,.91)],.17,paint)
        a.box((.53,0,1.11),(.07,.28,.28),'white',rot=(0,-.13,0))
        for sy in (-1,1): a.box((-.30,sy*.19,.77),(.33,.025,.22),'white')
        _bar(a,(-.57,0,.84),(-.18,0,.45),.055,'silver')
    return a

CYCLES=[
 ('drop_bar_road_bicycle','road'),('suspension_mountain_bicycle','mountain'),
 ('swept_bar_beach_cruiser','cruiser'),('stepthrough_city_bicycle','stepthrough'),
 ('small_wheel_folding_bicycle','folding'),('front_box_cargo_bicycle','frontloader'),
 ('longtail_family_cargo_bicycle','longtail'),('child_training_wheel_bicycle','child'),
 ('stunt_bmx_bicycle','bmx'),('two_rider_tandem_bicycle','tandem'),
 ('recumbent_tadpole_tricycle','recumbent'),('rear_basket_adult_tricycle','tricycle')]
for _suffix,_style in CYCLES:
    _name='b03_'+_suffix
    register(_name,CAT,'person',lambda n=_name,s=_style:_bike(n,s))
for _suffix,_electric in [('folding_kick_scooter',False),('battery_kick_scooter',True)]:
    _name='b03_'+_suffix
    register(_name,CAT,'person',lambda n=_name,e=_electric:_scooter(n,e))
for _suffix,_kind in [('stepthrough_motor_scooter','moped'),('faired_sport_motorcycle','sport'),('luggage_touring_motorcycle','touring'),('long_fork_dirt_motorcycle','dirt')]:
    _name='b03_'+_suffix
    register(_name,CAT,'person',lambda n=_name,k=_kind:_moto(n,k))
