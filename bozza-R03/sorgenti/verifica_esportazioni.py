#!/usr/bin/env python3
"""Controlli indipendenti sugli esportati R03; non importa il generatore CAD.

Solo quote nominali della bozza: nessun controllo di compatibilita con il casco,
comfort, resistenza, temperatura, montabilita o comportamento della stampa.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import cadquery as cq
import manifold3d
import numpy as np
import trimesh
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from scipy.spatial import cKDTree
from shapely.geometry import Polygon


def self_intersections(mesh):
    """Screening derivato dal verificatore DiscoX Cage R02, non adiacenti.

    Esclude le coppie che condividono un vertice. Non e una prova CAD completa.
    """
    tri = mesh.triangles
    bounds_all = np.c_[tri.min(axis=1), tri.max(axis=1)]
    try:
        tree = mesh.triangles_tree
    except ImportError:
        tree = None
    pairs = []
    for i, bounds in enumerate(bounds_all):
        overlapping = tree.intersection(bounds) if tree is not None else np.flatnonzero(
            np.all(bounds_all[:, :3] <= bounds[3:] + 1e-8, axis=1)
            & np.all(bounds_all[:, 3:] >= bounds[:3] - 1e-8, axis=1))
        for j in overlapping:
            if j <= i or np.intersect1d(mesh.faces[i], mesh.faces[j]).size:
                continue
            pairs.append((i, j))
    hits = []
    eps = 1e-7
    for i, j in pairs:
        a, b = tri[i], tri[j]
        na = np.cross(a[1] - a[0], a[2] - a[0])
        nb = np.cross(b[1] - b[0], b[2] - b[0])
        la, lb = np.linalg.norm(na), np.linalg.norm(nb)
        if la < eps or lb < eps:
            continue
        na /= la
        nb /= lb
        if np.linalg.norm(np.cross(na, nb)) < eps:
            if np.max(np.abs((b - a[0]) @ na)) > eps:
                continue
            axis = int(np.argmax(np.abs(na)))
            aa, bb = np.delete(a, axis, 1), np.delete(b, axis, 1)
            area = Polygon(aa).intersection(Polygon(bb)).area
            if area > 1e-7:
                hits.append({"facce": [int(i), int(j)], "tipo": "sovrapposizione_coplanare", "area_proiettata_mm2": float(area)})
            continue
        found = False
        for first, second in [(a, b), (b, a)]:
            e1, e2 = second[1] - second[0], second[2] - second[0]
            for k in range(3):
                origin, delta = first[k], first[(k + 1) % 3] - first[k]
                p = np.cross(delta, e2)
                determinant = e1 @ p
                if abs(determinant) < eps:
                    continue
                tv = origin - second[0]
                u = (tv @ p) / determinant
                q = np.cross(tv, e1)
                v = (delta @ q) / determinant
                t = (e2 @ q) / determinant
                if -eps <= u <= 1 + eps and -eps <= v and u + v <= 1 + eps and eps < t < 1 - eps:
                    found = True
                    break
            if found:
                break
        if found:
            hits.append({"facce": [int(i), int(j)], "tipo": "attraversamento"})
    return {
        "coppie_candidate_senza_vertici_comuni": len(pairs),
        "coppie_con_intersezione": len(hits), "esempi": hits[:20],
        "limite": "Coppie con vertice comune escluse; screening della mesh esportata, non prova CAD completa.",
        "metodo": "Broadphase AABB, segmento-triangolo per non coplanari e area proiettata per coplanari; derivato dal verificatore locale DiscoX Cage R02.",
    }


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mesh_metrics(mesh):
    _, counts = np.unique(mesh.edges_sorted, axis=0, return_counts=True)
    _, face_counts = np.unique(np.sort(mesh.faces, axis=1), axis=0, return_counts=True)
    mf = manifold3d.Manifold(manifold3d.Mesh(
        np.asarray(mesh.vertices, dtype=np.float32),
        np.asarray(mesh.faces, dtype=np.uint32)))
    return {
        "vertici": len(mesh.vertices), "triangoli": len(mesh.faces),
        "limiti_mm": mesh.bounds.tolist(), "dimensioni_mm": mesh.extents.tolist(),
        "volume_mm3": float(mesh.volume), "volume_positivo": bool(mesh.volume > 0),
        "mesh_chiusa": bool(mesh.is_watertight), "normali_coerenti": bool(mesh.is_winding_consistent),
        "corpi_connessi": len(mesh.split(only_watertight=False)),
        "spigoli_incidenza_diversa_da_2": int(np.count_nonzero(counts != 2)),
        "facce_duplicate": int(np.sum(face_counts - 1)),
        "facce_degeneri_area_inferiore_1e-10": int(np.count_nonzero(mesh.area_faces < 1e-10)),
        "vertici_finiti": bool(np.isfinite(mesh.vertices).all()),
        "manifold_importazione": {"stato": str(mf.status()), "volume_mm3": float(mf.volume())},
    }


def compare_mesh(a, b, tolerance=1e-4):
    """Confronta vertici saldati e facce, anche se gli indici cambiano."""
    distances, mapping = cKDTree(a.vertices).query(b.vertices, k=1)
    vertices_match = (len(a.vertices) == len(b.vertices)
                      and len(np.unique(mapping)) == len(a.vertices)
                      and np.max(distances) <= tolerance)
    def faces_canonical(f):
        return sorted(tuple(sorted(tri)) for tri in f)
    return {
        "tolleranza_coordinate_mm": tolerance,
        "massima_distanza_vertici_mm": float(np.max(distances)),
        "corrispondenza_vertici_biunivoca": bool(len(np.unique(mapping)) == len(a.vertices) == len(b.vertices)),
        "limiti_coincidenti": bool(np.allclose(a.bounds, b.bounds, atol=tolerance, rtol=0)),
        "numero_triangoli_coincidente": bool(len(a.faces) == len(b.faces)),
        "vertici_coincidenti": bool(vertices_match),
        "triangoli_coincidenti": bool(vertices_match and len(a.faces) == len(b.faces) and faces_canonical(a.faces) == faces_canonical(mapping[b.faces])),
        "differenza_volume_mm3": float(a.volume - b.volume),
    }


def bounds_cad(shape):
    b = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape.wrapped, b, False, False)
    xmin, ymin, zmin, xmax, ymax, zmax = b.Get()
    return np.array([[xmin, ymin, zmin], [xmax, ymax, zmax]])


def line_sections(shape, origin, end):
    result = shape.intersect(cq.Edge.makeLine(cq.Vector(*origin), cq.Vector(*end)))
    return [{"estremi_mm": [e.startPoint().toTuple(), e.endPoint().toTuple()], "lunghezza_mm": e.Length()} for e in result.Edges()]


def nominal_cad_checks(shape):
    cylinders = []
    for face in shape.Faces():
        if face.geomType() != "CYLINDER":
            continue
        surface = face._geomAdaptor()
        axis = surface.Axis()
        direction = np.array([axis.Direction().X(), axis.Direction().Y(), axis.Direction().Z()])
        location = np.array([axis.Location().X(), axis.Location().Y(), axis.Location().Z()])
        if abs(surface.Radius() - 2.25) <= 1e-6 and abs(abs(direction[0]) - 1) <= 1e-6:
            cylinders.append({"raggio_mm": surface.Radius(), "punto_asse_mm": location.tolist(), "direzione_asse": direction.tolist(), "limiti_mm": bounds_cad(face).tolist()})
    target = [c for c in cylinders if np.allclose(np.array(c["punto_asse_mm"])[1:], [50, 8], atol=1e-6, rtol=0)]
    hole_test = {"nominale": "Due fori con asse X, y=50 mm, z=8 mm, raggio=2.25 mm; tutte quote assunte.", "superfici_cilindriche_trovate": cylinders, "superfici_corrispondenti": len(target), "due_fori_nominali": len(target) == 2}
    gap = None
    if len(target) == 2:
        ordered = sorted(target, key=lambda c: c["limiti_mm"][0][0])
        gap = ordered[1]["limiti_mm"][0][0] - ordered[0]["limiti_mm"][1][0]
    hole_test["luce_fra_facce_interne_ricavata_dai_cilindri_mm"] = gap
    hole_test["luce_nominale_68_mm"] = bool(gap is not None and abs(gap - 68) <= 1e-6)
    hole_test["intersezione_linea_asse_fori"] = line_sections(shape, [-100, 50, 8], [100, 50, 8])
    # L'asse mediano x=0 attraversa il ponte curvo, lontano dai raccordi.
    bridge = line_sections(shape, [0, -150, 6], [0, 150, 6])
    return {
        "fori_e_luce_U": hole_test,
        "ponte_centrale": {"sezione_CAD": bridge, "nominale_spessore_radiale_mm": 1.2,
            "una_sezione_di_1_2_mm": bool(len(bridge) == 1 and abs(bridge[0]["lunghezza_mm"] - 1.2) <= 1e-6),
            "limite": "Sezione sull'asse mediano; non e una verifica di spessore globale o resistenza."},
        "limite": "Quote confrontate solo con i nominali assunti della bozza, senza rilievi di casco o torcia.",
    }


def transform_3mf(raw):
    out = np.eye(4)
    if raw is not None:
        vals = np.array([float(v) for v in raw.split()])
        if len(vals) != 12:
            raise ValueError("Trasformazione 3MF non composta da 12 numeri")
        out[:3, :3] = vals[:9].reshape(3, 3).T
        out[:3, 3] = vals[9:]
    return out


def inspect_3mf(path, stl):
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with zipfile.ZipFile(path) as z:
        corrupt = z.testzip()
        model_files = [p for p in z.namelist() if p.lower().endswith(".model")]
        root = ET.fromstring(z.read("3D/3dmodel.model"))
        objects = root.findall("m:resources/m:object", ns)
        builds = root.findall("m:build/m:item", ns)
        output = {"file": path.name, "sha256": digest(path), "ZIP_senza_errori_CRC": corrupt is None,
            "unita": root.get("unit"), "file_model": model_files, "oggetti": len(objects), "elementi_build": len(builds),
            "file_relazioni_presente": "_rels/.rels" in z.namelist(), "elementi": [],
            "tipo": "3MF geometrico; nessuna prova di progetto slicer o profili macchina."}
        byid = {o.get("id"): o for o in objects}
        expected = stl.copy()
        stl_center = stl.bounds.mean(axis=0)
        offset = np.array([128 - stl_center[0], 128 - stl_center[1], -stl.bounds[0, 2]])
        expected.apply_translation(offset)
        output["posizionamento_atteso"] = {"centro_ingombro_XY_mm": [128, 128], "z_minimo_mm": 0,
            "traslazione_attesa_rispetto_STL_mm": offset.tolist()}
        for item in builds:
            obj = byid[item.get("objectid")]
            element = obj.find("m:mesh", ns)
            if element is None:
                raise ValueError("Atteso un solo oggetto mesh diretto, trovati componenti")
            vertices = [[float(v.get(c)) for c in ["x", "y", "z"]] for v in element.findall("m:vertices/m:vertex", ns)]
            faces = [[int(f.get(c)) for c in ["v1", "v2", "v3"]] for f in element.findall("m:triangles/m:triangle", ns)]
            transformation = transform_3mf(item.get("transform"))
            mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)
            mesh.apply_transform(transformation)
            output["elementi"].append({"id_oggetto": obj.get("id"), "trasformazione": transformation.tolist(),
                "trasformazione_finita": bool(np.isfinite(transformation).all()), "determinante_trasformazione": float(np.linalg.det(transformation[:3, :3])),
                "metriche": mesh_metrics(mesh), "confronto_STL_posizionato_sul_piatto": compare_mesh(expected, mesh)})
        return output


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--progetto", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    project = args.progetto.resolve()
    output = args.output or project / "verifiche/verifica_indipendente.json"
    report = {"revisione": "R03", "data_UTC": datetime.now(timezone.utc).isoformat(),
        "stato": "incompleto", "scopo": "Verifica indipendente dei file finali riaperti, senza importare il generatore.",
        "versioni": {p: importlib.metadata.version(p) for p in ["cadquery", "trimesh", "manifold3d", "numpy", "shapely"]},
        "controlli": {}, "limiti": ["Bozza di forma con quote assunte, non supporto funzionale pronto per la stampa.",
            "Compatibilita casco/torcia, montabilita, comfort, carichi, calore e prova fisica non verificati.",
            "Nessuno slicing o percorso di estrusione verificato da questo script."]}
    failures = []
    def check(name, condition):
        report["controlli"][name] = bool(condition)
        if not condition:
            failures.append(name)
    try:
        folder = project / "stampa"
        stls = sorted(folder.glob("*.stl"))
        steps = sorted(folder.glob("*.step")) + sorted(folder.glob("*.stp"))
        three_mfs = sorted(folder.glob("*.3mf"))
        check("un_solo_STL", len(stls) == 1)
        check("un_solo_STEP", len(steps) == 1)
        check("un_solo_3MF_geometrico", len(three_mfs) == 1)
        if not stls or not steps or not three_mfs:
            raise FileNotFoundError("Esportazioni STL, STEP o 3MF non ancora disponibili")
        raw = trimesh.load_mesh(stls[0], process=False)
        mesh = trimesh.load_mesh(stls[0], process=True)
        info = mesh_metrics(mesh)
        info.update({"file": stls[0].name, "sha256": digest(stls[0]), "facce_STL_prima_saldatura": len(raw.faces),
            "nota_importazione": "Saldatura dei vertici coincidenti con process=True; nessuna riparazione, rimozione facce o inversione delle normali eseguita.",
            "autointersezioni_screening": self_intersections(mesh)})
        report["STL"] = info
        check("STL_un_corpo", info["corpi_connessi"] == 1)
        for key in ["mesh_chiusa", "normali_coerenti", "volume_positivo", "vertici_finiti"]:
            check("STL_" + key, info[key])
        for key in ["spigoli_incidenza_diversa_da_2", "facce_duplicate", "facce_degeneri_area_inferiore_1e-10"]:
            check("STL_" + key + "_zero", info[key] == 0)
        check("STL_nessuna_faccia_rimossa", len(raw.faces) == len(mesh.faces))
        check("STL_manifold_import_NoError", info["manifold_importazione"]["stato"] == "Error.NoError")
        check("STL_autointersezioni_screening_zero", info["autointersezioni_screening"]["coppie_con_intersezione"] == 0)
        step = cq.importers.importStep(str(steps[0]))
        solids = step.solids().vals()
        shape = step.val()
        step_info = {"file": steps[0].name, "sha256": digest(steps[0]), "solidi": len(solids),
            "forma_valida": bool(shape.isValid()), "volume_mm3": float(shape.Volume()), "limiti_mm": bounds_cad(shape).tolist(),
            "metodo_limiti": "OCCT BRepBndLib.AddOptimal, senza triangolazione e senza espansione per tolleranze di forma.",
            "confronto_STL": {"tolleranza_limiti_mm": 0.05, "limiti_coincidenti": bool(np.allclose(bounds_cad(shape), mesh.bounds, atol=0.05, rtol=0)),
                "differenza_volume_mm3": float(shape.Volume() - mesh.volume), "errore_relativo_volume": float(abs(shape.Volume() - mesh.volume) / shape.Volume()),
                "tolleranza_relativa_volume": 0.002}}
        report["STEP"] = step_info
        check("STEP_un_solido_valido", len(solids) == 1 and shape.isValid() and shape.Volume() > 0)
        check("STEP_limiti_coincidenti_STL", step_info["confronto_STL"]["limiti_coincidenti"])
        check("STEP_volume_coincidente_STL", step_info["confronto_STL"]["errore_relativo_volume"] <= 0.002)
        nominal = nominal_cad_checks(shape)
        report["quote_nominali_su_STEP"] = nominal
        check("due_fori_nominali_r2_25_y50_z8", nominal["fori_e_luce_U"]["due_fori_nominali"])
        check("luce_U_nominale_68", nominal["fori_e_luce_U"]["luce_nominale_68_mm"])
        check("ponte_nominale_1_2_al_centro", nominal["ponte_centrale"]["una_sezione_di_1_2_mm"])
        check("linea_asse_fori_libera", len(nominal["fori_e_luce_U"]["intersezione_linea_asse_fori"]) == 0)
        report["3MF"] = inspect_3mf(three_mfs[0], mesh)
        th = report["3MF"]
        check("3MF_struttura_un_oggetto_un_build_mm", th["ZIP_senza_errori_CRC"] and th["unita"] == "millimeter" and th["oggetti"] == 1 and th["elementi_build"] == 1)
        for index, element in enumerate(th["elementi"]):
            compare = element["confronto_STL_posizionato_sul_piatto"]
            check(f"3MF_elemento_{index}_trasformazione_valida", element["trasformazione_finita"] and abs(element["determinante_trasformazione"] - 1) < 1e-8)
            check(f"3MF_elemento_{index}_geometria_coincidente_STL", all(compare[k] for k in ["limiti_coincidenti", "numero_triangoli_coincidente", "vertici_coincidenti", "triangoli_coincidenti"]))
        glbs = sorted(folder.glob("*.glb"))
        if glbs:
            scene = trimesh.load(glbs[0], force="scene", process=False)
            glb = scene.to_geometry()
            glb.merge_vertices()
            glb.apply_scale(1000)
            report["GLB"] = {"file": glbs[0].name, "sha256": digest(glbs[0]), "nodi_geometria": len(scene.graph.nodes_geometry),
                "unita_dichiarata_glTF": "meter", "fattore_conversione_in_mm": 1000,
                "confronto_STL": compare_mesh(mesh, glb), "nota": "File di visualizzazione; conversione da metri glTF a millimetri per il confronto."}
            check("GLB_geometria_coincidente_STL", report["GLB"]["confronto_STL"]["triangoli_coincidenti"])
        report["stato"] = "verifiche_geometriche_superate_bozza_non_funzionale" if not failures else "controlli_non_superati"
    except Exception as exc:
        report["errore"] = {"tipo": type(exc).__name__, "messaggio": str(exc)}
        failures.append("eccezione")
    report["controlli_non_superati"] = failures
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"report": str(output), "stato": report["stato"], "controlli_non_superati": failures}, ensure_ascii=False))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
