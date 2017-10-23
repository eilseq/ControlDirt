# IMPORT LIBRARIES
import sys

sys.path.insert(1, '../..')  # search modules from parent directory

from kivy.app import App

from controldirt.core import Control, Preset, PresetMorphing
from controldirt.uix import ImageButton, XY, Knob


# ---- UIX DEFINITIONS
class SimpleKnob(Control, Knob):
    pass


class PresetButton(Preset, ImageButton):
    def on_preset_id(self, instance, preset_id):
        self.background_normal = 'images/presetbar_' + str(self.preset_id) + '_normal.png'
        self.background_down = 'images/presetbar_' + str(self.preset_id) + '_pressed.png'

    def on_long_press(self):
        self.record_preset()

    def on_short_press(self):
        self.call_preset()


class PresetMorphingXY(PresetMorphing, XY):
    def on_press(self, touch):
        self.interpolate_presets(self.evaluate_distances(touch))


# ---- APPLICATION BUILDER
class XYMorphingApp(App):
    pass


if __name__ == '__main__':
    XYMorphingApp().run()
