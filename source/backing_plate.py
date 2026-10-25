"""Geometria conservata dalla prototipo-R10-arrotondato-logo-PETG, integrata nella R13."""
from pathlib import Path
import json,math,hashlib,zipfile,importlib.metadata,re
from shapely.geometry import Polygon
import xml.etree.ElementTree as ET
import cadquery as cq
import numpy as np
import trimesh
from geometry_utils import bounds_cad
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'source/base-parameters.json').read_text())
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
def base():
 r=P['base_raggio_interno'];a=math.asin(P['base_corda_interna']/(2*r))
 shell=arc(r,P['base_spessore_radiale'],-a,a,0,P['base_altezza'],1.2)
 # Cornice aperta in alto: conserva fondo e montanti, libera rivetti e collo.
 shape=shell.cut(block(0,-50,P['base_bordo_inferiore_altezza'],P['base_finestra_centrale_larghezza'],100,60))
 for x in P['assi_terminali_x']:
  shape=shape.fuse(block(x,P['boss_retro_y'],P['boss_basso_z'],P['boss_larghezza'],P['boss_fronte_y']-P['boss_retro_y'],P['boss_alto_z']-P['boss_basso_z'],1))
  z=P['asse_terminali_z'];a=(P['terminale_larghezza']+2*P['gioco_sede_per_lato'])/2;b=(P['terminale_altezza']+2*P['gioco_sede_per_lato'])/2
  roof=cq.Workplane('XZ',origin=(x,-50,z)).polyline([(-a,-b),(a,-b),(a,b),(0,b+a),(-a,b)]).close().extrude(-55).val()
  shape=shape.cut(roof).cut(cyl(x,P['fissaggio_asse_y'],8,P['fissaggio_diametro'],20))
  shape=shape.cut(hexagon(x,P['fissaggio_asse_y'],P['boss_basso_z']-.01,P['dado_tasca_chiave'],P['dado_tasca_profondita']+.01))
 for sign in [-1,1]:
  shape=shape.fuse(block(sign*35,-2,10.4,8,8,8))
 c=P['centro_curva_xy'];inside=cq.Solid.makeCylinder(r+P['offset_rifilo_curva_base'],100,cq.Vector(*c,-20),cq.Vector(0,0,1))
 # Piastra piana continua, collegata al fondo, ai montanti e ai ripiani R08.
 panel=cq.Workplane('XZ',origin=(0,P['piastra_retro_y'],P['piastra_altezza']/2)).box(P['piastra_larghezza'],P['piastra_altezza'],P['piastra_spessore'],centered=(True,True,False)).edges('|Y').fillet(P['piastra_raggio_angoli']).val()
 # Normale XZ verso -Y: trasla la piastra sul piano Y3..8.
 panel=panel.translate((0,P['piastra_spessore'],0))
 shape=shape.fuse(panel)
 # Scarichi passanti: non costringono i rivetti a diventare punti di appoggio.
 for x in P['rivetti_x']:
  shape=shape.cut(block(x,-5,P['rivetti_z']-P['scarico_rivetti_altezza']/2,P['scarico_rivetti_larghezza'],25,P['scarico_rivetti_altezza'],1))
 # Ripassa i due fissaggi laterali attraverso l'intera piastra.
 for x in [-P['farfalla_interasse']/2,P['farfalla_interasse']/2]:
  shape=shape.cut(cq.Workplane('XZ',origin=(x,-5,P['appoggio_foro_z'])).slot2D(P['appoggio_lunghezza_asola'],P['appoggio_luce_asola'],0).extrude(-25).val())
 # Terzo fissaggio all'asola superiore: posizione Z provvisoria e passaggio1.9.
 shape=shape.cut(cq.Workplane('XZ',origin=(0,-5,P['superiore_foro_z'])).slot2D(P['appoggio_lunghezza_asola'],P['appoggio_luce_asola'],0).extrude(-25).val())
 shape=shape.cut(inside).clean()
 # Arrotonda anche le estremita della cornice esterna viste di fronte.
 envelope=cq.Workplane('XZ',origin=(0,40,23)).box(103,46,100,centered=(True,True,False)).edges('|Y').fillet(P['involucro_raggio_angoli']).val()
 shape=shape.intersect(envelope).clean()
 for glyph in logo():shape=shape.fuse(glyph)
 return shape.clean()
def logo():
 # Legge soltanto le coordinate M/L/Z del disegno SVG; nessun testo e' un'istruzione.
 tree=ET.parse(ROOT/'assets/logo_S9.svg');result=[];scale=P['logo_larghezza']/513
 for el in tree.getroot():
  if not el.tag.endswith('path'):continue
  data=el.attrib['d'];tokens=re.findall(r'[MLZmlz]|[-+]?[0-9]*\.?[0-9]+',data)
  assert not re.search(r'[ACQSTHVachqstv]',data)
  loops=[];loop=[];i=0
  while i<len(tokens):
   t=tokens[i];i+=1
   if t=='Z':loops.append(loop);loop=[];continue
   assert t in ['M','L']
   x=float(tokens[i]);y=float(tokens[i+1]);i+=2;loop.append((x*scale,-y*scale))
  assert not loop
  poly=Polygon(loops[0],loops[1:]).simplify(P['logo_semplificazione_mm'],preserve_topology=True)
  assert poly.is_valid and poly.area>0
  def wire(coords):
   return cq.Wire.makePolygon([cq.Vector(P['logo_x_piano']-.05,P['logo_centro_y']+u-P['logo_larghezza']/2,P['logo_centro_z']+v+250*scale/2) for u,v in list(coords)[:-1]],close=True)
  face=wire(poly.exterior.coords);holes=[wire(h.coords) for h in poly.interiors]
  result.append(cq.Solid.extrudeLinear(face,holes,cq.Vector(P['logo_rilievo']+.05,0,0)))
 assert len(result)==2
 return result
def hardware():
 refs={};top=P['terminale_basso_z']+P['terminale_altezza'];washer_top=top+P['rondella_spessore']
 for i,x in enumerate(P['assi_terminali_x'],1):
  y=P['fissaggio_asse_y'];screw=cyl(x,y,washer_top-P['vite_lunghezza'],3,P['vite_lunghezza']).fuse(cyl(x,y,washer_top,5.5,3))
  washer=cyl(x,y,top,7,.5).cut(cyl(x,y,top-.1,3.2,.7))
  nz=P['boss_basso_z']+P['dado_tasca_profondita']-P['dado_altezza'];nut=hexagon(x,y,nz,5.5,4).cut(cyl(x,y,nz-.1,3,4.2))
  refs[f'vite_M3x16_{i}']=screw;refs[f'rondella_M3_{i}']=washer;refs[f'dado_autobloccante_M3_{i}']=nut
 return refs
