'''
Preset
======

.. versionadded:: 1.1.0

.. warning::
    This module is highly experimental, use it with care.

:class:`Preset` rapresent a decorator for :class:`Widget` class, that allow
any interface to store values from an existing :class:`ControlSurface` instance.

Usage
-----
This class inhert from Widget, so is possible to create new instances directly
from the python script::

    prt = Preset(control_surface_id = "cs", session_id = "ss")

or in the attached KV file::

    Preset:
        preset_id: "cs"

This ID's is unique in the preset surface where is collected.

.. warning::
:class:`Control` can be add only to :class:`ControlSurface` instances.

Launching store operations from python code::

    prt.store()

this class collect all current values from the connected surface. Once it is
done, these values can be called from the same instance::

    prt.call()

Every control is set to the stored value, sending over the network
an OSC messages to synchronize all devices:

    #OSC messages from remote device
    /{session_id}/{control_surface_id}/{control_id} {stored value}

Other functionality are provided from Widget class. For more
informations: https://kivy.org/docs/api-kivy.uix.widget.html
'''
from 	threading 				import 	Event, Thread
from	kivy.clock			 	import  Clock
from 	kivy.properties			import	StringProperty
from 	kivy.uix.widget	   		import	Widget
from	liveness.core.control	import	Control

class Preset(Widget):

	#Properties Definitions
	preset_id			= 	StringProperty(None)

	#Threading Syncronization Events
	in_construction   	=   Event()
	in_construction.set()

	#Preset Constructor
	def __init__(self, **kwargs):
		#send initialization event
		Preset.in_construction.clear()
		#Widget constructor
		super(Preset, self).__init__(**kwargs)
		#run init in a new thread, with some delay to get widget resources
		Clock.schedule_once(self.launch_deferred__init__, 0)

	def launch_deferred__init__(self, *largs):
		Thread(target = self.deferred__init__).start()

	#Creation Conditions
	def deferred__init__(self, *largs):
		#values container
		self.values			=   {}
		#Send termination event
		Preset.in_construction.set()

	#Preset Operations
	def call_preset(self):
		Thread(target = self.deferred_call_preset).start()

	def deferred_call_preset(self):
		#wait for control instances
		Control.in_construction.wait()
		#get and collect all values from pointed control surface
		for control in self.parent.control_surface.children:
			control.value = self.values.get(control.control_id, 0)

	def record_preset(self):
		Thread(target = self.deferred_record_preset).start()

	def deferred_record_preset(self):
		#reset all values
		self.values			=   {}
		#wait for control instances
		Control.in_construction.wait()
		#get and collect all values from pointed control surface
		for control in self.parent.control_surface.children:
			self.values.setdefault(control.control_id, control.value)
