# 游戏用户界面小部件

import pyglet
import pyglet.text
from pyglet.shapes import Line, Rectangle

class BaseHUD(pyglet.event.EventDispatcher):

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def aabb(self):
        return self._x, self._y, self._x + self._width, self._y + self._height

    def _check_hit(self, x, y):
        return self._x < x < self._x + self._width and self._y < y < self._y + self._height

    def on_mouse_press(self, x, y, buttons, modifiers):
        pass

    def on_mouse_release(self, x, y, buttons, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_scroll(self, x, y, mouse, direction):
        pass


BaseHUD.register_event_type('on_mouse_press')
BaseHUD.register_event_type('on_mouse_release')
BaseHUD.register_event_type('on_mouse_drag')
BaseHUD.register_event_type('on_mouse_scroll')


class Bag():

    def __init__(self, x, y, width, height):
        self._element = {}
        self._element['seq1'] = Rectangle(x, y, width, height, color=(200, 200, 200))
        self._element['seq2'] = Rectangle(x + 2, y + 2, width - 4, height - 4, color=(192, 192, 192))

    def draw(self):
        self._element['seq1'].draw()
        self._element['seq2'].draw()

    def resize(self, x, y, width, height):
        self._element['seq1'].position = (x, y)
        self._element['seq2'].position = (x + 2, + 2)
        self._element['seq1'].width = width
        self._element['seq1'].height = height
        self._element['seq2'].width = width - 4
        self._element['seq2'].height = height - 4
