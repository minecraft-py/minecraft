from os.path import join

from Minecraft.gui.base import GUI
from Minecraft.source import path
from Minecraft.utils.utils import *

import pyglet
from pyglet import image
from pyglet.sprite import Sprite

class XPBar(GUI):

    def __init__(self):
        width, height = get_size()
        GUI.__init__(self, width, height)
        self._xp_bar = Sprite(image.load(join(path['texture.gui'], 'icons.png')).get_region(0, 187, 182, 5),
                x=(width - 455) / 2, y=61)
        self._xp_bar.scale_y = 2
        self._xp_bar.scale_x = 455 / 182

    def draw(self):
        self._xp_bar.draw()

    def resize(self, width, height):
        self._xp_bar.position = (width - 455) / 2, 61
