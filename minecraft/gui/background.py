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

from minecraft import assets
from pyglet.gl import *
from pyglet.graphics import Batch
from pyglet.sprite import Sprite
from pyglet.window import Window


class BackGround:

    def __init__(self, window: Window):
        self._window = window
        width, height = window.width, window.height
        self._bg_img = assets.loader.image(
            "textures/gui/options_background.png")
        self._batch = Batch()
        self._sprites = []
        self.resize(width, height)

    def draw(self):
        self._batch.draw()

    def resize(self, width: int, height: int):
        bgw, bgh = self._bg_img.width * 4, self._bg_img.height * 4
        if bgw * (width / bgw) > width and bgh * (height / bgh) > height:
            return
        del self._sprites
        self._sprites = []
        for x in range(0, width + bgw, bgw):
            for y in range(0, height + bgh, bgh):
                sprite = Sprite(self._bg_img, x, y, batch=self._batch)
                sprite.color = (128, 128, 128)
                sprite.scale = 4
                self._sprites.append(sprite)


__all__ = ("BackGround")
