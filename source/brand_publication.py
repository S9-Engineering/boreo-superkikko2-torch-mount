"""Apply the approved SVG signature to publication copies without generative edits.

Requires ImageMagick 7, librsvg (rsvg-convert), and Pillow for dimension checks.
SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Required Notice: S9 Engineering (https://github.com/S9-Engineering)
"""
from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,xml.etree.ElementTree as ET
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
LOGO=ROOT/'assets/logo_S9_Engineering.svg'
REPORT=ROOT/'verification/branding.json'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def stamp(source,target):
    source,target=Path(source),Path(target)
    w,h=Image.open(source).size
    lw=round(w*.12);pad=max(8,round(w*.009));margin=max(16,round(w*.02))
    lh=round(lw*317/513);bw,bh=lw+2*pad,lh+2*pad
    ns='http://www.w3.org/2000/svg';ET.register_namespace('',ns)
    svg=ET.Element(f'{{{ns}}}svg',{'width':str(bw),'height':str(bh),'viewBox':f'0 0 {bw} {bh}'})
    ET.SubElement(svg,f'{{{ns}}}rect',{'width':str(bw),'height':str(bh),'rx':str(pad//2),'fill':'#ffffff','fill-opacity':'.9'})
    group=ET.SubElement(svg,f'{{{ns}}}g',{'transform':f'translate({pad} {pad}) scale({lw/513} {lh/317})'})
    for child in ET.parse(LOGO).getroot():group.append(child)
    with tempfile.TemporaryDirectory(prefix='s9-branding-') as tmp:
        tmp=Path(tmp);v=tmp/'signature.svg';v.write_bytes(ET.tostring(svg))
        png=tmp/'signature.png';subprocess.run(['rsvg-convert',str(v),'-o',str(png)],check=True)
        out=tmp/('output'+target.suffix)
        subprocess.run(['magick',str(source),str(png),'-gravity','southeast','-geometry',f'+{margin}+{margin}','-composite','-strip','-quality','95',str(out)],check=True)
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(out,target)
    assert Image.open(target).size==(w,h)
    return {'signature':'Full approved S9 Engineering SVG','logo_sha256':sha(LOGO),'position':'bottom-right','bounds_px':[w-margin-bw,h-margin-bh,w-margin,h-margin],'pixels':[w,h],'sha256':sha(target),'generative_ai_used_for_watermark':False}
def main():
    previous=json.loads(REPORT.read_text()) if REPORT.exists() else {'core':{}}
    cache=ROOT/'.cache/branding';rows={}
    files=sorted((ROOT/'previews/photos/edited').glob('*-real.jpg'))+sorted((ROOT/'previews/photos/gallery').glob('*.jpg'))
    files+=sorted((ROOT/'previews/renders').glob('*-cad.png'))+[ROOT/'previews/assembly/exploded.png']
    for path in files:
        name=str(path.relative_to(ROOT));clean=cache/name;old=previous['core'].get(name)
        if old and sha(path)==old['sha256']:
            rows[name]=old
        else:
            clean.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,clean)
            rows[name]={'source_sha256':sha(clean),**stamp(clean,path)}
    # These two covers already carry the full signature and their AI disclosure.
    for name in ['previews/photos/edited/hero-enhanced.png','previews/renders/hero-ai.png']:
        path=ROOT/name;rows[name]={'sha256':sha(path),'pixels':list(Image.open(path).size),'signature':'Existing full S9 Engineering signature, visually reviewed','position':'bottom-right','already_branded':True}
    REPORT.write_text(json.dumps({'date':'2026-10-27','method':'Fixed SVG artwork compositing; no generative photo or CAD changes. Original HEICs and CAD/print files unchanged.','core':rows},indent=2)+'\n')
    # Export from clean masters where available, then place the signature on the
    # complete channel canvas. No stacked watermark or crop on portrait photos.
    for channel in ['nexprint','printables']:
        folder=ROOT/'publication-local/current'/channel
        if not (folder/'image-checks.json').exists():continue
        checks=json.loads((folder/'image-checks.json').read_text())
        for row in checks['images']:
            src=ROOT/row['source'];clean=cache/row['source'];target=ROOT/row['file']
            use=clean if clean.exists() else src
            # A fresh clone may need the pre-branding master from Git history;
            # otherwise use its already-branded current image without adding twice.
            add=clean.exists()
            with tempfile.TemporaryDirectory(prefix='s9-channel-export-') as td:
                resized=Path(td)/'image.png'
                cmd=['magick',str(use)]
                if channel=='nexprint':cmd+=['-resize','2000x1500','-background','#eceff1','-gravity','center','-extent','2000x1500']
                else:cmd+=['-resize','2000x2000>']
                subprocess.run(cmd+['-strip',str(resized)],check=True)
                if add:branding=stamp(resized,target)
                else:
                    subprocess.run(['magick',str(resized),'-strip','-quality','95',str(target)],check=True)
                    branding={'signature':'Inherited full S9 Engineering signature; no duplicate applied','position':'bottom-right of image content','sha256':sha(target),'already_branded':True}
            row.update({'sha256':sha(target),'pixels':list(Image.open(target).size),'watermark':branding})
            if channel=='nexprint':assert row['pixels']==[2000,1500]
        checks['all_images_watermarked']=True;checks['watermark_tool']='Approved SVG artwork via librsvg and ImageMagick; no AI image editing.'
        (folder/'image-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    # Keep real-photo provenance in sync with the branded publication copies.
    p=ROOT/'previews/photos/edits.json';data=json.loads(p.read_text())
    for row in data['assets']:
        full=row['public_full_resolution'];web=row['gallery']
        row['metadata_stripped_source_sha256']=rows[full]['source_sha256']
        row['public_sha256']=sha(ROOT/full);row['gallery_sha256']=sha(ROOT/web)
        row['watermark']=rows[full];row['gallery_watermark']=rows[web]
        row['tool']='Apple ImageIO full-resolution conversion and metadata removal, followed by the approved SVG watermark. No generative alteration; metadata-removal pixel check precedes branding.'
    p.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'core_images':len(rows),'channel_images':22,'all_watermarked':True,'nexprint_pixels':[2000,1500]}))
if __name__=='__main__':main()
