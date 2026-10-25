"""Controlla il progetto slicer PETG finale e la corrispondenza agli STL esportati."""
from pathlib import Path
import hashlib,json,zipfile,re,subprocess,xml.etree.ElementTree as ET
import numpy as np,trimesh
from slicer_utils import parse_gcode
from geometria_utils import compare_mesh,transform_3mf,read_3mf
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    checks={};geo=json.loads((R/'verifiche/geometria.json').read_text())
    checks['geometria_superata']=not geo['fallimenti'] and all(geo['controlli'].values()) and len(geo['controlli'])>=140
    for rel,h in geo['hash_input'].items():checks['hash_geometria:'+rel]=sha(R/rel)==h
    report=json.loads((R/'verifiche/slicing/report.json').read_text())
    for group in ['input_sha256','file']:
        for rel,h in report[group].items():checks['hash:'+rel]=sha(R/rel)==h
    project=next(R/k for k in report['file'] if k.endswith('.3mf'))
    code=next(R/k for k in report['file'] if k.endswith('.gcode'))
    native_results=[]
    with zipfile.ZipFile(project) as z:
        checks['CRC_native']=z.testzip() is None;s=json.loads(z.read('Metadata/project_settings.config'))
        g=[n for n in z.namelist() if n.endswith('.gcode')]
        checks['Gcode_identico_esterno']=len(g)==1 and z.read(g[0])==code.read_bytes()
        checks['macchina_ECC2']='Carbon 2' in s['printer_settings_id']
        checks['ugello04']=s['nozzle_diameter']==['0.4']
        checks['PEI_testurizzato']=s['curr_bed_type']=='Textured PEI Plate'
        checks['PETG_Pro']=s['filament_type']==['PETG'] and s['filament_settings_id']==['ELEGOO PETG PRO - BOREO R13']
        checks['temperature']=s['nozzle_temperature']==['240'] and s['textured_plate_temp']==['65']
        checks['densita_ufficiale']=s['filament_density']==['1.27']
        checks['portata5']=s['filament_max_volumetric_speed']==['5']
        checks['strati02']=s['layer_height']=='0.2'
        checks['pareti5_riempimento30']=s['wall_loops']=='5' and s['sparse_infill_density']=='30%'
        checks['supporti_attivi']=s['enable_support']=='1' and s['support_on_build_plate_only']=='1'
        checks['giochi_supporti']=s['support_top_z_distance']=='0.4' and s['support_object_xy_distance']=='0.55'
        checks['senza_brim_raft_torre']=s['brim_type']=='no_brim' and s['brim_width']=='0' and s['raft_layers']=='0' and s['enable_prime_tower']=='0'
        # Il progetto nativo ricentra le mesh e le sposta con trasformazioni esplicite.
        ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
        root=ET.fromstring(z.read('3D/3dmodel.model'))
        checks['native_unita_mm']=root.get('unit')=='millimeter'
        builds=root.findall('m:build/m:item',ns);objects={o.get('id'):o for o in root.findall('m:resources/m:object',ns)}
        checks['native_due_oggetti_stampabili']=len(builds)==2 and all(i.get('printable')=='1' for i in builds)
        _,expected=read_3mf(R/'stampa/R13_COMPLETO_SOLO_GEOMETRIA.3mf')
        config=ET.fromstring(z.read('Metadata/model_settings.config'))
        checks['native_due_oggetti_config']=len(config.findall('object'))==2
        checks['native_stesso_filamento']=all(any(n.get('key')=='extruder' and n.get('value')=='1' for n in ob.findall('metadata')) for ob in config.findall('object'))
        stats=config.findall('.//mesh_stat')
        checks['nessuna_riparazione_slicer']=len(stats)==2 and all(all(int(v)==0 for v in n.attrib.values()) for n in stats)
        for index,item in enumerate(builds):
            ob=objects[item.get('objectid')];components=ob.findall('m:components/m:component',ns)
            assert len(components)==1
            comp=components[0];path=comp.get('{http://schemas.microsoft.com/3dmanufacturing/production/2015/06}path').lstrip('/')
            child=ET.fromstring(z.read(path));checks[f'native_parte{index}:unita_mm']=child.get('unit')=='millimeter'
            obj=next(x for x in child.findall('m:resources/m:object',ns) if x.get('id')==comp.get('objectid'))
            v=np.array([[float(n.get(k)) for k in 'xyz'] for n in obj.findall('m:mesh/m:vertices/m:vertex',ns)])
            f=np.array([[int(n.get(k)) for k in ['v1','v2','v3']] for n in obj.findall('m:mesh/m:triangles/m:triangle',ns)])
            m=trimesh.Trimesh(v,f,process=True)
            transform=transform_3mf(item.get('transform'))@transform_3mf(comp.get('transform'))
            checks[f'native_parte{index}:scala1']=np.allclose(transform[:3,:3],np.eye(3))
            m.apply_transform(transform);comparison=compare_mesh(expected[index]['mondo'],m)
            checks[f'native_parte{index}:mesh_pose_identiche']=comparison['triangoli_coincidenti']
            checks[f'native_parte{index}:sul_piano']=abs(m.bounds[0,2])<1e-5
            native_results.append({'id':expected[index]['nome'],'confronto_mesh':comparison,'bounds_mm':m.bounds.tolist()})
    layers,a=parse_gcode(code)
    checks['230_strati']=len(layers)==230 and a['all_layers_nonempty'] and a['layer_count_matches_header']
    checks['ingombri_reali']=not a['out_of_bed_layers'] and not a['profile_exclusion_zone_violations']
    roles={role for l in a['layers'] for role in l['roles']}
    checks['supporti_presenti']=any(role.startswith('Support') for role in roles)
    checks['nessun_brim']='Brim' not in roles
    saved=json.loads((R/'verifiche/slicing/analisi_tutti_strati.json').read_text())
    checks['nessuna_isola_candidata']=saved['screening_isole']['candidate_count']==0
    checks['revisione_visiva']=report.get('revisione_visiva_tutti_strati_completata') is True
    checks['nessun_avviso']=not report['warnings_progetto'] and not report['warnings_log']
    for rel in report['anteprime']['tutti_strati']+report['anteprime']['dettagli']:checks['anteprima:'+rel]=(R/rel).exists()
    logo=json.loads((R/'verifiche/logo_percorsi.json').read_text())['COMPLETO']
    checks['logo_percorsi_aggiornati']=sha(R/logo['gcode'])==logo['sha256']
    checks['logo_due_lettere_presenti']=len(logo['lettere'])==2 and all(len(g['strati_con_percorsi'])>20 for g in logo['lettere'])
    native=subprocess.run(['/Applications/ElegooSlicer.app/Contents/MacOS/ElegooSlicer','--info',str(project)],text=True,capture_output=True)
    (R/'verifiche/slicing/riapertura_3mf.log').write_text(native.stdout+native.stderr)
    checks['riapertura_native_due_pezzi']=native.returncode==0 and len(re.findall(r'number_of_parts\s*=\s*1',native.stdout))==2
    for p in R.rglob('*.json'):json.loads(p.read_text())
    for rel in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)',(R/'README.md').read_text()):
        if not rel.startswith(('https:','http:')):
            # Il report stesso viene scritto qui sotto, anche alla prima esecuzione.
            checks['link:'+rel]=(R/rel).exists() or rel=='verifiche/pacchetto.json'
    out={'revisione':'R13','controlli':{k:bool(v) for k,v in checks.items()},'fallimenti':[k for k,v in checks.items() if not v],
      'native_geometria_pose':native_results,'hash_stampa':{str(p.relative_to(R)):sha(p) for p in [project,code]},
      'limite':'Pronto per stampa di prototipo PETG completo. Nessuna prova fisica di montaggio, carico, calore o immersione.'}
    (R/'verifiche/pacchetto.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(len(checks),'controlli, fallimenti:',out['fallimenti']);assert not out['fallimenti']
if __name__=='__main__':main()
