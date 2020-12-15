import pyglet


class DialogueFrame():

    def __init__(self, window):
        window.push_handlers(self)
        self._count = -1
        self._widget = []
        self._enable = False

    def add_widget(self, width):
        self._count += 1
        self._widget.append(width)
        return self._count

    def clean(self):
        self._count = -1
        self.widget = []
        self._enable = False

    def enable(self, status=True):
        self._enable = bool(status)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self._enable:
            return
        for widget in self._widget:
            if widget.check_hit(x, y):
                widget.dispatch_event('on_mouse_press', x, y, buttons, modifiers)
                return True

    def on_mouse_release(self, x, y, buttons, modifiers):
        for widget in self._widget:
            widget.dispatch_event('on_mouse_release', x, y, buttons, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event('on_mouse_drag', x, y, dx, dy, buttons, modifiers)
    
    def on_mouse_scroll(self, x, y, index, direction):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event('on_mouse_scroll', x, y, index, direction)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event('on_mouse_motion', x, y, dx, dy)

    def on_text(self, text):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event('on_text', text)

    def on_text_motion(self, motion):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event('on_text_motion', motion)

    def on_text_motion_select(self, motion):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event('on_text_motion_select', motion)

    def draw(self):
        if not self._enable:
            return
        for widget in self._widget:
            widget.draw()

    def on_resize(self, width, height):
        for widget in self._widget:
            widget.on_resize(width, height)
