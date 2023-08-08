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

from typing import List

from pyglet.graphics import Batch
from pyglet.sprite import Sprite
from pyglet.window import Window

from minecraft import assets


class BackGround:
    def __init__(self, window: Window, darkness=0.5):
        assert 0 <= darkness <= 1
        self._window = window
        self._darkness = darkness
        if self._darkness < 0.01:
            self._darkness = 0.01
        width, height = window.width, window.height
        self._bg_img = assets.loader.image("textures/gui/options_background.png")
        self._batch = Batch()
        self._sprites: List[Sprite] = []
        self.resize(width, height)

    @property
    def darkness(self) -> float:
        return self._darkness

    @darkness.setter
    def darkness(self, value: float) -> None:
        assert 0 <= value <= 1
        self._darkness = value
        if self._darkness < 0.01:
            self._darkness = 0.01
        for sprite in self._sprites:
            sprite.color = (256 * (1 - self._darkness),) * 3

    def draw(self) -> None:
        self._batch.draw()

    def resize(self, width: int, height: int) -> None:
        bgw, bgh = self._bg_img.width * 4, self._bg_img.height * 4
        if bgw * (width / bgw) > width and bgh * (height / bgh) > height:
            return
        del self._sprites
        self._sprites = []
        for x in range(0, width + bgw, bgw):
            for y in range(0, height + bgh, bgh):
                sprite = Sprite(self._bg_img, x, y, batch=self._batch)
                sprite.color = (256 * (1 - self._darkness),) * 3
                sprite.scale = 4
                self._sprites.append(sprite)


__all__ = "BackGround"
