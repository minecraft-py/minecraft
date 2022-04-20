from pyglet.event import EventDispatcher


class Widget(EventDispatcher):

    def __init__(self, x, y, width, height):
        # 窗口中所有可交互(当然, 也可以不提供交互功能)的小部件的基类
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def position(self):
        return self._x, self._y

    @position.setter
    def position(self, x, y):
        self._x, self._y = x, y
        self._update()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self._update()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = get_size()[1] - y
        self._update()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        self._update()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
        self._update()

    def _update(self):
        pass

    def register_event(self, event, func):
        setattr(self, "on_%s" % event, func)

    def check_hit(self, x, y):
        return self._x < x < self._x + self._width and self._y < y < self._y + self._height

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        pass

    def on_mouse_release(self, x, y, buttons, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_scroll(self, x, y, mouse, direction):
        pass

    def on_resize(self, width, height):
        pass

    def on_text(self, text):
        pass

    def on_text_motion(self, motion):
        pass

    def on_text_motion_select(self, motion):
        pass


Widget.register_event_type("on_key_press")
Widget.register_event_type("on_key_release")
Widget.register_event_type("on_mouse_press")
Widget.register_event_type("on_mouse_release")
Widget.register_event_type("on_mouse_motion")
Widget.register_event_type("on_mouse_drag")
Widget.register_event_type("on_mouse_scroll")
Widget.register_event_type("on_text")
Widget.register_event_type("on_text_motion")
Widget.register_event_type("on_text_motion_select")
