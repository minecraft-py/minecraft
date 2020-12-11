from collections import deque
from hashlib import sha256

from Minecraft.world.block import blocks
from Minecraft.utils.utils import *

from pyglet import graphics
from opensimplex import OpenSimplex as simplex

class Chunk(object):
    
    def __init__(self, x, z, seed, world):
        self.position = (x, z)
        self.seed = seed
        self.world = world
        self.blocks = {}
        self.shown = {}
        self._shown = {}
        self.queue = deque()

    def add_block(self, position, block, sync=True, record=True):
        if position in self.blocks:
            self.remove_block(position, sync, record=False)
        if 0 <= position[1] <= 256:
            if record:
                self.change[pos2str(position)] = block
            if block in blocks:
                self.blocks[position] = blocks[block]
            else:
                self.blocks[position] = blocks['missing']
        if sync:
            if self.exposed(position):
                self.show_block(position)
            self.check_neighbors(position)

    def remove_block(self, positioin, sync=True, record=True):
        if position in self.blocks:
            del self.blocks[position]
            if record:
                self.change[pos2str(position)] = 'air'
            if sync:
                if position in self.shown:
                    self.hide_block(position)
                self.check_neighbors(position)
