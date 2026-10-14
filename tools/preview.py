"""Render catalog previews directly from authored polygon geometry (software shading)."""
from pathlib import Path
import sys, importlib.util, math, json, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,str(Path(__file__).parent))
from assetlib import REGISTRY, PALETTE, Asset
from validate import read_glb, accessor_values
ROOT=Path(__file__).resolve().parents[1]

def load_batches():
    for p in sorted((ROOT/'batches').glob('batch*.py')):
        spec=importlib.util.spec_from_file_location(p.stem,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def render(a,size=256):
    a.bottom_center(); v=np.array(a.vertices)
    eye=np.array([1.5,-2.2,1.5]); eye/=np.linalg.norm(eye)
    right=np.cross([0,0,1],eye);right/=np.linalg.norm(right)
    up=np.cross(eye,right)
    p=np.stack((v@right,-v@up,v@eye),axis=1)
    lo=p[:,:2].min(axis=0); hi=p[:,:2].max(axis=0)
    scale=(size-30)/max(max(hi-lo),.001)
    xy=(p[:,:2]-(lo+hi)/2)*scale+np.array([size/2,size/2-3])
    pixels=np.empty((size,size,3),dtype=np.uint8);pixels[:]=[233,230,223]
    depth=np.full((size,size),-np.inf)
    light=np.array([-.4,-.6,1]);light/=np.linalg.norm(light)
    order=sorted(range(len(a.faces)),key=lambda i: float(np.mean(p[list(a.faces[i]),2])))
    for i in order:
        f=a.faces[i]; coords=v[list(f)]
        n=np.zeros(3)
        for j in range(1,len(f)-1): n+=np.cross(coords[j]-coords[0],coords[j+1]-coords[0])
        nlen=np.linalg.norm(n)
        if nlen<1e-12:continue
        n/=nlen
        # Two-sided preview exposes authored surfaces even if winding needs review.
        if n@eye<0:n=-n
        shade=.53+.47*max(float(n@light),0)
        h=PALETTE[a.face_materials[i]][0].lstrip('#');color=tuple(int(int(h[j:j+2],16)*shade) for j in (0,2,4))
        # Triangulated barycentric depth test: broad panels must not obscure glyphs.
        for j in range(1,len(f)-1):
            ids=[f[0],f[j],f[j+1]];tri=xy[ids];zz=p[ids,2]
            x0=max(0,int(math.floor(tri[:,0].min())));x1=min(size-1,int(math.ceil(tri[:,0].max())))
            y0=max(0,int(math.floor(tri[:,1].min())));y1=min(size-1,int(math.ceil(tri[:,1].max())))
            if x0>x1 or y0>y1:continue
            ax,ay=tri[0];bx,by=tri[1];cx,cy=tri[2]
            den=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
            if abs(den)<1e-10:continue
            yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
            u=((by-cy)*(xx-cx)+(cx-bx)*(yy-cy))/den
            w=((cy-ay)*(xx-cx)+(ax-cx)*(yy-cy))/den
            t=1-u-w;z=u*zz[0]+w*zz[1]+t*zz[2]
            region=depth[y0:y1+1,x0:x1+1]
            mask=(u>=-1e-6)&(w>=-1e-6)&(t>=-1e-6)&(z>region)
            region[mask]=z[mask];pixels[y0:y1+1,x0:x1+1][mask]=color
    return Image.fromarray(pixels)

def exported_asset(name,row):
    path=ROOT/'exports'/f'{name}.glb'
    if not path.exists(): return row['factory']()
    doc,binary=read_glb(path,True);a=Asset(name,row['category'],row['size_class'])
    for mesh in doc['meshes']:
        for p in mesh['primitives']:
            positions=accessor_values(doc,binary,p['attributes']['POSITION'])
            indices=[v[0] for v in accessor_values(doc,binary,p['indices'])]
            mat=doc['materials'][p['material']]['name']
            a.mesh([(x,-z,y) for x,y,z in positions],[indices[i:i+3] for i in range(0,len(indices),3)],mat)
    return a

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--batch');args=ap.parse_args();load_batches()
    out=ROOT/'previews';(out/'items').mkdir(parents=True,exist_ok=True)
    if not args.batch:
        for stale in (out/'items').glob('*.png'):
            if stale.stem not in REGISTRY:stale.unlink()
    fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    try:font=ImageFont.truetype(fontpath,14);small=ImageFont.truetype(fontpath,11);title=ImageFont.truetype(fontpath,25)
    except OSError:font=small=title=ImageFont.load_default()
    groups={};catalog=[]
    manifest={r['name']:r for r in json.loads((ROOT/'manifest.json').read_text())['assets']} if (ROOT/'manifest.json').exists() else {}
    for name,row in sorted(REGISTRY.items()):
        if args.batch and not name.startswith(args.batch):continue
        a=exported_asset(name,row);a.bottom_center();a.validate();im=render(a,256);im.save(out/'items'/f'{name}.png',optimize=True)
        entry={'name':name,'category':row['category'],'size_class':row['size_class'],'source_vertices':manifest.get(name,{}).get('source_vertices',len(a.vertices)),'dimensions_m':[round(y-x,3) for x,y in zip(*a.bounds())]}
        catalog.append(entry);groups.setdefault(name.split('_')[0],[]).append((entry,im))
    if not args.batch:
        groups["overview"]=[items[len(items)//3] for items in groups.values()]
    for batch,items in groups.items():
        w=1250;cw=250;ch=282;sheet=Image.new('RGB',(w,75+ch*math.ceil(len(items)/5)),'#f4f1ea');d=ImageDraw.Draw(sheet)
        d.text((22,15),(f'{batch.upper()}  /  {len(items)} assets' if batch!='overview' else f'AMERICAN CITY  /  {len(catalog)} assets — representative selection'),fill='#25343b',font=title)
        d.text((22,49),'Geometry • orthographic software-shaded previews • not scale matched',fill='#59636a',font=small)
        for i,(entry,im) in enumerate(items):
            x=(i%5)*cw;y=75+(i//5)*ch
            sheet.paste(im.resize((238,238)),(x+6,y))
            label=entry['name'][4:].replace('_',' ')
            if len(label)>33:
                cut=label.rfind(' ',0,33);cut=cut if cut>0 else 33
                lines=[label[:cut],label[cut:].strip()]
            else:lines=[label]
            for j,line in enumerate(lines):d.text((x+9,y+240+j*16),line,fill='#24323a',font=small)
        sheet.save(out/f'{batch}.jpg',quality=90)
        print(batch,len(items),flush=True)
    if not args.batch:
        (out/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')
        data=json.dumps(catalog)
        html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>American City • 1,000 low-poly assets</title><style>*{box-sizing:border-box}body{margin:0;background:#f4f1ea;color:#25343b;font:15px system-ui}header{padding:32px 4vw;border-bottom:1px solid #d4d1c8}h1{font-size:32px;margin:0 0 12px}p{max-width:850px;line-height:1.6}input,select{padding:12px;border:1px solid #a6aaa8;background:#fffaf2;border-radius:5px;margin:5px 8px 5px 0}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:18px;padding:25px 4vw}article{background:#e9e6df;border-radius:6px;overflow:hidden}img{width:100%;aspect-ratio:1;object-fit:contain}section{padding:12px}h2{font-size:15px;margin:0 0 8px}small{color:#57676c}a{color:#34688d}footer{padding:24px 4vw}</style><header><h1>American City / 1,000 everyday objects</h1><p>Original low-poly game props. Meter scale, bottom-centered origin, shared material palette. Previews use software shading of the exported geometry and are individually fitted to frame. GLBs embed the same palette definitions; re-use materials by name in your engine.</p><input id="q" placeholder="Search objects…" aria-label="Search objects"><select id="size" aria-label="Size class"><option value="">All sizes</option><option>handheld</option><option>person</option><option>large</option></select><span id="count"></span></header><main id="grid"></main><footer><a href="../city_items.blend">Download master Blender file</a> · <a href="../manifest.json">Validation manifest</a></footer><script>const items=DATA;const grid=document.getElementById('grid'),q=document.getElementById('q'),s=document.getElementById('size');function draw(){const found=items.filter(i=>(i.name+' '+i.category).toLowerCase().includes(q.value.toLowerCase())&&(!s.value||i.size_class===s.value));document.getElementById('count').textContent=found.length+' assets';grid.innerHTML=found.map(i=>`<article><a href="../exports/${i.name}.glb"><img loading="lazy" src="items/${i.name}.png" alt="${i.name}"></a><section><h2>${i.name.slice(4).replaceAll('_',' ')}</h2><small>${i.size_class} · ${i.source_vertices} source vertices<br>${i.dimensions_m.join(' × ')} m</small><p><a href="../exports/${i.name}.glb">Download GLB</a></p></section></article>`).join('')}q.oninput=s.onchange=draw;draw();</script></html>'''.replace('DATA',data)
        (out/'index.html').write_text(html)
    print(f'Previewed {len(catalog)} assets.',flush=True)
if __name__=='__main__':main()
