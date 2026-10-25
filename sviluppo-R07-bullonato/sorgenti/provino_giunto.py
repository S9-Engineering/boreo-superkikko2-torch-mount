"""Piccolo provino M3 per tasca dado, foro e gioco laterale, separato dal casco."""
from pathlib import Path
import sys,shutil,json,hashlib
import cadquery as cq
import trimesh
from genera import block,cyl,hexagon,plate
from geometria_utils import mesh_metrics,self_intersections
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'provino-giunto'
def main():
 for d in ['sorgenti','stampa','slicer','verifiche','anteprime']:(OUT/d).mkdir(parents=True,exist_ok=True)
 for name in ['machine.json','process.json','filament.json']:shutil.copy2(ROOT/'slicer'/name,OUT/'slicer'/name)
 seat=block(0,0,0,14,20,10.6,1)
 for x in [-5.975,5.975]:seat=seat.fuse(block(x,0,10.6,2.05,5,3.9))
 seat=seat.cut(cyl(0,10,-1,3.4,20)).cut(hexagon(0,10,-.01,5.85,4.31)).clean()
 tongue=block(0,0,0,9.2,20,3.2,.6).cut(cyl(0,10,-1,3.4,6)).clean()
 shapes={'sede_dado':seat,'linguetta':tongue};meshes={};items=[];checks={};details={}
 for name,s in shapes.items():
  stem='R07_PROVINO_'+name.upper();cq.exporters.export(s,str(OUT/'stampa'/(stem+'.step')));cq.exporters.export(s,str(OUT/'stampa'/(stem+'.stl')),tolerance=.04,angularTolerance=.1)
  reopened=cq.importers.importStep(str(OUT/'stampa'/(stem+'.step'))).val()
  m=trimesh.load_mesh(OUT/'stampa'/(stem+'.stl'),process=True);metrics=mesh_metrics(m);screen=self_intersections(m)
  checks[name+':STEP_valido']=bool(reopened.isValid() and len(reopened.Solids())==1)
  for key in ['mesh_chiusa','normali_coerenti','volume_positivo','vertici_finiti']:checks[name+':'+key]=metrics[key]
  checks[name+':un_corpo']=metrics['corpi_connessi']==1
  for key in ['spigoli_incidenza_diversa_da_2','facce_duplicate','facce_degeneri_area_inferiore_1e-10']:checks[name+':'+key]=metrics[key]==0
  checks[name+':manifold']=metrics['manifold_importazione']['stato']=='Error.NoError'
  checks[name+':screening_autointersezioni']=screen['coppie_con_intersezione']==0
  checks[name+':piano']=abs(m.bounds[0,2])<1e-6
  details[name]={'mesh':metrics,'autointersezioni':screen};meshes[name]=m
  items.append({'id':name,'quantita':1,'stl_stampa':f'stampa/{stem}.stl','step_stampa':f'stampa/{stem}.step'})
 checks['gioco_assemblaggio_nominale']=seat.intersect(tongue.translate((0,0,10.6))).Volume()<1e-6
 mf=OUT/'stampa/R07_PROVINO_SOLO_GEOMETRIA.3mf';placements=plate(meshes,mf)
 manifest={'revisione':'R07_PROVINO_GIUNTO','pezzi':items,'piatto_geometrico':{'file':str(mf.relative_to(OUT)),'items':placements,'unita':'mm','numero_pezzi':2}}
 (OUT/'sorgenti/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 checks={k:bool(v) for k,v in checks.items()}
 (OUT/'verifiche/geometria.json').write_text(json.dumps({'controlli':checks,'fallimenti':[k for k,v in checks.items() if not v],'pezzi':details,'hash_input':{str(f.relative_to(OUT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (OUT/'stampa').iterdir()}},indent=2)+'\n')
 assert all(checks.values());print('Provino:',len(checks),'controlli superati')
 if '--slice' in sys.argv:
  sys.argv=[sys.argv[0]]
  import prepara_slicing_pla as slicer
  slicer.ROOT=OUT;slicer.NAME='BOREO_R07_PROVINO_GIUNTO_PLA_ECC2_04';slicer.main()
if __name__=='__main__':main()
