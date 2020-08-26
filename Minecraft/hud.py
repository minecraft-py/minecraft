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


class Button(BaseHUD):

    def __init__(self, text, x, y, width, height, func):
        self._pressed = False
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._element = {}
        self._element['label'] = pyglet.text.Label(text, x=x + width // 2, y=y - height // 2,
                anchor_x='center', anchor_y='center')
        self._element['seq']   = Rectangle(x, y, width, width, color=(192, 192, 192))
        self._element['line1'] = Line(x, y, x + width, y, color=(0, 0, 0))
        self._element['line2'] = Line(x, y, x, y + height, color=(0, 0, 0))
        self.func = func

    def _update(self):
        self._element['label'].x = self._x + self._width // 2
        self._element['label'].y = self._y - self._height // 2
        self._element['seq'].x = self._x
        self._element['seq'].y = self._y
        self._element['seq'].width = self._width
        self._element['seq'].height = self._height
        self._element['line1'].position = (self._x, self._y, self._x + self._width, self._y)
        self._element['line2'].position = (self._x, self._y, self._x, self._y + self._height)

    def draw(self):
        self._element['seq'].draw()
        self._element['line1'].draw()
        self._element['line2'].draw()
        self._element['label'].draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self._check_hit(x, y):
            return
        self._pressed = True
        self._element['seq'].color = (200, 200, 200)
        self.func()

    def on_mouse_release(self, buttons, modifiers):
        if not self._pressed:
            return
        self._element['seq'].color = (192, 192, 192)

    def on_mouse_montion(self, x, y, dx, dy):
        if self._pressed:
            return
        if self._check_hit(x, y):
            self._element['seq'].color = (200, 200, 200)
        else:
            self._element['seq'].color = (192, 192, 192)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._update()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._update()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self._update

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self._update

