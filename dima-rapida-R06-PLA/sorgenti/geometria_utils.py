#!/usr/bin/env python3
"""Verifica indipendente degli esportati PROVA R05 PLA; nessuna prova funzionale.

Helper geometrici copiati dal verificatore R03, senza importare il generatore.
Il manifest descrive solo convenzioni nominali e trasformazioni di esportazione.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import itertools
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
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.gp import gp_Trsf
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

def transform_3mf(raw):
    out = np.eye(4)
    if raw is not None:
        vals = np.array([float(v) for v in raw.split()])
        if len(vals) != 12:
            raise ValueError("Trasformazione 3MF non composta da 12 numeri")
        out[:3, :3] = vals[:9].reshape(3, 3).T
        out[:3, 3] = vals[9:]
    return out


def manifold_from_mesh(mesh):
    return manifold3d.Manifold(manifold3d.Mesh(
        np.asarray(mesh.vertices, dtype=np.float32),
        np.asarray(mesh.faces, dtype=np.uint32)))


def cad_metrics(path):
    workplane = cq.importers.importStep(str(path))
    shape = workplane.val()
    return shape, {"file": path.name, "sha256": digest(path),
        "solidi": len(shape.Solids()), "forma_valida": bool(shape.isValid()),
        "volume_mm3": float(shape.Volume()), "limiti_mm": bounds_cad(shape).tolist(),
        "metodo_limiti": "OCCT BRepBndLib.AddOptimal senza triangolazione o espansione per tolleranze."}


def transform_cad_rigid(shape, matrix):
    """Trasformazione nativa: evita GTrsf con forma non inizializzata CQ/OCP."""
    trsf = gp_Trsf()
    trsf.SetValues(*np.asarray(matrix, float)[:3, :].reshape(-1).tolist())
    return cq.Shape.cast(BRepBuilderAPI_Transform(shape.wrapped, trsf, True).Shape())


def compare_sampled_surfaces(a, b, tolerance=1e-4):
    """Ammette triangolazioni diverse delle stesse facce dopo posa rigida."""
    distances_a = trimesh.proximity.closest_point(b, a.triangles_center)[1]
    distances_b = trimesh.proximity.closest_point(a, b.triangles_center)[1]
    maximum = float(max(distances_a.max(), distances_b.max()))
    return {"campioni_centroidi_per_direzione": [len(distances_a), len(distances_b)],
        "distanza_massima_mm": maximum, "tolleranza_mm": tolerance, "coincide": maximum <= tolerance,
        "limite": "Distanza campionata bidirezionale, usata insieme a vertici biunivoci e trasformazione CAD."}


def cad_cylinders(shape):
    output = []
    for face in shape.Faces():
        if face.geomType() != "CYLINDER":
            continue
        surface = face._geomAdaptor()
        axis = surface.Axis()
        output.append({"raggio_mm": float(surface.Radius()),
            "punto_asse_mm": [axis.Location().X(), axis.Location().Y(), axis.Location().Z()],
            "direzione_asse": [axis.Direction().X(), axis.Direction().Y(), axis.Direction().Z()],
            "limiti_mm": bounds_cad(face).tolist()})
    return output


def axis_matches(cylinder, point, direction, radius, tolerance=1e-5):
    direction = np.asarray(direction, float)
    direction /= np.linalg.norm(direction)
    found_direction = np.asarray(cylinder["direzione_asse"], float)
    difference = np.asarray(cylinder["punto_asse_mm"], float) - point
    return (abs(cylinder["raggio_mm"] - radius) <= tolerance
            and abs(abs(found_direction @ direction) - 1) <= tolerance
            and np.linalg.norm(np.cross(difference, direction)) <= tolerance)


def read_3mf(path):
    """Legge risorse e trasformazioni effettive, senza usare lo slicer."""
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with zipfile.ZipFile(path) as package:
        root = ET.fromstring(package.read("3D/3dmodel.model"))
        objects = root.findall("m:resources/m:object", ns)
        builds = root.findall("m:build/m:item", ns)
        rows = []
        byid = {o.get("id"): o for o in objects}
        for item in builds:
            obj = byid[item.get("objectid")]
            element = obj.find("m:mesh", ns)
            if element is None:
                raise ValueError("Attese mesh dirette, non componenti 3MF o riferimenti esterni")
            vertices = [[float(v.get(c)) for c in ["x", "y", "z"]] for v in element.findall("m:vertices/m:vertex", ns)]
            faces = [[int(f.get(c)) for c in ["v1", "v2", "v3"]] for f in element.findall("m:triangles/m:triangle", ns)]
            local = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)
            transform = transform_3mf(item.get("transform"))
            world = local.copy()
            world.apply_transform(transform)
            rows.append({"id": obj.get("id"), "nome": obj.get("name"), "locale": local,
                "mondo": world, "trasformazione": transform})
        return {"file": path.name, "sha256": digest(path), "unita": root.get("unit"),
            "numero_oggetti": len(objects), "numero_build": len(builds),
            "ZIP_CRC_valido": package.testzip() is None,
            "nomi_model": [p for p in package.namelist() if p.lower().endswith(".model")],
            "tipo": "3MF geometrico; nessun profilo macchina, materiale o percorso di estrusione."}, rows


def entries(value):
    if isinstance(value, list):
        return [(str(row.get("id", row.get("nome", index))), row) for index, row in enumerate(value)]
    if isinstance(value, dict):
        return [(str(key), row) for key, row in value.items()]
    raise ValueError("Manifest: elenco pezzi/riferimenti non riconosciuto")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--progetto", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--manifest", type=Path)
    ap.add_argument("--riusa-screening-identici", action="store_true",
                    help="Riusa solo screening gia completati per STL con SHA256 identico; riapre e controlla tutti i file.")
    args = ap.parse_args()
    root = args.progetto.resolve()
    manifest_path = args.manifest or root / "sorgenti/manifest.json"
    output = root / "verifiche/verifica_indipendente.json"
    cached = json.loads(output.read_text()) if args.riusa_screening_identici and output.exists() else {}
    report = {"revisione": "PROVA_R05_PLA_NON_PORTANTE", "data_UTC": datetime.now(timezone.utc).isoformat(),
        "stato": "incompleto", "controlli": {}, "pezzi": {}, "riferimenti": {},
        "versioni": {p: importlib.metadata.version(p) for p in ["cadquery", "trimesh", "manifold3d", "numpy", "scipy", "shapely"]},
        "limiti": ["PROVA DI FORMA PLA BASIC NON PORTANTE: tutte le quote geometriche sono assunte.",
            "Piastra interna unica con fascia da 1.2 mm: solo dima, non componente portante validato.",
            "Casco, feritoie, schiuma e girotesta reali non sono modellati o verificati.",
            "Montaggio reale, appoggi, resistenza, calore, comfort, freddo e immersione non verificati.",
            "Questo report verifica geometria esportata; slicing e percorsi vengono verificati separatamente.",
            "Le verifiche digitali non trasformano la prova di forma in un supporto idoneo all uso con la torcia."]}
    failed = []
    def check(name, condition):
        report["controlli"][name] = bool(condition)
        if not condition:
            failed.append(name)
    def pathof(value):
        return root / value
    try:
        manifest = json.loads(manifest_path.read_text())
        report["manifest"] = {"file": str(manifest_path.relative_to(root)), "sha256": digest(manifest_path)}
        parameters_path = root / "sorgenti/parametri_assunti.json"
        parameters = json.loads(parameters_path.read_text())
        report["parametri_assunti"] = {"file": str(parameters_path.relative_to(root)), "sha256": digest(parameters_path),
            "origine": "Assunzioni del modello, non quote del casco o del prodotto reale."}
        snapshot_paths = {manifest_path, parameters_path}
        for optional_name in ["genera_modello.py", "report_generazione.json"]:
            optional_path = root / "sorgenti" / optional_name
            if optional_path.exists():
                snapshot_paths.add(optional_path)
        for _, item in entries(manifest["pezzi"]) + entries(manifest.get("riferimenti", [])):
            for key in ["stl_stampa", "step_stampa", "stl_assieme", "step_assieme"]:
                if key in item:
                    snapshot_paths.add(pathof(item[key]))
        for key in ["step", "glb"]:
            if key in manifest.get("assieme", {}):
                snapshot_paths.add(pathof(manifest["assieme"][key]))
        if "piatto_geometrico" in manifest:
            snapshot_paths.add(pathof(manifest["piatto_geometrico"]["file"]))
        snapshot_hashes = {str(path.relative_to(root)): digest(path) for path in sorted(snapshot_paths)}
        def nominal(group, key):
            return parameters[group][key]["valore"]
        parts = entries(manifest["pezzi"])
        check("due_pezzi_nuovi_nel_manifest", len(parts) == 2)
        check("identita_due_pezzi_attese", {identifier for identifier, _ in parts} == {"base", "piastra_interna"})
        check("quantita_uno_per_pezzo", all(part.get("quantita") == 1 for _, part in parts))
        print_meshes, assembly_shapes, print_shapes, assembly_meshes = {}, {}, {}, {}
        for identifier, part in parts:
            print("verifica", identifier, flush=True)
            stl_print_path, step_print_path = pathof(part["stl_stampa"]), pathof(part["step_stampa"])
            stl_assembly_path, step_assembly_path = pathof(part["stl_assieme"]), pathof(part["step_assieme"])
            raw = trimesh.load_mesh(stl_print_path, process=False)
            mesh = trimesh.load_mesh(stl_print_path, process=True)
            assembly_mesh = trimesh.load_mesh(stl_assembly_path, process=True)
            info = mesh_metrics(mesh)
            cached_stl = cached.get("pezzi", {}).get(identifier, {}).get("STL_stampa", {})
            if cached_stl.get("sha256") == digest(stl_print_path) and "autointersezioni_screening" in cached_stl:
                screen = dict(cached_stl["autointersezioni_screening"])
                screen["riusato_su_STL_SHA256_identico"] = True
            else:
                screen = self_intersections(mesh)
                screen["riusato_su_STL_SHA256_identico"] = False
            info.update({"file": str(stl_print_path.relative_to(root)), "sha256": digest(stl_print_path),
                "facce_prima_saldatura": len(raw.faces), "autointersezioni_screening": screen,
                "nota_importazione": "Solo saldatura vertici coincidenti; nessuna riparazione, rimozione facce o inversione normali.",
                "assemblato_file": str(stl_assembly_path.relative_to(root)), "assemblato_sha256": digest(stl_assembly_path)})
            shape_print, step_info = cad_metrics(step_print_path)
            shape_assembly, assembly_step_info = cad_metrics(step_assembly_path)
            transform = np.asarray(part["matrice_stampa_da_assieme"], float)
            restored = mesh.copy()
            restored.apply_transform(np.linalg.inv(transform))
            compare_assembly = compare_mesh(restored, assembly_mesh)
            surface_comparison = compare_sampled_surfaces(restored, assembly_mesh)
            transformed_cad = transform_cad_rigid(shape_assembly, transform)
            common_volume = float(transformed_cad.intersect(shape_print).Volume())
            symmetric_difference = abs(transformed_cad.Volume() + shape_print.Volume() - 2 * common_volume)
            step_info["confronto_STL"] = {"tolleranza_limiti_mm": .05,
                "limiti_coincidenti": bool(np.allclose(bounds_cad(shape_print), mesh.bounds, atol=.05, rtol=0)),
                "errore_relativo_volume": float(abs(shape_print.Volume() - mesh.volume) / shape_print.Volume()),
                "tolleranza_relativa_volume": .002}
            assembly_step_info["confronto_STL"] = {"limiti_coincidenti": bool(np.allclose(bounds_cad(shape_assembly), assembly_mesh.bounds, atol=.05, rtol=0)),
                "errore_relativo_volume": float(abs(shape_assembly.Volume() - assembly_mesh.volume) / shape_assembly.Volume())}
            report["pezzi"][identifier] = {"STL_stampa": info, "STEP_stampa": step_info, "STEP_assieme": assembly_step_info,
                "matrice_stampa_da_assieme": transform.tolist(), "trasformazione_inversa_confronto_STL_assieme": compare_assembly,
                "confronto_superfici_STL_assieme_stampa": surface_comparison,
                "confronto_CAD_assieme_trasformato": {"volume_differenza_simmetrica_mm3": symmetric_difference,
                    "tolleranza_relativa": 1e-5, "coincide": symmetric_difference / shape_print.Volume() < 1e-5},
                "cilindri_STEP_assieme": cad_cylinders(shape_assembly)}
            print_meshes[identifier] = mesh
            print_shapes[identifier] = shape_print
            assembly_shapes[identifier] = shape_assembly
            assembly_meshes[identifier] = assembly_mesh
            prefix = identifier + ":"
            check(prefix + "un_corpo", info["corpi_connessi"] == 1)
            for key in ["mesh_chiusa", "normali_coerenti", "volume_positivo", "vertici_finiti"]:
                check(prefix + key, info[key])
            for key in ["spigoli_incidenza_diversa_da_2", "facce_duplicate", "facce_degeneri_area_inferiore_1e-10"]:
                check(prefix + key + "_zero", info[key] == 0)
            check(prefix + "nessuna_faccia_rimossa", len(raw.faces) == len(mesh.faces))
            check(prefix + "manifold_NoError", info["manifold_importazione"]["stato"] == "Error.NoError")
            check(prefix + "screening_autointersezioni_zero", info["autointersezioni_screening"]["coppie_con_intersezione"] == 0)
            check(prefix + "STEP_stampa_un_solido_valido", step_info["solidi"] == 1 and step_info["forma_valida"] and step_info["volume_mm3"] > 0)
            check(prefix + "STEP_assieme_un_solido_valido", assembly_step_info["solidi"] == 1 and assembly_step_info["forma_valida"] and assembly_step_info["volume_mm3"] > 0)
            check(prefix + "STEP_stampa_coincide_STL", step_info["confronto_STL"]["limiti_coincidenti"] and step_info["confronto_STL"]["errore_relativo_volume"] <= .002)
            check(prefix + "STEP_assieme_coincide_STL", assembly_step_info["confronto_STL"]["limiti_coincidenti"] and assembly_step_info["confronto_STL"]["errore_relativo_volume"] <= .002)
            check(prefix + "trasformazione_rigida_finita", transform.shape == (4, 4) and np.isfinite(transform).all()
                  and np.allclose(transform[3], [0, 0, 0, 1], atol=1e-10)
                  and np.allclose(transform[:3, :3].T @ transform[:3, :3], np.eye(3), atol=1e-10)
                  and abs(np.linalg.det(transform[:3, :3]) - 1) < 1e-10)
            check(prefix + "trasformazione_STL_assieme_stampa_coerente", compare_assembly["vertici_coincidenti"] and surface_comparison["coincide"])
            check(prefix + "trasformazione_CAD_assieme_stampa_coerente", symmetric_difference / shape_print.Volume() < 1e-5)
            # Assi nominali dei fissaggi base-fermi, definiti dal contract R05; assunzioni, non rilievi del casco.
            center_x = bounds_cad(shape_assembly).mean(axis=0)[0]
            targets_x = [-42, 42] if abs(center_x) < 1 else [42 if center_x > 0 else -42]
            axes = []
            for target_x in targets_x:
                found = [cy for cy in cad_cylinders(shape_assembly)
                         if axis_matches(cy, [target_x, 0, 23], [0, 1, 0], nominal("collegamento_piastra", "diametro_passante_mm") / 2)]
                axes.append({"punto_asse_nominale_mm": [target_x, 0, 23], "direzione": [0, 1, 0],
                    "cilindri_corrispondenti": found})
                check(prefix + f"asse_fissaggio_assunto_x{target_x}_z23", bool(found))
            report["pezzi"][identifier]["assi_fissaggi_nominali"] = axes
        base_id = max(assembly_shapes, key=lambda identifier: assembly_shapes[identifier].Volume())
        base = assembly_shapes[base_id]
        extra_axes = []
        for x in nominal("farfalla_schematica", "asole_laterali_assi_x_mm"):
            found = [cy for cy in cad_cylinders(base) if axis_matches(cy,
                [x, 0, nominal("farfalla_schematica", "asole_laterali_centro_z_mm")], [0, 1, 0], nominal("fissaggio_farfalla", "diametro_passante_mm") / 2)]
            extra_axes.append({"x_mm": x, "cilindri_corrispondenti": found})
            check(f"base_asse_farfalla_assunto_x{x}", bool(found))
        report["base_assi_farfalla"] = extra_axes
        # Tre sonde radiali della fascia continua, lontane dai codoli e bordi.
        plate = assembly_shapes["piastra_interna"]
        radial_mid = nominal("piastra_interna_dima", "raggio_interno_mm") + nominal("piastra_interna_dima", "spessore_radiale_mm") / 2
        nominal_thickness = nominal("piastra_interna_dima", "spessore_radiale_mm")
        curve_center = np.asarray(nominal("base", "centro_curva_xy_mm"), float)
        probe_z = nominal("piastra_interna_dima", "z_min_mm") + nominal("piastra_interna_dima", "altezza_z_mm") / 2
        center = np.r_[curve_center, probe_z]
        dima_sections = []
        for index, angle in enumerate([-.2, 0., .2]):
            direction = np.array([np.sin(angle), np.cos(angle), 0.])
            sections = line_sections(plate, center + (radial_mid - 2) * direction, center + (radial_mid + 2) * direction)
            ok = len(sections) == 1 and abs(sections[0]["lunghezza_mm"] - nominal_thickness) <= 1e-5
            dima_sections.append({"angolo_campione_rad": float(angle), "sezione_CAD": sections,
                "spessore_radiale_nominale_mm": nominal_thickness, "coincide": ok})
            check(f"piastra_unica:spessore_radiale_locale_sonda_{index}", ok)
        report["sezioni_locali_piastra_unica"] = {"campioni": dima_sections,
            "limite": "Solo3sezioni locali lontane dai codoli; non verifica di resistenza o spessore funzionale globale."}
        # Distanza radiale al centro fra faccia esterna piastra e faccia interna
        # base: scenario nominale indipendente dalla misura casco+schiuma.
        radial = np.array([0., 1., 0.])
        base_sections = line_sections(base, center + 100 * radial, center + 125 * radial)
        plate_sections = line_sections(plate, center + 85 * radial, center + 100 * radial)
        gap = None
        if len(base_sections) == len(plate_sections) == 1:
            base_radii = [np.linalg.norm(np.asarray(p)[:2] - curve_center) for p in base_sections[0]["estremi_mm"]]
            plate_radii = [np.linalg.norm(np.asarray(p)[:2] - curve_center) for p in plate_sections[0]["estremi_mm"]]
            gap = min(base_radii) - max(plate_radii)
        expected_gap = nominal("piastra_interna_dima", "gap_radiale_nominale_mm")
        report["gap_radiale_centrale_assunto"] = {"z_sonda_mm": probe_z,
            "sezioni_base": base_sections, "sezioni_piastra": plate_sections,
            "gap_mm": float(gap) if gap is not None else None, "nominale_mm": expected_gap,
            "limite": "Scenario geometrico ASSUNTO; non prova di passaggio, appoggio o compatibilita casco/schiuma."}
        check("gap_radiale_centrale_coerente_assunzione", gap is not None and abs(gap - expected_gap) <= 1e-5)
        collisions = []
        for (aid, a), (bid, b) in itertools.combinations(assembly_shapes.items(), 2):
            volume = float(a.intersect(b).Volume())
            collisions.append({"pezzi": [aid, bid], "volume_intersezione_mm3": volume, "distanza_minima_CAD_mm": float(a.distance(b))})
            check("assieme_" + aid + "_" + bid + "_senza_collisione_volumetrica", volume <= 1e-6)
        report["interferenze_soli_pezzi_nuovi"] = {"coppie": collisions,
            "limite": "Nessun casco reale nel modello. Nessuna prova della traiettoria di montaggio o di contatti con schiuma/testa."}
        three_files = sorted((root / "stampa").glob("*.3mf"))
        check("un_3MF_geometrico", len(three_files) == 1)
        three_info, rows = read_3mf(three_files[0])
        check("3MF_millimetri_2_oggetti_2_build", three_info["ZIP_CRC_valido"] and three_info["unita"] == "millimeter" and three_info["numero_oggetti"] == 2 and three_info["numero_build"] == 2)
        identifiers = list(print_meshes)
        comparisons = [[compare_mesh(print_meshes[identifier], row["locale"]) for identifier in identifiers] for row in rows]
        assignments = [permutation for permutation in itertools.permutations(range(len(identifiers)))
                       if all(comparisons[i][j]["triangoli_coincidenti"] for i, j in enumerate(permutation))]
        check("3MF_contiene_solo_le_due_geometrie_nuove", bool(assignments))
        if not assignments:
            raise ValueError("Geometrie 3MF non riconciliate con STL di stampa")
        def name_score(assignment):
            return sum(str(identifier).lower() in str(rows[i]["nome"]).lower()
                       for i, identifier in enumerate(identifiers[j] for j in assignment))
        assignment = max(assignments, key=name_score)
        three_info["elementi"] = []
        world_shapes = {}
        for index, (row, j) in enumerate(zip(rows, assignment)):
            identifier = identifiers[j]
            transform = row["trasformazione"]
            world = row["mondo"]
            world_shapes[identifier] = transform_cad_rigid(print_shapes[identifier], transform)
            three_info["elementi"].append({"id": row["id"], "nome": row["nome"], "pezzo_STL": identifier,
                "trasformazione": transform.tolist(), "confronto_STL_locale": comparisons[index][j], "metriche_posizionate": mesh_metrics(world)})
            check(f"3MF_{identifier}_trasformazione_rigida", np.isfinite(transform).all() and np.allclose(transform[:3, :3].T @ transform[:3, :3], np.eye(3), atol=1e-9) and abs(np.linalg.det(transform[:3, :3]) - 1) < 1e-9)
            check(f"3MF_{identifier}_su_piano_nominale", abs(world.bounds[0, 2]) <= .05)
            check(f"3MF_{identifier}_nel_volume_solo_nominale_256", np.all(world.bounds[0] >= -.05) and np.all(world.bounds[1] <= 256.05))
        distances = []
        for (aid, a), (bid, b) in itertools.combinations(world_shapes.items(), 2):
            distance = float(a.distance(b))
            volume = float(a.intersect(b).Volume())
            distances.append({"pezzi": [aid, bid], "distanza_minima_CAD_mm": distance, "volume_intersezione_mm3": volume})
            check("3MF_" + aid + "_" + bid + "_separati", distance > .01 and volume <= 1e-6)
        three_info["separazioni"] = distances
        three_info["limite_piatto"] = "Solo ingombri geometrici nel cubo nominale256 mm; margini profilo, brim, supporti, torre e slicing non verificati."
        report["3MF"] = three_info
        principals = dict(assembly_shapes)
        hardware_shapes = {}
        for identifier, ref in entries(manifest.get("riferimenti", [])):
            data = {"ruolo": "RIFERIMENTO VISIVO, NON PEZZO DA STAMPARE"}
            for key in ["stl_assieme", "step_assieme", "stl", "step"]:
                if key in ref:
                    path = pathof(ref[key])
                    data[key] = {"file": str(path.relative_to(root)), "sha256": digest(path)}
            if "stl_assieme" in ref:
                assembly_meshes[identifier] = trimesh.load_mesh(pathof(ref["stl_assieme"]), process=True)
            if "step_assieme" in ref:
                shape, metrics = cad_metrics(pathof(ref["step_assieme"]))
                data["CAD_REF"] = metrics
                if identifier in ["farfalla", "U_metallica", "torcia"]:
                    principals[identifier] = shape
                else:
                    hardware_shapes[identifier] = shape
                check("REF_" + identifier + "_CAD_valido_volume_positivo", metrics["forma_valida"] and metrics["volume_mm3"] > 0)
                if identifier == "farfalla":
                    lines = []
                    for x in nominal("farfalla_schematica", "asole_laterali_assi_x_mm"):
                        z = nominal("farfalla_schematica", "asole_laterali_centro_z_mm")
                        sections = line_sections(shape, [x, -50, z], [x, 50, z])
                        bbox = bounds_cad(shape)
                        within = bbox[0, 0] < x < bbox[1, 0] and bbox[0, 2] < z < bbox[1, 2]
                        lines.append({"x_mm": x, "z_mm": z, "intersezione_CAD": sections, "asse_compreso_nel_profilo_esterno": bool(within)})
                        check(f"farfalla_REF_linea_fissaggio_laterale_x{x}_libera", within and len(sections) == 0)
                    data["assi_asole_laterali_nominali"] = lines
            report["riferimenti"][identifier] = data
        principal_collisions = []
        for (aid, a), (bid, b) in itertools.combinations(principals.items(), 2):
            volume = float(a.intersect(b).Volume())
            principal_collisions.append({"pezzi": [aid, bid], "volume_intersezione_mm3": volume})
            check("assieme_schematico_" + aid + "_" + bid + "_senza_collisione", volume <= 1e-5)
        report["interferenze_assieme_schematico"] = {"coppie": principal_collisions,
            "limite": "Solo posizionamento nominale di base, piastra unica, farfalla, U e corpo REF; hardware di serraggio e contatti reali esclusi."}
        hardware_collisions = []
        for aid, a in principals.items():
            for bid, b in hardware_shapes.items():
                volume = float(a.intersect(b).Volume())
                hardware_collisions.append({"pezzo_nuovo": aid, "ferramenta_REF": bid, "volume_intersezione_mm3": volume})
                check("hardware_" + bid + "_" + aid + "_senza_collisione", volume <= 1e-5)
        report["interferenze_ferramenta_REF_componenti_principali"] = {"coppie": hardware_collisions,
            "limite": "Solo volumi illustrativi senza filetti; include5componenti principali e4gruppi ferramenta. Non verifica ferramenta reale o serraggio."}
        glb_path = pathof(manifest["assieme"]["glb"])
        scene = trimesh.load(glb_path, force="scene", process=False)
        nodes = {}
        check("GLB_numero_nodi_coincide_manifest", len(scene.graph.nodes_geometry) == len(assembly_meshes))
        for node in scene.graph.nodes_geometry:
            transform, geometry_name = scene.graph[node]
            mesh = scene.geometry[geometry_name].copy()
            mesh.apply_transform(transform)
            mesh.merge_vertices()
            mesh.apply_scale(1000)
            if node not in assembly_meshes:
                check("GLB_nodo_" + node + "_noto", False)
                continue
            comparison = compare_mesh(assembly_meshes[node], mesh)
            nodes[node] = {"confronto_STL_assieme_dopo_conversione_metri_mm": comparison}
            check("GLB_" + node + "_coincide_STL_assieme", comparison["triangoli_coincidenti"])
        report["GLB_assieme"] = {"file": str(glb_path.relative_to(root)), "sha256": digest(glb_path),
            "unita_glTF": "meter", "fattore_conversione_mm": 1000, "nodi": nodes,
            "limite": "I nodi REF sono soltanto volumi illustrativi, non parti da stampare o CAD rilevati."}
        final_hashes = {str(path.relative_to(root)): digest(path) for path in sorted(snapshot_paths)}
        report["hash_input_inizio_verifica"] = snapshot_hashes
        report["hash_input_fine_verifica"] = final_hashes
        check("input_esportati_manifest_parametri_immutati_durante_verifica", snapshot_hashes == final_hashes)
        report["stato"] = "geometrie_verificate_prova_di_forma_PLA_non_portante" if not failed else "controlli_non_superati"
    except Exception as exc:
        report["errore"] = {"tipo": type(exc).__name__, "messaggio": str(exc)}
        failed.append("eccezione")
    report["controlli_non_superati"] = failed
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"report": str(output), "stato": report["stato"], "controlli_non_superati": failed}, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
