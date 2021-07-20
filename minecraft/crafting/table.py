from minecraft.crafting.recipe import match_recipe
from minecraft.gui.widget.slot import ItemSlot
from minecraft.utils.utils import *


class CraftingTable(): 

    def __init__(self, x, y, size):
        self._x = x
        self._y = y
        self._size = min(3, max(2, size))
        self._slots = dict()
        self._output_offset = (0, 0)
        self._output = None
        index = -1
        for x in range(self._size):
            for y in range(0, -self._size, -1):
                self._slots.setdefault((x, -y), ItemSlot(self._x + 36 * x,
                    self._y + 36 * y, index))
                self._slots[x, -y].register_event('change', self.on_change)
                index += 1

    def set_output(self, offset_x, offset_y):
        self._output_offset = offset_x, offset_y
        self._output = ItemSlot(self._x + offset_x, self._y + offset_y, index=4)
        self._output.set_state(False, True)
        self._output.register_event('change', self.on_output_change)

    def clear(self):
        for slot in self._slots.values():
            slot.set_item()

    def resize(self, x, y):
        self._x = x
        self._y = y
        for x in range(self._size):
            for y in range(0, -self._size, -1):
                self._slots[x, -y].x = self._x + 36 * x
                self._slots[x, -y].y = self._y + 36 * y
        if self._output is not None:
            self._output.x = self._x + self._output_offset[0]
            self._output.y = self._y + self._output_offset[1]

    def on_change(self, buttons, modifiers, index):
        data = list()
        for slot in self._slots.values():
            data.append(slot.get_item())
        result = match_recipe(data)
        if result == False:
            self._output.set_item()
        else:
            self._output.set_item(result['item'])

    def on_output_change(self, buttons, modifiers, index):
        if self._output.get_item() is None:
            for slot in self._slots.values():
                slot.set_item()

    def slots(self):
        l = list()
        for slot in self._slots.values():
            l.append(slot)
        if self._output is not None:
            l.append(self._output)
        return l
