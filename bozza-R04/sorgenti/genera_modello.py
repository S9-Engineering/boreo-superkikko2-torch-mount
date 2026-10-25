#!/usr/bin/env python3
"""R04: bozza visiva maker, tutte le quote ASSUNTE, NON USO sul casco.

Rigenera con python genera_modello.py. I tre derivati in stampa/ sono soltanto
geometrie di bozza. I fermi sottili sono DIME DI FORMA. Casco, schiume, resistenza,
termica, materiali, slicing e compatibilita reale non sono rappresentati/verificati.
Farfalla, U, torcia e ferramenta sono SCHEMATICI_NON_STAMPABILI, separati.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

import cadquery as cq
import numpy as np
import trimesh
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

QUI = Path(__file__).resolve().parent
ROOT = QUI.parent
STAMPA = ROOT / "stampa"
REF = QUI / "riferimenti-visuali"
P = json.loads((QUI / "parametri_assunti.json").read_text())


def q(gruppo, nome):
    v = P[gruppo][nome]
    assert v["stato"] == "ASSUNTA"
    return v["valore"]


def cilindro_y(x, z, y0, lunghezza, r):
    return cq.Solid.makeCylinder(r, lunghezza, cq.Vector(x, y0, z), cq.Vector(0, 1, 0))


def scatola_xz(x, z, y0, larghezza, altezza, profondita, raccordo=0):
    w = cq.Workplane("XY", origin=(x, y0, z)).box(larghezza, profondita, altezza,
                                                   centered=(True, False, True))
    if raccordo:
        w = w.edges("|Y").fillet(raccordo)
    return w.val()


def arco(ri, sp, theta0, theta1, z0, altezza, raccordo=0):
    cx, cy = q("base", "centro_curva_xy_mm")
    ro = ri + sp
    tm = (theta0 + theta1) / 2
    def pt(r, t):
        return (cx + r * math.sin(t), cy + r * math.cos(t))
    w = (cq.Workplane("XY", origin=(0, 0, z0))
         .moveTo(*pt(ri, theta0)).threePointArc(pt(ri, tm), pt(ri, theta1))
         .lineTo(*pt(ro, theta1)).threePointArc(pt(ro, tm), pt(ro, theta0))
         .close().extrude(altezza))
    if raccordo:
        w = w.edges("|Z").fillet(raccordo)
    return w.val()


def cilindro_centro_curva(r):
    cx, cy = q("base", "centro_curva_xy_mm")
    return cq.Solid.makeCylinder(r, 120, cq.Vector(cx, cy, -30), cq.Vector(0, 0, 1))


def esagono_y(x, z, y0, profondita, tra_facce):
    return (cq.Workplane("XZ", origin=(x, y0, z))
            .polygon(6, tra_facce / math.cos(math.pi/6)).extrude(-profondita).val())


def taglio_dado_aperto(x, z, fronte, top_z):
    """Tasca esagonale e canale dall'alto: inseribile prima dell'accoppiamento."""
    profondita = q("collegamento_fermi", "dado_tasca_profondita_y_mm")
    y0 = fronte - profondita
    hexshape = esagono_y(x, z, y0, profondita,
                        q("collegamento_fermi", "dado_tasca_tra_facce_mm"))
    canale = scatola_xz(x, (z + top_z + 1) / 2, y0,
                        q("collegamento_fermi", "canale_inserimento_dado_larghezza_mm"),
                        top_z + 1 - z, profondita)
    return hexshape.fuse(canale).clean()


def crea_base():
    r = q("base", "raggio_interno_mm")
    theta = math.asin(q("base", "corda_interna_mm") / (2*r))
    base = arco(r, q("base", "spessore_radiale_mm"), -theta, theta, 0,
                q("base", "altezza_z_mm"), q("base", "raccordo_estremi_mm"))
    maschera_interna = cilindro_centro_curva(r)
    # Quattro appoggi della farfalla sullo stesso piano Y=6; spessore principale
    # radiale4, rinforzi locali piu profondi esplicitamente previsti.
    y_app = q("base", "piano_appoggio_farfalla_y_mm")
    pads = [(x,q("farfalla_schematica", "asole_laterali_centro_z_mm"),
             q("fissaggio_farfalla", "pad_laterali_larghezza_mm"),
             q("fissaggio_farfalla", "pad_laterali_altezza_mm"))
            for x in q("farfalla_schematica", "asole_laterali_assi_x_mm")]
    pads += [(0,9,30,6),(0,32,12,8)]
    for x, z, lx, hz in pads:
        pad = scatola_xz(x, z, -15, lx, hz, y_app+15, 1.0).cut(maschera_interna)
        base = base.fuse(pad)
    # Guide laterali con gioco per lato, piu battuta inferiore positiva.
    gioco = q("base", "gioco_guide_farfalla_per_lato_mm")
    sg = q("base", "spessore_guide_mm")
    yf = q("base", "fronte_guide_y_mm")
    for segno in (-1,1):
        x = segno * (35 + gioco + sg/2)
        guida = scatola_xz(x, 17, -15, sg, 25, yf+15, 0.6).cut(maschera_interna)
        base = base.fuse(guida)
    stop = scatola_xz(0, 2, -15, 65, 2, yf+15, 0.5).cut(maschera_interna)
    base = base.fuse(stop)
    # Sedi indipendenti dei due codoli. Il fronte Y=-4 dei codoli chiude contro
    # il fondo della sede: la vite non ha corsa nominale per richiamare il pattino.
    g = q("collegamento_fermi", "gioco_sede_per_lato_mm")
    z = q("collegamento_fermi", "assi_z_mm")
    ys = q("collegamento_fermi", "codolo_fronte_y_mm")
    yb = q("collegamento_fermi", "bossolo_fronte_y_mm")
    for x in q("collegamento_fermi", "assi_x_mm"):
        boss = scatola_xz(x,z,-18,
                         q("collegamento_fermi", "bossolo_larghezza_x_mm"),
                         q("collegamento_fermi", "bossolo_altezza_z_mm"), yb+18, 1.5)
        base = base.fuse(boss.cut(maschera_interna))
        sede = scatola_xz(x,z,-45,
                         q("collegamento_fermi", "codolo_larghezza_x_mm") + 2*g,
                         q("collegamento_fermi", "codolo_altezza_z_mm") + 2*g,
                         ys+45, q("collegamento_fermi", "raccordo_codolo_mm") + g)
        base = base.cut(sede).cut(cilindro_y(x,z,-45,60,
                                    q("collegamento_fermi", "diametro_passante_mm")/2))
    # Due fissaggi della farfalla alle sole asole laterali; tasche dadi apribili
    # dall'alto prima di posare la farfalla. I fori centrali della U sono distinti.
    for x in q("farfalla_schematica", "asole_laterali_assi_x_mm"):
        z = q("farfalla_schematica", "asole_laterali_centro_z_mm")
        base = base.cut(cilindro_y(x,z,-30,45,q("fissaggio_farfalla", "diametro_passante_mm")/2))
        top = z + q("fissaggio_farfalla", "pad_laterali_altezza_mm")/2
        base = base.cut(taglio_dado_aperto(x,z,q("fissaggio_farfalla", "tasca_dado_fronte_y_mm"),top))
    # Scarichi ciechi per le code schematiche dei due fissaggi ORIGINALI della U.
    # Non sono punti di fissaggio aggiuntivi della base alla farfalla.
    prof = q("base", "scarichi_ciechi_fissaggi_U_profondita_mm")
    for x in q("farfalla_schematica", "fori_U_assi_x_mm"):
        base = base.cut(cilindro_y(x,q("farfalla_schematica", "fori_U_centro_z_mm"),
                                  y_app-prof,prof+1,
                                  q("base", "scarichi_ciechi_fissaggi_U_diametro_mm")/2))
    # Conservare le facce dei diversi appoggi: l'unificazione delle facce
    # tangenti alla superficie cilindrica puo invalidare il B-Rep in OCP7.9.
    return base


def crea_fermo(segno):
    r = q("fermi_dima", "raggio_interno_mm")
    sp = q("fermi_dima", "spessore_radiale_mm")
    rm = r + sp/2
    x = segno * abs(q("collegamento_fermi", "assi_x_mm")[1])
    t = math.asin(x/rm)
    dt = q("fermi_dima", "lunghezza_arco_centrolinea_mm")/(2*rm)
    z0 = q("fermi_dima", "z_min_mm")
    h = q("fermi_dima", "altezza_z_mm")
    pattino = arco(r,sp,t-dt,t+dt,z0,h,q("fermi_dima", "raccordo_estremi_mm"))
    z = q("collegamento_fermi", "assi_z_mm")
    yf = q("collegamento_fermi", "codolo_fronte_y_mm")
    codolo = scatola_xz(x,z,-45,q("collegamento_fermi", "codolo_larghezza_x_mm"),
                       q("collegamento_fermi", "codolo_altezza_z_mm"),yf+45,
                       q("collegamento_fermi", "raccordo_codolo_mm"))
    # Nessun volume del codolo sporge oltre la faccia interna arcuata del pattino.
    codolo = codolo.cut(cilindro_centro_curva(r))
    fermo = pattino.fuse(codolo).clean()
    fermo = fermo.cut(cilindro_y(x,z,-45,60,q("collegamento_fermi", "diametro_passante_mm")/2))
    top = z + q("collegamento_fermi", "codolo_altezza_z_mm")/2
    fermo = fermo.cut(taglio_dado_aperto(x,z,q("collegamento_fermi", "dado_tasca_fronte_y_mm"),top))
    return fermo.clean()


def asola_y(x,z,y0,lx,hz,profondita):
    return scatola_xz(x,z,y0,lx,hz,profondita,min(lx,hz)/2-1e-4)


def crea_farfalla():
    y0 = q("base", "piano_appoggio_farfalla_y_mm")
    sp = q("farfalla_schematica", "spessore_y_mm")
    w = (cq.Workplane("XZ",origin=(0,y0,0))
         .polyline(q("farfalla_schematica", "profilo_xz_mm")).close().extrude(-sp))
    farfalla = w.edges("|Y").fillet(q("farfalla_schematica", "raccordo_profilo_mm")).val()
    for x in q("farfalla_schematica", "asole_laterali_assi_x_mm"):
        farfalla = farfalla.cut(asola_y(x,q("farfalla_schematica", "asole_laterali_centro_z_mm"),y0-1,
                                      q("farfalla_schematica", "asole_laterali_larghezza_mm"),
                                      q("farfalla_schematica", "asole_laterali_lunghezza_mm"),sp+2))
    farfalla = farfalla.cut(asola_y(0,q("farfalla_schematica", "asola_alta_centro_z_mm"),y0-1,
                                  q("farfalla_schematica", "asola_alta_larghezza_mm"),
                                  q("farfalla_schematica", "asola_alta_altezza_mm"),sp+2))
    for x in q("farfalla_schematica", "fori_U_assi_x_mm"):
        farfalla = farfalla.cut(cilindro_y(x,q("farfalla_schematica", "fori_U_centro_z_mm"),y0-1,sp+2,1.7))
    return farfalla.clean()


def crea_U():
    sp = q("U_schematica", "spessore_metallo_mm")
    xi = q("U_schematica", "luce_interna_x_mm")/2
    y0 = q("base", "piano_appoggio_farfalla_y_mm") + q("farfalla_schematica", "spessore_y_mm")
    h = q("U_schematica", "traversa_altezza_z_mm")
    z = q("U_schematica", "traversa_centro_z_mm")
    U = scatola_xz(0,z,y0,2*(xi+sp),h,sp,0.7)
    y1 = q("U_schematica", "bracci_fronte_y_mm")
    zh = q("U_schematica", "bracci_altezza_z_mm")
    zc = q("U_schematica", "bracci_z_min_mm") + zh/2
    for segno in (-1,1):
        arm = scatola_xz(segno*(xi+sp/2),zc,y0+sp/2,sp,zh,y1-y0-sp/2,0.6)
        U = U.fuse(arm)
    for x in q("farfalla_schematica", "fori_U_assi_x_mm"):
        U = U.cut(cilindro_y(x,z,y0-1,sp+2,1.7))
    yp = q("U_schematica", "asse_torcia_y_mm")
    zp = q("U_schematica", "asse_torcia_z_mm")
    U = U.cut(cq.Solid.makeCylinder(q("U_schematica", "diametro_fori_perni_mm")/2,
                                   2*(xi+sp)+4,cq.Vector(-xi-sp-2,yp,zp),cq.Vector(1,0,0)))
    return U.clean()


def crea_torcia():
    return scatola_xz(0,q("torcia_schematica", "altezza_z_mm")/2,
                      q("torcia_schematica", "retro_y_mm"),
                      q("torcia_schematica", "larghezza_x_mm"),
                      q("torcia_schematica", "altezza_z_mm"),
                      q("torcia_schematica", "profondita_y_mm"),
                      q("torcia_schematica", "raccordo_ingombro_mm"))


def vite_y(x,z,appoggio,lunghezza):
    ds = q("ferramenta_schematica", "diametro_gambo_mm")
    dr = q("ferramenta_schematica", "rondella_diametro_esterno_mm")
    sr = q("ferramenta_schematica", "rondella_spessore_mm")
    dt = q("ferramenta_schematica", "diametro_testa_mm")
    ht = q("ferramenta_schematica", "altezza_testa_mm")
    rondella = cilindro_y(x,z,appoggio,sr,dr/2).cut(cilindro_y(x,z,appoggio-1,sr+2,1.7))
    gambo = cilindro_y(x,z,appoggio+sr-lunghezza,lunghezza,ds/2)
    testa = cilindro_y(x,z,appoggio+sr,ht,dt/2)
    return cq.Compound.makeCompound([gambo.fuse(testa).clean(),rondella])


def dado_y(x,z,front):
    sp = q("ferramenta_schematica", "dado_spessore_mm")
    dado = esagono_y(x,z,front-sp,sp,q("ferramenta_schematica", "dado_tra_facce_mm"))
    return dado.cut(cilindro_y(x,z,front-sp-1,sp+2,1.7))


def crea_ferramenta():
    clip, farf, originali, perni = [], [], [], []
    z = q("collegamento_fermi", "assi_z_mm")
    for x in q("collegamento_fermi", "assi_x_mm"):
        clip.extend([vite_y(x,z,2,12),dado_y(x,z,-5.5)])
    for x in q("farfalla_schematica", "asole_laterali_assi_x_mm"):
        farf.extend([vite_y(x,z,7.5,10),dado_y(x,z,4.5)])
    for x in q("farfalla_schematica", "fori_U_assi_x_mm"):
        # Volumi di riferimento dei fissaggi originali, distinti da quelli laterali.
        originali.append(vite_y(x,12,9.5,6))
    for segno in (-1,1):
        perni.append(cq.Solid.makeCylinder(2.0,3.0,cq.Vector(segno*32,33,23),cq.Vector(segno,0,0)))
        perni.append(cq.Solid.makeCylinder(3.6,2.0,cq.Vector(segno*35,33,23),cq.Vector(segno,0,0)))
    return {"viti_fermi":cq.Compound.makeCompound(clip),
            "viti_farfalla":cq.Compound.makeCompound(farf),
            "fissaggi_U_originali":cq.Compound.makeCompound(originali),
            "perni_torcia_originali":cq.Compound.makeCompound(perni)}


def bounds(shape):
    # BoundingBox() include margini OCCT conservativi, visibili anche come
    # Z negativo su un pezzo appoggiato a Z0. Questi sono metadati geometrici
    # ottimizzati, senza usare triangolazioni o dilatare per tolleranze delle forme.
    b=Bnd_Box()
    BRepBndLib.AddOptimal_s(shape.wrapped,b,False,False)
    valori=[round(float(v),6) or 0.0 for v in b.Get()]
    return [valori[:3],valori[3:]]


def mesh_da_shape(shape):
    v,f=shape.tessellate(q("esportazione", "tolleranza_lineare_mesh_mm"),
                        q("esportazione", "tolleranza_angolare_mesh_rad"))
    return trimesh.Trimesh(vertices=[[p.x,p.y,p.z] for p in v],faces=f,process=True)


def salva_shape(shape,path):
    cq.exporters.export(shape,str(path.with_suffix(".step")))
    cq.exporters.export(shape,str(path.with_suffix(".stl")),
                        tolerance=q("esportazione", "tolleranza_lineare_mesh_mm"),
                        angularTolerance=q("esportazione", "tolleranza_angolare_mesh_rad"))


def shape_transform(shape,matrice):
    if np.allclose(matrice,np.eye(4)):
        return shape
    m = np.asarray(matrice)
    assert np.allclose(m[:3,:3],[[1,0,0],[0,0,1],[0,-1,0]])
    # Operazioni rigide native; non convertire gp_GTrsf (scala non inizializzata
    # da cq.Matrix(list) con questa combinazione CQ/OCP).
    return shape.rotate((0,0,0),(1,0,0),-90).translate(tuple(m[:3,3]))


def crea_3mf(meshes,path):
    ns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
    ET.register_namespace("",ns)
    def el(nome,attrs=None): return ET.Element(f"{{{ns}}}{nome}",attrs or {})
    model=el("model",{"unit":"millimeter","xml:lang":"it-IT"})
    ET.SubElement(model,f"{{{ns}}}metadata",{"name":"Title"}).text="BOZZA R04 NON USO - tre geometrie, due DIME"
    ET.SubElement(model,f"{{{ns}}}metadata",{"name":"Description"}).text="Solo base e due fermi DIMA; nessun riferimento lampada, profilo macchina, materiale o slicing."
    ris=ET.SubElement(model,f"{{{ns}}}resources")
    build=ET.SubElement(model,f"{{{ns}}}build")
    items=[]
    for idx,((nome,mesh),centro) in enumerate(zip(meshes.items(),q("esportazione","centri_piatto_xy_mm")),1):
        obj=ET.SubElement(ris,f"{{{ns}}}object",{"id":str(idx),"type":"model","name":nome})
        me=ET.SubElement(obj,f"{{{ns}}}mesh")
        ve=ET.SubElement(me,f"{{{ns}}}vertices")
        for x,y,z in mesh.vertices:
            ET.SubElement(ve,f"{{{ns}}}vertex",{k:f"{v:.9f}" for k,v in zip(("x","y","z"),(x,y,z))})
        tri=ET.SubElement(me,f"{{{ns}}}triangles")
        for a,b,c in mesh.faces:
            ET.SubElement(tri,f"{{{ns}}}triangle",{"v1":str(a),"v2":str(b),"v3":str(c)})
        dx,dy=np.asarray(centro)-mesh.bounds.mean(axis=0)[:2]
        tr=[float(dx),float(dy),float(-mesh.bounds[0,2])]
        ET.SubElement(build,f"{{{ns}}}item",{"objectid":str(idx),"transform":f"1 0 0 0 1 0 0 0 1 {tr[0]:.9f} {tr[1]:.9f} {tr[2]:.9f}"})
        items.append({"id":nome,"traslazione_da_stampa_mm":tr})
    tipi=('<?xml version="1.0" encoding="UTF-8"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    rel=('<?xml version="1.0" encoding="UTF-8"?>'
         '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
         '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    with zipfile.ZipFile(path,"w",compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",tipi)
        z.writestr("_rels/.rels",rel)
        z.writestr("3D/3dmodel.model",ET.tostring(model,encoding="utf-8",xml_declaration=True))
    return items


def principale():
    STAMPA.mkdir(parents=True,exist_ok=True)
    REF.mkdir(parents=True,exist_ok=True)
    nuovi={"base":crea_base(),"fermo_sx":crea_fermo(-1),"fermo_dx":crea_fermo(1)}
    refs={"farfalla":crea_farfalla(),"U_metallica":crea_U(),"torcia":crea_torcia(),**crea_ferramenta()}
    for nome,s in {**nuovi,**refs}.items():
        assert s.isValid() and s.Volume()>0,(nome,"CAD non valido")
        if nome in nuovi or nome in ("farfalla","U_metallica","torcia"):
            assert len(s.Solids())==1,(nome,len(s.Solids()))
    identita=np.eye(4).tolist()
    matrici={"base":identita}
    for nome,segno in (("fermo_sx",-1),("fermo_dx",1)):
        x = q("collegamento_fermi", "assi_x_mm")[0 if segno<0 else 1]
        z = q("collegamento_fermi", "assi_z_mm")
        yf = q("collegamento_fermi", "codolo_fronte_y_mm")
        matrici[nome]=[[1,0,0,-x],[0,0,1,-z],[0,-1,0,yf],[0,0,0,1]]
    nomifile={"base":"BOZZA_R04_BASE_NON_USO","fermo_sx":"BOZZA_R04_FERMO_SX_DIMA_NON_USO",
              "fermo_dx":"BOZZA_R04_FERMO_DX_DIMA_NON_USO"}
    colori={"base":[0.12,0.48,0.76,1],"fermo_sx":[1.0,0.48,0.08,1],"fermo_dx":[1.0,0.48,0.08,1],
            "farfalla":[0.70,0.73,0.77,1],"U_metallica":[0.48,0.51,0.56,1],"torcia":[0.12,0.14,0.17,1]}
    manifest={"revisione":P["revisione"],"stato":P["stato"],"unita_assieme":"mm","assi":P["assi"],
              "metodo_bounds":"OCCT AddOptimal, senza triangolazione/tolleranze di forma; arrotondamento 0,000001 mm",
              "tutte_quote_ASSUNTE":True,"casco_presente":False,"pezzi":[],"riferimenti":[],
              "nota":"Solo BOZZA NON USO; i fermi 1,2 sono DIME DI FORMA. Nessuna prova sul casco o slicing.",
              "assi_fori_nominali_mm":{
                  "collegamento_fermi":{"punti":[[-42,-4,23],[42,-4,23]],"direzione":[0,1,0],"diametro":3.4},
                  "fissaggio_farfalla":{"punti":[[-27,6,23],[27,6,23]],"direzione":[0,1,0],"diametro_base":3.4,"larghezza_asole":3.8},
                  "fissaggi_U_originali_REF":{"punti":[[-14,7.5,12],[14,7.5,12]],"direzione":[0,1,0],"diametro":3.4}},
              "contatti_intenzionali":["fronte codolo/fondo socket: Y=-4", "retro farfalla/quattro appoggi base: Y=6", "farfalla/battuta inferiore: Z=3", "farfalla/U originale: Y=7.5"],
              "sequenza_assemblaggio_nominale":["Inserire dadi nelle tasche dall alto di codoli e base, prima di accoppiarli.","Inserire separatamente i fermi dall interno; i codoli impegnano i socket della base.","Chiudere i 2 fissaggi esterni X+-42 fino al contatto nominale della battuta terminale.","Appoggiare la farfalla sulle 4 sedi coplanari e sulla battuta bassa, fissandola nelle 2 asole laterali X+-27.","Rimontare il corpo torcia sulla U con la ferramenta originale: il corpo in posizione limita l accesso assiale ai fissaggi della farfalla."],
              "limiti":["Nessun casco o volume schiuma: passaggi, appoggi, inserimento nel casco e compressione non verificati.","Nessuna attribuzione di materiale funzionale ai fermi da1,2mm.","Accessibilita e ferramenta reali, rotazione torcia, dissipatore/cavo, calore e carichi non verificati."]}
    meshes_stampa={}
    rapporti={}
    for nome,shape in nuovi.items():
        salva_shape(shape,REF/f"{nome}_assieme")
        stamp=shape_transform(shape,matrici[nome])
        salva_shape(stamp,STAMPA/nomifile[nome])
        step_r=cq.importers.importStep(str(STAMPA/f"{nomifile[nome]}.step")).val()
        mesh=trimesh.load_mesh(STAMPA/f"{nomifile[nome]}.stl",process=True)
        assert step_r.isValid() and len(step_r.Solids())==1
        assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
        assert len(mesh.split(only_watertight=False))==1 and np.all(mesh.area_faces>1e-12)
        assert abs(mesh.bounds[0,2])<1e-5,(nome,mesh.bounds)
        meshes_stampa[nome]=mesh
        voce={"id":nome,"ruolo":"BASE_BOZZA_NON_USO" if nome=="base" else "FERMO_SOLO_DIMA_FORMA_NON_USO",
              "quantita":1,"solo_dima_forma":nome!="base",
              "stl_stampa":f"stampa/{nomifile[nome]}.stl","step_stampa":f"stampa/{nomifile[nome]}.step",
              "stl_assieme":f"sorgenti/riferimenti-visuali/{nome}_assieme.stl",
              "step_assieme":f"sorgenti/riferimenti-visuali/{nome}_assieme.step",
              "matrice_stampa_da_assieme":matrici[nome],"colore_display":colori[nome],
              "bounds_assieme_mm":bounds(shape),"bounds_stampa_mm":bounds(stamp)}
        manifest["pezzi"].append(voce)
        rapporti[nome]={"CAD_valido":shape.isValid(),"solidi":len(shape.Solids()),"volume_CAD_mm3":shape.Volume(),
                        "STEP_riaperto_valido":step_r.isValid(),"STEP_solidi":len(step_r.Solids()),
                        "mesh_chiusa":mesh.is_watertight,"mesh_normali_coerenti":mesh.is_winding_consistent,
                        "componenti_mesh":len(mesh.split(only_watertight=False)),"facce_degeneri":int(np.sum(mesh.area_faces<=1e-12)),
                        "volume_mesh_mm3":mesh.volume,"bounds_stampa_mm":mesh.bounds.tolist(),"triangoli":len(mesh.faces)}
    for nome,shape in refs.items():
        salva_shape(shape,REF/f"{nome}_assieme")
        manifest["riferimenti"].append({"id":nome,"tipologia":"SCHEMATICO_NON_STAMPARE",
                                       "stl_assieme":f"sorgenti/riferimenti-visuali/{nome}_assieme.stl",
                                       "step_assieme":f"sorgenti/riferimenti-visuali/{nome}_assieme.step",
                                       "matrice_stampa_da_assieme":None,
                                       "colore_display":colori.get(nome,[0.72,0.75,0.80,1]),"bounds_assieme_mm":bounds(shape)})
    # Il manifest parziale permette anteprime appena esistono i singoli pezzi.
    (QUI/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")
    # Collisioni volumetriche soltanto dei componenti principali; la ferramenta
    # e i contatti di serraggio sono verificati con classi di interfaccia proprie.
    principali={**nuovi,**{n:refs[n] for n in ("farfalla","U_metallica","torcia")}}
    collisioni=[]
    for i,(a,sa) in enumerate(principali.items()):
        for b,sb in list(principali.items())[i+1:]:
            volume=sa.intersect(sb).Volume()
            collisioni.append({"a":a,"b":b,"volume_intersezione_mm3":volume})
            assert volume<1e-5,(a,b,volume)
    collisioni_ferramenta=[]
    for hardware in ("viti_fermi","viti_farfalla","fissaggi_U_originali","perni_torcia_originali"):
        for nome,shape in principali.items():
            volume=refs[hardware].intersect(shape).Volume()
            collisioni_ferramenta.append({"hardware":hardware,"parte":nome,"volume_intersezione_mm3":volume})
            assert volume<1e-5,(hardware,nome,volume)
    scena=trimesh.Scene()
    assembly=cq.Assembly(name="BOZZA_R04_ASSIEME_SCHEMATICO_NON_STAMPARE")
    for nome,shape in {**nuovi,**refs}.items():
        colore=colori.get(nome,[0.72,0.75,0.80,1])
        assembly.add(shape,name=nome if nome in nuovi else f"NON_STAMPARE_{nome}",color=cq.Color(*colore))
        m=trimesh.load_mesh(REF/f"{nome}_assieme.stl",process=True)
        m.apply_scale(0.001)
        m.visual=trimesh.visual.ColorVisuals(m,face_colors=np.round(np.asarray(colore)*255).astype(np.uint8))
        scena.add_geometry(m,node_name=nome,geom_name=nome)
    step_ass=REF/"BOZZA_R04_ASSIEME_SCHEMATICO_NON_STAMPARE.step"
    assembly.export(str(step_ass))
    glb_ass=REF/"BOZZA_R04_ASSIEME_SCHEMATICO_NON_STAMPARE.glb"
    scena.metadata.update({"unita":"metri","scala_da_mm":0.001,"stato":P["stato"],"casco_presente":False})
    glb_ass.write_bytes(scena.export(file_type="glb"))
    mf=STAMPA/"BOZZA_R04_TRE_PEZZI_SOLO_GEOMETRIA.3mf"
    items=crea_3mf(meshes_stampa,mf)
    manifest["assieme"]={"step":str(step_ass.relative_to(ROOT)),"glb":str(glb_ass.relative_to(ROOT)),"unita_glb":"m"}
    manifest["piatto_geometrico"]={"file":str(mf.relative_to(ROOT)),"unita":"mm","numero_pezzi":3,"items":items,
                                  "profili_slicer_presenti":False,"slicing_eseguito":False}
    (QUI/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")
    report={"revisione":P["revisione"],"stato":P["stato"],"pezzi":rapporti,"collisioni_principali_assieme":collisioni,
            "collisioni_ferramenta_schematica":collisioni_ferramenta,
            "quote_assunte":True,"riferimenti_non_stampabili":list(refs),"casco_presente":False,
            "battuta_codolo_y_mm":-4,"gioco_codolo_per_lato_mm":0.35,"fermi_solo_dima_forma":True,
            "unita_STL_STEP_3MF":"mm","unita_GLB":"m","scala_GLB_da_mm":0.001,
            "limiti_verifica":"Controlli sorgente e riapertura dei tre STEP/STL. Nessuna verifica di montaggio reale, materiale, resistenza, termica, slicing o stampa. Verificatore indipendente separato.",
            "dipendenze":{n:importlib.metadata.version(n) for n in ("cadquery","cadquery-ocp","numpy","trimesh")},
            "sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted([*STAMPA.glob("*"),*REF.glob("*")]) if p.is_file()}}
    (QUI/"report_generazione.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"manifest":"sorgenti/manifest.json","pezzi":rapporti,"collisioni_principali":collisioni},indent=2))


if __name__=="__main__":
    principale()
