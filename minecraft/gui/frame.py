from contextlib import contextmanager
from typing import Dict, Set

from minecraft.utils import *
from pyglet.gui.widgets import WidgetBase
from pyglet.window import Window


class GUIFrame:
    """The Frame object, rewritten from `pyglet.gui.frame.Frame`."""

    def __init__(self, window: Window, cell_size=128, order=0):
        self._window = window
        self._cell_size = cell_size
        self._cells: Dict[Set[int, int], Set[WidgetBase]] = {}
        self._active_widgets = set()
        self._order = order
        self._enable = False
        self._mouse_pos = 0, 0

    def _hash(self, x, y):
        return int(x / self._cell_size), int(y / self._cell_size)

    @property
    def enable(self):
        return self._enable

    @enable.setter
    def enable(self, value: bool):
        self._enable = bool(value)
        if self._enable:
            self._window.push_handlers(self)
        else:
            self._window.remove_handlers(self)

    def add_widget(self, *widgets: WidgetBase):
        for widget in widgets:
            min_vec, max_vec = self._hash(
                *widget.aabb[0:2]), self._hash(*widget.aabb[2:4])
            for i in range(min_vec[0], max_vec[0] + 1):
                for j in range(min_vec[1], max_vec[1] + 1):
                    self._cells.setdefault((i, j), set()).add(widget)
            widget.update_groups(self._order)

    def remove_widget(self, *widgets: WidgetBase):
        for widget in widgets:
            min_vec, max_vec = self._hash(
                *widget.aabb[0:2]), self._hash(*widget.aabb[2:4])
            for i in range(min_vec[0], max_vec[0] + 1):
                for j in range(min_vec[1], max_vec[1] + 1):
                    self._cells.get((i, j)).remove(widget)

    @contextmanager
    def update(self):
        all_widgets: Set[WidgetBase] = set()
        for widgets_set in self._cells.values():
            [all_widgets.add(widget) for widget in widgets_set]
        self.remove_widget(*all_widgets)
        try:
            yield
        finally:
            self.add_widget(*all_widgets)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self._enable:
            return
        for widget in self._cells.get(self._hash(x, y), set()):
            widget.on_mouse_press(x, y, buttons, modifiers)
            self._active_widgets.add(widget)

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self._enable:
            return
        for widget in self._active_widgets:
            widget.on_mouse_release(x, y, buttons, modifiers)
        self._active_widgets.clear()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self._enable:
            return
        for widget in self._active_widgets:
            widget.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        self._mouse_pos = x, y

    def on_mouse_scroll(self, x, y, index, direction):
        if not self._enable:
            return
        for widget in self._cells.get(self._hash(x, y), set()):
            widget.on_mouse_scroll(x, y, index, direction)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self._enable:
            return
        for widgets in self._cells.values():
            [widget.on_mouse_motion(x, y, dx, dy) for widget in widgets]
        self._mouse_pos = x, y

    def on_text(self, text):
        if not self._enable:
            return
        for widget in self._cells.get(self._hash(*self._mouse_pos), set()):
            widget.on_text(text)

    def on_text_motion(self, motion):
        if not self._enable:
            return
        for widget in self._cells.get(self._hash(*self._mouse_pos), set()):
            widget.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if not self._enable:
            return
        for widget in self._cells.get(self._hash(*self._mouse_pos), set()):
            widget.on_text_motion_select(motion)
