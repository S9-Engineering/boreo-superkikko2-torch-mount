"""Sonde geometriche R10/R12 conservate e applicate agli esportati R13."""
import math,json
import numpy as np
import cadquery as cq
from geometria_utils import bounds_cad,line_sections

def verifica_ponte(shape,R,check):
    b=bounds_cad(shape);check('fascia_basso8_2',abs(b[0,2]-8.2)<1e-5);check('fascia_alto37',abs(b[1,2]-37)<1e-5);check('aletta_centrata22_6',abs((b[0,2]+b[1,2])/2-22.6)<1e-5)
    flip=shape.rotate((0,0,22.6),(0,1,22.6),180)
    base=cq.importers.importStep(str(R/'sorgenti/riferimenti/BASE_R10_STAMPA.step')).val();old=cq.importers.importStep(str(R/'sorgenti/riferimenti/PONTE_R10_STAMPA.step')).val().translate((0,0,21))
    for name,pose in [('normale',shape),('capovolto',flip)]:
     check(f'{name}:nessuna_interferenza_base_R10',pose.intersect(base).Volume()<1e-5)
     for x in [-42,42]:
      check(f'{name}:{x}:foro_M3_libero',not line_sections(pose,[x,8,18],[x,8,27]))
      hs=line_sections(pose,[x,-12,18],[x,-12,27]);ws=line_sections(pose,[x-8,-12,22.6],[x+8,-12,22.6])
      check(f'{name}:{x}:altezza_passaggio3_2',len(hs)==1 and abs(hs[0]['lunghezza_mm']-3.2)<1e-5)
      check(f'{name}:{x}:larghezza_passaggio9_2',len(ws)==1 and abs(ws[0]['lunghezza_mm']-9.2)<1e-5)
    cylinder=cq.Solid.makeCylinder(105.0001,100,cq.Vector(0,-110,-20),cq.Vector(0,0,1))
    outside=shape.cut(cylinder);refoutside=old.cut(cylinder);outsideflip=flip.cut(cylinder)
    check('tratto_oltre_raggio105_invariato',outside.cut(refoutside).Volume()+refoutside.cut(outside).Volume()<1e-5)
    check('passante_invariato_anche_capovolto',outsideflip.cut(refoutside).Volume()+refoutside.cut(outsideflip).Volume()<1e-5)
    inner=cq.Solid.makeCylinder(90,100,cq.Vector(0,-110,-20),cq.Vector(0,0,1));outer=cq.Solid.makeCylinder(92,100,cq.Vector(0,-110,-20),cq.Vector(0,0,1));annulus=outer.cut(inner)
    body=shape.intersect(annulus);flipped_body=flip.intersect(annulus)
    check('fascia_simmetrica_verticalmente',body.cut(flipped_body).Volume()+flipped_body.cut(body).Volume()<1e-5)
    for angle in [-.4,0,.4]:
     c=[0,-110];start=[89*math.sin(angle),c[1]+89*math.cos(angle),30];end=[93*math.sin(angle),c[1]+93*math.cos(angle),30]
     sec=line_sections(shape,start,end);check(f'spessore2mm_{angle}',len(sec)==1 and abs(sec[0]['lunghezza_mm']-2)<1e-5)
     check(f'raggio_esterno92_{angle}',len(sec)==1 and abs(max(math.hypot(e[0],e[1]+110) for e in sec[0]['estremi_mm'])-92)<1e-5)
    # La geometria nuova resta dal lato esterno; il retro R90 e' libero.
    check('nessun_tallone_o_rinforzo_verso_testa',shape.intersect(inner).Volume()<1e-5)
    rinforzi=[]
    for x in [-42,42]:
     check(f'nervatura_verso_aletta_sotto_{x}',bool(line_sections(shape,[x,-27,20.5],[x,-18,20.5])))
     check(f'nessuna_nervatura_sopra_{x}',not line_sections(shape,[x,-25,24.7],[x,-18,24.7]))
     check(f'nessun_tallone_interno_{x}',not line_sections(shape,[x,-33,22.6],[x,-30.8,22.6]))
     check(f'inversione_nervatura_sopra_{x}',bool(line_sections(flip,[x,-27,24.7],[x,-18,24.7])))
     heights=[]
     for y in np.linspace(-29.6,-16.2,16):
      hs=line_sections(shape,[x,float(y),18],[x,float(y),27])
      # Salta i campioni dentro la fascia, che e' intenzionalmente alta28.8.
      if math.hypot(x,y+110)>92.01 and len(hs)==1:heights.append(hs[0]['lunghezza_mm'])
     check(f'ingombro_verticale_locale_fino4_4_{x}',heights and max(heights)<=4.40001 and max(heights)>3.5)
     rinforzi.append({'x':x,'altezza_locale_campionata_max_mm':max(heights)})


def verifica_base(shapes,manifest,R,check):
    params=json.loads((R/'sorgenti/parametri_base.json').read_text())
    # Il logo e' esterno sul fianco destro, oltre il pianoX49 del boss.
    region=cq.Workplane('XY',origin=(49, -5.1,11.7)).box(2.1,16.2,8.0,centered=(False,False,False)).val()
    raised=shapes['base_appoggi'].intersect(region)
    check('logo_due_lettere',len(raised.Solids())==2)
    br=bounds_cad(raised)
    check('logo_estrusione2mm',abs(br[0,0]-49)<1e-5 and abs(br[1,0]-51)<1e-5)
    check('logo_larghezza16mm',abs(br[1,1]-br[0,1]-16)<1e-5)
    check('logo_altezza_proporzionale',abs(br[1,2]-br[0,2]-16*250/513)<.03)
    check('logo_non_sul_piano_farfalla',br[0,0]>33.75)
    check('logo_non_sul_contatto_casco',br[0,1]>-6)
    check('logo_SVG_originale_archiviato',(R/'sorgenti/logo_S9.svg').exists())
    # Piano arrotondato: assenti i quattro vecchi angoli della piastraX+-33.75/Z0,46.
    for x,z in [(-33.5,.25),(33.5,.25),(-33.5,45.75),(33.5,45.75)]:
        check(f'angolo_piastra_{x}_{z}_rimosso',not line_sections(shapes['base_appoggi'],[x,6,z],[x,9,z]))
    for x in [-28.75,28.75]:
        check(f'appoggio_{x}:foro_passante',not line_sections(shapes['base_appoggi'],[x,-5,22.6],[x,20,22.6]))
        face=line_sections(shapes['base_appoggi'],[x,-5,10],[x,9,10])
        check(f'appoggio_{x}:piano_Y8',len(face)==1 and abs(max(e[1] for e in face[0]['estremi_mm'])-8)<1e-5)
        cut=line_sections(shapes['base_appoggi'],[x-5,7.9,22.6],[x+5,7.9,22.6])
        cut=sorted(sorted(e[0] for e in q['estremi_mm']) for q in cut)
        check(f'appoggio_{x}:asola_lunga3',len(cut)==2 and abs(cut[1][0]-cut[0][1]-3)<1e-5)
        vertical_cut=line_sections(shapes['base_appoggi'],[x,7.9,20],[x,7.9,25])
        ranges=sorted(sorted(e[2] for e in q['estremi_mm']) for q in vertical_cut)
        check(f'appoggio_{x}:luce1_9',len(ranges)==2 and abs(ranges[1][0]-ranges[0][1]-1.9)<1e-5)
    check('foro_superiore_passante',not line_sections(shapes['base_appoggi'],[0,-5,41.5],[0,20,41.5]))
    for x,z in [(0,10),(0,20),(0,30),(0,38),(-28.75,32),(28.75,32),(-10,40),(10,40)]:
        face=line_sections(shapes['base_appoggi'],[x,3.01,z],[x,8.01,z])
        check(f'piano_completo_{x}_{z}',len(face)==1 and abs(max(e[1] for e in face[0]['estremi_mm'])-8)<1e-5)
    for x in [-14.5,14.5]:
        relief=cq.Workplane('XY',origin=(x,-3,8)).box(10,20,10,centered=(True,False,False)).val()
        check(f'rivetto_{x}_scarico',shapes['base_appoggi'].intersect(relief).Volume()<1e-5)
    top_width=line_sections(shapes['base_appoggi'],[-5,7.9,41.5],[5,7.9,41.5])
    ranges=sorted(sorted(e[0] for e in q['estremi_mm']) for q in top_width)
    check('asola_superiore_lunga3',len(ranges)==2 and abs(ranges[1][0]-ranges[0][1]-3)<1e-5)
    top_height=line_sections(shapes['base_appoggi'],[0,7.9,39],[0,7.9,44])
    ranges=sorted(sorted(e[2] for e in q['estremi_mm']) for q in top_height)
    check('asola_superiore_luce1_9',len(ranges)==2 and abs(ranges[1][0]-ranges[0][1]-1.9)<1e-5)

    bp=bounds_cad(shapes['ponte_centrato'])
    check('ponte_centrato_basso8_2',abs(bp[0,2]-8.2)<1e-6)
    check('ponte_centrato_alto37',abs(bp[1,2]-37)<1e-6)
    c=params['centro_curva_xy'];inside=cq.Solid.makeCylinder(params['base_raggio_interno'],100,cq.Vector(*c,-20),cq.Vector(0,0,1))
    check('base_non_protrude_dietro_curva_contatto',shapes['base_appoggi'].intersect(inside).Volume()<1e-5)
    for index,x in enumerate(params['assi_terminali_x'],1):
        y=params['fissaggio_asse_y']
        check(f'vite_{x}:passaggio_base',not line_sections(shapes['base_appoggi'],[x,y,8],[x,y,30]))
        check(f'vite_{x}:passaggio_ponte',not line_sections(shapes['ponte_centrato'],[x,y,19],[x,y,30]))
        check(f'vite_{x}:bordo_trasversale2_9',abs((params['terminale_larghezza']-params['fissaggio_diametro'])/2-2.9)<1e-6)
        check(f'vite_{x}:bordo_frontale4_3',abs(params['terminale_fronte_y']-y-params['fissaggio_diametro']/2-4.3)<1e-6)
        nut=next(p for p in manifest['riferimenti'] if p['id'].startswith('dado_') and p['id'].endswith(str(index)))
        n=cq.importers.importStep(str(R/nut['step_assieme'])).val()
        check(f'dado_{x}:tasca_libera',n.intersect(shapes['base_appoggi']).Volume()<1e-5)
        check(f'dado_{x}:inserimento_da_sotto',max(n.translate((0,0,-float(d))).intersect(shapes['base_appoggi']).Volume() for d in range(9))<1e-5)
        for kind in ['vite_','rondella_']:
            ref=next(p for p in manifest['riferimenti'] if p['id'].startswith(kind) and p['id'].endswith(str(index)))
            h=cq.importers.importStep(str(R/ref['step_assieme'])).val()
            check(f'{kind}{x}:nessuna_interferenza',all(h.intersect(s).Volume()<1e-5 for s in shapes.values()))
