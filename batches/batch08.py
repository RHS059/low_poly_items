"""Fifty planted landscape assets; species silhouettes and restrained city greenery.
Branches, leaves, florets and container joinery are geometric; all units metres.
"""
import math
from assetlib import Asset, register, add, sub, mul, cross, unit

TAU=math.tau
F='foliage'; D='foliage_dark'; L='foliage_light'; B='wood_dark'

def branch(a,p,q,r=.04,r2=None,m=B,n=7):
    a.cylinder(p,q,r,mat=m,sides=n,radius2=r*.48 if r2 is None else r2)

def crown(a,p,s,m=F,n=9,split=True):
    """Irregular tapered foliage masses, with staggered lobes and broken lower edges.
    Flower centres and seed heads retain their small botanical solid forms.
    """
    if m not in (F,D,L) and not (a.category=='tree' and max(s)>.45):
        a.sphere(p,1,mat=m,segments=n,rings=4,scale=s)
        return
    # Broad spreading species need multiple terminal leaf groups per scaffold bough.
    if split and a.name in {'b08_mature_white_oak','b08_sycamore','b08_american_elm','b08_flowering_cherry'} and max(s)>.7:
        phase=p[0]*1.7+p[1]*2.3+p[2]
        for j in range(3):
            t=phase+j*TAU/3
            q=add(p,(s[0]*.40*math.cos(t),s[1]*.38*math.sin(t),s[2]*(.12 if j==1 else -.04)))
            crown(a,q,(s[0]*.66,s[1]*.66,s[2]*(.78 if j==1 else .70)),m,max(8,n-1),False)
        return
    # Phase is deterministic but differs for every branch; never repeat a sphere.
    phase=p[0]*1.71+p[1]*2.31+p[2]*.79
    if a.size_class=='large': n=max(n,10)
    vs=[add(p,(s[0]*.08*math.sin(phase),s[1]*.09*math.cos(phase),-s[2]*.88))]
    for j,(h,r) in enumerate(((-.59,.52),(-.13,.97),(.38,.83),(.78,.43))):
        for i in range(n):
            t=TAU*i/n+phase+(j%2)*.12
            scallop=1+.12*math.sin(i*2.19+phase)+.055*math.cos(i*3.1+j*.7)
            rr=r*scallop
            zz=h+.075*math.sin(i*2.47+phase+j*.8)
            vs.append(add(p,(s[0]*(rr*math.cos(t)+.07*h),s[1]*rr*math.sin(t),s[2]*zz)))
    vs.append(add(p,(s[0]*.11*math.sin(phase+.8),s[1]*.10*math.cos(phase),s[2]*1.02)))
    top=len(vs)-1; fs=[]; mats=[]
    for i in range(n):
        fs.append((0,1+(i+1)%n,1+i));mats.append(D if m==F else m)
    for j in range(3):
        for i in range(n):
            k=1+j*n+i; nx=1+j*n+(i+1)%n
            fs.append((k,nx,nx+n,k+n));mats.append(m)
    for i in range(n):
        fs.append((1+3*n+i,1+3*n+(i+1)%n,top));mats.append(m)
    a.mesh(vs,fs,mats)

def disk(a,p,r,h,m='soil',n=12):
    a.cylinder(p,add(p,(0,0,h)),r,mat=m,sides=n)

def leaf(a,p,q,w=.10,m=F,bend=.06):
    """Closed, keeled lanceolate leaf with an elevated midrib."""
    v=sub(q,p); side=unit(cross(v,(0,0,1)))
    if abs(v[0])+abs(v[1])<1e-8: side=(1,0,0)
    mid=add(add(p,mul(v,.53)),(0,0,bend))
    vs=[p,add(mid,mul(side,w)),q,add(mid,mul(side,-w)),add(mid,(0,0,w*.27)),add(mid,(0,0,-w*.13))]
    # Ordering is checked below by orienting each closed convex face outward.
    fs=[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(1,0,5),(2,1,5),(3,2,5),(0,3,5)]
    center=tuple(sum(v[i] for v in vs)/6 for i in range(3))
    out=[]
    for f in fs:
        n=cross(sub(vs[f[1]],vs[f[0]]),sub(vs[f[2]],vs[f[0]]))
        delta=sub(tuple(sum(vs[j][i] for j in f)/3 for i in range(3)),center)
        out.append(f if sum(n[i]*delta[i] for i in range(3))>0 else tuple(reversed(f)))
    a.mesh(vs,out,m)

def blade_clump(a,x,y,z,height=.7,spread=.45,count=15,m=F,phase=0):
    for i in range(count):
        th=phase+i*2.39996; rr=spread*(.54+.46*(i%4)/3)
        q=(x+rr*math.cos(th),y+rr*math.sin(th),z+height*(.64+.36*(i%5)/4))
        leaf(a,(x+.025*math.cos(th),y+.025*math.sin(th),z),q,.035 if height<1 else .044,m,height*.20)

def flower(a,p,r=.07,m='pink',petals=5,core='yellow',stem=None):
    if stem is not None:
        branch(a,stem,p,.008,.005,F,5)
        for t,sgn in ((.34,1),(.63,-1)):
            base=add(stem,mul(sub(p,stem),t)); leaf(a,base,add(base,(sgn*r*1.7,r*.45,r*.40)),r*.40,F)
    for j in range(petals):
        th=j*TAU/petals
        leaf(a,p,add(p,(r*math.cos(th),r*math.sin(th),r*.14)),r*.34,m,r*.20)
    crown(a,add(p,(0,0,r*.15)),(r*.28,r*.28,r*.20),core,7)

def root_flare(a,r=.22,h=.42):
    for th in (.2,1.5,2.65,3.9,5.25):
        branch(a,(0,0,h),(r*2*math.cos(th),r*2*math.sin(th),.035),r*.48,.055)

def broad_branch(a,p,q,r,scale,m=F):
    elbow=add(add(p,mul(sub(q,p),.56)),(0,0,-scale[2]*.10))
    branch(a,p,elbow,r,r*.65)
    branch(a,elbow,q,r*.65,r*.23)
    for sign in (-1,1):
        end=add(q,(sign*scale[0]*.52,scale[1]*.23,-scale[2]*.27))
        branch(a,elbow,end,r*.34,r*.095,n=5)
    crown(a,q,scale,m)

def rim_pot(a,r=.35,h=.52,m='terracotta',p=(0,0,0)):
    x,y,z=p
    a.cylinder((x,y,z+.025),(x,y,z+h-.035),r*.72,m,12,radius2=r)
    a.torus((x,y,z+h-.015),r*.97,.035,m,segments=12,sides=4)
    disk(a,(x,y,z+h),r*.88,.008)

def rect_bed(a,w,d,h=.13):
    a.box((0,0,h*.50),(w,d,h),'soil')
    for x in (-w/2,w/2): a.box((x,0,h*.61),(.09,d+.09,h*1.22),'wood_dark')
    for y in (-d/2,d/2): a.box((0,y,h*.61),(w,.09,h*1.22),'wood_dark')

def asset(name,size='person',category='planted_landscaping'):
    return Asset('b08_'+name,category,size)

# Broadleaf trees have independently arranged scaffold branches and crown lobes.
def b08_mature_white_oak():
    a=asset('mature_white_oak','large','tree');root_flare(a,.32,.65)
    branch(a,(0,0,.12),(.12,.04,2.7),.31,.22)
    for p,q,r,s in [((.08,0,1.9),(-2.1,.45,3.7),.18,(1.65,1.4,1.08)),((.1,0,2.1),(1.9,.8,4),.16,(1.5,1.5,1.3)),((.1,0,2.5),(.3,-1.6,4.25),.15,(1.65,1.35,1.32)),((.1,0,2.6),(-.1,.4,5.15),.16,(1.6,1.5,1.3)),((-.8,.1,2.8),(-2.4,-.65,3.2),.11,(1.1,1.1,.85))]:
        broad_branch(a,p,q,r,s)
    return a

def b08_sugar_maple():
    a=asset('sugar_maple','large','tree');root_flare(a,.24,.4)
    branch(a,(0,0,.08),(-.10,.02,4.0),.23,.075)
    for i,(z,r) in enumerate(((2.25,1.0),(2.7,1.6),(3.2,1.8),(3.85,1.3),(4.45,.72))):
        for j in range(3):
            t=j*TAU/3+i*.65; q=(r*.66*math.cos(t),r*.66*math.sin(t),z+.65)
            broad_branch(a,(0,0,z-.3),q,.065,(r*.69,r*.65,.80),F if j!=1 else D)
    return a

def b08_american_elm():
    a=asset('american_elm','large','tree'); root_flare(a,.3,.55)
    branch(a,(0,0,.06),(0,.06,2.65),.29,.19)
    for i in range(6):
        t=i*TAU/6+.25;p=(.65*math.cos(t),.65*math.sin(t),3.85);q=(2.1*math.cos(t),2.1*math.sin(t),5.0+.18*(i%2))
        branch(a,(0,.04,2.2),p,.155,.09);branch(a,p,q,.09,.025)
        crown(a,q,(1.30,1.20,.73),F)
        crown(a,add(p,(.1,.1,.8)),(.90,.85,.9),D if i%3==0 else F)
    crown(a,(0,0,5.4),(1.4,1.3,.9),F)
    return a

def b08_sycamore():
    a=asset('sycamore','large','tree');root_flare(a,.31,.5)
    branch(a,(0,0,.06),(.2,0,3.1),.3,.19,m='wood_light')
    for p,q,r in [((.13,0,2.4),(-1.3,-.6,4.3),.17),((.15,0,2.7),(1.6,.35,4.7),.15),((.16,0,2.9),(.2,1.2,5.3),.14)]:
        branch(a,p,q,r,.05,m='concrete_light')
        crown(a,q,(1.6,1.45,1.1),F)
        crown(a,add(q,(.4,-.5,.75)),(1.3,1.05,.95),L)
    for z,th in ((.5,.2),(1.2,2.9),(1.8,4.6),(2.25,1.3)):
        crown(a,(.22*math.cos(th)+.06,.22*math.sin(th),z),(.09,.07,.22),'brown',6)
    return a

def b08_river_birch_clump():
    a=asset('river_birch_clump','large','tree')
    for i,(x,y,h) in enumerate(((-.24,-.1,4.8),(.25,.08,5.3),(-.03,.28,4.25))):
        q=(x*3,y*3,h*.76);branch(a,(x*.5,y*.5,.02),q,.115,.047,m='concrete_light')
        for j in range(4):
            z=h*(.42+j*.12);t=i*1.8+j*2.4;end=(x*2+.85*math.cos(t),y*2+.85*math.sin(t),z+.65)
            branch(a,(x*2,y*2,z),end,.042,.016,m='brown');crown(a,end,(.8,.72,.78),L if j%2 else F)
        crown(a,(q[0],q[1],h),(.72,.7,.92),F)
        for j in range(5):
            z=.45+j*.36; a.cylinder((x*.5+q[0]*z/h,y*.5+q[1]*z/h,z),(x*.5+q[0]*z/h,y*.5+q[1]*z/h,z+.045),.105,'brown',7)
    return a

def b08_tulip_poplar():
    a=asset('tulip_poplar','large','tree');branch(a,(0,0,0),(0,0,6.8),.25,.045)
    for j in range(5):
        z=2.75+j*.78;rad=(1.3,1.55,1.30,1.02,.68)[j]
        for i in range(3):
            th=i*TAU/3+j*.83;q=(rad*.66*math.cos(th),rad*.66*math.sin(th),z+.28)
            broad_branch(a,(0,0,z-.45),q,.065,(rad*.65,rad*.59,.91),F)
    crown(a,(0,0,6.55),(.7,.7,.88),L)
    return a

def b08_ginkgo():
    a=asset('ginkgo','large','tree');branch(a,(0,0,.02),(0,0,4.7),.17,.045)
    for i in range(7):
        th=i*2.4;z=1.9+i*.36;r=1.35-i*.085
        q=(r*math.cos(th),r*math.sin(th),z+.52);branch(a,(0,0,z-.2),q,.065,.018)
        crown(a,q,(.79,.69,.64),L)
        for j in range(3):
            t=th+j*.75; tip=add(q,(.45*math.cos(t),.45*math.sin(t),.16*j))
            leaf(a,q,tip,.28,L,.15)
    crown(a,(0,0,4.85),(.72,.72,.78),L)
    return a

def b08_weeping_willow():
    a=asset('weeping_willow','large','tree');branch(a,(0,0,.02),(.22,0,3.2),.27,.15)
    for i in range(8):
        th=i*TAU/8;q=(1.8*math.cos(th),1.8*math.sin(th),3.9+.14*(i%3))
        branch(a,(.15,0,2.6),q,.12,.034);crown(a,q,(1.12,.96,.7),F)
        for j in range(3):
            t=th+(j-1)*.28;x=q[0]+.62*math.cos(t);y=q[1]+.62*math.sin(t)
            end=(x*1.08,y*1.08,.95+.32*(j%2));branch(a,(x,y,3.72),end,.016,.008,m=F,n=5)
            crown(a,(x,y,2.5),(.26,.27,1.45),L if j==1 else F,7)
    crown(a,(0,0,4.25),(1.7,1.5,.86),F)
    return a

def b08_eastern_redbud():
    a=asset('eastern_redbud','large','tree')
    for i in range(3):
        th=i*TAU/3;mid=(.35*math.cos(th),.35*math.sin(th),1.5);q=(1.1*math.cos(th),1.1*math.sin(th),2.65)
        branch(a,(0,0,0),mid,.10,.07);branch(a,mid,q,.07,.02)
        for j in range(3):
            e=add(q,(.5*math.cos(th+j*1.8),.5*math.sin(th+j*1.8),.25*(j%2)))
            branch(a,mid,e,.032,.012);crown(a,e,(.7,.61,.47),F)
            for k in range(3): crown(a,add(e,(.38*math.cos(k*2.1),.38*math.sin(k*2.1),.3)),(.20,.19,.13),'pink',6)
    return a

def b08_flowering_dogwood():
    a=asset('flowering_dogwood','large','tree');branch(a,(0,0,0),(.1,0,2.5),.12,.045)
    for i in range(7):
        th=i*2.4;z=1.45+(i%3)*.52;r=.95+(i%2)*.3;p=(0,0,z-.35);q=(r*math.cos(th),r*math.sin(th),z)
        branch(a,p,q,.047,.015);crown(a,q,(.74,.60,.25),F)
        for k in range(3):
            t=th+k*TAU/3; flower(a,add(q,(.39*math.cos(t),.35*math.sin(t),.22)),.15,'cream',4)
    return a

def b08_crape_myrtle():
    a=asset('crape_myrtle','large','tree')
    for i in range(5):
        th=i*TAU/5; q=(.7*math.cos(th),.7*math.sin(th),2.6+.3*(i%2))
        branch(a,(.1*math.cos(th),.1*math.sin(th),0),q,.076,.024,m='wood_light')
        crown(a,add(q,(0,0,.18)),(.64,.62,.64),F)
        for j in range(4):
            t=j*2.4+i;crown(a,add(q,(.38*math.cos(t),.38*math.sin(t),.45+.22*(j%2))),(.27,.25,.36),'pink',7)
    return a

def b08_flowering_cherry():
    a=asset('flowering_cherry','large','tree');branch(a,(0,0,0),(-.10,.04,1.65),.15,.11)
    for i in range(5):
        th=i*TAU/5;mid=(.7*math.cos(th),.7*math.sin(th),2.55);q=(1.55*math.cos(th),1.55*math.sin(th),2.95)
        branch(a,(-.1,.04,1.4),mid,.09,.05);branch(a,mid,q,.05,.019)
        crown(a,q,(.96,.9,.58),'pink')
        crown(a,add(mid,(0,0,.4)),(.85,.75,.68),'cream')
    crown(a,(0,0,3.4),(.95,.9,.7),'pink')
    return a

def b08_southern_magnolia():
    a=asset('southern_magnolia','large','tree');branch(a,(0,0,0),(.08,0,3.5),.19,.06)
    for i in range(8):
        th=i*2.4;z=1.8+(i%4)*.6;r=1.0-(i%4)*.09;q=(r*math.cos(th),r*math.sin(th),z)
        branch(a,(0,0,z-.6),q,.065,.022);crown(a,q,(.85,.74,.83),D)
        for j in range(3):
            t=th+j*1.4;p=add(q,(.5*math.cos(t),.5*math.sin(t),.24));leaf(a,p,add(p,(.27*math.cos(t),.27*math.sin(t),.10)),.09,F)
        if i%2==0: flower(a,add(q,(.42*math.cos(th),.42*math.sin(th),.45)),.19,'cream',7)
    crown(a,(0,0,4.0),(.7,.72,.85),D)
    return a

def b08_blue_spruce():
    a=asset('blue_spruce','large','tree');branch(a,(0,0,0),(0,0,5.35),.14,.025)
    for j in range(7):
        z=.65+j*.60;rad=1.46-j*.175
        for k in range(6):
            t=k*TAU/6+j*.73
            end=(rad*math.cos(t),rad*math.sin(t),z-.12)
            branch(a,(0,0,z+.29),end,.03,.007,B,5)
            # Drooping, flattened branch foliage preserves open gaps between whorls.
            mid=(end[0]*.69,end[1]*.69,z+.12)
            crown(a,mid,(rad*.46,rad*.34,.31 if j<4 else .24),D,7)
    crown(a,(0,0,5.01),(.25,.26,.53),F,7)
    return a

def b08_eastern_white_pine():
    a=asset('eastern_white_pine','large','tree');branch(a,(0,0,0),(0,0,6.5),.19,.02)
    for j in range(5):
        z=2.6+j*.68;rad=1.65-j*.23
        for k in range(4):
            th=k*TAU/4+j*.75;q=(rad*math.cos(th),rad*math.sin(th),z+.05)
            branch(a,(0,0,z-.23),q,.043,.015);crown(a,q,(rad*.55,rad*.46,.43),D)
    a.cone((0,0,5.45),(0,0,6.9),.72,F,9)
    return a

def b08_eastern_red_cedar():
    a=asset('eastern_red_cedar','large','tree');branch(a,(0,0,0),(.05,0,4.2),.13,.025)
    for j,(z,r) in enumerate(((.9,.91),(1.65,.98),(2.4,.8),(3.15,.56),(3.8,.35))):
        crown(a,(.12*math.sin(j*2),.10*math.cos(j),z),(r,r*.83,.92),D,8)
        for k in range(3):
            t=k*TAU/3+j*.7;crown(a,(r*.65*math.cos(t),r*.65*math.sin(t),z-.15),(r*.47,r*.45,.61),F,7)
    return a

def b08_arborvitae_screen_pair():
    a=asset('arborvitae_screen_pair','large','tree')
    for x,h in ((-.64,3.4),(.64,3.10)):
        branch(a,(x,0,0),(x,0,h*.86),.075,.016)
        crown(a,(x,0,h*.47),(.67,.58,h*.46),D,9)
        for j in range(5):
            t=j*2.4;crown(a,(x+.32*math.cos(t),.31*math.sin(t),.8+j*.37),(.37,.33,.67),F,7)
        a.cone((x,0,h*.76),(x,0,h+.12),.33,F,7)
    return a

def b08_bald_cypress():
    a=asset('bald_cypress','large','tree');a.cone((0,0,.01),(0,0,1.3),.46,B,9,radius2=.20)
    branch(a,(0,0,1),(0,0,5.4),.19,.035)
    for j in range(5):
        z=2+j*.62;r=1.45-j*.22
        for k in range(4):
            t=k*TAU/4+j*.6;q=(r*math.cos(t),r*math.sin(t),z)
            branch(a,(0,0,z-.1),q,.04,.012);crown(a,q,(r*.65,r*.40,.35),L)
    crown(a,(0,0,5.25),(.55,.55,.78),F)
    for x,y,h in ((.65,.22,.37),(-.6,-.35,.29),(.14,-.66,.46)):
        a.cone((x,y,0),(x,y,h),.13,B,7)
    return a

def b08_honeylocust():
    a=asset('honeylocust','large','tree');branch(a,(0,0,0),(.18,.04,2.7),.17,.08)
    for i in range(6):
        th=i*2.4;z=2.7+(i%3)*.6;q=(1.5*math.cos(th),1.5*math.sin(th),z)
        branch(a,(.1,0,1.9),q,.065,.018)
        for j in range(3):
            t=th+(j-1)*.75;v=add(q,(.65*math.cos(t),.65*math.sin(t),.12*j));branch(a,q,v,.022,.009);crown(a,v,(.69,.5,.39),L,8)
            if j==0:
                branch(a,add(v,(0,0,-.1)),add(v,(.08,0,-.49)),.018,.012,'brown',5)
    return a

def b08_staked_young_street_tree():
    a=asset('staked_young_street_tree','large','tree');disk(a,(0,0,0),.70,.025,'soil',12)
    branch(a,(0,0,.02),(.05,0,2.4),.052,.014)
    for i in range(5):
        th=i*2.4;q=(.52*math.cos(th),.52*math.sin(th),1.65+.2*i)
        branch(a,(0,0,1.3+.15*i),q,.022,.008);crown(a,q,(.42,.39,.51),F,8)
    for x in (-.42,.42):
        a.cylinder((x,0,.015),(x,0,1.48),.036,'wood',7)
        a.beam((x,0,1.35),(0,0,1.45),.022,.04,'rubber')
    a.cylinder((0,0,.03),(0,0,.52),.065,'cream',9)
    return a

# Shrubs: ten distinct habits, pruning forms and flowering structures.
def b08_boxwood_globe():
    a=asset('boxwood_globe');branch(a,(0,0,0),(0,0,.38),.045,.02)
    # Densely overlapping small shoots form a clipped spherical shrub, rather than
    # a single large sphere with a few attached bumps.
    for j,(z,r,count) in enumerate(((.24,.30,6),(.48,.37,8),(.73,.26,6),(.84,.10,3))):
        for i in range(count):
            t=i*TAU/count+j*.53
            crown(a,(r*math.cos(t),r*math.sin(t),z),(.22,.22,.22),D if j==0 else F,7)
    return a

def b08_clipped_yew_hedge():
    a=asset('clipped_yew_hedge','large','shrub')
    for x in (-1.1,-.55,0,.55,1.1): branch(a,(x,0,0),(x,0,.58),.043,.024)
    # Chamfered, deliberately pruned rectangular profile.
    pts=[(-1.4,-.39),(-1.29,-.5),(1.29,-.5),(1.4,-.39),(1.4,.39),(1.29,.5),(-1.29,.5),(-1.4,.39)]
    a.prism(pts,.17,1.24,D)
    for x in (-1.1,-.58,0,.57,1.1):
        crown(a,(x,0,1.23),(.34,.42,.16),F,8)
        for y in (-.46,.46):
            for z in (.39,.82): crown(a,(x,y,z),(.32,.085,.25),D if z<.6 else F,7)
    return a

def b08_privet_flowering_hedge():
    a=asset('privet_flowering_hedge','large','shrub')
    for i,x in enumerate((-1,-.5,0,.5,1)):
        branch(a,(x,0,0),(x,.04,1.0),.055,.017)
        crown(a,(x,.03,.82),(.51,.47,.71),F)
        for j in range(3):
            t=i+j*2;crown(a,(x+.27*math.cos(t),.30*math.sin(t),1.27+.10*(j%2)),(.12,.12,.2),'cream',6)
    return a

def b08_creeping_juniper():
    a=asset('creeping_juniper')
    for i in range(9):
        th=i*2.4;r=.5+.36*(i%3)/2;p=(r*.55*math.cos(th),r*.55*math.sin(th),.12);q=(r*math.cos(th),r*math.sin(th),.21+.05*(i%2))
        branch(a,(0,0,.09),q,.029,.009)
        crown(a,p,(.39,.25,.16),D,7);crown(a,q,(.35,.21,.14),F,7)
    return a

def b08_rhododendron():
    a=asset('rhododendron')
    for i in range(5):
        t=i*2.4;r=.47 if i else 0;q=(r*math.cos(t),r*math.sin(t),.79+.24*(i%3)/2)
        branch(a,(0,0,.02),q,.028,.010)
        for j in range(6):
            th=j*TAU/6;leaf(a,add(q,(0,0,-.1)),add(q,(.30*math.cos(th),.30*math.sin(th),-.07)),.075,D)
        for j in range(3):
            th=j*TAU/3;flower(a,add(q,(.12*math.cos(th),.12*math.sin(th),.10)),.095,'pink',5)
    return a

def b08_azalea_mound():
    a=asset('azalea_mound');crown(a,(0,0,.40),(.77,.61,.40),D)
    for i in range(14):
        t=i*2.4;r=.16+.42*(i%4)/3;x=r*math.cos(t);y=r*.8*math.sin(t);z=.60-.14*(i%4)/3
        crown(a,(x,y,z),(.19,.18,.19),F,7)
        flower(a,(x,y,z+.15),.095,'pink',5)
    return a

def b08_hydrangea():
    a=asset('hydrangea')
    for i in range(7):
        t=i*2.4;r=.45*(i%3)/2;q=(r*math.cos(t),r*math.sin(t),.82+.22*(i%2))
        branch(a,(0,0,0),q,.018,.009,B,5)
        for sg in (-1,1): leaf(a,add(q,(0,0,-.23)),add(q,(sg*.29,.08,-.12)),.13,F)
        crown(a,q,(.22,.21,.19),'cream',9)
        for j in range(4):
            th=j*TAU/4;crown(a,add(q,(.13*math.cos(th),.13*math.sin(th),.13)),(.095,.09,.075),'white',6)
    return a

def b08_forsythia():
    a=asset('forsythia')
    for i in range(9):
        t=i*2.4;h=1.2+.22*(i%3);p=(.34*math.cos(t),.34*math.sin(t),h);q=(.93*math.cos(t),.93*math.sin(t),h-.25)
        branch(a,(0,0,0),p,.024,.011);branch(a,p,q,.012,.006)
        for j in range(2):
            base=add(mul(p,1-j/2),mul(q,j/2));flower(a,base,.056,'yellow',4,core='gold')
        leaf(a,p,add(p,(.17*math.cos(t),.17*math.sin(t),.07)),.045,L)
    return a

def b08_common_lilac():
    a=asset('common_lilac')
    for i in range(7):
        th=i*2.4;h=1.28+.36*(i%3)/2;q=(.45*math.cos(th),.45*math.sin(th),h)
        branch(a,(.1*math.cos(th),.1*math.sin(th),0),q,.034,.012)
        crown(a,add(q,(0,0,-.27)),(.34,.29,.41),F,8)
        for j in range(3):
            p=add(q,(.13*math.cos(j*2.1),.13*math.sin(j*2.1),.09*j));a.cone(p,add(p,(0,0,.35)),.13,'purple',7)
    return a

def b08_redtwig_dogwood_winter():
    a=asset('redtwig_dogwood_winter')
    for i in range(11):
        th=i*2.4;r=.22+.35*(i%4)/3;h=1.15+.46*(i%3)/2;q=(r*math.cos(th),r*math.sin(th),h)
        branch(a,(.08*math.cos(th),.08*math.sin(th),0),q,.02,.007,'brick',6)
        for j in range(2):
            p=mul(q,.6+j*.18);e=add(p,(.24*math.cos(th+j),.24*math.sin(th+j),.32));branch(a,p,e,.009,.003,'brick',5)
    return a

# Ornamental grasses and a wetland margin clump.
def b08_maiden_grass():
    a=asset('maiden_grass');blade_clump(a,0,0,0,1.08,.72,23,F)
    for i in range(7):
        t=i*2.4;q=(.31*math.cos(t),.31*math.sin(t),1.56+.20*(i%3)/2);branch(a,(0,0,.04),q,.008,.004,'wood_light',5)
        for j in range(3): crown(a,add(q,(.05*j,0,.10*j)),(.07,.06,.19),'cream',6)
    return a

def b08_fountain_grass():
    a=asset('fountain_grass');blade_clump(a,0,0,0,.67,.64,21,F)
    for i in range(9):
        t=i*2.4;mid=(.23*math.cos(t),.23*math.sin(t),.82);end=(.48*math.cos(t),.48*math.sin(t),.94+.10*(i%3))
        branch(a,(0,0,0),mid,.007,.005,'wood_light',5);branch(a,mid,end,.005,.003,'wood_light',5)
        a.cylinder(end,add(end,(.10*math.cos(t),.10*math.sin(t),.22)),.04,'brown',6,radius2=.026)
    return a

def b08_pampas_grass():
    a=asset('pampas_grass');blade_clump(a,0,0,0,1.18,.86,22,F)
    for i in range(6):
        t=i*2.4;q=(.33*math.cos(t),.33*math.sin(t),1.63+.31*(i%3)/2);branch(a,(0,0,.04),q,.014,.009,'wood_light',6)
        crown(a,add(q,(.035,0,.27)),(.12,.10,.38),'cream',8)
        crown(a,add(q,(.02,0,.15)),(.15,.12,.20),'sand',7)
    return a

def b08_switchgrass():
    a=asset('switchgrass');blade_clump(a,0,0,0,1.05,.37,17,L)
    for i in range(8):
        t=i*2.4;x=.21*math.cos(t);y=.21*math.sin(t);z=1.27+.22*(i%3)/2
        branch(a,(0,0,.06),(x,y,z),.006,.003,F,5)
        for j in range(4):
            th=t+j*2.1;p=(x,y,z-.20+j*.045);q=(x+.13*math.cos(th),y+.13*math.sin(th),z+.08*j)
            branch(a,p,q,.004,.002,'wood_light',5);crown(a,q,(.027,.024,.046),'sand',5)
    return a

def b08_cattail_cluster():
    a=asset('cattail_cluster');blade_clump(a,0,0,0,1.35,.45,14,F)
    for i in range(6):
        t=i*2.4;x=.21*math.cos(t);y=.21*math.sin(t);h=1.40+.30*(i%3)/2
        branch(a,(x,y,0),(x+.04,y,h+.29),.012,.005,F,6)
        a.cylinder((x+.035,y,h-.07),(x+.04,y,h+.19),.037,'brown',7,radius2=.034)
        branch(a,(x+.04,y,h+.20),(x+.04,y,h+.36),.006,.003,'brown',5)
    return a

# Perennials and bulbs. Leaf structures and inflorescences distinguish species.
def b08_daylily_clump():
    a=asset('daylily_clump');blade_clump(a,0,0,0,.44,.40,17,F)
    for i in range(5):
        t=i*2.4;p=(.22*math.cos(t),.22*math.sin(t),.64+.07*(i%2));branch(a,(0,0,0),p,.009,.006,F,5)
        # Six long pointed tepals around a trumpet throat.
        a.cone(add(p,(0,0,-.045)),add(p,(0,0,.04)),.034,'gold',6)
        flower(a,add(p,(0,0,.045)),.15,'orange',6,'gold')
    return a

def b08_flowering_hosta():
    a=asset('flowering_hosta')
    for i in range(14):
        t=i*2.4;r=.30+.16*(i%3)/2;leaf(a,(0,0,.045),(r*math.cos(t),r*math.sin(t),.14+.10*(i%2)),.115,F,.18)
    for i in range(3):
        x=(i-1)*.14;y=.04*(i%2);branch(a,(x,y,.08),(x,y,.95),.009,.005,F,5)
        for j in range(4):
            z=.55+j*.10;sg=1 if j%2 else -1;p=(x+sg*.08,y,z);branch(a,(x,y,z+.03),p,.004,.002,F,5)
            a.cone(add(p,(0,0,-.055)),add(p,(0,0,.035)),.039,'purple',6)
    return a

def b08_bearded_iris():
    a=asset('bearded_iris')
    for i in range(12):
        th=(i%3)*.38+(math.pi if i%2 else 0);r=.10+.13*(i%4)/3;leaf(a,(0,(i%3-1)*.045,0),(r*math.cos(th),r*math.sin(th),.52+.18*(i%3)/2),.036,F,.025)
    for i,(x,y,h) in enumerate(((-.1,0,.83),(.11,.06,.72),(.02,-.08,.96))):
        branch(a,(x,y,0),(x,y,h),.01,.006,F,5)
        for j in range(3):
            t=j*TAU/3;leaf(a,(x,y,h),(x+.13*math.cos(t),y+.13*math.sin(t),h-.09),.055,'purple',.04)
            leaf(a,(x,y,h),(x+.07*math.cos(t+.6),y+.07*math.sin(t+.6),h+.14),.05,'purple',.03)
        crown(a,(x,y,h),(.032,.032,.033),'yellow',6)
    return a

def b08_purple_coneflowers():
    a=asset('purple_coneflowers')
    for i in range(7):
        t=i*2.4;r=.30*(i%3)/2;x=r*math.cos(t);y=r*math.sin(t);h=.62+.27*(i%4)/3;p=(x,y,h)
        branch(a,(x*.7,y*.7,0),p,.009,.005,F,5)
        leaf(a,(x,y,h*.43),(x+.16,y+.09,h*.52),.051,F)
        for j in range(9):
            th=j*TAU/9;leaf(a,p,(x+.105*math.cos(th),y+.105*math.sin(th),h-.032),.020,'pink',.008)
        a.cone(p,add(p,(0,0,.060)),.040,'brown',8)
    return a

def b08_black_eyed_susans():
    a=asset('black_eyed_susans')
    for i in range(10):
        t=i*2.4;r=.31*(i%4)/3;x=r*math.cos(t);y=r*math.sin(t);h=.38+.24*(i%3)/2
        flower(a,(x,y,h),.077,'yellow',8,'wood_dark',stem=(x*.65,y*.65,0))
    return a

def b08_tulip_cluster():
    a=asset('tulip_cluster')
    for i in range(7):
        th=i*2.4;r=.24*(i%3)/2;x=r*math.cos(th);y=r*math.sin(th);h=.37+.12*(i%3)/2
        branch(a,(x,y,0),(x,y,h),.008,.006,F,6)
        for sg in (-1,1):leaf(a,(x,y,.05),(x+sg*.12,y+.05,.30),.038,F,.04)
        # Upright six overlapping petals form a closed cup with a dark interior.
        crown(a,(x,y,h+.055),(.059,.059,.072),'brick',6)
        for j in range(6):
            t=j*TAU/6;leaf(a,(x,y,h-.006),(x+.049*math.cos(t),y+.049*math.sin(t),h+.12),.030,'red',.022)
    return a

def b08_daffodil_cluster():
    a=asset('daffodil_cluster');blade_clump(a,0,0,0,.31,.16,13,F)
    for i in range(6):
        t=i*2.4;x=.17*math.cos(t);y=.17*math.sin(t);h=.34+.07*(i%3);p=(x+.04,y,h)
        branch(a,(x,y,0),(x,y,h+.035),.006,.004,F,5);branch(a,(x,y,h+.035),p,.004,.003,F,5)
        flower(a,p,.070,'cream',6,'yellow')
        a.cylinder(add(p,(0,0,.005)),add(p,(0,0,.061)),.019,'yellow',7,radius2=.032)
    return a

def b08_lavender_patch():
    a=asset('lavender_patch')
    for i in range(13):
        t=i*2.4;r=.31*(i%4)/3;x=r*math.cos(t);y=r*math.sin(t);h=.42+.20*(i%3)/2
        branch(a,(x*.6,y*.6,0),(x,y,h),.006,.003,F,5)
        for z in (.08,.16,.24):
            leaf(a,(x*.8,y*.8,z),(x+.10,y+.018,z+.025),.015,L)
        for j in range(3):crown(a,(x,y,h+.044*j),(.025-.004*j,.025-.004*j,.046),'purple',6)
    return a

def b08_salvia_border():
    a=asset('salvia_border')
    for i in range(9):
        x=(i%3-1)*.24;y=(i//3-1)*.19;h=.38+.15*((i+1)%3)/2
        branch(a,(x,y,0),(x,y,h+.12),.009,.004,F,5)
        for sg in (-1,1):leaf(a,(x,y,.13),(x+sg*.13,y+.055,.21),.044,F)
        for j in range(5):
            z=h+j*.045;r=.036-j*.004
            crown(a,(x,y,z),(r,r,.035),'purple',6)
    return a

# Six planted containers / civic beds, not empty garden furnishings.
def b08_geranium_window_box():
    a=asset('geranium_window_box')
    a.box((0,0,.145),(1.0,.29,.27),'terracotta');a.box((0,0,.287),(1.05,.34,.05),'terracotta');a.box((0,0,.32),(.94,.25,.014),'soil')
    for x in (-.34,0,.34):
        crown(a,(x,0,.43),(.20,.18,.15),D,8)
        for j in range(2):
            t=j*2.4;p=(x+.10*math.cos(t),.07*math.sin(t),.58+.06*(j%2));branch(a,(x,0,.32),p,.009,.005,F,5)
            for k in range(3):flower(a,add(p,(.039*math.cos(k*2.1),.039*math.sin(k*2.1),.02)),.045,'red',5)
    return a

def b08_hanging_petunia_basket():
    a=asset('hanging_petunia_basket')
    a.cylinder((0,0,.05),(0,0,.28),.13,'wood_dark',10,radius2=.27);disk(a,(0,0,.281),.245,.008)
    a.torus((0,0,.278),.266,.025,'dark_metal',segments=12,sides=4)
    for j in range(3):
        t=j*TAU/3;branch(a,(.25*math.cos(t),.25*math.sin(t),.29),(0,0,.86),.005,.005,'dark_metal',5)
    a.torus((0,0,.89),.033,.008,'dark_metal',axis='x',segments=8,sides=4,arc=math.pi*1.6)
    for i in range(9):
        t=i*2.4;r=.19+.09*(i%2);z=.30 if i%2 else .13
        crown(a,(r*math.cos(t),r*math.sin(t),z),(.13,.11,.17),F,7)
        flower(a,(r*math.cos(t),r*math.sin(t),z+.11),.069,'pink',5)
    return a

def b08_whiskey_barrel_flowers():
    a=asset('whiskey_barrel_flowers');a.cylinder((0,0,.02),(0,0,.52),.32,'wood',14,radius2=.39)
    for z,r in ((.10,.334),(.42,.38)):
        a.torus((0,0,z),r,.024,'dark_metal',segments=14,sides=4)
    for i in range(14):
        t=i*TAU/14;branch(a,(.325*math.cos(t),.325*math.sin(t),.06),(.385*math.cos(t),.385*math.sin(t),.52),.008,.008,'wood_dark',4)
    disk(a,(0,0,.528),.357,.012)
    blade_clump(a,0,0,.54,.48,.21,9,F)
    for i in range(8):
        t=i*2.4;r=.25;p=(r*math.cos(t),r*math.sin(t),.69+.11*(i%3)/2)
        flower(a,p,.073,'yellow',7,'brown',stem=(r*.7*math.cos(t),r*.7*math.sin(t),.54))
    return a

def b08_concrete_mixed_planter():
    a=asset('concrete_mixed_planter')
    a.box((0,0,.32),(.85,.85,.64),'concrete');a.box((0,0,.665),(.93,.93,.07),'concrete_light');a.box((0,0,.708),(.77,.77,.017),'soil')
    blade_clump(a,.1,.05,.72,.80,.36,15,F)
    for i in range(5):
        t=i*TAU/5;r=.28;p=(r*math.cos(t),r*math.sin(t),.9)
        crown(a,p,(.20,.18,.16),D,7);flower(a,add(p,(0,0,.14)),.085,'cream',6)
    for i in range(3):
        x=(i-1)*.16;branch(a,(x,-.32,.77),(x,-.49,.38),.008,.005,F,5)
        for j in range(3):leaf(a,(x,-.40,.63-j*.09),(x+.08,-.5,.58-j*.09),.048,F)
    return a

def b08_circular_civic_flower_bed():
    a=asset('circular_civic_flower_bed','large')
    disk(a,(0,0,.015),1.32,.11)
    for i in range(18):
        t=i*TAU/18;a.box((1.35*math.cos(t),1.35*math.sin(t),.095),(.26,.13,.19),'brick',rot=t+math.pi/2)
    for i in range(12):
        t=i*TAU/12;r=.96;flower(a,(r*math.cos(t),r*math.sin(t),.39),.091,'yellow',6,'brown',stem=(r*math.cos(t),r*math.sin(t),.13))
    for i in range(5):
        t=i*TAU/5;r=.48;flower(a,(r*math.cos(t),r*math.sin(t),.66),.11,'pink',7,'yellow',stem=(r*math.cos(t),r*math.sin(t),.13))
    blade_clump(a,0,0,.13,.83,.29,11,F)
    return a

def b08_raised_perennial_bed():
    a=asset('raised_perennial_bed','large');rect_bed(a,2.6,1.0,.32)
    for x in (-1.22,1.22):
        for y in (-.43,.43):a.box((x,y,.23),(.075,.075,.46),'wood')
    for x in (-.92,-.33,.33,.92):
        blade_clump(a,x,.22,.33,.46,.20,7,F)
        for j in range(3):
            p=(x+(j-1)*.12,.24,.98+.12*(j%2));branch(a,(x,.24,.34),p,.006,.003,F,5)
            for k in range(4):crown(a,add(p,(0,0,.045*k)),(.035,.035,.035),'purple',6)
    for x in (-.96,-.48,0,.48,.96):
        flower(a,(x,-.24,.58),.086,'cream',6,'yellow',stem=(x,-.24,.33))
    return a

REVIEW_RETAIN = {
 'hydrangea':'Existing branching stems, broad leaves and compound rounded blossom heads already provide species-specific structure.',
 'bearded_iris':'Existing keeled leaf fans, separate fall/standard petals and staggered stems already convey iris structure.',
 'black_eyed_susans':'Separate keeled petals, flower centres and paired stem leaves already carry the needed structure.',
 'cattail_cluster':'Separate leaf blades, seed cylinders, tips and varied stem heights already resolve the silhouette.',
 'daffodil_cluster':'Existing six petals, projecting trumpet and bending stems are species-specific; no extra tessellation needed.',
 'daylily_clump':'Long separate tepals, throat, keeled foliage and varying stem heights already support the intended form.',
 'flowering_hosta':'Broad keeled basal leaves and separate hanging flowers already represent the species.',
 'forsythia':'Existing arched twig structure and small separate flowers are appropriate for open spring growth.',
 'fountain_grass':'Curving blades and bent seed stems already form the appropriate fountain habit.',
 'lavender_patch':'Narrow leaves, multi-lobed spikes and varied heights already provide botanical construction.',
 'maiden_grass':'Curved blades and lobed panicles already supply the essential structure.',
 'pampas_grass':'Separate arching leaves and elongated compound plumes already distinguish the grass.',
 'purple_coneflowers':'Separate drooping petals and raised cone centres already provide the botanical shape.',
 'redtwig_dogwood_winter':'Bare tapered branches and paired secondary twigs are appropriate for the winter state.',
 'rhododendron':'Radial leathery leaves and individual flowers are already modeled; no generic canopy mass to replace.',
 'salvia_border':'Paired broad leaves and tapered whorled flower spikes already define this perennial.',
 'switchgrass':'Open secondary seed panicles and upright blades are already structurally specific.',
 'tulip_cluster':'Separate upright overlapping petals and broad basal leaves already define the bloom.',
 'whiskey_barrel_flowers':'Individual flowers/blades and geometric barrel staves/hoops already carry sufficient construction.',
 'circular_civic_flower_bed':'The brick ring and individually modeled flowering plants already carry necessary detail.',
 'raised_perennial_bed':'Existing board corners, stakes and separate species are structurally developed.'
}
REVIEW = {}
_FACTORIES=[v for k,v in list(globals().items()) if k.startswith('b08_') and callable(v)]
assert len(_FACTORIES)==50, len(_FACTORIES)
for _factory in _FACTORIES:
    _prototype=_factory()
    _name=_prototype.name
    _category=_prototype.category
    _size=_prototype.size_class
    _short=_name.removeprefix('b08_')
    REVIEW[_name]={'status':'retained' if _short in REVIEW_RETAIN else 'revised',
        'reason':REVIEW_RETAIN.get(_short,'Replaced repeated spherical foliage with asymmetrical, scalloped, tapered crown topology; species branching/proportions preserved.')}
    if _short=='boxwood_globe': REVIEW[_name]['reason']='Rebuilt the single large globe with attached bumps as densely overlapping small shoot groups, keeping a clipped spherical habit.'
    if _short=='blue_spruce': REVIEW[_name]['reason']='Replaced stacked conical shells with individual drooping boughs, broken whorls and irregular foliage pads.'
    if _short=='clipped_yew_hedge': REVIEW[_name]['reason']='Added shallow leaf growth across clipped side planes and irregular crown tips so the hedge no longer reads as a solid block.'
    if _short in ('mature_white_oak','sugar_maple','tulip_poplar'): REVIEW[_name]['reason']+=' Main boughs now taper through an elbow into visible daughter forks.'
    def _make(f=_factory):
        return f().bottom_center()
    register(_name,_category,_size,_make)
del _prototype, _factory, _name, _category, _size, _make
