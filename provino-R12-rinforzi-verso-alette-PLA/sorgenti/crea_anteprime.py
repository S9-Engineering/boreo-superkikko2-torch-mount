"""R12: nervature esterne sotto i bracci, viste dai file esportati riaperti."""
from pathlib import Path
import os,json,hashlib
os.environ.setdefault('MPLCONFIGDIR','/tmp/boreo-r12-mpl')
import numpy as np,trimesh,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_utils import render,BG
R=Path(__file__).resolve().parents[1]
def main():
 path=R/'sorgenti/assieme/ponte.stl';m=trimesh.load_mesh(path,process=True);views=R/'anteprime/viste';views.mkdir(parents=True,exist_ok=True)
 def draw(mesh,direction,name):
  render([{'id':'ponte','mesh':mesh,'role':1,'exploded':[0,0,0],'reference':False}],'assembled',direction,views/(name+'.png'))
 draw(m,[1.2,1.65,-.85],'rinforzi_verso_alette')
 chosen=m.faces[np.all(m.vertices[m.faces][:,:,0]>35,axis=1)];close=trimesh.Trimesh(vertices=m.vertices.copy(),faces=chosen,process=True);close.remove_unreferenced_vertices()
 draw(close,[1.8,.25,-.8],'dettaglio_radice')
 section=m.section(plane_origin=[42,0,0],plane_normal=[1,0,0]);assert section is not None
 fig=plt.figure(figsize=(15,10),facecolor=BG);fig.text(.04,.955,'BOREO R12 - RINFORZO DALLA FASCIA ALL’ALETTA',fontsize=20,weight='bold',color='#173341')
 fig.text(.04,.917,'Fascia centrata 28,8 mm - pelle 2 mm - nervature sotto i bracci, sul lato verso la torcia',fontsize=11,color='#526774')
 for box,name,title in [([.025,.45,.47,.40],'rinforzi_verso_alette','Pezzo intero: vista dal lato delle alette'),([.515,.45,.47,.40],'dettaglio_radice','Dettaglio della nervatura sotto il braccio destro')]:
  ax=fig.add_axes(box);ax.imshow(plt.imread(views/(name+'.png')));ax.axis('off');ax.set_title(title,fontsize=11,color='#173341')
 ax=fig.add_axes([.13,.12,.74,.25]);ax.set_facecolor(BG)
 for loop in section.discrete:ax.plot(loop[:,1],loop[:,2],color='#a6602d',linewidth=2.4)
 ax.axhline(21,color='#7b8d97',linestyle='--',linewidth=.9)
 ax.annotate('Fascia curva',xy=(-29.4,23.6),xytext=(-33.5,24.4),arrowprops={'arrowstyle':'->','color':'#173341'},color='#173341',fontsize=11)
 ax.annotate('Nervatura verso la torcia',xy=(-23.0,20.5),xytext=(-24,18.9),arrowprops={'arrowstyle':'->','color':'#17637f'},color='#17637f',fontsize=11)
 ax.annotate('Aletta',xy=(-17.5,22.8),xytext=(-17,24.5),arrowprops={'arrowstyle':'->','color':'#173341'},color='#173341',fontsize=11)
 ax.set_xlim(-34,-11);ax.set_ylim(18.5,25.4);ax.set_aspect('equal');ax.set_xticks([]);ax.set_yticks([])
 for spine in ax.spines.values():spine.set_visible(False)
 ax.set_xlabel('Sezione reale ingrandita - sporgenza del rinforzo fino a 1,2 mm sotto l’aletta',fontsize=10,color='#173341')
 fig.text(.04,.061,'Retro verso la testa libero: eliminati i talloni della R11. Tratto anteriore e fori di fissaggio conservati.',fontsize=10,color='#526774')
 fig.text(.04,.035,'Spessore locale fino a 4,4 mm: nuovo ingombro nelle feritoie da provare senza forzare.',fontsize=10,weight='bold',color='#173341')
 fig.savefig(R/'anteprime/PROVINO_R12_anteprima.png',dpi=150,facecolor=BG);plt.close(fig)
 (R/'anteprime/metodo.json').write_text(json.dumps({'metodo':'VTK dal solo STL esportato riaperto e sua sezione aX42. Il dettaglio ritaglia solo la visualizzazione, non i file da stampare.','stl_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'casco_o_torcia_ricostruiti':False},indent=2)+'\n')
 print(R/'anteprime/PROVINO_R12_anteprima.png')
if __name__=='__main__':main()
