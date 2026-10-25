"""Verifica indipendente dei piatti geometrici e dei progetti slicer R10."""
from pathlib import Path
import json,hashlib,re,zipfile,subprocess,xml.etree.ElementTree as ET
import numpy as np
import trimesh
from geometria_utils import compare_mesh
from slicer_utils import parse_gcode
ROOT=Path(__file__).resolve().parents[1]
SLICER='/Applications/ElegooSlicer.app/Contents/MacOS/ElegooSlicer'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks={};inputs={};ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
 geo=json.loads((ROOT/'verifiche/geometria.json').read_text());checks['geometria_completa']=len(geo['controlli'])>=115 and not geo['fallimenti'] and all(geo['controlli'].values())
 for rel,h in geo['hash_input'].items():checks['hash_geometria:'+rel]=sha(ROOT/rel)==h
 for suffix,expected in [('',3),('_A_PROVINO_PONTE',2),('_B_BASE_ARROTONDATA',1)]:
  manifest=json.loads((ROOT/f'sorgenti/manifest{suffix}.json').read_text());target=ROOT/manifest['piatto_geometrico']['file']
  with zipfile.ZipFile(target) as z:
   checks['CRC'+suffix]=z.testzip() is None;model=ET.fromstring(z.read('3D/3dmodel.model'));checks['unita_mm'+suffix]=model.get('unit')=='millimeter'
   objects=model.findall('m:resources/m:object',ns);build=model.findall('m:build/m:item',ns);checks['quantita'+suffix]=len(objects)==len(build)==len(manifest['pezzi'])==expected
   bounds=[]
   for ob,item,part in zip(objects,build,manifest['pezzi']):
    vs=np.array([[float(v.get(k)) for k in 'xyz'] for v in ob.findall('m:mesh/m:vertices/m:vertex',ns)])
    fs=np.array([[int(f.get(k)) for k in ['v1','v2','v3']] for f in ob.findall('m:mesh/m:triangles/m:triangle',ns)])
    mesh=trimesh.Trimesh(vs,fs,process=True);ref=trimesh.load_mesh(ROOT/part['stl_stampa'],process=True)
    checks['mesh'+suffix+':'+part['id']]=compare_mesh(ref,mesh)['triangoli_coincidenti']
    tr=np.array([float(v) for v in item.get('transform').split()]);checks['matrice'+suffix+':'+part['id']]=len(tr)==12 and np.allclose(tr[:9],[1,0,0,0,1,0,0,0,1])
    mesh.apply_translation(tr[9:]);b=mesh.bounds;bounds.append(b);checks['piatto'+suffix+':'+part['id']]=abs(b[0,2])<1e-6 and np.all(b[0,:2]>4) and np.all(b[1,:2]<242)
   for i in range(len(bounds)):
    for j in range(i+1,len(bounds)):checks[f'separazione{suffix}:{i}:{j}']=bool(np.any(bounds[i][1,:2]+4<bounds[j][0,:2]) or np.any(bounds[j][1,:2]+4<bounds[i][0,:2]))
  inputs[str(target.relative_to(ROOT))]=sha(target)
 for tag,expected in [('A_PROVINO_PONTE',2),('B_BASE_ARROTONDATA',1)]:
  qa=ROOT/'verifiche/slicing'/tag;report=json.loads((qa/'report.json').read_text())
  for key in ['input_sha256','file']:
   for rel,h in report[key].items():checks[tag+':hash:'+rel]=sha(ROOT/rel)==h
  project=next(ROOT/k for k in report['file'] if k.endswith('.3mf'));code=next(ROOT/k for k in report['file'] if k.endswith('.gcode'))
  with zipfile.ZipFile(project) as z:
   checks[tag+':CRC_slicer']=z.testzip() is None;settings=json.loads(z.read('Metadata/project_settings.config'));g=[x for x in z.namelist() if x.endswith('.gcode')]
   checks[tag+':gcode_identico']=len(g)==1 and z.read(g[0])==code.read_bytes()
   checks[tag+':macchina']='Carbon 2' in settings['printer_settings_id'] and settings['nozzle_diameter']==['0.4'] and settings['curr_bed_type']=='Textured PEI Plate'
   checks[tag+':PETG']=settings['filament_type']==['PETG'] and settings['nozzle_temperature']==['240'] and settings['textured_plate_temp']==['65']
   checks[tag+':processo']=settings['layer_height']=='0.2' and settings['wall_loops']=='5' and settings['sparse_infill_density']=='30%'
   checks[tag+':brim_off']=settings['brim_width']=='0' and settings['brim_type']=='no_brim'
   checks[tag+':torre_raft_off']=settings['enable_prime_tower']=='0' and settings['raft_layers']=='0'
  checks[tag+':distanze_supporti']=settings['support_top_z_distance']=='0.4' and settings['support_object_xy_distance']=='0.55'
  layers,a=parse_gcode(code);roles={r for l in a['layers'] for r in l['roles']}
  checks[tag+':tutti_strati']=a['all_layers_nonempty'] and a['layer_count_matches_header']
  checks[tag+':ingombri_supporti']=not a['out_of_bed_layers'] and not a['profile_exclusion_zone_violations']
  checks[tag+':nessun_Brim']='Brim' not in roles
  checks[tag+':supporti_come_previsto']=any(r.startswith('Support') for r in roles)
  saved=json.loads((qa/'analisi_tutti_strati.json').read_text());checks[tag+':nessuna_isola_candidata']=saved['screening_isole']['candidate_count']==0
  checks[tag+':visiva']=report.get('revisione_visiva_tutti_strati_completata') is True
  checks[tag+':nessun_avviso']=not report['warnings_progetto']
  info=subprocess.run([SLICER,'--info',str(project)],capture_output=True,text=True);(qa/'riapertura_3mf.log').write_text(info.stdout+info.stderr)
  checks[tag+':riapertura_native']=info.returncode==0 and len(re.findall(r'number_of_parts\s*=\s*1',info.stdout))==expected
  for f in [project,code]:inputs[str(f.relative_to(ROOT))]=sha(f)
 for f in ROOT.rglob('*.json'):json.loads(f.read_text())
 for rel in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)',(ROOT/'README.md').read_text()):
  if not rel.startswith(('http:','https:')):checks['link:'+rel]=(ROOT/rel).exists()
 checks={k:bool(v) for k,v in checks.items()};result={'controlli':checks,'fallimenti':[k for k,v in checks.items() if not v],'hash_file_stampa':inputs,'limite':'Solo prove digitali dei provini PETG: nessuna verifica fisica R10, carico, temperatura o uso del casco.'}
 (ROOT/'verifiche/pacchetto.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(len(checks),'controlli, fallimenti:',result['fallimenti']);assert not result['fallimenti']
if __name__=='__main__':main()
