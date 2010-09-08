#!/usr/bin/env python

from enthought.tvtk.api import tvtk
from enthought.tvtk.pyface.scene_model import SceneModel
from enthought.tvtk.pyface.scene_editor import SceneEditor

from enthought.traits.api import HasTraits, Instance
from enthought.traits.ui.api import View, Item, HSplit


class ActorView(HasTraits):
    cube = Instance(tvtk.CubeSource, ())
    scene = Instance(SceneModel)
    
    traits_view = View(HSplit(
                        Item("scene", style="custom", editor=SceneEditor(),
                                show_label=False),
                        Item("cube", style="custom", show_label=False)
                            ),
                        resizable=True, width=700, height=600
                        )
                        
    def _scene_default(self):
        cube = self.cube
        map = tvtk.PolyDataMapper(input=cube.output)
        act = tvtk.Actor(mapper=map)
        scene = SceneModel()
        scene.add_actor(act)
        return scene
                        
                        
if __name__=="__main__":
    test = ActorView()
    test.configure_traits()
    