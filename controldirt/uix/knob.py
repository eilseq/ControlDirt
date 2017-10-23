"""
Knob
====
"""
import math

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import BoundedNumericProperty, NumericProperty, StringProperty

Builder.load_string('''
#KVOperations
<Knob>:
    size_hint: None,None
    size: 125, 125
    source: 'images/dial_background.png'
    
    canvas.before:
        Color:
            rgba: 1,1,1,1
        PushMatrix
        Rotate:
            angle: 360. - self.angle
            origin: self.center
        Rectangle:
            pos: self.pos[0],self.pos[1]
            size: self.size[0],self.size[1]
            source: self.source
    
    canvas:
        PopMatrix

    Label:
        font_name: 'courier'
        font_size: '15sp'
        center: root.center[0] + 100, root.center[1] + 12
        text: str(root.name)
                
    Label:
        font_name: 'courier'
        font_size: '15sp'
        center: root.center[0] + 100, root.center[1] - 12
        text: str(root.value)[:6].upper()
''')


class Knob(Widget):
    name = StringProperty("")
    value = BoundedNumericProperty(0, min=0, max=1)
    angle = NumericProperty(0)
    source = StringProperty("")

    def evaluate_angle(self, touch):
        y = touch.y - self.center[1]
        x = touch.x - self.center[0]
        if y == 0:
            a = 0
        else:
            a = math.atan2(x, y)
        while a < 0.0:
            a = a + (math.pi * 2)
        return math.degrees(a)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.angle = self.evaluate_angle(touch)

    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.angle = self.evaluate_angle(touch)

    def on_angle(self, instance, angle):
        self.value = self.angle / 360.
