"""Viste dell'assieme e del piatto dai soli STL finali riaperti."""
from pathlib import Path
import os,json,hashlib
os.environ.setdefault('MPLCONFIGDIR','/tmp/boreo-r13-matplotlib')
import numpy as np,trimesh,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_utils import render,carica,BG
R=Path(__file__).resolve().parents[1]
def main():
    man=json.loads((R/'source/manifest.json').read_text());parts=carica();views=R/'previews/technical';views.mkdir(exist_ok=True)
    for mode,direction,name in [('assembled',[1.5,2.0,1.0],'assieme_frontale'),
                               ('support',[-1.4,-2.0,1.0],'assieme_interno'),
                               ('exploded',[1.5,2.0,1.1],'esploso')]:
        render(parts,mode,direction,views/(name+'.png'))
    layout=[]
    for p in man['pezzi']:
        m=trimesh.load_mesh(R/p['stl_stampa'],process=True)
        pos=next(q for q in man['piatto_geometrico']['items'] if q['id']==p['id'])
        m.apply_translation(pos['traslazione_da_stampa_mm'])
        layout.append({'id':p['id'],'mesh':m,'role':0 if p['id']=='base_appoggi' else 1,'reference':False,'exploded':[0,0,0]})
    render(layout,'assembled',[.6,-1,1.5],views/'piatto.png')
    fig=plt.figure(figsize=(15,11),facecolor=BG)
    fig.text(.04,.96,'BOREO R13 — PROGETTO COMPLETO PETG PRO',fontsize=23,weight='bold',color='#173341')
    fig.text(.04,.923,'Ponte R12 centrato e rinforzato + base arrotondata con logo S9 estruso 2 mm',fontsize=12,color='#526774')
    for box,name,title in [([.02,.49,.47,.38],'assieme_frontale','Assieme: base esterna e giunto M3'),
                           ([.51,.49,.47,.38],'assieme_interno','Dal lato interno: fascia curva da 2 mm'),
                           ([.02,.09,.47,.35],'esploso','Montaggio: due pezzi e ferramenta separata'),
                           ([.51,.09,.47,.35],'piatto','Disposizione di stampa: una copia per pezzo')]:
        ax=fig.add_axes(box);ax.imshow(plt.imread(views/(name+'.png')));ax.axis('off');ax.set_title(title,fontsize=12,color='#173341')
    fig.text(.04,.042,'Colori illustrativi: si stampa con un solo PETG Pro. Grigio = ferramenta metallica, non da stampare.',fontsize=10,color='#526774')
    fig.text(.04,.018,'Assieme per prove di montaggio; tenuta della torcia e comportamento al calore ancora da verificare.',fontsize=10,color='#173341')
    fig.savefig(R/'previews/technical/BOREO_R13_COMPLETO_PETG.png',dpi=140,facecolor=BG);plt.close(fig)
    (R/'previews/technical/metodo.json').write_text(json.dumps({'metodo':'VTK da STL finali riaperti; piatto ricostruito con le trasformazioni del 3MF geometrico.',
      'casco_o_torcia_ricostruiti':False,'file_sha256':{str(p['file'].relative_to(R)):hashlib.sha256(p['file'].read_bytes()).hexdigest() for p in parts}},indent=2)+'\n')
    print(R/'previews/technical/BOREO_R13_COMPLETO_PETG.png')
if __name__=='__main__':main()
