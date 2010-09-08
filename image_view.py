#!/usr/bin/env python

import numpy as np

from enthought.traits.api import HasTraits, Array, Property, Any, Float, \
        Instance, Int, on_trait_change, Event, Bool, DelegatesTo, File
from enthought.traits.ui.api import View, Item, HSplit, VGroup

from enthought.tvtk.api import tvtk
from enthought.tvtk.pyface.scene_model import SceneModel
from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.mayavi.core.lut_manager import LUTManager


class ImageViewer(HasTraits):
    lm = Instance(LUTManager, ())
    source = Instance(tvtk.ProgrammableSource, ())
    mapwin = Instance(tvtk.ImageMapToWindowLevelColors,())
    scene = Instance(SceneModel)
    
    traits_view = View(
                    Item('scene', style="custom", editor=SceneEditor()),
                    Item('lm'),
                    Item('object.mapwin.level'),
                    Item('object.mapwin.window'),
                    resizable=True, width=700, height=600
                    )
    
    def _scene_default(self):
        scene = SceneModel()
        
        src = self.source
        def execute():
            x,y = np.ogrid[-10:10:0.1,-10:10:0.1]
            r = 3*np.sqrt(x**2 + y**2) + 0.001
            z = np.sin(r)/r
            print "shape", z.shape
            output = src.structured_points_output
            #output.origin = [0,0,0]
            #output.spacing = [1,1,1]
            #output.dimensions = [z.shape[0], z.shape[1], 1]
            output.whole_extent = [0,z.shape[0]-1,0,z.shape[1]-1,0,0]
            output.point_data.scalars = z.reshape(-1,1)
            #print "output", output
        src.set_execute_method(execute)
        
#        output = tvtk.ImageData()
#        x,y = np.ogrid[-10:10:0.1,-10:10:0.1]
#        r = 3*np.sqrt(x**2 + y**2) + 0.001
#        z = np.sin(r)/r
#        print "shape", z.shape
#        output.origin = [0,0,0]
#        output.spacing = [1,1,1]
#        #output.dimensions = [z.shape[0], z.shape[1], 1]
#        output.point_data.scalars = z.reshape(-1,1)
#        output.extent = [0,z.shape[0]-1,0,z.shape[1]-1,0,0]

        ss = tvtk.ImageShiftScale(input = src.structured_points_output,
                                shift = 127.0,
                                scale = 127.0)
        ss.set_output_scalar_type_to_unsigned_char()
        print "set source output"
        
        mapwin = self.mapwin
        mapwin.input = src.structured_points_output
        mapwin.lookup_table = self.lm.lut
        
        #ss.update()
        #print ss.output
        
        act = tvtk.ImageActor(input = mapwin.output)
        
        scene.add_actor(act)
        
        scene.add_actor(self.lm.scalar_bar)
        return scene
    

    
if __name__=="__main__":
    viewer = ImageViewer()
    viewer.configure_traits()
    
    