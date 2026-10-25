"""Anteprime R04 dai file STL riaperti. Quote in mm, parti originali schematiche."""
from pathlib import Path
import os,json,hashlib,base64,zlib
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
import numpy as np
import trimesh
import vtk
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BG=np.array([245,247,248])/255
COLORS=[[39,128,163],[219,135,80],[143,153,162],[63,76,88]]

def ruolo(ident,is_reference):
    if not is_reference:return 0 if 'base' in ident.lower() else 1
    return 3 if any(k in ident.lower() for k in ['torcia','lampada','corpo']) else 2

def esplosione(ident,role):
    name=ident.lower()
    if role==0:return [0,0,0]
    if role==1:return [-16 if any(k in name for k in ['sx','sinistr']) else 16,-28,0]
    if 'farfalla' in name:return [0,23,0]
    if role==3:return [0,65,0]
    if any(k in name for k in ['u_metal','staffa','u_original']):return [0,45,0]
    return [0,12,0]

def carica():
    manifest=json.loads((ROOT/'sorgenti/manifest.json').read_text())
    result=[]
    for ref,key in [(False,'pezzi'),(True,'riferimenti')]:
        for item in manifest[key]:
            ident=item['id'];file=ROOT/item['stl_assieme']
            mesh=trimesh.load_mesh(file,process=True)
            role=ruolo(ident,ref)
            result.append({'id':ident,'mesh':mesh,'role':role,'exploded':esplosione(ident,role),'file':file,'reference':ref})
    return result

def attore(mesh,role,offset):
    points=vtk.vtkPoints();points.SetData(numpy_to_vtk(mesh.vertices+offset,deep=True))
    cells=vtk.vtkCellArray();raw=np.column_stack((np.full(len(mesh.faces),3),mesh.faces)).astype(np.int64).ravel()
    cells.SetCells(len(mesh.faces),numpy_to_vtkIdTypeArray(raw,deep=True))
    poly=vtk.vtkPolyData();poly.SetPoints(points);poly.SetPolys(cells)
    normals=vtk.vtkPolyDataNormals();normals.SetInputData(poly);normals.SplittingOn();normals.SetFeatureAngle(35)
    mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(normals.GetOutputPort())
    actor=vtk.vtkActor();actor.SetMapper(mapper);prop=actor.GetProperty()
    prop.SetColor(*(np.array(COLORS[role])/255));prop.SetInterpolationToPhong();prop.SetAmbient(.3);prop.SetDiffuse(.7);prop.SetSpecular(.12);prop.SetSpecularPower(30)
    return actor

def render(parts,mode,direction,dest):
    renderer=vtk.vtkRenderer();renderer.SetBackground(*BG)
    all_vertices=[]
    for c in parts:
        if mode=='support' and c['reference']:continue
        offset=np.array(c['exploded'] if mode=='exploded' else [0,0,0])
        renderer.AddActor(attore(c['mesh'],c['role'],offset));all_vertices.append(c['mesh'].vertices+offset)
    vertices=np.vstack(all_vertices);center=(vertices.max(axis=0)+vertices.min(axis=0))/2
    direction=np.asarray(direction,dtype=float);direction/=np.linalg.norm(direction)
    right=np.cross([0,0,1],direction);right/=np.linalg.norm(right);up=np.cross(direction,right)
    relative=vertices-center;xx=relative@right;yy=relative@up
    focus=center+right*(xx.max()+xx.min())/2+up*(yy.max()+yy.min())/2
    camera=renderer.GetActiveCamera();camera.SetFocalPoint(*focus);camera.SetPosition(*(focus+direction*500));camera.SetViewUp(*up);camera.ParallelProjectionOn()
    camera.SetParallelScale(max(np.ptp(yy)/2,np.ptp(xx)/(2*1.6))*1.12)
    window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1);window.SetMultiSamples(8);window.SetSize(1600,1000);window.AddRenderer(renderer);renderer.ResetCameraClippingRange();window.Render()
    capture=vtk.vtkWindowToImageFilter();capture.SetInput(window);capture.SetInputBufferTypeToRGB();capture.ReadFrontBufferOff();capture.Update()
    writer=vtk.vtkPNGWriter();writer.SetFileName(str(dest));writer.SetInputConnection(capture.GetOutputPort());writer.Write();window.Finalize()

def main():
    parts=carica();out=ROOT/'anteprime';views=out/'viste';views.mkdir(parents=True,exist_ok=True)
    configurations=[('esploso','exploded',[1.2,1.5,1.1]),('assemblato','assembled',[1.1,1.6,.8]),('supporto','support',[1.1,1.5,.9]),('retro','support',[-1,-1.5,.8])]
    for name,mode,direction in configurations:render(parts,mode,direction,views/f'{name}.png')
    fig=plt.figure(figsize=(16,11),facecolor=BG)
    fig.text(.035,.955,'BOREO / SUPERKIKKO2 - BOZZA R04',fontsize=22,weight='bold',color='#173341')
    fig.text(.035,.918,'Base portafarfalla e due fermi separati - quote assunte - nessun casco ricostruito',fontsize=12,color='#526774')
    panels=[([.025,.49,.46,.38],'esploso','Esploso: fermi, base, farfalla, U e torcia'),([.515,.49,.46,.38],'assemblato','Assemblato con parti originali schematiche'),([.025,.095,.46,.34],'supporto','Il nuovo supporto: base e due fermi'),([.515,.095,.46,.34],'retro','Dal retro: superfici interne e collegamenti')]
    for box,name,title in panels:
        ax=fig.add_axes(box);ax.imshow(plt.imread(views/f'{name}.png'));ax.axis('off');ax.set_title(title,fontsize=11,color='#173341',pad=7)
    fig.text(.035,.061,'Blu: base esterna. Arancio: fermi interni, soltanto dime. Grigio: originali e ferramenta schematici.',fontsize=10,color='#526774')
    fig.text(.035,.034,'BOZZA DI FORMA - accoppiamento, resistenza, calore, immersione e stampa non verificati.',fontsize=10,weight='bold',color='#173341')
    fig.savefig(out/'BOZZA_R04_anteprima.png',dpi=160,facecolor=BG);plt.close(fig)
    data={'revision':'R04','units':'mm','all_dimensions_assumed':True,'components':[]}
    for c in parts:
        data['components'].append({'id':c['id'],'role':c['role'],'exploded':c['exploded'],'vertices':np.round(c['mesh'].vertices,4).tolist(),'faces':c['mesh'].faces.tolist()})
    packed=json.dumps(data,separators=(',',':'))
    (out/'geometria_visualizzazione.json').write_text(packed)
    template=(ROOT/'sorgenti/visualizzatore.template.html').read_text()
    inline=ROOT.parent/'previews/legacy-visualizations/boreo-portafarfalla-r04.html';inline.parent.mkdir(parents=True,exist_ok=True)
    encoded=base64.b64encode(zlib.compress(packed.encode(),9)).decode('ascii')
    inline.write_text(template.replace('__MESH_DATA_ZLIB__',encoded))
    assert inline.stat().st_size<1_000_000,'Anteprima inline supera1MB: semplificare solo riferimenti visivi.'
    report={'metodo':'STL finali riaperti; VTK Z-buffer per PNG e WebGL per vista interattiva','componenti':[{k:v for k,v in c.items() if k not in ['mesh','file']}|{'stl':str(c['file'].relative_to(ROOT)),'sha256':hashlib.sha256(c['file'].read_bytes()).hexdigest()} for c in parts], 'casco_ricostruito':False,'riferimenti_originali_schematici':True,'inline_byte':inline.stat().st_size,'inline_sha256':hashlib.sha256(inline.read_bytes()).hexdigest(),'versioni':{'vtk':vtk.vtkVersion.GetVTKVersion(),'trimesh':trimesh.__version__}}
    (ROOT/'verifiche').mkdir(exist_ok=True)
    (ROOT/'verifiche/anteprime.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'anteprima':str(out/'BOZZA_R04_anteprima.png'),'inline':str(inline),'componenti':len(parts),'inline_byte':inline.stat().st_size},indent=2))

if __name__=='__main__':main()
