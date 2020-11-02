from os.path import join

from Minecraft.gui.hud.base import HUD
from Minecraft.source import path
from Minecraft.utils.utils import *

import pyglet
from pyglet import image
from pyglet.sprite import Sprite


class Hunger(HUD):

    def __init__(self, batch=None):
        width, height = get_size()
        HUD.__init__(self, width, height, batch)
        self._status = []
        for i in range(1, 11):
            self._status.append(Sprite(image.load(join(path['texture.hud'], 'hunger.png')),
                x=width - i * 21, y=height - 21, batch=batch))

    def resize(self, width, height):
        for i in range(1, 11):
            self._status[i - 1].position = width - i * 21, height - 21
