'''
Control
=======

:class:`Control` rapresent a decorator for :class:`Widget` class, that allow
any interface to send datas over network simply changing its own value.

Usage
-----
Is possible to create new instances directly from the python script::

    ctl = Control(control_id = "ctl")

or in the attached KV file::

    Control:
        control_id:         "cs"

This ID's is unique in the control surface where is collected.

.. warning::
:class:`Control` can be add only to :class:`ControlSurface` instances.

Setting a control's value property from python code::

    ctl.value = {incoming value}

this class send over the network an OSC message containing this new value::

    #OSC message from remote device
    /{session_id}/{control_surface_id}/{control_id} {incoming value}

Other functionality are provided from Widget class. For more
informations: https://kivy.org/docs/api-kivy.uix.widget.html
'''
from    threading import Event, Thread
from    kivy.clock import Clock
from    kivy.properties import StringProperty, BoundedNumericProperty
from    kivy.uix.widget import Widget


class Control(Widget):
    # Properties Definitions
    control_id = StringProperty(None)
    value = BoundedNumericProperty(0, min=0, max=1)

    # Syncronization Events
    in_construction = Event()
    in_construction.set()

    # Control Constructor
    def __init__(self, **kwargs):
        # send initialization event
        Control.in_construction.clear()
        # Widget constructor
        super(Control, self).__init__(**kwargs)
        # run init in a new thread, with some delay to get widget resources
        Clock.schedule_once(self.launch_deferred__init__, 0)

    def launch_deferred__init__(self, *largs):
        Thread(target=self.deferred__init__).start()

    # Creation Conditions
    def deferred__init__(self, *largs):
        # instance variables
        self.values = {}
        # Send termination event
        Control.in_construction.set()

    # Event Listener Methods Definition
    def on_value(self, instance, value):
        self.parent.send(self.control_id, self.value)
