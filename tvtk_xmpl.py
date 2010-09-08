#!/usr/bin/env python

from enthought.tvtk.api import tvtk
from enthought.tvtk.pyface.scene_model import SceneModel
from enthought.tvtk.pyface.scene_editor import SceneEditor

from enthought.traits.api import HasTraits, Instance

from enthought.traits.ui.api import View, Item


class ActorView(HasTraits):
    scene = Instance(SceneModel, ())
    
    traits_view = View(Item("scene", style="custom", editor=SceneEditor(),
                                show_label=False),
                        resizable=True, width=700, height=600
                        )
                        
    
                        
                        
if __name__=="__main__":
    graph = tvtk.RandomGraphSource()
    
    layout = tvtk.GraphLayout(input_connection=graph.output_port,
                            layout_strategy=tvtk.Simple2DLayoutStrategy())
    
    poly = tvtk.GraphToPolyData(input_connection=layout.output_port)
    
    s = tvtk.SphereSource()
    
    glyph = tvtk.Glyph3D(input_connection=poly.output_port,
                        source=s.output)
                        
    app = tvtk.AppendPolyData()
    app.add_input_connection(glyph.output_port)
    app.add_input_connection(poly.output_port)
    
    map = tvtk.PolyDataMapper(input_connection=app.output_port)
    
    act = tvtk.Actor(mapper=map)
    
    demo = ActorView()
    demo.scene.add_actor(act)
    demo.configure_traits()
    