from minecraft.gui.frame import Frame
from minecraft.gui.widget.image import Image
from minecraft.gui.widget.slot import BagSlot
from minecraft.source import resource_pack
from minecraft.utils.utils import *

import pyglet

class CraftingTable():

    def __init__(self, game):
        width, height = get_size()
        self.game = game
        self.frame = Frame(self.game, True)
        self._table = Image((width - 352) / 2, (height - 332) / 2,
                resource_pack.get_resource('textures/gui/containers/crafting_table').get_region(0, 90, 176, 166))
        self._table.sprite.scale = 2
        self._slot = BagSlot((width - 352) / 2 + 16, (height - 332) / 2 + 168)

        def on_resize(width, height):
            self._table.sprite.position = (width - 352) / 2, (height - 332) / 2
            self._slot.resize((width - 352) / 2 + 16, (height - 332) / 2 + 168)

        self.frame.register_event('resize', on_resize)
        self.frame.add_widget(self._table)
        for slot in self._slot.slots():
            self.frame.add_widget(slot)
