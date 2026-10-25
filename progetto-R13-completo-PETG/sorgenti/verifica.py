"""Controlli indipendenti su STEP, STL, GLB e 3MF finali riaperti."""
from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as ET
import numpy as np
import trimesh,cadquery as cq
from geometria_utils import mesh_metrics,self_intersections,bounds_cad,line_sections,compare_mesh,transform_cad_rigid
from verifiche_specifiche import verifica_ponte,verifica_base
R=Path(__file__).resolve().parents[1]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def main():
    man=json.loads((R/'sorgenti/manifest.json').read_text());checks={};meshes={};shapes={};detail={}
    def check(k,c):checks[k]=bool(c)
    files=[R/'sorgenti/manifest.json',R/man['piatto_geometrico']['file'],R/man['assieme']['glb'],R/man['assieme']['step'],
      *[R/p[k] for p in man['pezzi'] for k in ['stl_stampa','step_stampa','stl_assieme','step_assieme']],
      *[R/p[k] for p in man['riferimenti'] for k in ['stl_assieme','step_assieme']],
      *list((R/'sorgenti/riferimenti').glob('*.step')),*list((R/'sorgenti').glob('*.json')),R/'sorgenti/logo_S9.svg']
    hashes={str(f.relative_to(R)):sha(f) for f in files}
    check('due_pezzi_una_copia',len(man['pezzi'])==2 and all(p['quantita']==1 for p in man['pezzi']))
    for p in man['pezzi']:
        name=p['id'];mesh=trimesh.load_mesh(R/p['stl_stampa'],process=True)
        metrics=mesh_metrics(mesh);screen=self_intersections(mesh)
        for k in ['mesh_chiusa','normali_coerenti','volume_positivo','vertici_finiti']:check(name+':'+k,metrics[k])
        for k in ['spigoli_incidenza_diversa_da_2','facce_duplicate','facce_degeneri_area_inferiore_1e-10']:check(name+':'+k,metrics[k]==0)
        check(name+':un_solo_corpo',metrics['corpi_connessi']==1)
        check(name+':manifold',metrics['manifold_importazione']['stato']=='Error.NoError')
        check(name+':autointersezioni_screening',screen['coppie_con_intersezione']==0)
        printing=cq.importers.importStep(str(R/p['step_stampa'])).val()
        shape=cq.importers.importStep(str(R/p['step_assieme'])).val()
        check(name+':STEP_valido',printing.isValid() and shape.isValid() and len(shape.Solids())==len(printing.Solids())==1)
        check(name+':volume_STEP_STL',abs(printing.Volume()-mesh.volume)/printing.Volume()<.01)
        check(name+':limiti_STEP_STL',np.max(np.abs(bounds_cad(printing)-mesh.bounds))<.061)
        moved=transform_cad_rigid(shape,p['matrice_stampa_da_assieme'])
        check(name+':pose_CAD_coerenti',moved.cut(printing).Volume()+printing.cut(moved).Volume()<1e-5)
        am=trimesh.load_mesh(R/p['stl_assieme'],process=True);am.apply_transform(p['matrice_stampa_da_assieme'])
        check(name+':pose_STL_coerenti',np.allclose(am.bounds,mesh.bounds,atol=1e-4,rtol=0) and abs(am.volume-mesh.volume)<.01)
        check(name+':sul_piano',abs(mesh.bounds[0,2])<1e-6)
        ref='PONTE_R12_STAMPA.step' if name=='ponte_centrato' else 'BASE_R10_STAMPA.step'
        original=cq.importers.importStep(str(R/'sorgenti/riferimenti'/ref)).val()
        check(name+':geometria_precedente_conservata',printing.cut(original).Volume()+original.cut(printing).Volume()<1e-5)
        meshes[name]=mesh;shapes[name]=shape;detail[name]={'mesh':metrics,'autointersezioni':screen}
    verifica_ponte(shapes['ponte_centrato'],R,check)
    verifica_base(shapes,man,R,check)
    ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'};placed=[]
    with zipfile.ZipFile(R/man['piatto_geometrico']['file']) as z:
        check('3MF_CRC',z.testzip() is None);model=ET.fromstring(z.read('3D/3dmodel.model'))
        check('3MF_unita_mm',model.get('unit')=='millimeter')
        obs=model.findall('m:resources/m:object',ns);items=model.findall('m:build/m:item',ns)
        check('3MF_due_oggetti',len(obs)==len(items)==2)
        for ob,item,p in zip(obs,items,man['pezzi']):
            name=p['id'];v=np.array([[float(v.get(k)) for k in 'xyz'] for v in ob.findall('m:mesh/m:vertices/m:vertex',ns)])
            f=np.array([[int(f.get(k)) for k in ['v1','v2','v3']] for f in ob.findall('m:mesh/m:triangles/m:triangle',ns)])
            m=trimesh.Trimesh(v,f,process=True);check('3MF_mesh_identica:'+name,compare_mesh(meshes[name],m)['triangoli_coincidenti'])
            tr=np.array([float(v) for v in item.get('transform').split()])
            check('3MF_matrice_rigida:'+name,len(tr)==12 and np.allclose(tr[:9],[1,0,0,0,1,0,0,0,1]))
            m.apply_translation(tr[9:]);placed.append(m)
            check('3MF_posa_piano:'+name,abs(m.bounds[0,2])<1e-5)
            check('3MF_margini:'+name,np.all(m.bounds[0,:2]>10) and np.all(m.bounds[1,:2]<246))
        separation=placed[1].bounds[0,1]-placed[0].bounds[1,1]
        check('piatto_oggetti_separati_oltre20mm',separation>20)
    scene=trimesh.load(R/man['assieme']['glb'],force='scene');check('GLB_due_oggetti',len(scene.geometry)==2)
    for node in scene.graph.nodes_geometry:
        transform,geometry=scene.graph[node];gm=scene.geometry[geometry].copy();gm.apply_transform(transform);gm.apply_scale(1000)
        check('GLB_metri:'+node,np.allclose(gm.bounds,bounds_cad(shapes[node]),atol=.061))
    whole=cq.importers.importStep(str(R/man['assieme']['step'])).val()
    check('STEP_assieme_due_solidi',len(whole.Solids())==2 and whole.isValid())
    check('nessuna_modifica_input',all(sha(R/k)==h for k,h in hashes.items()))
    result={'revisione':'R13','controlli':checks,'fallimenti':[k for k,v in checks.items() if not v],
      'pezzi':detail,'hash_input':hashes,'distanza_pezzi_piatto_Y_mm':float(separation),
      'limiti':'Verifiche digitali sui file esportati, senza riparazioni mesh. Screening autointersezioni non matematicamente completo. Montaggio, carico e temperatura non verificati fisicamente.'}
    (R/'verifiche/geometria.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'controlli':len(checks),'fallimenti':result['fallimenti']}));assert not result['fallimenti']
if __name__=='__main__':main()
