from minecraft.block.base import Block
from minecraft.utils.utils import *


class Dirt(Block):
    textures = 'dirt',

    def on_ticking(self, pos):
        block = get_game().world.get((pos[0], pos[1] + 1, pos[2]))
        if block == None:
            get_game().world.add_block(pos, 'grass')
