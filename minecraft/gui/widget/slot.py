from minecraft.block import blocks
from minecraft.block.base import get_block_icon
from minecraft.gui.widget.base import Widget
from minecraft.utils.utils import *

from pyglet.shapes import Rectangle
from pyglet.sprite import Sprite
from pyglet.window import mouse


class ItemSlot(Widget):
    
    def __init__(self, x, y, index=None):
        y = get_size()[1] - y
        super().__init__(x, y, 32, 32)
        self._index = index
        self._on = False
        self._item = self._item_name = None
        self._state = {'set': True, 'get': True}
        self._rect = Rectangle(self.x, get_size()[1] - self.y - 32, 32, 32, color=(255, ) * 3)
        self._rect.opacity = 100

    def _update(self):
        self._rect.position = self.x, get_size()[1] - self.y - 32
        if self._item is not None:
            self._item.position = self.x, get_size()[1] - self.y - 32

    def on_mouse_motion(self, x, y, dx, dy):
        if self.check_hit(x, get_size()[1] - y):
            self._on = True
        else:
            self._on = False

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self._on:
            return
        if buttons == mouse.LEFT:
            i1, i2 = self._item_name, get_game().get_active_item()
            if all(self._state.values()):
                self.set_item(i2)
                get_game().set_active_item(i1)
            elif self._state['set']:
                if get_game().get_active_item() is not None:
                    self.set_item(i2)
                    get_game().set_active_item(i1)
            elif self._state['get']:
                if get_game().get_active_item() is None:
                    self.set_item()
                    get_game().set_active_item(i1)
        elif buttons == mouse.MIDDLE:
            get_game().set_active_item(self._item_name)
        if hasattr(self, 'on_change'):
            self.on_change(buttons, modifiers, self._index)

    def set_item(self, item=None):
        if item is None:
            self._item_name = self._item = None
        else:
            self._item_name = item
            self._item = Sprite(get_block_icon(blocks[item], 32), x=self.x, y=get_size()[1] - self.y - 32)

    def set_state(self, set_=True, get=True):
        self._state['set'] = set_
        self._state['get'] = get

    def get_item(self):
        return self._item_name

    def draw(self):
        if self._item is not None:
            self._item.draw()
        if self._on:
            self._rect.draw()


class BagSlot():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._slot = dict()
        self._slot['bag'] = dict()
        self._slot['hotbar'] = dict()
        for x in range(9):
            for y in range(0, -3, -1):
                self._slot['bag'].setdefault((x, -y), ItemSlot(self.x + 36 * x, self.y + 36 * y))
        for x in range(9):
            self._slot['hotbar'].setdefault(x, ItemSlot(self.x + 36 * x, self.y - 116))

    def resize(self, x, y):
        self.x = x
        self.y = y
        for x in range(9):
            for y in range(0, -3, -1):
                self._slot['bag'][x, -y].x = self.x + 36 * x
                self._slot['bag'][x, -y].y = self.y + 36 * y
            self._slot['hotbar'][x].x = self.x + 36 * x
            self._slot['hotbar'][x].y = self.y - 116

    def async_data(self, mode='open'):
        if mode == 'open':
            for i in range(len(get_game().inventory)):
                self._slot['hotbar'][i].set_item(get_game().inventory[i])
        elif mode == 'close':
            for i in range(len(get_game().inventory)):
                get_game().inventory[i] = self._slot['hotbar'][i].get_item()
            get_game().hud['hotbar'].set_all(get_game().inventory)

    def slots(self):
        slots = list()
        for slot0 in self._slot.values():
            for slot in slot0.values():
                slots.append(slot)
        else:
            return slots
