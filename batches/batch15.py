"""Fifty municipal, commercial and emergency fleet vehicles.

Purpose-built working bodies, chassis, glazed cabs and mounted equipment.
Dimensions are metres; +X is forward. No external models or textures.
"""
from assetlib import Asset, register
import math

CAT = 'municipal_commercial_emergency_vehicles'


def _triangulate(poly):
    ids = list(range(len(poly)))
    area = sum(poly[i][0]*poly[(i+1)%len(poly)][1] - poly[(i+1)%len(poly)][0]*poly[i][1] for i in ids)
    if area < 0:
        ids.reverse()
    def turn(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def inside(p, a, b, c):
        return turn(a,b,p) >= -1e-10 and turn(b,c,p) >= -1e-10 and turn(c,a,p) >= -1e-10
    tris = []
    while len(ids) > 3:
        for j, b in enumerate(ids):
            aa, cc = ids[j-1], ids[(j+1)%len(ids)]
            if turn(poly[aa], poly[b], poly[cc]) <= 1e-10:
                continue
            if any(inside(poly[k],poly[aa],poly[b],poly[cc]) for k in ids if k not in (aa,b,cc)):
                continue
            tris.append((aa,b,cc)); ids.pop(j)
            break
        else:
            raise ValueError('Untriangulable fleet profile')
    tris.append(tuple(ids))
    return tris


def _profile(a, poly, width, mat='white', y=0):
    """Closed extrusion of a side silhouette, including real wheel openings."""
    n=len(poly)
    vs=[(x,y+s*width/2,z) for s in (-1,1) for x,z in poly]
    ts=_triangulate(poly)
    fs=list(ts)+[tuple(i+n for i in reversed(t)) for t in ts]
    fs += [(i,i+n,(i+1)%n+n,(i+1)%n) for i in range(n)]
    a.mesh(vs,fs,mat)


def _pane(a, points, mat='glass', reverse=False):
    face=tuple(range(len(points)))
    a.mesh(points,[tuple(reversed(face)) if reverse else face],mat)


def _wheel(a, x, y, r=.48, width=.25, outer=True):
    """Bevelled twelve-sided truck tyre with separate rim and lug hardware."""
    vs=[]
    rings=[(-width/2,.86),(-width*.32,1),(width*.32,1),(width/2,.86)]
    for yy,rr in rings:
        for j in range(12):
            t=2*math.pi*j/12
            vs.append((x+r*rr*math.cos(t),y+yy,r+r*rr*math.sin(t)))
    fs=[]
    # Cross sections are clockwise when viewed along +Y.
    for k in range(3):
        for j in range(12):
            q=(j+1)%12
            fs.append((k*12+j,(k+1)*12+j,(k+1)*12+q,k*12+q))
    fs += [tuple(range(12)),tuple(reversed(range(36,48)))]
    a.mesh(vs,fs,'rubber')
    if outer:
        s=1 if y>0 else -1
        yy=y+s*(width/2+.006)
        a.cylinder((x,yy-s*.025,r),(x,yy+s*.022,r),r*.57,'silver',sides=10)
        a.cylinder((x,yy,r),(x,yy+s*.06,r),r*.25,'dark_metal',sides=8)
        for j in range(5):
            t=2*math.pi*j/5
            a.box((x+r*.35*math.cos(t),yy+s*.025,r+r*.35*math.sin(t)),(.035,.035,.035),'steel')


def _chassis(a,L,W,axles,r=.48,dual=True):
    for y in (-W*.25,W*.25):
        a.box((-.05,y,.60),(L-.35,.15,.24),'dark_metal')
    for x in (-L*.34,0,L*.33):
        a.box((x,0,.58),(.16,W*.57,.15),'metal')
    for ix,x in enumerate(axles):
        a.cylinder((x,-W*.46,r),(x,W*.46,r),.075,'dark_metal',sides=8)
        a.sphere((x,0,r),.18,'dark_metal',segments=8,rings=3,scale=(.24,.26,.19))
        for s in (-1,1):
            _wheel(a,x,s*(W/2-.045),r,.26,True)
            if dual and ix>0:
                _wheel(a,x,s*(W/2-.355),r,.25,False)
            a.box((x,s*W*.25,r+.13),(.78,.10,.065),'black')
    a.box((-L/2-.05,0,.61),(.16,W*.93,.16),'dark_metal')
    for s in (-1,1):
        a.box((-L/2-.14,s*W*.37,.88),(.04,.22,.12),'red')
        a.box((-L/2+.23,s*(W/2-.06),.57),(.15,.035,.31),'rubber')
    a.box((-L/2-.14,0,.72),(.026,.39,.16),'white')


def _archpoly(lo,hi,floor,axles,r,top):
    p=[(lo,floor)]
    ar=r+.065
    for x in sorted(axles):
        if x-ar>lo and x+ar<hi:
            p.append((x-ar,floor))
            for j in range(7):
                t=math.pi-j*math.pi/6
                p.append((x+ar*math.cos(t),r+ar*math.sin(t)))
            p.append((x+ar,floor))
    p.append((hi,floor))
    p.extend(top)
    return p


def _cab(a,front,W,paint='white',hood=True,crew=False,r=.48):
    length=(3.65 if crew else 3.1) if hood else (2.85 if crew else 2.05)
    rear=front-length
    axle=front-(.97 if hood else .89)
    belt=1.56 if hood else 1.65
    h=2.66 if hood else 2.88
    if hood:
        top=[(front,1.27),(front-.18,1.49),(front-1.32,1.61),(front-1.52,1.57),(rear,1.57)]
        windshield=front-1.35; roofedge=front-1.66
    else:
        top=[(front,1.48),(front-.04,belt),(rear,belt)]
        windshield=front-.035; roofedge=front-.30
    _profile(a,_archpoly(rear,front,.56,[axle],r,top),W,paint)
    # Tapered cab roof, sloped front glass and separate side panes.
    rr=rear+.10; rf=roofedge; yb=W/2; yt=W*.46
    a.mesh([(rear,-yb,belt),(windshield,-yb,belt),(windshield,yb,belt),(rear,yb,belt),
            (rr,-yt,h),(rf,-yt,h),(rf,yt,h),(rr,yt,h)],
           [(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],paint)
    zlo=belt+.12; zhi=h-.11
    tl=(zlo-belt)/(h-belt); th=(zhi-belt)/(h-belt)
    xb=windshield+(rf-windshield)*tl+.012
    xt=windshield+(rf-windshield)*th+.012
    yl=yb+(yt-yb)*tl-.09; yh=yb+(yt-yb)*th-.09
    for s in (-1,1):
        _pane(a,[(xb,s*.025,zlo),(xb,s*yl,zlo),(xt,s*yh,zhi),(xt,s*.025,zhi)],reverse=s<0)
        pane_count=2 if crew else 1
        xlo=rear+.14; xhi=windshield-.12
        for j in range(pane_count):
            lo=xlo+(xhi-xlo)*j/pane_count+.035
            hi=xlo+(xhi-xlo)*(j+1)/pane_count-.035
            hit=min(hi-.12,rf-.10)
            _pane(a,[(lo,s*(yb-.012),zlo),(hi,s*(yb-.012),zlo),(hit,s*(yt+.012),zhi),(lo+.045,s*(yt+.012),zhi)],reverse=s>0)
            a.box(((lo+hi)/2,s*(W/2+.015),1.20),(.21,.035,.055),'dark_metal')
            a.box((lo-.055,s*(W/2+.012),1.18),(.011,.026,.67),'dark_metal')
        a.box((rear+.72,s*(W/2+.09),.66),(1.12,.24,.11),'metal')
        a.beam((windshield-.05,s*W*.43,1.8),(windshield+.19,s*(W/2+.22),1.95),.045,mat='dark_metal')
        a.box((windshield+.19,s*(W/2+.23),2.02),(.16,.09,.32),'dark_metal')
        a.box((windshield+.105,s*(W/2+.232),2.02),(.015,.072,.27),'silver')
        # Segmented arch lip follows the body opening.
        pts=[]
        for j in range(7):
            t=math.pi-j*math.pi/6
            pts.append((axle+(r+.073)*math.cos(t),s*(W/2+.012),r+(r+.073)*math.sin(t)))
        a.tube(pts,.026,paint,sides=4)
        a.box((front+.025,s*W*.35,1.19),(.045,.31,.15),'light')
        a.box((front+.04,s*W*.37,.99),(.05,.18,.065),'orange')
    a.box((front+.04,0,.74),(.17,W*.97,.18),'silver')
    a.box((front+.014,0,1.12),(.04,W*.39,.44),'black')
    for z in (1.00,1.10,1.20,1.30):
        a.box((front+.042,0,z),(.025,W*.37,.025),'metal')
    a.box((front+.139,0,.80),(.018,.40,.15),'white')
    for y in (-W*.33,0,W*.33):
        a.box((rf-.12,y,h+.035),(.12,.10,.058),'orange')
    # Two windshield wipers lie against the glass.
    for y in (-W*.23,W*.23):
        a.beam((xb+.012,y,zlo+.02),(xt+.09,y+.16,zlo+.30),.021,mat='black')
    return rear,h


def _truck(name,L=8.4,W=2.45,paint='white',hood=True,tandem=False,crew=False,r=.48):
    a=Asset(name,CAT,'large',forward_axis='+X',style='muted faceted American city fleet')
    front=L/2
    axles=[front-(.97 if hood else .89),-L/2+1.35]
    if tandem: axles.append(-L/2+2.53)
    if 'tiller_ladder' in name:
        axles=[front-.89,front-4.0,-L/2+1.35]
    _chassis(a,L,W,axles,r,True)
    rear,h=_cab(a,front,W*.95,paint,hood,crew,r)
    a.box((rear-.65,-W*.30,.80),(1.10,.49,.38),'silver')
    a.box((rear-.65,W*.28,.73),(1.05,.40,.33),'black')
    return a,(-L/2+.10,rear-.10),W,h


def _beacon(a,x,y,z,color='orange'):
    a.cylinder((x,y,z),(x,y,z+.045),.13,'black',sides=8)
    a.cylinder((x,y,z+.045),(x,y,z+.22),.106,color,sides=8,radius2=.092)


def _lightbar(a,x,z,W=1.45):
    a.box((x,0,z),(.22,W,.07),'dark_metal')
    for s in (-1,1):
        a.box((x,s*W*.28,z+.07),(.24,W*.38,.13),'red' if s<0 else 'blue')
    a.box((x,0,z+.07),(.23,W*.16,.12),'white')


def _bed(a,lo,hi,W,z=1.04,mat='dark_metal',th=.14):
    a.box(((lo+hi)/2,0,z),(hi-lo,W,th),mat)
    for s in (-1,1):
        a.box(((lo+hi)/2,s*(W/2-.06),z-.16),(hi-lo,.12,.20),'dark_metal')
        for x in (lo+.28,hi-.24):
            a.box((x,s*(W/2+.008),z-.02),(.15,.021,.07),'orange')


def _compartments(a,lo,hi,W,z=1.05,h=1.05,paint='white',count=4,slats=False):
    a.box(((lo+hi)/2,0,z+h/2),(hi-lo,W,h),paint)
    for s in (-1,1):
        for j in range(count):
            x=lo+(j+.5)*(hi-lo)/count
            dw=(hi-lo)/count-.07
            a.box((x,s*(W/2+.008),z+h/2),(dw,.022,h-.09),'metal' if slats else paint)
            # Dark inset seams and an actual recessed latch.
            a.box((x-dw/2,s*(W/2+.024),z+h/2),(.018,.018,h-.10),'dark_metal')
            a.box((x,s*(W/2+.029),z+.18),(.16,.028,.065),'black')
            if slats:
                for k in range(1,4):
                    a.box((x,s*(W/2+.025),z+k*h/4),(dw,.012,.015),'dark_metal')
    a.box(((lo+hi)/2,0,z+h+.025),(hi-lo+.04,W+.025,.05),'dark_metal')


def _cargo_box(a,lo,hi,W,h=2.40,paint='white',refrigerated=False):
    z=1.07
    # Chamfered top corners avoid a featureless rectangular silhouette.
    _profile(a,[(lo,z),(hi,z),(hi,z+h-.10),(hi-.14,z+h),(lo+.14,z+h),(lo,z+h-.10)],W,paint)
    for s in (-1,1):
        for x in (lo+.05,hi-.05):
            a.box((x,s*(W/2+.006),z+h/2),(.045,.025,h-.06),'silver')
        for zz in (z+.10,z+h-.08):
            a.box(((lo+hi)/2,s*(W/2+.008),zz),(hi-lo-.06,.025,.045),'silver')
        for j in range(6):
            a.box((lo+.28+j*(hi-lo-.56)/5,s*(W/2+.026),z+.10),(.14,.012,.045),'red' if j%2 else 'white')
        a.box(((lo+hi)/2,s*W*.39,.64),(hi-lo-.35,.07,.08),'metal')
    for sy in (-1,1):
        a.box((lo-.014,sy*W*.247,z+h/2),(.027,W*.48,h-.12),paint)
        a.cylinder((lo-.049,sy*W*.28,z+.18),(lo-.049,sy*W*.28,z+h-.18),.022,'steel',sides=6)
        a.box((lo-.071,sy*W*.28,z+.65),(.03,.22,.055),'dark_metal')
        for zz in (z+.36,z+h-.34):
            a.box((lo-.04,sy*W*.44,zz),(.048,.15,.066),'silver')
    a.box((lo-.035,0,z+h/2),(.035,.021,h-.04),'dark_metal')
    if refrigerated:
        a.box((hi+.19,0,z+h-.24),(.42,W*.67,.75),'white')
        for s in (-1,1):
            a.cylinder((hi+.414,s*.40,z+h-.22),(hi+.44,s*.40,z+h-.22),.23,'dark_metal',sides=12)
            a.cylinder((hi+.443,s*.40,z+h-.22),(hi+.46,s*.40,z+h-.22),.08,'silver',sides=6)
        for zz in (z+h-.50,z+h-.43):
            a.box((hi+.43,0,zz),(.026,W*.51,.025),'metal')


def _ladder(a,lo,hi,z,width=.64,sideheight=.22,mat='silver',rungs=18):
    for s in (-1,1):
        for zz in (z,z+sideheight):
            a.beam((lo,s*width/2,zz),(hi,s*width/2,zz),.065,mat=mat)
        n=max(3,int((hi-lo)/1.0))
        for j in range(n):
            x=lo+(hi-lo)*j/n; xx=lo+(hi-lo)*(j+1)/n
            a.beam((x,s*width/2,z),(xx,s*width/2,z+sideheight),.034,mat=mat)
    for j in range(rungs):
        x=lo+(hi-lo)*j/(rungs-1)
        a.beam((x,-width/2,z+.05),(x,width/2,z+.05),.038,mat=mat)


def _outriggers(a,x,W,z=.85):
    for s in (-1,1):
        a.box((x,s*W*.42,z),(.30,W*.25,.27),'dark_metal')
        a.cylinder((x,s*W*.55,.38),(x,s*W*.55,z),.065,'steel',sides=8)
        a.box((x,s*W*.55,.32),(.37,.33,.09),'black')


def _tank(a,lo,hi,z,r=.90,mat='white'):
    a.cylinder((lo+.12,0,z),(hi-.12,0,z),r,mat,sides=12)
    a.cylinder((lo,0,z),(lo+.12,0,z),r*.86,mat,sides=12,radius2=r)
    a.cylinder((hi-.12,0,z),(hi,0,z),r,mat,sides=12,radius2=r*.86)
    for x in (lo+.32,hi-.32):
        a.torus((x,0,z),r+.015,.032,'metal',axis='x',segments=12,sides=4)
        a.box((x,0,z-r-.03),(.26,r*1.65,.16),'dark_metal')
    a.cylinder(((lo+hi)/2,0,z+r-.02),((lo+hi)/2,0,z+r+.17),.23,'metal',sides=10)
    a.cylinder(((lo+hi)/2,0,z+r+.17),((lo+hi)/2,0,z+r+.22),.28,'dark_metal',sides=10)


def _hose_reel(a,x,y,z,r=.42,width=.40,axis='y'):
    if axis=='y':
        a.cylinder((x,y-width/2,z),(x,y+width/2,z),r*.75,'black',sides=12)
        for s in (-1,1):
            a.cylinder((x,y+s*(width/2),z),(x,y+s*(width/2+.03),z),r,'metal',sides=12)
        a.cylinder((x,y-width*.6,z),(x,y+width*.6,z),.075,'steel',sides=8)
        for s in (-1,1):
            a.beam((x-.35,y+s*width*.55,z-.50),(x,y+s*width*.55,z),.055,mat='dark_metal')
            a.beam((x+.35,y+s*width*.55,z-.50),(x,y+s*width*.55,z),.055,mat='dark_metal')
    else:
        a.cylinder((x-width/2,y,z),(x+width/2,y,z),r*.75,'rubber',sides=12)
        for s in (-1,1):
            a.cylinder((x+s*width/2,y,z),(x+s*(width/2+.035),y,z),r,'metal',sides=12)


def _roof_ac(a,x,z,W=1.55,L=1.35):
    a.box((x,0,z+.13),(L,W,.26),'concrete_light')
    for y in (-W*.26,W*.26):
        a.cylinder((x,y,z+.26),(x,y,z+.29),.25,'dark_metal',sides=10)
    for j in range(5):
        a.box((x-.45+j*.22,-W/2-.008,z+.12),(.10,.015,.11),'dark_metal')


def _bus_body(a,lo,hi,W,H,axles,r=.49,paint='white',school=False,open_top=False):
    floor=.51
    top=[(hi,1.62),(hi-.20,H-.20),(hi-.44,H),(lo+.24,H),(lo,H-.20)]
    _profile(a,_archpoly(lo,hi,floor,axles,r,top),W,paint)
    for s in (-1,1):
        a.box(((lo+hi)/2,s*(W/2+.01),1.44),(hi-lo-.12,.026,.075),'dark_metal' if school else 'navy')
        n=max(3,int((hi-lo-.70)/.90))
        for j in range(n):
            x=lo+.35+(j+.5)*(hi-lo-.9)/n
            ww=(hi-lo-.9)/n-.08
            zh=2.55 if school else H-.20
            a.box((x,s*(W/2+.018),(1.76+zh)/2),(ww,.027,zh-1.76),'dark_metal')
            a.box((x,s*(W/2+.035),(1.80+zh)/2),(ww-.065,.014,zh-1.86),'glass')
            if school:
                a.box((x,s*(W/2+.047),2.22),(ww-.055,.015,.024),'metal')
        if school:
            for z in (1.12,1.23,1.56):
                a.box(((lo+hi)/2,s*(W/2+.016),z),(hi-lo-.15,.038,.041),'black')
        else:
            for j in range(max(2,int((hi-lo)/1.5))):
                x=lo+.65+j*1.40
                if x<hi-.4:
                    a.box((x,s*(W/2+.026),1.13),(1.15,.012,.025),'metal')
                    a.box((x,s*(W/2+.033),1.27),(.13,.022,.035),'dark_metal')
    # Glass follows the raked front; a painted center divider remains.
    for s in (-1,1):
        _pane(a,[(hi-.012,s*.035,1.78),(hi-.012,s*(W*.43),1.78),
                 (hi-.204,s*(W*.43),H-.23),(hi-.204,s*.035,H-.23)],reverse=s<0)
        a.box((hi+.012,s*W*.35,1.13),(.037,.28,.13),'light')
        a.box((lo-.018,s*W*.38,1.38),(.03,.18,.21),'red')
        a.beam((hi-.23,s*W*.44,2.16),(hi+.15,s*(W/2+.22),2.24),.045,mat='black')
        a.box((hi+.16,s*(W/2+.23),2.22),(.13,.11,.31),'black')
    a.box((hi+.022,0,.73),(.12,W*.94,.16),'dark_metal')
    a.box((hi+.014,0,1.39),(.04,W*.58,.12),'black')
    a.box((lo-.015,0,2.21),(.024,W*.59,.62),'glass')
    for j in range(5):
        a.box((lo-.027,0,.95+j*.061),(.024,W*.45,.025),'dark_metal')
    if not school:
        a.box((hi-.30,0,H-.105),(.05,W*.67,.12),'black')


def _bus_door(a,x,W,z=1.50,h=1.98,width=.80):
    for side in (-1,1):
        xx=x+side*width*.25
        a.box((xx,-W/2-.045,z),(.46*width,.045,h),'dark_metal')
        a.box((xx,-W/2-.073,z+.11),(.46*width-.09,.022,h-.45),'glass')
    a.box((x,-W/2-.15,.45),(width+.06,.28,.12),'metal')


def _bus_vehicle(name,kind):
    a=Asset(name,CAT,'large',forward_axis='+X',style='American municipal bus')
    if kind=='articulated_transit_bus':
        L=17.7; W=2.55; H=3.16
        ax=[7.1,-.20,-6.70]
        _chassis(a,L,W,ax,.49,True)
        _bus_body(a,-1.15,L/2,W,H,[ax[0],ax[1]])
        _bus_body(a,-L/2,-2.23,W,H,[ax[2]])
        a.box((-1.69,0,1.85),(1.08,W*.90,2.38),'black')
        for j in range(9):
            x=-2.19+j*.123
            for s in (-1,1): a.box((x,s*(W/2-.018),1.85),(.040,.10,2.50),'dark_metal')
            a.box((x,0,H-.04),(.04,W,.11),'dark_metal')
        for x in (7.52,1.45,-5.3): _bus_door(a,x,W)
        _roof_ac(a,4.1,H,1.75,1.8); _roof_ac(a,-5.0,H,1.75,1.8)
    elif kind in ('conventional_school_bus','short_school_bus'):
        short=kind=='short_school_bus';L=7.35 if short else 10.7;W=2.43;H=3.07
        front=L/2; rear=-L/2; ax=[front-1.0,rear+1.60]
        _chassis(a,L,W,ax,.48,True)
        _bus_body(a,rear,front-1.40,W,H,[ax[1]],.48,'yellow',True)
        _profile(a,_archpoly(front-1.46,front,.52,[ax[0]],.48,
                            [(front,1.35),(front-.17,1.55),(front-1.46,1.59)]),W*.82,'yellow')
        a.box((front+.045,0,1.13),(.06,W*.43,.53),'black')
        for z in (1.,1.12,1.24): a.box((front+.081,0,z),(.03,W*.41,.022),'metal')
        a.box((front+.08,0,.72),(.20,W*.92,.20),'black')
        for s in (-1,1):
            a.cylinder((front+.03,s*.76,1.25),(front+.09,s*.76,1.25),.11,'light',sides=10)
            for x in (rear-.014,front-1.394):
                for y in (.77,.96):
                    a.cylinder((x,s*y,2.84),(x+(-.03 if x<0 else .03),s*y,2.84),.07,'red' if y>.8 else 'orange',sides=8)
        _bus_door(a,front-1.99,W,1.50,1.98,.84)
        # Folded octagonal stop paddle and crossing arm identify a US school bus.
        sx=front-2.9
        a.cylinder((sx,W/2+.07,1.74),(sx,W/2+.11,1.74),.28,'white',sides=8)
        a.cylinder((sx,W/2+.112,1.74),(sx,W/2+.126,1.74),.245,'red',sides=8)
        a.box((front+.20,-.55,.91),(.07,1.15,.07),'yellow')
        a.box((rear-.028,0,1.38),(.024,.77,1.45),'yellow')
        a.box((rear-.045,0,1.89),(.026,.55,.46),'glass')
        a.box((rear-.048,.22,1.31),(.04,.15,.04),'black')
        a.box((-1.0 if not short else -.6,0,H+.055),(.70,.74,.11),'white')
    else:
        specs={
            'low_floor_transit_bus':(12.0,2.55,3.18,'white'),
            'paratransit_shuttle_bus':(6.85,2.33,2.95,'white'),
            'intercity_motor_coach':(12.4,2.55,3.60,'navy'),
            'open_top_tour_bus':(10.8,2.55,3.20,'red'),
            'airport_shuttle_bus':(8.15,2.50,3.11,'cream'),
            'mobile_command_bus':(10.25,2.52,3.34,'navy'),
            'mobile_library_bus':(9.25,2.50,3.32,'teal')}
        L,W,H,paint=specs[kind];ax=[L/2-1.45,-L/2+1.75]
        if kind=='intercity_motor_coach': ax.append(-L/2+2.91)
        _chassis(a,L,W,ax,.49,True)
        _bus_body(a,-L/2,L/2,W,H,ax,.49,paint)
        _bus_door(a,L/2-.81,W)
        if kind=='low_floor_transit_bus':
            _bus_door(a,-.65,W,1.51,1.98,1.18)
            _roof_ac(a,-1.0,H,1.75,2.10)
            a.box((-4.1,0,H+.23),(2.15,1.68,.43),'concrete_light')
            # Folded bicycle carrier at the nose.
            for y in (-.65,.65): a.beam((L/2+.14,y,.60),(L/2+.35,y,1.22),.045,mat='metal')
            for z in (.71,1.03): a.beam((L/2+.33,-.82,z),(L/2+.33,.82,z),.045,mat='metal')
        elif kind=='paratransit_shuttle_bus':
            # Underfloor wheelchair lift cassette and tall accessible entry.
            a.box((-.98,-W/2-.04,.61),(1.38,.19,.34),'dark_metal')
            _bus_door(a,-.95,W,1.58,1.90,1.12)
            a.box((-.95,-W/2-.087,2.54),(.24,.025,.24),'blue')
            a.torus((-.96,-W/2-.11,2.51),.057,.012,'white',axis='y',segments=8,sides=4)
            _roof_ac(a,-.45,H,1.2,.98)
        elif kind=='intercity_motor_coach':
            for s in (-1,1):
                for x in (-2.8,-1.1,.6,2.3):
                    a.box((x,s*(W/2+.038),1.31),(1.53,.019,.68),'navy')
                    a.box((x,s*(W/2+.05),1.52),(.15,.021,.04),'silver')
            _roof_ac(a,-2.2,H,1.7,2.25)
            a.box((L/2-.25,0,H+.04),(.33,W*.85,.12),'navy')
        elif kind=='open_top_tour_bus':
            # Open upper deck: hollow parapets, aisle and twelve individual seats.
            a.box((-.3,0,H+.04),(L-1.15,W-.16,.10),'dark_metal')
            for s in (-1,1):
                a.box((-.35,s*(W/2-.07),H+.39),(L-1.1,.14,.68),'red')
                a.beam((-L/2+.22,s*(W/2-.07),H+.76),(L/2-.88,s*(W/2-.07),H+.76),.055,mat='silver')
                for j in range(6):
                    x=-L/2+.75+j*1.35
                    a.box((x,s*.72,H+.43),(.52,.59,.12),'cream')
                    a.box((x-.23,s*.72,H+.71),(.10,.59,.61),'cream')
            a.box((L/2-.83,0,H+.35),(.14,W-.12,.61),'glass')
        elif kind=='airport_shuttle_bus':
            _bus_door(a,-.7,W,1.50,1.98,1.32)
            # External luggage cage at the rear is unlike a standard transit bus.
            a.box((-L/2-.49,0,1.0),(.78,W*.80,.10),'dark_metal')
            for s in (-1,1):
                for x in (-L/2-.84,-L/2-.10):
                    a.box((x,s*W*.38,1.69),(.065,.065,1.42),'metal')
                a.box((-L/2-.47,s*W*.38,2.40),(.83,.065,.065),'metal')
            for y in (-.72,-.24,.24,.72): a.box((-L/2-.84,y,1.69),(.055,.045,1.4),'metal')
            _roof_ac(a,0,H,1.5,1.5)
        elif kind=='mobile_command_bus':
            # Telescopic communications mast, radome and deployable side awning.
            _roof_ac(a,1.45,H,1.65,1.60)
            a.cylinder((-2.85,0,H),(-2.85,0,H+1.58),.07,'silver',sides=8)
            for y in (-.5,.5): a.beam((-2.85,0,H+1.5),(-2.85,y,H+1.5),.035,mat='metal')
            a.sphere((-.5,0,H+.27),.42,'white',segments=10,rings=4,scale=(.44,.44,.39))
            a.box((.10,-W/2-.085,H-.15),(5.4,.20,.21),'dark_metal')
            for s in (-1,1):
                a.box((0,s*(W/2+.06),2.34),(3.45,.06,.80),'navy')
            _lightbar(a,L*.29,H+.11)
        elif kind=='mobile_library_bus':
            # Extended service awning, book return hatch and rear entrance steps.
            a.box((-.15,-W/2-.54,2.76),(4.1,1.05,.07),'cream',rot=(.08,0,0))
            for x in (-2.05,1.72):
                a.beam((x,-W/2-.03,1.87),(x,-W/2-1.03,2.71),.045,mat='metal')
            a.box((.0,-W/2-.055,1.52),(.64,.08,.49),'silver')
            a.box((0,-W/2-.105,1.66),(.49,.03,.07),'black')
            for j in range(3):
                a.box((L/2-.8,-W/2-.20-j*.21,.51-j*.13),(.89,.25,.12),'dark_metal')
            _roof_ac(a,-1,H,1.3,1.1)
    return a.bottom_center()


def _van_shell(name,L=6.15,W=2.10,H=2.65,paint='white',step=False):
    a=Asset(name,CAT,'large',forward_axis='+X',style='American fleet van')
    r=.37 if L<6 else .41
    ax=[L/2-.93,-L/2+1.02]
    _chassis(a,L,W,ax,r,False)
    hi=L/2; lo=-L/2
    cabx=hi-(.42 if step else 1.06)
    top=[(hi,1.12),(hi-.13,1.43),(cabx,1.57),(cabx-.36,H-.17),(cabx-.63,H),(lo+.18,H),(lo,H-.18)]
    _profile(a,_archpoly(lo,hi,.47,ax,r,top),W,paint)
    zlo=1.63;zhi=H-.22
    for s in (-1,1):
        _pane(a,[(cabx-.06,s*(W/2+.016),zlo),(cabx-1.10,s*(W/2+.016),zlo),
                 (cabx-1.10,s*(W/2+.016),zhi),(cabx-.45,s*(W/2+.016),zhi)],reverse=s<0)
        a.box((cabx-.81,s*(W/2+.025),1.39),(.18,.028,.048),'dark_metal')
        a.box((cabx-.16,s*(W/2+.13),1.88),(.18,.16,.21),'black')
        a.box((hi+.016,s*W*.34,1.20),(.04,.29,.15),'light')
        a.box((lo-.026,s*W*.40,1.54),(.04,.13,.35),'red')
        a.box((cabx-1.30,s*(W/2+.018),1.18),(.014,.02,1.17),'dark_metal')
        a.box((cabx-.8,s*(W/2+.063),.52),(1.03,.15,.10),'dark_metal')
    _pane(a,[(cabx+.006,-W*.44,zlo),(cabx+.006,W*.44,zlo),
             (cabx-.36,W*.44,zhi),(cabx-.36,-W*.44,zhi)])
    a.box((hi+.02,0,.73),(.14,W*.92,.18),'dark_metal')
    a.box((hi+.021,0,1.04),(.04,W*.52,.17),'black')
    for z in (1.,1.06,1.12): a.box((hi+.047,0,z),(.015,W*.49,.015),'metal')
    for s in (-1,1):
        a.box((lo-.022,s*W*.245,1.58),(.03,W*.47,1.77),paint)
        a.box((lo-.05,s*.10,1.25),(.04,.04,.19),'black')
        for z in (.95,2.18): a.box((lo-.056,s*W*.445,z),(.06,.12,.053),'silver')
    a.box((lo-.045,0,1.59),(.018,.022,1.75),'dark_metal')
    return a,lo,cabx-1.35,W,H


def _emergency_cross(a,x,y,z,size=.48):
    a.box((x,y,z),(size,.025,size*.28),'red')
    a.box((x,y-.001,z),(size*.28,.028,size),'red')


def _fire_pump_panel(a,x,y,z):
    a.box((x,y,z),(1.05,.07,.77),'dark_metal')
    s=1 if y>0 else -1
    for dx in (-.32,.02,.33):
        a.cylinder((x+dx,y+s*.04,z+.18),(x+dx,y+s*.07,z+.18),.075,'silver',sides=10)
        a.cylinder((x+dx,y+s*.07,z+.18),(x+dx,y+s*.08,z+.18),.052,'white',sides=8)
    for dx in (-.27,.24):
        a.cylinder((x+dx,y+s*.04,z-.18),(x+dx,y+s*.14,z-.18),.105,'silver',sides=8)
        a.cylinder((x+dx,y+s*.14,z-.18),(x+dx,y+s*.155,z-.18),.074,'black',sides=8)


def _make_fleet(name,kind):
    if kind in BUS_KINDS:
        return _bus_vehicle(name,kind)
    if kind=='van_ambulance':
        a,lo,hi,W,H=_van_shell(name,6.15,2.14,2.70)
        _lightbar(a,hi+.60,H+.09)
        for s in (-1,1):
            a.box(((lo+hi)/2,s*(W/2+.022),1.39),(hi-lo,.026,.17),'red')
            _emergency_cross(a,-.65,s*(W/2+.06),2.07,.53)
            for x in (lo+.23,hi-.05): a.box((x,s*(W/2+.036),2.53),(.19,.035,.10),'red')
        for y in (-.52,.52): a.box((lo-.055,y,1.97),(.018,.69,.54),'glass')
        a.box((-.60,0,H+.055),(.50,.46,.11),'white')
        return a.bottom_center()
    if kind in ('parcel_step_van','postal_walkin_truck','food_service_truck','ice_cream_truck'):
        specs={'parcel_step_van':(6.95,2.30,3.05,'brown'),
               'postal_walkin_truck':(5.15,2.10,2.77,'white'),
               'food_service_truck':(7.20,2.38,3.06,'cream'),
               'ice_cream_truck':(5.85,2.17,2.78,'white')}
        L,W,H,paint=specs[kind]
        a,lo,hi,W,H=_van_shell(name,L,W,H,paint,True)
        if kind=='parcel_step_van':
            for s in (-1,1):
                a.box((hi+.63,s*(W/2+.021),1.31),(.89,.035,1.75),'brown')
                a.box((hi+.63,s*(W/2+.047),2.03),(.67,.021,.67),'glass')
                a.box((hi+.90,s*(W/2+.065),1.38),(.031,.035,.29),'silver')
                a.box((hi+.48,s*(W/2+.11),.44),(1.03,.22,.10),'metal')
            for j in range(10): a.box((lo-.062,0,.85+j*.185),(.025,W*.86,.022),'dark_metal')
            a.box((lo-.078,0,1.12),(.03,.28,.07),'silver')
        elif kind=='postal_walkin_truck':
            a.box(((lo+hi)/2,-W/2-.026,1.30),(hi-lo,.024,.08),'blue')
            a.box(((lo+hi)/2,-W/2-.027,1.20),(hi-lo,.024,.036),'red')
            # Mail tubs behind glazed rolling side door, short blunt rear body.
            a.box((hi+.55,-W/2-.035,1.34),(.87,.045,1.60),'white')
            a.box((hi+.55,-W/2-.067,1.99),(.70,.027,.62),'glass')
            a.box((hi+.92,-W/2-.08,1.36),(.03,.025,.26),'black')
            a.box((lo-.095,0,.57),(.25,W*.78,.12),'metal')
            a.cylinder((lo+.34,.52,H),(lo+.34,.52,H+.33),.023,'dark_metal',sides=6)
        elif kind=='food_service_truck':
            a.box((-.6,-W/2-.035,1.98),(2.42,.055,1.08),'dark_metal')
            a.box((-.6,-W/2-.077,1.97),(2.20,.027,.83),'glass')
            a.box((-.6,-W/2-.32,1.48),(2.58,.65,.10),'silver')
            a.box((-.6,-W/2-.42,2.61),(2.68,.88,.075),'cream',rot=(.12,0,0))
            for x in (-1.81,.61): a.beam((x,-W/2-.07,2.03),(x,-W/2-.84,2.55),.035,mat='metal')
            a.box((lo+.75,-W/2-.045,1.21),(.50,.035,.68),'black')
            for z in (1.04,1.18,1.32): a.box((lo+.75,-W/2-.069,z),(.37,.025,.055),'cream')
            a.box((-.35,0,H+.23),(1.15,.68,.46),'silver')
            a.cylinder((.44,.12,H),(.44,.12,H+.59),.14,'metal',sides=8)
            a.cone((.44,.12,H+.64),(.44,.12,H+.70),.23,'metal',sides=8)
            for y in (-.41,.41):
                a.cylinder((lo-.24,y,.88),(lo-.24,y,1.52),.21,'white',sides=10)
                a.cylinder((lo-.24,y,1.52),(lo-.24,y,1.59),.13,'metal',sides=8)
        else:
            a.box((-.36,-W/2-.038,1.97),(1.75,.05,.86),'dark_metal')
            for x in (-.79,.07): a.box((x,-W/2-.071,1.97),(.79,.025,.70),'glass')
            a.box((-.36,-W/2-.24,1.51),(1.96,.46,.095),'silver')
            a.box((lo+.54,-W/2-.058,1.52),(.59,.05,1.03),'cream')
            for j in range(3):
                a.cylinder((lo+.54,-W/2-.09,1.26+j*.26),(lo+.54,-W/2-.11,1.26+j*.26),.075,('pink','brown','white')[j],sides=8)
            # Roof cone sign is built geometry, not a texture.
            a.cone((-.9,0,H+.72),(-.9,0,H+.17),.23,'wood_light',sides=8)
            a.sphere((-.9,0,H+.80),.30,'cream',segments=10,rings=5)
            for y in (-.43,.43): a.cylinder((hi+.65,y,H+.09),(hi+.79,y,H+.22),.14,'silver',sides=8,radius2=.20)
        return a.bottom_center()

    # All remaining working vehicles use their own mounted functional body.
    specs={
        'modular_ambulance':(7.10,2.40,'white',True,False,False),
        'fire_pumper_engine':(9.10,2.48,'red',False,False,True),
        'aerial_ladder_fire_truck':(11.25,2.50,'red',False,True,True),
        'tiller_ladder_fire_truck':(15.60,2.50,'red',False,True,True),
        'heavy_rescue_squad':(9.40,2.48,'red',False,False,True),
        'wildland_brush_fire_truck':(6.95,2.33,'red',True,False,False),
        'fire_water_tender':(9.40,2.48,'red',True,True,False),
        'prisoner_transport_truck':(8.25,2.44,'white',True,False,False),
        'armored_security_truck':(7.0,2.42,'concrete_light',False,False,False),
        'tactical_rescue_truck':(7.75,2.48,'dark_metal',True,False,False),
        'rollback_tow_truck':(8.75,2.44,'white',True,False,False),
        'wheel_lift_tow_truck':(6.95,2.36,'blue',True,False,False),
        'heavy_recovery_wrecker':(10.55,2.50,'orange',True,True,False),
        'bucket_utility_truck':(8.85,2.44,'white',True,False,False),
        'cable_spool_utility_truck':(8.35,2.45,'white',True,False,False),
        'line_maintenance_service_truck':(7.65,2.40,'white',True,False,False),
        'sewer_vacuum_truck':(9.60,2.49,'teal',False,True,False),
        'water_spray_truck':(9.35,2.47,'white',True,True,False),
        'rear_loader_refuse_truck':(9.35,2.51,'white',False,True,False),
        'front_loader_refuse_truck':(10.40,2.51,'green',False,True,False),
        'automated_side_loader_refuse_truck':(9.50,2.51,'white',False,True,False),
        'split_body_recycling_truck':(8.85,2.48,'white',False,False,False),
        'rolloff_container_truck':(10.10,2.50,'white',True,True,False),
        'commercial_box_truck':(8.60,2.47,'white',True,False,False),
        'refrigerated_delivery_truck':(8.45,2.46,'white',False,False,False),
        'beverage_delivery_truck':(9.30,2.50,'blue',True,True,False),
        'flatbed_stake_truck':(8.75,2.45,'green',True,False,False),
        'municipal_dump_truck':(9.10,2.49,'orange',True,True,False),
        'fuel_delivery_tanker':(9.55,2.49,'white',True,True,False),
        'glass_transport_truck':(8.55,2.45,'white',True,False,False),
        'tree_service_chip_truck':(8.15,2.44,'white',True,False,False),
        'snowplow_spreader_truck':(9.30,2.49,'orange',True,True,False),
        'street_marking_truck':(8.35,2.44,'yellow',False,False,False),
        'airport_crash_tender':(10.15,2.95,'yellow',False,True,True),
        'hi_rail_utility_truck':(7.55,2.39,'white',True,False,False)}
    L,W,paint,hood,tandem,crew=specs[kind]
    a,(lo,hi),W,H=_truck(name,L,W,paint,hood,tandem,crew)
    mid=(lo+hi)/2
    if kind=='modular_ambulance':
        _cargo_box(a,lo,hi+.14,W,2.03,'white')
        for s in (-1,1):
            a.box((mid,s*(W/2+.032),1.69),(hi-lo-.08,.034,.19),'red')
            _emergency_cross(a,mid-.45,s*(W/2+.071),2.43,.65)
            for x in (lo+.20,hi-.20): a.box((x,s*(W/2+.048),2.86),(.28,.033,.13),'red')
            for x in (lo+.65,hi-.40):
                a.box((x,s*(W/2+.031),1.38),(.70,.02,.032),'metal')
                a.box((x,s*(W/2+.044),1.51),(.15,.028,.055),'black')
        for y in (-.56,.56): a.box((lo-.038,y,2.44),(.03,.68,.47),'glass')
        _lightbar(a,hi+.69,H+.12)
        a.box((hi+.02,0,3.16),(.34,1.87,.13),'white')
    elif kind in ('fire_pumper_engine','aerial_ladder_fire_truck','tiller_ladder_fire_truck','heavy_rescue_squad'):
        long=kind=='tiller_ladder_fire_truck'
        bodyhi=hi-.45 if kind=='fire_pumper_engine' else hi
        bodylo=lo+2.0 if long else lo
        _compartments(a,bodylo,bodyhi,W,1.05,1.37,'red',4,True)
        _lightbar(a,L/2-1.32,H+.10)
        for s in (-1,1):
            a.box(((bodylo+bodyhi)/2,s*(W/2+.047),1.48),(bodyhi-bodylo-.08,.03,.12),'white')
            for x in (bodylo+.19,bodyhi-.18): a.box((x,s*(W/2+.049),2.18),(.15,.03,.11),'red')
        if kind=='fire_pumper_engine':
            for s in (-1,1): _fire_pump_panel(a,hi-.08,s*(W/2+.065),1.62)
            for y in (-.50,0,.50):
                # Several folded hose layers in an open upper hose bed.
                for z in (2.48,2.57): a.box((mid-.25,y,z),(2.30,.40,.075),'cream')
            _ladder(a,lo+.30,hi-.55,2.60,.53,.13,rungs=14)
            for s in (-1,1): a.cylinder((lo+.25,s*.99,2.55),(hi-.45,s*.99,2.55),.075,'black',sides=8)
            a.cylinder((hi-.05,0,2.50),(hi-.05,0,2.92),.08,'metal',sides=8)
            a.cylinder((hi-.05,0,2.92),(hi+.42,0,3.00),.075,'dark_metal',sides=8,radius2=.045)
        elif kind=='heavy_rescue_squad':
            a.box((mid,0,2.75),(hi-lo-.20,W-.10,.67),'red')
            for s in (-1,1):
                for j in range(4):
                    x=lo+.45+j*(hi-lo-.9)/3
                    a.box((x,s*(W/2+.025),2.75),(.70,.035,.57),'metal')
                    a.box((x,s*(W/2+.050),2.63),(.14,.025,.05),'black')
            a.cylinder((lo+.57,0,3.13),(lo+.57,0,3.63),.065,'metal',sides=8)
            for y in (-.42,.42): a.box((lo+.57,y,3.63),(.20,.55,.20),'light')
            _roof_ac(a,hi-.50,3.1,1.10,.90)
            _ladder(a,lo+.75,hi-.80,3.13,.52,.11,rungs=10)
        else:
            pivot=hi-.40
            a.cylinder((pivot,0,2.43),(pivot,0,2.64),.64,'dark_metal',sides=12)
            for y in (-.36,.36):
                a.beam((pivot-.28,y,2.60),(pivot+.23,y,3.07),.15,mat='red')
            _ladder(a,bodylo+.15,L/2-.08,3.03,.78,.35,rungs=20 if not long else 23)
            _ladder(a,bodylo+.55,L/2+.14,3.42,.59,.24,rungs=16 if not long else 19)
            for x in (bodylo+.55,hi-.65): _outriggers(a,x,W)
            if long:
                # Rear steering cab on a tillered trailer; fifth-wheel articulation.
                a.box((lo+1.0,0,1.25),(1.80,W*.90,.73),'red')
                _profile(a,[(lo+.22,1.48),(lo+1.78,1.48),(lo+1.56,2.84),(lo+.43,2.84)],W*.83,'red')
                for s in (-1,1):
                    _pane(a,[(lo+.39,s*W*.42,1.89),(lo+1.57,s*W*.42,1.89),(lo+1.43,s*W*.42,2.69),(lo+.51,s*W*.42,2.69)],reverse=s>0)
                a.box((lo+.215,0,2.25),(.03,W*.66,.71),'glass')
                _lightbar(a,lo+1,2.91,1.25)
                a.cylinder((hi+.13,0,.73),(hi+.13,0,.95),.52,'dark_metal',sides=12)
    elif kind=='wildland_brush_fire_truck':
        _bed(a,lo,hi,W)
        for s in (-1,1):
            a.box((mid,s*W*.37,1.42),(hi-lo,.49,.70),'red')
            a.box((mid,s*(W/2+.01),1.60),(hi-lo-.15,.026,.028),'silver')
        a.box((mid+.20,0,1.50),(2.0,.87,.82),'white')
        _hose_reel(a,lo+.80,0,2.09,.36,.62)
        a.box((lo+.26,0,1.29),(.53,.68,.40),'dark_metal')
        a.cylinder((lo+.22,-.34,1.40),(lo+.22,-.66,1.4),.065,'silver',sides=8)
        _lightbar(a,hi+.64,H+.11)
        for s in (-1,1):
            a.beam((lo+.15,s*.72,1.12),(lo+.15,s*.72,1.91),.048,mat='metal')
            a.beam((lo+.15,s*.72,1.91),(lo+.95,s*.72,1.91),.048,mat='metal')
        a.beam((L/2+.16,-.93,.89),(L/2+.16,.93,.89),.09,mat='dark_metal')
    elif kind=='fire_water_tender':
        _tank(a,lo+.25,hi,2.05,.89,'red')
        _compartments(a,lo,lo+1.0,W,1.04,.68,'red',1,True)
        for s in (-1,1):
            a.box((mid,s*.905,2.05),(hi-lo-.4,.03,.16),'white')
            a.cylinder((lo+.1,s*W*.43,1.18),(hi-.1,s*W*.43,1.18),.12,'black',sides=8)
        _fire_pump_panel(a,lo+.45,-W/2-.06,1.47)
        _lightbar(a,hi+.85,H+.11)
        a.cylinder((lo-.12,0,1.0),(lo-.38,0,1.0),.14,'silver',sides=8)
    elif kind=='prisoner_transport_truck':
        _cargo_box(a,lo,hi,W,2.13,'white')
        for s in (-1,1):
            a.box((mid,s*(W/2+.037),1.39),(hi-lo-.1,.022,.14),'navy')
            for j in range(3):
                x=lo+.65+j*(hi-lo-1.3)/2
                a.box((x,s*(W/2+.028),2.61),(.68,.025,.33),'glass')
                for dx in (-.23,0,.23): a.box((x+dx,s*(W/2+.052),2.61),(.025,.027,.34),'metal')
        a.box((lo-.10,-.48,1.20),(.15,.80,.10),'metal')
        _lightbar(a,hi+.73,H+.10)
        _roof_ac(a,mid,3.20,1.1,.90)
    elif kind=='armored_security_truck':
        _cargo_box(a,lo,hi+.10,W,1.95,'concrete_light')
        for s in (-1,1):
            # Thick framed narrow ballistic apertures, side transfer hatch.
            a.box((hi-.52,s*(W/2+.04),2.50),(.63,.10,.37),'dark_metal')
            a.box((hi-.52,s*(W/2+.096),2.50),(.42,.019,.18),'glass')
            a.box((lo+.85,s*(W/2+.044),1.78),(.66,.075,.82),'metal')
            a.box((lo+.85,s*(W/2+.089),1.80),(.44,.025,.12),'black')
            for x in (lo+.16,hi-.15):
                for z in (1.31,2.82): a.box((x,s*(W/2+.03),z),(.055,.04,.055),'dark_metal')
        a.box((lo-.11,0,2.0),(.11,W*.79,1.54),'metal')
        a.box((lo-.185,0,2.19),(.04,.63,.16),'dark_metal')
        for y in (-.82,.82): a.beam((L/2+.23,y,.62),(L/2+.23,y,1.49),.10,mat='black')
        a.beam((L/2+.23,-1.02,1.19),(L/2+.23,1.02,1.19),.10,mat='black')
    elif kind=='tactical_rescue_truck':
        _profile(a,[(lo,1.0),(hi,1.0),(hi,2.47),(hi-.25,2.84),(lo+.28,2.84),(lo,2.53)],W,'dark_metal')
        for s in (-1,1):
            for j in range(3):
                x=lo+.59+j*(hi-lo-1.18)/2
                a.box((x,s*(W/2+.025),2.31),(.62,.04,.33),'black')
                a.box((x,s*(W/2+.05),2.31),(.47,.02,.20),'glass')
                a.cylinder((x,s*(W/2+.055),1.73),(x,s*(W/2+.12),1.73),.056,'black',sides=8)
            a.box((mid,s*(W/2+.12),.82),(hi-lo,.21,.13),'black')
            a.beam((lo+.2,s*(W/2+.06),1.0),(lo+.2,s*(W/2+.06),2.01),.04,mat='silver')
        a.cylinder((mid,0,2.84),(mid,0,2.98),.60,'black',sides=10)
        a.box((mid,0,3.13),(.91,.92,.31),'dark_metal')
        a.box((mid+.47,0,3.15),(.025,.65,.11),'glass')
        _lightbar(a,hi+.80,H+.13)
        a.box((L/2+.20,0,.94),(.26,W*.91,.30),'black')
        for y in (-.62,.62): a.beam((L/2+.24,y,.74),(L/2+.24,y,1.62),.09,mat='black')
        a.cylinder((lo-.30,0,1.85),(lo-.58,0,1.85),.44,'rubber',sides=12)
        a.cylinder((lo-.59,0,1.85),(lo-.63,0,1.85),.24,'metal',sides=10)
    elif kind=='rollback_tow_truck':
        # Long steel rollback deck, flared wheel guides, winch and headboard.
        _profile(a,[(lo-.40,.85),(hi,1.02),(hi,1.21),(lo-.40,1.02)],W,'dark_metal')
        for s in (-1,1):
            a.beam((lo-.38,s*W*.47,1.04),(hi-.06,s*W*.47,1.24),.08,mat='silver')
            a.box((mid,s*W*.47,1.12),(hi-lo,.09,.18),'dark_metal')
        a.box((hi-.15,0,1.72),(.15,W*.90,1.0),'dark_metal')
        a.box((hi-.17,0,2.04),(.18,W*.66,.36),'black')
        _hose_reel(a,hi-.51,0,1.43,.20,.60)
        a.cylinder((hi-.59,0,1.44),(lo+.5,0,1.14),.018,'silver',sides=6)
        for y in (-.71,.71): a.box((lo-.18,y,.99),(.54,.28,.065),'silver')
        _beacon(a,hi-.15,0,2.27)
    elif kind in ('wheel_lift_tow_truck','heavy_recovery_wrecker'):
        heavy=kind=='heavy_recovery_wrecker'
        _bed(a,lo,hi,W)
        a.box((hi-.51,0,1.36),(1.01,.55,.48),'dark_metal')
        for s in (-1,1):
            a.box((mid,s*(W/2-.30),1.48),(hi-lo,.56,.81),paint)
            for j in range(3 if heavy else 2):
                x=lo+(j+.5)*(hi-lo)/(3 if heavy else 2)
                a.box((x,s*(W/2+.018),1.48),((hi-lo)/(3 if heavy else 2)-.07,.03,.68),paint)
                a.box((x,s*(W/2+.04),1.39),(.14,.028,.047),'silver')
        base=(hi-.53,0,1.45); tip=(lo+.17,0,2.55 if heavy else 1.97)
        a.beam(base,tip,.35,.34,paint)
        a.beam((hi-.48,0,1.20),(lo+.80,0,2.28 if heavy else 1.74),.12,mat='silver')
        _hose_reel(a,hi-.48,0,1.87,.27,.72)
        for s in (-1,1):
            a.cylinder((tip[0],s*.23,tip[2]),(lo-.10,s*.23,1.29),.018,'steel',sides=6)
            a.torus((lo-.10,s*.23,1.22),.09,.018,'dark_metal',axis='y',segments=8,sides=4,arc=math.pi*1.5)
        a.beam((lo+.36,0,1.12),(lo-.89,0,.59),.19,mat='dark_metal')
        a.box((lo-.88,0,.58),(.18,1.85,.16),'dark_metal')
        for y in (-.75,.75): a.box((lo-.98,y,.63),(.62,.17,.11),'silver')
        a.box((hi-.09,0,2.21),(.15,W*.93,.61),paint)
        _beacon(a,hi-.1,0,2.55)
        if heavy:
            _outriggers(a,lo+.42,W)
            a.cylinder((hi+.02,W*.42,.76),(hi+.02,W*.42,3.03),.064,'silver',sides=8)
    elif kind in ('bucket_utility_truck','cable_spool_utility_truck','line_maintenance_service_truck','hi_rail_utility_truck'):
        _bed(a,lo,hi,W)
        for s in (-1,1):
            a.box((mid,s*(W/2-.27),1.44),(hi-lo,.54,.79),'white')
            n=4 if hi-lo>4 else 3
            for j in range(n):
                x=lo+(j+.5)*(hi-lo)/n
                a.box((x,s*(W/2+.02),1.47),((hi-lo)/n-.07,.026,.67),'white')
                a.box((x,s*(W/2+.044),1.38),(.13,.027,.05),'black')
        if kind=='bucket_utility_truck':
            a.cylinder((hi-.60,0,1.13),(hi-.60,0,1.76),.44,'dark_metal',sides=10)
            # Folded two-section insulated boom and hollow fiberglass basket.
            a.beam((hi-.60,0,1.79),(lo+.77,0,2.82),.29,.31,'white')
            a.beam((lo+.77,0,2.82),(hi+.66,0,3.11),.23,.25,'cream')
            a.cylinder((lo+.77,-.20,2.82),(lo+.77,.20,2.82),.19,'metal',sides=10)
            a.beam((hi-.55,0,1.62),(lo+1.45,0,2.47),.11,mat='silver')
            bx=hi+.79
            a.box((bx,0,3.12),(.87,.98,.12),'cream')
            for s in (-1,1): a.box((bx,s*.44,3.46),(.86,.10,.65),'cream')
            for x in (bx-.385,bx+.385): a.box((x,0,3.46),(.10,.82,.65),'cream')
            _outriggers(a,hi-.64,W);_outriggers(a,lo+.67,W)
        elif kind=='cable_spool_utility_truck':
            # Large transverse timber cable drum sits in a cradled reel frame.
            x=mid-.25;z=1.98;r=.85
            a.cylinder((x,-.74,z),(x,.74,z),r*.69,'black',sides=14)
            for s in (-1,1):
                a.cylinder((x,s*.72,z),(x,s*.80,z),r,'wood_light',sides=12)
                a.cylinder((x,s*.81,z),(x,s*.84,z),.16,'dark_metal',sides=8)
                for angle in (0,math.pi/3,2*math.pi/3):
                    a.beam((x-r*.78*math.cos(angle),s*.845,z-r*.78*math.sin(angle)),(x+r*.78*math.cos(angle),s*.845,z+r*.78*math.sin(angle)),.075,mat='wood')
                a.beam((x-.68,s*.90,1.10),(x,s*.90,z),.09,mat='dark_metal')
                a.beam((x+.68,s*.90,1.10),(x,s*.90,z),.09,mat='dark_metal')
            a.box((lo+.12,0,1.20),(.20,W*.87,.35),'dark_metal')
            _beacon(a,hi+.8,0,H+.05)
        elif kind=='line_maintenance_service_truck':
            # Elevated ladder rack with conduit tube and a bed-mounted welder.
            for s in (-1,1):
                for x in (lo+.22,hi-.14): a.box((x,s*.83,2.16),(.07,.07,1.42),'dark_metal')
                a.box((mid,s*.83,2.89),(hi-lo+.48,.07,.07),'dark_metal')
            _ladder(a,lo-.23,hi+.56,2.94,.62,.11,rungs=14)
            a.cylinder((lo-.12,.72,3.09),(hi+.62,.72,3.09),.14,'white',sides=8)
            a.box((hi-.79,0,1.43),(1.0,.68,.65),'dark_metal')
            for j in range(4): a.box((hi-.80,-.35,1.23+j*.12),(.60,.02,.035),'metal')
            _hose_reel(a,lo+.62,0,1.63,.30,.44)
        else:
            _beacon(a,hi+.75,0,H+.04)
            a.box((hi-.55,0,1.34),(.81,.77,.49),'dark_metal')
            _hose_reel(a,lo+.70,0,1.65,.33,.47)
            for x in (lo-.12,L/2+.27):
                a.box((x,0,.34),(.19,1.67,.13),'metal')
                for s in (-1,1):
                    a.beam((x,s*.66,.78),(x,s*.66,.27),.09,mat='dark_metal')
                    a.cylinder((x,s*.67,.23),(x,s*.79,.23),.23,'steel',sides=10)
                    a.cylinder((x,s*.785,.23),(x,s*.82,.23),.255,'dark_metal',sides=10)
            a.box((lo+.09,0,1.47),(.10,W*.85,.80),'white')
    elif kind in ('sewer_vacuum_truck','water_spray_truck','fuel_delivery_tanker'):
        if kind=='sewer_vacuum_truck':
            _tank(a,lo+.43,hi-.26,2.14,1.03,'concrete_light')
            _hose_reel(a,hi+.05,-.31,1.48,.62,.73,axis='x')
            a.cylinder((lo+.01,0,2.14),(lo-.19,0,2.14),.97,'metal',sides=12)
            for j in range(8):
                t=2*math.pi*j/8
                a.box((lo-.22,.92*math.cos(t),2.14+.92*math.sin(t)),(.07,.095,.095),'dark_metal')
            # Parked vacuum boom runs over tank and drops to the rear inlet.
            a.tube([(hi-.22,.52,2.58),(hi-.22,.52,3.55),(lo+.36,.52,3.55),(lo-.36,.52,2.92)],.14,'dark_metal',sides=8)
            for x in (lo+1.1,hi-1.0): a.box((x,.53,3.21),(.12,.36,.46),'metal')
            a.cylinder((lo-.28,0,1.59),(lo-.51,0,1.59),.19,'black',sides=10)
            _beacon(a,hi+.87,0,H+.04)
        elif kind=='water_spray_truck':
            _tank(a,lo+.3,hi,2.03,.90,'white')
            for s in (-1,1): a.box((mid,s*.913,2.03),(hi-lo-.75,.024,.17),'blue')
            a.tube([(hi-.28,-.85,1.17),(lo-.24,-.85,1.17),(lo-.24,.85,1.17)],.072,'metal',sides=8)
            for y in (-.78,0,.78):
                a.cylinder((lo-.24,y,1.18),(lo-.38,y,.94),.05,'metal',sides=8,radius2=.09)
            _hose_reel(a,hi-.53,0,3.07,.26,.48)
            a.cylinder((lo-.14,0,1.1),(lo-.14,0,2.85),.055,'silver',sides=8)
            for z in (1.22,1.62,2.02,2.42): a.box((lo-.16,0,z),(.09,.50,.035),'metal')
        else:
            _tank(a,lo+.21,hi,2.15,1.02,'silver')
            for x in (lo+.85,mid,hi-.60):
                a.cylinder((x,0,3.16),(x,0,3.30),.22,'metal',sides=10)
                a.box((x,0,3.35),(.47,.46,.08),'dark_metal')
            a.box((mid,.74,3.10),(hi-lo-.1,.47,.08),'metal')
            for x in (lo+.35,hi-.24): a.box((x,.96,3.37),(.045,.045,.56),'metal')
            a.box((mid,.96,3.66),(hi-lo-.59,.045,.045),'metal')
            a.box((mid,-W*.46,1.17),(hi-lo-.4,.20,.19),'dark_metal')
            for x in (lo+.9,mid,hi-.66):
                a.cylinder((x,-.86,1.30),(x,-1.20,1.30),.08,'silver',sides=8)
                a.torus((x,-1.22,1.30),.13,.02,'red',axis='y',segments=8,sides=4)
            _hose_reel(a,lo+.46,0,1.06,.30,.70)
            for s in (-1,1): a.box((mid,s*1.035,2.25),(.30,.028,.30),'orange',rot=(0,0,0))
    elif kind in ('rear_loader_refuse_truck','front_loader_refuse_truck','automated_side_loader_refuse_truck','split_body_recycling_truck'):
        # Faceted compactor body, deep lower sill and hydraulic packer hardware.
        bh=3.35;back=lo+.69 if kind=='rear_loader_refuse_truck' else lo
        _profile(a,[(back,1.04),(hi,1.04),(hi,2.98),(hi-.26,bh),(back+.26,bh),(back,bh-.32)],W*.96,'green' if kind!='split_body_recycling_truck' else 'blue')
        for s in (-1,1):
            a.box(((back+hi)/2,s*(W/2-.01),1.24),(hi-back,.11,.28),'dark_metal')
            for x in (back+.29,hi-.31): a.box((x,s*(W/2-.011),2.16),(.12,.055,1.91),'metal')
            a.box((mid,s*(W/2+.018),2.14),(hi-lo-1.1,.024,.10),'white')
        if kind=='rear_loader_refuse_truck':
            # Hopper has a visibly open mouth and sloping packer lip.
            for s in (-1,1):
                _profile(a,[(lo-.43,1.09),(lo+.72,1.02),(lo+.72,3.17),(lo+.25,2.96),(lo-.43,1.81)],.21,'green',s*(W/2-.17))
                a.beam((lo+.31,s*(W/2-.05),2.89),(lo-.13,s*(W/2-.05),1.70),.08,mat='silver')
                a.box((lo-.37,s*.78,.91),(.42,.36,.10),'metal')
            a.box((lo+.29,0,1.81),(.08,W*.74,1.07),'black')
            _profile(a,[(lo-.42,1.09),(lo+.46,1.16),(lo+.51,1.40),(lo-.33,1.31)],W*.80,'metal')
            a.box((lo-.38,0,1.54),(.10,W*.86,.20),'dark_metal')
            for y in (-.46,.46): a.beam((lo-.43,y,1.31),(lo-.57,y,1.95),.06,mat='metal')
        elif kind=='front_loader_refuse_truck':
            # Paired lifting arms arch above the cab to a forward fork carriage.
            for s in (-1,1):
                yy=s*(W/2+.11)
                a.beam((hi-.68,yy,1.66),(hi-.51,yy,3.53),.20,.17,'green')
                a.beam((hi-.51,yy,3.53),(L/2+.20,yy,3.53),.19,.16,'green')
                a.beam((L/2+.20,yy,3.53),(L/2+.66,yy,2.19),.18,.16,'green')
                a.beam((hi-.44,yy,1.31),(hi+.03,yy,3.19),.095,mat='silver')
                a.beam((L/2+.65,yy,2.21),(L/2+.66,s*.78,2.21),.12,mat='dark_metal')
                a.box((L/2+1.00,s*.77,2.14),(.84,.13,.11),'dark_metal')
            a.box((hi-.69,0,3.43),(1.40,W*.78,.11),'dark_metal')
        elif kind=='automated_side_loader_refuse_truck':
            x=hi-.70;yy=-W/2-.12
            a.box((x,yy,1.74),(.72,.19,1.30),'dark_metal')
            a.beam((x,yy,1.40),(x-.10,yy-.48,1.03),.15,.13,'green')
            a.beam((x-.10,yy-.48,1.03),(x+.34,yy-.66,1.48),.13,.12,'green')
            a.cylinder((x-.13,yy-.58,1.08),(x+.23,yy-.62,1.38),.055,'silver',sides=8)
            for xx in (x-.02,x+.71):
                a.beam((xx,yy-.67,1.51),(xx,yy-.92,1.51),.10,mat='dark_metal')
            a.box((x+.35,yy-.68,1.52),(.78,.09,.16),'dark_metal')
            a.box((hi-.62,0,3.35),(1.13,W*.75,.11),'black')
        else:
            # Two separate streams, partitioned roof hoppers and curbside bins.
            a.box((mid,0,3.39),(hi-lo-.14,.13,.26),'dark_metal')
            for s in (-1,1):
                a.box((mid,s*.63,3.39),(hi-lo-.30,.89,.10),'blue')
                for x in (lo+.63,hi-.63):
                    a.box((x,s*(W/2+.061),2.68),(.67,.045,.56),'black')
                    a.box((x,s*(W/2+.091),2.37),(.75,.13,.10),'metal')
            for y in (-.57,.57):
                a.box((lo-.19,y,1.90),(.18,.95,1.48),'blue')
                a.box((lo-.29,y,1.24),(.05,.42,.09),'dark_metal')
        _beacon(a,hi+.82,0,H+.07)
    elif kind=='rolloff_container_truck':
        _bed(a,lo,hi,W,1.11)
        for y in (-.48,.48): a.box((mid,y,1.21),(hi-lo,.13,.15),'dark_metal')
        # Demountable open-top container with internal floor, deep corrugated walls.
        a.box((mid,0,1.35),(hi-lo-.2,W*.88,.13),'green')
        for s in (-1,1):
            a.box((mid,s*W*.44,2.25),(hi-lo-.12,.12,1.82),'green')
            a.box((mid,s*W*.45,3.16),(hi-lo,.15,.13),'dark_metal')
            for j in range(7):
                x=lo+.24+j*(hi-lo-.48)/6
                a.box((x,s*W*.465,2.25),(.09,.10,1.88),'green')
        for x in (lo+.05,hi-.05): a.box((x,0,2.23),(.13,W*.86,1.78),'green')
        a.box((hi-.02,0,3.17),(.14,W*.96,.14),'dark_metal')
        for y in (-.67,.67):
            a.cylinder((lo-.10,y-.12,1.28),(lo-.10,y+.12,1.28),.20,'metal',sides=10)
        a.beam((hi+.09,0,.97),(hi+.09,0,2.44),.22,mat='dark_metal')
        a.beam((hi+.09,0,2.44),(hi-.15,0,2.55),.15,mat='dark_metal')
        a.cylinder((hi-.81,0,.79),(hi-.15,0,1.88),.10,'silver',sides=8)
    elif kind in ('commercial_box_truck','refrigerated_delivery_truck'):
        _cargo_box(a,lo,hi,W,2.35,'white',kind=='refrigerated_delivery_truck')
        # Rear liftgate folds upright below the double cargo doors.
        a.box((lo-.18,0,1.06),(.12,W*.82,.66),'metal')
        for y in (-W*.34,W*.34):
            a.beam((lo+.08,y,.54),(lo-.22,y,1.20),.075,mat='dark_metal')
        if kind=='commercial_box_truck':
            for s in (-1,1):
                a.box((hi+.63,s*W*.35,H+.14),(1.04,.05,.35),'white',rot=(0,.30,0))
            _profile(a,[(hi+.15,H),(hi+1.33,H),(hi+.29,3.36),(hi+.15,3.36)],W*.89,'white')
        else:
            a.box((mid,-W/2-.04,2.14),(1.10,.055,1.85),'white')
            a.box((mid+.36,-W/2-.09,1.95),(.04,.04,.27),'dark_metal')
            a.box((mid,-W/2-.14,.96),(1.07,.32,.12),'metal')
    elif kind=='beverage_delivery_truck':
        a.box((mid,0,2.09),(hi-lo,W,2.09),'blue')
        for s in (-1,1):
            for j in range(5):
                x=lo+(j+.5)*(hi-lo)/5;dw=(hi-lo)/5-.065
                a.box((x,s*(W/2+.020),2.12),(dw,.04,1.96),'silver')
                for k in range(7): a.box((x,s*(W/2+.046),1.24+k*.26),(dw-.025,.025,.023),'metal')
                a.box((x,s*(W/2+.065),1.34),(.17,.029,.055),'dark_metal')
            a.box((mid,s*(W/2+.12),1.01),(hi-lo+.03,.26,.13),'dark_metal')
        a.box((mid,0,3.17),(hi-lo+.03,W+.06,.13),'blue')
        # Folding hand-truck holder on the tail, with dolly wheels.
        for y in (-.28,.28):
            a.beam((lo-.20,y,1.03),(lo-.20,y,2.25),.045,mat='metal')
            a.cylinder((lo-.20,y-.055,1.09),(lo-.20,y+.055,1.09),.14,'rubber',sides=8)
        for z in (1.22,1.61,2.04): a.box((lo-.20,0,z),(.045,.56,.045),'metal')
        a.box((lo-.32,0,1.12),(.28,.58,.065),'metal')
    elif kind=='flatbed_stake_truck':
        _bed(a,lo,hi,W,1.09,'wood_dark')
        for s in (-1,1):
            for j in range(5):
                x=lo+.08+j*(hi-lo-.16)/4
                a.box((x,s*(W/2-.06),1.68),(.07,.07,1.20),'dark_metal')
            for z in (1.37,1.77,2.17): a.box((mid,s*(W/2-.05),z),(hi-lo,.085,.23),'wood')
        for x in (lo+.04,hi-.04):
            for z in (1.37,1.77,2.17): a.box((x,0,z),(.09,W*.94,.23),'wood')
        for y in (-W*.35,0,W*.35): a.box((hi-.08,y,1.83),(.065,.075,1.60),'dark_metal')
        a.box((hi-.08,0,2.63),(.08,W*.96,.07),'dark_metal')
    elif kind in ('municipal_dump_truck','snowplow_spreader_truck'):
        _bed(a,lo,hi,W,1.14)
        if kind=='municipal_dump_truck':
            # Tapered open dump body, over-cab shield and hinged tailgate.
            a.box((mid,0,1.29),(hi-lo-.12,W*.74,.18),'dark_metal')
            for s in (-1,1):
                a.mesh([(lo,s*W*.36,1.22),(hi,s*W*.36,1.22),(hi,s*W*.49,2.58),(lo,s*W*.49,2.58),
                        (lo,s*W*.39,1.22),(hi,s*W*.39,1.22),(hi,s*W*.52,2.58),(lo,s*W*.52,2.58)],
                       [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)] if s<0 else [(3,2,1,0),(4,5,6,7),(1,5,4,0),(2,6,5,1),(3,7,6,2),(0,4,7,3)],'orange')
                for j in range(5):
                    x=lo+.15+j*(hi-lo-.30)/4
                    a.beam((x,s*W*.39,1.31),(x,s*W*.52,2.55),.075,mat='orange')
                a.box((mid,s*W*.51,2.61),(hi-lo+.04,.11,.12),'dark_metal')
            a.box((lo-.018,0,1.96),(.12,W*.91,1.32),'orange')
            for y in (-.83,0,.83): a.box((lo-.085,y,1.95),(.06,.075,1.22),'dark_metal')
            a.box((hi,0,2.11),(.13,W*.94,1.66),'orange')
            a.box((hi+.47,0,2.96),(.99,W*.96,.16),'orange')
            a.cylinder((hi-.26,0,.75),(hi-.64,0,1.29),.13,'silver',sides=8)
            for y in (-.8,.8): a.cylinder((lo-.10,y-.10,2.60),(lo-.10,y+.10,2.60),.08,'metal',sides=8)
        else:
            # Open V hopper, top grate, auger discharge and broad curved plow.
            _profile(a,[(lo+.1,1.47),(hi-.1,1.47),(hi-.1,2.90),(lo+.1,2.90)],.85,'orange')
            for s in (-1,1):
                a.beam((lo+.15,s*.37,1.46),(lo+.15,s*1.08,2.84),.085,mat='metal')
                a.beam((hi-.15,s*.37,1.46),(hi-.15,s*1.08,2.84),.085,mat='metal')
                _pane(a,[(lo+.1,s*.40,1.47),(hi-.1,s*.40,1.47),(hi-.1,s*1.07,2.89),(lo+.1,s*1.07,2.89)],'orange',reverse=s>0)
                a.box((mid,s*1.07,2.92),(hi-lo,.11,.13),'dark_metal')
            for j in range(9): a.box((lo+.15+j*(hi-lo-.30)/8,0,2.95),(.04,2.13,.04),'metal')
            a.box((lo-.22,0,1.24),(.63,.47,.66),'dark_metal')
            a.cylinder((lo-.24,0,.78),(lo-.24,0,.92),.45,'metal',sides=12)
            for s in (-1,1): a.beam((L/2-.01,s*.48,.66),(L/2+.86,s*.48,.56),.12,mat='dark_metal')
            # Three slope bands approximate the mouldboard's concave section.
            px=L/2+1.13
            for z,xx,tilt in ((.40,px-.02,-.45),(.73,px-.04,-.12),(1.05,px-.16,.35)):
                a.box((xx,0,z),(.12,3.13,.39),'orange',rot=(0,tilt,.13))
            a.box((px+.03,0,.22),(.12,3.20,.15),'dark_metal',rot=(0,0,.13))
            for s in (-1,1):
                a.cylinder((px-.21,s*1.38,1.11),(px-.21,s*1.38,1.73),.018,'orange',sides=6)
            _beacon(a,hi+.88,0,H+.06)
    elif kind=='glass_transport_truck':
        _bed(a,lo,hi,W,1.10)
        # Two A-frame racks carry separate green-blue glass panes at a safe inward lean.
        for x in (lo+.32,hi-.29):
            for s in (-1,1): a.beam((x,s*.96,1.17),(x,s*.14,2.91),.075,mat='dark_metal')
            a.beam((x,-.96,1.17),(x,.96,1.17),.075,mat='dark_metal')
        a.box((mid,0,2.92),(hi-lo-.44,.16,.12),'dark_metal')
        for s in (-1,1):
            for j in range(3):
                x=lo+.40+(j+.5)*(hi-lo-.80)/3
                a.box((x,s*.57,2.06),((hi-lo-.80)/3-.05,.045,1.79),'glass',rot=(s*.42,0,0))
            for x in (lo+.52,hi-.52): a.beam((x,s*1.0,1.22),(x,s*.18,2.93),.045,mat='wood_dark')
            a.box((mid,s*.99,1.17),(hi-lo-.18,.18,.10),'wood')
        a.box((hi-.02,0,1.55),(.13,W*.90,.78),'white')
    elif kind=='tree_service_chip_truck':
        # Tall enclosed chip box, sloping roof, vented sides and rear discharge flap.
        _profile(a,[(lo,1.12),(hi,1.12),(hi,3.18),(hi-.36,3.38),(lo,3.03)],W,'white')
        for s in (-1,1):
            for j in range(7):
                x=lo+.25+j*(hi-lo-.50)/6
                a.box((x,s*(W/2+.02),2.76),(.07,.025,.34),'dark_metal')
            for x in (lo+.14,mid,hi-.14): a.box((x,s*(W/2+.017),1.92),(.06,.026,1.57),'metal')
        a.box((lo-.06,0,2.18),(.09,W*.86,1.74),'white')
        a.box((lo-.116,0,2.52),(.028,W*.55,.73),'black')
        a.box((lo-.15,0,2.56),(.035,W*.58,.72),'rubber',rot=(0,.09,0))
        for y in (-.82,.82): a.box((lo-.14,y,1.43),(.04,.13,.055),'dark_metal')
        a.box((mid,0,1.02),(hi-lo-.2,W*.70,.13),'dark_metal')
        a.box((lo-.40,0,.64),(.58,.12,.12),'dark_metal')
        a.sphere((lo-.68,0,.70),.065,'steel',segments=8,rings=3)
        _beacon(a,hi+.86,0,H+.045)
    elif kind=='street_marking_truck':
        _bed(a,lo,hi,W)
        # Paint reservoirs, compressed-air plant, crew platform and curbside spray carriage.
        for x in (hi-.67,hi-1.73):
            a.cylinder((x,0,1.15),(x,0,2.24),.45,'white',sides=10)
            a.cylinder((x,0,2.24),(x,0,2.33),.33,'metal',sides=10)
        a.cylinder((lo+.83,-.54,1.51),(lo+.83,.54,1.51),.29,'orange',sides=10)
        a.box((lo+.83,0,1.95),(.81,.70,.32),'dark_metal')
        _hose_reel(a,mid-.27,-.79,1.69,.28,.33)
        for s in (-1,1):
            a.beam((lo+.13,s*W*.46,1.12),(lo+.13,s*W*.46,2.04),.04,mat='metal')
            a.beam((lo+.13,s*W*.46,2.04),(lo+1.16,s*W*.46,2.04),.04,mat='metal')
        a.box((lo+.21,0,1.47),(.42,.51,.12),'black')
        a.box((lo+.05,0,1.75),(.10,.51,.48),'black')
        a.beam((mid,-.98,.91),(mid,-1.72,.42),.08,mat='dark_metal')
        a.box((mid,-1.74,.39),(.82,.23,.11),'metal')
        for x in (mid-.30,mid+.30):
            a.cylinder((x,-1.74,.39),(x,-1.74,.19),.035,'metal',sides=6,radius2=.07)
        a.tube([(hi-.66,-.34,1.52),(mid,-1.12,1.08),(mid,-1.71,.44)],.037,'black',sides=6)
        for x in (lo+.24,hi-.21): _beacon(a,x,0,2.39)
        a.box((lo-.09,0,2.25),(.08,1.72,.58),'dark_metal')
        for y in (-.65,-.32,0,.32,.65): a.cylinder((lo-.14,y,2.25),(lo-.17,y,2.25),.083,'orange',sides=8)
    elif kind=='airport_crash_tender':
        # Broad low airport body, side pump cabinets and roof-mounted foam cannon.
        _profile(a,[(lo,1.05),(hi,1.05),(hi,2.68),(hi-.4,3.00),(lo+.37,3.00),(lo,2.67)],W*.99,'yellow')
        for s in (-1,1):
            for j in range(4):
                x=lo+(j+.5)*(hi-lo)/4
                a.box((x,s*(W/2+.012),1.78),((hi-lo)/4-.12,.035,1.16),'metal')
                for k in range(4): a.box((x,s*(W/2+.035),1.39+k*.24),((hi-lo)/4-.15,.012,.022),'dark_metal')
            a.box((mid,s*(W/2+.04),2.61),(hi-lo-.22,.029,.17),'red')
        a.cylinder((hi-.28,0,3.02),(hi-.28,0,3.37),.29,'dark_metal',sides=10)
        a.cylinder((hi-.28,0,3.37),(hi+.64,0,3.57),.13,'metal',sides=8,radius2=.095)
        a.cylinder((hi+.64,0,3.57),(hi+1.0,0,3.64),.11,'black',sides=8,radius2=.065)
        _lightbar(a,L/2-1.22,H+.10,1.9)
        a.box((L/2+.25,0,.91),(.31,W*.96,.24),'black')
        a.cylinder((L/2+.31,0,1.08),(L/2+.61,0,1.13),.10,'metal',sides=8)
        for y in (-.78,.78):
            a.cylinder((hi-.75,y,3.02),(hi-.75,y,3.14),.24,'dark_metal',sides=10)
        a.box((lo-.12,0,2.05),(.10,.68,1.65),'dark_metal')
        for z in (1.44,1.81,2.18,2.55): a.box((lo-.20,0,z),(.10,.69,.045),'silver')
    else:
        raise ValueError(kind)
    return a.bottom_center()


BUS_KINDS = (
    'low_floor_transit_bus','articulated_transit_bus','conventional_school_bus',
    'short_school_bus','paratransit_shuttle_bus','intercity_motor_coach',
    'open_top_tour_bus','airport_shuttle_bus','mobile_command_bus','mobile_library_bus')

KINDS = (
    'low_floor_transit_bus',
    'articulated_transit_bus',
    'conventional_school_bus',
    'short_school_bus',
    'paratransit_shuttle_bus',
    'intercity_motor_coach',
    'open_top_tour_bus',
    'airport_shuttle_bus',
    'modular_ambulance',
    'van_ambulance',
    'fire_pumper_engine',
    'aerial_ladder_fire_truck',
    'tiller_ladder_fire_truck',
    'heavy_rescue_squad',
    'wildland_brush_fire_truck',
    'fire_water_tender',
    'mobile_command_bus',
    'prisoner_transport_truck',
    'armored_security_truck',
    'tactical_rescue_truck',
    'rollback_tow_truck',
    'wheel_lift_tow_truck',
    'heavy_recovery_wrecker',
    'bucket_utility_truck',
    'cable_spool_utility_truck',
    'line_maintenance_service_truck',
    'sewer_vacuum_truck',
    'water_spray_truck',
    'rear_loader_refuse_truck',
    'front_loader_refuse_truck',
    'automated_side_loader_refuse_truck',
    'split_body_recycling_truck',
    'rolloff_container_truck',
    'commercial_box_truck',
    'refrigerated_delivery_truck',
    'parcel_step_van',
    'postal_walkin_truck',
    'beverage_delivery_truck',
    'food_service_truck',
    'ice_cream_truck',
    'flatbed_stake_truck',
    'municipal_dump_truck',
    'fuel_delivery_tanker',
    'glass_transport_truck',
    'tree_service_chip_truck',
    'snowplow_spreader_truck',
    'street_marking_truck',
    'mobile_library_bus',
    'airport_crash_tender',
    'hi_rail_utility_truck',
)

assert len(KINDS)==50 and len(set(KINDS))==50
for _kind in KINDS:
    _name='b15_'+_kind
    register(_name,CAT,'large',lambda n=_name,k=_kind: _make_fleet(n,k))
