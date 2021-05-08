from Minecraft.gui.widget.base import Widget
from Minecraft.utils.utils import *

from pyglet.sprite import Sprite


class Image(Widget):

    def __init__(self, x, y, image):
        self._size = win_width, win_height = get_size()
        self.sprite = Sprite(image, x, y)
        super().__init__(x, y, image.width, image.height)

    def draw(self):
        self.sprite.draw()
