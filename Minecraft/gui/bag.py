from os.path import join

from Minecraft.gui.base import GUI
from Minecraft.source import path
from Minecraft.utils.utils import *

import pyglet
from pyglet import image
from pyglet.sprite import Sprite


class Bag(GUI):

    def __init__(self):
        width, height = get_size()
        GUI.__init__(self, width, height)
        self._element = {}
        self._element['panel'] = Sprite(image.load(join(path['texture.gui'], 'containers', 'inventory.png')).get_region(0, 90, 176, 166),
                x=(width - 264) / 2, y=(height - 279) / 2)
        self._element['panel'].scale = 1.5
        
    def draw(self):
        get_game().full_screen.color = (0, 0, 0)
        get_game().full_screen.opacity = 100
        get_game().full_screen.draw()
        self._element['panel'].draw()

    def resize(self, width, height):
        self._element['panel'].position = (width - 264) / 2, (height - 279) / 2
