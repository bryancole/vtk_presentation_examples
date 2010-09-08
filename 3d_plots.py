#!/usr/bin/env python

from enthought.tvtk.api import tvtk
import numpy
from numpy import pi, sin, cos, tan

theta, phi = numpy.ogrid[-pi:pi:100j,0:pi:100j]

r = ((cos(theta)) * (sin(phi)))**2

x = r*sin(phi)*cos(theta)
y = r*sin(phi)*sin(theta)
z = r*cos(phi)

src = tvtk.ProgrammableSource()
def execute():
    output = src.structured_grid_output
    output.points = numpy.dstack((x,y,z)).reshape(-1,3)
    output.point_data.scalars = r.ravel()
    output.extent = [0, r.shape[0]-1, 0, r.shape[1]-1, 0, 0]
    output.whole_extent = [0, r.shape[0]-1, 0, r.shape[1]-1, 0, 0]
    output.set_update_extent_to_whole_extent()
src.set_execute_method(execute)

axes = tvtk.CubeAxesActor()
axes.bounds = [0,1,0,1,0,1]
axes.draw_x_gridlines=True

geom = tvtk.GeometryFilter(input=src.structured_grid_output)
norm = tvtk.PolyDataNormals(input=geom.output)
ds = tvtk.DepthSortPolyData(input=norm.output)

map = tvtk.PolyDataMapper(input=ds.output)
act = tvtk.Actor(mapper=map)
act.property.opacity=0.5
ren = tvtk.Renderer(viewport=[0,0,0.5,1])
ren.add_actor(act)
ren.add_actor(axes)
renwin = tvtk.RenderWindow()
renwin.add_renderer(ren)

axes.camera = ren.active_camera
ds.camera = ren.active_camera
axes.position = [0,0,0]
axes.fly_mode = "static_triad"
ren.reset_camera()

src2 = tvtk.ProgrammableSource()
def execute():
    output = src2.structured_points_output
    output.origin = [0,-pi, 0]
    output.spacing = [pi/100,2*pi/100,1]
    output.point_data.scalars = r.ravel()
    output.extent = [0, r.shape[0]-1, 0, r.shape[1]-1, 0, 0]
    output.whole_extent = [0, r.shape[0]-1, 0, r.shape[1]-1, 0, 0]
    output.set_update_extent_to_whole_extent()
src2.set_execute_method(execute)

geom = tvtk.GeometryFilter(input=src2.structured_points_output)
warp = tvtk.WarpScalar(input = geom.output,
                        scale_factor=5)
norm = tvtk.PolyDataNormals(input=warp.output)
map = tvtk.PolyDataMapper(input=norm.output)
act = tvtk.Actor(mapper=map)

outline = tvtk.OutlineFilter(input=norm.output)
omap = tvtk.PolyDataMapper(input=outline.output)
oact = tvtk.Actor(mapper=omap)

outline.update()
axes = tvtk.CubeAxesActor2D(bounds=outline.output.bounds,
                            y_label="Theta",
                            x_label="Phi",
                            z_label="R")

ren = tvtk.Renderer(viewport=[0.5,0,1,1])
ren.add_actor(act)
ren.add_actor(oact)
ren.add_actor(axes)
axes.camera = ren.active_camera
ren.reset_camera()

renwin.add_renderer(ren)

iren = tvtk.RenderWindowInteractor(render_window=renwin)
iren.start()
