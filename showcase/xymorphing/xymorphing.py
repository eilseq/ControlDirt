#---- IMPORT LIBRARIES
import sys
sys.path.insert(1, '../..')	#search modules from parent directory

import kivy
from kivy.app 				import	App
from kivy.uix.image 		import 	Image

import liveness
from liveness.core 			import	Control, ControlSurface, Preset, PresetSurface, PresetMorphing
from liveness.uix 			import	ImageButton, XY, Knob

#---- UIX DEFINITIONS
class SimpleKnob(Control, Knob):
	pass

class PresetButton(Preset, ImageButton):

	#Event Listener Methods Definition
	def on_preset_id(self, instance, preset_id):
		self.background_normal	=	'images/presetbar_'+str(self.preset_id)+'_normal.png'
		self.background_down	=	'images/presetbar_'+str(self.preset_id)+'_pressed.png'

	def on_long_press(self):
		self.record_preset()

	def on_short_press(self):
		self.call_preset()

class PresetMorphingXY(PresetMorphing, XY):
	def on_press(self, touch):
		self.interpolate_presets({  'top_left':	 self.top_left,
									'top_right':	self.top_right,
									'bottom_left':  self.bottom_left,
									'bottom_right': self.bottom_right  })

#---- APPLICATION BUILDER
class XYMorphingApp(App):
	pass

if __name__ == '__main__':
	XYMorphingApp().run()
