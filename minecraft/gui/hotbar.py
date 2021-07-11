from minecraft.gui.base import GUI
from minecraft.source import resource_pack
from minecraft.block import blocks
from minecraft.block.base import get_block_icon
from minecraft.utils.utils import *

import pyglet
from pyglet.sprite import Sprite


class HotBar(GUI):

    def __init__(self):
        width, height = get_size()
        GUI.__init__(self, width, height)
        self._index = 0
        self._item = list()
        self._items = list()
        self._hotbar = Sprite(resource_pack.get_resource('textures/gui/widgets').get_region(0, 234, 182, 22),
                x=(width - 364) / 2, y=0)
        self._select = Sprite(resource_pack.get_resource('textures/gui/widgets').get_region(0, 210, 24, 24),
                x=(width - 364) / 2 + 40 * self._index - 2, y=-2)
        self._hotbar.scale = 2
        self._select.scale = 2

    def draw(self):
        self._hotbar.draw()
        self._select.draw()
        for item in self._item:
            if item:
                item.draw()

    def set_all(self, items):
        width = get_size()[0]
        self._items = items
        self._item = list()
        for item in range(len(self._items)):
            if item <= 9:
                if self._items[item]:
                    self._item.append(Sprite(get_block_icon(blocks[self._items[item]], 128),
                        x =(width - 364) / 2 + 40 * item + 2, y=2))
                    self._item[item].scale = 40 / self._item[item].image.width
                else:
                    self._item.append(None)
            else:
                return

    def set_index(self, index):
        width = get_size()[0]
        self._index = index
        self._select.position = ((width - 364) / 2 + 40 * self._index - 2, -2)

    def resize(self, width, height):
       self._hotbar.position = (width - 364) / 2, 0
       self._select.position = (width - 364) / 2 + 40 * self._index - 2, -2
       for i in range(len(self._item)):
           if self._item[i]:
               self._item[i].position = (width - 364) / 2 + 40 * i + 2, 2
