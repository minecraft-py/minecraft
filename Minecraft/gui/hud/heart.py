from os.path import join

from Minecraft.gui.hud.base import HUD
from Minecraft.source import path
from Minecraft.utils.utils import *

import pyglet
from pyglet import image
from pyglet.sprite import Sprite


class Heart(HUD):

    def __init__(self, batch=None):
        width, height = get_size()
        HUD.__init__(self, width, height, batch)
        self._status = []
        for i in range(10):
            self._status.append(Sprite(image.load(join(path['texture.hud'], 'heart.png')),
                x=(width - 450) // 2 + i * 20, y=64, batch=batch))

    def resize(self, width, height):
        for i in range(10):
            self._status[i].position = (width - 450) // 2 + i * 20, 64
