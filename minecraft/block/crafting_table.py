from minecraft.block.base import Block
from minecraft.utils.utils import *


class CraftingTable(Block):
    name = 'crafting_table'
    textures = 'crafting_table_top', 'oak_planks', 'crafting_table_front', 'crafting_table_side'

    def on_use(self):
        get_game().toggle_gui('crafting_table')
