from Minecraft.world.block import block
from Minecraft.utils.utils import *

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

    def add_block(self, position, name, record=True):
        if 0 <= position[1] <= 256:
            if name in block:
                self.block[position] = name
                self,shown[position] = block[name].show(self.batch)
            else:
                self.block[position] = name
                self.shown[position] = block[name].show(self.batch)
            if record:
                self.change[pos2str(position)] = name

    def destroy(self, position, i=0.01):
        if position in self.block:
            self.block[position].destroy(i)
            if self.block[position].has_destroy:
                self.remove_block(position)

    def generate(self):
        raise NotImplementedError('not implemented')

    def remove_block(self, position, record=True):
        if position in self.block:
            del self.block[position]
            self.shown.pop(position)
            if record:
                self.change[pos2str(position)] = 'air'

    def show_chunk(self):
        self.batch.draw()
