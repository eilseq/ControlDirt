'''
ControlSurface
==============

.. versionadded:: 1.1.0

.. warning::
	This module is highly experimental, use it with care.

:class:`ControlSurface` class collect defined controls and provide remote
operations to create new onces. Also, this class provide session resources
to :class:`Control` and :class:`Preset` classes, interfacing :class:`Session`.

Session interfacing
-------------------
To gurantee the accuracy of process, all instance initializations are launched
by new threads, applying concurrence policies based on this hierarchy:

	.. graphviz::
	digraph {
		"ControlSurface" -> "Session"		 [label="acquire resources / create a new one"]
		"ControlSurface" -> "Control"		 [label="wait for"]
		"PresetSurface"  -> "ControlSurface" [label="wait for"]
		"PresetSurface"  -> "Preset"		 [label="wait for"]
		"Preset"		 -> "Control"		 [label="wait for"]
	}

As can be seen in the diagram, :class:`ControlSurface` is the only class able to access
and manipulate session resources, and provide it to other classes. Also, if the
selected session is not defined yet this class is able to create a new one.

Usage
-----
This class inhert from :class:`Widget`, so is possible to create new instances directly
from the python script::

	cs = ControlSurface(control_surface_id = "cs", session_id = "ss")

or in the attached KV file::

	ControlSurface:
		control_surface_id: "cs"
		session_id:		 "ss"

The combination of this ID's is unique in the system. A contrl surface exist
in his specific session context, and its ID is unique in this context.

:class:`ControlSurface` also allow others devices to create new controls,
providing remote functionalities::

	#OSC message from remote device
	/{session_id}/{control_surface_id}/new_control {control_type, control_id, init_value}

This operation create a new instance of :class:`Control`, from received specifications,
and add it to the control surface itself.

Other functionality are provided from :class:`Widget` class. For more
informations: https://kivy.org/docs/api-kivy.uix.widget.html
'''
from	threading 				import 	Event, Thread
from	kivy.clock			 	import  Clock
from	kivy.properties			import	StringProperty
from	kivy.uix.widget 		import	Widget
from	liveness.core.session	import	Session
from	liveness.core.control	import	Control

class ControlSurface(Widget):

	#Properties Definition
	session_id			=   StringProperty('default')
	control_surface_id	=   StringProperty('default')

	#Syncronization Events
	in_construction		=   Event()

	#ControlSurface Constructor
	def __init__(self, **kwargs):
		#send initialization event
		ControlSurface.in_construction.clear()
		#Widget constructor
		super(ControlSurface, self).__init__(**kwargs)
		#run init in a new thread, with some delay to get widget resources
		Clock.schedule_once(self.launch_deferred__init__, 0)

	def launch_deferred__init__(self, *largs):
		Thread(target = self.deferred__init__).start()

	#Creation Conditions
	def deferred__init__(self):
		#acquire session resources
		Session.resources_lock.acquire()
		#check for control surface already defined in the specified session, or session not defined
		if Session.check_connected_surface(self.session_id, self.control_surface_id):
			#remove the new widget instance
			self.parent.remove_widget(self)
			#return the existing control surface instance
			self = Session.get_connected_surface(self.session_id, sel.control_surface_id)
			#add the old widget instance
			self.parent.add_widget(self)
		else:
			#get the specified session, or create a new one if doesn't defined yet
			self.session					=   Session(self.session_id)
			#add instance to the control surface container
			self.session.connected_surfaces.setdefault(self.control_surface_id, self)
			#set-up remote operations
			self.session.set_responder(self.control_surface_id, 'add_control', self.add_control)
			#Controls container
			self.connected_controls			=   {}
			#Connected preset surface
			self.connected_preset_surface	=   None
			#Enable new incoming controls
			self.enable_add_widget			=	True
		#Release session resources and send termination event
		Session.resources_lock.release()
		ControlSurface.in_construction.set()

	#Overload add_widget
	def add_widget(self, new_control):
		Thread(target = self.deferred_add_widget, args = [new_control]).start()

	def deferred_add_widget(self, new_control):
		#control surface allow only control childs
		if isinstance(new_control, Control):
			#wait for initialization end
			ControlSurface.in_construction.wait()
			#wait for controls initialization
			Control.in_construction.wait()
			#check for controls already defined
			if new_control.control_id in self.connected_controls:
					del new_control
			else:
				super(ControlSurface, self).add_widget(new_control)
				self.connected_controls.setdefault(new_control.control_id, new_control)
		else:
			del new_control

	#OSC Responder
	def add_control(self, *incoming):
		#values coming from remote communication: [time_tag, control_type, control_id, value]
		control_type	=   str(incoming[0][2])	#sub-class name implementing Control
		control_id	 	=   str(incoming[0][3])
		value			=   float(incoming[0][4])
		#import selected class
		type_index	 	=	[cls.__name__ for cls in Control.__subclasses__()].index(control_type)
		type_def		=	Control.__subclasses__()[type_index]
		#evaluate the constructor
		new_control		=   type_def(control_id = control_id, value = value)
		self.add_widget(new_control)

	#OSC Send Method Interfacing
	def send(self, control_id, value):
		'''Send the passed value over network to all connected devices

		.. versionadded:: 1.0.8
		:attr:`widget_id` it refers to the assigned id of given widget producing the value.
		:attr:`value` can be any type of value accepted from OSC standard.
		'''
		self.session.send(self.control_surface_id + "/"+ str(control_id), value)
