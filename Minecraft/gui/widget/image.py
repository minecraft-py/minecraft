from Minecraft.gui.widget.base import Widget
from Minecraft.utils.utils import *

from pyglet import image


class Image(Widget):

    def __init__(self, x, y, image):
        self._size = win_width, win_height = get_size()
        self._img = image.load(image)
        self._img.anchor_x = self._img.width / 2
        self._img.anchor_y = self._img.height / 2
        super().__init__(x, win_height - y, self._img.width, self._img.height)

    def draw(self):
        self._img.blit(self._x, self._y)

    def on_resize(self, width, height):
        self._x *= width / self._size[0]
        self._y = (height / self._size[1]) * self._y
        self._size = width, height
