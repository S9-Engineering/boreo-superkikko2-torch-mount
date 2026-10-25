"""Slicing reale R05: due dime PLA Basic, ECC2 0.4 / PEI testurizzato.

Il G-code e' prodotto esclusivamente da ElegooSlicer; nessun invio alla macchina.
La provenienza dei profili e le ipotesi di forma sono conservate separatamente.
"""
from pathlib import Path
import argparse, hashlib, json, math, plistlib, shutil, subprocess, tempfile, zipfile
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from slicer_utils import parse_gcode, screen_new_wall_islands, estimate_totals

ROOT=Path(__file__).resolve().parents[1]
SLICER=Path('/Applications/ElegooSlicer.app/Contents/MacOS/ElegooSlicer')
NAME='BOREO_R05_DIMA_PLA_BASIC_ECC2_04'
COLORS={'Outer wall':'#1c4568','Inner wall':'#5183a5','Overhang wall':'#8b448b',
        'Sparse infill':'#218d88','Internal solid infill':'#68a293','Top surface':'#6c4786',
        'Bottom surface':'#6c4786','Bridge':'#d6482e','Internal Bridge':'#c35e30',
        'Support':'#c49423','Support interface':'#d46c28','Brim':'#b0bbc3'}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def render(layers,analysis,out):
    """Tutti i percorsi, con inquadratura del lavoro invece del piano intero."""
    out.mkdir(parents=True,exist_ok=True)
    bounds=np.array(analysis['extrusion_bounds_xy_mm']);lo=bounds[0]-5;hi=bounds[1]+5
    span=np.maximum(hi-lo,1)
    fontfile=Path('/System/Library/Fonts/Supplemental/Arial.ttf')
    def font(size):return ImageFont.truetype(str(fontfile),size) if fontfile.exists() else ImageFont.load_default()
    def tile(draw,layer,xy,size):
        x,y=xy;scale=min((size-16)/span[0],(size-38)/span[1])
        cx=x+(size-span[0]*scale)/2;cy=y+30+(size-38-span[1]*scale)/2
        draw.rectangle((x,y,x+size-1,y+size-1),fill='#fafbfd',outline='#d6dbe0')
        draw.text((x+5,y+4),f"Strato {layer['number']} · Z {layer['z_mm']:.2f}",fill='#162c40',font=font(12 if size<300 else 18))
        for x1,y1,x2,y2,role in layer['segments']:
            draw.line((cx+(x1-lo[0])*scale,cy+(hi[1]-y1)*scale,
                       cx+(x2-lo[0])*scale,cy+(hi[1]-y2)*scale),
                      fill=COLORS.get(role,'#778892'),width=1 if size<300 else 2)
    pages=[];cols,rows,size,gap,header=8,8,170,4,46
    for start in range(0,len(layers),cols*rows):
        subset=layers[start:start+cols*rows];nrows=math.ceil(len(subset)/cols)
        im=Image.new('RGB',(cols*(size+gap)+gap,nrows*(size+gap)+header),'white');d=ImageDraw.Draw(im)
        d.text((8,10),f'BOREO R05 · percorsi reali ElegooSlicer · strati {start+1}–{start+len(subset)}',fill='#162c40',font=font(18))
        for i,layer in enumerate(subset):tile(d,layer,(gap+(i%cols)*(size+gap),header+(i//cols)*(size+gap)),size)
        target=out/f'strati_{start+1:04d}_{start+len(subset):04d}.png';im.save(target);pages.append(str(target.relative_to(ROOT)))
    indices=sorted(set([0,1,9,29,len(layers)//2,len(layers)-1]))
    indices=[x for x in indices if x<len(layers)]
    detail=[]
    for start in range(0,len(indices),4):
        chosen=indices[start:start+4];im=Image.new('RGB',(1200,650 if len(chosen)<=2 else 1250),'white');d=ImageDraw.Draw(im)
        d.text((12,9),'BOREO R05 · primo strato, supporti e dettagli · nessuna stampa eseguita',fill='#162c40',font=font(19))
        for i,index in enumerate(chosen):tile(d,layers[index],((i%2)*600,46+(i//2)*600),600)
        target=out/f'dettagli_{start//4+1}.png';im.save(target);detail.append(str(target.relative_to(ROOT)))
    return {'tutti_strati':pages,'dettagli':detail,'legenda_ruoli':COLORS,'tutti_strati_renderizzati':True}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--slicer',type=Path,default=SLICER);args=parser.parse_args()
    manifest=json.loads((ROOT/'sorgenti/manifest.json').read_text())
    model=ROOT/manifest['piatto_geometrico']['file']
    assert model.exists() and len(manifest['pezzi'])==2
    profiles=[ROOT/'slicer'/n for n in ('machine.json','process.json','filament.json')]
    assert all(p.exists() for p in profiles)
    watched=[model,ROOT/'sorgenti/manifest.json',*profiles,*[ROOT/p['stl_stampa'] for p in manifest['pezzi']]]
    inputs={str(p.relative_to(ROOT)):sha(p) for p in watched}
    qa=ROOT/'verifiche/slicing';qa.mkdir(parents=True,exist_ok=True)
    deliver=ROOT/'stampa/PLA_BASIC_ECC2';deliver.mkdir(parents=True,exist_ok=True)
    slicer=args.slicer.resolve();version=plistlib.loads((slicer.parents[1]/'Info.plist').read_bytes())['CFBundleShortVersionString']
    with tempfile.TemporaryDirectory(prefix='boreo-r05-pla-') as td:
        td=Path(td);out=td/'out';out.mkdir()
        command=[str(slicer),'--debug','2','--datadir',str(td/'data'),
                 '--load-settings',str(profiles[0])+';'+str(profiles[1]),'--load-filaments',str(profiles[2]),
                 '--arrange','0','--orient','0','--slice','0','--export-3mf',NAME+'.3mf','--outputdir',str(out),str(model)]
        result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (qa/'ElegooSlicer.log').write_text(result.stdout)
        errors=[line for line in result.stdout.splitlines() if __import__('re').search(r'\berror\b|\bfatal\b',line,__import__('re').I)]
        assert result.returncode==0 and not errors,(result.returncode,errors[:5])
        gcodes=list(out.glob('*.gcode'));assert len(gcodes)==1
        layers,analysis=parse_gcode(gcodes[0])
        assert analysis['all_layers_nonempty'] and analysis['layer_count_matches_header']
        assert not analysis['out_of_bed_layers'] and not analysis['profile_exclusion_zone_violations']
        analysis['screening_isole']=screen_new_wall_islands(layers)
        project=out/(NAME+'.3mf')
        with zipfile.ZipFile(project) as z:
            assert z.testzip() is None
            warnings=[dict(n.attrib) for n in ET.fromstring(z.read('Metadata/slice_info.config')).iter() if n.tag=='warning']
            settings=json.loads(z.read('Metadata/project_settings.config'))
            assert settings['nozzle_diameter']==['0.4']
            assert settings['curr_bed_type']=='Textured PEI Plate'
            assert settings['filament_type']==['PLA']
            assert settings['layer_height']=='0.2'
            assert settings['enable_prime_tower']=='0'
            assert 'Carbon 2' in settings['printer_settings_id']
            embedded=[n for n in z.namelist() if n.endswith('.gcode')];assert len(embedded)==1
            assert hashlib.sha256(z.read(embedded[0])).hexdigest()==sha(gcodes[0])
            embedded_code=z.read(embedded[0]).decode()
            assert 'filament_type = PLA' in embedded_code
            selected={k:settings.get(k) for k in ('printer_settings_id','curr_bed_type','nozzle_diameter','filament_settings_id','filament_type','nozzle_temperature','nozzle_temperature_initial_layer','textured_plate_temp','textured_plate_temp_initial_layer','layer_height','wall_loops','sparse_infill_density','brim_width','brim_object_gap','enable_support','support_on_build_plate_only','support_type','support_top_z_distance','wall_generator','enable_prime_tower','filament_max_volumetric_speed')}
        previews=render(layers,analysis,ROOT/'anteprime/slicing')
        save(qa/'analisi_tutti_strati.json',analysis)
        shutil.copy2(project,deliver/(NAME+'.3mf'))
        shutil.copy2(gcodes[0],deliver/(NAME+'.gcode'))
        for p in watched:assert sha(p)==inputs[str(p.relative_to(ROOT))]
        report={'revisione':'R05_DIMA_PLA_BASIC','slicer_app_version':version,'slicer_help_version':'ElegooSlicer-2.4.2',
                'slicer_binary_sha256':sha(slicer),'command':command,'input_sha256':inputs,
                'stato':'SLICING_ESEGUITO_IN_ATTESA_REVISIONE_VISIVA','warnings_progetto':warnings,
                'warnings_log':[line for line in result.stdout.splitlines() if 'warning' in line.lower()],
                'impostazioni_salvate':selected,'strati':len(layers),'stime_slicer':analysis['slicer_estimates'],
                'anteprime':previews,'gcode_generato_dallo_slicer':True,'gcode_modificato':False,
                'gcode_incorporato_identico':True,'file':{str(p.relative_to(ROOT)):sha(p) for p in deliver.iterdir() if p.is_file()},
                'avvio_stampa_o_invio_macchina':False,'stampa_fisica_eseguita':False,
                'limite':'Solo dima di forma: curvatura e terminali assunti; montaggio, comfort, resistenza, calore e immersione non convalidati.'}
        save(qa/'report.json',report)
        print(json.dumps({'strati':len(layers),'stime':analysis['slicer_estimates'],'warning_progetto':warnings,'isole_da_esaminare':analysis['screening_isole']['candidate_count'],'file':report['file']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
