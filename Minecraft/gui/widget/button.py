from os.path import join

from Minecraft.gui.widget.base import Widget
from Minecraft.source import path
from Minecraft.utils.utils import *

from pyglet import image
from pyglet.sprite import Sprite
from pyglet.text import Label


class Button(Widget):

    def __init__(self, x, y, width, height, text):
        self._size = win_width, win_height = get_size()
        super().__init__(x, win_height - y, width, height)
        self._width = width
        self._depressed_img = image.load(join(path['texture.ui'], 'button.png'))
        self._pressed_img = image.load(join(path['texture.ui'], 'button_over.png'))
        self._sprite = Sprite(self._depressed_img, x, win_height - y)
        self._text = text
        self._label = Label(self._text, align='center', anchor_x='center', anchor_y='center',
                x=x + width / 2, y=win_height - y + height / 2)
        self._pressed = False
        self._enable = True

    def draw(self):
        self._sprite.scale_x = self._width / 200
        self._sprite.scale_y = self._height / 20
        self._sprite.draw()
        self._label.draw()

    def enable(self, status):
        self._enable = bool(status)
        if self._enable:
            self._label.color = (255, ) * 4
        else:
            self._label.color = (255, ) * 3 + (100, )

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
            else:
                self._sprite.image = self._depressed_img

    def on_resize(self, width, height):
        self._x *= width / self._size[0]
        self._y = (height / self._size[1]) * self._y
        self._size = width, height
        self._sprite.position = self._x, self._y
        self._label.x = self._x + self._width / 2
        self._label.y = self._y + self._height / 2


Button.register_event_type('on_press')
Button.register_event_type('on_release')
