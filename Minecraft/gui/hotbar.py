from os.path import join

from Minecraft.gui.base import GUI
from Minecraft.source import path
from Minecraft.world.block import blocks, get_block_icon
from Minecraft.utils.utils import *

import pyglet
from pyglet import image
from pyglet.sprite import Sprite


class HotBar(GUI):

    def __init__(self):
        width, height = get_size()
        GUI.__init__(self, width, height)
        self._element = []
        self._items = []
        self._item = []
        self.start = Sprite(image.load(join(path['texture.ui'], 'hotbar_start.png')),
                x=(width - 450) / 2 - 2, y=5)
        self.start.scale = 2.5
        self.end = Sprite(image.load(join(path['texture.ui'], 'hotbar_end.png')),
                x=(width - 450) / 2 + 450, y=5)
        self.end.scale = 2.5
        for i in range(9):
            self._element.append(Sprite(image.load(join(path['texture.ui'], 'hotbar_%d.png' % i)),
                x=(width - 450) / 2 + 50 * i, y=5))
            self._element[i].scale = 2.5
        self.set_index(0)

    def draw(self):
        self.start.draw()
        self.end.draw()
        for i in range(len(self._element)):
            if i != self.index:
                self._element[i].draw()
        else:
            self._element[self.index].draw()
            for i in range(len(self._item)):
                self._item[i].draw()

    def set_all(self, items):
        width = get_size()[0]
        self._items = items
        for item in range(len(self._items)):
            if item <= len(self._element):
                self._item.append(Sprite(get_block_icon(blocks[self._items[item]], 64),
                    x =(width - 450) / 2 + 50 * item + 1, y=8))
                self._item[item].scale = 0.75
            else:
                return

    def set_index(self, index):
        width = get_size()[0]
        for i in range(len(self._element)):
            self._element[i] = Sprite(image.load(join(path['texture.ui'], 'hotbar_%d.png' % i)),
                x=(width - 450) / 2 + 50 * i, y=5)
            self._element[i].scale = 2.5
        if 0 <= index < len(self._element):
            self._element[index] = Sprite(image.load(join(path['texture.ui'], 'hotbar_highlight.png')),
                    x=(width - 450) / 2 + 50 * index - 5, y=3)
            self._element[index].scale = 2.5
            self.index = index

    def resize(self, width, height):
        self.start.position = (width - 450) / 2 - 2, 5
        self.end.position = (width - 450) / 2 + 450, 5
        for i in range(len(self._element)):
            if i != self.index:
                self._element[i].position = (width - 450) / 2 + 50 * i, 5
            else:
                self._element[i].position = (width - 450) / 2 + 50 * i - 5, 3
        for i in range(len(self._item)):
            self._item[i].position = (width - 450) / 2 + 50 * i + 1, 8
