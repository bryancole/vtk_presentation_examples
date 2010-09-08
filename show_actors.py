#!/usr/bin/env python

from vtk import vtkConeSource, vtkSphereSource, vtkCubeSource, vtkRenderer,\
    vtkRenderWindow, vtkPolyDataMapper, vtkActor, vtkRenderWindowInteractor,\
    vtkInteractorStyleTrackball

sources = [vtkConeSource(), vtkSphereSource(), vtkCubeSource()]
positions = [ (-2,-2,0),
              (0,2,0),
              (2,-2,0) ]

def make_actor(src):
    map = vtkPolyDataMapper()
    map.SetInputConnection(src.GetOutputPort())
    act = vtkActor()
    act.SetMapper(map)
    return act

ren = vtkRenderer()
ren.SetBackground(0.2,0,0.2)
ren.SetBackground2(0.6,0.4,0.6)
ren.SetGradientBackground(True)

for s,p in zip(sources, positions):
    act = make_actor(s)
    act.SetPosition(*p)
    ren.AddActor(act)

renwin = vtkRenderWindow()
renwin.AddRenderer(ren)

iren = vtkRenderWindowInteractor()
renwin.SetInteractor(iren)
iren.Start()
