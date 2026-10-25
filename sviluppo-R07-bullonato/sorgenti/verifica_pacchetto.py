"""Controlli finali R07 e provino, senza modificare file di stampa."""
from pathlib import Path
import json,hashlib,re,zipfile,xml.etree.ElementTree as ET
import numpy as np
import trimesh
from geometria_utils import compare_mesh
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks={};inputs={};ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
 for folder in [ROOT,ROOT/'provino-giunto']:
  label='R07' if folder==ROOT else 'provino';m=json.loads((folder/'sorgenti/manifest.json').read_text())
  for filename in ['verifiche/geometria.json','verifiche/slicing/report.json']:
   d=json.loads((folder/filename).read_text());checks[label+':'+filename+':stato']=not d.get('fallimenti',[]) and all(d.get('controlli',{}).values())
   for key in ['hash_input','input_sha256','file']:
    for rel,h in d.get(key,{}).items():
     if isinstance(h,str) and re.fullmatch('[0-9a-f]{64}',h):checks[label+':hash:'+rel]=sha(folder/rel)==h
  geom=folder/m['piatto_geometrico']['file']
  with zipfile.ZipFile(geom) as z:
   checks[label+':3mf_CRC']=z.testzip() is None
   model=ET.fromstring(z.read('3D/3dmodel.model'));checks[label+':3mf_mm']=model.get('unit')=='millimeter'
   objects=model.findall('m:resources/m:object',ns);items=model.findall('m:build/m:item',ns)
   checks[label+':3mf_due_pezzi']=len(objects)==len(items)==len(m['pezzi'])==2
   for obj,item,part in zip(objects,items,m['pezzi']):
    vs=np.array([[float(v.get(k)) for k in 'xyz'] for v in obj.findall('m:mesh/m:vertices/m:vertex',ns)])
    fs=np.array([[int(f.get(k)) for k in ['v1','v2','v3']] for f in obj.findall('m:mesh/m:triangles/m:triangle',ns)])
    mesh=trimesh.Trimesh(vs,fs,process=True);ref=trimesh.load_mesh(folder/part['stl_stampa'],process=True)
    checks[label+':3mf_mesh:'+part['id']]=compare_mesh(ref,mesh)['triangoli_coincidenti']
    tr=np.array([float(v) for v in item.get('transform').split()]);checks[label+':3mf_trasformazione:'+part['id']]=len(tr)==12 and np.allclose(tr[:9],[1,0,0,0,1,0,0,0,1])
    mesh.apply_translation(tr[9:]);checks[label+':3mf_piano_volume:'+part['id']]=abs(mesh.bounds[0,2])<1e-6 and np.all(mesh.bounds[0,:2]>0) and np.all(mesh.bounds[1,:2]<246)
  report=json.loads((folder/'verifiche/slicing/report.json').read_text());project=next(folder/x for x in report['file'] if x.endswith('.3mf'));gcode=next(folder/x for x in report['file'] if x.endswith('.gcode'))
  with zipfile.ZipFile(project) as z:
   checks[label+':slicer_CRC']=z.testzip() is None
   settings=json.loads(z.read('Metadata/project_settings.config'));g=[x for x in z.namelist() if x.endswith('.gcode')]
   checks[label+':gcode_incorporato_identico']=len(g)==1 and z.read(g[0])==gcode.read_bytes()
   checks[label+':macchina']='Carbon 2' in settings['printer_settings_id'] and settings['nozzle_diameter']==['0.4'] and settings['curr_bed_type']=='Textured PEI Plate'
   checks[label+':PLA']=settings['filament_type']==['PLA'] and settings['nozzle_temperature']==['220'] and settings['textured_plate_temp']==['60']
   checks[label+':brim_disisattivato']=settings['brim_width']=='0' and settings['brim_type']=='no_brim'
  analysis=json.loads((folder/'verifiche/slicing/analisi_tutti_strati.json').read_text())
  checks[label+':tutti_strati_non_vuoti']=analysis['all_layers_nonempty'] and analysis['layer_count_matches_header']
  checks[label+':ingombri_con_supporti']=not analysis['out_of_bed_layers'] and not analysis['profile_exclusion_zone_violations']
  checks[label+':nessun_percorso_brim']=all('Brim' not in l['roles'] for l in analysis['layers'])
  checks[label+':supporti_presenti']=any('Support' in l['roles'] for l in analysis['layers'])
  checks[label+':nessuna_isola_candidata']=analysis['screening_isole']['candidate_count']==0
  checks[label+':avviso_PLA_conservato']=len(report['warnings_progetto'])==1 and report['warnings_progetto'][0]['msg']=='bed_temperature_too_high_than_filament'
  checks[label+':revisione_visiva']=report.get('revisione_visiva_tutti_strati_completata') is True
  for f in [geom,project,gcode]:inputs[str(f.relative_to(ROOT))]=sha(f)
 for readme in ROOT.rglob('README.md'):
  for rel in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)',readme.read_text()):
   if not rel.startswith(('http:','https:')):checks['link:'+str(readme.relative_to(ROOT))+':'+rel]=(readme.parent/rel).exists()
 for f in ROOT.rglob('*.json'):json.loads(f.read_text())
 checks={k:bool(v) for k,v in checks.items()};result={'controlli':checks,'fallimenti':[k for k,v in checks.items() if not v],'hash_file_stampa':inputs,'limite':'Verifiche digitali del prototipo PLA e del provino; R07 e provino non stampati o provati fisicamente.'}
 (ROOT/'verifiche/pacchetto.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(len(checks),'controlli, fallimenti:',result['fallimenti']);assert not result['fallimenti']
if __name__=='__main__':main()
