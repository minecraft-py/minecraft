# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from minecraft.utils.utils import *

from pyglet.shapes import Rectangle
from pyglet.sprite import Sprite


class LoadingBackground():

    def __init__(self, opacity=100):
        # 加载时使用的背景
        width, height = get_size()
        self._rect = Rectangle(0, 0, width, height, color=(0, 0, 0))
        self._rect.opacity = opacity
        self._elements = []
        self._img = get_game().resource_pack.get_resource("textures/gui/options_background")
        for x in range(0, width + self._img.width * 4, self._img.width * 4):
            for y in range(0, height + self._img.height * 4, self._img.height * 4):
                sprite = Sprite(self._img, x=x, y = y)
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
                sprite = Sprite(self._img, x=x, y = y)
                sprite.scale = 4
                self._elements.append(sprite)
