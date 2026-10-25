"""Dima rapida R06: due pezzi leggeri, senza ferramenta o parti della torcia."""
from pathlib import Path
import json, math, hashlib, zipfile, importlib.metadata
import xml.etree.ElementTree as ET
import cadquery as cq
import numpy as np
import trimesh
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'sorgenti/parametri.json').read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def box(x,z,y,w,h,d):return cq.Workplane('XY',origin=(x,y,z)).box(w,d,h,centered=(True,False,True)).val()
def arc(r,t,a,b,z,h,fillet=0):
    cx,cy=P['centro_curva_xy'];m=(a+b)/2
    def pt(rr,th):return (cx+rr*math.sin(th),cy+rr*math.cos(th))
    w=(cq.Workplane('XY',origin=(0,0,z)).moveTo(*pt(r,a)).threePointArc(pt(r,m),pt(r,b))
       .lineTo(*pt(r+t,b)).threePointArc(pt(r+t,m),pt(r+t,a)).close().extrude(h))
    if fillet:w=w.edges('|Z').fillet(fillet)
    return w.val()
def bbox(s):
    b=Bnd_Box();BRepBndLib.AddOptimal_s(s.wrapped,b,False,False);v=list(b.Get())
    return [[round(x,6) for x in v[:3]],[round(x,6) for x in v[3:]]]
def base():
    r=P['base_raggio_interno'];theta=math.asin(P['base_corda_interna']/(2*r))
    shell=arc(r,P['base_spessore_radiale'],-theta,theta,0,P['base_altezza'],1.2)
    bottom=P['base_bordo_inferiore_altezza']
    frame=shell.cut(box(0,(bottom+60)/2,-50,P['base_finestra_centrale_larghezza'],60-bottom,80))
    g=P['gioco_sede_per_lato'];w=P['terminale_larghezza']+2*g;h=P['terminale_altezza']+2*g
    for x in P['assi_terminali_x']:
        # Allargamento locale per il passaggio, senza sedi dadi o bulloni.
        frame=frame.fuse(shell.intersect(box(x,P['asse_terminali_z']+.5,-50,14,19,80)))
        # Tetto a45gradi: mantiene il foro passante senza un ponte orizzontale10.7mm.
        z=P['asse_terminali_z'];a=w/2;b=h/2
        cut=(cq.Workplane('XZ',origin=(x,-50,z)).polyline([(-a,-b),(a,-b),(a,b),(0,b+a),(-a,b)]).close().extrude(-80).val())
        frame=frame.cut(cut)
    return frame.clean()
def ponte():
    r=P['raggio_interno_ponte'];t=P['spessore_radiale_ponte'];rm=r+t/2
    a=math.asin(P['assi_terminali_x'][0]/rm)-P['estensione_arco_per_estremita']/rm
    b=math.asin(P['assi_terminali_x'][1]/rm)+P['estensione_arco_per_estremita']/rm
    z=P['asse_terminali_z'];h=P['altezza_ponte'];shape=arc(r,t,a,b,z-h/2,h,.3)
    cx,cy=P['centro_curva_xy'];cyl=cq.Solid.makeCylinder(r,100,cq.Vector(cx,cy,-20),cq.Vector(0,0,1))
    for x in P['assi_terminali_x']:
        tongue=(cq.Workplane('XY',origin=(x,-55,z)).box(P['terminale_larghezza'],55+P['terminale_fronte_y'],P['terminale_altezza'],centered=(True,False,True)).edges('|Z').fillet(P['terminale_raccordo']).val())
        shape=shape.fuse(tongue.cut(cyl))
    return shape.clean()
def plate(meshes,path):
    ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
    def sub(p,n,a=None):return ET.SubElement(p,f'{{{ns}}}{n}',a or {})
    model=ET.Element(f'{{{ns}}}model',{'unit':'millimeter'});sub(model,'metadata',{'name':'Title'}).text='BOREO R06 DIMA RAPIDA - due pezzi'
    res=sub(model,'resources');build=sub(model,'build');placements=[]
    for i,((name,m),center) in enumerate(zip(meshes.items(),[[128,95],[128,155]]),1):
        ob=sub(res,'object',{'id':str(i),'type':'model','name':name});me=sub(ob,'mesh');ve=sub(me,'vertices');tr=sub(me,'triangles')
        for v in m.vertices:sub(ve,'vertex',{k:f'{v[j]:.8f}' for j,k in enumerate('xyz')})
        for f in m.faces:sub(tr,'triangle',{k:str(f[j]) for j,k in enumerate(['v1','v2','v3'])})
        delta=np.array([*center,0.])-np.r_[m.bounds.mean(0)[:2],m.bounds[0,2]]
        sub(build,'item',{'objectid':str(i),'transform':'1 0 0 0 1 0 0 0 1 '+' '.join(f'{v:.8f}' for v in delta)})
        placements.append({'id':name,'traslazione_da_stampa_mm':delta.tolist()})
    types='<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'
    rel='<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:z.writestr('[Content_Types].xml',types);z.writestr('_rels/.rels',rel);z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
    return placements
def main():
    out=ROOT/'stampa';out.mkdir(parents=True,exist_ok=True);refs=ROOT/'sorgenti/assieme';refs.mkdir(exist_ok=True)
    shapes={'base_cornice':base(),'ponte_terminale':ponte()};meshes={};items=[];report={};scene=trimesh.Scene();assembly=cq.Assembly()
    for name,s in shapes.items():
        assert s.isValid() and len(s.Solids())==1 and s.Volume()>0,name
        delta=[0,0,0] if name=='base_cornice' else [0,0,-21]
        printing=s.translate(tuple(delta));stem='R06_'+name.upper()+'_SOLO_DIMA'
        for obj,path in [(printing,out/stem),(s,refs/name)]:
            cq.exporters.export(obj,str(path.with_suffix('.step')))
            cq.exporters.export(obj,str(path.with_suffix('.stl')),tolerance=.06,angularTolerance=.1)
        m=trimesh.load_mesh(out/(stem+'.stl'),process=True);assert m.is_watertight and m.is_winding_consistent and m.volume>0
        assert np.all(m.area_faces>1e-12) and abs(m.bounds[0,2])<1e-6
        meshes[name]=m
        items.append({'id':name,'quantita':1,'solo_dima_forma':True,'stl_stampa':f'stampa/{stem}.stl','step_stampa':f'stampa/{stem}.step','stl_assieme':f'sorgenti/assieme/{name}.stl','step_assieme':f'sorgenti/assieme/{name}.step','matrice_stampa_da_assieme':[[1,0,0,delta[0]],[0,1,0,delta[1]],[0,0,1,delta[2]],[0,0,0,1]],'bounds_stampa_mm':bbox(printing),'bounds_assieme_mm':bbox(s)})
        report[name]={'CAD_valido':True,'volume_CAD_mm3':s.Volume(),'triangoli':len(m.faces),'dimensioni_STL_mm':m.extents.tolist(),'volume_STL_mm3':m.volume}
        a=trimesh.load_mesh(refs/(name+'.stl'),process=True);a.apply_scale(.001);a.visual.face_colors=[39,128,163,255] if name=='base_cornice' else [219,135,80,255];scene.add_geometry(a,node_name=name,geom_name=name)
        assembly.add(s,name=name)
    overlap=shapes['base_cornice'].intersect(shapes['ponte_terminale']).Volume();assert overlap<1e-6
    scene.export(str(refs/'R06_ASSIEME.glb'));assembly.export(str(refs/'R06_ASSIEME.step'))
    mf=out/'R06_DUE_PEZZI_SOLO_GEOMETRIA.3mf';placements=plate(meshes,mf)
    manifest={'revisione':'R06_DIMA_RAPIDA','unita_assieme':'mm','tutte_quote_ASSUNTE':True,'casco_presente':False,'pezzi':items,'riferimenti':[],
              'piatto_geometrico':{'file':str(mf.relative_to(ROOT)),'numero_pezzi':2,'unita':'mm','items':placements},
              'assieme':{'step':'sorgenti/assieme/R06_ASSIEME.step','glb':'sorgenti/assieme/R06_ASSIEME.glb','unita_glb':'m'},
              'scopo':P['scopo'],'differenze_R05':['Ponte e terminali alti4mm; terminali10x4 senza viti.','Base ridotta a cornice aperta con ingombro esterno originale, senza sede farfalla.','Sedi passanti con tetto inclinato, gioco0.35mm/lato; nessun serraggio.']}
    (ROOT/'sorgenti/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    report={'pezzi':report,'intersezione_assieme_mm3':overlap,'sha256':{str(p.relative_to(ROOT)):sha(p) for p in [*out.glob('*'),*refs.glob('*')]},'dipendenze':{n:importlib.metadata.version(n) for n in ['cadquery','trimesh','numpy']}}
    (ROOT/'sorgenti/report_generazione.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['pezzi'],indent=2))
if __name__=='__main__':main()
