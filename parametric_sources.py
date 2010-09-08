#!/usr/bin/env python
from enthought.tvtk.api import tvtk
from enthought.tvtk.pyface.scene_model import SceneModel
from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.traits.api import HasTraits, Instance, Enum, Property,\
            on_trait_change
from enthought.traits.ui.api import View, Item, InstanceEditor, HSplit,\
            VGroup, Tabbed

source_types = [tvtk.ParametricBoy,
                tvtk.ParametricConicSpiral,
                tvtk.ParametricCrossCap,
                tvtk.ParametricDini,
                tvtk.ParametricKlein]
                
sources = dict((c.__name__, c()) for c in source_types)
                

class MyDemo(HasTraits):
    scene = Instance(SceneModel, ())
    
    source = Instance(tvtk.ParametricFunctionSource, ())
    
    func_name = Enum([c.__name__ for c in source_types])
    
    func = Property(depends_on="func_name")
    
    traits_view = View(HSplit(
                          VGroup(
                            Item("func_name", show_label=False),
                            Tabbed(
                                Item("func", style="custom", editor=InstanceEditor(),
                                    show_label=False),
                                Item("source", style="custom", show_label=False)
                                )
                              ),
                            Item("scene", style="custom", show_label=False,
                                editor=SceneEditor())
                            ),
                        resizable=True, width=700, height=600
                        )
                        
    def __init__(self, *args, **kwds):
        super(MyDemo, self).__init__(*args, **kwds)
        self._make_pipeline()
        
    def _get_func(self):
        return sources[self.func_name]
        
    def _make_pipeline(self):
        self.func.on_trait_change(self.on_change, "anytrait")
        src = self.source
        src.on_trait_change(self.on_change, "anytrait")
        src.parametric_function = self.func
        map = tvtk.PolyDataMapper(input_connection=src.output_port)
        act = tvtk.Actor(mapper=map)
        self.scene.add_actor(act)
        self.src = src
        
    def _func_changed(self, old_func, this_func):
        if old_func is not None:
            old_func.on_trait_change(self.on_change, "anytrait", remove=True)
        this_func.on_trait_change(self.on_change, "anytrait")
        self.src.parametric_function = this_func
        self.scene.render()
        
    def on_change(self):
        self.scene.render()
                        
                        
if __name__=="__main__":
    demo = MyDemo()
    demo.configure_traits()