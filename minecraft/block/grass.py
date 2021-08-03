from minecraft.block.base import Block
from minecraft.block.base import BlockColorizer
from minecraft.utils.utils import *


class Grass(Block):
    colorizer = BlockColorizer('foliage')
    name = 'grass'
    textures = 'grass_top', 'dirt', 'grass_side', 'grass_side'

    def get_color(self, temp, rainfall, brightness=16):
        color = []
        color.extend(get_color_by_brightness(brightness, self.colorizer.get_color(temp, rainfall)) * 4)
        color.extend(get_color_by_brightness(brightness) * 20)
        return color

    def on_ticking(self, pos):
        pos = (pos[0], pos[1] + 1, pos[2])
        if (pos in get_game().world.world) and (not get_game().world.get(pos).transparent):
            get_game().world.add_block(pos, 'dirt')
