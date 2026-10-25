"""Anteprime della bozza R03 dai soli file finali esportati. Unita: mm."""
from pathlib import Path
import os, json, math
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'.cache/matplotlib'))
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from render_vtk import main as render_vtk

BG = '#f5f7f8'
INK = '#173341'
BLUE = '#2780a3'
ORANGE = '#db8750'

def main():
    out = ROOT/'anteprime'
    out.mkdir(parents=True, exist_ok=True)
    mesh = trimesh.load_mesh(ROOT/'stampa/BOZZA_R03_NON_USO.stl', process=True)
    render_vtk()
    p=json.loads((ROOT/'sorgenti/parametri_assunti.json').read_text())
    val=lambda group,key:p[group][key]['valore']
    radius=val('ponte','raggio_centrolinea_mm');chord=val('ponte','corda_centrolinea_mm');wall=val('ponte','spessore_radiale_mm')
    height=val('ponte','altezza_mm');clearance=val('orecchie','luce_interna_mm');hole=val('orecchie','diametro_fori_mm');hole_y=val('orecchie','asse_fori_y_mm')
    cy = -math.sqrt(radius*radius-(chord/2)**2)
    cent = mesh.triangles_center
    radial = np.sqrt(cent[:,0]**2+(cent[:,1]-cy)**2)
    bridge = (np.abs(radial-radius)<wall/2+.12) & (np.abs(cent[:,0])<=chord/2+.7)
    colors = np.where(bridge[:,None], matplotlib.colors.to_rgb(BLUE), matplotlib.colors.to_rgb(ORANGE))
    def model(box,name,title):
        ax=fig.add_axes(box)
        ax.imshow(plt.imread(out/'viste_vtk'/f'{name}.png'))
        ax.set_axis_off();ax.set_title(title,fontsize=11,color=INK,pad=8)
    fig=plt.figure(figsize=(16,10),facecolor=BG)
    fig.text(.04,.944,'BOREO / SUPERKIKKO2 - BOZZA R03',fontsize=23,weight='bold',color=INK)
    fig.text(.04,.902,'Forma indicativa - quote assunte - accoppiamento e tenuta non verificati',fontsize=12,color='#526774')
    model([.025,.285,.59,.55],'iso','Unico corpo: ponte curvo interno e due bracci esterni')
    model([.65,.55,.31,.27],'alto','Dall’alto: bracci convergenti verso la torcia')
    model([.65,.28,.31,.22],'lato',f'Di lato: foro provvisorio da {hole:g} mm')
    # Radial cross-section enlargement: clearly show low-profile bridge intent.
    ax=fig.add_axes([.065,.12,.47,.105]);ax.set_facecolor(BG)
    ax.add_patch(plt.Rectangle((0,0),wall,height,facecolor=BLUE,edgecolor='none'))
    ax.annotate('',xy=(0,-1.1),xytext=(wall,-1.1),arrowprops=dict(arrowstyle='<->',color=INK,lw=1))
    ax.text(wall/2,-2.2,f'{wall:g} mm assunti',ha='center',va='top',fontsize=10,color=INK)
    ax.text(wall+1.3,height/2,f'Sezione ingrandita del ponte\nAltezza {height:g} mm; spessore radiale {wall:g} mm',va='center',fontsize=10,color=INK)
    ax.set(xlim=(-.8,16),ylim=(-4,15));ax.axis('off')
    fig.text(.65,.182,'QUOTE DI PARTENZA',fontsize=10,weight='bold',color=INK)
    fig.text(.65,.139,f'Ponte: corda {chord:g} mm / raggio {radius:g} mm\nLuce interna fra orecchie: {clearance:g} mm\nAsse fori: {hole_y:g} mm avanti dagli estremi del ponte',fontsize=10,color='#526774',linespacing=1.55,va='top')
    fig.text(.04,.047,'Colori esplicativi: blu = ponte interno, arancio = bracci. Nessun casco 3D ricostruito.',fontsize=10,color='#526774')
    fig.text(.04,.023,'BOZZA DI FORMA: non utilizzare come supporto della torcia in attivita. Nessuna prova fisica eseguita.',fontsize=10,weight='bold',color=INK)
    fig.savefig(out/'BOZZA_R03_anteprima.png',dpi=160,facecolor=BG)
    plt.close(fig)
    # Exact exported geometry with display-only region colors.
    glb_mesh=mesh.copy()
    glb_mesh.visual.face_colors=np.column_stack((np.clip(colors*255,0,255).astype(np.uint8),np.full(len(colors),255,dtype=np.uint8)))
    glb_mesh.apply_scale(.001)
    glb_mesh.metadata['units']='meters'
    glb_mesh.export(out/'BOZZA_R03_colori_esplicativi.glb')
    data={'vertices':np.round(mesh.vertices,4).tolist(),'faces':mesh.faces.tolist(),'bridge':bridge.astype(int).tolist(),
          'bounds':mesh.bounds.tolist(),'units':'mm','revision':'R03','status':'BOZZA_DI_FORMA_NON_USO',
          'all_dimensions_assumed':True}
    (out/'geometria_visualizzazione.json').write_text(json.dumps(data,separators=(',',':')))
    inline_out=ROOT.parent/'previews/legacy-visualizations/boreo-superkikko2-bozza-r03.html'
    inline_out.parent.mkdir(parents=True,exist_ok=True)
    template=(ROOT/'sorgenti/visualizzatore.template.html').read_text()
    inline_out.write_text(template.replace('__MESH_DATA__',json.dumps(data,separators=(',',':'))))
    print(json.dumps({'png':str(out/'BOZZA_R03_anteprima.png'),'dimensions_mm':mesh.extents.tolist(),'faces':len(mesh.faces)},indent=2))

if __name__=='__main__':main()
