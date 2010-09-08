#!/usr/bin/env python

from enthought.tvtk.api import tvtk
from enthought.mayavi.core.lut_manager import LUTManager
import numpy

points = [(0,0,0),
          (0,1,0),
          (1,1,0),
          (1,0,0),
          
          (0,0,-1),
          (1,1,1)]

cells = [[0,1,2,3]]

lines = [[0,4],[4,5]]

data = tvtk.PolyData(points=points, polys=cells, lines=lines)
data.point_data.scalars = numpy.linspace(-5,5,6)

lm = LUTManager()
#lm.configure_traits()
map = tvtk.PolyDataMapper(input=data)
map.lookup_table = lm.lut
act = tvtk.Actor(mapper=map)

x,y = numpy.ogrid[-5:5:0.1, -5:5:0.1]
r = x**2 + y**2
z = numpy.cos(r*2) * numpy.exp(-r/3)

img = tvtk.ImageData(origin=(2,2,2), spacing=(0.1,0.1,0.1),
                    dimensions = (z.shape[0], z.shape[1],1 ))
img.point_data.scalars=z.ravel()

img_poly = tvtk.GeometryFilter(input=img)
warp = tvtk.WarpScalar(input_connection=img_poly.output_port)
norm = tvtk.PolyDataNormals(input_connection = warp.output_port)
img_map = tvtk.PolyDataMapper(input_connection=norm.output_port)
img_act = tvtk.Actor(mapper=img_map)

ren = tvtk.Renderer()
#ren.add_actor(act)
ren.add_actor(img_act)

renwin = tvtk.RenderWindow()
renwin.add_renderer(ren)
iren = tvtk.RenderWindowInteractor(render_window=renwin)
iren.start()