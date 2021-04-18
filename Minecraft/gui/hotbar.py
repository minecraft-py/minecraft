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
        self._index = 0
        self._item = list()
        self._items = list()
        self._hotbar = Sprite(image.load(join(path['texture.gui'], 'widgets.png')).get_region(0, 234, 182, 22),
                x=(width - 455) / 2, y=1)
        self._select = Sprite(image.load(join(path['texture.gui'], 'widgets.png')).get_region(0, 210, 24, 24),
                x=(width - 455) / 2 + 50 * self._index - 2, y=-2)
        self._hotbar.scale = 2.5
        self._select.scale = 2.5

    def draw(self):
        self._hotbar.draw()
        self._select.draw()
        for item in self._item:
            if item:
                item.draw()

    def set_all(self, items):
        width = get_size()[0]
        self._items = items
        for item in range(len(self._items)):
            if item <= 9:
                if self._items[item]:
                    self._item.append(Sprite(get_block_icon(blocks[self._items[item]], 128),
                        x =(width - 455) / 2 + 50 * item + 3, y=4))
                    self._item[item].scale = 48 / self._item[item].image.width
                else:
                    self._item.append(None)
            else:
                return

    def set_index(self, index):
        width = get_size()[0]
        self._index = index
        self._select.position = ((width - 455) / 2 + 50 * self._index - 2, -2)

    def resize(self, width, height):
       self._hotbar.position = (width - 455) / 2, 1
       self._select.position = (width - 455) / 2 + 50 * self._index - 2, -2
       for i in range(len(self._item)):
           if self._item[i]:
               self._item[i].position = (width - 455) / 2 + 50 * i + 3, 4
