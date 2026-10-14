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

def _mix(p,q,t): return tuple(v+(w-v)*t for v,w in zip(p,q))

def _ring(a,rings,mat,cap=False):
    n=len(rings[0]); vs=[p for ring in rings for p in ring]
    fs=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i)
        for j in range(len(rings)-1) for i in range(n)]
    if cap: fs += [tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))]
    a.mesh(vs,fs,mat)

def _chamfer(a,center,size,mat,cut=.10):
    # Deliberate broad corner planes, not a modifier on a rectangular primitive.
    x,y,z=center; lx,ly,lz=(v/2 for v in size); d=min(lx,ly,lz)*cut
    profile=[(-ly+d,-lz),(ly-d,-lz),(ly,-lz+d),(ly,lz-d),
             (ly-d,lz),(-ly+d,lz),(-ly,lz-d),(-ly,-lz+d)]
    rings=[]
    for xx,shrink in ((-lx,0),(lx,0)):
        rings.append([(x+xx,y+yy*(1-shrink/max(ly,1e-5)),z+zz*(1-shrink/max(lz,1e-5))) for yy,zz in profile])
    _ring(a,rings,mat,True)

def _auto_wheel(a,x,y,r=.34,width=.22,style='alloy'):
    side=1 if y>0 else -1; seg=16
    # Tyre carcass: rounded shoulders, wide flat tread and recessed bead.
    tire=[(-.50,.65),(-.52,.84),(-.38,.98),(.38,.98),(.52,.84),(.50,.65)]
    rings=[[(x+r*rr*math.cos(i*2*math.pi/seg),y+width*yy,r+r*rr*math.sin(i*2*math.pi/seg)) for i in range(seg)] for yy,rr in tire]
    _ring(a,rings,'rubber')
    yy=y+side*width*.47
    # Dish and rim barrel leave the spoke openings visibly hollow.
    rim=[(.0,.67),(.022,.69),(.032,.61),(-.025,.56)]
    rings=[[(x+r*rr*math.cos(i*2*math.pi/seg),yy+side*d,r+r*rr*math.sin(i*2*math.pi/seg)) for i in range(seg)] for d,rr in rim]
    _ring(a,rings,'silver')
    a.cylinder((x,y-side*width*.12,r),(x,y+side*width*.21,r),r*.49,'dark_metal',sides=16)
    a.cylinder((x,yy,r),(x,yy+side*.038,r),r*.18,'silver',sides=10)
    if style=='classic':
        a.cylinder((x,yy-side*.005,r),(x,yy+side*.015,r),r*.43,'silver',sides=16)
        # Narrow whitewall only, so period cars retain normal tyre proportions.
        rings=[[(x+r*rr*math.cos(i*2*math.pi/seg),yy+side*.004,r+r*rr*math.sin(i*2*math.pi/seg)) for i in range(seg)] for rr in (.72,.82)]
        _ring(a,rings,'cream')
    else:
        for i in range(5):
            th=2*math.pi*i/5
            pts=[]
            for yy2,rad,ang in ((yy,.17,th-.23),(yy,.60,th-.07),(yy,.60,th+.07),(yy,.17,th+.23)):
                pts.append((x+math.cos(ang)*r*rad,yy2,r+math.sin(ang)*r*rad))
            back=[(px,py-side*.036,pz) for px,py,pz in pts]
            _ring(a,[back,pts],'silver',True)
    a.box((x+r*.30,y+side*width*.27,r+.02),(.075,.045,r*.55),'metal')

def _body_z(x,L,belt,wb,kind):
    end=max(0,(abs(x)-L*.33)/(L*.17))
    z=belt-.075*min(1,end)**1.5
    if kind in ('muscle','classic','vintage_pickup','stepside'):
        z+=.028*math.exp(-((x+wb/2)/.55)**2)
    if kind in ('coupe','roadster','fastback','coupe_crossover'):
        z-=.055*max(0,x/(L/2))**2
        z+=.025*math.exp(-((x+wb/2)/.50)**2)
    return z

def _body_width(x,L,W,wb,kind):
    end=max(0,(abs(x)-L*.34)/(L*.16))
    taper=.10 if kind in ('coupe','roadster','hatch','micro') else .065
    shoulder=1-taper*min(1,end)**1.4
    if kind in ('muscle','coupe','roadster','stepside'):
        shoulder-=(.047 if kind=='muscle' else .031)*(1-max(math.exp(-((x-wb/2)/.48)**2),math.exp(-((x+wb/2)/.48)**2)))
    return W*.5*shoulder

def _body(a,L,W,belt,wb,r,paint,style='alloy',kind='sedan',cab=None):
    floor=r*.76; ar=r+.065
    stations={-L/2,L/2,-L/2+.13,L/2-.13,-L*.38,L*.38,0}
    stations.update(-L/2+L*j/12 for j in range(1,12))
    for xx in (-wb/2,wb/2):
        stations.update(xx+ar*math.cos(j*math.pi/12) for j in range(13))
    pickup=('pickup' in kind or kind=='stepside')
    opened=kind in ('roadster','convertible')
    if cab:
        xr,xf,rr,rf,roof,panes=cab
        stations.update((xr,xf))
    xs=sorted(set(round(x,7) for x in stations if -L/2<=x<=L/2))
    rings=[]
    # Six deliberate planes per shoulder form crown, hood edge, belt crease,
    # convex door skin and inward-tucked rocker; the wheel cutout sets the floor.
    for x in xs:
        z=_body_z(x,L,belt,wb,kind); w=_body_width(x,L,W,wb,kind)
        low=floor
        for xx in (-wb/2,wb/2):
            d=abs(x-xx)
            if d<=ar+1e-8: low=max(low,r+math.sqrt(max(0,ar*ar-d*d)))
        shoulder=max(z-.12,low+.018)
        top=[(0,z+.026),(.56*w,z+.020),(.82*w,z-.006),(.96*w,z-.061),
             (w,shoulder),(.992*w,low+(shoulder-low)*.40),(.947*w,low)]
        # top-to-rocker on left and right; center roof deck remains a crown.
        section=[(x,-yy,zz) for yy,zz in reversed(top[1:])]+[(x,yy,zz) for yy,zz in top]
        rings.append(section)
    vs=[q for ring in rings for q in ring]; n=len(rings[0]);fs=[]
    for j in range(len(rings)-1):
        mid=(xs[j]+xs[j+1])/2
        hollow=(pickup and mid<cab[0]-.02) or (opened and cab[0]<mid<cab[1])
        for k in range(n-1):
            if hollow and 3<=k<=8: continue
            fs.append((j*n+k,j*n+k+1,(j+1)*n+k+1,(j+1)*n+k))
    fs += [tuple(reversed(range(n))),tuple((len(rings)-1)*n+k for k in range(n))]
    a.mesh(vs,fs,paint)
    a.box((0,0,r*.73),(wb,W*.70,.13),'dark_metal')
    for xx in (-wb/2,wb/2):
        for sy in (-1,1):
            _auto_wheel(a,xx,sy*W*.464,r,width=r*.65,style=style)
            # A true rolled arch rim has an outer painted return and a dark
            # recessed inner liner. Neither surface fills the wheel opening.
            arches=[]
            for radius,depth in ((ar+.022,.002),(ar,.007),(ar,-.048)):
                row=[]
                for j in range(13):
                    th=math.pi-j*math.pi/12; x=xx+radius*math.cos(th)
                    y=sy*(_body_width(x,L,W,wb,kind)+depth)
                    row.append((x,y,r+radius*math.sin(th)))
                arches.append(row)
            for k,mat in ((0,paint),(1,'dark_metal')):
                av=arches[k]+arches[k+1]
                a.mesh(av,[(j,j+1,j+14,j+13) for j in range(12)],mat)
    # Rocker strips and underbody crossmembers read as construction at low view.
    for sy in (-1,1):
        a.beam((-wb/2+ar,sy*W*.465,floor+.018),(wb/2-ar,sy*W*.465,floor+.018),.065,.055,paint)
    a.metadata['body_construction']='sculpted section shell, open wheel arches and recessed glazing'

def _framed_panel(a,outer,inner,paint,normal=(0,0,0),seal=True):
    # Frame surrounds an actual hole; glass is sunk behind the seal lip.
    n=len(outer); a.mesh(outer+inner,[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],paint)
    center=tuple(sum(q[i] for q in inner)/n for i in range(3))
    inset=[tuple(v+(c-v)*.027 for v,c in zip(q,center)) for q in inner]
    a.mesh(inner+inset,[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],'black' if seal else paint)
    glass=[tuple(v+d for v,d in zip(q,normal)) for q in inset]
    a.mesh(inset+glass,[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],'black')
    a.mesh(glass,[tuple(range(n))],'glass')

def _cabin(a,xr,xf,rr,rf,zbase,zroof,W,paint,panes=2,backglass=True,kind='sedan'):
    wb=W*.956; wr=W*.795; height=zroof-zbase
    eave=zroof-.037
    def sidept(u,t,sign):
        rear=xr+(rr-xr)*t; front=xf+(rf-xf)*t
        return (rear+(front-rear)*u,sign*(wb+(wr-wb)*t)/2,zbase+(eave-zbase)*t)
    breaks=[j/panes for j in range(panes+1)]
    if panes==1 and kind in ('muscle','coupe','hatch','micro'):breaks=[0,.28,1]
    for sign in (-1,1):
        for j in range(len(breaks)-1):
            lo=breaks[j];hi=breaks[j+1]
            du=.033/max(xf-xr,.1);dt=min(.20,.07/max(height,.1))
            left=(.15 if j==0 else .033)/max(xf-xr,.1)
            right=(.09 if j==len(breaks)-2 else .033)/max(xf-xr,.1)
            outer=[sidept(lo,0,sign),sidept(hi,0,sign),sidept(hi,1,sign),sidept(lo,1,sign)]
            inner=[sidept(lo+left,dt,sign),sidept(hi-right,dt,sign),sidept(hi-right,1-dt,sign),sidept(lo+left,1-dt,sign)]
            _framed_panel(a,outer,inner,paint,(0,-sign*.010,0))
    # A folded sill return joins the cabin to the curved body shoulder.
    for sign in (-1,1):
        a.mesh([(xr,sign*wb/2,zbase),(xf,sign*wb/2,zbase),
                (xf,sign*W*.458,zbase-.10),(xr,sign*W*.458,zbase-.10)],[(0,1,2,3)],paint)
    for x in (xr,xf):
        a.mesh([(x,-wb/2,zbase),(x,wb/2,zbase),(x,W*.458,zbase-.10),(x,-W*.458,zbase-.10)],[(0,1,2,3)],paint)
    # Crown and rounded roof shoulders are baked geometry, with chamfered ends.
    rows=[]
    for u in (0,.06,.35,.65,.94,1):
        x=rr+(rf-rr)*u
        rows.append([(x,q*wr/2,zroof-.037*abs(q)**2)
                     for q in (-1,-.86,-.53,0,.53,.86,1)])
    vs=[p for row in rows for p in row]
    a.mesh(vs,[(j*7+i,j*7+i+1,(j+1)*7+i+1,(j+1)*7+i) for j in range(5) for i in range(6)],paint)
    def endglass(xbot,xtop,direction):
        # Windshield divided across its shallow lateral bow; glass recess is
        # bounded by a continuous painted A/C-pillar and rubber gasket.
        def pt(u,t):
            width=(wb+(wr-wb)*t)/2
            return (xbot+(xtop-xbot)*t+direction*.025*(1-u*u)*(1-t),u*width,zbase+(eave-zbase)*t+.037*(1-u*u)*t)
        us=(-1,-.60,0,.60,1)
        for j in range(4):
            u0,u1=us[j],us[j+1]
            outside=[pt(u0,0),pt(u1,0),pt(u1,1),pt(u0,1)]
            il=u0+(.055 if j==0 else 0);ir=u1-(.055 if j==3 else 0)
            inner=[pt(il,.13),pt(ir,.13),pt(ir,.88),pt(il,.88)]
            # Only the perimeter receives a gasket, avoiding false window bars.
            v=outside+inner
            fs=[(0,1,5,4),(2,3,7,6)]
            if j==0:fs.append((3,0,4,7))
            if j==3:fs.append((1,2,6,5))
            a.mesh(v,fs,paint)
            lowered=[(x-direction*.006,y,z) for x,y,z in inner]
            a.mesh(lowered,[(0,1,2,3)],'glass')
        for sign in (-1,1):
            pts=[pt(sign*.938,t) for t in (.12,.89)]
            a.beam(*pts,.018,.013,'black')
        for t in (.12,.89):
            pts=[pt(u,t) for u in (-.945,-.6,0,.6,.945)]
            for p,q in zip(pts,pts[1:]):a.beam(p,q,.015,.013,'black')
    endglass(xf,rf,1)
    if backglass:endglass(xr,rr,-1)
    else:
        a.mesh([sidept(0,0,-1),sidept(0,0,1),sidept(0,1,1),sidept(0,1,-1)],[(0,1,2,3)],paint)
    for sign in (-1,1):
        # Side rain gutter, plus two parked windshield wipers.
        a.beam((rr,sign*wr*.501,eave),(rf,sign*wr*.501,eave),.020,.014,paint)
        a.beam((xf-.055,sign*W*.30,zbase+.065),(xf-.14,sign*W*.11,zbase+.12),.018,.012,'black')

def _fascia(a,L,W,belt,paint,kind,round_lights):
    front=L/2; rear=-L/2
    # Faceted wrap-around fascia follows the nose's narrowed plan view.
    for direction in (-1,1):
        x=front if direction==1 else rear
        _chamfer(a,(x-direction*.015,0,belt*.435),(.16,W*.91,.19),paint,.46)
        _chamfer(a,(x+direction*.045,0,belt*.365),(.10,W*.84,.07),'dark_metal',.28)
        _chamfer(a,(x+direction*.073,0,belt*.495),(.025,.36,.145),'black',.14)
        a.box((x+direction*.090,0,belt*.495),(.009,.30,.11),'white')
    # Grille pocket surrounded by a painted lip, then a dark backplane.
    grille_z=belt*.705;grille_w=W*(.67 if round_lights else .44)
    if kind in ('muscle','classic'):grille_w=W*.84;grille_z=belt*.73
    _chamfer(a,(front+.026,0,grille_z),(.074,grille_w+.052,.222),'dark_metal',.34)
    _chamfer(a,(front+.067,0,grille_z),(.012,grille_w,.165),'black',.36)
    for j in range(3):
        a.box((front+.079,0,grille_z-.061+j*.059),(.009,grille_w*.95,.013),'metal')
    for sign in (-1,1):
        if round_lights or kind=='muscle':
            count=2 if kind=='muscle' else 1
            for k in range(count):
                y=sign*(W*.342+(.104 if k else -.075)) if count==2 else sign*W*.34
                radius=.096 if count==2 else .12
                a.cylinder((front+.075,y,belt*.748),(front+.095,y,belt*.748),radius,'silver',sides=16)
                a.cylinder((front+.096,y,belt*.748),(front+.104,y,belt*.748),radius*.81,'light',sides=16)
        else:
            # Lens bevel, recessed dark housing and separate amber end marker.
            y=sign*W*.344
            _chamfer(a,(front+.035,y,belt*.786),(.085,W*.245,.15),'dark_metal',.6)
            _chamfer(a,(front+.081,y,belt*.789),(.023,W*.218,.117),'light',.6)
            a.box((front+.096,sign*W*.431,belt*.781),(.012,.044,.086),'orange')
        _chamfer(a,(rear-.055,sign*W*.347,belt*.755),(.070,W*.245,.15),'dark_metal',.5)
        _chamfer(a,(rear-.093,sign*W*.347,belt*.761),(.012,W*.223,.108),'red',.5)
        a.box((rear-.102,sign*W*.300,belt*.751),(.012,W*.05,.046),'white')
        # Lower corner intakes and a small reverse/fog lamp complete the bumper.
        _chamfer(a,(front+.078,sign*W*.343,belt*.493),(.025,W*.18,.095),'black',.45)
        a.cylinder((front+.09,sign*W*.35,belt*.49),(front+.105,sign*W*.35,belt*.49),.026,'light',sides=8)
        a.cylinder((rear+.08,sign*W*.29,.26),(rear-.12,sign*W*.29,.26),.038,'dark_metal',sides=10)
        a.cylinder((rear-.121,sign*W*.29,.26),(rear-.125,sign*W*.29,.26),.027,'black',sides=10)

def _details(a,L,W,belt,paint,doors=4,round_lights=False,offroad=False,kind='sedan',wb=None,cab=None):
    _fascia(a,L,W,belt,paint,kind,round_lights)
    xr,xf,rr,rf,roof,panes=cab
    for sign in (-1,1):
        mirrorx=xf-.17
        a.beam((mirrorx,sign*W*.455,belt+.12),(mirrorx-.035,sign*W*.54,belt+.17),.045,.040,'dark_metal')
        _chamfer(a,(mirrorx-.045,sign*W*.558,belt+.18),(.24,.19,.135),paint,.75)
        a.box((mirrorx-.167,sign*W*.559,belt+.185),(.012,.14,.082),'glass')
        # Door perimeter lines follow the shaped outer skin and stop above sills.
        edges=[xr+.14,xf-.21]
        if doors>=4:edges.insert(1,(xr+xf)*.5)
        for xx in edges:
            y=sign*(_body_width(xx,L,W,wb,kind)+.004)
            a.beam((xx,y,belt-.12),(xx+.018,y,belt*.52),.009,.006,'dark_metal')
        for j in range(len(edges)-1):
            x=(edges[j]+edges[j+1])/2-.16;y=sign*(_body_width(x,L,W,wb,kind)+.008)
            _chamfer(a,(x,y,belt-.148),(.20,.022,.048),'dark_metal',.3)
            a.box((x+.012,y+sign*.013,belt-.145),(.142,.013,.019),'silver')
        # Thin sill highlight, lower doors subtly inset from the wheel shoulders.
        a.beam((xr+.15,sign*W*.472,belt*.47),(xf-.22,sign*W*.472,belt*.47),.019,.018,paint)
        a.box((L/2-.19,sign*W*.472,belt*.57),(.12,.018,.04),'orange')
    # Hood shut lines, physically raised a few millimetres from crowned skin.
    for sign in (-1,1):
        pts=[]
        for j in range(5):
            x=xf+.06+(L/2-.23-xf-.06)*j/4
            pts.append((x,sign*W*.33,_body_z(x,L,belt,wb,kind)+.019))
        for p,q in zip(pts,pts[1:]):a.beam(p,q,.008,.006,'dark_metal')
    if offroad:
        for sign in (-1,1):_chamfer(a,(0,sign*(W/2+.055),.40),(L*.54,.18,.12),'black',.45)
        a.beam((L/2+.17,-W*.41,.48),(L/2+.17,W*.41,.48),.075,mat='dark_metal')
        for y in (-W*.31,W*.31):a.beam((L/2+.17,y,.47),(L/2+.17,y,.89),.055,mat='dark_metal')

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

def _pickup_bed(a,L,W,belt,cabrear,paint,stepside=False,wb=3,r=.38):
    back=-L/2+.10; front=cabrear-.07; floor=belt-.39
    a.box(((back+front)/2,0,floor),(front-back,W*.84,.07),'dark_metal')
    for sy in (-1,1):
        # Full-depth inner bed skin, thin return rail, and raised wheel tub.
        a.box(((back+front)/2,sy*W*.448,belt-.15),(front-back,.11,.43),paint)
        _chamfer(a,((back+front)/2,sy*W*.448,belt+.072),(front-back,.135,.05),'black',.6)
        _chamfer(a,(-wb/2,sy*W*.34,floor+.075),(r*2.5,W*.22,.17),paint,.6)
    a.box((back,0,belt-.14),(.11,W*.84,.43),paint)
    a.box((front,0,belt-.13),(.06,W*.84,.42),paint)
    a.box((back-.059,0,belt-.016),(.018,.31,.067),'black')
    for j in range(7):
        a.box(((back+front)/2,(j-3)*W*.095,floor+.042),(front-back-.12,.018,.014),'metal')
    for sy in (-1,1):
        a.box((back-.058,sy*W*.29,belt-.29),(.019,.11,.029),'silver')
    if stepside:
        for sy in (-1,1):
            _chamfer(a,(cabrear-.23,sy*W*.54,.41),(.35,.22,.10),'dark_metal',.4)
            _chamfer(a,(-wb/2,sy*W*.505,r*2+.08),(r*2.7,.22,.12),paint,.6)

def _vehicle(name,spec):
    L,W,belt,wb,r,paint,kind,cab=spec
    a=Asset(name,CAT,'large',style='faceted city fleet',forward_axis='+X')
    old=kind in ('classic','stepside','vintage_pickup')
    _body(a,L,W,belt,wb,r,paint,'classic' if old else 'alloy',kind,cab)
    xr,xf,rr,rf,roof,panes=cab
    isopen=kind in ('roadster','convertible')
    if isopen:
        a.box(((xr+xf)/2,0,belt-.22),(xf-xr,W*.79,.075),'black')
        _seats(a, .02 if kind=='roadster' else .3,W,belt-.15)
        if kind=='convertible': _seats(a,-.68,W,belt-.15)
        _cabin(a,xf-.10,xf,rf-.10,rf,belt,roof,W,paint,1,False)
        # A-frame windshield retains an open, roofless passenger compartment.
        for s in (-1,1): a.beam((xf,s*W*.475,belt),(rf,s*W*.395,roof),.055,mat=paint)
        a.beam((rf,-W*.4,roof),(rf,W*.4,roof),.055,mat=paint)
        a.box((xr-.06,0,belt+.07),(.24,W*.76,.15),'black')
        a.torus((.54,-W*.24,belt+.38),.13,.018,'black',axis='x',segments=10,sides=4)
        if kind=='roadster':
            for s in (-1,1): a.tube([(-.46,s*W*.22,belt+.26),(-.46,s*W*.22,belt+.54),(-.68,s*W*.22,belt+.54),(-.68,s*W*.22,belt+.26)],.037,'silver',sides=6)
    else:
        _cabin(a,xr,xf,rr,rf,belt,roof,W,paint,panes,kind=kind)
    doors=2 if kind in ('coupe','muscle','roadster','convertible','micro','jeep','regular_pickup','stepside','vintage_pickup') else 4
    _details(a,L,W,belt,paint,doors,round_lights=old or kind in ('jeep','micro'),offroad=kind in ('jeep','offroad','full_suv'),kind=kind,wb=wb,cab=cab)
    if 'pickup' in kind or kind=='stepside':
        _pickup_bed(a,L,W,belt,xr,paint,kind=='stepside',wb,r)
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
        scoop_rear=xf+.10;scoop_front=L/2-.38
        _profile(a,[(scoop_rear,belt+.035),(scoop_rear+.09,belt+.145),
                    (scoop_front-.07,belt+.125),(scoop_front,belt+.025)],W*.23,paint)
        a.box((scoop_front-.025,0,belt+.074),(.018,W*.195,.063),'black')
        # Conforming hood stripes stop at the cowl and remain above its crown.
        for sy in (-1,1):
            vs=[]
            for j in range(13):
                x=xf+.075+(L/2-.12-xf-.075)*j/12
                for y in (sy*.30-.055,sy*.30+.055):
                    vs.append((x,y,_body_z(x,L,belt,wb,kind)+.032))
            a.mesh(vs,[(j*2,j*2+1,j*2+3,j*2+2) for j in range(12)],'cream')
        _profile(a,[(-L*.445,belt+.19),(-L*.405,belt+.215),(-L*.37,belt+.19),(-L*.405,belt+.175)],W*.77,'black')
        for y in (-W*.28,W*.28):a.box((-L*.405,y,belt+.09),(.055,.055,.18),'black')
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
