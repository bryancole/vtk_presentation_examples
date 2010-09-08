#!/usr/bin/env python

from enthought.tvtk.api import tvtk

cube = tvtk.CubeSource()

map = tvtk.PolyDataMapper(input=cube.output)

act = tvtk.Actor(mapper=map)

ren = tvtk.Renderer()
ren.add_actor(act)

renwin = tvtk.RenderWindow()
renwin.add_renderer(ren)

iren = tvtk.RenderWindowInteractor(render_window=renwin)
iren.initialize()
iren.start()
