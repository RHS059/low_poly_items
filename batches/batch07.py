"""Fifty construction machines and worksite assemblies, authored in metres.

Mechanical silhouettes, real attachment points and exposed steel wear surfaces are
favoured over decals. X is the direction of travel; axle shafts run along Y.
"""
from math import sin, cos, pi
from assetlib import Asset, register


def asset(label, size='large'):
    def decorate(fn):
        name='b07_'+label
        def factory():
            a=Asset(name, 'construction_machinery', size,
                    description=label.replace('_',' '), units='metres')
            fn(a)
            return a.bottom_center()
        register(name, 'construction_machinery', size, factory)
        return fn
    return decorate


def xz(a, pts, y0, y1, mat):
    """Closed extrusion of an XZ outline, with outward face winding."""
    if sum(x*z1-x1*z for (x,z),(x1,z1) in zip(pts,pts[1:]+pts[:1]))<0:
        pts=list(reversed(pts))
    n=len(pts)
    vs=[(x,y,z) for y in (y0,y1) for x,z in pts]
    a.mesh(vs,[tuple(range(n)),tuple(reversed(range(n,2*n)))]+
           [(i,n+i,n+(i+1)%n,(i+1)%n) for i in range(n)],mat)


def chamfer(a,c,s,mat='yellow',cut=.12):
    x,y,z=c; l,w,h=s; r=min(cut,l*.2,w*.2)
    a.prism([(x-l/2+r,y-w/2),(x+l/2-r,y-w/2),(x+l/2,y-w/2+r),
             (x+l/2,y+w/2-r),(x+l/2-r,y+w/2),(x-l/2+r,y+w/2),
             (x-l/2,y+w/2-r),(x-l/2,y-w/2+r)],z-h/2,z+h/2,mat)


def hood(a,c,s,mat='yellow',nose=1):
    """Pressed engine cover: sloping nose, raised crown and tapered shoulders."""
    x,y,z=c; l,w,h=s; b=z-h/2
    sections=[(-.50,.71,.87),(-.32,.98,1),(.25,.94,1),(.50,.60,.82)]
    if nose<0:sections=[(-t,ht,wd) for t,ht,wd in reversed(sections)]
    vs=[]
    for t,ht,wd in sections:
        xx=x+t*l; top=b+ht*h; ww=w*wd/2
        vs.extend([(xx,y-ww,b),(xx,y+ww,b),(xx,y+ww,b+h*.42),
                   (xx,y+ww*.77,top),(xx,y-ww*.77,top),(xx,y-ww,b+h*.42)])
    fs=[tuple(reversed(range(6))),tuple(range(18,24))]
    fs.extend((j*6+i,j*6+(i+1)%6,(j+1)*6+(i+1)%6,(j+1)*6+i) for j in range(3) for i in range(6))
    a.mesh(vs,fs,mat)


def fender(a,x,y,z,r,w,mat='yellow'):
    """Wheel-following sheet-metal arch, with thickness and exposed underside."""
    vs=[]; n=7
    for yy in (y-w/2,y+w/2):
        for rr in (r*1.10,r*1.10+.055):
            vs.extend((x+rr*cos(pi*.12+i*pi*.76/(n-1)),yy,z+rr*sin(pi*.12+i*pi*.76/(n-1))) for i in range(n))
    fs=[]
    for i in range(n-1):
        fs.extend([(i,i+1,n+i+1,n+i),(2*n+i,3*n+i,3*n+i+1,2*n+i+1),
                   (i,2*n+i,2*n+i+1,i+1),(n+i,n+i+1,3*n+i+1,3*n+i)])
    fs.extend([(0,n,3*n,2*n),(n-1,3*n-1,4*n-1,2*n-1)])
    a.mesh(vs,fs,mat)


def wheel(a,x,y,z,r=.48,w=.26,hub='yellow',treads=False):
    # Continuous tire shoulders replace stacked discs. Rim recess is visible on
    # both faces; the tread blocks follow the circumference in paired chevrons.
    rings=[(-.50,.55),(-.50,.78),(-.34,.96),(-.22,1),(.22,1),(.34,.96),(.50,.78),(.50,.55)]
    n=12;vs=[(x+r*rr*cos(i*2*pi/n),y+w*yy,z+r*rr*sin(i*2*pi/n)) for yy,rr in rings for i in range(n)]
    a.mesh(vs,[(j*n+i,j*n+(i+1)%n,((j+1)%len(rings))*n+(i+1)%n,((j+1)%len(rings))*n+i) for j in range(len(rings)) for i in range(n)],'rubber')
    for side in (-1,1):
        ya=y+side*w*.43; yb=y+side*w*.505
        a.cylinder((x,ya,z),(x,yb,z),r*.53,hub,12,r*.43)
        a.cylinder((x,yb,z),(x,yb+side*.046,z),r*.19,'dark_metal',8)
    if treads:
        for i in range(12):
            ang=2*pi*i/12
            for side in (-1,1):
                theta=ang+side*.06
                a.beam((x+r*1.015*cos(ang),y,z+r*1.015*sin(ang)),
                       (x+r*.985*cos(theta),y+side*w*.40,z+r*.985*sin(theta)),r*.16,r*.065,'rubber')


def wheels(a,xs,halfwidth,z,r,w=.28,treads=False):
    for x in xs:
        a.cylinder((x,-halfwidth,z),(x,halfwidth,z),.085,'dark_metal',8)
        for y in (-halfwidth,halfwidth):wheel(a,x,y,z,r,w,treads=treads)


def tracks(a,length=3.6,halfwidth=1.05,width=.45,height=.75,z=.04):
    for y in (-halfwidth,halfwidth):
        l=length/2; h=height; r=h*.5; side=-1 if y<0 else 1
        outer=[];inner=[]
        for xx,start in ((l-r,-pi/2),(-l+r,pi/2)):
            for j in range(5):
                th=start+j*pi/4
                outer.append((xx+r*cos(th),z+r+r*sin(th)))
                inner.append((xx+r*.77*cos(th),z+r+r*.77*sin(th)))
        n=len(outer);vs=[(xx,yy,zz) for yy in (y-width/2,y+width/2) for loop in (outer,inner) for xx,zz in loop];fs=[]
        for i in range(n):
            j=(i+1)%n
            fs.extend([(i,j,2*n+j,2*n+i),(n+i,3*n+i,3*n+j,n+j),
                       (i,n+i,n+j,j),(2*n+i,2*n+j,3*n+j,3*n+i)])
        a.mesh(vs,fs,'rubber')
        outside=y+side*width*.40
        a.box((0,y,z+h*.41),(length-h*.74,width*.51,h*.19),'dark_metal')
        for x in (-l+r,l-r):
            a.cylinder((x,y-width*.34,z+r),(x,y+width*.34,z+r),h*.35,'dark_metal',12)
            a.cylinder((x,outside,z+r),(x,outside+side*.025,z+r),h*.23,'metal',10)
            a.cylinder((x,outside+side*.03,z+r),(x,outside+side*.048,z+r),h*.095,'dark_metal',8)
        for i in range(4):
            x=(-l+r)+(length-h)*(i+1)/5
            a.cylinder((x,y-width*.34,z+h*.33),(x,y+width*.34,z+h*.33),h*.23,'dark_metal',10)
            a.cylinder((x,outside,z+h*.33),(x,outside+side*.018,z+h*.33),h*.11,'metal',8)
        # Track shoes wrap the idlers, then continue along the straight runs.
        for p,q in zip(outer,outer[1:]+outer[:1]):
            dx=q[0]-p[0];dz=q[1]-p[1];d=(dx*dx+dz*dz)**.5
            steps=max(1,round(d/(h*.37)))
            for j in range(steps):
                t=(j+.5)/steps;xx=p[0]+dx*t;zz=p[1]+dz*t
                a.beam((xx-dx/steps*.35,y,zz-dz/steps*.35),(xx+dx/steps*.35,y,zz+dz/steps*.35),width+.045,h*.075,'dark_metal')


def grille(a,x,y,z,width=.8,height=.5,axis='x'):
    if axis=='x':
        a.box((x,y,z),(.023,width,height),'black')
        for i in range(6): a.box((x+.016,y-width*.42+i*width*.168,z),(.022,.025,height*.84),'metal')
    else:
        a.box((x,y,z),(width,.023,height),'black')
        for i in range(6):a.box((x-width*.42+i*width*.168,y-.016,z),(.025,.022,height*.84),'metal')


def cab(a,c=(0,0,1.8),s=(1.3,1.35,1.65),mat='yellow'):
    """Tapered operator cell with fitted glazing, narrow pillars and a roof cap."""
    x,y,z=c; l,w,h=s; b=z-h/2; belt=b+h*.24; eave=b+h*.91
    # A chamfered waist and a narrower sloping roof define the actual body shape.
    levels=[(b,-.50,.49,.50),(belt,-.49,.49,.50),(eave,-.42,.27,.43)]
    vs=[]
    for zz,back,front,half in levels:
        xx0=x+l*back;xx1=x+l*front;yy0=y-w*half;yy1=y+w*half;k=l*.055
        vs.extend([(xx0+k,yy0,zz),(xx1-k,yy0,zz),(xx1,yy0+k,zz),(xx1,yy1-k,zz),
                   (xx1-k,yy1,zz),(xx0+k,yy1,zz),(xx0,yy1-k,zz),(xx0,yy0+k,zz)])
    fs=[tuple(reversed(range(8))),tuple(range(16,24))]
    fs.extend((j*8+i,j*8+(i+1)%8,(j+1)*8+(i+1)%8,(j+1)*8+i) for j in range(2) for i in range(8))
    a.mesh(vs,fs,mat)
    # Side window quads lie on the tapered wall rather than over a cuboid.
    for side in (-1,1):
        lower_y=y+side*(w*.50+.006);upper_y=y+side*(w*.43+.006)
        outer=[(x-l*.405,lower_y,belt+.025),(x+l*.405,lower_y,belt+.025),
               (x+l*.202,upper_y,eave-.025),(x-l*.338,upper_y,eave-.025)]
        a.mesh(outer,[(0,1,2,3)],'black')
        # Inset windshield frame, door stile and usable external handle.
        inset=[]
        for px,py,pz in outer:
            inset.append((x+(px-x)*.93,py+side*.004,pz+(.035 if pz<belt+.1 else -.035)))
        a.mesh(inset,[(0,1,2,3)],'glass')
        a.beam((x-l*.035,lower_y+side*.011,belt+.02),(x-l*.08,upper_y+side*.011,eave-.02),.055,.048,'dark_metal')
        a.box((x-l*.20,lower_y+side*.025,belt-.065),(.19,.055,.035),'silver')
        a.box((x-l*.24,y+side*w*.51,b+.02),(l*.63,.17,.065),'dark_metal')
        # Mirror stems emerge from the corner pillar, above hood height.
        a.beam((x+l*.27,upper_y,b+h*.76),(x+l*.39,y+side*w*.66,b+h*.75),.034,mat='dark_metal')
        a.box((x+l*.39,y+side*w*.68,b+h*.75),(.12,.065,.21),'black')
    # The forward and rear glazing match each inclined face exactly.
    for direction,xb,xt in ((1,.49,.27),(-1,-.49,-.42)):
        z0=belt+.065;z1=eave-.060;t0=(z0-belt)/(eave-belt);t1=(z1-belt)/(eave-belt)
        xx0=x+l*(xb+(xt-xb)*t0)+direction*.009;xx1=x+l*(xb+(xt-xb)*t1)+direction*.009
        wy0=w*(.50-.07*t0)-l*.09;wy1=w*(.50-.07*t1)-l*.09
        a.mesh([(xx0,y-wy0,z0),(xx0,y+wy0,z0),(xx1,y+wy1,z1),(xx1,y-wy1,z1)],[(0,1,2,3)],'glass')
        if direction==1:
            a.beam((xx0+.012,y-w*.21,z0+.045),(xx1+.045,y+w*.10,z1-h*.24),.023,mat='black')
    # Crown and drip edge have their own profile instead of a rectangular slab.
    hood(a,(x-l*.075,y,b+h*.958),(l*.91,w*.96,h*.13),'dark_metal')


def seat(a,x=0,y=0,z=1.3):
    a.cylinder((x,y,z-.35),(x,y,z-.08),.075,'dark_metal',8)
    a.box((x,y,z),(.46,.48,.12),'black')
    a.box((x-.23,y,z+.25),(.10,.46,.47),'black',rot=(0,-.10,0))
    for yy in (y-.28,y+.28):a.box((x-.02,yy,z+.19),(.30,.065,.065),'dark_metal')


def rops(a,x=0,width=1.2,z0=.8,z1=2.5,length=1.4):
    for xx in (x-length*.42,x+length*.42):
        for yy in (-width/2,width/2):a.beam((xx,yy,z0),(x+(xx-x)*.88,yy*.92,z1),.07,mat='dark_metal')
    hood(a,(x,0,z1+.045),(length,width+.16,.13),'yellow')


def ram(a,p,q,r=.08):
    t=tuple(p[i]+(q[i]-p[i])*.59 for i in range(3))
    a.cylinder(p,t,r,'dark_metal',8)
    a.cylinder(t,q,r*.53,'silver',8)
    for point in (p,q):a.cylinder((point[0],point[1]-.065,point[2]),(point[0],point[1]+.065,point[2]),r*1.2,'metal',8)


def bucket(a,x=2,y=0,z=.2,w=1.8,l=1,h=.8,teeth=5):
    profile=[(x,z+h),(x+l*.19,z+.07),(x+l,z),(x+l*.94,z+.16),(x+l*.32,z+.29),(x+.13,z+h)]
    for yy in (y-w/2,y+w/2-.065):xz(a,profile,yy,yy+.065,'dark_metal')
    a.beam((x+l*.20,y,z+.13),(x+l*.95,y,z+.07),w,.085,'dark_metal')
    a.beam((x+.055,y,z+h*.94),(x+l*.24,y,z+.15),w,.085,'dark_metal')
    a.cylinder((x+.16,y-w*.43,z+h*.72),(x+.16,y+w*.43,z+h*.72),.07,'metal',8)
    for i in range(teeth):
        yy=y-w*.43+w*.86*i/max(1,teeth-1)
        a.box((x+l+.035,yy,z+.09),(.24,.10,.065),'steel',rot=(0,-.12,0))


def beacon(a,x,y,z):
    a.cylinder((x,y,z),(x,y,z+.06),.08,'black',8)
    a.cylinder((x,y,z+.06),(x,y,z+.19),.07,'orange',8,radius2=.05)


def lamps(a,x,ys,z):
    for y in ys:
        a.box((x,y,z),(.08,.17,.14),'dark_metal')
        a.box((x+.044,y,z),(.018,.13,.09),'light')


def trailer(a,length=2.6,width=1.45,z=.58,wheel_r=.34):
    for y in (-width*.40,width*.40):a.box((0,y,z),(length,.11,.16),'dark_metal')
    for x in (-length*.42,length*.42):a.box((x,0,z),(.12,width,.16),'dark_metal')
    wheels(a,[-.22],width*.55,wheel_r,wheel_r,.22)
    for yy in (-width*.36,width*.36):a.beam((length*.48,yy,z),(length*.9,0,z),.10,mat='dark_metal')
    a.box((length*.94,0,z),(.30,.15,.11),'metal')
    a.cylinder((length*.76,.18,.08),(length*.76,.18,z+.12),.045,'metal',8)
    a.box((length*.76,.18,.07),(.22,.21,.045),'dark_metal')
    for y in (-width*.58,width*.58):
        a.box((-.22,y,wheel_r*2+.055),(.88,.34,.045),'metal')
        a.box((-length*.47,y*.80,z+.08),(.035,.14,.10),'red')


def railing(a,x0,x1,y,z,h=.95,mat='metal'):
    for x in (x0,(x0+x1)/2,x1):a.cylinder((x,y,z),(x,y,z+h),.026,mat,6)
    for zz in (z+h*.52,z+h):a.cylinder((x0,y,zz),(x1,y,zz),.025,mat,6)


def ladder(a,x,y,z0,z1,width=.45,step=.28):
    for yy in (y-width/2,y+width/2):a.cylinder((x,yy,z0),(x,yy,z1),.025,'metal',6)
    n=max(1,int((z1-z0)/step))
    for i in range(n):
        zz=z0+(z1-z0)*(i+.25)/n
        a.cylinder((x,y-width/2,zz),(x,y+width/2,zz),.023,'metal',6)


def outrigger(a,x,y,z=1):
    a.beam((x,y*.38,z),(x,y,z*.50),.14,mat='yellow')
    a.cylinder((x,y,.11),(x,y,z*.67),.07,'silver',8)
    a.box((x,y,.09),(.38,.38,.12),'dark_metal')


@asset('tracked_hydraulic_excavator')
def tracked_excavator(a):
    tracks(a,4.5,1.22,.60,.92)
    a.box((0,0,.88),(3.1,2.3,.28),'dark_metal')
    a.cylinder((0,0,1),(0,0,1.25),.89,'dark_metal',12)
    hood(a,(-.65,0,1.55),(2.4,2.48,.64),nose=-1)
    cab(a,(.05,-.65,2.25),(1.65,1.10,1.80))
    grille(a,-1.865,0,1.44,1.45,.28)
    a.cylinder((-1.20,.48,1.85),(-1.20,.48,2.60),.07,'dark_metal',8)
    # Forged gooseneck boom and a tapered dipper have a continuous outline.
    xz(a,[(.47,1.60),(.65,1.43),(1.94,3.06),(3.61,2.55),(3.83,2.81),(2.17,3.57),(1.87,3.59)],.21,.59,'yellow')
    xz(a,[(3.52,2.76),(3.83,2.76),(3.73,2.36),(3.55,.85),(3.34,.87),(3.42,1.43)],.25,.55,'yellow')
    for xx,zz in ((.60,1.65),(2,3.40),(3.7,2.7),(3.45,.90)):
        a.cylinder((xx,.16,zz),(xx,.64,zz),.13,'dark_metal',10)
    ram(a,(.60,.08,1.60),(1.85,.08,3.15),.105)
    ram(a,(2.1,.12,3.47),(3.53,.12,2.71),.075)
    ram(a,(3.82,.1,2.5),(3.60,.1,1.14),.065)
    bucket(a,3.23,.4,.17,1.02,.92,.89,5)
    a.tube([(.9,.65,1.75),(1.65,.65,3.26),(2.08,.65,3.51),(3.54,.65,2.84)],.022,'black')
    beacon(a,-.58,-.62,3.19)
    lamps(a,.88,[-.91,-.4],2.91)


@asset('mini_excavator_open_canopy')
def mini_excavator(a):
    tracks(a,2.1,.65,.32,.48)
    a.cylinder((0,0,.54),(0,0,.72),.57,'dark_metal',10)
    hood(a,(-.27,0,.87),(1.5,1.35,.39),nose=-1)
    seat(a,-.37,-.15,1.04);rops(a,-.42,.95,.86,2.1,1.05)
    a.box((.18,-.35,1.06),(.28,.17,.20),'dark_metal')
    for p,q in [((.53,.32,.98),(1.05,.32,2.14)),((1.05,.32,2.14),(1.94,.32,1.64)),((1.94,.32,1.64),(1.88,.32,.52))]:a.beam(p,q,.19,.22,'yellow')
    ram(a,(.38,.16,.90),(.94,.16,1.95),.06);ram(a,(1.21,.16,2.19),(1.91,.16,1.73),.044)
    bucket(a,1.7,.32,.03,.48,.58,.52,3)
    a.beam((.42,-.56,.55),(.94,-.56,.3),.12,mat='dark_metal');a.beam((.42,.56,.55),(.94,.56,.3),.12,mat='dark_metal')
    a.box((1.08,0,.26),(.17,1.5,.40),'yellow',rot=(0,-.13,0))
    a.box((1.16,0,.07),(.07,1.55,.065),'steel')


def skid_body(a,tracked=False):
    if tracked:tracks(a,2.2,.74,.38,.50)
    else:wheels(a,[-.71,.69],.71,.43,.43,.32,True)
    hood(a,(-.05,0,.72),(1.88,1.35,.61),'yellow',-1)
    cab(a,(-.12,0,1.47),(1.02,1.01,1.35),'dark_metal')
    grille(a,-1.002,0,.70,.87,.29)
    for y in (-.66,.66):
        a.beam((-.65,y,1.43),(.44,y,1.09),.15,.19,'yellow')
        a.beam((.44,y,1.09),(1.13,y,.52),.15,.18,'yellow')
        ram(a,(-.67,y,.79),(.36,y,1.06),.06)
        for x in (-.52,-.30,-.08,.14,.36):a.box((x,y*.77,1.69),(.025,.018,.65),'dark_metal')
    bucket(a,1.0,0,.1,1.54,.69,.60,5)
    lamps(a,.43,[-.43,.43],2.12)


@asset('wheeled_skid_steer_loader')
def skid_steer(a):skid_body(a)


@asset('compact_track_loader_grapple')
def track_loader(a):
    skid_body(a,True)
    for y in (-.53,.53):
        a.beam((1.13,y,.79),(1.59,y,.95),.09,mat='dark_metal')
        a.beam((1.59,y,.95),(1.87,y,.47),.09,mat='dark_metal')
        ram(a,(.82,y,1.05),(1.46,y,.90),.04)
    a.cylinder((1.30,-.70,.80),(1.30,.70,.80),.07,'yellow',8)


@asset('articulated_wheel_loader')
def wheel_loader(a):
    wheels(a,[-1.35,1.19],1.08,.72,.72,.44,True)
    # Distinct front and rear chassis expose the oscillating articulation joint.
    chamfer(a,(-1.03,0,.93),(2.10,1.48,.39),'dark_metal')
    xz(a,[(.12,.74),(1.70,.74),(1.72,1.05),(.85,1.24),(.13,1.08)],-.59,.59,'yellow')
    a.cylinder((-.02,0,.74),(-.02,0,1.20),.24,'dark_metal',10)
    for y in (-.44,.44):ram(a,(-.43,y,.91),(.62,y,.98),.055)
    hood(a,(-1.35,0,1.43),(1.46,1.9,.89),nose=-1)
    cab(a,(-.35,0,2.26),(1.32,1.48,1.75))
    grille(a,-2.088,0,1.30,1.30,.35)
    a.cylinder((-1.52,.67,1.85),(-1.52,.67,2.8),.07,'dark_metal',8)
    for y in (-.52,.52):
        xz(a,[(.22,1.22),(.32,1.49),(1.49,1.84),(1.68,1.75),(2.46,.77),(2.28,.59),(1.44,1.48)],y-.11,y+.11,'yellow')
        ram(a,(.27,y,1.14),(1.47,y,1.68),.09)
        for xx,zz in ((.30,1.36),(1.53,1.65),(2.38,.71)):
            a.cylinder((xx,y-.15,zz),(xx,y+.15,zz),.115,'dark_metal',8)
    bucket(a,2.05,0,.07,2.22,1.1,.99,6)
    ram(a,(.77,0,1.6),(1.97,0,1.08),.085)
    beacon(a,-.42,0,3.18)
    for y in (-.83,.83):a.box((-.58,y,.97),(.53,.26,.12),'metal')
    for x in (-1.35,1.19):
        for y in (-1.08,1.08):fender(a,x,y,.72,.72,.55)


@asset('backhoe_loader')
def backhoe(a):
    for x,r,z in [(-1.30,.68,.68),(1.05,.51,.51)]:wheels(a,[x],.91,z,r,.35,True)
    a.box((0,0,.86),(3.2,1.48,.35),'dark_metal')
    hood(a,(.76,0,1.31),(1.39,1.22,.64))
    cab(a,(-.60,0,1.99),(1.47,1.41,1.75))
    for y in (-.91,.91):fender(a,-1.30,y,.68,.68,.48)
    grille(a,1.465,0,1.18,.85,.28)
    for y in (-.7,.7):
        a.beam((-.59,y,1.34),(1.05,y,1.12),.16,mat='yellow')
        a.beam((1.05,y,1.12),(1.78,y,.55),.16,mat='yellow')
        ram(a,(-.41,y,.93),(.89,y,1.09),.065)
    bucket(a,1.62,0,.08,1.9,.7,.67,5)
    a.beam((-1.50,0,1.08),(-2.33,0,2.74),.23,.27,'yellow')
    a.beam((-2.33,0,2.74),(-3.04,0,1.16),.19,.24,'yellow')
    ram(a,(-1.6,-.17,1.07),(-2.39,-.17,2.5),.065)
    a.beam((-3.04,0,1.16),(-3.18,0,.45),.16,mat='yellow')
    bucket(a,-3.40,0,.1,.54,.60,.65,3)
    for y in (-1.48,1.48):outrigger(a,-1.45,y,.95)


@asset('crawler_bulldozer')
def bulldozer(a):
    tracks(a,3.6,1.03,.55,.87)
    a.box((0,0,.99),(2.6,1.8,.35),'dark_metal')
    hood(a,(.57,0,1.42),(1.67,1.6,.66))
    cab(a,(-.75,0,2.06),(1.25,1.49,1.62))
    grille(a,1.42,0,1.30,1.12,.31)
    for y in (-1.26,1.26):
        a.beam((-.62,y,.43),(2.12,y,.64),.18,.21,'dark_metal')
        ram(a,(.73,y*.70,1.62),(1.93,y,.79),.09)
    # A folded moldboard rolls material upward; the cutting edge is its own part.
    blade=[(2.31,.25),(2.25,.53),(2.09,.94),(2.03,1.31),(2.13,1.31),(2.19,.94),(2.36,.53),(2.42,.25)]
    xz(a,blade,-1.52,1.52,'yellow')
    a.box((2.40,0,.24),(.17,3.16,.12),'steel',rot=(0,-.12,0))
    for y in (-1.56,1.48):
        xz(a,[(2.02,1.30),(2.20,1.30),(2.46,.32),(2.30,.24),(2.15,.65)],y,y+.08,'yellow')
    for y in (-.95,.95):a.beam((1.96,y,.55),(1.88,y,1.16),.11,.15,'dark_metal')
    a.beam((-1.31,0,.80),(-2.0,0,.63),.18,mat='yellow')
    for y in (-.57,0,.57):xz(a,[(-1.83,.76),(-2.01,.76),(-2.11,.31),(-2.34,.13),(-2.13,.12),(-1.94,.30)],y-.065,y+.065,'dark_metal')


@asset('motor_grader')
def motor_grader(a):
    wheels(a,[-2.1,-1.12,2.30],1.04,.59,.59,.33,True)
    a.box((-1.75,0,.92),(2.2,1.48,.39),'dark_metal')
    hood(a,(-2.01,0,1.51),(1.56,1.44,.78),nose=-1)
    cab(a,(-.77,0,2.08),(1.26,1.34,1.65))
    grille(a,-2.80,0,1.36,1.01,.36)
    for y in (-1.04,1.04):
        a.beam((-2.10,y,.59),(-1.12,y,.59),.22,.28,'dark_metal')
        fender(a,-2.10,y,.59,.59,.42)
        fender(a,-1.12,y,.59,.59,.42)
    a.beam((-.7,0,1.29),(1.98,0,1.06),.26,.28,'yellow')
    a.beam((1.98,0,1.06),(2.35,0,.62),.24,.27,'yellow')
    a.cylinder((.30,0,.50),(.30,0,.61),.67,'dark_metal',12)
    a.box((.52,0,.39),(.20,3.03,.66),'yellow',rot=(0,-.13,-.36))
    a.box((.58,0,.095),(.09,3.10,.08),'steel',rot=(0,0,-.36))
    for y in (-.55,.55):ram(a,(-.12,y,1.3),(.54,y,.62),.066)
    a.cylinder((-2.5,.52,1.70),(-2.5,.52,2.55),.065,'dark_metal',8)


@asset('tracked_asphalt_paver')
def asphalt_paver(a):
    tracks(a,3.45,1.09,.46,.70)
    chamfer(a,(-.3,0,1.0),(3.2,2.05,.55))
    # Wide receiving hopper with open interior and folded sloped wings.
    a.box((1.49,0,.97),(1.47,1.92,.12),'dark_metal')
    for y in (-1.15,1.15):a.box((1.45,y,1.28),(1.58,.16,.78),'yellow',rot=(.38 if y<0 else -.38,0,0))
    a.box((2.18,0,1.03),(.10,2.52,.48),'yellow')
    a.box((.61,0,1.32),(.16,2.0,.73),'yellow')
    hood(a,(-.36,0,1.52),(1.55,1.62,.75))
    grille(a,.43,0,1.43,1.10,.30)
    a.box((-1.29,0,1.2),(1.0,2.1,.12),'dark_metal')
    for y in (-.67,.67):seat(a,-1.19,y,1.64)
    rops(a,-.97,1.90,1.27,2.83,1.6)
    a.box((-2.15,0,.34),(.72,3.2,.29),'dark_metal')
    a.box((-2.47,0,.18),(.16,3.35,.13),'steel')
    for y in (-.94,.94):a.beam((-.50,y,.69),(-2.13,y,.49),.12,mat='yellow')
    railing(a,-1.64,-.7,-1.04,1.25,.75)


@asset('tandem_vibratory_road_roller')
def tandem_roller(a):
    for x in (-1.05,1.05):
        a.cylinder((x,-.82,.62),(x,.82,.62),.62,'metal',16)
        for y in (-.91,.91):
            xz(a,[(x-.38,.64),(x-.28,1.12),(x+.27,1.12),(x+.38,.64),(x+.23,.49),(x-.23,.49)],y-.075,y+.075,'yellow')
            a.cylinder((x,y-.07,.62),(x,y+.07,.62),.17,'dark_metal',8)
    for x in (-.81,.81):hood(a,(x,0,1.03),(1.36,1.38,.40),'yellow')
    a.cylinder((0,0,.90),(0,0,1.20),.20,'dark_metal',10)
    hood(a,(.67,0,1.34),(1.02,1.23,.40))
    seat(a,-.36,0,1.50);rops(a,-.48,1.32,1.1,2.65,1.45)
    a.beam((.12,0,1.28),(.12,0,1.68),.08,mat='dark_metal')
    a.torus((.13,0,1.71),.20,.025,'black',axis=(.45,0,1),segments=10,sides=5)
    for x in (-1.03,1.04):a.box((x,0,1.25),(.52,1.57,.045),'yellow')
    beacon(a,-.66,.52,2.72)


@asset('single_drum_soil_compactor')
def soil_compactor(a):
    wheels(a,[-1.22],1.03,.69,.69,.44,True)
    a.cylinder((1.32,-1.09,.78),(1.32,1.09,.78),.78,'metal',16)
    for y in (-1.17,1.17):
        a.beam((.25,y,.94),(1.33,y,.78),.19,.22,'yellow')
        a.cylinder((1.32,y-.08,.78),(1.32,y+.08,.78),.19,'dark_metal',8)
    a.box((-.42,0,1.15),(2.66,1.69,.40),'yellow')
    hood(a,(-1.32,0,1.55),(1.30,1.80,.54),nose=-1)
    cab(a,(-.32,0,2.19),(1.36,1.48,1.61))
    grille(a,-1.985,0,1.44,1.29,.26)
    for y in (-1.03,1.03):fender(a,-1.22,y,.69,.69,.55)
    a.box((1.98,0,.88),(.14,2.3,.16),'dark_metal')
    beacon(a,-.44,0,3.03)


@asset('remote_trench_padfoot_roller')
def trench_roller(a):
    for x in (-.61,.61):
        for y in (-.35,.35):
            a.cylinder((x,y-.22,.37),(x,y+.22,.37),.34,'dark_metal',12)
            for i in range(10):
                theta=2*pi*i/10
                a.box((x+.35*cos(theta),y,.37+.35*sin(theta)),(.12,.29,.07),'metal',rot=(0,pi/2-theta,0))
    hood(a,(0,0,.91),(1.62,.70,.55),'yellow')
    a.box((0,0,1.23),(.38,.49,.12),'dark_metal')
    a.cylinder((0,0,1.24),(0,0,1.40),.06,'orange',8)
    a.tube([(-.45,0,1.16),(-.45,0,1.35),(.45,0,1.35),(.45,0,1.16)],.035,'dark_metal')
    grille(a,.825,0,.81,.39,.20)


@asset('cold_planer_road_milling_machine')
def road_mill(a):
    for x in (-1.65,1.40):
        temp=Asset('track')
        tracks(temp,1.38,1.02,.36,.52)
        temp.translate((x,0,.0));a.mesh(temp.vertices,temp.faces,temp.face_materials)
    hood(a,(-.23,0,1.12),(4.3,2.07,.85),nose=-1)
    a.box((-.1,0,.43),(1.45,2.14,.46),'dark_metal')
    grille(a,-2.395,0,.96,1.50,.39)
    a.box((.83,0,1.63),(1.70,1.96,.12),'dark_metal')
    seat(a,.84,-.53,1.93);rops(a,.85,1.72,1.62,3.02,1.68)
    # Angled discharge conveyor, with rubber belt and high sidewalls.
    p=(1.30,0,1.17);q=(4.5,0,2.97)
    a.beam(p,q,.80,.15,'black')
    for y in (-.45,.45):a.beam((p[0],y,p[2]+.05),(q[0],y,q[2]+.05),.09,.22,'yellow')
    for i in range(9):
        t=(i+.4)/9;a.box((1.3+3.2*t,0,1.23+1.8*t),(.055,.77,.045),'dark_metal',rot=(0,-.51,0))
    ram(a,(1.5,.55,1.04),(3.45,.55,2.42),.07)
    beacon(a,.30,.63,3.10)


@asset('telescopic_construction_handler')
def telehandler(a):
    wheels(a,[-1.28,1.28],1.0,.64,.64,.43,True)
    a.box((0,0,.92),(3.42,1.74,.44),'dark_metal')
    hood(a,(-.56,.56,1.27),(2.35,.92,.69),nose=-1)
    cab(a,(-.48,-.5,1.99),(1.53,1.01,1.62))
    p=(-1.13,.35,1.56);q=(2.32,.35,2.55)
    a.beam(p,q,.36,.40,'yellow')
    a.beam((1.32,.35,2.26),(3.07,.35,2.77),.26,.27,'dark_metal')
    ram(a,(-.22,.32,1.02),(1.12,.32,2.21),.095)
    a.box((3.16,.35,2.33),(.13,1.35,1.06),'dark_metal')
    for y in (-.10,.80):
        a.box((3.25,y,2.15),(.10,.12,.80),'steel')
        a.box((3.72,y,1.78),(1.03,.12,.10),'steel')
    grille(a,-1.74,.58,1.14,.56,.29)
    for xx in (-1.28,1.28):
        for yy in (-1.0,1.0):fender(a,xx,yy,.64,.64,.50)
    beacon(a,-.50,-.5,2.84)


@asset('electric_scissor_lift_extended')
def scissor_lift(a):
    wheels(a,[-.9,.9],.51,.25,.25,.16)
    chamfer(a,(0,0,.48),(2.25,1.0,.45),'blue')
    for y in (-.40,.40):
        for k in range(3):
            z=.72+k*.64
            a.beam((-.82,y,z),(.82,y,z+.68),.075,.115,'metal')
            a.beam((.82,y,z),(-.82,y,z+.68),.075,.115,'metal')
            a.cylinder((0,y-.085,z+.34),(0,y+.085,z+.34),.06,'dark_metal',8)
    ram(a,(-.67,0,.77),(.46,0,1.83),.07)
    a.box((.13,0,2.78),(2.69,1.20,.14),'dark_metal')
    for y in (-.6,.6):
        a.box((.13,y,2.93),(2.69,.05,.23),'blue')
        railing(a,-1.20,1.47,y,2.86,1.0,'blue')
    for x in (-1.20,1.47):
        for z in (3.32,3.86):a.cylinder((x,-.6,z),(x,.6,z),.028,'blue',6)
    a.box((1.28,-.51,3.70),(.3,.20,.13),'dark_metal')
    ladder(a,-1.16,0,.37,1.3,.47)


def basket(a,x,y,z,w=1.35,l=.9):
    a.box((x,y,z),(l,w,.12),'dark_metal')
    for yy in (y-w/2,y+w/2):
        railing(a,x-l/2,x+l/2,yy,z+.1,.95,'yellow')
        a.box((x,yy,z+.19),(l,.035,.23),'yellow')
    for xx in (x-l/2,x+l/2):
        for zz in (z+.57,z+1.05):a.cylinder((xx,y-w/2,zz),(xx,y+w/2,zz),.024,'yellow',6)
    a.box((x+l*.20,y-w*.43,z+.96),(.25,.18,.12),'dark_metal')


@asset('articulating_boom_lift')
def boom_lift(a):
    wheels(a,[-.98,.98],.95,.55,.55,.34,True)
    hood(a,(0,0,.78),(2.75,1.80,.6),'blue')
    a.cylinder((-.40,0,1.04),(-.40,0,1.25),.61,'dark_metal',10)
    hood(a,(-.66,0,1.39),(1.50,1.44,.42),'blue',-1)
    pts=[(-.30,0,1.5),(.85,0,3.28),(2.45,0,2.7),(3.23,0,3.45)]
    for p,q in zip(pts,pts[1:]):a.beam(p,q,.24,.28,'blue')
    ram(a,(-.24,-.21,1.34),(.79,-.21,3.04),.075)
    ram(a,(.97,-.18,3.18),(2.27,-.18,2.76),.065)
    a.tube([(0,.18,1.50),(.8,.18,3.41),(2.47,.18,2.88),(3.28,.18,3.52)],.022,'black')
    basket(a,3.64,0,3.37)


@asset('towable_cherry_picker')
def towable_lift(a):
    trailer(a,2.52,1.38,.62,.35)
    hood(a,(-.52,0,.93),(1.47,1.19,.53),'green',-1)
    for x in (-.96,.85):
        for y in (-1.39,1.39):outrigger(a,x,y,.71)
    a.cylinder((-.45,0,1.13),(-.45,0,1.35),.4,'dark_metal',10)
    for p,q in [((-.45,0,1.39),(-1.54,0,3.36)),((-1.54,0,3.36),(.80,0,3.0))]:a.beam(p,q,.19,.22,'cream')
    ram(a,(-.19,-.2,1.14),(-1.35,-.2,3.09),.066)
    a.beam((.24,0,3.12),(1.43,0,2.94),.14,mat='metal')
    basket(a,1.65,0,2.57,1.05,.78)


@asset('rough_terrain_mobile_crane')
def mobile_crane(a):
    wheels(a,[-1.54,1.54],1.16,.74,.74,.46,True)
    a.box((0,0,1.06),(4.4,2.04,.40),'dark_metal')
    for x in (-1.32,1.25):
        for y in (-2.01,2.01):outrigger(a,x,y,1.05)
    a.cylinder((-.26,0,1.26),(-.26,0,1.51),.87,'dark_metal',12)
    hood(a,(-.60,0,1.72),(2.77,2.13,.48),nose=-1)
    cab(a,(.23,-.74,2.23),(1.62,.89,1.53))
    for xx in (-1.54,1.54):
        for yy in (-1.16,1.16):fender(a,xx,yy,.74,.74,.55)
    a.beam((-1.15,.30,1.94),(1.9,.30,4.34),.50,.46,'yellow')
    a.beam((1.45,.30,3.99),(3.35,.30,5.48),.34,.32,'dark_metal')
    ram(a,(-.68,.22,1.53),(1.30,.22,3.88),.13)
    a.cylinder((3.35,.06,5.42),(3.35,.53,5.42),.21,'dark_metal',10)
    a.tube([(3.48,.3,5.47),(3.48,.3,2.64)],.015,'black')
    a.box((3.48,.3,2.52),(.22,.18,.29),'yellow')
    a.torus((3.48,.3,2.26),.13,.04,'dark_metal',axis='y',segments=8,sides=5,arc=1.6*pi)
    beacon(a,-.07,-.66,3.03)


def lattice(a,p,q,width=.65,segments=6,mat='yellow'):
    # Boom in XZ plane; four longitudinal chords and diagonal braces.
    dx=q[0]-p[0];dz=q[2]-p[2];length=(dx*dx+dz*dz)**.5
    nx=-dz/length*width/2;nz=dx/length*width/2
    corners=[]
    for sy in (-1,1):
        for sn in (-1,1):
            corners.append((sy*width/2,sn*nx,sn*nz))
            a.beam((p[0]+sn*nx,p[1]+sy*width/2,p[2]+sn*nz),
                   (q[0]+sn*nx,q[1]+sy*width/2,q[2]+sn*nz),.075,mat=mat)
    for j in range(segments):
        t0=j/segments;t1=(j+1)/segments
        for sy in (-1,1):
            sign=1 if j%2 else -1
            a.beam((p[0]+dx*t0+sign*nx,p[1]+sy*width/2,p[2]+dz*t0+sign*nz),
                   (p[0]+dx*t1-sign*nx,p[1]+sy*width/2,p[2]+dz*t1-sign*nz),.04,mat=mat)
        a.beam((p[0]+dx*t0+nx,p[1]-width/2,p[2]+dz*t0+nz),
               (p[0]+dx*t0+nx,p[1]+width/2,p[2]+dz*t0+nz),.055,mat=mat)


@asset('self_erecting_tower_crane')
def tower_crane(a):
    a.box((0,0,.2),(3.8,3.4,.4),'concrete')
    for x in (-.6,.6):
        for y in (-.6,.6):a.box((x,y,.50),(.28,.28,.24),'dark_metal')
    lattice(a,(0,0,.48),(0,0,8.1),1.02,10)
    a.cylinder((0,0,8.04),(0,0,8.29),.72,'dark_metal',12)
    lattice(a,(-3.0,0,8.65),(8.30,0,8.65),.64,12)
    a.beam((0,0,8.20),(0,0,10.02),.16,mat='yellow')
    a.tube([(-2.9,0,8.90),(0,0,10.02),(7.65,0,8.90)],.023,'dark_metal')
    a.box((-2.58,0,8.13),(1.0,1.22,.8),'concrete')
    cab(a,(.61,-.80,7.85),(1.01,.87,1.28))
    a.box((6.29,0,8.22),(.45,.65,.18),'dark_metal')
    for y in (-.12,.12):a.cylinder((6.29,y,8.2),(6.29,y,4.82),.012,'black',6)
    a.box((6.29,0,4.68),(.22,.32,.31),'yellow')
    a.torus((6.29,0,4.4),.14,.044,'dark_metal',axis='y',segments=8,sides=5,arc=1.6*pi)
    ladder(a,.60,0,.54,7.50,.39,.32)


@asset('lattice_boom_crawler_crane')
def crawler_crane(a):
    tracks(a,4.2,1.22,.61,.86)
    a.cylinder((-.17,0,.96),(-.17,0,1.16),.98,'dark_metal',12)
    hood(a,(-.5,0,1.59),(3.0,2.35,.9),'yellow',-1)
    cab(a,(.55,-.76,2.05),(1.45,1.01,1.57))
    lattice(a,(.76,.30,1.8),(5.28,.30,7.18),.77,9)
    a.beam((-.89,0,1.94),(-.21,0,3.85),.13,mat='dark_metal')
    a.tube([(-1.48,0,1.99),(-.21,0,3.85),(5.28,.3,7.18)],.025,'dark_metal')
    a.cylinder((5.3,.02,7.16),(5.3,.56,7.16),.21,'dark_metal',10)
    for y in (.17,.39):a.cylinder((5.42,y,7.13),(5.42,y,2.65),.014,'black',6)
    a.box((5.42,.28,2.52),(.3,.36,.36),'yellow')
    a.torus((5.42,.28,2.17),.18,.055,'dark_metal',axis='y',segments=9,sides=5,arc=1.6*pi)
    grille(a,-2.015,0,1.39,1.63,.40)


@asset('tilting_drum_concrete_mixer','person')
def cement_mixer(a):
    wheels(a,[-.27],.60,.25,.25,.14)
    for y in (-.40,.40):
        a.beam((-.56,y,.25),(.29,y,1.05),.07,mat='dark_metal')
        a.beam((.53,y,.04),(.24,y,1.02),.07,mat='dark_metal')
    a.box((.53,0,.04),(.25,1.0,.075),'dark_metal')
    a.cylinder((0,-.48,.94),(0,.48,.94),.06,'steel',8)
    p=(-.36,0,1.03);q=(.12,0,1.50);r=(.48,0,1.76)
    a.cylinder(p,q,.45,'yellow',12,radius2=.49)
    a.cylinder(q,r,.49,'yellow',12,radius2=.30,cap=False)
    a.torus(r,.30,.037,'dark_metal',axis=(.7,0,.7),segments=12,sides=5)
    a.cylinder((.47,0,1.75),(.40,0,1.70),.264,'black',12)
    a.torus((0,.62,1.03),.33,.028,'metal',axis='y',segments=12,sides=5)
    for ang in (0,2*pi/3,4*pi/3):a.beam((0,.62,1.03),(.3*cos(ang),.62,1.03+.3*sin(ang)),.025,mat='metal')
    a.box((-.39,0,.59),(.43,.46,.35),'dark_metal')


@asset('towable_paddle_mortar_mixer')
def mortar_mixer(a):
    trailer(a,1.95,1.27,.48,.29)
    for x in (-.67,.62):a.box((x,0,.84),(.11,1.02,.56),'dark_metal')
    a.cylinder((-.77,0,1.22),(.79,0,1.22),.45,'green',12)
    a.box((0,0,1.58),(1.40,.72,.1),'dark_metal')
    for x in (-.58,-.36,-.14,.08,.30,.52):a.box((x,0,1.65),(.035,.71,.045),'metal')
    a.cylinder((-.88,0,1.22),(.89,0,1.22),.07,'metal',8)
    a.box((-.82,0,.78),(.46,.60,.32),'black')
    a.torus((.98,0,1.22),.24,.027,'metal',axis='x',segments=10,sides=5)
    a.beam((.98,0,1.22),(.98,.23,1.22),.024,mat='metal')
    a.box((.17,-.4,1.34),(.55,.10,.36),'green',rot=(.35,0,0))


@asset('diesel_air_compressor_trailer')
def compressor(a):
    trailer(a,2.15,1.30,.50,.31)
    hood(a,(-.16,0,1.10),(2.05,1.21,.91),'yellow',-1)
    grille(a,-1.20,0,1.02,.86,.30)
    for y in (-.62,.62):
        grille(a,.35,y,.91,.65,.22,'y')
        a.box((-.20,y,1.05),(.19,.04,.04),'dark_metal')
    a.cylinder((-.73,.31,1.44),(-.73,.31,1.97),.055,'dark_metal',8)
    a.tube([(-.35,-.16,1.50),(-.35,-.16,1.70),(.14,-.16,1.70),(.14,-.16,1.50)],.035,'dark_metal')
    for y in (-.27,.27):
        a.cylinder((.95,y,.87),(1.10,y,.87),.05,'gold',8)
        a.box((1.05,y,.97),(.04,.22,.035),'red')
    a.tube([(1.10,.27,.87),(1.28,.4,.62),(1.12,.57,.36),(.77,.60,.32)],.033,'black')


@asset('silenced_diesel_generator_trailer')
def generator(a):
    trailer(a,3.05,1.54,.59,.36)
    chamfer(a,(-.09,0,1.30),(2.87,1.45,1.16),'cream')
    grille(a,-1.54,0,1.31,1.10,.89)
    a.box((.32,-.734,1.39),(.98,.025,.79),'metal')
    a.box((.30,-.754,1.56),(.65,.024,.32),'dark_metal')
    for x in (.03,.21,.39):a.cylinder((x,-.78,1.57),(x,-.80,1.57),.037,'black',8)
    a.box((.60,-.78,1.57),(.08,.03,.11),'green')
    for x in (.04,.39,.66):a.cylinder((x,-.755,1.18),(x,-.793,1.18),.073,'black',8)
    a.cylinder((-.68,.32,1.9),(-.68,.32,2.2),.058,'dark_metal',8)
    a.box((-.69,.34,2.22),(.22,.13,.045),'dark_metal')
    for x in (-.7,.7):a.torus((x,0,1.94),.085,.025,'metal',axis='y',segments=8,sides=5)


@asset('portable_light_tower_trailer')
def light_tower(a):
    trailer(a,2.10,1.27,.49,.30)
    hood(a,(-.34,0,.94),(1.43,1.12,.76),'cream',-1)
    grille(a,-1.075,0,.84,.77,.31)
    a.box((.39,0,.72),(.29,.40,.32),'dark_metal')
    for x,y in [(-.87,-1),(-.87,1),(.73,-.82),(.73,.82)]:outrigger(a,x,y,.55)
    for z,h,w in [(1.63,2.1,.17),(3.27,1.7,.13),(4.50,1.0,.085)]:a.box((.35,0,z), (w,w,h),'metal')
    a.box((.35,0,5.02),(.1,1.95,.1),'dark_metal')
    for y in (-.80,-.27,.27,.80):
        a.beam((.35,y,5.0),(.45,y,5.20),.035,mat='dark_metal')
        a.box((.50,y,5.22),(.15,.39,.35),'dark_metal',rot=(0,-.25,0))
        a.box((.592,y,5.23),(.03,.32,.28),'light',rot=(0,-.25,0))
    a.cylinder((.32,-.20,1.4),(.32,-.3,1.4),.12,'dark_metal',10)
    a.tube([(.32,-.31,1.4),(.32,-.42,1.4),(.47,-.42,1.4)],.022,'metal')


def skid(a,l=2,w=1.2):
    for y in (-w*.4,w*.4):
        a.box((0,y,.10),(l,.13,.20),'dark_metal')
        for x in (-l*.42,l*.42):a.box((x,y,.045),(.23,.30,.07),'dark_metal')
    for x in (-l*.42,l*.42):a.box((x,0,.23),(.10,w,.12),'dark_metal')


@asset('diesel_dewatering_pump_skid','person')
def dewater_pump(a):
    skid(a,1.84,1.04)
    a.box((-.38,0,.55),(.83,.62,.51),'green')
    a.cylinder((-.90,0,.62),(-.79,0,.62),.28,'dark_metal',10)
    grille(a,-.92,0,.62,.36,.36)
    a.cylinder((.23,0,.6),(.53,0,.6),.34,'metal',12)
    a.cylinder((.52,0,.6),(.86,0,.6),.17,'metal',10)
    a.cylinder((.85,0,.6),(.91,0,.6),.215,'steel',10)
    a.cylinder((.38,0,.72),(.38,0,1.02),.14,'metal',10)
    a.cylinder((.38,0,1.02),(.38,0,1.07),.19,'steel',10)
    a.cylinder((-.51,.21,.78),(-.51,.21,1.25),.047,'dark_metal',8)
    for x in (-.82,.78):a.tube([(x,-.51,.24),(x,-.51,1.22),(x,.51,1.22),(x,.51,.24)],.035,'dark_metal')
    a.box((-.35,-.323,.63),(.34,.025,.23),'dark_metal')
    a.cylinder((-.4,-.34,.65),(-.4,-.36,.65),.069,'white',10)


@asset('water_storage_tank_skid')
def water_skid(a):
    skid(a,3.2,1.58)
    for x in (-1.02,1.02):a.box((x,0,.48),(.26,1.45,.42),'dark_metal')
    a.cylinder((-1.26,0,1.17),(1.26,0,1.17),.78,'cream',16)
    a.cylinder((-1.4,0,1.17),(-1.26,0,1.17),.67,'cream',16,radius2=.78)
    a.cylinder((1.26,0,1.17),(1.4,0,1.17),.78,'cream',16,radius2=.67)
    for x in (-.91,.91):a.torus((x,0,1.17),.787,.027,'metal',axis='x',segments=16,sides=5)
    a.cylinder((0,0,1.91),(0,0,2.05),.20,'dark_metal',10)
    a.cylinder((0,0,2.05),(0,0,2.09),.24,'metal',10)
    a.tube([(1.41,0,.65),(1.63,0,.65),(1.63,0,.36)],.09,'metal',8)
    a.torus((1.64,-.1,.58),.11,.019,'red',axis='y',segments=8,sides=5)
    a.box((-.42,-.782,1.30),(.73,.025,.29),'blue')


@asset('trailer_concrete_line_pump')
def concrete_pump(a):
    trailer(a,3.04,1.50,.53,.35)
    hood(a,(.20,0,1.06),(2.07,1.29,.91),'yellow')
    grille(a,1.25,0,.95,.88,.33)
    # Open aggregate hopper with grate and visible feed chamber.
    a.box((-1.26,0,.92),(.74,1.40,.16),'dark_metal')
    for y in (-.64,.64):a.box((-1.26,y,1.19),(.95,.08,.60),'yellow',rot=(.16 if y<0 else -.16,0,0))
    for x in (-1.73,-.81):a.box((x,0,1.19),(.07,1.34,.60),'yellow')
    for y in (-.46,-.23,0,.23,.46):a.box((-1.26,y,1.53),(.93,.033,.035),'metal')
    for y in (-.40,.40):a.cylinder((-.75,y,.70),(.75,y,.70),.13,'metal',10)
    a.tube([(-1.43,0,.76),(-1.89,0,.76),(-2.05,0,.51),(-2.36,0,.51)],.13,'dark_metal',10)
    a.cylinder((-2.41,0,.51),(-2.33,0,.51),.18,'metal',10)
    for x in (-1.3,1.04):
        for y in (-.92,.92):a.cylinder((x,y,.10),(x,y,.76),.046,'metal',8)


@asset('twin_tank_grout_injection_skid')
def grout_skid(a):
    skid(a,2.20,1.25)
    for x,r,h in [(-.54,.39,1.18),(.41,.30,.97)]:
        a.cylinder((x,0,.43),(x,0,h),r,'green',12)
        a.cone((x,0,.47),(x,0,.24),r,'green',12)
        a.cylinder((x,0,h),(x,0,h+.07),r*1.06,'metal',12)
        a.box((x,0,h+.10),(r*2,.15,.1),'dark_metal')
        a.cylinder((x,0,h+.14),(x,0,h+.37),.11,'dark_metal',8)
        for yy in (-.28,.28):a.beam((x,yy,.30),(x,yy,.74),.045,mat='dark_metal')
    a.box((.83,0,.50),(.37,.57,.34),'blue')
    a.cylinder((.75,0,.48),(1.17,0,.48),.10,'metal',8)
    a.tube([(-.5,-.40,.65),(-.5,-.57,.65),(.85,-.57,.65),(.85,-.3,.46)],.045,'dark_metal')
    a.cylinder((.1,-.58,.73),(.1,-.58,.94),.025,'metal',6)
    a.cylinder((.1,-.59,.95),(.1,-.65,.95),.08,'white',10)


@asset('asphalt_patch_kettle_trailer')
def asphalt_kettle(a):
    trailer(a,2.73,1.45,.57,.34)
    a.cylinder((-.76,0,1.16),(.80,0,1.16),.64,'green',12)
    for x in (-.77,.80):a.cylinder((x-.03,0,1.16),(x+.03,0,1.16),.67,'dark_metal',12)
    for x in (-.69,.72):a.box((x,0,.61),(.13,1.0,.26),'dark_metal')
    a.cylinder((-.13,0,1.77),(-.13,0,1.85),.27,'dark_metal',10)
    a.box((-.13,0,1.91),(.28,.06,.06),'metal')
    a.cylinder((.61,.27,1.63),(.61,.27,2.23),.07,'dark_metal',8)
    a.cylinder((.61,.27,2.23),(.61,.27,2.29),.12,'metal',8)
    a.box((-.98,0,.82),(.45,.68,.36),'dark_metal')
    a.cylinder((-.93,0,.83),(-1.25,0,.83),.15,'metal',10)
    a.tube([(.64,-.52,1.0),(1.08,-.52,1.0),(1.08,-.52,.57)],.07,'metal')
    a.torus((1.08,-.60,.91),.13,.02,'red',axis='y',segments=8,sides=5)


@asset('rack_and_pinion_material_hoist')
def material_hoist(a):
    a.box((0,0,.14),(2.40,2.16,.28),'concrete')
    lattice(a,(-.67,.44,.27),(-.67,.44,6.1),.43,9,'dark_metal')
    for z in (.9,2.6,4.3,6):a.beam((-.67,.45,z),(-.67,1.0,z),.08,mat='metal')
    a.box((.22,-.12,1.74),(1.90,1.73,.17),'dark_metal')
    # Open cage floor with closely spaced bars, sliding gate and mast roller blocks.
    for x in (-.68,1.12):
        for y in (-.96,.71):a.beam((x,y,1.83),(x,y,3.87),.055,mat='orange')
    for y in (-.96,.71):
        for z in (2.03,2.85,3.8):a.beam((-.68,y,z),(1.12,y,z),.045,mat='orange')
        for i in range(9):a.beam((-.59+i*.2,y,2.04),(-.59+i*.2,y,3.79),.025,mat='metal')
    for z in (2.02,2.89,3.8):a.beam((1.12,-.96,z),(1.12,.71,z),.045,mat='orange')
    for y in (-.74,-.5,-.26,-.02,.22,.46):a.beam((1.12,y,2.05),(1.12,y,3.78),.025,mat='metal')
    a.box((.20,-.12,3.9),(1.95,1.8,.08),'orange')
    a.box((-.87,.20,2.48),(.31,.45,.56),'blue')
    a.box((.53,-1.02,2.83),(.22,.09,.25),'dark_metal')


@asset('rolling_scaffold_tower')
def rolling_scaffold(a):
    for x in (-1.05,1.05):
        for y in (-.64,.64):
            wheel(a,x,y,.115,.115,.07,'metal')
            a.beam((x,y,.19),(x,y,3.23),.042,mat='metal')
            a.box((x,y,.3),(.13,.11,.13),'dark_metal')
    for z in (.45,1.30,2.24):
        for x in (-1.05,1.05):a.beam((x,-.64,z),(x,.64,z),.04,mat='metal')
    for y in (-.64,.64):
        a.beam((-1.05,y,.5),(1.05,y,2.24),.031,mat='metal')
        a.beam((1.05,y,.5),(-1.05,y,2.24),.031,mat='metal')
        railing(a,-1.05,1.05,y,2.25,.97)
        a.box((0,y,2.38),(2.10,.045,.22),'wood')
    for y in (-.43,-.14,.14,.43):a.box((0,y,2.24),(2.14,.27,.09),'wood_light')
    for x in (-1.05,1.05):
        for z in (2.72,3.23):a.beam((x,-.64,z),(x,.64,z),.04,mat='metal')
    ladder(a,-1.085,0,.38,2.22,.50,.26)


@asset('mason_frame_scaffold_bay')
def scaffold_bay(a):
    for x in (-1.51,1.51):
        for y in (-.63,.63):
            a.box((x,y,.045),(.27,.27,.09),'dark_metal')
            a.cylinder((x,y,.08),(x,y,.36),.035,'steel',8)
            a.cylinder((x,y,.29),(x,y,2.92),.03,'metal',6)
        for z in (.58,1.17,1.78,2.33):a.cylinder((x,-.63,z),(x,.63,z),.027,'metal',6)
    for y in (-.63,.63):
        a.beam((-1.51,y,.52),(1.51,y,2.13),.035,mat='metal')
        a.beam((1.51,y,.52),(-1.51,y,2.13),.035,mat='metal')
        for z in (2.48,2.92):a.cylinder((-1.51,y,z),(1.51,y,z),.026,'metal',6)
        a.box((0,y,2.09),(3.08,.035,.20),'wood')
    for y in (-.46,-.15,.15,.46):a.box((0,y,1.99),(3.16,.29,.065),'wood_light')


@asset('scaffold_access_stair_tower')
def scaffold_stairs(a):
    l=2.7;w=1.4
    for x in (-l/2,l/2):
        for y in (-w/2,w/2):
            a.box((x,y,.04),(.3,.3,.08),'dark_metal')
            a.beam((x,y,.08),(x,y,3.37),.055,mat='metal')
    for y in (-w/2,w/2):
        a.beam((-1.35,y,.11),(1.35,y,2.38),.10,.17,'dark_metal')
        a.beam((-1.35,y,.96),(1.35,y,3.23),.035,mat='metal')
        a.beam((-1.35,y,.55),(1.35,y,2.82),.028,mat='metal')
    for i in range(11):
        x=-1.24+i*.246;z=.19+i*.208
        a.box((x,0,z),(.29,1.29,.07),'metal')
        for y in (-w/2,w/2):
            if i%3==0:a.beam((x,y,z),(x,y,z+.92),.03,mat='metal')
    a.box((1.61,0,2.35),(.55,1.45,.11),'metal')
    for y in (-.7,.7):railing(a,1.34,1.87,y,2.41,.96)
    a.beam((1.85,-.7,3.36),(1.85,.7,3.36),.04,mat='metal')
    for x in (-1.35,1.35):
        a.beam((x,-.70,.32),(x,.70,2.33),.03,mat='metal')
        a.beam((x,.70,.32),(x,-.70,2.33),.03,mat='metal')


@asset('steel_trench_shoring_box')
def trench_box(a):
    for y in (-1.03,1.03):
        a.box((0,y,1.25),(3.8,.16,2.50),'yellow')
        for x in (-1.77,-.88,0,.88,1.77):a.box((x,y+(.12 if y>0 else -.12),1.28),(.13,.12,2.38),'dark_metal')
        for z in (.12,2.40):a.box((0,y+(.12 if y>0 else -.12),z),(3.85,.16,.16),'dark_metal')
        for x in (-1.3,1.3):a.torus((x,y,2.57),.13,.037,'metal',axis='y',segments=8,sides=5)
    for x in (-1.41,1.41):
        for z in (.51,1.91):
            a.cylinder((x,-1.03,z),(x,1.03,z),.115,'metal',10)
            for y in (-.89,.89):a.box((x,y,z),(.36,.20,.37),'dark_metal')


@asset('hydraulic_trench_shore_assembly')
def trench_shore(a):
    for y in (-.84,.84):
        a.box((0,y,1.21),(.57,.19,2.42),'metal')
        for x in (-.23,.23):a.box((x,y+(.13 if y>0 else -.13),1.21),(.08,.16,2.40),'dark_metal')
        a.box((0,y,2.42),(.68,.27,.08),'metal')
    for z in (.51,1.78):
        a.cylinder((0,-.73,z),(0,.16,z),.105,'blue',10)
        a.cylinder((0,.15,z),(0,.78,z),.058,'steel',8)
        a.cylinder((0,-.10,z),(0,.02,z),.135,'dark_metal',10)
        a.tube([(.10,-.58,z),(.22,-.59,z),(.22,-.57,z+.16)],.024,'black')
    a.tube([(.22,-.57,.67),(.28,-.63,1.35),(.22,-.57,1.94)],.022,'black')
    for y in (-.84,.84):a.torus((0,y,2.49),.08,.025,'metal',axis='y',segments=8,sides=5)


@asset('circular_foundation_rebar_cage')
def rebar_cage(a):
    for i in range(12):
        th=2*pi*i/12;x=.65*cos(th);y=.65*sin(th)
        a.cylinder((x,y,.05),(x,y,3.3),.023,'brown',6)
        a.beam((x,y,3.3),(x*.87,y*.87,3.52),.035,mat='brown')
    for z in (.12,.45,.8,1.15,1.5,1.85,2.2,2.55,2.9,3.23):a.torus((0,0,z),.65,.02,'dark_metal',segments=12,sides=5)
    for x in (-.50,.50):a.box((x,0,.05),(.14,1.64,.10),'wood')


@asset('braced_wall_formwork_panels')
def wall_formwork(a):
    for i in range(3):
        x=-1.2+i*1.2
        a.box((x,0,1.50),(1.17,.065,3.0),'wood')
        for xx in (x-.59,x+.59):a.box((xx,-.07,1.50),(.065,.14,3.04),'dark_metal')
        for z in (.05,.76,1.5,2.24,2.97):a.box((x,-.08,z),(1.17,.13,.055),'dark_metal')
    for x in (-1.15,1.15):
        a.beam((x,-.11,2.28),(x,-1.6,.11),.075,mat='blue')
        a.beam((x,-.11,.69),(x,-1.6,.11),.065,mat='metal')
        a.box((x,-1.6,.055),(.37,.31,.11),'dark_metal')
        for z in (.74,2.23):
            a.cylinder((x,-.25,z),(x,.13,z),.025,'steel',6)
            a.box((x,-.23,z),(.25,.055,.11),'metal',rot=(0,.23,0))
    for x in (-1.64,1.64):a.torus((x,-.07,3.12),.12,.03,'metal',axis='y',segments=8,sides=5)


@asset('adjustable_steel_shoring_tripod','person')
def shoring_prop(a):
    a.box((0,0,.045),(.29,.29,.09),'dark_metal')
    a.cylinder((0,0,.07),(0,0,1.52),.057,'green',8)
    a.cylinder((0,0,1.50),(0,0,2.6),.040,'steel',8)
    a.cylinder((0,0,1.25),(0,0,1.51),.08,'dark_metal',8)
    for z in (1.27,1.33,1.39,1.45):a.torus((0,0,z),.071,.009,'steel',segments=8,sides=4)
    a.beam((-.22,0,1.37),(.22,0,1.37),.025,mat='metal')
    for i in range(3):
        th=i*2*pi/3
        a.beam((0,0,.88),(.58*cos(th),.58*sin(th),.06),.04,mat='green')
        a.box((.58*cos(th),.58*sin(th),.04),(.15,.12,.06),'dark_metal')
    a.box((0,0,2.62),(.32,.28,.08),'dark_metal')
    for y in (-.15,.15):a.box((0,y,2.72),(.32,.045,.20),'dark_metal')
    for z in (1.75,1.93,2.11,2.29,2.47):a.cylinder((-.043,0,z),(-.049,0,z),.013,'black',6)


@asset('heavy_steel_shoring_trestle')
def shoring_trestle(a):
    for x in (-1.12,1.12):
        for y in (-.72,.72):
            a.box((x,y,.06),(.45,.4,.12),'dark_metal')
            a.beam((x,y,.12),(x,y*.60,1.79),.15,.12,'metal')
        a.beam((x,-.7,.3),(x,.41,1.66),.065,mat='dark_metal')
        a.beam((x,.7,.3),(x,-.41,1.66),.065,mat='dark_metal')
        a.box((x,0,1.79),(.26,1.31,.12),'dark_metal')
    a.box((0,0,1.98),(3.08,.11,.36),'metal')
    for z in (1.80,2.16):a.box((0,0,z),(3.14,.48,.08),'metal')
    for y in (-.39,.39):a.beam((-1.12,y,.44),(1.12,y,1.70),.06,mat='dark_metal')


@asset('masonry_cutoff_saw_bench','person')
def masonry_saw(a):
    for x in (-.67,.67):
        for y in (-.39,.39):a.beam((x,y,.07),(x*.88,y*.88,.90),.055,mat='dark_metal')
    a.box((0,0,.90),(1.55,.96,.11),'green')
    a.box((.17,0,.98),(.86,.71,.05),'metal')
    for y in (-.30,.30):a.box((.12,y,1.02),(1.18,.028,.035),'dark_metal')
    a.box((-.58,.26,1.22),(.17,.15,.55),'green')
    a.beam((-.55,.26,1.44),(.10,.26,1.39),.10,mat='green')
    a.cylinder((.09,.15,1.32),(.09,.30,1.32),.32,'dark_metal',16)
    a.cylinder((.09,.135,1.31),(.09,.15,1.31),.282,'steel',16)
    a.cylinder((.09,.10,1.31),(.09,.14,1.31),.059,'dark_metal',8)
    a.box((-.22,.53,1.36),(.39,.29,.26),'dark_metal')
    a.tube([(-.28,.21,1.45),(-.21,.05,1.61),(.30,.05,1.61)],.028,'black')
    a.box((.49,0,1.035),(.045,.66,.09),'metal')
    a.tube([(-.59,.34,1.29),(-.58,.41,.91),(-.15,.41,.91)],.016,'blue')


@asset('bridge_style_wet_tile_saw','person')
def wet_tile_saw(a):
    for x in (-.67,.67):
        for y in (-.35,.35):a.beam((x,y,.04),(x*.84,y*.84,.83),.045,mat='metal')
    a.box((0,0,.81),(1.62,.91,.14),'blue')
    a.box((0,0,.91),(1.46,.75,.04),'dark_metal')
    for x in (-.44,0,.44):a.box((x,0,.944),(.40,.70,.025),'metal')
    for x in (-.72,.72):a.box((x,.26,1.14),(.07,.08,.51),'blue')
    a.box((0,.26,1.40),(1.55,.09,.12),'metal')
    a.box((.15,.26,1.38),(.28,.19,.18),'blue')
    a.cylinder((.15,.11,1.16),(.15,.20,1.16),.23,'blue',14)
    a.cylinder((.15,.098,1.14),(.15,.11,1.14),.205,'steel',14)
    a.box((.14,.40,1.28),(.32,.28,.23),'dark_metal')
    a.tube([(.20,.18,1.49),(.40,.18,1.49),(.47,.06,1.36)],.025,'black')
    a.box((-.53,0,.987),(.04,.73,.07),'yellow')
    a.tube([(.24,.34,1.3),(.43,.46,1.3),(.64,.46,.76)],.017,'black')


@asset('pipe_threading_machine_stand','person')
def pipe_threader(a):
    for x in (-.51,.51):
        for y in (-.33,.33):a.beam((x,y,.03),(x*.67,y*.67,.87),.05,mat='dark_metal')
    a.box((0,0,.86),(1.03,.62,.12),'dark_metal')
    a.box((-.18,0,1.03),(.55,.53,.30),'red')
    a.cylinder((-.50,0,1.22),(.14,0,1.22),.235,'dark_metal',12)
    a.cylinder((.12,0,1.22),(.21,0,1.22),.266,'metal',10)
    a.cylinder((.215,0,1.22),(.223,0,1.22),.13,'black',10)
    for i in range(3):
        t=i*2*pi/3;a.box((.245,.15*cos(t),1.22+.15*sin(t)),(.07,.10,.10),'steel',rot=(t,0,0))
    for y in (-.25,.25):a.cylinder((-.12,y,1.04),(.69,y,1.04),.026,'steel',8)
    a.box((.46,0,1.09),(.25,.62,.09),'metal')
    a.torus((.45,0,1.25),.18,.036,'dark_metal',axis='x',segments=10,sides=5)
    a.beam((.44,.15,1.42),(.44,.27,1.72),.035,mat='metal')
    a.box((.44,.28,1.73),(.10,.06,.14),'black')
    a.box((.18,0,.56),(.73,.57,.11),'metal')
    a.tube([(-.31,-.27,1.03),(-.70,-.49,.52),(-.59,-.53,.05),(-.24,-.52,.05)],.012,'black')
    a.box((-.18,-.52,.06),(.26,.16,.08),'black')


@asset('electric_rebar_bending_table','person')
def rebar_bender(a):
    for x in (-.43,.43):
        for y in (-.37,.37):a.box((x,y,.13),(.13,.12,.26),'dark_metal')
    chamfer(a,(0,0,.60),(1.05,.92,.87),'green',.055)
    a.box((0,0,1.055),(1.14,1.0,.07),'metal')
    a.cylinder((.1,0,1.09),(.1,0,1.13),.30,'dark_metal',16)
    for x,y,r in [(.10,0,.052),(.27,.15,.049),(-.07,-.15,.045),(-.39,.17,.05)]:a.cylinder((x,y,1.13),(x,y,1.26),r,'steel',8)
    for y in (-.35,.35):a.box((-.11,y,1.11),(.69,.055,.07),'dark_metal')
    a.tube([(-1.02,.07,1.23),(.10,.07,1.23),(.12,.56,1.23)],.026,'brown',6)
    a.box((.27,-.473,.75),(.37,.045,.25),'dark_metal')
    for x,m in [(.17,'green'),(.34,'red')]:a.cylinder((x,-.50,.76),(x,-.52,.76),.037,m,8)
    grille(a,-.537,0,.51,.56,.36)
    a.tube([(.41,-.47,.49),(.67,-.60,.23),(.66,-.64,.05)],.014,'black')
    a.box((.66,-.66,.05),(.25,.18,.09),'black')


@asset('heavy_jobsite_gang_box','person')
def gang_box(a):
    for x in (-.57,.57):a.box((x,0,.10),(.20,.71,.20),'dark_metal')
    chamfer(a,(0,0,.60),(1.53,.77,.92),'green',.035)
    a.box((0,0,1.10),(1.61,.85,.11),'dark_metal')
    a.box((0,0,1.16),(1.56,.81,.035),'green')
    for x in (-.55,.55):
        a.box((x,-.40,.99),(.18,.045,.21),'dark_metal')
        a.box((x,-.425,1.0),(.08,.035,.06),'metal')
        a.cylinder((x,.397,1.06),(x+.19,.397,1.06),.032,'metal',8)
    for x in (-.795,.795):a.tube([(x,-.16,.71),(x*1.035,-.16,.79),(x*1.035,.16,.79),(x,.16,.71)],.025,'dark_metal')
    a.box((0,-.395,.60),(.29,.018,.12),'cream')


@asset('jobsite_office_trailer')
def office_trailer(a):
    # American eight-foot-wide portable office on a tandem chassis.
    for y in (-.94,.94):a.box((0,y,.53),(6.6,.14,.20),'dark_metal')
    wheels(a,[-1.02,-.12],1.13,.38,.38,.23)
    a.box((0,0,1.97),(6.60,2.44,2.64),'cream')
    a.box((0,0,3.35),(6.79,2.60,.14),'white')
    for x in (-3.25,3.25):
        for y in (-1.23,1.23):a.box((x,y,1.98),(.08,.045,2.65),'metal')
    for z in (1.04,1.31,1.58,1.85,2.12,2.39,2.66,2.93,3.20):
        for y in (-1.228,1.228):a.box((0,y,z),(6.53,.02,.025),'sand')
    # Inset windows and opening-specific trim.
    for x in (-1.81,.13):
        a.box((x,-1.252,2.29),(1.33,.05,.93),'white')
        a.box((x,-1.285,2.29),(1.18,.025,.79),'glass')
        a.box((x,-1.308,2.29),(.045,.018,.80),'metal')
        a.box((x,-1.309,2.29),(1.18,.018,.035),'metal')
    a.box((2.29,-1.257,1.79),(.91,.06,2.2),'white')
    a.box((2.29,-1.296,1.83),(.76,.035,1.99),'metal')
    a.box((2.29,-1.321,2.21),(.58,.015,.63),'glass')
    a.box((2.54,-1.34,1.62),(.12,.04,.036),'dark_metal')
    for i in range(3):a.box((2.29,-1.42-i*.29,.54-i*.16),(.99,.31,.13),'metal')
    for x in (1.78,2.8):a.tube([(x,-2.0,.12),(x,-2.0,.87),(x,-1.29,1.23)],.026,'metal')
    a.box((-3.41,0,2.13),(.25,.79,.75),'concrete')
    grille(a,-3.55,0,2.10,.58,.50)
    for x in (-2.54,2.59):
        for y in (-1.05,1.05):a.cylinder((x,y,.05),(x,y,.65),.055,'metal',8)
    for y in (-.8,.8):a.beam((3.3,y,.53),(4.22,0,.53),.12,mat='dark_metal')
    a.box((4.29,0,.53),(.31,.19,.13),'metal')


@asset('portable_cement_storage_silo')
def cement_silo(a):
    for x in (-1.0,1.0):
        for y in (-1.0,1.0):
            a.box((x,y,.07),(.39,.39,.14),'dark_metal')
            a.beam((x,y,.14),(x,y,2.85),.11,mat='metal')
    for y in (-1.,1.):
        a.beam((-1.,y,.38),(1.,y,2.48),.06,mat='metal')
        a.beam((1.,y,.38),(-1.,y,2.48),.06,mat='metal')
    a.cylinder((0,0,2.50),(0,0,4.46),1.12,'cream',16)
    a.cylinder((0,0,1.30),(0,0,2.51),.20,'cream',16,radius2=1.12)
    a.cylinder((0,0,4.46),(0,0,4.57),1.15,'metal',16)
    a.cylinder((0,0,4.57),(0,0,4.86),.20,'dark_metal',10)
    a.cylinder((0,0,1.05),(0,0,1.33),.18,'dark_metal',10)
    a.box((0,0,1.05),(.49,.42,.10),'metal')
    a.tube([(.18,0,1.08),(.50,0,1.08),(.50,0,.93)],.075,'dark_metal',8)
    ladder(a,1.17,0,.32,4.88,.43,.28)
    for z in (2.51,3.2,3.91):a.torus((1.14,0,z),.43,.021,'metal',axis='z',segments=10,sides=5,arc=pi)
    for y in (-.43,.43):a.cylinder((1.15,y,2.5),(1.15,y,4.05),.022,'metal',6)
    a.box((-.015,-1.135,3.48),(.91,.023,.38),'green')


@asset('aggregate_feed_hopper')
def aggregate_hopper(a):
    for x in (-1.1,1.1):
        for y in (-.79,.79):
            a.box((x,y,.06),(.36,.32,.12),'dark_metal')
            a.beam((x,y,.1),(x,y,1.83),.11,mat='dark_metal')
    # Hollow hopper: each trapezoidal side wall has its own steel thickness.
    wall_faces=[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    for y in (-1,1):
        a.mesh([(-1.42,y*1.03,2.68),(1.42,y*1.03,2.68),(.42,y*.30,1.37),(-.42,y*.30,1.37),
                (-1.42,y*1.00,2.65),(1.42,y*1.00,2.65),(.42,y*.27,1.37),(-.42,y*.27,1.37)],
               [tuple(reversed(f)) for f in wall_faces] if y<0 else wall_faces,'green')
    for x in (-1,1):
        a.mesh([(x*1.42,-1.03,2.68),(x*1.42,1.03,2.68),(x*.42,.30,1.37),(x*.42,-.30,1.37),
                (x*1.39,-1.0,2.65),(x*1.39,1.,2.65),(x*.39,.30,1.37),(x*.39,-.30,1.37)],
               [tuple(reversed(f)) for f in wall_faces] if x>0 else wall_faces,'green')
    for y in (-1.02,1.02):a.box((0,y,2.69),(2.92,.11,.11),'dark_metal')
    for x in (-1.43,1.43):a.box((x,0,2.69),(.11,2.10,.11),'dark_metal')
    for x in (-.8,0,.8):a.box((x,0,2.69),(.055,2.06,.045),'metal')
    a.box((0,0,1.29),(1.0,.79,.15),'dark_metal')
    a.box((.17,0,1.21),(1.15,.70,.06),'metal')
    a.beam((.66,0,1.26),(1.15,0,1.09),.05,mat='metal')
    for y in (-.79,.79):a.beam((-1.1,y,.31),(1.1,y,1.78),.045,mat='metal')


@asset('crane_concrete_pouring_bucket')
def concrete_bucket(a):
    for x in (-.60,.60):
        for y in (-.60,.60):
            a.beam((x,y,.06),(x,y,.91),.065,mat='dark_metal')
            a.box((x,y,.04),(.20,.20,.08),'dark_metal')
    a.cylinder((0,0,.45),(0,0,1.10),.20,'yellow',12,radius2=.78,cap=False)
    a.cylinder((0,0,1.10),(0,0,1.84),.78,'yellow',12,cap=False)
    a.cylinder((0,0,1.16),(0,0,1.82),.735,'dark_metal',12,cap=False)
    a.torus((0,0,1.84),.76,.043,'dark_metal',segments=12,sides=5)
    for y in (-.63,.63):a.beam((0,y,1.56),(0,y,2.30),.08,mat='dark_metal')
    a.beam((0,-.63,2.30),(0,.63,2.30),.1,mat='dark_metal')
    a.torus((0,0,2.44),.15,.045,'metal',axis='y',segments=10,sides=5)
    a.box((0,0,.40),(.58,.54,.12),'dark_metal')
    a.box((0,-.34,.39),(.11,.58,.06),'metal')
    a.beam((.21,-.53,.40),(.21,-.87,1.17),.035,mat='metal')
    a.cylinder((.15,-.87,1.17),(.43,-.87,1.17),.035,'black',8)
    for z in (.88,1.19,1.5):a.box((-.80,0,z),(.14,.37,.04),'metal')


@asset('mobile_inclined_belt_conveyor')
def belt_conveyor(a):
    wheels(a,[-.17],.73,.34,.34,.19)
    a.box((-.17,0,.47),(.17,1.5,.13),'dark_metal')
    p=(-2.0,0,.52);q=(2.45,0,2.42)
    a.beam(p,q,.73,.10,'black')
    for y in (-.44,.44):
        a.beam((p[0],y,p[2]),(q[0],y,q[2]),.09,.20,'green')
        a.beam((-.17,y,.48),(.80,y,1.76),.07,mat='metal')
        a.beam((-.17,y,.48),(-1.30,y,.79),.055,mat='metal')
    for i in range(13):
        t=i/12;x=-2+4.45*t;z=.52+1.90*t
        a.cylinder((x,-.44,z-.08),(x,.44,z-.08),.09,'metal',8)
        a.box((x,0,z+.09),(.055,.70,.07),'dark_metal',rot=(0,-.40,0))
    for y in (-.45,.45):a.box((-1.65,y,.80),(.8,.10,.42),'green',rot=(.23 if y<0 else -.23,0,-.0))
    a.box((-2.02,0,.69),(.07,.83,.35),'green')
    a.cylinder((2.33,.48,2.35),(2.33,.79,2.35),.19,'dark_metal',10)
    a.box((2.28,.82,2.35),(.42,.15,.38),'green')
    a.cylinder((.07,-.54,.96),(.07,-.64,.96),.15,'dark_metal',10)
    a.beam((.07,-.65,.96),(.21,-.65,.98),.025,mat='metal')
