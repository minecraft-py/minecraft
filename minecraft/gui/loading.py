from minecraft.utils.utils import *

import pyglet
from pyglet.sprite import Sprite


class LoadingBackground():

    def __init__(self):
        width, height = get_size()
        self._elements = []
        self._img = get_game().resource_pack.get_resource('textures/gui/options_background')
        for x in range(0, width + self._img.width * 4, self._img.width * 4):
            for y in range(0, height + self._img.height * 4, self._img.height * 4):
                sprite = Sprite(self._img, x=x, y = y)
                sprite.scale = 4
                self._elements.append(sprite)
    
    def draw(self):
        for img in self._elements:
            img.draw()
    
    def resize(self, width, height):
        self._elements = []
        for x in range(0, width + self._img.width * 4, self._img.width * 4):
            for y in range(0, height + self._img.height * 4, self._img.height * 4):
                sprite = Sprite(self._img, x=x, y = y)
                sprite.scale = 4
                self._elements.append(sprite)
        