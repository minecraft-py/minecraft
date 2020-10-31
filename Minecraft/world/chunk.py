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

    def generate(self):
        pass

    def destroy(self, position, i):
        if position in self.block:
            self.block[position].destroy(i)
            if self.block[position].has_destroy:
                del self.block[position]
