# minecraftpy, a sandbox game
# Copyright (C) 2020-2023  minecraftpy team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Dict, List, Tuple

from pyglet.text import Label as _pyglet_label

from minecraft.gui.font import SIZE16

# https://minecraft.fandom.com/wiki/Formatting_codes#Formatting_codes
COLOR: Dict[str, List[Tuple[int, ...]]] = {
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
    "white": [(255, 255, 255), (63, 63, 63)],
}


class Label:
    def __init__(self, text: str, x=0, y=0, color="white", size=SIZE16, **kwargs):
        colors = {}
        colors["fg"] = COLOR.get(color, COLOR["white"])[0] + (255,)
        colors["bg"] = COLOR.get(color, COLOR["white"])[1] + (255,)
        self._offset = size / 8
        self._label: List[_pyglet_label] = []
        self._label.append(
            _pyglet_label(
                text=text,
                x=x,
                y=y,
                color=colors["fg"],
                font_name="minecraft",
                font_size=size,
                **kwargs
            )
        )
        self._label.append(
            _pyglet_label(
                text=text,
                x=x + self._offset,
                y=y - self._offset,
                color=colors["bg"],
                font_name="minecraft",
                font_size=size,
                **kwargs
            )
        )

    @property
    def color(self):
        return "white"

    @color.setter
    def color(self, value: str):
        color = {}
        color["fg"] = COLOR.get(value, COLOR["white"])[0] + (255,)
        color["bg"] = COLOR.get(value, COLOR["white"])[1] + (255,)
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
        return self._label[0].content_width + self._offset

    @width.setter
    def width(self, value):
        self._label[0].width = value
        self._label[1].width = value

    @property
    def height(self):
        return self._label[0].content_height + self._offset

    @property
    def x(self):
        return self._label[0].x

    @x.setter
    def x(self, value):
        self._label[0].x = value
        self._label[1].x = value + self._offset

    @property
    def y(self):
        return self._label[0].y

    @y.setter
    def y(self, value):
        self._label[0].y = value
        self._label[1].y = value - self._offset

    @property
    def position(self):
        return self._label[0].x, self._label[0].y

    @position.setter
    def position(self, value: Tuple[int, ...]):
        d = self._offset
        self._label[0].position = value
        self._label[1].position = (value[0] + d, value[1] - d, value[2])

    def draw(self):
        self._label[1].draw()
        self._label[0].draw()


__all__ = "Label"
