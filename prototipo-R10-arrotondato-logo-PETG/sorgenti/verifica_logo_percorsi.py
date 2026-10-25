"""Controllo dei percorsi estrusi del logo sui due G-code finali, con offset macchina."""
from pathlib import Path
import json,hashlib
import numpy as np
from slicer_utils import parse_gcode
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 machine=json.loads((R/'slicer/machine.json').read_text());offset=np.array([float(x) for x in machine['extruder_offset'][0].split('x')])
 result={}
 for tag,name in [('A_PROVINO_PONTE','provino_supporti'),('B_BASE_ARROTONDATA','base_appoggi')]:
  m=json.loads((R/f'sorgenti/manifest_{tag}.json').read_text());part=next(p for p in m['pezzi'] if p['id']==name);place=next(p for p in m['piatto_geometrico']['items'] if p['id']==name)
  # Coordinate originali prima della traslazione80mm che separa il solo provino nell'assieme.
  original_to_assembly=np.array([0,80,0]) if name=='provino_supporti' else np.zeros(3)
  move=original_to_assembly+np.array(part['matrice_stampa_da_assieme'])[:3,3]+np.array(place['traslazione_da_stampa_mm']);move[:2]-=offset
  code=next((R/'stampa/PETG_PRO_ECC2'/tag).glob('*.gcode'));layers,analysis=parse_gcode(code)
  plane=49+move[0];glyphs=[]
  for glyph,a,b in [('S',-5,-5+247*16/513),('9',-5+269*16/513,11)]:
   points=[];present=[]
   for layer in layers:
    if not 11.7<layer['z_mm']<19.7:continue
    found=False
    for x1,y1,x2,y2,role in layer['segments']:
     if role.startswith('Support'):continue
     cx=(x1+x2)/2;cy=(y1+y2)/2
     if plane+.05<cx<plane+2.01 and a+move[1]-.01<cy<b+move[1]+.01:
      points.extend([[x1,y1],[x2,y2]]);found=True
    if found:present.append(layer['number'])
   assert len(present)>20,(tag,glyph,len(present))
   bound=np.array([np.min(points,axis=0),np.max(points,axis=0)])
   assert 1.5<bound[1,0]-plane<2.05
   glyphs.append({'lettera':glyph,'strati_con_percorsi':present,'segmenti_campionati':len(points)//2,'estensione_X_oltre_piano_mm':float(bound[1,0]-plane)})
  result[tag]={'gcode':str(code.relative_to(R)),'sha256':sha(code),'offset_estrusore_mm':offset.tolist(),'lettere':glyphs,'esito':'S_E_9_PRESENTI_NEI_PERCORSI_FINALI','limite':'Non prova leggibilita, finitura o estrusione reale2mm: controlla presenza dei percorsi entro la geometria nominale.'}
 (R/'verifiche/logo_percorsi.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:{g['lettera']:len(g['strati_con_percorsi']) for g in v['lettere']} for k,v in result.items()}))
if __name__=='__main__':main()
