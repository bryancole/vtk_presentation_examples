#!/usr/bin/env python

from enthought.tvtk.api import tvtk
from glob import glob
import numpy, os

data_dir = "/home/bryan/TeraView/mydata/MyDocuments/Cdev/rabi1/test"

files = glob(data_dir+"/*.bob")

data = numpy.fromfile(open(os.path.join(data_dir,"c_003650.bob"),'rb'), numpy.uint8)

ns = int(round(data.shape[0]**(1./3)))

data.shape = (-1,1)
print "Range", data.max(), data.min(), data.mean()

src = tvtk.ProgrammableSource()
def execute():
    output = src.structured_points_output
    output.scalar_type = "char"
    output.origin = (0,0,0)
    output.spacing = (.1,.1,.1)
    output.point_data.scalars = data
    extent = (0,ns-1,0,ns-1,0,ns-1)
    output.extent = extent
    output.whole_extent = extent
    output.set_update_extent_to_whole_extent()
src.set_execute_method(execute)

info = tvtk.ImageChangeInformation(input=src.structured_points_output,
                                center_image=True,
                                spacing_scale=(1,1,1))

#src.update()
#print src.structured_points_output

opac = tvtk.PiecewiseFunction()
opac.add_point(0,0.005)
opac.add_point(255, 0.6)

colors = tvtk.ColorTransferFunction()
plist=[(0,0.0,0.0,0.75),
            (15,0.0,0.0,1.0),
            (31,0.0,0.25,1.0),
            (47,0.0,0.50,1.0),
            (63,0.0,0.75,1.0),
            (79,0.0,1.0,1.0),
            (95,0.25,1.0,0.75),
            (111,0.50,1.0,0.5),
            (127,0.75,1.0,0.25),
            (143,1.0,1.0,0.0),
            (159,1.0,0.75,0.0),
            (174,1.0,0.5,0.0),
            (191,1.0,0.25,0.0),
            (207,1.0,0.0,0.0),
            (223,0.75,0.0,0.0),
            (239,0.5,0.0,0.0),
            (255,0.25,0.0,0.0)]
for pt in plist:
    colors.add_rgb_point(*pt)

volprop = tvtk.VolumeProperty(
                            shade=True,
                            ambient=0.3,
                            diffuse=1.0,
                            interpolation_type="linear")
volprop.set_color(colors)
volprop.set_scalar_opacity(opac)

cf = tvtk.VolumeRayCastCompositeFunction()

volmap = tvtk.VolumeRayCastMapper(input=info.output,
                            volume_ray_cast_function=cf)

map = tvtk.VolumeRayCastMapper(input=info.output)

vol = tvtk.Volume(mapper=volmap, property=volprop)

outline = tvtk.OutlineFilter(input=info.output)
omap = tvtk.PolyDataMapper(input=outline.output)
oact = tvtk.Actor(mapper=omap)

src.update()
data = src.output
print data.scalar_range

contour = tvtk.ContourFilter(input=info.output)
contour.generate_values(5, 0.0, 1.0)

contour.update()
print contour.output

cmap = tvtk.PolyDataMapper(input=contour.output)
cact = tvtk.Actor(mapper=cmap)

ren = tvtk.Renderer()
ren.add_actor(vol)
ren.add_actor(oact)
ren.add_actor(cact)
ren.background=(0.3,0.2,0.1)

renwin = tvtk.RenderWindow()
renwin.add_renderer(ren)

ren.reset_camera()

iren = tvtk.RenderWindowInteractor(render_window=renwin)
iren.start()

