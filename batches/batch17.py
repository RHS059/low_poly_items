"""Personal recreation and carry props; authored at real-world metre scale."""
import math
from itertools import combinations
from assetlib import Asset,register


def model(label, size='handheld'):
    def decorate(fn):
        name = 'b17_' + label
        def factory():
            a = Asset(name, 'personal_recreation_carry', size,
                      description=label.replace('_', ' '), batch=17)
            fn(a)
            return a.bottom_center()
        register(name, 'personal_recreation_carry', size, factory)
        return fn
    return decorate


def bevel(a, c, size, mat, cut=.15):
    x,y,z=size; h=x/2; d=y/2; b=min(x,y)*cut
    pts=[(-h+b,-d),(h-b,-d),(h,-d+b),(h,d-b),(h-b,d),(-h+b,d),(-h,d-b),(-h,-d+b)]
    a.prism([(c[0]+u,c[1]+v) for u,v in pts],c[2]-z/2,c[2]+z/2,mat)


def handle(a,x,y,z,w,h,mat='rubber',r=.014):
    a.beam((x-w/2,y,z),(x-w/2,y,z+h),r,r,mat)
    a.beam((x+w/2,y,z),(x+w/2,y,z+h),r,r,mat)
    a.beam((x-w/2,y,z+h),(x+w/2,y,z+h),r,r,mat)


def line(a,pts,r=.003,mat='cream',sides=4):
    a.tube(pts,r,mat,sides)


def wheel(a,x,y,z,r=.05,width=.028):
    a.cylinder((x-width/2,y,z),(x+width/2,y,z),r,'rubber',10)
    a.cylinder((x-width*.55,y,z),(x+width*.55,y,z),r*.45,'metal',8)


def dome(a, rx, ry, base, height, mat):
    """Closed shallow headwear shell with a contrasting underside."""
    n=12; vs=[]
    for j in range(3):
        lat=math.pi*j/6
        vs.extend((rx*math.cos(lat)*math.cos(2*math.pi*i/n),
                   ry*math.cos(lat)*math.sin(2*math.pi*i/n),
                   base+height*math.sin(lat)) for i in range(n))
    vs.append((0,0,base+height));fs=[tuple(reversed(range(n)))];m=['black']
    for j in range(2):
        for i in range(n):
            k=j*n+i;q=j*n+(i+1)%n
            fs.append((k,q,q+n,k+n));m.append(mat)
    for i in range(n):fs.append((24+i,24+(i+1)%n,36));m.append(mat)
    a.mesh(vs,fs,m)


def soft_shell(a,c,size,mat):
    """Tailored fabric silhouette with bulging panels and tucked base/crown."""
    w,d,h=size;vs=[]
    shape=[(-.72,-1),(.72,-1),(1,-.65),(1,.65),(.72,1),(-.72,1),(-1,.65),(-1,-.65)]
    for z,sx,sy in [(-.5,.78,.73),(-.37,.98,.98),(.12,1,1),(.37,.91,.91),(.5,.68,.65)]:
        vs.extend((c[0]+x*w*.5*sx,c[1]+y*d*.5*sy,c[2]+z*h) for x,y in shape)
    fs=[tuple(reversed(range(8)))]
    for j in range(4):
        fs.extend((j*8+i,j*8+(i+1)%8,(j+1)*8+(i+1)%8,(j+1)*8+i) for i in range(8))
    fs.append(tuple(range(32,40)));a.mesh(vs,fs,mat)


def shoe(a,boot=False):
    """Last-shaped upper, thin contoured sole, open padded collar and fitted laces."""
    color='brown' if boot else 'navy'
    outline=[(-.035,-.137),(.035,-.137),(.052,-.105),(.054,-.04),(.063,.055),(.053,.12),(.027,.147),(-.027,.147),(-.055,.12),(-.061,.05),(-.05,-.045),(-.05,-.11)]
    a.prism(outline,0,.018,'rubber')
    a.prism([(x*.98,y*.995) for x,y in outline],.018,.027,'sand' if boot else 'cream')
    sections=[(-.136,.028,.074),(-.105,.046,.105),(-.055,.049,.121),(-.005,.054,.096),(.055,.059,.07),(.113,.049,.06),(.145,.022,.043)]
    vs=[]
    for y,w,h in sections:
        vs.extend([(0,y,.026),(-w*.86,y,.028),(-w,y,.043),(-w*.72,y,h*.88),(-w*.35,y,h),(w*.35,y,h),(w*.72,y,h*.88),(w,y,.043),(w*.86,y,.028)])
    fs=[tuple(reversed(range(9)))]
    for j in range(len(sections)-1):
        fs.extend((j*9+i,j*9+(i+1)%9,(j+1)*9+(i+1)%9,(j+1)*9+i) for i in range(9))
    fs.append(tuple(range(54,63)));a.mesh(vs,fs,color)
    # Four-ring open collar provides real wall thickness, never a capped cylinder.
    n=10;vs=[];height=.197 if boot else .12
    for rx,ry,z in [(.047,.052,.08),(.043,.049,height),(.032,.037,height-.003),(.031,.035,.085)]:
        vs.extend((rx*math.cos(i*math.tau/n),-.083+ry*math.sin(i*math.tau/n),z) for i in range(n))
    fs=[];m=[]
    for j in range(3):
        for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i));m.append(color if j==0 else 'black')
    a.mesh(vs,fs,m)
    for y,z in [(-.048,.123),(-.024,.111),(.002,.10),(.027,.087)]:
        a.beam((-.023,y,z),(.023,y+.013,z-.006),.004,.003,'sand')
    if boot:
        a.beam((-.02,-.064,.18),(.02,-.055,.18),.004,.003,'sand')
        a.beam((-.02,-.048,.157),(.02,-.044,.155),.004,.003,'sand')
    a.box((0,-.132,.099),(.014,.007,.035),'wood_dark' if boot else 'teal')


@model('paneled_soccer_ball')
def soccer(a):
    p=(1+math.sqrt(5))/2
    vs=[(0,s,t*p) for s in [-1,1] for t in [-1,1]]+[(s,t*p,0) for s in [-1,1] for t in [-1,1]]+[(t*p,0,s) for s in [-1,1] for t in [-1,1]]
    sub=lambda u,v: tuple(x-y for x,y in zip(u,v))
    dot=lambda u,v: sum(x*y for x,y in zip(u,v))
    cross=lambda u,v:(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
    norm=lambda u: tuple(x/math.sqrt(dot(u,u)) for x in u)
    edges={(i,j) for i in range(12) for j in range(12) if i!=j and abs(dot(sub(vs[i],vs[j]),sub(vs[i],vs[j]))-4)<1e-5}
    out=[]; idx={}
    for i,j in sorted(edges):
        v=norm(tuple((2*x+y)/3 for x,y in zip(vs[i],vs[j])))
        idx[i,j]=len(out);out.append(tuple(.11*x for x in v))
    fs=[]; mats=[]
    for i in range(12):
        ids=[idx[i,j] for ii,j in edges if ii==i]
        n=norm(vs[i]);u=norm(sub(out[ids[0]],tuple(n[k]*dot(out[ids[0]],n) for k in range(3))));v=cross(n,u)
        ids.sort(key=lambda k:math.atan2(dot(out[k],v),dot(out[k],u)))
        fs.append(tuple(ids));mats.append('black')
    for i,j,k in combinations(range(12),3):
        if (i,j) in edges and (j,k) in edges and (k,i) in edges:
            if dot(cross(sub(vs[j],vs[i]),sub(vs[k],vs[i])),vs[i])<0:j,k=k,j
            fs.append((idx[i,j],idx[j,i],idx[j,k],idx[k,j],idx[k,i],idx[i,k]));mats.append('white')
    a.mesh(out,fs,mats)


@model('seamed_basketball')
def basketball(a):
    a.sphere((0,0,0),.12,'terracotta',12,6)
    for axis in ['x','y','z']:a.torus((0,0,0),.1205,.0017,'black',axis,12,4)


@model('laced_american_football')
def football(a):
    a.sphere((0,0,0),1,'brown',12,6,scale=(.15,.085,.085))
    for x in [-.091,.091]:
        a.torus((x,0,0),.067,.007,'cream','x',10,4)
    a.beam((-.052,0,.085),(.052,0,.085),.008,.008,'wood_dark')
    for x in [-.042,-.028,-.014,0,.014,.028,.042]:a.box((x,0,.09),(.006,.034,.005),'cream')


@model('tennis_ball')
def tennisball(a):
    a.sphere((0,0,0),.034,'foliage_light',12,5)
    pts=[]
    for i in range(19):
        t=2*math.pi*i/18; z=.015*math.cos(2*t);r=math.sqrt(.0345**2-z*z)
        pts.append((r*math.cos(t),r*math.sin(t),z))
    line(a,pts,.0008,'cream')


@model('stitched_baseball')
def baseball(a):
    a.sphere((0,0,0),.037,'cream',10,5)
    for s in [-1,1]:
        pts=[]
        for i in range(9):
            t=-1.35+2.7*i/8;x=.024*s;rr=math.sqrt(.0375**2-x*x)
            pts.append((x,rr*math.sin(t),rr*math.cos(t)))
        line(a,pts,.0005,'brown')
        for i in range(7):
            t=-1.2+2.4*i/6;rr=.029
            line(a,[(.021*s,rr*math.sin(t-.06),rr*math.cos(t-.06)),(.027*s,rr*math.sin(t+.06),rr*math.cos(t+.06))],.00065,'red')


@model('striped_volleyball')
def volleyball(a):
    a.sphere((0,0,0),.105,'cream',12,6)
    for i in range(len(a.face_materials)):
        a.face_materials[i]=['cream','cream','navy','navy','sand','sand'][(i+i//12)%6]
    a.cylinder((0,0,.103),(0,0,.1055),.004,'rubber',6)


@model('wooden_baseball_bat')
def bat(a):
    a.cylinder((0,0,.02),(0,0,.19),.017,'wood_dark',8)
    a.cylinder((0,0,.19),(0,0,.53),.017,'wood_light',10,.032)
    a.cylinder((0,0,.53),(0,0,.81),.032,'wood_light',10,.033)
    a.sphere((0,0,.81),1,'wood_light',10,4,scale=(.033,.033,.022))
    a.cylinder((0,0,0),(0,0,.017),.026,'wood_dark',10)
    for z in [.04,.072,.104,.136]:a.cylinder((0,0,z),(0,0,z+.008),.018,'black',8)
    a.box((0,-.032,.62),(.024,.002,.065),'brown')


@model('baseball_fielders_glove')
def glove(a):
    # Concave leather catching pocket, separate curved finger stalls and open web.
    rim=[(-.063,.022),(.043,.019),(.077,.06),(.075,.12),(.044,.153),(-.028,.157),(-.074,.121),(-.084,.058)]
    vs=[(0,.012,.085)]+[(x,-.025,z) for x,z in rim]+[(0,.036,.085)]+[(x,.005,z) for x,z in rim]
    fs=[];m=[]
    for i in range(8):
        q=(i+1)%8;fs.extend([(0,1+i,1+q),(9,10+q,10+i),(1+i,10+i,10+q,1+q)]);m.extend(['brown','wood','wood_dark'])
    a.mesh(vs,fs,m)
    for i,(x,h) in enumerate([(-.043,.206),(-.007,.226),(.029,.215),(.061,.19)]):
        line(a,[(x,.004,.11),(x*1.1,.008,h-.026),(x*1.06,-.011,h)],.018,'wood',6)
    line(a,[(-.072,.005,.048),(-.111,-.006,.102),(-.101,-.024,.154)],.024,'wood',6)
    for z in [.12,.14,.16]:
        a.beam((-.104,-.02,z-.015),(-.052,-.012,z+.015),.01,.006,'wood_dark')
    for x in [-.055,-.029]:a.beam((x,-.025,.03),(x,-.028,.145),.004,.003,'sand')
    a.beam((-.048,-.029,.029),(.035,-.029,.024),.012,.009,'wood_dark')


@model('tennis_racket')
def tennisracket(a):
    a.torus((0,0,.28),.142,.009,'navy','y',16,4)
    for x in [-.09,-.06,-.03,0,.03,.06,.09]:
        dz=math.sqrt(.13**2-x*x);a.beam((x,0,.28-dz),(x,0,.28+dz),.0015,.0015,'cream')
    for z in [.19,.22,.25,.28,.31,.34,.37]:
        dx=math.sqrt(.13**2-(z-.28)**2);a.beam((-dx,0,z),(dx,0,z),.0015,.0015,'cream')
    a.beam((-.078,0,.162),(0,0,.03),.013,.012,'navy');a.beam((.078,0,.162),(0,0,.03),.013,.012,'navy')
    a.cylinder((0,0,-.12),(0,0,.035),.018,'rubber',8)


@model('badminton_racket')
def badminton(a):
    a.torus((0,0,.4),.105,.005,'metal','y',14,4)
    for x in [-.07,-.035,0,.035,.07]:
        dz=math.sqrt(.1**2-x*x);a.beam((x,0,.4-dz),(x,0,.4+dz),.001,.001,'cream')
    for z in [.33,.365,.4,.435,.47]:
        dx=math.sqrt(.1**2-(z-.4)**2);a.beam((-dx,0,z),(dx,0,z),.001,.001,'cream')
    a.cylinder((0,0,.06),(0,0,.3),.0035,'steel',6)
    a.cylinder((0,0,-.08),(0,0,.06),.013,'wood_dark',8,.009)
    a.cylinder((0,0,-.088),(0,0,-.076),.015,'black',8)


@model('feather_shuttlecock')
def shuttle(a):
    a.sphere((0,0,.012),1,'cream',8,4,scale=(.012,.012,.012))
    a.cylinder((0,0,.012),(0,0,.026),.012,'cream',8)
    for i in range(8):
        t=2*math.pi*i/8;x,y=math.cos(t),math.sin(t)
        a.beam((.009*x,.009*y,.023),(.031*x,.031*y,.071),.003,.002,'sand')
        a.beam((.021*x,.021*y,.047),(.032*x,.032*y,.073),.019,.0015,'white')
    a.torus((0,0,.039),.02,.001,'sand','z',8,4)


@model('table_tennis_paddle')
def pingpong(a):
    a.cylinder((0,-.004,.17),(0,.004,.17),.083,'wood_light',12)
    a.cylinder((0,-.006,.17),(0,-.004,.17),.079,'red',12)
    a.cylinder((0,.004,.17),(0,.006,.17),.079,'rubber',12)
    bevel(a,(0,0,.052),(.03,.024,.13),'wood_dark')
    a.box((0,-.0125,.042),(.009,.001,.092),'wood_light')


@model('flying_disc')
def frisbee(a):
    a.cylinder((0,0,.015),(0,0,.022),.125,'teal',16,.111)
    a.torus((0,0,.014),.12,.006,'teal','z',16,4)
    a.cylinder((0,0,.022),(0,0,.023),.063,'cream',16)
    a.cylinder((0,0,.023),(0,0,.024),.036,'teal',12)


@model('wooden_boomerang')
def boomerang(a):
    a.prism([(-.19,-.03),(-.18,-.065),(.012,.053),(.025,.105),(-.019,.107)],0,.009,'wood_light')
    a.prism([(.012,.053),(.18,-.065),(.195,-.031),(.054,.105),(.025,.105)],0,.009,'wood')
    a.beam((-.16,-.015,.0095),(-.11,.015,.0095),.016,.001,'brown')
    a.beam((.115,.012,.0095),(.159,-.022,.0095),.016,.001,'brown')


@model('coiled_jump_rope')
def jumprope(a):
    a.torus((0,0,.008),.19,.004,'teal','z',16,4,math.pi*1.85)
    a.torus((.009,0,.016),.175,.004,'teal','z',16,4,math.pi*1.65)
    for x in [-.08,.075]:
        a.cylinder((x,-.185,.015),(x,-.3,.015),.012,'rubber',8)
        a.cylinder((x,-.188,.015),(x,-.202,.015),.013,'metal',8)


@model('quad_roller_skate')
def rollerskate(a):
    shoe(a)
    a.box((0,0,-.012),(.085,.21,.025),'metal')
    for x in [-.085,.085]:
        for y in [-.075,.076]:
            a.cylinder((x-.019,y,-.043),(x+.019,y,-.043),.031,'wood',8)
    a.cylinder((0,.12,-.03),(0,.15,-.05),.021,'rubber',6)


@model('inline_skate')
def inlineskate(a):
    shoe(a,True)
    for x in [-.018,.018]:a.box((x,0,-.04),(.009,.25,.052),'dark_metal')
    for y in [-.095,-.032,.032,.095]:a.cylinder((-.027,y,-.06),(.027,y,-.06),.035,'rubber',8)
    a.box((0,-.093,.196),(.114,.027,.022),'black')


@model('street_skateboard')
def skateboard(a):
    pts=[(-.07,-.4),(.07,-.4),(.105,-.34),(.1,.31),(.07,.4),(-.07,.4),(-.1,.31),(-.105,-.34)]
    a.prism(pts,.086,.1,'wood_light')
    a.prism([(x*.94,y*.94) for x,y in pts],.1,.103,'rubber')
    for y in [-.25,.25]:
        a.box((0,y,.071),(.057,.06,.03),'metal')
        a.cylinder((-.12,y,.044),(.12,y,.044),.009,'steel',6)
        for x in [-.106,.106]:a.cylinder((x-.02,y,.043),(x+.02,y,.043),.03,'cream',10)
    for x in [-.023,.023]:
        for y in [-.275,-.225,.225,.275]:a.cylinder((x,y,.103),(x,y,.105),.003,'steel',6)


@model('vented_bicycle_helmet')
def helmet(a):
    dome(a,.115,.15,.025,.177,'navy')
    for x in [-.049,0,.049]:
        a.box((x,-.03,.195),(.015,.086,.004),'black',rot=(0,.22 if x<0 else -.22 if x>0 else 0,0))
    for x in [-.09,.09]:line(a,[(x,0,.048),(x*.5,-.025,-.065),(0,.028,-.085)],.004,'black')
    a.box((0,.028,-.085),(.026,.013,.011),'metal')


@model('skate_elbow_guard')
def elbow(a):
    a.sphere((0,0,.018),1,'black',10,4,scale=(.064,.095,.026))
    a.sphere((0,0,.041),1,'metal',8,4,scale=(.046,.061,.026))
    for y in [-.063,.063]:a.box((0,y,.01),(.155,.024,.007),'navy')
    for x in [-.023,.023]:a.cylinder((x,0,.064),(x,0,.068),.003,'steel',6)


@model('zippered_day_backpack')
def backpack(a):
    soft_shell(a,(0,0,.23),(.3,.17,.43),'navy')
    soft_shell(a,(0,-.105,.14),(.24,.058,.18),'teal')
    a.box((0,-.137,.21),(.208,.005,.009),'black')
    a.box((.085,-.143,.202),(.013,.006,.029),'steel')
    for x in [-.095,.095]:
        a.beam((x,.09,.4),(x,.145,.27),.032,.012,'black')
        a.beam((x,.145,.27),(x,.09,.07),.032,.012,'black')
    handle(a,0,0,.445,.105,.053)
    a.box((0,-.135,.116),(.046,.003,.028),'cream')


@model('external_frame_hiking_pack','person')
def hikingpack(a):
    soft_shell(a,(0,0,.32),(.35,.23,.59),'green')
    soft_shell(a,(0,-.015,.63),(.39,.25,.09),'foliage_dark')
    for x in [-.22,.22]:soft_shell(a,(x,0,.25),(.115,.19,.28),'foliage_dark')
    for x in [-.14,.14]:
        a.cylinder((x,.15,.04),(x,.15,.66),.012,'metal',6)
        a.beam((x,-.127,.55),(x,-.127,.16),.024,.01,'sand')
        a.box((x,-.139,.22),(.036,.015,.031),'black')
        line(a,[(x,.15,.57),(x*.64,.23,.4),(x,.15,.1)],.018,'black')
    a.cylinder((-.19,0,.72),(.19,0,.72),.078,'sand',10)
    for x in [-.1,.1]:a.torus((x,0,.72),.08,.009,'black','x',10,4)


@model('sports_duffel_bag')
def duffel(a):
    a.cylinder((-.26,0,.13),(.26,0,.13),.14,'teal',8)
    for x in [-.263,.263]:a.cylinder((x-.004,0,.13),(x+.004,0,.13),.139,'navy',8)
    for x in [-.14,.14]:
        a.box((x,0,.269),(.034,.21,.006),'black')
        handle(a,x,0,.272,.035,.125,'black',.014)
    a.box((0,-.1,.235),(.42,.012,.012),'black')
    a.box((.15,-.11,.23),(.017,.012,.035),'silver')


@model('messenger_satchel')
def satchel(a):
    soft_shell(a,(0,0,.17),(.39,.12,.3),'brown')
    soft_shell(a,(0,-.075,.245),(.41,.036,.17),'wood_dark')
    for x in [-.12,.12]:
        a.box((x,-.098,.14),(.028,.012,.096),'sand')
        a.box((x,-.11,.134),(.041,.01,.033),'metal')
    line(a,[(-.19,0,.27),(-.16,0,.54),(.16,0,.54),(.19,0,.27)],.013,'wood_dark')


@model('canvas_shopping_tote')
def tote(a):
    soft_shell(a,(0,0,.19),(.34,.12,.35),'cream')
    a.box((0,0,.369),(.31,.1,.012),'brown')
    for y in [-.043,.043]:handle(a,0,y,.36,.17,.2,'sand',.018)
    a.box((0,-.061,.17),(.12,.003,.105),'teal')
    a.box((0,-.064,.17),(.088,.003,.073),'cream')


@model('ribbed_rolling_suitcase')
def suitcase(a):
    bevel(a,(0,0,.35),(.37,.24,.54),'navy',.13)
    for x in [-.13,-.065,0,.065,.13]:bevel(a,(x,-.123,.35),(.018,.012,.39),'teal')
    for x in [-.135,.135]:
        a.cylinder((x,-.035,.62),(x,-.035,.99),.011,'steel',6)
        wheel(a,x,0,.05,.045,.04)
    a.beam((-.135,-.035,.99),(.135,-.035,.99),.029,.024,'rubber')
    handle(a,0,0,.621,.1,.036)
    a.box((.19,0,.36),(.015,.06,.11),'black')


@model('folding_shopping_trolley')
def trolley(a):
    for x in [-.15,.15]:
        a.cylinder((x,.04,.1),(x,.04,.93),.012,'metal',6)
        wheel(a,x,0,.087,.087,.04)
    a.beam((-.15,.04,.93),(.15,.04,.93),.032,.025,'rubber')
    a.box((0,-.095,.14),(.32,.27,.022),'metal')
    soft_shell(a,(0,-.09,.39),(.28,.23,.47),'brown')
    soft_shell(a,(0,-.11,.64),(.29,.25,.06),'sand')
    a.box((0,-.212,.43),(.16,.012,.14),'wood_dark')


@model('open_rain_umbrella','person')
def umbrella(a):
    n=10;vs=[(0,0,1.02)]+[(.29*math.cos(2*math.pi*i/n),.29*math.sin(2*math.pi*i/n),.96) for i in range(n)]+[(.53*math.cos(2*math.pi*i/n),.53*math.sin(2*math.pi*i/n),.78) for i in range(n)]
    fs=[];m=[]
    for i in range(n):
        j=(i+1)%n;fs.extend([(0,1+i,1+j),(1+i,11+i,11+j,1+j)]);m.extend(['navy' if i%2 else 'teal']*2)
    # A thin second canopy surface gives the visible underside its own outward normal.
    vs2=[(x,y,z-.006) for x,y,z in vs]
    rim=[(11+i,11+i+len(vs),11+(i+1)%n+len(vs),11+(i+1)%n) for i in range(n)]
    a.mesh(vs+vs2,fs+[tuple(k+len(vs) for k in reversed(f)) for f in fs]+rim,m+m+['navy']*n)
    for i in range(n):
        t=2*math.pi*i/n
        line(a,[(0,0,.9),(.29*math.cos(t),.29*math.sin(t),.95),(.53*math.cos(t),.53*math.sin(t),.775)],.004,'metal')
    a.cylinder((0,0,.13),(0,0,1.055),.008,'metal',8)
    line(a,[(0,0,.16),(0,0,.055),(.022,0,.022),(.054,0,.028),(.066,0,.06)],.012,'wood_dark',6)


@model('furled_walking_umbrella')
def closedumbrella(a):
    a.cylinder((0,0,.02),(0,0,.11),.007,'steel',6)
    a.cylinder((0,0,.1),(0,0,.61),.016,'navy',10,.043)
    a.cone((0,0,.61),(0,0,.69),.043,'navy',10)
    a.cylinder((0,0,.48),(0,0,.5),.038,'black',10)
    a.cylinder((0,0,.65),(0,0,.77),.009,'metal',6)
    line(a,[(0,0,.77),(0,0,.83),(.035,0,.86),(.07,0,.83),(.07,0,.795)],.013,'wood_dark',6)


@model('folding_baby_stroller','person')
def stroller(a):
    for x in [-.24,.24]:
        for y in [-.31,.31]:wheel(a,x,y,.095,.095,.048)
        a.beam((x,-.31,.11),(x,.24,.84),.028,.028,'metal')
        a.beam((x,.31,.11),(x,-.22,.61),.028,.028,'metal')
        a.beam((x,.12,.64),(x,.32,1.02),.024,.024,'metal')
    a.beam((-.24,.32,1.02),(.24,.32,1.02),.04,.035,'rubber')
    a.box((0,0,.46),(.44,.39,.07),'navy')
    a.box((0,.15,.65),(.44,.055,.38),'teal',rot=(-.2,0,0))
    a.box((0,-.28,.3),(.34,.14,.035),'rubber')
    a.box((0,0,.24),(.37,.41,.075),'black')
    a.beam((-.23,-.21,.66),(.23,-.21,.66),.038,.035,'rubber')
    vs=[(-.25,-.15,.85),(.25,-.15,.85),(-.25,0,1.02),(.25,0,1.02),(-.25,.26,.95),(.25,.26,.95),(-.25,.26,.76),(.25,.26,.76)]
    a.mesh(vs,[(0,1,3,2),(2,3,5,4),(4,5,7,6),(0,2,4,6),(1,7,5,3)],'navy')
    for x in [-.11,.11]:a.beam((x,.115,.8),(0,-.04,.48),.025,.008,'black')


@model('soft_structured_baby_carrier')
def babycarrier(a):
    soft_shell(a,(0,0,.22),(.27,.07,.38),'teal')
    soft_shell(a,(0,-.02,.435),(.24,.08,.075),'navy')
    a.box((0,0,.048),(.47,.042,.09),'navy')
    for x in [-.105,.105]:
        line(a,[(x,.04,.39),(x,.17,.48),(x,.22,.19),(x,.04,.12)],.025,'navy')
    a.box((.19,-.03,.048),(.05,.02,.056),'black')
    a.box((0,-.042,.22),(.13,.012,.12),'navy')


@model('running_shoe')
def runningshoe(a):shoe(a)


@model('lace_up_hiking_boot')
def hikingboot(a):
    shoe(a,True)
    for y in [-.11,-.055,0,.055,.11]:a.box((0,y,.001),(.13,.025,.012),'rubber')


@model('trail_sandal')
def sandal(a):
    pts=[(-.04,-.135),(.04,-.135),(.068,-.05),(.065,.105),(.038,.138),(-.04,.138),(-.068,.1),(-.065,-.06)]
    a.prism(pts,0,.022,'rubber');a.prism([(x*.92,y*.97) for x,y in pts],.022,.032,'sand')
    for y in [.045,-.071]:
        line(a,[(-.057,y,.029),(-.035,y,.075),(.035,y,.075),(.057,y,.029)],.013,'brown')
    line(a,[(-.052,-.05,.05),(-.048,-.124,.075),(.048,-.124,.075),(.052,-.05,.05)],.009,'brown')
    a.box((.044,.045,.061),(.023,.034,.009),'metal')


@model('wide_brim_sun_hat')
def sunhat(a):
    a.cylinder((0,0,.008),(0,0,.016),.2,'sand',16,.19)
    a.cylinder((0,0,.016),(0,0,.12),.105,'sand',12,.087)
    a.cylinder((0,0,.024),(0,0,.048),.106,'brown',12,.101)
    a.sphere((0,0,.119),1,'sand',12,4,scale=(.087,.087,.016))
    line(a,[(-.095,0,.016),(-.038,-.045,-.17),(.038,-.045,-.17),(.095,0,.016)],.002,'wood_dark')


@model('baseball_cap')
def cap(a):
    dome(a,.092,.099,.03,.103,'green')
    a.prism([(-.08,-.038),(.08,-.038),(.088,-.11),(.052,-.172),(-.052,-.172),(-.088,-.11)],.025,.031,'foliage_dark')
    a.cylinder((0,0,.132),(0,0,.142),.009,'foliage_dark',6)
    a.box((0,-.09,.074),(.033,.007,.024),'cream')
    a.box((0,.096,.042),(.041,.007,.02),'black')


@model('folded_sunglasses')
def glasses(a):
    for x in [-.034,.034]:
        bevel(a,(x,0,.018),(.057,.013,.043),'wood_dark',.2)
        bevel(a,(x,-.0075,.019),(.046,.003,.032),'black',.2)
    a.beam((-.009,0,.026),(.009,0,.026),.006,.006,'wood_dark')
    for x in [-.063,.063]:line(a,[(x,0,.03),(x,.03,.031),(-x*.65,.055,.032)],.004,'wood_dark')


@model('compact_binoculars')
def binoculars(a):
    for x in [-.038,.038]:
        a.cylinder((x,-.075,.033),(x,.045,.033),.03,'navy',10,.022)
        a.cylinder((x,-.08,.033),(x,-.075,.033),.031,'rubber',10)
        a.cylinder((x,-.081,.033),(x,-.079,.033),.025,'glass',10)
        a.cylinder((x,.045,.033),(x,.065,.033),.018,'rubber',8)
    a.box((0,0,.033),(.081,.041,.025),'dark_metal')
    a.cylinder((0,-.007,.035),(0,-.007,.063),.014,'rubber',8)


@model('compact_digital_camera')
def camera(a):
    bevel(a,(0,0,.037),(.116,.036,.075),'dark_metal')
    a.cylinder((.012,-.018,.036),(.012,-.049,.036),.031,'black',12)
    a.cylinder((.012,-.05,.036),(.012,-.053,.036),.023,'metal',12)
    a.cylinder((.012,-.054,.036),(.012,-.055,.036),.019,'glass',12)
    a.box((-.037,-.02,.061),(.025,.004,.011),'cream')
    a.box((.012,.019,.037),(.068,.003,.043),'glass')
    a.cylinder((-.035,0,.074),(-.035,0,.08),.009,'silver',8)
    a.box((.05,0,.038),(.013,.045,.063),'rubber')


@model('outdoor_two_way_radio')
def radio(a):
    bevel(a,(0,0,.067),(.061,.034,.128),'navy')
    a.cylinder((-.02,0,.128),(-.02,0,.241),.005,'rubber',6,.003)
    a.cylinder((.018,0,.129),(.018,0,.146),.008,'black',8)
    a.box((0,-.018,.093),(.04,.003,.025),'glass')
    for z in [.04,.05,.06,.07]:a.box((0,-.019,z),(.036,.003,.003),'black')
    for x in [-.014,0,.014]:a.box((x,-.019,.019),(.007,.004,.008),'rubber')
    a.box((0,.024,.07),(.024,.013,.075),'black')


@model('handheld_torch_flashlight')
def torch(a):
    a.cylinder((0,0,.015),(0,0,.15),.019,'dark_metal',10)
    a.cylinder((0,0,.15),(0,0,.186),.019,'dark_metal',10,.035)
    a.cylinder((0,0,.186),(0,0,.207),.035,'rubber',10)
    a.cylinder((0,0,.207),(0,0,.209),.03,'silver',10)
    a.cylinder((0,0,.209),(0,0,.211),.024,'glass',10)
    a.cylinder((0,0,.001),(0,0,.018),.021,'rubber',10)
    for z in [.045,.065,.085,.105]:a.cylinder((0,0,z),(0,0,z+.005),.0205,'rubber',10)
    a.box((0,-.02,.133),(.017,.007,.014),'rubber')


@model('portable_folding_camp_chair','person')
def campchair(a):
    for x in [-.25,.25]:
        a.beam((x,-.24,.035),(x,.21,.64),.024,.024,'metal')
        a.beam((x,.24,.035),(x,-.22,.61),.024,.024,'metal')
        a.beam((x,.15,.39),(x,.24,.9),.024,.024,'metal')
        a.box((x,-.04,.64),(.075,.5,.034),'black')
        a.cylinder((x-.018,0,.33),(x+.018,0,.33),.025,'black',8)
        for y in [-.24,.24]:a.box((x,y,.017),(.056,.056,.03),'rubber')
    a.box((0,0,.43),(.46,.42,.024),'green')
    a.box((0,.215,.712),(.46,.025,.34),'green',rot=(-.13,0,0))
    a.beam((-.25,.15,.4),(.25,.15,.4),.02,.02,'metal')
    a.box((.25,-.11,.658),(.06,.12,.006),'black')


@model('tripod_folding_camp_stool')
def campstool(a):
    pts=[(-.19,-.12),(.19,-.12),(0,.2)]
    a.prism(pts,.43,.448,'sand')
    for x,y in pts:
        a.cylinder((x*.8,y*.8,.018),(-x,-y,.43),.013,'wood_dark',8)
        a.cylinder((x*.8,y*.8,0),(x*.8,y*.8,.033),.018,'rubber',8)
    a.cylinder((-.04,0,.22),(.04,0,.22),.021,'metal',8)


@model('strapped_sleeping_bag_roll')
def sleepingbag(a):
    a.cylinder((-.22,0,.135),(.22,0,.135),.135,'green',12)
    for x in [-.222,.222]:a.cylinder((x-.002,0,.135),(x+.002,0,.135),.095,'foliage_dark',10)
    for x in [-.12,.12]:a.torus((x,0,.135),.139,.01,'black','x',12,4)
    a.beam((-.12,0,.278),(.12,0,.278),.021,.012,'black')
    for x in [-.12,.12]:a.box((x,-.06,.263),(.026,.04,.015),'metal')


@model('ribbed_foam_sleeping_mat','person')
def sleepingmat(a):
    a.box((0,0,.009),(.55,1.65,.018),'teal')
    for y in [-.75,-.6,-.45,-.3,-.15,0,.15,.3,.45,.6,.75]:
        a.box((0,y,.019),(.53,.045,.012),'navy')
    a.cylinder((-.275,.83,.057),(.275,.83,.057),.055,'teal',12)
    a.cylinder((-.277,.83,.057),(-.276,.83,.057),.034,'navy',10)


@model('folded_picnic_blanket')
def blanket(a):
    for z in [.018,.05,.08]:a.box((0,0,z),(.43,.31,.028),'sand')
    for x in [-.16,-.07,.02,.11]:a.box((x,0,.095),(.022,.31,.003),'brown')
    for y in [-.11,-.02,.07]:a.box((0,y,.098),(.43,.022,.003),'cream')
    for x in [-.17,-.12,-.07,-.02,.03,.08,.13,.18]:a.box((x,-.17,.079),(.022,.04,.009),'sand')
    a.box((0,0,.103),(.035,.33,.014),'wood_dark')


@model('ventilated_pet_carrier','person')
def petcarrier(a):
    bevel(a,(0,0,.13),(.34,.55,.23),'navy')
    bevel(a,(0,0,.33),(.32,.53,.21),'cream')
    a.box((0,-.28,.255),(.282,.018,.302),'black')
    for x in [-.115,-.077,-.039,0,.039,.077,.115]:a.beam((x,-.291,.12),(x,-.291,.39),.006,.006,'metal')
    for z in [.13,.25,.38]:a.beam((-.13,-.293,z),(.13,-.293,z),.008,.008,'metal')
    for s in [-1,1]:
        for y in [-.17,-.09,-.01,.07,.15]:a.box((s*.161,y,.32),(.006,.033,.078),'black')
    handle(a,0,0,.44,.13,.056,'black',.019)
    a.box((.135,-.299,.25),(.018,.014,.04),'metal')


@model('retractable_dog_leash')
def leash(a):
    a.cylinder((0,-.018,.06),(0,.018,.06),.059,'navy',12)
    handle(a,.078,0,.025,.044,.085,'navy',.017)
    a.box((0,0,.121),(.025,.03,.012),'black')
    line(a,[(-.055,0,.06),(-.15,-.01,.045),(-.24,.02,.018)],.002,'black')
    a.torus((-.259,.02,.018),.015,.003,'metal','z',8,4,math.pi*1.7)
    a.box((-.237,.02,.018),(.02,.009,.007),'metal')


@model('padded_dog_walking_harness')
def harness(a):
    a.torus((0,0,.065),.078,.011,'brown','y',10,4)
    a.torus((0,.14,.065),.055,.012,'brown','y',10,4)
    for x in [-.052,.052]:a.beam((x,0,.108),(x*.72,.14,.101),.034,.01,'navy')
    a.beam((0,0,-.005),(0,.14,.015),.042,.012,'navy')
    a.box((.072,0,.058),(.022,.027,.024),'black')
    a.torus((0,.04,.15),.018,.003,'metal','y',8,4)
    a.box((0,.04,.13),(.05,.035,.018),'navy')


@model('diamond_flying_kite','person')
def kite(a):
    vs=[(0,0,.9),(-.32,0,.55),(0,0,0),(.32,0,.55),(0,-.025,.55)]
    fs=[(0,1,4),(1,2,4),(2,3,4),(3,0,4)]
    vs+= [(x,y+.0015,z) for x,y,z in vs]
    fs+= [tuple(i+5 for i in reversed(f)) for f in fs]
    fs+= [(i,i+5,(i+1)%4+5,(i+1)%4) for i in range(4)]
    a.mesh(vs,fs,['cream','teal','navy','sand']*2+['sand']*4)
    a.beam((0,.006,0),(0,.006,.9),.006,.006,'wood_light')
    a.beam((-.32,.006,.55),(.32,.006,.55),.006,.006,'wood_light')
    line(a,[(0,0,0),(.045,0,-.19),(-.045,0,-.38),(.01,0,-.57)],.002,'sand')
    for x,z in [(.045,-.19),(-.045,-.38),(.01,-.57)]:
        a.mesh([(x,0,z),(x-.052,0,z-.025),(x-.052,0,z+.025),(x+.052,0,z-.025),(x+.052,0,z+.025)],[(0,2,1),(0,3,4)],'teal')
    line(a,[(0,-.03,.55),(0,-.27,.38),(.06,-.4,.04)],.001,'cream')
