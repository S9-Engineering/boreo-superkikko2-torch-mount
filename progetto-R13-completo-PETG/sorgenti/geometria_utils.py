#!/usr/bin/env python3
"""Verifica indipendente degli esportati PROVA R05 PETG; nessuna prova funzionale.

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


