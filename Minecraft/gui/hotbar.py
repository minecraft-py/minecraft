from os.path import join

import pyglet
from pyglet import image
from pyglet.sprite import Sprite

from Minecraft.gui.base import GUI
from Minecraft.source import path


class HotBar(GUI):

    def __init__(self, width, height):
        GUI.__init__(self, width, height)
        self._element = []
        for i in range(9):
            self._element.append(Sprite(image.load(join(path['texture.ui'], 'hotbar-%d.png' % i)),
                x=(width - 360) // 2 + i * 40, y=5))
            self._element[i].scale = 2
            self._element[i].opacity = 200
        self.set_index(width, 0)

    def draw(self):
        for i in range(len(self._element)):
            if i != self.index:
                self._element[i].draw()
        else:
            self._element[self.index].draw()

    def set_index(self, width, index):
        for i in range(len(self._element)):
            self._element[i] = Sprite(image.load(join(path['texture.ui'], 'hotbar-%d.png' % i)),
                x=(width - 360) // 2 + i * 40, y=5)
            self._element[i].scale = 2
            self._element[i].opacity = 200
        if 0 <= index < len(self._element):
            self._element[index] = Sprite(image.load(join(path['texture.ui'], 'hotbar-highlight.png')),
                    x=(width - 360) // 2 + index * 40 - 2, y=3)
            self._element[index].scale = 2
            self.index = index

    def resize(self, width, height):
        for i in range(len(self._element)):
            if i != self.index:
                self._element[i].position = (width - 360) // 2 + i * 40, 5
            else:
                self._element[i].position = (width - 360) // 2 + i * 40 - 2, 3
