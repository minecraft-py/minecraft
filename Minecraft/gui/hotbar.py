from os.path import join

import pyglet
from pyglet import image
from pyglet.sprite import Sprite

from Minecraft.gui.base import GUI
from Minecraft.source import path
from Minecraft.utils.utils import *


class HotBar(GUI):

    def __init__(self):
        width, height = get_size()
        GUI.__init__(self, width, height)
        self._element = []
        self.start = Sprite(image.load(join(path['texture.ui'], 'hotbar-start.png')),
                x=(width - 360) // 2 - 2, y=5)
        self.start.scale = 2
        self.end = Sprite(image.load(join(path['texture.ui'], 'hotbar-start.png')),
                x=(width - 360) // 2 + 360, y=5)
        self.end.scale = 2
        for i in range(9):
            self._element.append(Sprite(image.load(join(path['texture.ui'], 'hotbar-%d.png' % i)),
                x=(width - 360) // 2 + i * 40, y=5))
            self._element[i].scale = 2
        self.set_index(0)

    def draw(self):
        self.start.draw()
        self.end.draw()
        for i in range(len(self._element)):
            if i != self.index:
                self._element[i].draw()
        else:
            self._element[self.index].draw()

    def set_index(self, index):
        width = get_size()[0]
        for i in range(len(self._element)):
            self._element[i] = Sprite(image.load(join(path['texture.ui'], 'hotbar-%d.png' % i)),
                x=(width - 360) // 2 + i * 40, y=5)
            self._element[i].scale = 2
        if 0 <= index < len(self._element):
            self._element[index] = Sprite(image.load(join(path['texture.ui'], 'hotbar-highlight.png')),
                    x=(width - 360) // 2 + index * 40 - 4, y=3)
            self._element[index].scale = 2
            self.index = index

    def resize(self, width, height):
        self.start.position = (width - 360) // 2 - 2, 5
        self.end.position = (width - 360) // 2 + 360, 5
        for i in range(len(self._element)):
            if i != self.index:
                self._element[i].position = (width - 360) // 2 + i * 40, 5
            else:
                self._element[i].position = (width - 360) // 2 + i * 40 - 4, 3
