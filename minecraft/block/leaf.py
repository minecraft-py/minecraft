from minecraft.block.base import Block
from minecraft.block.base import BlockColorizer


class Leaf(Block):
    colorizer = BlockColorizer('foliage')
    name = 'leaf'
    textures = 'oak_leaves',
    transparent = True

    def get_color(self, temp, rainfall):
        color = []
        color.extend(list(self.colorizer.get_color(temp, rainfall)) * 24)
        return color
