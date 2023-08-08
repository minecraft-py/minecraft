# minecraftpy, a sandbox game
# Copyright (C) 2020-2023 minecraftpy team
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

from pyglet.gl import *
from pyglet.graphics import Batch
from pyglet.shapes import BorderedRectangle as _Rect
from pyglet.shapes import get_default_shader


class BorderedRectangle(_Rect):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        border=1,
        color=(255, 255, 255),
        border_color=(100, 100, 100),
        batch=None,
        group=None,
    ):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._rotation = 0
        self._border = border
        self._num_verts = 8

        fill_r, fill_g, fill_b, *fill_a = color
        border_r, border_g, border_b, *border_a = border_color

        self._rgba = fill_r, fill_g, fill_b, fill_a[0] if fill_a else 255
        self._border_rgba = (
            border_r,
            border_g,
            border_b,
            border_a[0] if border_a else 255,
        )

        program = get_default_shader()
        self._batch = batch or Batch()
        self._group = self.group_class(
            GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, program, group
        )

        self._create_vertex_list()
        self._update_vertices()

    @property
    def opacity(self):
        return -1

    @opacity.setter
    def opacity(self, value):
        pass


__all__ = "BorderedRectangle"
