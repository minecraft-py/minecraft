from os.path import join

from Minecraft.gui.widget.base import Widget
from Minecraft.source import path
from Minecraft.utils.utils import get_size

from pyglet import image
from pyglet.sprite import Sprite


class Button(Widget):

    def __init__(self, x, y, width, height, text):
        win_width, win_height = get_size()
        super().__init__(x, y, width, 40)
        self._width = width
        self._heiglt = height
        self._depressed_img = image.load(join(path['texture.ui'], 'button.png'))
        self._pressed_img = image.load(join(path['texture.ui'], 'button_over.png'))
        self._sprite = Sprite(self._depressed_img, x, win_height - y)
        self._pressed = False

    def draw(self):
        self._sprite.scale_x = self._width / 200
        self._sprite.scale_y = self._height / 20
        self._sprite.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y):
            self._sprite.image = self._pressed_img
            self._pressed = True
            self.dispatch_event('on_press')

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self._pressed:
            self._sprite = self._depressed_img
            self._pressed = False
            self.dispatch_event('on_release')

    def on_mouse_motion(self, x, y, dx, dy):
        if not self._pressed:
            if self._check_hit(x, y):
                self._sprite.image = self._depressed_img


Button.register_event_type('on_press')
Button.register_event_type('on_release')
