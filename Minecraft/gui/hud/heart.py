from os.path import join

from Minecraft.gui.hud.base import HUD
from Minecraft.source import path
from Minecraft.utils.utils import *

import pyglet
from pyglet import image
from pyglet.sprite import Sprite


class Heart(HUD):

    def __init__(self):
        width, height = get_size()
        HUD.__init__(self, width, height)
        self._status = []
        for i in range(10):
            sprite = Sprite(image.load(join(path['texture.gui'], 'icons.png')).get_region(16, 247, 9, 9),
                    x=(width - 364) / 2 + i * 13.5, y=56)
            sprite.scale = 1.5
            self._status.append(sprite)

    def draw(self):
        for item in self._status:
            item.draw()

    def resize(self, width, height):
        for i in range(10):
            self._status[i].position = (width - 364) / 2 + i * 13.5, 56
