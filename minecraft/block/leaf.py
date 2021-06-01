from minecraft.block.base import Block
from minecraft.block.base import BlockColorizer


class Leaf(Block):
    textures = 'leaves_oak',
    colorizer = BlockColorizer('foliage')

    def get_color(self, temp, rainfall):
        color = []
        color.extend(list(self.colorizer.get_color(temp, rainfall)) * 24)
        return color

    def get_item_color(self):
        color = []
        color.extend(list(self.colorizer.get_color(0.8, 0.4)) * 24)
        return color
