# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from minecraft.utils.utils import *


class Frame():
    """小部件框架。

    绑定到窗口以实现交互功能。
    """

    def __init__(self):
        self._widget = []
        self._enable = False

    def add_widget(self, *widgets):
        for widget in widgets:
            self._widget.append(widget)

    def clean(self):
        self._widget = []
        self._enable = False

    def enable(self):
        self._enable = True
        self.on_mouse_motion(*get_game().mouse_position, 0, 0)
        get_game().push_handlers(self)

    def disable(self):
        self._enable = False
        get_game().remove_handlers(self)

    def on_key_press(self, symbol, modifiers):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event("on_key_press", symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event("on_key_release", symbol, modifiers)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event("on_mouse_press", x, y, buttons, modifiers)

    def on_mouse_release(self, x, y, buttons, modifiers):
        for widget in self._widget:
            widget.dispatch_event("on_mouse_release", x, y, buttons, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event("on_mouse_drag", x, y,
                                  dx, dy, buttons, modifiers)

    def on_mouse_scroll(self, x, y, index, direction):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event("on_mouse_scroll", x, y, index, direction)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event("on_mouse_motion", x, y, dx, dy)

    def on_text(self, text):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event("on_text", text)

    def on_text_motion(self, motion):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event("on_text_motion", motion)

    def on_text_motion_select(self, motion):
        if not self._enable:
            return
        for widget in self._widget:
            widget.dispatch_event("on_text_motion_select", motion)

    def draw(self):
        if not self._enable:
            return
        for widget in self._widget:
            widget.draw()

    def on_resize(self, width, height):
        for widget in self._widget:
            widget.on_resize(width, height)
