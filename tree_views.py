#!/usr/bin/env python

import vtk
import os

graph = vtk.vtkMutableDirectedGraph()

name = vtk.vtkStringArray()
name.SetName("path")

size = vtk.vtkLongArray()
size.SetName("size")

graph.GetVertexData().AddArray(name)
graph.GetVertexData().AddArray(size)

folder = "/home/bryan/Documents"

parent = graph.AddVertex()
name.InsertNextValue(folder)
id_map = {folder:parent}

for dirpath, dirnames, filenames in os.walk(folder):
    parent = id_map[dirpath]
    this_size = 0
    for filename in filenames:
        child_path = os.path.join(dirpath, filename)
        try:
            child_size = os.path.getsize(child_path)
        except OSError:
            child_size = 0
        idx = graph.AddChild(parent)
        name.InsertNextValue(filename)
        size.InsertValue(idx, child_size)
        this_size += child_size
    size.InsertValue(parent, this_size)
    for dirname in dirnames:
        child_path = os.path.join(dirpath, dirname)
        idx = graph.AddChild(parent)
        name.InsertNextValue(dirname)
        id_map[child_path] = idx

tree = vtk.vtkTree()
tree.ShallowCopy(graph)

del graph

#view = vtk.vtkGraphLayoutView()
#view.AddRepresentationFromInputConnection(tree.GetProducerPort())
#view.SetVertexLabelArrayName("path")
#view.SetVertexLabelVisibility(True)
#view.SetVertexColorArrayName("size")
#view.SetColorVertices(True)
#view.SetLayoutStrategyToCommunity2D()
#view.SetVertexLabelFontSize(14)

view = vtk.vtkTreeMapView() #IcicleView()
view.AddRepresentationFromInputConnection(tree.GetProducerPort())
view.SetAreaLabelArrayName("path")
view.SetAreaLabelVisibility(True)
view.SetColorVertices(True)
view.SetAreaColorArrayName("size")

theme = vtk.vtkViewTheme.CreateMellowTheme()
theme.SetLineWidth(4)
theme.SetPointSize(10)
theme.SetCellOpacity(1)
view.ApplyViewTheme(theme)
theme.FastDelete()

#

renwin = vtk.vtkRenderWindow()
renwin.SetSize(600,600)
view.SetupRenderWindow(renwin)
view.GetRenderer().ResetCamera()
renwin.Render()
#view.GetInteractor().Start()
renwin.GetInteractor().Start()
