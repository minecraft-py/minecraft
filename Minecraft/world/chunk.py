from Minecraft.world.block import block

from pyglet import graphics
from opensimplex import OpenSimplex as simplex

class Chunk(object):
    
    def __init__(self, x, z, seed):
        self.batch = graphics.Batch()
        self.position = (x, z)
        self.noise = simplex(seed=seed)
        # 每一个方块的坐标: tuple(x, y, z)
        self.block = {}
        # 显示的方块
        self.shown = {}
        # 改变的方块
        self.change = {}

    def add_block(self, position, block, record=True):
        self.block[position] = block
        if record:
            self.change[pos2str(position)] = block
        
    def generate(self):
        pass

    def destroy(self, position, i=0.01):
        if position in self.block:
            self.block[position].destroy(i)
            if self.block[position].has_destroy:
                del self.block[position]
                del self.shown[position]
                self.change[pos2str(position)] = 'air'
