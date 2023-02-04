# Copyright 2020-2023 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from minecraft.gui.widget import Widget
from pyglet.text import Label

# 颜色代码请见https://minecraft.fandom.com/wiki/Formatting_codes#Formatting_codes
_color_tabel = {
    "black": [(0, 0, 0), (255, 255, 255)],
    "dark_blue": [(0, 0, 170), (0, 0, 42)],
    "dark_green": [(0, 170, 0), (0, 42, 0)],
    "dark_aqua": [(0, 170, 170), (0, 42, 42)],
    "dark_red": [(170, 0, 0), (42, 0, 0)],
    "dark_purple": [(170, 0, 170), (42, 0, 42)],
    "gold": [(255, 170, 0), (64, 42, 0)],
    "gray": [(170, 170, 170), (42, 42, 42)],
    "dark_gray": [(85, 85, 85), (21, 21, 21)],
    "blue": [(85, 85, 255), (21, 21, 63)],
    "aqua": [(85, 255, 255), (21, 63, 63)],
    "red": [(255, 85, 85), (66, 21, 21)],
    "light_purple": [(255, 85, 255), (63, 21, 63)],
    "yellow": [(255, 255, 85), (63, 63, 21)],
    "white": [(255, 255, 255), (63, 63, 63)]
}


class ColorLabel(Widget):
    """标签。"""

    def __init__(self, text="", color="white", x=0, y=0, shadow=True, **kwargs):
        global _color_tabel
        colors = {}
        colors["fg"] = _color_tabel.get(
            color, _color_tabel["white"])[0] + (255,)
        colors["bg"] = _color_tabel.get(
            color, _color_tabel["white"])[1] + (255,)
        self._label = []
        self._label.append(
            Label(text=text, x=x, y=y, color=colors["fg"], **kwargs))
        self._label.append(Label(text=text, x=x + 3, y=y -
                           2, color=colors["bg"], **kwargs))
        self._shadow = shadow
        super().__init__(x, y, 1, 1)

    @property
    def color(self):
        return "white"

    @color.setter
    def color(self, value):
        global _color_tabel
        color = {}
        color["fg"] = _color_tabel.get(
            value, _color_tabel["white"])[0] + (255,)
        color["bg"] = _color_tabel.get(
            value, _color_tabel["white"])[1] + (255,)
        self._label[0].color = color["fg"]
        self._label[1].color = color["bg"]

    @property
    def text(self):
        return self._label[0].text

    @text.setter
    def text(self, value):
        self._label[0].text = value
        self._label[1].text = value

    @property
    def width(self):
        return self._label[0].content_width + 2

    @width.setter
    def width(self, value):
        self._label[0].width = value
        self._label[1].width = value

    @property
    def height(self):
        return self._label[0].content_height + 3

    @property
    def x(self):
        return self._label[0].x

    @x.setter
    def x(self, value):
        self._label[0].x = value
        self._label[1].x = value + 3

    @property
    def y(self):
        return self._label[0].y

    @y.setter
    def y(self, value):
        self._label[0].y = value
        self._label[1].y = value - 2

    def draw(self):
        if self._shadow:
            self._label[1].draw()
        self._label[0].draw()
