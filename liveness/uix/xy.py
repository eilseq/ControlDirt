"""
	XY
	====

"""
import	math

from	kivy.lang			import	Builder
from	kivy.uix.widget		import	Widget
from	kivy.properties		import	BoundedNumericProperty, StringProperty
from	kivy.graphics	 	import 	Ellipse

Builder.load_string('''
#KVOperations
<XY>:
	canvas:
		Color:
			rgba:	0, 0, 0, 0
		Rectangle:
			pos:	self.pos[0],self.pos[1]
			size:	self.size[0],self.size[1]
			source:	self.source
''')

class XY(Widget):

	source			=	StringProperty(None)

	#Listeners Methods Definition
	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y):
			self.do_translation = True
			self.on_press(touch)
			super(XY, self).on_touch_down(touch)
		else:
			self.do_translation = False

	def on_touch_move(self, touch):
		if self.collide_point(touch.x, touch.y):
			self.do_translation = True
			self.on_press(touch)
			super(XY, self).on_touch_move(touch)
		else:
			self.do_translation = False

	#Abstract Method
	def on_press(self, touch):
		pass

	#Control Generation Methods Definition
	def evaluate_distances(self, touch):
		ip = pow((pow(self.size[0], 2) + pow(self.size[1], 2)), 0.5)
		return {'top_left':	   pow(pow((touch.pos[0] - self.pos[0]), 2) + pow((touch.pos[1] - self.pos[1]), 2), 0.5)/ip,
				'top_right':	  pow(pow((touch.pos[0] - self.pos[0]), 2) + pow((self.pos[1] - touch.pos[1]), 2), 0.5)/ip,
				'bottom_left':	pow(pow((self.pos[0] - touch.pos[0]), 2) + pow((touch.pos[1] - self.pos[1]), 2), 0.5)/ip,
				'bottom_right':   pow(pow((self.pos[0] - touch.pos[0]), 2) + pow((self.pos[1] - touch.pos[1]), 2), 0.5)/ip}
