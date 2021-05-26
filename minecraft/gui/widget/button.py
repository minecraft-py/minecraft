from os.path import join

from minecraft.gui.widget.base import Widget
from minecraft.gui.widget.label import ColorLabel
from minecraft.source import resource_pack
from minecraft.utils.utils import *

from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.window import key


class Button(Widget):

    def __init__(self, x, y, width, height, text):
        self._size = win_width, win_height = get_size()
        super().__init__(x, win_height - y, width, height)
        self._width = width
        self._depressed_img = resource_pack.get_resource('textures/gui/widgets').get_region(0, 170, 200, 20)
        self._pressed_img = resource_pack.get_resource('textures/gui/widgets').get_region(0, 150, 200, 20)
        self._unable_img = resource_pack.get_resource('textures/gui/widgets').get_region(0, 190, 200, 20)
        self._sprite = Sprite(self._depressed_img, x, win_height - y)
        self._text = text
        self._label = ColorLabel(self._text, color='white', align='center', anchor_x='center', anchor_y='center',
                x=x + width / 2, y=win_height - y + height / 2, font_size=16)
        self._pressed = False
        self._enable = True

    def _update(self):
        width, height = get_size()
        self._sprite.position = self._x, self._y
        self._label.x = self._x + self._width / 2
        self._label.y = self._y + self._height / 2

    def draw(self):
        self._sprite.scale_x = self._width / 200
        self._sprite.scale_y = self._height / 20
        self._sprite.draw()
        self._label.draw()

    def enable(self, status):
        self._enable = bool(status)
        if self._enable:
            self._label.color = 'white'
        else:
            self._label.color = 'gray'

    def text(self, text):
        self._text = text
        self._label.text = self._text

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_hit(x, y) and self._enable:
            self._sprite.image = self._pressed_img
            self._pressed = True
            self.dispatch_event('on_press')

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self._pressed:
            self._sprite.image = self._depressed_img
            self._pressed = False
            self.dispatch_event('on_release')

    def on_mouse_motion(self, x, y, dx, dy):
        if not self._pressed:
            if self.check_hit(x, y) and self._enable:
                self._sprite.image = self._pressed_img
                self._label.color = 'yellow'
            else:
                self._sprite.image = self._depressed_img if self._enable else self._unable_img
                self._label.color = 'white' if self._enable else 'gray'


Button.register_event_type('on_press')
Button.register_event_type('on_release')


class ChoseButton(Button):

    def __init__(self, x, y, width, height, prefix, values):
        super().__init__(x, y, width, height, text='%s: %s' % (prefix, values[0]))
        self._prefix = prefix
        self._values = values
        self._point = 0

    def on_mouse_press(self, x, y, buttons, modifiers):
        super().on_mouse_press(x, y, buttons, modifiers)
        if self.check_hit(x, y):
            if modifiers == key.MOD_SHIFT:
                self._point -= 1
            else:
                self._point += 1
            if self._point > len(self._values) - 1:
                self._point = 0
            elif self._point < 0:
                self._point = len(self._values) - 1
            self.text('%s: %s' %(self._prefix, self._values[self._point]))

    def value(self):
        return self._values[self._point]
