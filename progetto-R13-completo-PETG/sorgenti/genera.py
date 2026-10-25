"""R13: insieme completo PETG Pro, base R10 e ponte centrato R12. Quote mm."""
from pathlib import Path
import hashlib, json, zipfile, importlib.metadata
import xml.etree.ElementTree as ET
import numpy as np
import cadquery as cq
import trimesh
import base_r10, ponte_r12
from geometria_utils import bounds_cad

R=Path(__file__).resolve().parents[1]
NAME='BOREO_R13_COMPLETO_PETG_PRO_ECC2_04'

def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def plate(meshes,path):
    ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
    ET.register_namespace('',ns)
    def sub(p,n,a=None):return ET.SubElement(p,f'{{{ns}}}{n}',a or {})
    model=ET.Element(f'{{{ns}}}model',{'unit':'millimeter'})
    sub(model,'metadata',{'name':'Title'}).text='BOREO R13 COMPLETO PETG - ponte R12 e base R10'
    res=sub(model,'resources');build=sub(model,'build');positions=[]
    for i,((name,m),center) in enumerate(zip(meshes.items(),[(128,90),(128,160)]),1):
        ob=sub(res,'object',{'id':str(i),'type':'model','name':name})
        me=sub(ob,'mesh');ve=sub(me,'vertices');tr=sub(me,'triangles')
        for v in m.vertices:sub(ve,'vertex',{k:f'{v[j]:.8f}' for j,k in enumerate('xyz')})
        for f in m.faces:sub(tr,'triangle',{k:str(f[j]) for j,k in enumerate(['v1','v2','v3'])})
        delta=np.array([*center,0.])-np.r_[m.bounds.mean(0)[:2],m.bounds[0,2]]
        sub(build,'item',{'objectid':str(i),'transform':'1 0 0 0 1 0 0 0 1 '+' '.join(f'{v:.8f}' for v in delta)})
        positions.append({'id':name,'traslazione_da_stampa_mm':delta.tolist()})
    types='<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'
    rel='<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',types);z.writestr('_rels/.rels',rel)
        z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
    return positions

def main():
    bridge,ribs=ponte_r12.build()
    shapes={'ponte_centrato':bridge,'base_appoggi':base_r10.base()}
    out=R/'stampa';refs=R/'sorgenti/assieme';metal=R/'sorgenti/ferramenta-riferimento'
    for d in [out,refs,metal,R/'verifiche']:d.mkdir(parents=True,exist_ok=True)
    parts=[];meshes={};report={};scene=trimesh.Scene();assembly=cq.Assembly()
    for name,shape in shapes.items():
        assert shape.isValid() and len(shape.Solids())==1 and shape.Volume()>0
        dz=-ponte_r12.P['fascia_basso_z'] if name=='ponte_centrato' else 0
        printing=shape.translate((0,0,dz));stem='R13_'+name.upper()+'_PETG'
        for obj,path in [(printing,out/stem),(shape,refs/name)]:
            cq.exporters.export(obj,str(path.with_suffix('.step')))
            cq.exporters.export(obj,str(path.with_suffix('.stl')),tolerance=.04,angularTolerance=.1)
        m=trimesh.load_mesh(out/(stem+'.stl'),process=True)
        assert m.is_watertight and m.is_winding_consistent and m.volume>0
        assert abs(m.bounds[0,2])<1e-6;meshes[name]=m
        parts.append({'id':name,'quantita':1,'materiale':'ELEGOO PETG Pro','solo_prototipo':True,
          'stl_stampa':f'stampa/{stem}.stl','step_stampa':f'stampa/{stem}.step',
          'stl_assieme':f'sorgenti/assieme/{name}.stl','step_assieme':f'sorgenti/assieme/{name}.step',
          'matrice_stampa_da_assieme':[[1,0,0,0],[0,1,0,0],[0,0,1,dz],[0,0,0,1]],
          'bounds_stampa_mm':bounds_cad(printing).tolist(),'bounds_assieme_mm':bounds_cad(shape).tolist()})
        report[name]={'CAD_valido':True,'CAD_solidi':1,'CAD_volume_mm3':shape.Volume(),
                     'STL_volume_mm3':float(m.volume),'STL_dim_mm':m.extents.tolist()}
        a=trimesh.load_mesh(refs/(name+'.stl'),process=True);a.apply_scale(.001)
        a.visual.face_colors=[224,140,67,255] if name=='ponte_centrato' else [39,128,163,255]
        scene.add_geometry(a,node_name=name,geom_name=name);assembly.add(shape,name=name)
    overlap=shapes['base_appoggi'].intersect(bridge).Volume();assert overlap<1e-5
    scene.export(str(refs/'R13_ASSIEME_PLASTICA.glb'))
    assembly.export(str(refs/'R13_ASSIEME_PLASTICA.step'))
    references=[]
    for name,shape in base_r10.hardware().items():
        for ext in ['step','stl']:cq.exporters.export(shape,str(metal/(name+'.'+ext)))
        references.append({'id':name,'stl_assieme':f'sorgenti/ferramenta-riferimento/{name}.stl',
          'step_assieme':f'sorgenti/ferramenta-riferimento/{name}.step','non_stampare':True,'schematico_non_filettato':True})
        a=trimesh.load_mesh(metal/(name+'.stl'),process=True);a.apply_scale(.001);a.visual.face_colors=[160,170,175,255]
        scene.add_geometry(a,node_name=name,geom_name=name);assembly.add(shape,name=name)
    scene.export(str(refs/'R13_ASSIEME_FERRAMENTA_SCHEMATICA.glb'))
    assembly.export(str(refs/'R13_ASSIEME_FERRAMENTA_SCHEMATICA.step'))
    model=out/'R13_COMPLETO_SOLO_GEOMETRIA.3mf';positions=plate(meshes,model)
    manifest={'revisione':'R13_COMPLETO_PETG','unita':'mm','casco_o_torcia_ricostruiti':False,
      'pezzi':parts,'riferimenti':references,'piatto_geometrico':{'file':str(model.relative_to(R)),
      'numero_pezzi':2,'unita':'mm','items':positions},
      'assieme':{'step':'sorgenti/assieme/R13_ASSIEME_PLASTICA.step','glb':'sorgenti/assieme/R13_ASSIEME_PLASTICA.glb','unita_glb':'m'},
      'scopo':'Progetto completo per stampa di prova PETG Pro. Base R10 e ponte R12 invariati. Montaggio/carico/calore aperti.'}
    save(R/'sorgenti/manifest.json',manifest)
    files=[model,*[R/p[k] for p in parts for k in ['stl_stampa','step_stampa','stl_assieme','step_assieme']],*refs.glob('*.glb'),*refs.glob('R13*.step')]
    save(R/'verifiche/generazione.json',{'revisione':'R13','pezzi':report,'intersezione_assieme_mm3':overlap,
      'rinforzi':len(ribs),'dipendenze':{n:importlib.metadata.version(n) for n in ['cadquery','trimesh','numpy']},
      'file_sha256':{str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}})
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
