'''
PresetMorphing
==============

.. versionadded:: 1.1.0

.. warning::
    This module is highly experimental, use it with care.

:class:`PresetMorphing` rapresent a decorator for :class:`Widget` class, that
provide morphing functionalities for manage stored presets. Morphing is a term
indicating the smooth transition between presets, so this class simply evaluate
interpolation values of indicated presets, and call the result.

Usage
-----
This class inhert from Widget, so is possible to create new instances directly
from the python script::

    prt = PresetMorphing(preset_surface = ps)   #where ps is a PreseteSurface

or in the attached KV file::

    PresetMorphing:
        preset_surface: ps					  #where ps is a PreseteSurface

From a list of weights, this class create a new set of values that rapresent
the weighted mean of values by all presets in the same preset surface::

    prt.interpolate_presets({list of float vlaues})

Once values are evaluated, controls are set to this new onces and sended over
the network as OSC messages to synchronize all devices:

    #OSC messages from remote device
    /{session_id}/{control_surface_id}/{control_id} {stored value}

Other functionality are provided from Widget class. For more
informations: https://kivy.org/docs/api-kivy.uix.widget.html
'''
from    threading import Thread
from    kivy.clock import Clock
from    kivy.properties import ObjectProperty
from    kivy.uix.widget import Widget
from    controldirt.core.presetsurface import PresetSurface


class PresetMorphing(Widget):

    # Properties Definitions
    preset_surface = ObjectProperty(None)

    # PresetMorphing Constructor
    def __init__(self, **kwargs):
        super(PresetMorphing, self).__init__(**kwargs)
        Clock.schedule_once(self.launch_deferred__init__, 0)

    def launch_deferred__init__(self, *largs):
        Thread(target=self.deferred__init__).start()

    def deferred__init__(self, *largs):
        # wait for initialization end
        PresetSurface.in_construction.wait()
        # check if the connected objects are a preset surface
        if isinstance(self.preset_surface, PresetSurface):
            return
        else:
            # remove the new widget instance
            self.parent.remove_widget(self)
            del self
            return

    # Preset Operations
    def interpolate_presets(self, weights):
        Thread(target=self.deferred_interpolate_presets, args=[weights]).start()

    def deferred_interpolate_presets(self, weights):
        # wait for initialization end
        PresetSurface.in_construction.wait()
        # Interpolation
        try:
            # Evaluate result
            result = {}
            for preset_id, weight in weights.iteritems():
                for control_id, value in self.preset_surface.connected_presets[preset_id].values.iteritems():
                    interp_value = result.get(control_id, 0) + (value * weight)
                    result.setdefault(control_id, interp_value)
            # Send to control surface
            for control in self.preset_surface.control_surface.children:
                # clipped between 0 and 1
                if result[control.control_id] > 1:
                    control.value = 1
                elif result[control.control_id] < 0:
                    control.value = 0
                else:
                    control.value = result[control.control_id]
        except KeyError as AttributeError:
            print("ERROR: ID dosen't exist in preset list")
