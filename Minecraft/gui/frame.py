import pyglet


class DialogueFrame():

    def __init__(self, window, x, y, width, height):
        window.push_handlers(self)
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._count = -1
        self._widget = []

    def add_widget(self, width):
        self._count += 1
        self._widget.append(width)
        return self._count

    def on_mouse_press(self, x, y, buttons, modifiers):
        for widget in self._widget:
            widget.dispatch_event('on_mouse_press', x, y, buttons, modifiers)

    def on_mouse_release(self, x, y, buttons, modifiers):
        for widget in self._widget:
            widget.dispatch_event('on_mouse_release', x, y, buttons, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for widget in self._widget:
            widget.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    
    def on_mouse_scroll(self, x, y, index, direction):
        for widget in self._widget:
            widget.dispatch_event('on_mouse_scroll', x, y, index, direction)

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self._widget:
            widget.dispatch_event('on_mouse_motion', x, y, dx, dy)

    def on_text(self, text):
        for widget in self._widget:
            widget.dispatch_event('on_text', text)

    def on_text_motion(self, motion):
        for widget in self._widget:
            widget.dispatch_event('on_text_motion', motion)

    def on_text_motion_select(self, motion):
        for widget in self._widget:
            widget.dispatch_event('on_text_motion_select', motion)

    def draw(self):
        for widget in self._widget:
            widget.draw()

    def on_resize(self, width, height):
        for widget in self._widget:
            widget.on_resize(width, height)
