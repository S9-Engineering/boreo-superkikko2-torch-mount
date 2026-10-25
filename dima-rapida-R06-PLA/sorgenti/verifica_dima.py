"""Verifica dei file R06 riaperti; non importa il generatore CAD."""
from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as ET,importlib.metadata
import cadquery as cq
import trimesh,numpy as np
from geometria_utils import mesh_metrics,self_intersections,bounds_cad,transform_cad_rigid,compare_mesh,line_sections

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    manifest=json.loads((ROOT/'sorgenti/manifest.json').read_text());params=json.loads((ROOT/'sorgenti/parametri.json').read_text())
    files=[ROOT/'sorgenti/manifest.json',ROOT/'sorgenti/parametri.json',*[ROOT/p[k] for p in manifest['pezzi'] for k in ['stl_stampa','step_stampa','stl_assieme','step_assieme']],ROOT/manifest['piatto_geometrico']['file'],ROOT/manifest['assieme']['glb'],ROOT/manifest['assieme']['step']]
    hashes={str(p.relative_to(ROOT)):sha(p) for p in files};checks={};parts={};shapes={};meshes={}
    def check(key,condition):checks[key]=bool(condition)
    check('due_pezzi',len(manifest['pezzi'])==2)
    for p in manifest['pezzi']:
        key=p['id'];m=trimesh.load_mesh(ROOT/p['stl_stampa'],process=True);metrics=mesh_metrics(m);screen=self_intersections(m)
        for flag in ['mesh_chiusa','normali_coerenti','volume_positivo','vertici_finiti']:check(key+':'+flag,metrics[flag])
        for zero in ['spigoli_incidenza_diversa_da_2','facce_duplicate','facce_degeneri_area_inferiore_1e-10']:check(key+':'+zero,metrics[zero]==0)
        check(key+':un_corpo',metrics['corpi_connessi']==1);check(key+':manifold',metrics['manifold_importazione']['stato']=='Error.NoError')
        check(key+':nessuna_autointersezione_screening',screen['coppie_con_intersezione']==0)
        check(key+':sul_piano',abs(m.bounds[0,2])<1e-6)
        printing=cq.importers.importStep(str(ROOT/p['step_stampa'])).val();assembly=cq.importers.importStep(str(ROOT/p['step_assieme'])).val()
        check(key+':STEP_stampa_valido',printing.isValid() and len(printing.Solids())==1 and printing.Volume()>0)
        check(key+':STEP_assieme_valido',assembly.isValid() and len(assembly.Solids())==1)
        check(key+':STEP_STL_volume',abs(printing.Volume()-m.volume)/printing.Volume()<.01)
        # Export .06mm: il massimo di una curva puo cadere fra due vertici STL.
        bounds_delta=float(np.max(np.abs(bounds_cad(printing)-m.bounds)))
        check(key+':STEP_STL_limiti',bounds_delta<=.061)
        pose=transform_cad_rigid(assembly,p['matrice_stampa_da_assieme'])
        diff=pose.cut(printing).Volume()+printing.cut(pose).Volume();check(key+':pose_CAD_coerenti',diff<1e-5)
        am=trimesh.load_mesh(ROOT/p['stl_assieme'],process=True);am.apply_transform(p['matrice_stampa_da_assieme'])
        check(key+':pose_STL_coerenti',np.allclose(am.bounds,m.bounds,atol=1e-4,rtol=0) and abs(am.volume-m.volume)<.01)
        shapes[key]=assembly;meshes[key]=m;parts[key]={'mesh':metrics,'autointersezioni':screen,'differenza_pose_CAD_mm3':diff,'scarto_limiti_STEP_STL_mm':bounds_delta,'tolleranza_limiti_STEP_STL_mm':.061}
    overlap=shapes['base_cornice'].intersect(shapes['ponte_terminale']).Volume();check('assemblaggio_senza_interferenze',overlap<1e-6)
    probe={}
    for x in params['assi_terminali_x']:
        hs=line_sections(shapes['ponte_terminale'],[x,-12,18],[x,-12,28]);ws=line_sections(shapes['ponte_terminale'],[x-8,-12,23],[x+8,-12,23])
        check(f'terminale_{x}:altezza4',len(hs)==1 and abs(hs[0]['lunghezza_mm']-4)<1e-5)
        check(f'terminale_{x}:larghezza10',len(ws)==1 and abs(ws[0]['lunghezza_mm']-10)<1e-5)
        passage=line_sections(shapes['base_cornice'],[x,-50,23],[x,30,23]);check(f'base_{x}:passaggio_aperto',not passage)
        probe[str(x)]={'altezza':hs,'larghezza':ws,'base_lungo_passaggio':passage}
    skin=line_sections(shapes['ponte_terminale'],[0,-20,23],[0,-17,23]);check('ponte_spessore1_2',len(skin)==1 and abs(skin[0]['lunghezza_mm']-1.2)<1e-5)
    path=ROOT/manifest['piatto_geometrico']['file'];ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    with zipfile.ZipFile(path) as z:
        check('3MF_CRC',z.testzip() is None);model=ET.fromstring(z.read('3D/3dmodel.model'));check('3MF_mm',model.get('unit')=='millimeter')
        objects=model.findall('m:resources/m:object',ns);build=model.findall('m:build/m:item',ns);check('3MF_due_oggetti',len(objects)==len(build)==2)
        for o,item,p in zip(objects,build,manifest['pezzi']):
            vs=np.array([[float(v.get(k)) for k in 'xyz'] for v in o.findall('m:mesh/m:vertices/m:vertex',ns)])
            fs=np.array([[int(f.get(k)) for k in ['v1','v2','v3']] for f in o.findall('m:mesh/m:triangles/m:triangle',ns)])
            m=trimesh.Trimesh(vs,fs,process=True);comp=compare_mesh(meshes[p['id']],m);check('3MF_geometria_'+p['id'],comp['triangoli_coincidenti'])
            tr=np.array([float(v) for v in item.get('transform').split()]);check('3MF_matrice_'+p['id'],len(tr)==12 and np.allclose(tr[:9],[1,0,0,0,1,0,0,0,1]))
            m.apply_translation(tr[9:]);check('3MF_sul_piano_'+p['id'],abs(m.bounds[0,2])<1e-6)
            check('3MF_margine_brim_'+p['id'],np.all(m.bounds[0,:2]-4>0) and np.all(m.bounds[1,:2]+4<246))
    scene=trimesh.load(ROOT/manifest['assieme']['glb'],force='scene');check('GLB_due_componenti',len(scene.geometry)==2)
    for node in scene.graph.nodes_geometry:
        transform,geometry=scene.graph[node];m=scene.geometry[geometry].copy();m.apply_transform(transform);m.apply_scale(1000)
        ref=trimesh.load_mesh(ROOT/next(p['stl_assieme'] for p in manifest['pezzi'] if p['id']==node),process=True)
        check('GLB_scala_'+node,np.allclose(m.bounds,ref.bounds,atol=.001,rtol=0))
    whole=cq.importers.importStep(str(ROOT/manifest['assieme']['step'])).val();check('STEP_assieme_due_solidi',len(whole.Solids())==2 and whole.isValid())
    check('file_stabili',all(sha(ROOT/k)==v for k,v in hashes.items()))
    result={'revisione':'R06','controlli':checks,'fallimenti':[k for k,v in checks.items() if not v],'pezzi':parts,'sonde_terminali':probe,'sonda_pelle':skin,'intersezione_assieme_mm3':overlap,'hash_input':hashes,'limiti':'Solo dima di ingombro; nessuna prova fisica, di montaggio o resistenza. Screening delle autointersezioni, non prova geometrica completa.','dipendenze':{n:importlib.metadata.version(n) for n in ['cadquery','trimesh','manifold3d','numpy','scipy','shapely']}}
    folder=ROOT/'verifiche';folder.mkdir(exist_ok=True);(folder/'geometria.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'controlli':len(checks),'fallimenti':result['fallimenti']}));assert not result['fallimenti']
if __name__=='__main__':main()
