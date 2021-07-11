from minecraft.gui.widget.base import Widget
from minecraft.utils.utils import *

from pyglet.shapes import Rectangle


class ItemSlot(Widget):
    
    def __init__(self, x, y, variable=True):
        y = get_size()[1] - y
        super().__init__(x, y, 32, 32)
        self._variable = variable
        self._on = False
        self.rect = Rectangle(self.x + 4, get_size()[1] - self.y - 8 - 24, 24, 24, color=(255, ) * 3)
        self.rect.opacity = 100

    def _update(self):
        self.rect.position = x + 4, get_size()[1] - y - 8 - 24

    def on_mouse_motion(self, x, y, dx, dy):
        if self.check_hit(x, get_size()[1] - y):
            self._on = True
        else:
            self._on = False

    def draw(self):
        if self._on:
            self.rect.draw()
