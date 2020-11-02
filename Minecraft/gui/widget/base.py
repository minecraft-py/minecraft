from pyglet.event import EventDispatcher


class Widget(EventDispatcher):

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def position(self):
        return self._x, self._y

    @position.setter
    def position(self, pos):
        self._x, self._y = pos

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def _check_hit(self, x, y):
        return self._x < x < self._x + self._width and self._y < y < self._y + self._height

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_scroll(self, x, y, mouse, direction):
        pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        pass

    def on_mouse_release(self, x, y, buttons, modifiers):
        pass


Widget.register_event_type('on_mouse_drag')
Widget.register_event_type('on_mouse_motion')
Widget.register_event_type('on_mouse_press')
Widget.register_event_type('on_mouse_release')
