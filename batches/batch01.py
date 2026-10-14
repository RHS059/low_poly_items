"""Fifty individually designed North-American public-space furniture props.

Geometry uses metres, a grounded origin, Z-up, and intentionally economical
facets.  Small hardware and construction details are modelled, never textures.
"""
import math
from assetlib import Asset, register

M='dark_metal'
S='steel'
W='wood'
C='concrete'
B='blue'
G='glass'
Y='yellow'
R='red'
K='black'
WHITE='white'


def box(a, p, s, m=M): a.box(p, s, mat=m)
def rod(a, p, q, r=.025, m=M, n=8): a.cylinder(p,q,r,mat=m,sides=n)
def ball(a,p,r,m=M): a.sphere(p,r,mat=m,segments=8,rings=4)
def ring(a,p,r,t=.018,m=M,axis='z',n=12): a.torus(p,r,t,mat=m,axis=axis,segments=n,sides=6)
def tube(a,pts,r=.025,m=M,n=8):
    for p,q in zip(pts[:-1],pts[1:]): rod(a,p,q,r,m,n)
def foot(a,x,y,r=.09):
    a.cylinder((x,y,.006),(x,y,.024),r,mat=M,sides=8)
    for dx,dy in ((r*.6,0),(-r*.6,0),(0,r*.6),(0,-r*.6)):
        rod(a,(x+dx,y+dy,.023),(x+dx,y+dy,.035),.009,S,6)
def wood_seat(a, length=1.8, depth=.48,z=.47,y=0,back=True):
    for i in range(5): box(a,(0,y-depth/2+(i+.5)*depth/5,z),(length,depth/5-.012,.052),W)
    for x in (-length*.37,length*.37):
        tube(a,[(x,y-depth*.32,.02),(x,y-depth*.32,z-.06),(x,y+depth*.36,z-.06)],.032)
        rod(a,(x,y+depth*.34,.02),(x,y+depth*.34,1.01 if back else z-.04),.032)
        foot(a,x,y-depth*.32);foot(a,x,y+depth*.34)
    if back:
        for z1 in (.64,.77,.90): box(a,(0,y+depth*.41,z1),(length,.055,.105),W)
def bench_arms(a,length=1.8,depth=.48):
    for x in (-length*.47,length*.47):
        tube(a,[(x,-depth*.35,.49),(x,-depth*.35,.71),(x,depth*.34,.71),(x,depth*.34,.49)],.025)
def rounded_u(a,x,y,width,height,r=.03,m=M,plane='x'):
    if plane=='x':
        pts=[(x-width/2,y,.04),(x-width/2,y,height-.13),(x-width/2+.06,y,height-.035),(x-width/2+.13,y,height),(x+width/2-.13,y,height),(x+width/2-.06,y,height-.035),(x+width/2,y,height-.13),(x+width/2,y,.04)]
    else:
        pts=[(x,y-width/2,.04),(x,y-width/2,height-.13),(x,y-width/2+.06,height-.035),(x,y-width/2+.13,height),(x,y+width/2-.13,height),(x,y+width/2-.06,height-.035),(x,y+width/2,height-.13),(x,y+width/2,.04)]
    tube(a,pts,r,m)
def disk(a,p,r,h,m=S,n=12): rod(a,(p[0],p[1],p[2]-h/2),(p[0],p[1],p[2]+h/2),r,m,n)
def bowl(a,x,y,z,r=.21,m=S):
    # Four contour rings make a recessed, open basin with a solid underside.
    contours=[(r*.64,z-.085),(r,z),(r-.025,z-.008),(r*.50,z-.060)]
    vs=[(x+rr*math.cos(i*math.tau/12),y+rr*math.sin(i*math.tau/12),zz)
        for rr,zz in contours for i in range(12)]
    faces=[(j*12+i,j*12+(i+1)%12,(j+1)*12+(i+1)%12,(j+1)*12+i)
           for j in range(3) for i in range(12)]
    faces += [tuple(reversed(range(12))),tuple(range(36,48))]
    a.mesh(vs,faces,mat=m)
    ring(a,(x,y,z),r-.011,.016,m)
    disk(a,(x,y,z-.056),r*.47,.004,S)
    disk(a,(x,y,z-.052),.031,.006,M,8)
    for dx in (-.013,0,.013):box(a,(x+dx,y,z-.048),(.005,.041,.004),S)
    rod(a,(x,y+r*.25,z+.09),(x,y+r*.20,z+.07),.012,M,8)
    tube(a,[(x,y+r*.65,z),(x,y+r*.65,z+.095),(x,y+r*.28,z+.10)],.017,S)
def planked_disk(a,r,z,thick=.065,m=W,n=12,cx=0,cy=0):
    # Each board is clipped to the curved perimeter, rather than stair-stepping it.
    count=max(5,round(r*2/.14)); step=2*r/count
    for j in range(count):
        y0=-r+j*step+.0045;y1=-r+(j+1)*step-.0045;ym=(y0+y1)/2
        widths=[(r*r-y*y)**.5 for y in (y0,ym,y1)]
        points=[(-widths[0],y0),(widths[0],y0),(widths[1],ym),(widths[2],y1),(-widths[2],y1),(-widths[1],ym)]
        a.prism([(cx+x,cy+y) for x,y in points],z-thick/2,z+thick/2,m)
    for y in (-r*.47,r*.47):
        half=(r*r-y*y)**.5*.89
        box(a,(cx,cy+y,z-thick*.9),(2*half,.055,.048),M)

def table_slats(a,w,d,z,m=W):
    count=max(3,round(d/.13))
    for j in range(count): box(a,(0,-d/2+(j+.5)*d/count,z),(w,d/count-.012,.055),m)
def simple_shelter(a,w=3.1,d=1.4,roofz=2.45,glass=True):
    for x in (-w/2,w/2):
        for y in (-d/2,d/2):
            rod(a,(x,y,.025),(x,y,roofz),.047,S);foot(a,x,y)
    rod(a,(-w/2,-d/2,roofz),(w/2,-d/2,roofz),.055,S)
    rod(a,(-w/2,d/2,roofz),(w/2,d/2,roofz),.055,S)
    if glass:
        for x in (-w/3,0,w/3):
            box(a,(x,d/2,1.24),(w/3-.05,.018,2.20),G)
        for x in (-w/2,w/2): box(a,(x,0,1.24),(.018,d-.1,2.20),G)
        for x in (-w/6,w/6): rod(a,(x,d/2,.16),(x,d/2,roofz-.04),.021,S)
        for x in (-w/2,-w/6,w/6,w/2):
            for zz in (.30,2.05):
                box(a,(x,d/2-.017,zz),(.12,.042,.055),S)
                rod(a,(x,d/2-.043,zz),(x,d/2-.048,zz),.011,M,6)
        for x in (-w/2,w/2):
            for yy in (-d*.38,d*.38):
                box(a,(x,yy,.31),(.045,.10,.055),S)
                box(a,(x,yy,2.03),(.045,.10,.055),S)
        for x in (-w/2,w/2): rod(a,(x,-d/2,.18),(x,d/2,.18),.024,S)
        rod(a,(-w/2,d/2,.18),(w/2,d/2,.18),.024,S)
        for x in (-w/3,0,w/3): box(a,(x,d/2-.013,1.28),(.16,.012,.045),WHITE)
    for x in (-.65,.65): box(a,(x,d*.19,.25),(.065,.35,.46),M)
    for j in range(4): box(a,(0,d*.19-.15+j*.10,.50),(1.7,.087,.04),M)
    for x in (-.65,.65):
        box(a,(x,d*.19,.475),(.10,.41,.055),S)
        for yy in (-.08,.08):rod(a,(x,d*.19+yy,.501),(x,d*.19+yy,.529),.012,S,6)
    # Rear eave gutter and downspout with a bent outlet.
    box(a,(0,d/2+.06,roofz+.01),(w+.22,.10,.10),M)
    tube(a,[(w/2+.055,d/2+.05,roofz),(w/2+.055,d/2+.05,.20),(w/2+.13,d/2+.13,.08)],.027,S)

def b01_cast_iron_park_bench():
    a=Asset('b01_cast_iron_park_bench','bench','person')
    wood_seat(a);bench_arms(a)
    for x in (-.67,.67):
        ring(a,(x,.04,.27),.12,.021,M,axis='x')
        tube(a,[(x,-.13,.07),(x,.12,.43),(x,.15,.86)],.023)
    return a

def b01_backless_boardwalk_bench():
    a=Asset('b01_backless_boardwalk_bench','bench','person')
    for y in (-.18,0,.18): box(a,(0,y,.48),(2.15,.16,.10),W)
    for x in (-.73,.73):
        box(a,(x,0,.22),(.17,.42,.44),C)
        box(a,(x,0,.025),(.37,.54,.05),C)
        for y in (-.18,.18): rod(a,(x,y,.529),(x,y,.535),.017,S)
    return a

def b01_cantilever_concrete_bench():
    a=Asset('b01_cantilever_concrete_bench','bench','person')
    # A single cast shell has a eased front nose and a slightly reclined back.
    yz=[(-.31,.40),(-.30,.48),(-.26,.51),(.19,.51),(.27,1.035),(.32,1.06),(.38,1.045),(.30,.365),(-.27,.365)]
    n=len(yz);vs=[(x,y,z) for x in (-1.05,1.05) for y,z in yz]
    a.mesh(vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],C)
    for x in (-.61,.61):
        box(a,(x,.20,.19),(.23,.22,.38),C)
        box(a,(x,.20,.025),(.29,.28,.05),M)
    for x in (-.75,0,.75): box(a,(x,-.03,.513),(.012,.38,.007),M)
    return a

def b01_perforated_steel_bench():
    a=Asset('b01_perforated_steel_bench','bench','person')
    for y in (-.22,-.11,0,.11,.22): rod(a,(-.94,y,.47),(.94,y,.47),.026,B)
    for x in [i*.14 for i in range(-6,7)]:
        tube(a,[(x,-.22,.47),(x,.22,.47),(x,.26,.62),(x,.29,.94)],.018,B,6)
    for z in (.62,.75,.88,.97): rod(a,(-.95,.29,z),(.95,.29,z),.023,B)
    for x in (-.67,.67):
        tube(a,[(x,-.21,.02),(x,-.21,.43),(x,.23,.43),(x,.23,.02)],.035,S)
        foot(a,x,-.21);foot(a,x,.23)
    bench_arms(a)
    return a

def b01_rustic_split_log_bench():
    a=Asset('b01_rustic_split_log_bench','bench','person')
    for x in (-.68,.68):
        rod(a,(x,0,.04),(x,0,.35),.18,'wood_dark',9)
        for dy in (-.1,.1): rod(a,(x-.19,dy,.22),(x+.19,dy,.22),.016,M,6)
    # Split trunk: flat sawn seating surface over a faceted bark underside.
    yz=[(-.24,.48),(.24,.48),(.23,.38),(.17,.29),(0,.25),(-.17,.29),(-.23,.38)]
    vs=[(x,y,z) for x in (-1.04,1.04) for y,z in yz];n=len(yz)
    a.mesh(vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],mat=[W,W,W]+['wood_dark']*(n-1))
    for x in (-.71,.71): rod(a,(x,.15,.24),(x,.28,1.0),.06,'wood_dark',7)
    for z in (.75,.93):
        a.beam((-1,.25,z),(1,.25,z),.11,.09,mat=W)
        for x in (-.71,.71):rod(a,(x,.198,z),(x,.184,z),.013,M,6)
    for x in (-1.045,1.045):
        for rr in (.06,.10): ring(a,(x,0,.365),rr,.006,'wood_dark',axis='x',n=10)
    return a

def b01_curve_segment_park_bench():
    a=Asset('b01_curve_segment_park_bench','bench','person')
    def pt(t,r,z): return (r*math.sin(t),1.7-r*math.cos(t),z)
    for i in range(19):
        theta=-.8+i*(1.6/18)
        a.beam(pt(theta,1.48,.49),pt(theta,1.92,.49),.108,.052,mat=W)
        a.beam(pt(theta,1.46,.62),pt(theta,1.40,.96),.092,.045,mat=W)
    for i in range(18):
        t=-.80+i*(1.6/18);q=t+(1.6/18)
        for r,z in ((1.52,.42),(1.87,.42),(1.40,1.0)):
            rod(a,pt(t,r,z),pt(q,r,z),.027)
    for t in (-.66,0,.66):
        for r in (1.53,1.86):
            x,y,_=pt(t,r,0)
            rod(a,(x,y,.02),(x,y,.46),.032);foot(a,x,y)
    return a

def b01_hexagonal_tree_bench():
    a=Asset('b01_hexagonal_tree_bench','bench','large')
    for i in range(6):
        t=i*math.pi/3;q=(i+1)*math.pi/3
        for r in (.78,.90,1.02,1.14):
            rod(a,(r*math.cos(t),r*math.sin(t),.48),(r*math.cos(q),r*math.sin(q),.48),.054,W,4)
        x,y=1.01*math.cos(t),1.01*math.sin(t)
        rod(a,(x,y,.02),(x,y,.44),.055,M);foot(a,x,y)
        rod(a,(.77*math.cos(t),.77*math.sin(t),.49),(.72*math.cos(t),.72*math.sin(t),.91),.034,M)
        for z in (.71,.86): rod(a,(.72*math.cos(t),.72*math.sin(t),z),(.72*math.cos(q),.72*math.sin(q),z),.065,W,4)
    return a

def b01_wave_public_lounge_bench():
    a=Asset('b01_wave_public_lounge_bench','bench','person')
    yz=[(-.65,.18),(-.45,.30),(-.25,.44),(0,.48),(.22,.51),(.38,.65),(.46,.90),(.50,1.12)]
    for j in range(len(yz)-1):
        y,z=yz[j];yy,zz=yz[j+1]
        for k in range(3):
            f=k/3;yc=y+(yy-y)*f;zc=z+(zz-z)*f
            a.beam((-.75,yc,zc),(.75,yc,zc),.076,.048,mat=W)
    for x in (-.57,.57):
        tube(a,[(x,y,z-.06) for y,z in yz],.045,M)
        rod(a,(x,-.14,.02),(x,-.14,.40),.036,M);rod(a,(x,.40,.02),(x,.40,.62),.036,M)
    return a

def b01_memorial_wood_bench():
    a=Asset('b01_memorial_wood_bench','bench','person')
    wood_seat(a,1.95,.53,back=False);bench_arms(a,1.95,.53)
    for x in (-.86,.86):
        box(a,(x,.23,.71),(.075,.075,.67),W)
        ball(a,(x,.23,1.10),.058,W)
    for z in (.57,.98): box(a,(0,.23,z),(1.75,.075,.075),W)
    for i in range(9):
        x=(i-4)*.183;h=.45+.12*(1-abs(x)/.76)
        box(a,(x,.23,.59+h/2),(.14,.054,h),W)
    box(a,(0,.192,.915),(.36,.025,.12),'gold')
    for x in (-.145,.145): rod(a,(x,.171,.915),(x,.18,.915),.011,M,6)
    box(a,(0,-.005,.12),(1.5,.065,.075),W)
    return a

def b01_transit_leaning_rail():
    a=Asset('b01_transit_leaning_rail','public_seating','person')
    for x in (-.82,.82):
        rod(a,(x,.10,.03),(x,-.08,.86),.039,S);foot(a,x,.10)
    rod(a,(-1,-.08,.86),(1,-.08,.86),.10,B,8)
    rod(a,(-.86,.10,.27),(.86,.10,.27),.032,S)
    for x in (-.35,.35): ring(a,(x,-.08,.86),.104,.01,M,axis='x')
    return a

def b01_three_tier_bleachers():
    a=Asset('b01_three_tier_bleachers','public_seating','large')
    for j in range(3):
        y=j*.61;z=.47+j*.36
        box(a,(0,y,z),(3.25,.35,.06),S)
        if j: box(a,(0,y-.26,z-.31),(3.25,.30,.05),S)
        for x in (-1.28,0,1.28):
            rod(a,(x,y,.035),(x,y,z-.04),.033,M)
            rod(a,(x,y-.22,.035),(x,y+.21,z-.04),.025,M)
    for x in (-1.47,1.47):
        rod(a,(x,-.25,.055),(x,1.48,.055),.045,M)
        rod(a,(x,1.45,.05),(x,1.45,1.87),.033,M)
        rod(a,(x,-.15,.77),(x,1.45,1.87),.031,M)
    for z in (1.58,1.86): rod(a,(-1.47,1.45,z),(1.47,1.45,z),.032,M)
    return a

def b01_double_sided_station_bench():
    a=Asset('b01_double_sided_station_bench','bench','person')
    for sign in (-1,1):
        for j in range(4): box(a,(0,sign*(.12+j*.105),.47),(2.15,.09,.055),W)
        for z in (.65,.81,.97): box(a,(0,sign*.075,z),(2.15,.055,.12),W)
    for x in (-.77,.77):
        box(a,(x,0,.23),(.14,.82,.46),C)
        rod(a,(x,0,.48),(x,0,1.07),.042,M)
    rod(a,(-1.07,0,1.07),(1.07,0,1.07),.045,M)
    return a

def b01_classic_aframe_picnic_table():
    a=Asset('b01_classic_aframe_picnic_table','picnic_table','large')
    table_slats(a,1.85,.76,.77)
    for y in (-.63,.63):
        for dy in (-.08,.08): box(a,(0,y+dy,.45),(1.85,.145,.058),W)
    for x in (-.60,.60):
        for sign in (-1,1): rod(a,(x,sign*.67,.025),(x,sign*.26,.735),.075,W,4)
        box(a,(x,0,.39),(.12,1.54,.09),W)
    rod(a,(-.61,0,.23),(.61,0,.70),.044,W,4)
    rod(a,(.61,0,.23),(-.61,0,.70),.044,W,4)
    return a

def b01_accessible_end_picnic_table():
    a=Asset('b01_accessible_end_picnic_table','picnic_table','large')
    table_slats(a,2.5,.84,.79)
    for x in (-.64,.64):
        rod(a,(x,0,.04),(x,0,.75),.065,S)
        rod(a,(x,-.67,.045),(x,.67,.045),.055,S)
        rod(a,(x,-.37,.74),(x,.37,.74),.047,S)
    for y in (-.64,.64):
        for dy in (-.085,.085): box(a,(-.24,y+dy,.46),(1.70,.15,.06),W)
        for x in (-.68,.48): rod(a,(x,0,.15),(x,y,.42),.038,S)
    return a

def b01_square_four_stool_table():
    a=Asset('b01_square_four_stool_table','picnic_table','large')
    box(a,(0,0,.77),(.90,.90,.09),C)
    box(a,(0,0,.36),(.26,.26,.72),C)
    for x,y in ((.85,0),(-.85,0),(0,.85),(0,-.85)):
        disk(a,(x,y,.44),.235,.10,B,10)
        rod(a,(x,y,.035),(x,y,.39),.075,S)
        rod(a,(0,0,.10),(x,y,.10),.043,S)
        foot(a,x,y)
    return a

def b01_round_pedestal_picnic_table():
    a=Asset('b01_round_pedestal_picnic_table','picnic_table','large')
    planked_disk(a,.72,.77)
    rod(a,(0,0,.04),(0,0,.73),.105,M)
    disk(a,(0,0,.03),.34,.055,M)
    for deg in (45,135,225,315):
        t=math.radians(deg);x,y=1.02*math.cos(t),1.02*math.sin(t)
        planked_disk(a,.29,.46,cx=x,cy=y)
        rod(a,(x,y,.03),(x,y,.43),.07,M)
        rod(a,(0,0,.17),(x,y,.17),.044,M)
        foot(a,x,y)
    return a

def b01_concrete_checker_table():
    a=Asset('b01_concrete_checker_table','game_table','person')
    box(a,(0,0,.75),(.80,.80,.085),C)
    box(a,(0,0,.34),(.27,.27,.68),C)
    box(a,(0,0,.04),(.52,.52,.08),C)
    for i in range(8):
        for j in range(8):
            box(a,((i-3.5)*.069,(j-3.5)*.069,.796),(.067,.067,.006),K if (i+j)%2 else WHITE)
    for x in (-.80,.80):
        box(a,(x,0,.43),(.40,.45,.095),C)
        box(a,(x,0,.19),(.22,.27,.38),C)
    return a

def b01_outdoor_chess_pedestal_table():
    a=Asset('b01_outdoor_chess_pedestal_table','game_table','person')
    disk(a,(0,0,.76),.55,.10,C,8)
    rod(a,(0,0,.12),(0,0,.71),.14,C,8)
    disk(a,(0,0,.065),.35,.13,C,8)
    for i in range(8):
        for j in range(8): box(a,((i-3.5)*.072,(j-3.5)*.072,.814),(.07,.07,.01),W if (i+j)%2 else M)
    for x in (-.82,.82):
        disk(a,(x,0,.43),.24,.11,C,8)
        rod(a,(x,0,.04),(x,0,.375),.11,C,8)
        rod(a,(x,.19,.43),(x,.19,.78),.025,M)
        ring(a,(x,.19,.65),.14,.025,M,axis='y')
    return a

def b01_standing_barrel_community_table():
    a=Asset('b01_standing_barrel_community_table','outdoor_table','person')
    planked_disk(a,.66,1.05,.07)
    for i in range(12):
        t=i*math.tau/12;x,y=.30*math.cos(t),.30*math.sin(t)
        rod(a,(x*.80,y*.80,.035),(x,y,.53),.07,W,4)
        rod(a,(x,y,.53),(x*.80,y*.80,1.01),.07,W,4)
    for z,r in ((.17,.281),(.83,.29)):
        ring(a,(0,0,z),r,.033,M,n=12)
    ring(a,(0,0,.22),.51,.029,M,n=12)
    for i in range(4):
        t=i*math.pi/2;rod(a,(.23*math.cos(t),.23*math.sin(t),.22),(.51*math.cos(t),.51*math.sin(t),.22),.022,M)
    return a

def b01_hexagonal_family_picnic_table():
    a=Asset('b01_hexagonal_family_picnic_table','picnic_table','large')
    # Long parallel boards clipped against the hexagonal top boundary.
    for j in range(10):
        y0=(j-5)*.135+.005;y1=y0+.125
        x0=.81-abs(y0)/math.sqrt(3);x1=.81-abs(y1)/math.sqrt(3)
        a.prism([(-x0,y0),(x0,y0),(x1,y1),(-x1,y1)],.7475,.8125,W)
    for y in (-.39,.39): box(a,(0,y,.72),(1.10,.06,.065),M)
    for i in range(6):
        t=i*math.pi/3;q=t+math.pi/3
        rod(a,(1.07*math.cos(t),1.07*math.sin(t),.46),(1.07*math.cos(q),1.07*math.sin(q),.46),.14,W,4)
        tm=t+math.pi/6;x,y=.96*math.cos(tm),.96*math.sin(tm)
        rod(a,(x,y,.02),(x*.54,y*.54,.735),.053,M)
        rod(a,(x*.2,y*.2,.36),(x,y,.40),.046,M)
    ring(a,(0,0,.81),.044,.009,M,n=8)
    return a

def b01_decorative_cast_bollard():
    a=Asset('b01_decorative_cast_bollard','bollard','person')
    rod(a,(0,0,.055),(0,0,.81),.075,M,10)
    for z,r,h in ((.055,.145,.11),(.19,.105,.10),(.76,.102,.10),(.91,.095,.075)):
        disk(a,(0,0,z),r,h,M,10)
    ball(a,(0,0,.99),.104,M)
    for i in range(8):
        t=i*math.pi/4;x,y=.074*math.cos(t),.074*math.sin(t)
        rod(a,(x,y,.29),(x,y,.64),.010,S,6)
    return a

def b01_stainless_dome_bollard():
    a=Asset('b01_stainless_dome_bollard','bollard','person')
    rod(a,(0,0,.015),(0,0,.87),.11,S,12)
    ball(a,(0,0,.87),.109,S)
    ring(a,(0,0,.69),.110,.012,K)
    disk(a,(0,0,.027),.155,.054,S)
    for i in range(3):
        t=i*math.tau/3;rod(a,(.13*math.cos(t),.13*math.sin(t),.05),(.13*math.cos(t),.13*math.sin(t),.067),.012,M,6)
    return a

def b01_spherical_concrete_bollard():
    a=Asset('b01_spherical_concrete_bollard','bollard','person')
    disk(a,(0,0,.055),.32,.11,C,10)
    a.sphere((0,0,.40),.40,mat=C,segments=12,rings=8)
    ring(a,(0,0,.22),.333,.008,'concrete_light',n=12)
    return a

def b01_timber_trail_bollard():
    a=Asset('b01_timber_trail_bollard','bollard','person')
    box(a,(0,0,.48),(.18,.18,.96),W)
    box(a,(0,0,.98),(.21,.21,.045),M)
    box(a,(0,-.094,.77),(.115,.013,.065),Y)
    for z in (.17,.60): rod(a,(-.105,0,z),(.105,0,z),.015,S,6)
    disk(a,(0,0,.015),.16,.03,C,8)
    return a

def b01_flexible_lane_delineator():
    a=Asset('b01_flexible_lane_delineator','bollard','person')
    disk(a,(0,0,.035),.18,.07,K,8)
    rod(a,(0,0,.06),(0,0,.91),.065,Y,8)
    for z in (.60,.76): disk(a,(0,0,z),.067,.075,WHITE,8)
    ball(a,(0,0,.91),.066,Y)
    for x in (-.13,.13): rod(a,(x,0,.06),(x,0,.075),.016,S,6)
    return a

def b01_retractable_security_bollard():
    a=Asset('b01_retractable_security_bollard','bollard','person')
    disk(a,(0,0,.025),.235,.05,M,12)
    ring(a,(0,0,.051),.163,.026,S)
    rod(a,(0,0,.04),(0,0,.75),.138,S,12)
    for z in (.57,.69): disk(a,(0,0,z),.14,.035,R,12)
    disk(a,(0,0,.775),.145,.05,M,12)
    box(a,(0,0,.803),(.064,.016,.006),S)
    for x,y in ((.195,0),(-.195,0),(0,.195),(0,-.195)):
        rod(a,(x,y,.045),(x,y,.055),.012,S,6)
    return a

def b01_chain_linked_heritage_bollards():
    a=Asset('b01_chain_linked_heritage_bollards','bollard','large')
    for x in (-1.05,0,1.05):
        rod(a,(x,0,.03),(x,0,.77),.068,M)
        disk(a,(x,0,.05),.12,.10,M)
        disk(a,(x,0,.70),.09,.06,M)
        ball(a,(x,0,.84),.085,M)
    for offset in (-1.05,0):
        for j in range(15):
            f=(j+.5)/15;x=offset+f*1.05;z=.68-.18*math.sin(math.pi*f)
            ring(a,(x,0,z),.039,.009,M,axis='y' if j%2 else 'z',n=8)
    return a

def b01_fold_down_parking_bollard():
    a=Asset('b01_fold_down_parking_bollard','bollard','person')
    box(a,(0,0,.025),(.33,.25,.05),M)
    for x in (-.13,.13):
        for y in (-.085,.085): rod(a,(x,y,.05),(x,y,.066),.014,S,6)
    for x in (-.065,.065): box(a,(x,0,.115),(.028,.15,.15),S)
    rod(a,(-.093,0,.12),(.093,0,.12),.022,M)
    box(a,(0,0,.53),(.095,.095,.78),Y)
    for z in (.64,.78): box(a,(0,-.049,z),(.096,.006,.055),K)
    box(a,(0,-.066,.20),(.05,.028,.065),S)
    return a

def b01_inverted_u_bike_rack():
    a=Asset('b01_inverted_u_bike_rack','bike_rack','person')
    rounded_u(a,0,0,.90,.89,.037,S)
    foot(a,-.45,0);foot(a,.45,0)
    return a

def b01_serpentine_wave_bike_rack():
    a=Asset('b01_serpentine_wave_bike_rack','bike_rack','person')
    pts=[(-1.3,0,.03),(-1.3,0,.78),(-1.23,0,.9),(-1.1,0,.96),(-.97,0,.9),(-.9,0,.78),(-.9,0,.20),(-.82,0,.10),(-.65,0,.065),(-.48,0,.10),(-.40,0,.20),(-.4,0,.78),(-.33,0,.9),(-.20,0,.96),(-.07,0,.9),(0,0,.78),(0,0,.20),(.08,0,.10),(.25,0,.065),(.42,0,.10),(.5,0,.20),(.5,0,.78),(.57,0,.9),(.70,0,.96),(.83,0,.9),(.9,0,.78),(.9,0,.03)]
    tube(a,pts,.037,B);foot(a,-1.3,0);foot(a,.9,0)
    return a

def b01_five_slot_wheel_bike_rack():
    a=Asset('b01_five_slot_wheel_bike_rack','bike_rack','person')
    for y in (-.40,.40): rod(a,(-1.17,y,.075),(1.17,y,.075),.045,S)
    for x in (-1,-.5,0,.5,1):
        for dx in (-.045,.045):
            tube(a,[(x+dx,-.4,.08),(x+dx,-.14,.60),(x+dx,.14,.60),(x+dx,.4,.08)],.021,S)
    for x in (-1.08,1.08):
        rod(a,(x,-.47,.04),(x,.47,.04),.04,M)
        for y in (-.40,.40): foot(a,x,y)
    return a

def b01_post_and_ring_bike_rack():
    a=Asset('b01_post_and_ring_bike_rack','bike_rack','person')
    rod(a,(0,0,.04),(0,0,1.02),.048,M)
    ring(a,(0,0,.66),.35,.033,S,axis='y',n=16)
    foot(a,0,0,.13)
    disk(a,(0,0,1.035),.058,.035,M)
    for z in (.35,.97): box(a,(0,-.018,z),(.13,.042,.045),M)
    return a

def b01_spiral_bicycle_corral():
    a=Asset('b01_spiral_bicycle_corral','bike_rack','large')
    pts=[]
    for i in range(81):
        f=i/80;t=f*math.tau*5
        pts.append((-1.50+3*f,.33*math.cos(t),.41+.33*math.sin(t)))
    tube(a,pts,.026,S,6)
    for x in (-1.50,1.50):
        rod(a,(x,.33,.055),(x,.33,.41),.034,S)
        box(a,(x,0,.035),(.16,.85,.07),M)
    return a

def b01_double_hoop_bike_rack():
    a=Asset('b01_double_hoop_bike_rack','bike_rack','person')
    for x in (-.35,.35): ring(a,(x,0,.53),.47,.034,B,axis='y',n=16)
    for x in (-.35,.35):
        rod(a,(x,0,.025),(x,0,.15),.039,M);foot(a,x,0)
    rod(a,(-.35,0,.53),(.35,0,.53),.027,B)
    return a

def b01_vertical_bicycle_parking_stand():
    a=Asset('b01_vertical_bicycle_parking_stand','bike_rack','person')
    for x in (-.43,.43):
        box(a,(x,0,.045),(.15,.80,.09),M)
        rod(a,(x,.25,.08),(x,.25,1.86),.04,S)
        rod(a,(x,-.33,.08),(x,.25,1.00),.031,S)
    rod(a,(-.43,.25,1.84),(.43,.25,1.84),.046,S)
    for x in (-.23,.23):
        tube(a,[(x,.25,1.79),(x,-.12,1.79),(x,-.19,1.72),(x,-.19,1.59),(x,-.11,1.55),(x,-.05,1.59)],.019,R)
        for dx in (-.045,.045): rod(a,(x+dx,-.32,.11),(x+dx,.26,.11),.021,S)
    return a

def b01_dual_height_drinking_fountain():
    a=Asset('b01_dual_height_drinking_fountain','drinking_fountain','person')
    box(a,(0,0,.51),(.23,.22,1.02),M)
    disk(a,(0,0,.035),.23,.07,M)
    for x,z in ((-.31,.79),(.31,1.01)):
        box(a,(x*.55,0,z-.12),(.38,.16,.11),M)
        bowl(a,x,0,z,.20,S)
        rod(a,(x,-.193,z-.065),(x,-.213,z-.065),.021,S)
    box(a,(0,-.12,.52),(.095,.012,.19),S)
    return a

def b01_classic_pedestal_drinking_fountain():
    a=Asset('b01_classic_pedestal_drinking_fountain','drinking_fountain','person')
    disk(a,(0,0,.055),.23,.11,M,10)
    rod(a,(0,0,.1),(0,0,.83),.11,M,10)
    for z,r,h in ((.21,.135,.06),(.78,.15,.07)):
        disk(a,(0,0,z),r,h,M,10)
    bowl(a,0,0,.94,.245,S)
    for i in range(8):
        t=i*math.pi/4;rod(a,(.108*math.cos(t),.108*math.sin(t),.29),(.108*math.cos(t),.108*math.sin(t),.69),.01,S,6)
    rod(a,(0,-.11,.72),(0,-.145,.72),.03,S)
    return a

def b01_bottle_refill_station():
    a=Asset('b01_bottle_refill_station','drinking_fountain','person')
    box(a,(0,0,.075),(.48,.37,.15),M)
    box(a,(0,.095,.85),(.36,.16,1.55),B)
    for x in (-.19,.19): box(a,(x,-.04,1.25),(.045,.24,.63),S)
    box(a,(0,-.04,1.565),(.42,.24,.07),S)
    box(a,(0,-.045,.94),(.43,.32,.075),S)
    box(a,(0,.001,1.26),(.30,.018,.52),K)
    rod(a,(0,-.09,1.53),(0,-.09,1.46),.018,S)
    for x in (-.12,-.06,0,.06,.12): box(a,(x,-.074,.983),(.023,.20,.009),M)
    box(a,(0,-.001,1.42),(.045,.01,.025),WHITE)
    bowl(a,-.35,0,.80,.18,S)
    box(a,(-.23,.02,.69),(.28,.16,.10),B)
    box(a,(0,.006,.45),(.28,.02,.48),M)
    for x in (-.12,.12):
        for z in (.24,.66):rod(a,(x,-.008,z),(x,-.015,z),.007,S,6)
    for z in (.33,.38,.43):box(a,(0,-.008,z),(.16,.01,.012),K)
    return a

def b01_stone_spout_fountain():
    a=Asset('b01_stone_spout_fountain','drinking_fountain','person')
    for i in range(5): box(a,(0,0,.12+i*.21),(.39 if i%2 else .42,.39,.20),C)
    box(a,(0,0,1.11),(.49,.46,.09),C)
    bowl(a,0,-.22,.73,.25,C)
    tube(a,[(0,-.20,.99),(0,-.33,.99),(0,-.33,.92)],.027,S)
    ring(a,(.17,-.203,.94),.039,.012,S,axis='y',n=8)
    box(a,(0,-.18,.38),(.17,.28,.63),C)
    return a

def b01_people_and_pet_drinking_fountain():
    a=Asset('b01_people_and_pet_drinking_fountain','drinking_fountain','person')
    rod(a,(0,0,.06),(0,0,1.03),.13,B,10)
    disk(a,(0,0,.04),.23,.08,S)
    bowl(a,0,0,1.07,.225,S)
    rod(a,(0,-.02,.18),(.40,-.02,.18),.065,B)
    bowl(a,.43,-.02,.22,.185,S)
    rod(a,(0,-.13,.80),(0,-.16,.80),.028,S)
    rod(a,(.13,0,.35),(.17,0,.35),.022,S)
    for x in (-.15,.15): rod(a,(x,.10,.075),(x,.10,.09),.015,M,6)
    return a

def b01_glass_flat_roof_bus_shelter():
    a=Asset('b01_glass_flat_roof_bus_shelter','bus_shelter','large')
    simple_shelter(a)
    box(a,(0,0,2.49),(3.45,1.75,.13),M)
    box(a,(0,0,2.57),(3.29,1.58,.045),S)
    for x in (-1.20,0,1.20): box(a,(x,0,2.409),(.24,.48,.02),WHITE)
    return a

def b01_gabled_neighborhood_bus_shelter():
    a=Asset('b01_gabled_neighborhood_bus_shelter','bus_shelter','large')
    simple_shelter(a,3.0,1.5,2.2,False)
    for y in (-.79,.79): rod(a,(-1.68,y,2.23),(1.68,y,2.23),.065,M)
    rod(a,(-1.68,0,2.72),(1.68,0,2.72),.068,M)
    for x in (-1.5,0,1.5):
        tube(a,[(x,-.85,2.22),(x,0,2.74),(x,.85,2.22)],.055,M)
    roof_angle=math.atan2(.52,.85)
    for sign in (-1,1):
        a.box((0,sign*.425,2.48),(3.42,1.015,.070),mat=R,rot=(-sign*roof_angle,0,0))
        for j in range(9):
            x=-1.6+j*.4
            a.beam((x,0,2.768),(x,sign*.87,2.235),.024,.024,mat=M)
    for x in (-1.5,1.5):
        for y in (-.50,0,.50): rod(a,(x,y,.30),(x,y,1.55),.025,M)
        for z in (.30,1.55): rod(a,(x,-.75,z),(x,.75,z),.034,M)
    for x in (-1,-.5,0,.5,1): box(a,(x,.75,.94),(.40,.04,1.30),G)
    return a

def b01_cantilever_transit_shelter():
    a=Asset('b01_cantilever_transit_shelter','bus_shelter','large')
    for x in (-1.05,1.05):
        rod(a,(x,.45,.02),(x,.45,2.34),.09,S)
        foot(a,x,.45,.17)
        rod(a,(x,.45,1.83),(x,-.66,2.30),.056,S)
        rod(a,(x,-.80,2.34),(x,.66,2.34),.06,S)
    box(a,(0,-.08,2.40),(3.05,1.76,.10),B)
    box(a,(0,.48,1.2),(2.85,.025,2.17),G)
    for x in (-1.35,0,1.35): rod(a,(x,.49,.12),(x,.49,2.30),.025,S)
    for x in (-.88,.88): rod(a,(x,.4,.28),(x,.0,.55),.035,S)
    for j in range(4): box(a,(0,-.10+j*.10,.53),(2.0,.083,.04),W)
    rod(a,(-1.50,-.97,2.4),(1.50,-.97,2.4),.047,M)
    for x in (-1.35,0,1.35):
        for z in (.30,2.15):box(a,(x,.445,z),(.13,.05,.06),S)
    tube(a,[(1.39,.69,2.42),(1.39,.69,.23),(1.45,.77,.08)],.028,S)
    box(a,(0,.76,2.39),(3.04,.09,.10),M)
    return a

def b01_barrel_vault_bus_shelter():
    a=Asset('b01_barrel_vault_bus_shelter','bus_shelter','large')
    simple_shelter(a,3.2,1.45,2.15)
    for j in range(13):
        t=math.pi*j/13;q=math.pi*(j+1)/13
        p=(.89*math.cos(t),2.16+.47*math.sin(t))
        v=(.89*math.cos(q),2.16+.47*math.sin(q))
        length=math.hypot(v[0]-p[0],v[1]-p[1])
        tilt=math.atan2(v[1]-p[1],v[0]-p[0])
        a.box((0,(p[0]+v[0])/2,(p[1]+v[1])/2),(3.54,length+.003,.055),mat=B,rot=(tilt,0,0))
    for x in (-1.72,0,1.72):
        pts=[]
        for j in range(15):
            t=math.pi*j/14;pts.append((x,.90*math.cos(t),2.16+.48*math.sin(t)))
        tube(a,pts,.036,S)
    for y in (-.91,.91): rod(a,(-1.77,y,2.16),(1.77,y,2.16),.045,S)
    return a

def b01_louvered_shade_transit_shelter():
    a=Asset('b01_louvered_shade_transit_shelter','bus_shelter','large')
    simple_shelter(a,2.8,1.5,2.3,False)
    for x in (-1.40,1.40):
        for j in range(11): box(a,(x,.12,.30+j*.15),(.07,1.21,.08),W)
    for i in range(20): box(a,(-1.52+i*.16,0,2.37),(.095,1.94,.13),W)
    for x in (-1.0,0,1.0): box(a,(x,.74,1.10),(.86,.06,1.59),M)
    for i in range(18):
        x=-1.25+i*.147
        rod(a,(x,.70,.50),(x,.70,1.72),.014,S,6)
    box(a,(0,0,.04),(3.10,1.91,.08),C)
    return a

def b01_concrete_cube_seating_cluster():
    a=Asset('b01_concrete_cube_seating_cluster','public_seating','person')
    for x,y,size in ((-.52,0,.45),(.08,.25,.50),(.64,-.08,.43)):
        box(a,(x,y,.025),(size*.80,size*.80,.05),M)
        box(a,(x,y,size/2+.045),(size,size,size),C)
        for j in range(4): box(a,(x,y-size/2+(j+.5)*size/4,size+.057),(size-.035,size/4-.009,.026),W)
    return a

def b01_sculpted_concrete_recliner():
    a=Asset('b01_sculpted_concrete_recliner','public_seating','person')
    yz=[(-.75,.19),(-.58,.33),(-.38,.44),(-.18,.45),(.03,.44),(.20,.56),(.33,.80),(.43,1.02)]
    profile=[(-.85,.02),(-.85,.16)]+yz+[(.48,1.02),(.48,.02)]
    n=len(profile)
    verts=[(x,y,z) for x in (-.345,.345) for y,z in profile]
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    a.mesh(verts,faces,mat=C)
    for x in (-.275,.275):
        tube(a,[(x,-.28,.48),(x,-.27,.68),(x,.22,.68),(x,.26,.48)],.027,S)
    return a

def b01_stone_semicircular_seat():
    a=Asset('b01_stone_semicircular_seat','public_seating','large')
    for i in range(12):
        t=math.pi*i/12+.002;q=math.pi*(i+1)/12-.002
        for ri,ro,z1,z2 in ((1.21,1.48,.02,.41),(1.09,1.60,.40,.51)):
            points=[(ri*math.cos(t),ri*math.sin(t)),(ro*math.cos(t),ro*math.sin(t)),
                    (ro*math.cos(q),ro*math.sin(q)),(ri*math.cos(q),ri*math.sin(q))]
            a.prism(points,z1,z2,mat=C)
        rod(a,(1.66*math.cos(t),1.66*math.sin(t),.81),(1.66*math.cos(q),1.66*math.sin(q),.81),.025,M)
    for t in (0,math.pi/2,math.pi):
        x,y=1.66*math.cos(t),1.66*math.sin(t)
        rod(a,(x,y,.02),(x,y,.88),.07,C,8)
        ball(a,(x,y,.93),.09,C)
    return a

def b01_planter_integrated_sidewalk_seat():
    a=Asset('b01_planter_integrated_sidewalk_seat','public_seating','large')
    for x in (-1.0,1.0):
        box(a,(x,0,.31),(.64,.64,.62),C)
        box(a,(x,0,.63),(.72,.72,.075),C)
        box(a,(x,0,.672),(.55,.55,.012),K)
        for dx,dy,h in ((-.10,-.08,.32),(.09,.07,.42),(.15,-.12,.26),(-.15,.13,.37)):
            rod(a,(x+dx,dy,.67),(x+dx*1.5,dy*1.5,.67+h),.015,'green',5)
            # Tapered lance leaves fold along a raised midrib.
            for k in range(3):
                t=k*math.tau/3+dx*8
                px=x+dx;py=dy; zz=.71
                ex=px+math.cos(t)*(.15+h*.22);ey=py+math.sin(t)*(.15+h*.22)
                a.mesh([(px,py,zz),(px-.038*math.sin(t),py+.038*math.cos(t),zz+h*.5),(ex,ey,zz+h),(px+.038*math.sin(t),py-.038*math.cos(t),zz+h*.5),(px,py,zz+h*.55)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],'green')
    for j in range(5): box(a,(0,-.24+j*.12,.47),(1.67,.10,.075),W)
    for x in (-.56,.56): box(a,(x,0,.40),(.10,.57,.10),M)
    return a

def b01_timber_chaise_public_seat():
    a=Asset('b01_timber_chaise_public_seat','public_seating','person')
    yz=[(-.84,.30),(-.59,.43),(-.33,.48),(-.05,.44),(.17,.49),(.34,.71),(.50,1.03)]
    for j in range(len(yz)-1):
        y,z=yz[j];yy,zz=yz[j+1]
        for k in range(3):
            f=(k+.5)/3
            a.beam((-.36,y+(yy-y)*f,z+(zz-z)*f),(.36,y+(yy-y)*f,z+(zz-z)*f),.079,.045,mat=W)
    for x in (-.29,.29):
        tube(a,[(x,y,z-.07) for y,z in yz],.034,M)
        tube(a,[(x,-.60,.34),(x,-.44,.025),(x,.25,.025),(x,.29,.54)],.04,M)
    rod(a,(-.28,-.44,.05),(.28,-.44,.05),.028,M)
    rod(a,(-.28,.25,.05),(.28,.25,.05),.028,M)
    return a


_FACTORIES = [
    (b01_cast_iron_park_bench,'bench','person'),
    (b01_backless_boardwalk_bench,'bench','person'),
    (b01_cantilever_concrete_bench,'bench','person'),
    (b01_perforated_steel_bench,'bench','person'),
    (b01_rustic_split_log_bench,'bench','person'),
    (b01_curve_segment_park_bench,'bench','person'),
    (b01_hexagonal_tree_bench,'bench','large'),
    (b01_wave_public_lounge_bench,'bench','person'),
    (b01_memorial_wood_bench,'bench','person'),
    (b01_transit_leaning_rail,'public_seating','person'),
    (b01_three_tier_bleachers,'public_seating','large'),
    (b01_double_sided_station_bench,'bench','person'),
    (b01_classic_aframe_picnic_table,'picnic_table','large'),
    (b01_accessible_end_picnic_table,'picnic_table','large'),
    (b01_square_four_stool_table,'picnic_table','large'),
    (b01_round_pedestal_picnic_table,'picnic_table','large'),
    (b01_concrete_checker_table,'game_table','person'),
    (b01_outdoor_chess_pedestal_table,'game_table','person'),
    (b01_standing_barrel_community_table,'outdoor_table','person'),
    (b01_hexagonal_family_picnic_table,'picnic_table','large'),
    (b01_decorative_cast_bollard,'bollard','person'),
    (b01_stainless_dome_bollard,'bollard','person'),
    (b01_spherical_concrete_bollard,'bollard','person'),
    (b01_timber_trail_bollard,'bollard','person'),
    (b01_flexible_lane_delineator,'bollard','person'),
    (b01_retractable_security_bollard,'bollard','person'),
    (b01_chain_linked_heritage_bollards,'bollard','large'),
    (b01_fold_down_parking_bollard,'bollard','person'),
    (b01_inverted_u_bike_rack,'bike_rack','person'),
    (b01_serpentine_wave_bike_rack,'bike_rack','person'),
    (b01_five_slot_wheel_bike_rack,'bike_rack','person'),
    (b01_post_and_ring_bike_rack,'bike_rack','person'),
    (b01_spiral_bicycle_corral,'bike_rack','large'),
    (b01_double_hoop_bike_rack,'bike_rack','person'),
    (b01_vertical_bicycle_parking_stand,'bike_rack','person'),
    (b01_dual_height_drinking_fountain,'drinking_fountain','person'),
    (b01_classic_pedestal_drinking_fountain,'drinking_fountain','person'),
    (b01_bottle_refill_station,'drinking_fountain','person'),
    (b01_stone_spout_fountain,'drinking_fountain','person'),
    (b01_people_and_pet_drinking_fountain,'drinking_fountain','person'),
    (b01_glass_flat_roof_bus_shelter,'bus_shelter','large'),
    (b01_gabled_neighborhood_bus_shelter,'bus_shelter','large'),
    (b01_cantilever_transit_shelter,'bus_shelter','large'),
    (b01_barrel_vault_bus_shelter,'bus_shelter','large'),
    (b01_louvered_shade_transit_shelter,'bus_shelter','large'),
    (b01_concrete_cube_seating_cluster,'public_seating','person'),
    (b01_sculpted_concrete_recliner,'public_seating','person'),
    (b01_stone_semicircular_seat,'public_seating','large'),
    (b01_planter_integrated_sidewalk_seat,'public_seating','large'),
    (b01_timber_chaise_public_seat,'public_seating','person'),
]
assert len(_FACTORIES) == 50
for _factory, _category, _size_class in _FACTORIES:
    register(_factory.__name__, _category, _size_class, _factory)
