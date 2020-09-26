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
                x=(width - 270) // 2 + i * 30, y=3))
            self._element[i].scale = 1.5
            self._element[i].opacity = 200
        self.set_index(width, 0)

    def draw(self):
        for i in range(len(self._element)):
            if i == self.index:
                pass
            else:
                self._element[i].draw()
        else:
            self._element[self.index].draw()

    def set_index(self, width, index):
        for i in range(len(self._element)):
            self._element[i] = Sprite(image.load(join(path['texture.ui'], 'hotbar-%d.png' % i)),
                x=(width - 270) // 2 + i * 30, y=3)
            self._element[i].scale = 1.5
            self._element[i].opacity = 200
        if 0 <= index < len(self._element):
            self._element[index] = Sprite(image.load(join(path['texture.ui'], 'hotbar-highlight.png')),
                    x=(width - 270) // 2 + index * 30 - 1, y=2)
            self._element[index].scale = 1.5
            self.index = index

    def resize(self, width, height):
        for i in range(len(self._element)):
            self._element[i].position = (width - 270) // 2 + i * 30, 3 if i == self.index else 2
