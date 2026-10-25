"""Geometria conservata dalla provino-R12-rinforzi-verso-alette-PLA, integrata nella R13."""
from pathlib import Path
import math,json,hashlib,zipfile,importlib.metadata
import xml.etree.ElementTree as ET
import cadquery as cq
import numpy as np
import trimesh
from geometria_utils import bounds_cad
R=Path(__file__).resolve().parents[1]
P=json.loads((R/'sorgenti/parametri_ponte.json').read_text())
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
