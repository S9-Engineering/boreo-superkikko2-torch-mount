#!/usr/bin/env python3
"""Bozza visiva parametrica R03, NON FUNZIONALE e NON USABILE sul casco.

Rigenera con: python genera_modello.py
Dipendenze in requisiti.txt. Le quote nominali sono in parametri_assunti.json.
Non contiene CAD del casco, componenti della lampada, profili slicer o G-code.
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


QUI = Path(__file__).resolve().parent
ROOT = QUI.parent
STAMPA = ROOT / "stampa"
NOME = "BOZZA_R03_NON_USO"
P = json.loads((QUI / "parametri_assunti.json").read_text())


def quota(gruppo: str, nome: str):
    voce = P[gruppo][nome]
    assert voce["stato"] == "ASSUNTA"
    return voce["valore"]


def arco_ponte() -> cq.Shape:
    """Anello parziale con spessore radiale esatto, estruso da Z0."""
    r = quota("ponte", "raggio_centrolinea_mm")
    sem = quota("ponte", "corda_centrolinea_mm") / 2
    sp = quota("ponte", "spessore_radiale_mm")
    theta = math.asin(sem / r)
    cy = -math.sqrt(r * r - sem * sem)
    ri, ro = r - sp / 2, r + sp / 2
    def estremo(rad, segno):
        return (segno * rad * math.sin(theta), cy + rad * math.cos(theta))
    return (cq.Workplane("XY")
            .moveTo(*estremo(ri, -1))
            .threePointArc((0, cy + ri), estremo(ri, 1))
            .lineTo(*estremo(ro, 1))
            .threePointArc((0, cy + ro), estremo(ro, -1))
            .close().extrude(quota("ponte", "altezza_mm")).val())


def braccio(segno: int) -> cq.Shape:
    """Banda fra due spline morbide, allargata da 1.2 a 4 mm."""
    c = np.array(quota("bracci", "controlli_bezier_destro_xy_mm"), dtype=float)
    s0 = quota("bracci", "spessore_iniziale_mm")
    s1 = quota("bracci", "spessore_finale_mm")
    lati = [[], []]
    for t in np.linspace(0, 1, 61):
        u = 1 - t
        xy = u**3*c[0] + 3*u*u*t*c[1] + 3*u*t*t*c[2] + t**3*c[3]
        d = 3*u*u*(c[1]-c[0]) + 6*u*t*(c[2]-c[1]) + 3*t*t*(c[3]-c[2])
        n = np.array([d[1], -d[0]]) / np.linalg.norm(d)
        sp = s0 + (s1 - s0) * (3*t*t - 2*t*t*t)
        for lato, direzione in zip(lati, (-1, 1)):
            v = xy + direzione * n * sp / 2
            lato.append(cq.Vector(segno * v[0], v[1], 0))
    a, b = lati
    bordo = cq.Wire.assembleEdges([
        cq.Edge.makeSpline(a, tol=1e-7),
        cq.Edge.makeLine(a[-1], b[-1]),
        cq.Edge.makeSpline(list(reversed(b)), tol=1e-7),
        cq.Edge.makeLine(b[0], a[0]),
    ])
    return cq.Solid.extrudeLinear(bordo, [], cq.Vector(0, 0, quota("bracci", "altezza_mm")))


def orecchio(segno: int) -> cq.Shape:
    """Profilo YZ rettangolare raccordato; pareti X a +/-34 e +/-38."""
    interno = quota("orecchie", "luce_interna_mm") / 2
    sp = quota("orecchie", "spessore_x_mm")
    yy = quota("orecchie", "asse_fori_y_mm")
    hh = quota("orecchie", "altezza_z_mm")
    lung = quota("orecchie", "lunghezza_y_mm")
    rad = quota("orecchie", "raccordo_profilo_yz_mm")
    x0 = interno if segno > 0 else -interno - sp
    faccia = (cq.Workplane("YZ", origin=(x0, yy, hh / 2))
              .rect(lung, hh).extrude(sp).edges("|X").fillet(rad).val())
    return faccia


def crea_3mf(mesh: trimesh.Trimesh, path: Path):
    """3MF Core geometrico: millimetri, una mesh, un item, nessun preset."""
    ns = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
    ET.register_namespace("", ns)
    def el(nome, attributi=None):
        return ET.Element(f"{{{ns}}}{nome}", attributi or {})
    model = el("model", {"unit": "millimeter", "xml:lang": "it-IT"})
    meta = ET.SubElement(model, f"{{{ns}}}metadata", {"name": "Title"})
    meta.text = "BOZZA R03 NON USO - geometria soltanto"
    meta = ET.SubElement(model, f"{{{ns}}}metadata", {"name": "Description"})
    meta.text = "Bozza visiva non funzionale. Nessun profilo macchina, filamento o slicing."
    ris = ET.SubElement(model, f"{{{ns}}}resources")
    obj = ET.SubElement(ris, f"{{{ns}}}object", {"id": "1", "type": "model", "name": NOME})
    me = ET.SubElement(obj, f"{{{ns}}}mesh")
    ve = ET.SubElement(me, f"{{{ns}}}vertices")
    for x, y, z in mesh.vertices:
        ET.SubElement(ve, f"{{{ns}}}vertex", {k: f"{v:.9f}" for k, v in zip(("x", "y", "z"), (x, y, z))})
    tri = ET.SubElement(me, f"{{{ns}}}triangles")
    for a, b, c in mesh.faces:
        ET.SubElement(tri, f"{{{ns}}}triangle", {"v1": str(a), "v2": str(b), "v3": str(c)})
    centro = mesh.bounds.mean(axis=0)
    target = quota("esportazione", "centro_piatto_xy_mm")
    dx, dy = target[0] - centro[0], target[1] - centro[1]
    build = ET.SubElement(model, f"{{{ns}}}build")
    ET.SubElement(build, f"{{{ns}}}item", {"objectid": "1", "transform": f"1 0 0 0 1 0 0 0 1 {dx:.9f} {dy:.9f} 0"})
    tipi = ('<?xml version="1.0" encoding="UTF-8"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
            '</Types>')
    rel = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
           '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
           '</Relationships>')
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", tipi)
        z.writestr("_rels/.rels", rel)
        z.writestr("3D/3dmodel.model", ET.tostring(model, encoding="utf-8", xml_declaration=True))
    return [dx, dy, 0.0]


def principale():
    STAMPA.mkdir(parents=True, exist_ok=True)
    ponte = arco_ponte()
    bd, bs = braccio(1), braccio(-1)
    od, os = orecchio(1), orecchio(-1)
    contatti = {
        "ponte_braccio_destro_mm3": ponte.intersect(bd).Volume(),
        "ponte_braccio_sinistro_mm3": ponte.intersect(bs).Volume(),
        "braccio_orecchio_destro_mm3": bd.intersect(od).Volume(),
        "braccio_orecchio_sinistro_mm3": bs.intersect(os).Volume(),
    }
    assert all(v > 0.001 for v in contatti.values()), contatti
    solido = ponte.fuse(bd, bs, od, os).clean()
    assert len(solido.Solids()) == 1 and solido.isValid(), "Unione CAD non valida"
    # Raccordi locali alle giunzioni, senza modificare i piani delle orecchie.
    raccordo = quota("bracci", "raccordo_bordi_verticali_mm")
    giunti = []
    for edge in solido.Edges():
        box = edge.BoundingBox()
        c = edge.Center()
        if box.xlen < 1e-5 and box.ylen < 1e-5 and box.zlen > 1 and c.y < 40 and abs(c.x) > 40:
            giunti.append(edge)
    if giunti:
        solido = solido.fillet(raccordo, giunti).clean()
    for segno in (-1, 1):
        x = segno * (quota("orecchie", "luce_interna_mm") / 2 + quota("orecchie", "spessore_x_mm") / 2)
        yy = quota("orecchie", "asse_fori_y_mm")
        zz = quota("orecchie", "asse_fori_z_mm")
        foro = cq.Solid.makeCylinder(quota("orecchie", "diametro_fori_mm") / 2,
                                    quota("orecchie", "spessore_x_mm") + 4,
                                    cq.Vector(x - quota("orecchie", "spessore_x_mm") / 2 - 2, yy, zz), cq.Vector(1, 0, 0))
        solido = solido.cut(foro).clean()
    assert len(solido.Solids()) == 1 and solido.isValid() and solido.Volume() > 0
    step = STAMPA / f"{NOME}.step"
    stl = STAMPA / f"{NOME}.stl"
    cq.exporters.export(solido, str(step))
    cq.exporters.export(solido, str(QUI / f"{NOME}.brep"))
    cq.exporters.export(solido, str(stl), tolerance=quota("esportazione", "tolleranza_lineare_mesh_mm"),
                        angularTolerance=quota("esportazione", "tolleranza_angolare_mesh_rad"))
    # Riapertura dei derivati, senza riparazioni automatiche della geometria.
    reimportato = cq.importers.importStep(str(step)).val()
    assert reimportato.isValid() and len(reimportato.Solids()) == 1
    mesh = trimesh.load_mesh(stl, process=True)
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume > 0
    assert len(mesh.split(only_watertight=False)) == 1
    assert np.all(mesh.area_faces > 1e-12)
    traslazione = crea_3mf(mesh, STAMPA / "BOZZA_R03_GEOMETRIA.3mf")
    mesh_glb = mesh.copy()
    mesh_glb.apply_scale(0.001)  # glTF usa metri; STL/STEP/3MF sono in mm.
    mesh_glb.visual = trimesh.visual.ColorVisuals(mesh_glb, face_colors=[50, 115, 180, 255])
    scena = trimesh.Scene(mesh_glb)
    scena.metadata.update({"revisione": NOME, "stato": P["stato"], "unita": "metri", "origine_quote": "ASSUNTE in mm"})
    (STAMPA / f"{NOME}.glb").write_bytes(scena.export(file_type="glb"))
    bbox = solido.BoundingBox()
    rapporto = {
        "revisione": NOME, "stato": P["stato"], "unita_CAD_STL_3MF": "mm", "unita_GLB": "m",
        "scala_GLB_da_mm": 0.001,
        "volume_CAD_mm3": solido.Volume(), "volume_STL_mm3": mesh.volume,
        "bounds_CAD_mm": [[bbox.xmin, bbox.ymin, bbox.zmin], [bbox.xmax, bbox.ymax, bbox.zmax]],
        "bounds_STL_mm": mesh.bounds.tolist(), "ingombro_STL_mm": mesh.extents.tolist(),
        "solidi_CAD": len(solido.Solids()), "CAD_valido": solido.isValid(),
        "STEP_riaperto_valido": reimportato.isValid(), "STEP_solidi": len(reimportato.Solids()),
        "sovrapposizioni_prima_fusione": contatti, "raccordi_verticali_applicati": len(giunti),
        "STL_chiusa": mesh.is_watertight, "STL_normali_coerenti": mesh.is_winding_consistent,
        "STL_componenti": len(mesh.split(only_watertight=False)), "STL_facce_degeneri": int(np.sum(mesh.area_faces <= 1e-12)),
        "STL_vertici": len(mesh.vertices), "STL_triangoli": len(mesh.faces),
        "traslazione_3MF_mm": traslazione,
        "nota_verifiche": "Controlli sorgente e riapertura STEP/STL. Le verifiche indipendenti sono separate. Nessuno slicing e nessuna prova funzionale, di resistenza o montaggio.",
        "dipendenze": {nome: importlib.metadata.version(nome) for nome in ("cadquery", "cadquery-ocp", "numpy", "trimesh")},
        "sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(STAMPA.glob("*")) if p.is_file()},
    }
    (QUI / "report_generazione.json").write_text(json.dumps(rapporto, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(rapporto, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    principale()
