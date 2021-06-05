from minecraft.block.base import Block
from minecraft.entity.item.tnt import ExplodingTNT
from minecraft.utils.utils import *


class TNT(Block):
    name = 'tnt'
    textures = 'tnt_top', 'tnt_bottom', 'tnt_side', 'tnt_side'

    def on_use(self, fuse=4):
        get_game().entities.add_entity(ExplodingTNT(self.position, fuse=fuse))
        get_game().world.remove_block(self.position)
