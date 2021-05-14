from os.path import join

from Minecraft.gui.hud.base import HUD
from Minecraft.source import resource_pack
from Minecraft.utils.utils import *

import pyglet
from pyglet.sprite import Sprite


class Hunger(HUD):

    def __init__(self):
        width, height = get_size()
        HUD.__init__(self, width, height)
        self._status = []
        for i in range(9, -1, -1):
            sprite = Sprite(resource_pack.get_resource('textures/gui/icons').get_region(16, 220, 9, 9),
                x=(width - 364) / 2 + 364 - (i + 1) * 13.5, y=56)
            sprite.scale = 2
            self._status.append(sprite)

    def draw(self):
        for item in self._status:
            item.draw()

    def resize(self, width, height):
        for i in range(9, -1, -1):
            self._status[i].position = (width - 364) / 2 + 364 - (i + 1) * 13.5, 56
