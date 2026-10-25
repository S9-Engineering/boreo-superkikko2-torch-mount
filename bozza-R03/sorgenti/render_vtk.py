#!/usr/bin/env python3
"""Viste Z-buffer VTK dallo STL finale, con colori solo esplicativi."""
from pathlib import Path
import json
import math
import numpy as np
import trimesh
import vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray

ROOT = Path(__file__).resolve().parents[1]
BG = np.array([245, 247, 248]) / 255
BLUE = np.array([39, 128, 163], dtype=np.uint8)
ORANGE = np.array([219, 135, 80], dtype=np.uint8)


def main():
    mesh = trimesh.load_mesh(ROOT / 'stampa/BOZZA_R03_NON_USO.stl', process=True)
    centers = mesh.triangles_center
    p=json.loads((ROOT/'sorgenti/parametri_assunti.json').read_text())
    radius=p['ponte']['raggio_centrolinea_mm']['valore']
    chord=p['ponte']['corda_centrolinea_mm']['valore']
    wall=p['ponte']['spessore_radiale_mm']['valore']
    cy = -math.sqrt(radius**2 - (chord / 2)**2)
    radial = np.sqrt(centers[:, 0]**2 + (centers[:, 1] - cy)**2)
    bridge = (np.abs(radial - radius) < wall / 2 + .12) & (np.abs(centers[:, 0]) <= chord / 2 + .7)
    colors = np.where(bridge[:, None], BLUE, ORANGE).astype(np.uint8)
    points = vtk.vtkPoints()
    points.SetData(numpy_to_vtk(mesh.vertices, deep=True))
    cells = vtk.vtkCellArray()
    array = np.column_stack((np.full(len(mesh.faces), 3), mesh.faces)).astype(np.int64).ravel()
    cells.SetCells(len(mesh.faces), numpy_to_vtkIdTypeArray(array, deep=True))
    poly = vtk.vtkPolyData()
    poly.SetPoints(points)
    poly.SetPolys(cells)
    scalars = numpy_to_vtk(colors, deep=True, array_type=vtk.VTK_UNSIGNED_CHAR)
    scalars.SetName('colori_solo_display')
    poly.GetCellData().SetScalars(scalars)
    normals = vtk.vtkPolyDataNormals()
    normals.SetInputData(poly)
    normals.ComputePointNormalsOn()
    normals.ComputeCellNormalsOff()
    normals.SplittingOn()
    normals.SetFeatureAngle(35)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(normals.GetOutputPort())
    mapper.SetScalarModeToUseCellData()
    mapper.SetColorModeToDirectScalars()
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetInterpolationToPhong()
    actor.GetProperty().SetAmbient(.28)
    actor.GetProperty().SetDiffuse(.72)
    actor.GetProperty().SetSpecular(.10)
    actor.GetProperty().SetSpecularPower(30)
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(*BG)
    renderer.AddActor(actor)
    window = vtk.vtkRenderWindow()
    window.SetOffScreenRendering(1)
    window.SetMultiSamples(8)
    window.AddRenderer(renderer)
    out = ROOT / 'anteprime/viste_vtk'
    out.mkdir(parents=True, exist_ok=True)
    center = mesh.bounds.mean(axis=0)
    results = []
    for name, direction, up, size in [
        ('iso', [1.15, -1.3, 1.05], [0, 0, 1], (1600, 1000)),
        ('alto', [0, 0, 1], [0, 1, 0], (1600, 1000)),
        ('lato', [1, 0, 0], [0, 0, 1], (1600, 750)),
    ]:
        direction = np.asarray(direction, float)
        direction /= np.linalg.norm(direction)
        up = np.asarray(up, float)
        right = np.cross(up, direction)
        right /= np.linalg.norm(right)
        real_up = np.cross(direction, right)
        relative = mesh.vertices - center
        projected_x = relative @ right
        projected_y = relative @ real_up
        shift = right * ((projected_x.max() + projected_x.min()) / 2) + real_up * ((projected_y.max() + projected_y.min()) / 2)
        focus = center + shift
        camera = renderer.GetActiveCamera()
        camera.SetFocalPoint(*focus)
        camera.SetPosition(*(focus + direction * 400))
        camera.SetViewUp(*real_up)
        camera.ParallelProjectionOn()
        aspect = size[0] / size[1]
        camera.SetParallelScale(max(np.ptp(projected_y) / 2, np.ptp(projected_x) / (2 * aspect)) * 1.12)
        window.SetSize(*size)
        renderer.ResetCameraClippingRange()
        window.Render()
        capture = vtk.vtkWindowToImageFilter()
        capture.SetInput(window)
        capture.SetInputBufferTypeToRGB()
        capture.ReadFrontBufferOff()
        capture.Update()
        filename = out / f'{name}.png'
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(str(filename))
        writer.SetInputConnection(capture.GetOutputPort())
        writer.Write()
        results.append(str(filename))
    window.Finalize()
    print(json.dumps({'vtk': vtk.vtkVersion.GetVTKVersion(), 'file': results, 'metodo': 'Offscreen rendering con Z-buffer reale; nessuna modifica alla geometria STL.'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
