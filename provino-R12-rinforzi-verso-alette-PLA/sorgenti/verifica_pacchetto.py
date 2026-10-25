"""Verifica del progetto slicer finale R12 e coerenza degli input esportati."""
from pathlib import Path
import json,hashlib,zipfile,re,subprocess
from slicer_utils import parse_gcode
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks={};geo=json.loads((R/'verifiche/geometria.json').read_text());checks['geometria_superata']=not geo['fallimenti'] and all(geo['controlli'].values()) and len(geo['controlli'])>=59
 for rel,h in geo['hash_input'].items():checks['hash_geometria:'+rel]=sha(R/rel)==h
 report=json.loads((R/'verifiche/slicing/report.json').read_text())
 for group in ['input_sha256','file']:
  for rel,h in report[group].items():checks['hash:'+rel]=sha(R/rel)==h
 project=next(R/k for k in report['file'] if k.endswith('.3mf'));code=next(R/k for k in report['file'] if k.endswith('.gcode'))
 with zipfile.ZipFile(project) as z:
  checks['CRC_native']=z.testzip() is None;s=json.loads(z.read('Metadata/project_settings.config'));g=[n for n in z.namelist() if n.endswith('.gcode')]
  checks['Gcode_identico_esterno']=len(g)==1 and z.read(g[0])==code.read_bytes()
  checks['macchina_ECC2']='Carbon 2' in s['printer_settings_id'];checks['ugello04']=s['nozzle_diameter']==['0.4'];checks['PEI_testurizzato']=s['curr_bed_type']=='Textured PEI Plate'
  checks['PLA_Basic']=s['filament_type']==['PLA'] and 'PLA' in s['filament_settings_id'][0]
  checks['temperature']=s['nozzle_temperature']==['220'] and s['textured_plate_temp']==['60'];checks['strati02']=s['layer_height']=='0.2'
  checks['pareti5_riempimento30']=s['wall_loops']=='5' and s['sparse_infill_density']=='30%';checks['supporti_attivi']=s['enable_support']=='1' and s['support_on_build_plate_only']=='1'
  checks['giochi_supporti']=s['support_top_z_distance']=='0.4' and s['support_object_xy_distance']=='0.55'
  checks['senza_brim_raft_torre']=s['brim_type']=='no_brim' and s['brim_width']=='0' and s['raft_layers']=='0' and s['enable_prime_tower']=='0'
 layers,a=parse_gcode(code);checks['144_strati']=len(layers)==144 and a['all_layers_nonempty'] and a['layer_count_matches_header'];checks['ingombri_reali']=not a['out_of_bed_layers'] and not a['profile_exclusion_zone_violations']
 roles={role for l in a['layers'] for role in l['roles']};checks['supporti_presenti']=any(role.startswith('Support') for role in roles);checks['nessun_brim']='Brim' not in roles
 saved=json.loads((R/'verifiche/slicing/analisi_tutti_strati.json').read_text());checks['nessuna_isola_candidata']=saved['screening_isole']['candidate_count']==0
 checks['revisione_visiva']=report.get('revisione_visiva_tutti_strati_completata') is True
 checks['solo_avviso_PLA']=len(report['warnings_progetto'])==1 and report['warnings_progetto'][0]['msg']=='bed_temperature_too_high_than_filament'
 native=subprocess.run(['/Applications/ElegooSlicer.app/Contents/MacOS/ElegooSlicer','--info',str(project)],text=True,capture_output=True)
 (R/'verifiche/slicing/riapertura_3mf.log').write_text(native.stdout+native.stderr)
 checks['riapertura_native_un_pezzo']=native.returncode==0 and len(re.findall(r'number_of_parts\s*=\s*1',native.stdout))==1
 for p in R.rglob('*.json'):json.loads(p.read_text())
 for rel in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)',(R/'README.md').read_text()):
  if not rel.startswith(('https:','http:')):checks['link:'+rel]=(R/rel).exists()
 out={'controlli':{k:bool(v) for k,v in checks.items()},'fallimenti':[k for k,v in checks.items() if not v],'hash_stampa':{str(p.relative_to(R)):sha(p) for p in [project,code]},'limite':'Provino PLA, nessun montaggio R12, carico o temperatura fisicamente verificati.'}
 (R/'verifiche/pacchetto.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');print(len(checks),'controlli, fallimenti:',out['fallimenti']);assert not out['fallimenti']
if __name__=='__main__':main()
