"""Verifica indipendente dei file R12 riaperti, delle due pose e dei passaggi."""
from pathlib import Path
import json,hashlib,math,zipfile,xml.etree.ElementTree as ET
import numpy as np
import trimesh,cadquery as cq
from geometria_utils import mesh_metrics,self_intersections,bounds_cad,line_sections,compare_mesh
R=Path(__file__).resolve().parents[1]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def main():
 man=json.loads((R/'sorgenti/manifest.json').read_text());part=man['pezzi'][0];checks={}
 def check(k,c):checks[k]=bool(c)
 paths=[R/part[k] for k in ['stl_stampa','step_stampa','stl_assieme','step_assieme']]+[R/'sorgenti/parametri.json',R/'sorgenti/manifest.json',R/man['piatto_geometrico']['file'],R/'sorgenti/assieme/ponte.glb',R/'sorgenti/riferimenti/PONTE_R10_STAMPA.step',R/'sorgenti/riferimenti/BASE_R10_STAMPA.step']
 hashes={str(f.relative_to(R)):sha(f) for f in paths}
 mesh=trimesh.load_mesh(R/part['stl_stampa'],process=True);metrics=mesh_metrics(mesh);screen=self_intersections(mesh)
 for k in ['mesh_chiusa','normali_coerenti','volume_positivo','vertici_finiti']:check(k,metrics[k])
 for k in ['spigoli_incidenza_diversa_da_2','facce_duplicate','facce_degeneri_area_inferiore_1e-10']:check(k,metrics[k]==0)
 check('un_solo_corpo',metrics['corpi_connessi']==1);check('manifold',metrics['manifold_importazione']['stato']=='Error.NoError');check('autointersezioni_screening',screen['coppie_con_intersezione']==0)
 printing=cq.importers.importStep(str(R/part['step_stampa'])).val();shape=cq.importers.importStep(str(R/part['step_assieme'])).val();check('STEP_valido',printing.isValid() and shape.isValid() and len(shape.Solids())==len(printing.Solids())==1)
 check('volume_STEP_STL',abs(printing.Volume()-mesh.volume)/printing.Volume()<.01);check('limiti_STEP_STL',np.max(np.abs(bounds_cad(printing)-mesh.bounds))<.061)
 moved=shape.translate((0,0,-8.2));check('pose_coerenti',moved.cut(printing).Volume()+printing.cut(moved).Volume()<1e-5);check('sul_piano',abs(mesh.bounds[0,2])<1e-6)
 b=bounds_cad(shape);check('fascia_basso8_2',abs(b[0,2]-8.2)<1e-5);check('fascia_alto37',abs(b[1,2]-37)<1e-5);check('aletta_centrata22_6',abs((b[0,2]+b[1,2])/2-22.6)<1e-5)
 flip=shape.rotate((0,0,22.6),(0,1,22.6),180)
 base=cq.importers.importStep(str(R/'sorgenti/riferimenti/BASE_R10_STAMPA.step')).val();old=cq.importers.importStep(str(R/'sorgenti/riferimenti/PONTE_R10_STAMPA.step')).val().translate((0,0,21))
 for name,pose in [('normale',shape),('capovolto',flip)]:
  check(f'{name}:nessuna_interferenza_base_R10',pose.intersect(base).Volume()<1e-5)
  for x in [-42,42]:
   check(f'{name}:{x}:foro_M3_libero',not line_sections(pose,[x,8,18],[x,8,27]))
   hs=line_sections(pose,[x,-12,18],[x,-12,27]);ws=line_sections(pose,[x-8,-12,22.6],[x+8,-12,22.6])
   check(f'{name}:{x}:altezza_passaggio3_2',len(hs)==1 and abs(hs[0]['lunghezza_mm']-3.2)<1e-5)
   check(f'{name}:{x}:larghezza_passaggio9_2',len(ws)==1 and abs(ws[0]['lunghezza_mm']-9.2)<1e-5)
 cylinder=cq.Solid.makeCylinder(105.0001,100,cq.Vector(0,-110,-20),cq.Vector(0,0,1))
 outside=shape.cut(cylinder);refoutside=old.cut(cylinder);outsideflip=flip.cut(cylinder)
 check('tratto_oltre_raggio105_invariato',outside.cut(refoutside).Volume()+refoutside.cut(outside).Volume()<1e-5)
 check('passante_invariato_anche_capovolto',outsideflip.cut(refoutside).Volume()+refoutside.cut(outsideflip).Volume()<1e-5)
 inner=cq.Solid.makeCylinder(90,100,cq.Vector(0,-110,-20),cq.Vector(0,0,1));outer=cq.Solid.makeCylinder(92,100,cq.Vector(0,-110,-20),cq.Vector(0,0,1));annulus=outer.cut(inner)
 body=shape.intersect(annulus);flipped_body=flip.intersect(annulus)
 check('fascia_simmetrica_verticalmente',body.cut(flipped_body).Volume()+flipped_body.cut(body).Volume()<1e-5)
 for angle in [-.4,0,.4]:
  c=[0,-110];start=[89*math.sin(angle),c[1]+89*math.cos(angle),30];end=[93*math.sin(angle),c[1]+93*math.cos(angle),30]
  sec=line_sections(shape,start,end);check(f'spessore2mm_{angle}',len(sec)==1 and abs(sec[0]['lunghezza_mm']-2)<1e-5)
  check(f'raggio_esterno92_{angle}',len(sec)==1 and abs(max(math.hypot(e[0],e[1]+110) for e in sec[0]['estremi_mm'])-92)<1e-5)
 # La geometria nuova resta dal lato esterno; il retro R90 e' libero.
 check('nessun_tallone_o_rinforzo_verso_testa',shape.intersect(inner).Volume()<1e-5)
 rinforzi=[]
 for x in [-42,42]:
  check(f'nervatura_verso_aletta_sotto_{x}',bool(line_sections(shape,[x,-27,20.5],[x,-18,20.5])))
  check(f'nessuna_nervatura_sopra_{x}',not line_sections(shape,[x,-25,24.7],[x,-18,24.7]))
  check(f'nessun_tallone_interno_{x}',not line_sections(shape,[x,-33,22.6],[x,-30.8,22.6]))
  check(f'inversione_nervatura_sopra_{x}',bool(line_sections(flip,[x,-27,24.7],[x,-18,24.7])))
  heights=[]
  for y in np.linspace(-29.6,-16.2,16):
   hs=line_sections(shape,[x,float(y),18],[x,float(y),27])
   # Salta i campioni dentro la fascia, che e' intenzionalmente alta28.8.
   if math.hypot(x,y+110)>92.01 and len(hs)==1:heights.append(hs[0]['lunghezza_mm'])
  check(f'ingombro_verticale_locale_fino4_4_{x}',heights and max(heights)<=4.40001 and max(heights)>3.5)
  rinforzi.append({'x':x,'altezza_locale_campionata_max_mm':max(heights)})
 ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
 with zipfile.ZipFile(R/man['piatto_geometrico']['file']) as z:
  check('3MF_CRC',z.testzip() is None);model=ET.fromstring(z.read('3D/3dmodel.model'));check('3MF_unita_mm',model.get('unit')=='millimeter');obs=model.findall('m:resources/m:object',ns);items=model.findall('m:build/m:item',ns);check('3MF_un_oggetto',len(obs)==len(items)==1)
  ob=obs[0];v=np.array([[float(v.get(k)) for k in 'xyz'] for v in ob.findall('m:mesh/m:vertices/m:vertex',ns)]);f=np.array([[int(f.get(k)) for k in ['v1','v2','v3']] for f in ob.findall('m:mesh/m:triangles/m:triangle',ns)]);m=trimesh.Trimesh(v,f,process=True);check('3MF_mesh_identica_STL',compare_mesh(mesh,m)['triangoli_coincidenti'])
  transform=np.array([float(v) for v in items[0].get('transform').split()]);check('3MF_matrice_rigida',len(transform)==12 and np.allclose(transform[:9],[1,0,0,0,1,0,0,0,1]));m.apply_translation(transform[9:]);check('3MF_posa_piano',abs(m.bounds[0,2])<1e-5);check('3MF_margini',np.all(m.bounds[0,:2]>10) and np.all(m.bounds[1,:2]<246))
 scene=trimesh.load(R/'sorgenti/assieme/ponte.glb',force='scene');check('GLB_un_oggetto',len(scene.geometry)==1);gm=scene.to_mesh();check('GLB_metri',np.allclose(gm.bounds*1000,bounds_cad(shape),atol=.061))
 check('nessuna_modifica_input',all(sha(R/k)==h for k,h in hashes.items()))
 result={'revisione':'R12','controlli':checks,'fallimenti':[k for k,v in checks.items() if not v],'mesh':metrics,'autointersezioni':screen,'hash_input':hashes,'ingombri_rinforzi':rinforzi,'limiti':'Solo verifiche digitali: nessuna prova sul casco della fascia28.8mm o dei rinforzi esterni nelle feritoie; nessuna resistenza, ritenuta o temperatura convalidata. Screening autointersezioni non matematicamente completo.'}
 (R/'verifiche/geometria.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'controlli':len(checks),'fallimenti':result['fallimenti']}));assert not result['fallimenti']
if __name__=='__main__':main()
