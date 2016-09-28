"""
	XY
	====

"""
import	math

from	kivy.lang			import	Builder
from	kivy.uix.widget		import	Widget
from	kivy.properties		import	BoundedNumericProperty, StringProperty
from    kivy.graphics	 	import 	Ellipse

Builder.load_string('''
#KVOperations
<XY>:
	canvas:
		Color:
			rgba:	1,1,1,1
		Rectangle:
			pos:	self.pos[0],self.pos[1]
			size:	self.size[0],self.size[1]
			source:	self.source
''')

class XY(Widget):

	top_left		=   BoundedNumericProperty(0,min=0,max=1)
	top_right	    =   BoundedNumericProperty(0,min=0,max=1)
	bottom_left	    =   BoundedNumericProperty(0,min=0,max=1)
	bottom_right	=   BoundedNumericProperty(0,min=0,max=1)
	source		    =	StringProperty(None)

	#Listeners Methods Definition
	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y):
			self.do_translation = True
			self.on_press(touch)
			self.draw_pointer(touch)
			super(XY, self).on_touch_down(touch)
		else:
			self.do_translation = False

	def on_touch_move(self, touch):
		if self.collide_point(touch.x, touch.y):
			self.do_translation = True
			self.on_press(touch)
			self.draw_pointer(touch)
			super(XY, self).on_touch_move(touch)
		else:
			self.do_translation = False

	def on_touch_up(self, touch):
		self.clear_pointer()

	#Abstract Method
	def on_press(self, touch):
		pass

	#Graphic Functions
	def draw_pointer(self, touch):
		self.canvas.clear()
		with self.canvas:
			d = 30.
			Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d), source = 'data/logo/kivy-icon-512.png')

	def clear_pointer(self):
		self.canvas.clear()

	#Control Generation Methods Definition
	def evaluate_distances(self, touch):
		ip			= pow((pow(self.size[0], 2) + pow(self.size[1], 2)), 0.5)
		top_left	  = pow(pow((touch.pos[0] - self.pos[0]), 2) + pow((touch.pos[1] - self.pos[1]), 2), 0.5)/ip
		top_right	 = pow(pow((touch.pos[0] - self.pos[0]), 2) + pow((self.pos[1] - touch.pos[1]), 2), 0.5)/ip
		bottom_left   = pow(pow((self.pos[0] - touch.pos[0]), 2) + pow((touch.pos[1] - self.pos[1]), 2), 0.5)/ip
		bottom_right  = pow(pow((self.pos[0] - touch.pos[0]), 2) + pow((self.pos[1] - touch.pos[1]), 2), 0.5)/ip
