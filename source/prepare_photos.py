"""Preserve supplied HEICs and export public, orientation-correct JPEGs.

Requires macOS ImageIO (PyObjC Quartz/Foundation), Pillow and ImageMagick.
No generative changes are made by this conversion/metadata utility.

SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
Required Notice: S9 Engineering (https://github.com/S9-Engineering)
"""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,tempfile
from PIL import Image
import Quartz as Q
from Foundation import NSURL

ROOT=Path(__file__).resolve().parents[1]
NAMES={1670:'mount-side',1671:'butterfly-backing',1672:'mount-underside',
       1673:'inner-bridge',1674:'lamp-side',1675:'helmet-mounted'}
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def pixels(path):
    with Image.open(path) as im:return hashlib.sha256(im.convert('RGB').tobytes()).hexdigest()
def strip_private_segments(data):
    assert data[:2]==b'\xff\xd8'
    out=bytearray(data[:2]);i=2
    while i<len(data):
        assert data[i]==255
        start=i
        while data[i]==255:i+=1
        marker=data[i];i+=1
        if marker==0xda:
            out.extend(data[start:]);break
        if marker in [0xd8,0xd9] or 0xd0<=marker<=0xd7:
            out.extend(data[start:i]);continue
        length=int.from_bytes(data[i:i+2],'big');end=i+length
        # APP1 contains EXIF/XMP; COM may contain private text. ICC APP2 is retained.
        if marker not in [0xe1,0xfe]:out.extend(data[start:end])
        i=end
    return bytes(out)
def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path.home()/'Downloads');args=p.parse_args()
    photo=ROOT/'previews/photos';originals=photo/'originals';edited=photo/'edited';gallery=photo/'gallery'
    for d in [originals,edited,gallery]:d.mkdir(parents=True,exist_ok=True)
    ignore=ROOT/'.gitignore';rule='/previews/photos/originals/*.HEIC'
    text=ignore.read_text()
    if rule not in text:ignore.write_text(text+'\n# Untouched captures contain private GPS metadata. Public copies are versioned.\n'+rule+'\n')
    assets=[]
    with tempfile.TemporaryDirectory(prefix='boreo-photo-conversion-') as td:
        for n,name in NAMES.items():
            src=args.input/f'IMG_{n}.HEIC';raw=originals/src.name
            if raw.exists():assert sha(raw)==sha(src)
            else:shutil.copy2(src,raw)
            source=Q.CGImageSourceCreateWithURL(NSURL.fileURLWithPath_(str(raw)),None)
            props=Q.CGImageSourceCopyPropertiesAtIndex(source,0,None)
            edge=max(props[Q.kCGImagePropertyPixelWidth],props[Q.kCGImagePropertyPixelHeight])
            image=Q.CGImageSourceCreateThumbnailAtIndex(source,0,{
                Q.kCGImageSourceCreateThumbnailFromImageAlways:True,
                Q.kCGImageSourceCreateThumbnailWithTransform:True,
                Q.kCGImageSourceThumbnailMaxPixelSize:edge,
                Q.kCGImageSourceShouldCacheImmediately:True})
            temp=Path(td)/(name+'.jpg')
            dest=Q.CGImageDestinationCreateWithURL(NSURL.fileURLWithPath_(str(temp)),'public.jpeg',1,None)
            Q.CGImageDestinationAddImage(dest,image,{Q.kCGImageDestinationLossyCompressionQuality:.94})
            assert Q.CGImageDestinationFinalize(dest)
            target=edited/(name+'-real.jpg');target.write_bytes(strip_private_segments(temp.read_bytes()))
            assert pixels(temp)==pixels(target)
            public=Q.CGImageSourceCopyPropertiesAtIndex(Q.CGImageSourceCreateWithURL(NSURL.fileURLWithPath_(str(target)),None),0,None)
            assert not public.get(Q.kCGImagePropertyGPSDictionary)
            assert not public.get(Q.kCGImagePropertyExifDictionary)
            with Image.open(target) as im:size=list(im.size)
            expected=[props[Q.kCGImagePropertyPixelWidth],props[Q.kCGImagePropertyPixelHeight]]
            if props.get(Q.kCGImagePropertyOrientation) in [5,6,7,8]:expected.reverse()
            assert size==expected
            web=gallery/(name+'.jpg')
            subprocess.run(['magick',str(target),'-resize','2000x2000>','-strip','-quality','92',str(web)],check=True)
            assets.append({'source_id':src.stem,'original':str(raw.relative_to(ROOT)),'original_sha256':sha(raw),
                'original_gps_metadata_present':bool(props.get(Q.kCGImagePropertyGPSDictionary)),
                'original_git_ignored':True,'public_full_resolution':str(target.relative_to(ROOT)),
                'public_sha256':sha(target),'public_size':size,'decoded_pixels_unchanged_by_metadata_removal':True,
                'public_gps_metadata_present':False,'gallery':str(web.relative_to(ROOT)),'gallery_sha256':sha(web),
                'generative_ai_used':False,
                'tool':'Apple ImageIO: orientation baked into full-resolution JPEG, quality 94; APP1/COM removed losslessly. ImageMagick resizes the web gallery only.'})
    report={'prepared_on':'2026-10-27','project':'BOREO Superkikko2 Torch Mount',
        'evidence_scope':'User photographs show a physical printed mount installed with the original lamp and metal bracket. The user confirms the latest model was printed in PETG. Actual print settings were not supplied; no dimensional, load, heat or immersion test is inferred.',
        'private_original_policy':'GPS-bearing untouched HEICs stay local and ignored; full-resolution public references contain no private location metadata.',
        'assets':assets}
    previous=json.loads((photo/'edits.json').read_text()) if (photo/'edits.json').exists() else {}
    for key in ['cover','user_confirmation']:
        if key in previous:report[key]=previous[key]
    (photo/'edits.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'photos':len(assets),'private_originals_unchanged':True,'public_gps':False,'full_resolution_verified':True}))
if __name__=='__main__':main()
