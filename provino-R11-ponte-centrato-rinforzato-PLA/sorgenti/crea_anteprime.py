"""R11: due versi dello stesso provino, e sezione reale alla radice destra."""
from pathlib import Path
import json,hashlib,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/boreo-r11-mpl')
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_utils import render,BG
R=Path(__file__).resolve().parents[1]
def main():
 path=R/'sorgenti/assieme/ponte.stl';m=trimesh.load_mesh(path,process=True)
 views=R/'anteprime/viste';views.mkdir(parents=True,exist_ok=True)
 t=np.array([[-1,0,0,0],[0,1,0,0],[0,0,-1,45.2],[0,0,0,1]],float);flipped=m.copy();flipped.apply_transform(t)
 for name,mesh in [('rinforzi_sotto',m),('rinforzi_sopra',flipped)]:
  render([{'id':'ponte','mesh':mesh,'role':1,'exploded':[0,0,0],'reference':False}],'assembled',[-1.25,-1.65,1.0],views/(name+'.png'))
 section=m.section(plane_origin=[42,0,0],plane_normal=[1,0,0]);assert section is not None
 fig=plt.figure(figsize=(15,10),facecolor=BG);fig.text(.04,.955,'BOREO R11 - PONTE CENTRATO E RINFORZATO',weight='bold',fontsize=20,color='#173341')
 fig.text(.04,.917,'Un solo pezzo PLA: fascia 28,8 mm - pelle 2 mm - due nervature interne su un solo verso',fontsize=11,color='#526774')
 for box,name,title in [([.025,.45,.47,.40],'rinforzi_sotto','Posa 1: nervature sotto le radici'),([.515,.45,.47,.40],'rinforzi_sopra','Posa 2: lo stesso pezzo capovolto')]:
  ax=fig.add_axes(box);ax.imshow(plt.imread(views/(name+'.png')));ax.axis('off');ax.set_title(title,fontsize=12,color='#173341')
 ax=fig.add_axes([.085,.115,.83,.27]);ax.set_facecolor(BG)
 for loop in section.discrete:
  ax.plot(loop[:,1],loop[:,2],color='#ad6028',linewidth=2)
 ax.axhline(22.6,color='#28718a',linestyle='--',linewidth=1)
 ax.annotate('Alette al centro',xy=(5,22.6),xytext=(0,33),arrowprops={'arrowstyle':'->','color':'#28718a'},color='#28718a',fontsize=11)
 ax.annotate('Tallone + nervatura interna',xy=(-32.0,20),xytext=(-24,10),arrowprops={'arrowstyle':'->','color':'#ad6028'},color='#ad6028',fontsize=10)
 ax.annotate('',xy=(-39,37),xytext=(-39,8.2),arrowprops={'arrowstyle':'<->','color':'#173341'});ax.text(-40,22.6,'28,8 mm',rotation=90,ha='center',va='center',fontsize=10,color='#173341')
 ax.text(12,19,'Tratto passante invariato\n9,2 x 3,2 mm',ha='center',va='top',fontsize=10,color='#173341')
 ax.set_aspect('equal');ax.set_xlim(-44,20);ax.set_ylim(6,39);ax.set_xlabel('Sezione reale alla radice destra: direzione verso la torcia →',fontsize=10);ax.set_yticks([]);ax.set_xticks([])
 for spine in ax.spines.values():spine.set_visible(False)
 fig.text(.04,.045,'Arancio: solo il provino da stampare. Base torcia non inclusa. Supporti di stampa necessari sotto le alette.',fontsize=10,color='#526774')
 fig.text(.04,.020,'PROVA DI INSERIMENTO E INGOMBRO - portata, calore e uso sul casco non convalidati.',fontsize=10,weight='bold',color='#173341')
 fig.savefig(R/'anteprime/PROVINO_R11_anteprima.png',dpi=150,facecolor=BG);plt.close(fig)
 (R/'anteprime/metodo.json').write_text(json.dumps({'metodo':'VTK e sezione geometrica dal solo STL esportato riaperto','stl':str(path.relative_to(R)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pose_inversa_matrice':t.tolist(),'casco_o_torcia_ricostruiti':False},indent=2)+'\n')
 print(R/'anteprime/PROVINO_R11_anteprima.png')
if __name__=='__main__':main()
