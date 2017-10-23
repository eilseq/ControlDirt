# IMPORT LIBRARIES
import sys

from kivy.app import App
from controldirt.core import Control
from controldirt.uix import Knob

sys.path.insert(1, '../..')  # search modules from parent directory


# UIX DEFINITIONS
class SimpleKnob(Knob):
    pass


# APPLICATION BUILDER
class Frontend(App):
    pass


if __name__ == '__main__':
    Frontend().run()
