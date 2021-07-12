from minecraft.gui.widget.base import Widget
from minecraft.utils.utils import *

from pyglet.shapes import Rectangle


class ItemSlot(Widget):
    
    def __init__(self, x, y, variable=True):
        y = get_size()[1] - y
        super().__init__(x, y, 32, 32)
        self._variable = variable
        self._on = False
        self.rect = Rectangle(self.x, get_size()[1] - self.y - 32, 32, 32, color=(255, ) * 3)
        self.rect.opacity = 100

    def _update(self):
        self.rect.position = self.x, get_size()[1] - self.y - 32

    def on_mouse_motion(self, x, y, dx, dy):
        if self.check_hit(x, get_size()[1] - y):
            self._on = True
        else:
            self._on = False

    def draw(self):
        if self._on:
            self.rect.draw()


class BagSlot():

    def __init__(self, x, y):
        self.x = x
        self.y = y - 4
        self._slot = dict()
        self._slot['bag'] = dict()
        self._slot['hotbar'] = dict()
        for x in range(9):
            for y in range(0, -3, -1):
                self._slot['bag'].setdefault((x, y), ItemSlot(self.x + 36 * x, self.y + 36 * y))
            self._slot['hotbar'].setdefault(x, ItemSlot(self.x + 36 * x, self.y - 116))

    def resize(self, x, y):
        self.x = x
        self.y = y - 4
        for x in range(9):
            for y in range(0, -3, -1):
                self._slot['bag'][x, y].x = self.x + 36 * x
                self._slot['bag'][x, y].y = self.y + 36 * y
            self._slot['hotbar'][x].x = self.x + 36 * x
            self._slot['hotbar'][x].y = self.y - 116

    def slots(self):
        slots = list()
        for slot0 in self._slot.values():
            for slot in slot0.values():
                slots.append(slot)
        else:
            return slots
