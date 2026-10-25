"""R12: ponte centrato, nervature esterne dalla fascia ai bracci. Quote mm."""
from pathlib import Path
import math,json,hashlib,zipfile,importlib.metadata
import xml.etree.ElementTree as ET
import cadquery as cq
import numpy as np
import trimesh
from geometria_utils import bounds_cad
R=Path(__file__).resolve().parents[1];P=json.loads((R/'sorgenti/parametri.json').read_text())
STEM='R12_PONTE_CENTRATO_RINFORZATO_PLA'
def block(x,y,z,w,d,h,fillet=0):
 s=cq.Workplane('XY',origin=(x,y,z)).box(w,d,h,centered=(True,False,False))
 if fillet:s=s.edges('|Z').fillet(fillet)
 return s.val()
def ring(r,t,z,h):
 c=P['centro_curva_xy'];rr=P['riferimento_angolare_raggio'];a=math.asin(42/rr)+P['estensione_angolo_mm']/rr
 def pt(radius,theta):return (c[0]+radius*math.sin(theta),c[1]+radius*math.cos(theta))
 return (cq.Workplane('XY',origin=(0,0,z)).moveTo(*pt(r,-a)).threePointArc(pt(r,0),pt(r,a)).lineTo(*pt(r+t,a)).threePointArc(pt(r+t,0),pt(r+t,-a)).close().extrude(h).edges('|Z').fillet(.3).val())
def build():
 r=P['raggio_interno'];c=P['centro_curva_xy'];shape=ring(r,P['spessore_fascia'],P['fascia_basso_z'],P['fascia_altezza'])
 inner=cq.Solid.makeCylinder(r,100,cq.Vector(*c,-20),cq.Vector(0,0,1));outer=cq.Solid.makeCylinder(P['raggio_esterno'],100,cq.Vector(*c,-20),cq.Vector(0,0,1))
 ribs=[]
 for x in P['assi_x']:
  tongue=block(x,-55,P['aletta_basso_z'],P['aletta_larghezza'],55+P['aletta_fronte_y'],P['aletta_spessore'],P['aletta_raccordo']).cut(inner)
  hole=cq.Solid.makeCylinder(P['foro_diametro']/2,10,cq.Vector(x,P['foro_y'],19),cq.Vector(0,0,1));tongue=tongue.cut(hole)
  # Nervatura sul lato dei bracci: si lega alla fascia e corre verso la torcia.
  # Taglio del cilindro interno: nessun tallone o rinforzo sporge verso la testa.
  w=P['rinforzo_larghezza'];root_y=c[1]+math.sqrt(P['raggio_esterno']**2-(abs(x)+w/2)**2)-.8
  tip_y=c[1]+math.sqrt(P['raggio_esterno']**2-x*x)+P['rinforzo_lunghezza_esterna']
  z=P['aletta_basso_z'];h=P['rinforzo_altezza'];tip=P['rinforzo_spessore_punta']
  rib=(cq.Workplane('YZ',origin=(x-w/2,0,0)).polyline([(root_y,z+.15),(tip_y,z+.15),(tip_y,z-tip),(root_y,z-h)]).close().extrude(w).val()).cut(inner)
  shape=shape.fuse(tongue).fuse(rib);ribs.append(rib)
 return shape.clean(),ribs

def three_mf(m,path):
 ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
 def sub(p,n,a=None):return ET.SubElement(p,f'{{{ns}}}{n}',a or {})
 model=ET.Element(f'{{{ns}}}model',{'unit':'millimeter'});sub(model,'metadata',{'name':'Title'}).text='BOREO R12 - ponte centrato rinforzato - un solo provino PLA'
 res=sub(model,'resources');ob=sub(res,'object',{'id':'1','type':'model','name':STEM});me=sub(ob,'mesh');ve=sub(me,'vertices');tr=sub(me,'triangles')
 for v in m.vertices:sub(ve,'vertex',{k:f'{v[j]:.8f}' for j,k in enumerate('xyz')})
 for f in m.faces:sub(tr,'triangle',{k:str(f[j]) for j,k in enumerate(['v1','v2','v3'])})
 delta=np.array([128,128,0])-np.r_[m.bounds.mean(0)[:2],m.bounds[0,2]]
 build=sub(model,'build');sub(build,'item',{'objectid':'1','transform':'1 0 0 0 1 0 0 0 1 '+' '.join(f'{v:.8f}' for v in delta)})
 types='<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'
 rel='<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:z.writestr('[Content_Types].xml',types);z.writestr('_rels/.rels',rel);z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
 return delta.tolist()

def main():
 shape,ribs=build();assert shape.isValid() and len(shape.Solids())==1 and shape.Volume()>0
 printing=shape.translate((0,0,-P['fascia_basso_z']));out=R/'stampa';refs=R/'sorgenti/assieme'
 for obj,path in [(printing,out/STEM),(shape,refs/'ponte')]:
  cq.exporters.export(obj,str(path.with_suffix('.step')));cq.exporters.export(obj,str(path.with_suffix('.stl')),tolerance=.04,angularTolerance=.1)
 m=trimesh.load_mesh(out/(STEM+'.stl'),process=True);assert m.is_watertight and m.is_winding_consistent and m.volume>0 and abs(m.bounds[0,2])<1e-6
 am=trimesh.load_mesh(refs/'ponte.stl',process=True);am.apply_scale(.001);am.visual.face_colors=[224,140,67,255];trimesh.Scene(am).export(str(refs/'ponte.glb'))
 geom=out/'R12_PONTE_SOLO_GEOMETRIA.3mf';delta=three_mf(m,geom)
 part={'id':'ponte_centrato','quantita':1,'solo_prototipo':True,'stl_stampa':f'stampa/{STEM}.stl','step_stampa':f'stampa/{STEM}.step','stl_assieme':'sorgenti/assieme/ponte.stl','step_assieme':'sorgenti/assieme/ponte.step','matrice_stampa_da_assieme':[[1,0,0,0],[0,1,0,0],[0,0,1,-P['fascia_basso_z']],[0,0,0,1]],'bounds_stampa_mm':bounds_cad(printing).tolist(),'bounds_assieme_mm':bounds_cad(shape).tolist()}
 manifest={'revisione':P['revisione'],'unita':'mm','pezzi':[part],'piatto_geometrico':{'file':str(geom.relative_to(R)),'numero_pezzi':1,'unita':'mm','items':[{'id':part['id'],'traslazione_da_stampa_mm':delta}]},'scopo':P['scopo']}
 (R/'sorgenti/manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
 report={'revisione':'R12','CAD_valido':shape.isValid(),'CAD_solidi':len(shape.Solids()),'CAD_volume_mm3':shape.Volume(),'STL_dim_mm':m.extents.tolist(),'STL_volume_mm3':float(m.volume),'altezza_fascia':P['fascia_altezza'],'aletta_al_centro':(P['fascia_basso_z']+P['fascia_alto_z'])/2==P['aletta_centro_z'],'nervature':len(ribs),'riferimenti_rinforzo_bounds':[bounds_cad(s).tolist() for s in ribs],'dipendenze':{n:importlib.metadata.version(n) for n in ['cadquery','trimesh','numpy']},'file_sha256':{str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [out/(STEM+'.stl'),out/(STEM+'.step'),geom,refs/'ponte.stl',refs/'ponte.step',refs/'ponte.glb']}}
 (R/'verifiche/generazione.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
