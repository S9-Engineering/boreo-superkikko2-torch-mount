"""Sagoma illustrativa farfalla: misure fotografiche separate da ipotesi. NON stampare."""
from pathlib import Path
import json,hashlib,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/boreo-farfalla-rilievo-mpl')
import cadquery as cq
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'sorgenti/parametri-riferimento.json').read_text())
M=P['quote_da_letture_fotografiche'];A=P['quote_solo_assunte_per_sagoma'];C=P['quote_dichiarate_utente']
I=M['larghezza_totale']-2*C['bordo_esterno_asole']-C['larghezza_asole_laterali']
assert abs(I-P['quote_calcolate']['interasse_asole'])<1e-9
def main():
 W=M['larghezza_totale'];H=A['altezza_totale'];N=M['larghezza_collo']/2;T=M['larghezza_T'];cx=I/2;r=A['larghezza_alette_laterali']/2;z=A['altezza_alette_laterali']-r;b=A['traversa_inferiore_z'];bt=A['traversa_superiore_z'];tz=H-A['altezza_T']/2
 w=(cq.Workplane('XZ').moveTo(-cx-r,r).lineTo(-cx-r,z)
    .threePointArc((-cx,z+r),(-cx+r,z)).lineTo(-cx+r,24)
    .threePointArc((-23,20),(-19,bt)).lineTo(-13,bt)
    .threePointArc((-6.5,21),(-N,27)).lineTo(-N,34)
    .threePointArc((-6.5,37.5),(-10,H-6)).lineTo(-(T/2-3),H-6)
    .threePointArc((-T/2,tz),(-(T/2-3),H)).lineTo(T/2-3,H)
    .threePointArc((T/2,tz),(T/2-3,H-6)).lineTo(10,H-6)
    .threePointArc((6.5,37.5),(N,34)).lineTo(N,27)
    .threePointArc((6.5,21),(13,bt)).lineTo(19,bt)
    .threePointArc((23,20),(cx-r,24)).lineTo(cx-r,z)
    .threePointArc((cx,z+r),(cx+r,z)).lineTo(cx+r,r)
    .threePointArc((cx,0),(cx-r,r)).lineTo(cx-r,4.5)
    .threePointArc((23,8),(19,b)).lineTo(-19,b)
    .threePointArc((-23,8),(-cx+r,4.5)).lineTo(-cx+r,r)
    .threePointArc((-cx,0),(-cx-r,r)).close().extrude(A['spessore_lamiera']).val())
 for x in [-cx,cx]:
  cut=cq.Workplane('XZ',origin=(x,1,A['centro_asole_z'])).slot2D(A['lunghezza_asole_laterali'],C['larghezza_asole_laterali'],90).extrude(A['spessore_lamiera']+2).val();w=w.cut(cut)
 cut=cq.Workplane('XZ',origin=(0,1,tz)).slot2D(A['larghezza_asola_T'],A['altezza_asola_T'],0).extrude(A['spessore_lamiera']+2).val();w=w.cut(cut).clean()
 assert w.isValid() and len(w.Solids())==1 and w.Volume()>0
 dest=ROOT/'riferimenti-CAD-NON-STAMPARE/FARFALLA_STIMA_NON_STAMPARE.step';cq.exporters.export(w,str(dest))
 s=cq.importers.importStep(str(dest)).val();assert s.isValid() and len(s.Solids())==1
 line=cq.Edge.makeLine(cq.Vector(-40,-A['spessore_lamiera']/2,15),cq.Vector(40,-A['spessore_lamiera']/2,15))
 intervals=sorted(sorted([e.startPoint().x,e.endPoint().x]) for e in s.intersect(line).Edges())
 assert len(intervals)==3
 gaps=[[intervals[i][1],intervals[i+1][0]] for i in range(2)]
 widths=[b-a for a,b in gaps];centers=[(a+b)/2 for a,b in gaps]
 assert all(abs(x-C['larghezza_asole_laterali'])<1e-6 for x in widths)
 assert abs(centers[1]-centers[0]-I)<1e-6
 assert abs(intervals[0][1]-intervals[0][0]-C['bordo_esterno_asole'])<1e-6
 assert abs(intervals[2][1]-intervals[2][0]-C['bordo_esterno_asole'])<1e-6
 vs,fs=s.tessellate(.04,.1);mesh=trimesh.Trimesh(vertices=np.array([v.toTuple() for v in vs]),faces=np.array(fs),process=True)
 assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
 assert np.all(mesh.area_faces>1e-10)
 metric=mesh.copy();mesh.apply_scale(.001);mesh.visual.face_colors=[160,166,166,255];glb=dest.with_suffix('.glb');trimesh.Scene(mesh).export(str(glb))
 scene=trimesh.load(glb,force='scene');reopened=scene.to_mesh();assert np.allclose(reopened.bounds*1000,metric.bounds,atol=.001)
 section=metric.section(plane_origin=[0,-A['spessore_lamiera']/2,0],plane_normal=[0,1,0]);loops=section.discrete
 def area(v):
  p=v[:,[0,2]];return abs(np.sum(p[:,0]*np.roll(p[:,1],1)-np.roll(p[:,0],1)*p[:,1]))
 loops=sorted(loops,key=area,reverse=True)
 fig,ax=plt.subplots(figsize=(13,9),facecolor='#f5f7f8');ax.set_facecolor('#f5f7f8')
 for i,v in enumerate(loops):ax.add_patch(Polygon(v[:,[0,2]],closed=True,facecolor='#a5afb1' if i==0 else '#f5f7f8',edgecolor='#455a62',linewidth=1.3))
 blue='#17637f';red='#ab493c';green='#286956';orange='#975e16'
 def dim(p1,p2,text,pos,color=blue):
  ax.annotate('',xy=p2,xytext=p1,arrowprops={'arrowstyle':'<->','color':color,'lw':1.6});ax.text(*pos,text,ha='center',va='center',fontsize=11,color=color,bbox={'facecolor':'#f5f7f8','edgecolor':'none','pad':2})
 dim((-W/2,-5),(W/2,-5),'Foto 1: circa 63,5 mm',(0,-6.5))
 dim((-T/2,H+4),(T/2,H+4),'Foto 5: circa 31 mm',(0,H+6.2))
 dim((-N,30),(N,30),'Foto 7: circa 10,5 mm',(0,32.8))
 dim((38,b),(38,H),'Foto 6: circa 36 mm\nestremi da confermare',(49,27))
 dim((-cx,-12),(cx,-12),'Interasse calcolato: circa 57,5 mm',(0,-14),orange)
 ax.annotate('Larghezza libera asole\n2 mm - conferma utente',xy=(-cx,15),xytext=(-52,20),fontsize=11,color=green,ha='center',arrowprops={'arrowstyle':'->','color':green})
 ax.annotate('Bordo esterno nel piano: 2 mm\nSpessore lamiera ancora da rilevare',xy=(cx+2,24),xytext=(47,2),fontsize=10,color=green,ha='center',arrowprops={'arrowstyle':'->','color':green})
 ax.set_xlim(-65,70);ax.set_ylim(-19,58);ax.set_aspect('equal');ax.axis('off')
 fig.suptitle('FARFALLA SUPERKIKKO2 - RILIEVO PRELIMINARE',fontsize=19,weight='bold',color='#173341',y=.96)
 fig.text(.06,.90,'Blu: letture foto. Verde: quote utente. Ocra: calcolo con simmetria delle due alette.',fontsize=11,color='#455a62')
 fig.text(.06,.055,'Altezza totale, lunghezza asole e raccordi illustrativi. Spessore 1,5 mm solo assunto per il CAD.',fontsize=10,color='#455a62')
 fig.text(.06,.03,'RIFERIMENTO DA COMPLETARE - NON STAMPARE. I valori ignoti restano null nel rilievo.',fontsize=10,weight='bold',color=red)
 fig.savefig(ROOT/'anteprime/rilievo_quote.png',dpi=160,facecolor=fig.get_facecolor());plt.close(fig)
 report={'stato':'RIFERIMENTO_CAD_ILLUSTRATIVO_NON_STAMPARE','STEP_riaperto_valido':s.isValid(),'STEP_solidi':len(s.Solids()),'STEP_volume_mm3':s.Volume(),'sezione_STEP_asole':{'z_mm':15,'intervalli_metallo_x_mm':intervals,'luci_asole_mm':widths,'centri_x_mm':centers,'interasse_mm':centers[1]-centers[0]},'dimensioni_mm':metric.extents.tolist(),'scala_GLb':'metri, verificata contro STEP','mesh_GLb_chiusa':bool(metric.is_watertight),'normali_coerenti':bool(metric.is_winding_consistent),'volume_positivo':bool(metric.volume>0),'loop_sezione':len(loops),'file_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [dest,glb,ROOT/'sorgenti/parametri-riferimento.json']},'limiti':['Solo ricostruzione illustrativa della farfalla metallica.','Nessuna convalida dimensionale, di montaggio, strutturale o termica.','Luce asole2mm e bordo2mm dichiarati; interasse circa57.5 calcolato. Spessore e altezza totale non rilevati.','Non è una revisione pronta per lo slicer o per la stampa.','Non è stata modificata o preparata per stampa la base R07.']}
 (ROOT/'verifiche/riferimento.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
