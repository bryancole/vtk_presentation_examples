#!/usr/bin/env python

from vtk import vtkCubeSource, vtkPolyDataMapper, vtkActor,\
        vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor
        
        
cube = vtkCubeSource()

#Add other filters here

map = vtkPolyDataMapper()
map.SetInputConnection(cube.GetOutputPort())

act = vtkActor()
act.SetMapper(map)

ren = vtkRenderer()
ren.AddActor(act)

renwin = vtkRenderWindow()
renwin.AddRenderer(ren)

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)
iren.Initialize()
iren.Start()
