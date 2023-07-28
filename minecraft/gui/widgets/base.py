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

from pyglet.gui.widgets import WidgetBase as _WidgetBase


class WidgetBase(_WidgetBase):
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value
        self._update_position()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value
        self._update_position()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # Parameters were just renamed due to pyglet#904.
        return super().on_mouse_scroll(x, y, scroll_x, scroll_y)


__all__ = "WidgetBase"
