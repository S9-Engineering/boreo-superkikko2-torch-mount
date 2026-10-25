"""Verifica dei file R09 riaperti; non importa il generatore CAD."""
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
    check('tre_provini',len(manifest['pezzi'])==3)
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
    overlap=shapes['base_appoggi'].intersect(shapes['ponte_terminale']).Volume();check('assemblaggio_senza_interferenze',overlap<1e-6)
    probe={}
    original=cq.importers.importStep(str(ROOT/'sorgenti/riferimenti/PONTE_R07_ORIGINE.step')).val()
    bridge_print=shapes['ponte_terminale'].translate((0,0,-21))
    check('ponte_geometria_identica_R07',bridge_print.cut(original).Volume()+original.cut(bridge_print).Volume()<1e-5)
    pinsec=line_sections(shapes['dima_interasse'],[-40,83,2.2],[40,83,2.2])
    check('dima_due_pioli',len(pinsec)==2)
    check('dima_pioli_diametro1_6',all(abs(q['lunghezza_mm']-1.6)<1e-5 for q in pinsec))
    centers=sorted(sum(e[0] for e in q['estremi_mm'])/2 for q in pinsec)
    check('dima_interasse57_5',len(centers)==2 and abs(centers[1]-centers[0]-57.5)<1e-5)
    for x in [-28.75,28.75]:
        vertical=line_sections(shapes['dima_interasse'],[x,83,0],[x,83,4])
        check(f'dima_{x}:pelle_e_piolo_2_8',len(vertical)==1 and abs(vertical[0]['lunghezza_mm']-2.8)<1e-5)
        check(f'appoggio_{x}:foro_passante',not line_sections(shapes['base_appoggi'],[x,-5,22.6],[x,20,22.6]))
        face=line_sections(shapes['base_appoggi'],[x,-5,10],[x,9,10])
        check(f'appoggio_{x}:piano_Y8',len(face)==1 and abs(max(e[1] for e in face[0]['estremi_mm'])-8)<1e-5)
        cut=line_sections(shapes['base_appoggi'],[x-5,7.9,22.6],[x+5,7.9,22.6])
        cut=sorted(sorted(e[0] for e in q['estremi_mm']) for q in cut)
        check(f'appoggio_{x}:asola_lunga3',len(cut)==2 and abs(cut[1][0]-cut[0][1]-3)<1e-5)
        vertical_cut=line_sections(shapes['base_appoggi'],[x,7.9,20],[x,7.9,25])
        ranges=sorted(sorted(e[2] for e in q['estremi_mm']) for q in vertical_cut)
        check(f'appoggio_{x}:luce1_9',len(ranges)==2 and abs(ranges[1][0]-ranges[0][1]-1.9)<1e-5)
    top=line_sections(shapes['dima_interasse'],[-4,101.9,2.2],[4,101.9,2.2])
    check('dima_terzo_piolo',len(top)==1 and abs(top[0]['lunghezza_mm']-1.6)<1e-5)
    check('foro_superiore_passante',not line_sections(shapes['base_appoggi'],[0,-5,41.5],[0,20,41.5]))
    for x,z in [(0,10),(0,20),(0,30),(0,38),(-28.75,32),(28.75,32),(-10,40),(10,40)]:
        face=line_sections(shapes['base_appoggi'],[x,3.01,z],[x,8.01,z])
        check(f'piano_completo_{x}_{z}',len(face)==1 and abs(max(e[1] for e in face[0]['estremi_mm'])-8)<1e-5)
    for x in [-14.5,14.5]:
        relief=cq.Workplane('XY',origin=(x,-3,8)).box(10,20,10,centered=(True,False,False)).val()
        check(f'rivetto_{x}_scarico',shapes['base_appoggi'].intersect(relief).Volume()<1e-5)
    top_width=line_sections(shapes['base_appoggi'],[-5,7.9,41.5],[5,7.9,41.5])
    ranges=sorted(sorted(e[0] for e in q['estremi_mm']) for q in top_width)
    check('asola_superiore_lunga3',len(ranges)==2 and abs(ranges[1][0]-ranges[0][1]-3)<1e-5)
    top_height=line_sections(shapes['base_appoggi'],[0,7.9,39],[0,7.9,44])
    ranges=sorted(sorted(e[2] for e in q['estremi_mm']) for q in top_height)
    check('asola_superiore_luce1_9',len(ranges)==2 and abs(ranges[1][0]-ranges[0][1]-1.9)<1e-5)

    bp=bounds_cad(shapes['ponte_terminale'])
    check('ponte_limite_inferiore_R06_conservato',abs(bp[0,2]-21)<1e-6)
    check('ponte_sviluppo_solo_alto',abs(bp[1,2]-37)<1e-6)
    c=params['centro_curva_xy'];inside=cq.Solid.makeCylinder(params['base_raggio_interno'],100,cq.Vector(*c,-20),cq.Vector(0,0,1))
    check('base_non_protrude_dietro_curva_contatto',shapes['base_appoggi'].intersect(inside).Volume()<1e-5)
    for x in params['assi_terminali_x']:
        y=params['fissaggio_asse_y']
        check(f'vite_{x}:passaggio_base',not line_sections(shapes['base_appoggi'],[x,y,8],[x,y,30]))
        check(f'vite_{x}:passaggio_ponte',not line_sections(shapes['ponte_terminale'],[x,y,19],[x,y,30]))
        check(f'vite_{x}:bordo_trasversale_2_9',abs((params['terminale_larghezza']-params['fissaggio_diametro'])/2-2.9)<1e-6)
        check(f'vite_{x}:bordo_frontale_4_3',abs(params['terminale_fronte_y']-y-params['fissaggio_diametro']/2-4.3)<1e-6)
        nut=next(p for p in manifest['riferimenti'] if p['id'].startswith('dado_') and p['id'].endswith('1' if x<0 else '2'))
        ns=cq.importers.importStep(str(ROOT/nut['step_assieme'])).val()
        check(f'dado_{x}:tasca_libera',ns.intersect(shapes['base_appoggi']).Volume()<1e-5)
        # Il dado entra dall'esterno, da sotto; tutta la traiettoria nominale deve essere libera.
        travel=[ns.translate((0,0,-float(d))).intersect(shapes['base_appoggi']).Volume() for d in range(0,9)]
        check(f'dado_{x}:inserimento_da_sotto',max(travel)<1e-5)
        for kind in ['vite_','rondella_']:
            ref=next(p for p in manifest['riferimenti'] if p['id'].startswith(kind) and p['id'].endswith('1' if x<0 else '2'))
            hs=cq.importers.importStep(str(ROOT/ref['step_assieme'])).val()
            check(f'{kind}{x}:nessuna_interferenza_plastica',all(hs.intersect(obj).Volume()<1e-5 for obj in shapes.values()))
    for x in params['assi_terminali_x']:
        hs=line_sections(shapes['ponte_terminale'],[x,-12,18],[x,-12,28]);ws=line_sections(shapes['ponte_terminale'],[x-8,-12,23],[x+8,-12,23])
        check(f'terminale_{x}:altezza3_2',len(hs)==1 and abs(hs[0]['lunghezza_mm']-params['terminale_altezza'])<1e-5)
        check(f'terminale_{x}:larghezza9_2',len(ws)==1 and abs(ws[0]['lunghezza_mm']-params['terminale_larghezza'])<1e-5)
        passage=line_sections(shapes['base_appoggi'],[x,-50,23],[x,30,23]);check(f'base_{x}:passaggio_aperto',not passage)
        probe[str(x)]={'altezza':hs,'larghezza':ws,'base_lungo_passaggio':passage}
    skin=line_sections(shapes['ponte_terminale'],[0,-20,23],[0,-17,23]);check('ponte_spessore1_2',len(skin)==1 and abs(skin[0]['lunghezza_mm']-1.2)<1e-5)
    path=ROOT/manifest['piatto_geometrico']['file'];ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    with zipfile.ZipFile(path) as z:
        check('3MF_CRC',z.testzip() is None);model=ET.fromstring(z.read('3D/3dmodel.model'));check('3MF_mm',model.get('unit')=='millimeter')
        objects=model.findall('m:resources/m:object',ns);build=model.findall('m:build/m:item',ns);check('3MF_tre_oggetti',len(objects)==len(build)==3)
        for o,item,p in zip(objects,build,manifest['pezzi']):
            vs=np.array([[float(v.get(k)) for k in 'xyz'] for v in o.findall('m:mesh/m:vertices/m:vertex',ns)])
            fs=np.array([[int(f.get(k)) for k in ['v1','v2','v3']] for f in o.findall('m:mesh/m:triangles/m:triangle',ns)])
            m=trimesh.Trimesh(vs,fs,process=True);comp=compare_mesh(meshes[p['id']],m);check('3MF_geometria_'+p['id'],comp['triangoli_coincidenti'])
            tr=np.array([float(v) for v in item.get('transform').split()]);check('3MF_matrice_'+p['id'],len(tr)==12 and np.allclose(tr[:9],[1,0,0,0,1,0,0,0,1]))
            m.apply_translation(tr[9:]);check('3MF_sul_piano_'+p['id'],abs(m.bounds[0,2])<1e-6)
            check('3MF_margine_brim_'+p['id'],np.all(m.bounds[0,:2]-4>0) and np.all(m.bounds[1,:2]+4<246))
    scene=trimesh.load(ROOT/manifest['assieme']['glb'],force='scene');check('GLB_tre_componenti',len(scene.geometry)==3)
    for node in scene.graph.nodes_geometry:
        transform,geometry=scene.graph[node];m=scene.geometry[geometry].copy();m.apply_transform(transform);m.apply_scale(1000)
        ref=trimesh.load_mesh(ROOT/next(p['stl_assieme'] for p in manifest['pezzi'] if p['id']==node),process=True)
        check('GLB_scala_'+node,np.allclose(m.bounds,ref.bounds,atol=.001,rtol=0))
    whole=cq.importers.importStep(str(ROOT/manifest['assieme']['step'])).val();check('STEP_assieme_tre_solidi',len(whole.Solids())==3 and whole.isValid())
    check('file_stabili',all(sha(ROOT/k)==v for k,v in hashes.items()))
    result={'revisione':'R09','controlli':checks,'fallimenti':[k for k,v in checks.items() if not v],'pezzi':parts,'sonde_terminali':probe,'sonda_pelle':skin,'intersezione_assieme_mm3':overlap,'hash_input':hashes,'limiti':'R09 solo provini: asole/appoggi/comfort da provare; ponte identico R07. Carichi e calore non convalidati; R06 ha solo riscontro utente di inserimento al limite. Screening delle autointersezioni, non prova geometrica completa.','dipendenze':{n:importlib.metadata.version(n) for n in ['cadquery','trimesh','manifold3d','numpy','scipy','shapely']}}
    folder=ROOT/'verifiche';folder.mkdir(exist_ok=True);(folder/'geometria.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'controlli':len(checks),'fallimenti':result['fallimenti']}));assert not result['fallimenti']
if __name__=='__main__':main()
