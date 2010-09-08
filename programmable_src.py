#!/usr/bin/env python

import vtk

import numpy
from numpy import pi, sin, cos, tan

theta, phi = numpy.ogrid[-pi:pi:100j,0:pi:100j]

r = ((cos(theta)) * (sin(phi)))**2

x = r*sin(phi)*cos(theta)
y = r*sin(phi)*sin(theta)
z = r*cos(phi)

point_a = numpy.dstack((x,y,z)).reshape(-1,3)
points_A = vtk.vtkDoubleArray()
points_A.SetNumberOfValues(point_a.shape[0])
points_A.SetNumberOfComponents(3)
points_A.SetVoidArray(point_a, 3*point_a.shape[0], 1)

points = vtk.vtkPoints()
points.SetNumberOfPoints(point_a.shape[0])
points.SetDataTypeToDouble()
points.SetData(points_A)

scalars_a = r.ravel()
scalars = vtk.vtkDoubleArray()
scalars.SetNumberOfValues(len(scalars_a))
scalars.SetVoidArray(scalars_a, len(scalars_a), 1)

#dataset = vtk.vtkStructuredGrid()
#dataset.SetPoints(points)
#dataset.GetPointData().SetScalars(scalars)
#dataset.SetExtent(0, r.shape[0]-1, 0, r.shape[1]-1, 0, 0)

src = vtk.vtkProgrammableSource()
def execute():
    output = src.GetStructuredGridOutput()
    output.SetPoints(points)
    output.GetPointData().SetScalars(scalars)
    output.SetExtent(0, r.shape[0]-1, 0, r.shape[1]-1, 0, 0)
    output.SetWholeExtent(0, r.shape[0]-1, 0, r.shape[1]-1, 0, 0)
src.SetExecuteMethod(execute)

#dataset = vtk.vtkStructuredGrid()
#dataset.ShallowCopy(src.GetStructuredGridOutput())
dataset = src.GetStructuredGridOutput()
#print dataset

map = vtk.vtkDataSetMapper()
map.SetInput(dataset)

act = vtk.vtkActor()
act.SetMapper(map)

ren = vtk.vtkRenderer()
ren.AddActor(act)

renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(ren)
ren.ResetCamera()

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)
iren.Start()
