#!/usr/bin/env python

from enthought.tvtk.api import tvtk

graph = tvtk.RandomGraphSource(number_of_vertices=20,
                                number_of_edges=20)
                        
view = tvtk.GraphLayoutView()
view.add_representation_from_input_connection(graph.output_port)
renwin = tvtk.RenderWindow()
view.setup_render_window(renwin)
renwin.interactor.start()

    