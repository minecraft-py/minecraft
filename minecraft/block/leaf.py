from minecraft.block.base import Block
from minecraft.block.base import BlockColorizer
from minecraft.utils.utils import *


class Leaf(Block):
    colorizer = BlockColorizer('foliage')
    name = 'leaf'
    textures = 'oak_leaves',
    transparent = True

    def get_color(self, temp, rainfall, brightness=16):
        color = []
        color.extend(get_color_by_brightness(brightness, self.colorizer.get_color(temp, rainfall)) * 24)
        return color
