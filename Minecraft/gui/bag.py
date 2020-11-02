from os.path import join

from Minecraft.gui.base import GUI
from Minecraft.utils.utils import *

import pyglet
from pyglet.shapes import Rectangle


class Bag(GUI):

    def __init__(self):
        width, height = get_size()
        GUI.__init__(self, width, height)
        self._element = {}
        self._element['panel'] = Rectangle(x=(width - 600) // 2, y=(height - 400) // 2,
                width=600, height=400, color=(0, 0, 0))
        self._element['panel'].opacity = 128
        
    def draw(self):
        self._element['panel'].draw()

    def resize(self, width, height):
        self._element['panel'].position = (width - 600) // 2, (height - 400) // 2
