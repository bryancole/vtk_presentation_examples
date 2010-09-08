#!/usr/bin/env python
import pyximport
pyximport.install()

import numpy as np
from biot_savart import calc_wire_B_field

from enthought.traits.api import HasTraits, Array, Property, Any, Float, \
        Instance, Int, on_trait_change, Event, Bool, DelegatesTo
from enthought.traits.ui.api import View, Item, HSplit, VGroup

from enthought.tvtk.api import tvtk
from enthought.tvtk.pyface.scene_model import SceneModel
from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.mayavi.core.lut_manager import LUTManager


class WireLoop(HasTraits):
    nodes = Array(shape=(None,3), dtype=np.double)
    radius = Float(0.1, desc="radius of the wire")
    source = Instance(tvtk.ProgrammableSource, ())
    tube = Instance(tvtk.TubeFilter, ())
    pipeline = Any
    actor = Instance(tvtk.Actor, ())
    update = Event()
    
    def _radius_changed(self):
        self.tube.radius = self.radius
        self.update = True
    
    def _nodes_changed(self):
        self.source.modified()
        self.update = True
    
    def _pipeline_default(self):
        src = self.source
        def execute():
            output = src.poly_data_output
            output.points = self.nodes
            a = range(self.nodes.shape[0]) + [0]
            lines = [a]
            output.lines = lines
        src.set_execute_method(execute)
        
        tube = self.tube
        tube.number_of_sides = 18
        tube.input_connection = src.output_port
        tube.radius = self.radius
        
        return tube
    
    def _actor_default(self):
        map = tvtk.PolyDataMapper(input_connection = self.pipeline.output_port)
        act = tvtk.Actor(mapper=map)
        return act
    
    
class Solenoid(WireLoop):
    pitch = Float(0.2)
    diameter = Float(1.0)
    turns = Float(10.0)
    resolution = Int(64)
    radius = 0.02
    
    traits_view = View("pitch", "diameter",
                        "turns", "resolution",
                        "radius")
    
    @on_trait_change("pitch, diameter, turns, resolution")
    def on_change(self):
        a = np.arange(0,2*np.pi*self.turns,2*np.pi/self.resolution)
        r = self.diameter/2.
        x = np.cos(a)*r
        y = np.sin(a)*r
        z = (np.arange(len(a))- len(a)/2.0) * self.pitch/self.resolution
        self.nodes = np.column_stack((x,y,z))
    

class FieldExplorer(HasTraits):
    scene = Instance(SceneModel, ())
    wire = Instance(WireLoop)
    
    interact = Bool(False)
    ipl = Instance(tvtk.PlaneWidget, (), {'resolution':50, 'normal':[1.,0.,0.]})
    #plane_src = Instance(tvtk.PlaneSource, ())
    calc_B = Instance(tvtk.ProgrammableFilter,())
    
    glyph = Instance(tvtk.Glyph3D, (), {'scale_factor':0.02})
    scale_factor = DelegatesTo("glyph")
    
    lm = Instance(LUTManager, ())
    
    traits_view = View(HSplit(
                        Item("scene", style="custom", editor=SceneEditor(),
                                show_label=False),
                        VGroup(
                            Item("wire", style="custom", show_label=False),
                            Item("interact"),
                            Item("scale_factor"),
                            Item("lm")
                              ),
                            ),
                        resizable=True, width=700, height=600
                        )
        
    def _interact_changed(self, i):
        self.ipl.interactor = self.scene.interactor
        self.ipl.place_widget()
        if i:
            self.ipl.on()
        else:
            self.ipl.off()
            
    def make_probe(self):
        src = self.ipl.poly_data_algorithm
        
        map = tvtk.PolyDataMapper(lookup_table=self.lm.lut)
        act = tvtk.Actor(mapper=map)
        
        calc_B = self.calc_B
        calc_B.input=src.output
        def execute():
            print "calc fields!"
            output = calc_B.poly_data_output
            points = output.points.to_array().astype('d')
            nodes = self.wire.nodes.astype('d')
            vectors = calc_wire_B_field(nodes, points, self.wire.radius)
            output.point_data.vectors = vectors
            mag = np.sqrt((vectors**2).sum(axis=1))
            map.scalar_range = (mag.min(), mag.max())
        calc_B.set_execute_method(execute)
        
        cone = tvtk.ConeSource(height=0.05, radius=0.01, resolution=15)
        cone.update()
        
        glyph = self.glyph
        glyph.input_connection=calc_B.output_port
        glyph.source=cone.output
        glyph.scale_mode='scale_by_vector'
        glyph.color_mode='color_by_vector'
        
        map.input_connection=glyph.output_port
        self.scene.add_actor(act)
        
                        
    def on_update(self):
        self.calc_B.modified()
        self.scene.render()
                        
    def _wire_changed(self, anew):
        anew.on_trait_change(self.on_update, "update")
        self.scene.add_actor(anew.actor)

if __name__=="__main__":
    wire = Solenoid(turns=11)
    view = FieldExplorer(wire=wire)
    view.make_probe()
    view.configure_traits()
    
    