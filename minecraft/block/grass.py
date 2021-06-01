from minecraft.block.base import Block
from minecraft.block.base import BlockColorizer
from minecraft.utils.utils import *


class Grass(Block):
    textures = 'grass_top',
    colorizer = BlockColorizer('foliage')

    def get_color(self, temp, rainfall):
        color = []
        color.extend(list(self.colorizer.get_color(temp, rainfall)) * 24)
        return color

    def get_item_color(self):
        color = []
        color.extend(list(self.colorizer.get_color(0.8, 0.4)) * 24)
        return color

    def on_ticking(self, pos):
        block = get_game().world.get((pos[0], pos[1] + 1, pos[2]))
        if block != None:
            if block.transparent != True:
                get_game().world.add_block(pos, 'dirt')
