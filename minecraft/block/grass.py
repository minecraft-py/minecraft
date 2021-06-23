from minecraft.block.base import Block
from minecraft.block.base import BlockColorizer
from minecraft.utils.utils import *


class Grass(Block):
    colorizer = BlockColorizer('foliage')
    name = 'grass'
    textures = 'grass_top', 'dirt', 'grass_side', 'grass_side'

    def get_color(self, temp, rainfall):
        color = []
        color.extend(list(self.colorizer.get_color(temp, rainfall)) * 4)
        color.extend([1] * 60)
        return color

    def get_item_color(self):
        color = []
        color.extend(list(self.colorizer.get_color(0.8, 0.4)) * 4)
        color.extend([1] * 60)
        return color

    def on_ticking(self, pos):
        block = get_game().world.get((pos[0], pos[1] + 1, pos[2]))
        if block != None:
            if block.transparent != True:
                get_game().world.add_block(pos, 'dirt')
