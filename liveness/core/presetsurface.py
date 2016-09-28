'''
PresetSurface
=============

.. versionadded:: 1.1.0

.. warning::
    This module is highly experimental, use it with care.

:class:`PresetSurface` class collect defined presets and provide remote
operations to create new onces. Each instance of this class is connected
to one single :class:`ControlSurface` instance, and vice versa, working
as a sort decorator.

Usage
-----
This class inhert from Widget, so is possible to create new instances directly
from the python script::

    cs = PresetSurface(control_surface_id = "cs", session_id = "ss")

or in the attached KV file::

    PresetSurface:
        control_surface_id: "cs"
        session_id:         "ss"

The combination of this ID's is unique in the system. A preset surface exist
in the context of connected control surface, both pointed by the same ID's.

:class:`PresetSurface` also allow others devices to create new presets,
providing remote functionalities::

    #OSC message from remote device
    /{session_id}/{control_surface_id}/new_preset {preset_id}

This operation create a new instance of :class:`Preset`, from received specifications,
and add it to the preset surface itself.

Other functionality are provided from Widget class. For more
informations: https://kivy.org/docs/api-kivy.uix.widget.html
'''
from 	threading 						import 	Event, Thread
from	kivy.clock			 			import  Clock
from 	kivy.properties					import	StringProperty
from 	kivy.uix.widget	   				import	Widget
from	liveness.core.session 			import	Session
from 	liveness.core.preset 			import 	Preset
from 	liveness.core.controlsurface 	import 	ControlSurface

class PresetSurface(Widget):

	#Properties Definition
	session_id			= 	StringProperty('default')
	control_surface_id	=   StringProperty('default')

	#Syncronization Events
	in_construction		=   Event()

	#PresetSurface Constructor
	def __init__(self, **kwargs):
		#Send initialization event
		PresetSurface.in_construction.clear()
		#Deferred constructor
		super(PresetSurface, self).__init__(**kwargs)
		#run initialization in a new thread, with one frame delay
		Clock.schedule_once(self.launch_deferred__init__, 0)

	def launch_deferred__init__(self, *largs):
		Thread(target = self.deferred__init__).start()

	#Creation Conditions
	def deferred__init__(self):
		#wait for control surface instances
		ControlSurface.in_construction.wait()
		#check for control surface or session not defined
		if Session.check_connected_surface(self.session_id, self.control_surface_id):
			#return the existing control surface instance
			self.control_surface		= Session.get_connected_surface(self.session_id, self.control_surface_id)
		else:
			#remove the new widget instance
			self.parent.remove_widget(self)
			#and leave instance in the garbage collector
			del self
			return
		#check for preset surface already defined in the specified control surface
		if self.control_surface.connected_preset_surface is not None:
			#remove the new widget instance
			self.parent.remove_widget(self)
			#return the existing preset surface instance
			self = self.control_surface.connected_preset_surface
			#add the old widget instance
			self.parent.add_widget(self)
		else:
			#attach the new preset surface to the control surface
			self.control_surface.connected_preset_surface = self
			#set-up remote operations
			self.control_surface.session.set_responder(self.control_surface_id, 'add_preset', self.add_preset)
			#Presets container
			self.connected_presets   =   {}
		#Release session resources and send termination event
		PresetSurface.in_construction.set()

	#Overload add_widget
	def add_widget(self, new_preset):
		Thread(target = self.deferred_add_widget, args = [new_preset]).start()

	def deferred_add_widget(self, new_preset):
		#preset surface allow only preset childs
		if isinstance(new_preset, Preset):
			#wait for initialization end
			PresetSurface.in_construction.wait()
			#wait for presets initialization
			Preset.in_construction.wait()
			#check for presets already defined
			if new_preset.preset_id in self.connected_presets:
				del new_preset
			else:
				super(PresetSurface, self).add_widget(new_preset)
				self.connected_presets.setdefault(new_preset.preset_id, new_preset)
		else:
			del new_preset

	#OSC Responder
	def add_preset(self, *incoming):
		#values coming from remote communication: [time_tag, preset_type, preset_id]
		preset_type		=   str(incoming[0][2])	#sub-class name implementing Preset
		preset_id		=   str(incoming[0][3])
		#import selected class
		type_index	 	=	[cls.__name__ for cls in Control.__subclasses__()].index(preset_type)
		type_def		=	Preset.__subclasses__()[type_index]
		#evaluate the constructor
		new_preset		=   type_def(preset_id = preset_id)
		self.add_widget(new_preset)
