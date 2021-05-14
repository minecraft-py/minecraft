from os.path import join

from Minecraft.gui.base import GUI
from Minecraft.source import resource_pack
from Minecraft.utils.utils import *

import pyglet
from pyglet.sprite import Sprite

class XPBar(GUI):

    def __init__(self):
        width, height = get_size()
        GUI.__init__(self, width, height)
        self._xpbar = Sprite(resource_pack.get_resource('textures/gui/icons').get_region(0, 187, 182, 5),
                x=(width - 364) / 2, y=48)
        self._xpbar.scale_x = 2
        self._xpbar.scale_y = 1.5

    def draw(self):
        self._xpbar.draw()

    def resize(self, width, height):
        self._xpbar.position = (width - 364) / 2, 48
