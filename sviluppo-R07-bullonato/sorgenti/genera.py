"""R07: ponte verso alto, passaggi alleggeriti e giunto esterno M3. Quote mm."""
from pathlib import Path
import json,math,hashlib,zipfile,importlib.metadata
import xml.etree.ElementTree as ET
import cadquery as cq
import numpy as np
import trimesh
from geometria_utils import bounds_cad
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'sorgenti/parametri.json').read_text())
def arc(r,t,a,b,z,h,fillet=0):
 c=P['centro_curva_xy'];m=(a+b)/2
 def pt(rr,th):return (c[0]+rr*math.sin(th),c[1]+rr*math.cos(th))
 w=cq.Workplane('XY',origin=(0,0,z)).moveTo(*pt(r,a)).threePointArc(pt(r,m),pt(r,b)).lineTo(*pt(r+t,b)).threePointArc(pt(r+t,m),pt(r+t,a)).close().extrude(h)
 if fillet:w=w.edges('|Z').fillet(fillet)
 return w.val()
def block(x,y,z,w,d,h,fillet=0):
 s=cq.Workplane('XY',origin=(x,y,z)).box(w,d,h,centered=(True,False,False))
 if fillet:s=s.edges('|Z').fillet(fillet)
 return s.val()
def cyl(x,y,z,d,h):return cq.Solid.makeCylinder(d/2,h,cq.Vector(x,y,z),cq.Vector(0,0,1))
def hexagon(x,y,z,af,h):return cq.Workplane('XY',origin=(x,y,z)).polygon(6,af/math.cos(math.pi/6)).extrude(h).val()
def ponte():
 r=P['raggio_interno_ponte'];t=P['spessore_radiale_ponte'];rm=r+t/2
 a=math.asin(P['assi_terminali_x'][0]/rm)-P['estensione_arco_per_estremita']/rm
 b=math.asin(P['assi_terminali_x'][1]/rm)+P['estensione_arco_per_estremita']/rm
 shape=arc(r,t,a,b,P['ponte_basso_z'],P['altezza_ponte'],.3)
 c=P['centro_curva_xy'];inside=cq.Solid.makeCylinder(r,100,cq.Vector(*c,-20),cq.Vector(0,0,1))
 for x in P['assi_terminali_x']:
  tongue=block(x,-55,P['terminale_basso_z'],P['terminale_larghezza'],55+P['terminale_fronte_y'],P['terminale_altezza'],P['terminale_raccordo']).cut(inside)
  # Foro della vite solo nel tratto esterno; lati del terminale raccordati.
  tongue=tongue.cut(cyl(x,P['fissaggio_asse_y'],19,P['fissaggio_diametro'],10))
  shape=shape.fuse(tongue)
 return shape.clean()
def base():
 r=P['base_raggio_interno'];a=math.asin(P['base_corda_interna']/(2*r))
 shape=arc(r,P['base_spessore_radiale'],-a,a,0,P['base_altezza'],1.2)
 for x in P['assi_terminali_x']:
  boss=block(x,P['boss_retro_y'],P['boss_basso_z'],P['boss_larghezza'],P['boss_fronte_y']-P['boss_retro_y'],P['boss_alto_z']-P['boss_basso_z'],1)
  c=P['centro_curva_xy'];inside=cq.Solid.makeCylinder(r,100,cq.Vector(*c,-20),cq.Vector(0,0,1))
  shape=shape.fuse(boss)
  z=P['asse_terminali_z'];a=(P['terminale_larghezza']+2*P['gioco_sede_per_lato'])/2;b=(P['terminale_altezza']+2*P['gioco_sede_per_lato'])/2
  roof=cq.Workplane('XZ',origin=(x,-50,z)).polyline([(-a,-b),(a,-b),(a,b),(0,b+a),(-a,b)]).close().extrude(-55).val()
  shape=shape.cut(roof)
  shape=shape.cut(cyl(x,P['fissaggio_asse_y'],8,P['fissaggio_diametro'],20))
  shape=shape.cut(hexagon(x,P['fissaggio_asse_y'],P['boss_basso_z']-.01,P['dado_tasca_chiave'],P['dado_tasca_profondita']+.01))
 # Un taglio unico ripristina la curva interna e rimuove le sporgenze dei rinforzi.
 inside=cq.Solid.makeCylinder(r+P['offset_rifilo_curva_base'],100,cq.Vector(*c,-20),cq.Vector(0,0,1))
 shape=shape.cut(inside)
 return shape.clean()
def hardware():
 refs={};top=P['terminale_basso_z']+P['terminale_altezza'];washer_top=top+P['rondella_spessore']
 for i,x in enumerate(P['assi_terminali_x'],1):
  y=P['fissaggio_asse_y'];screw=cyl(x,y,washer_top-P['vite_lunghezza'],3,P['vite_lunghezza']).fuse(cyl(x,y,washer_top,5.5,3))
  washer=cyl(x,y,top,7,.5).cut(cyl(x,y,top-.1,3.2,.7))
  nz=P['boss_basso_z']+P['dado_tasca_profondita']-P['dado_altezza'];nut=hexagon(x,y,nz,5.5,4).cut(cyl(x,y,nz-.1,3,4.2))
  refs[f'vite_M3x16_{i}']=screw;refs[f'rondella_M3_{i}']=washer;refs[f'dado_autobloccante_M3_{i}']=nut
 return refs

def plate(meshes,path):
 ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
 def sub(p,n,a=None):return ET.SubElement(p,f'{{{ns}}}{n}',a or {})
 model=ET.Element(f'{{{ns}}}model',{'unit':'millimeter'});sub(model,'metadata',{'name':'Title'}).text='BOREO R07 PROTOTIPO BULLONATO - 2 pezzi plastici'
 res=sub(model,'resources');build=sub(model,'build');placements=[]
 for i,((name,m),center) in enumerate(zip(meshes.items(),[[128,95],[128,165]]),1):
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
 out=ROOT/'stampa';refs=ROOT/'sorgenti/assieme';metal=ROOT/'sorgenti/ferramenta-riferimento'
 shapes={'base_grezza':base(),'ponte_terminale':ponte()};meshes={};items=[];report={};scene=trimesh.Scene();assembly=cq.Assembly()
 for name,s in shapes.items():
  assert s.isValid() and len(s.Solids())==1 and s.Volume()>0,name
  delta=[0,0,0] if name=='base_grezza' else [0,0,-P['ponte_basso_z']]
  printing=s.translate(tuple(delta));stem='R07_'+name.upper()+'_PROTOTIPO_PLA'
  for obj,path in [(printing,out/stem),(s,refs/name)]:
   cq.exporters.export(obj,str(path.with_suffix('.step')));cq.exporters.export(obj,str(path.with_suffix('.stl')),tolerance=.04,angularTolerance=.1)
  m=trimesh.load_mesh(out/(stem+'.stl'),process=True);assert m.is_watertight and m.is_winding_consistent and m.volume>0
  assert np.all(m.area_faces>1e-12) and abs(m.bounds[0,2])<1e-6;meshes[name]=m
  items.append({'id':name,'quantita':1,'solo_prototipo':True,'stl_stampa':f'stampa/{stem}.stl','step_stampa':f'stampa/{stem}.step','stl_assieme':f'sorgenti/assieme/{name}.stl','step_assieme':f'sorgenti/assieme/{name}.step','matrice_stampa_da_assieme':[[1,0,0,delta[0]],[0,1,0,delta[1]],[0,0,1,delta[2]],[0,0,0,1]],'bounds_stampa_mm':bounds_cad(printing).tolist(),'bounds_assieme_mm':bounds_cad(s).tolist()})
  report[name]={'CAD_valido':True,'volume_CAD_mm3':s.Volume(),'triangoli':len(m.faces),'dimensioni_STL_mm':m.extents.tolist(),'volume_STL_mm3':m.volume}
  a=trimesh.load_mesh(refs/(name+'.stl'),process=True);a.apply_scale(.001);a.visual.face_colors=[39,128,163,255] if name=='base_grezza' else [219,135,80,255];scene.add_geometry(a,node_name=name,geom_name=name);assembly.add(s,name=name)
 overlap=shapes['base_grezza'].intersect(shapes['ponte_terminale']).Volume();assert overlap<1e-5,overlap
 scene.export(str(refs/'R07_ASSIEME_PLASTICA.glb'));assembly.export(str(refs/'R07_ASSIEME_PLASTICA.step'))
 reference_items=[]
 for name,s in hardware().items():
  cq.exporters.export(s,str(metal/(name+'.step')));cq.exporters.export(s,str(metal/(name+'.stl')),tolerance=.04,angularTolerance=.1)
  reference_items.append({'id':name,'stl_assieme':f'sorgenti/ferramenta-riferimento/{name}.stl','step_assieme':f'sorgenti/ferramenta-riferimento/{name}.step','non_stampare':True,'schematico_non_filettato':True})
  a=trimesh.load_mesh(metal/(name+'.stl'),process=True);a.apply_scale(.001);a.visual.face_colors=[160,170,175,255];scene.add_geometry(a,node_name=name,geom_name=name);assembly.add(s,name=name)
 scene.export(str(refs/'R07_ASSIEME_CON_FERRAMENTA_SCHEMATICA.glb'));assembly.export(str(refs/'R07_ASSIEME_CON_FERRAMENTA_SCHEMATICA.step'))
 mf=out/'R07_DUE_PEZZI_SOLO_GEOMETRIA.3mf';placements=plate(meshes,mf)
 manifest={'revisione':'R07_BULLONATO_SVILUPPO','unita_assieme':'mm','casco_presente':False,'pezzi':items,'riferimenti':reference_items,'piatto_geometrico':{'file':str(mf.relative_to(ROOT)),'numero_pezzi':2,'unita':'mm','items':placements},'assieme':{'step':'sorgenti/assieme/R07_ASSIEME_PLASTICA.step','glb':'sorgenti/assieme/R07_ASSIEME_PLASTICA.glb','unita_glb':'m'},'scopo':P['scopo']}
 (ROOT/'sorgenti/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 report={'pezzi':report,'intersezione_assieme_mm3':overlap,'sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [*out.glob('*'),*refs.glob('*'),*metal.glob('*')]},'dipendenze':{n:importlib.metadata.version(n) for n in ['cadquery','trimesh','numpy']}}
 (ROOT/'sorgenti/report_generazione.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['pezzi'],indent=2))
if __name__=='__main__':main()
