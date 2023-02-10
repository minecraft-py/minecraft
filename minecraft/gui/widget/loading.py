# Minecraft-in-python, a sandbox game
# Copyright (C) 2020-2023  Minecraft-in-python team
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

from minecraft.utils.utils import *

from pyglet.shapes import Rectangle
from pyglet.sprite import Sprite


class LoadingBackground():
    """加载时使用的背景。"""

    def __init__(self, opacity=100):
        width, height = get_size()
        self._rect = Rectangle(0, 0, width, height, color=(0, 0, 0))
        self._rect.opacity = opacity
        self._elements = []
        self._img = get_game().resource_pack.get_resource(
            "textures/gui/options_background")
        for x in range(0, width + self._img.width * 4, self._img.width * 4):
            for y in range(0, height + self._img.height * 4, self._img.height * 4):
                sprite = Sprite(self._img, x=x, y=y)
                sprite.scale = 4
                self._elements.append(sprite)

    def draw(self):
        for img in self._elements:
            img.draw()
        self._rect.draw()

    @property
    def opacity(self):
        return self._rect.opacity

    @opacity.setter
    def opacity(self, value):
        self._rect.opacity = value
        self.resize(*get_size())

    def resize(self, width, height):
        self._rect.width = width
        self._rect.height = height
        self._elements = []
        for x in range(0, width + self._img.width * 4, self._img.width * 4):
            for y in range(0, height + self._img.height * 4, self._img.height * 4):
                sprite = Sprite(self._img, x=x, y=y)
                sprite.scale = 4
                self._elements.append(sprite)
