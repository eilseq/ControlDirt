"""
	ImageButton
	===========
"""
from	kivy.lang				import	Builder
from	kivy.clock				import	Clock
from	kivy.properties			import	StringProperty, NumericProperty
from	kivy.uix.behaviors		import	ButtonBehavior
from	kivy.uix.image			import  Image

Builder.load_string('''
#KVOperations
<-ImageButton>:
    canvas:
        Color:
            rgb: (1, 1, 1)
        Rectangle:
            texture: self.texture
            size: self.width + 20, self.height + 20
            pos: self.x - 10, self.y - 10
''')

class ImageButton(ButtonBehavior, Image):

	#Properties Definitions
	background_normal		= 	StringProperty(None)
	background_down			= 	StringProperty(None)
	detection_thresh		=   NumericProperty(0.4)

	#Event Listener Methods Definition
	def on_background_normal(self, instance, background_normal):
		self.source			=	self.background_normal

	def on_press(self):
		self.source			=	self.background_down

	def on_release(self):
		self.source			=	self.background_normal

	#Event Listener Methods Definition
	def on_press(self):
		self.source			=	self.background_down
		self.delta			=	0
		self.timer			=	Clock.schedule_interval(self.long_press_detect, 0.1)

	def long_press_detect(self, dt):
		self.delta += dt
		if self.delta > self.detection_thresh:
			self.source		=	self.background_normal
			self.timer.cancel()
			self.on_long_press()

	def on_release(self):
		self.source			=	self.background_normal
		if self.delta < self.detection_thresh:
			self.timer.cancel()
			self.on_short_press()

	#Methods to eoverride
	def on_long_press(self):
		pass

	def on_short_press(self):
		pass
