from collections import deque
from hashlib import sha256
import time

from Minecraft.world.block import blocks
from Minecraft.utils.utils import *

from pyglet import graphics
from pyglet.gl import *
from opensimplex import OpenSimplex as simplex

class Chunk(object):
    
    def __init__(self, x, z, seed, world):
        self.position = (x, z)
        self.batch3d = graphics.Batch()
        self.seed = seed
        self.world = world
        self.blocks = {}
        self.change = {}
        self.shown = {}
        self._shown = {}
        self.queue = deque()

    def init_chunk(self):
        cx, cz = self.position
        for x in range(cx, cx+ 16):
            for z in range(cz, cz + 16):
                self.add_block((x, 0, z), 'bedrock', record=False)
        for x in range(cx, cx + 16):
            for y in range(1, 3):
                for z in range(cz, cz + 16):
                    self.add_block((x, y, z), 'dirt', record=False)
        for x in range(cx, cx + 16):
            for z in range(cz, cz + 16):
                self.add_block((x, y, z), 'grass', record=False)
    
    def exposed(self, position):
        x, y, z = position
        for dx, dy, dz in FACES:
            if self.world.get((x + dx, y + dy, z + dz)) is not None:
                return True
        else:
            return False
        
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

    def remove_block(self, position, sync=True, record=True):
        if position in self.blocks:
            del self.blocks[position]
            if record:
                self.change[pos2str(position)] = 'air'
            if sync:
                if position in self.shown:
                    self.hide_block(position)
                self.check_neighbors(position)
    
    def check_neighbors(self, position):
        x, y, z = position
        for dx, dy, dz in FACES:
            key = (x + dx, y + dy, z + dz)
            if self.world.get(key) is None:
                continue
            if self.exposed(key):
                if key not in self.shown and key in self.blocks:
                    self.blocks[key].on_neighbor_change(self.world, key, position)
                    self.show_block(key)
            else:
                if key in self.shown:
                    self.blocks[key].on_neighbor_change(self.world, key, position)
                    self.hide_block(key)
    
    def show_block(self, position, immediate=True):
        block = self.blocks[position]
        self.shown[position] = block
        if immediate:
            self._show_block(position, block)
        else:
            self._enqueue(self._show_block, position, block)

    def show_blocks(self):
        for block in self.blocks.keys():
            self.show_block(block)
    
    def _show_block(self, position, block):
        vertex_data = list(block.get_vertices(*position))
        texture_data = list(block.texture_data)
        color_data = None
        if hasattr(block, 'get_color'):
            color_data = block.get_color(0.5, 0.5)
        count = len(texture_data) // 2
        if color_data is None:
            self._shown[position] = self.batch3d.add(count, GL_QUADS, block.group,
                    ('v3f/static', vertex_data),
                    ('t2f/static', texture_data))
        else:
            self._shown[position] = self.batch3d.add(count, GL_QUADS, block.group,
                    ('v3f/static', vertex_data),
                    ('t2f/static', texture_data),
                    ('c3f/static', color_data))

    def hide_block(self, position, immediate=True):
        self.shown.pop(position)
        if immediate:
            self._hide_block(position)
        else:
            self._enqueue(self._hide_block, position)

    def _hide_block(self, position):
        self._shown.pop(position).delete()

    def _enqueue(self, func, *args):
        self.queue.append((func, args))

    def _dequeue(self):
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self):
        start = time.perf_counter()
        while self.queue and time.perf_counter() - start < 1.0 / TICKS_PER_SEC:
            self._dequeue()

    def process_entire_queue(self):
        while self.queue:
            self._dequeue()
