from collections import deque
import math
import os
import random
import time

import Minecraft.archiver as archiver
from Minecraft.source import path, settings
from Minecraft.world.chunk import Chunk
from Minecraft.utils.utils import *

msg = "module '{0}' not found, run `pip install {0}` to install, exit"

try:
    from opensimplex import OpenSimplex
except ModuleNotFoundError:
    log_err(msg.format('opensimplex'))
    exit(1)

import pyglet
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet import image

class World(object):

    def __init__(self, name, game):
        # 为了分开绘制3D物体和2D的 HUD, 我们需要两个 Batch
        self.batch2d = pyglet.graphics.Batch()
        # 存档名
        self.name = name
        # 父对象
        self.game = game
        # 区块
        self.chunk = {}
        # 种子
        self.seed = archiver.load_info(name)['seed']

    def init_world(self, position):
        position = normalize(position)
        for x in range(position[0] - 4, position[0] + 3):
            for z in range(position[2] - 4, position[2] + 3):
                self.add_chunk((x, z))

    def get(self, position):
        cx, _, cz = sectorize(position)
        if (cx, cz) in self.chunk:
            return self.chunk[cx, cz].blocks.get(position, None)

    def hit_test(self, position, vector, max_distance=8):
        """
        从当前位置开始视线搜索, 如果有任何方块与之相交, 返回之.
        如果没有找到, 返回 (None, None)

        :param: position 长度为3的元组, 当前位置
        :param: vector 长度为3的元组, 视线向量
        :param: max_distance 在多少方块的范围内搜索
        """
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in range(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and self.get(key) is not None:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        else:
            return None, None

    def exposed(self, position):
        # 如果 position 所有的六个面旁边都有方块, 返回 False. 否则返回 True
        x, y, z = position
        for dx, dy, dz in FACES:
            if self.get((x + dx, y + dy, z + dz)) is not None:
                return True
        else:
            return False

    def add_block(self, position, block, immediate=True, record=True):
        """
        在 position 处添加一个方块

        :param: pssition 长度为3的元组, 要添加方块的位置
        :param: block 方块
        :param: immediate 是否立即绘制方块
        :param: record 是否记录方块更改(在生成地形时不记录)
        """
        chunk = sectorize(position)
        self.chunk[chunk[0], chunk[2]].add_block(position, block, immediate, record)

    def add_chunk(self, position):
        self.chunk[position] = Chunk(position[0], position[1], 0, self)
        self.chunk[position].init_chunk()
        self.chunk[position].show_blocks()

    def remove_block(self, position, immediate=True, record=True):
        """
        在 position 处移除一个方块

        :param: position 长度为3的元组, 要移除方块的位置
        :param: immediate 是否要从画布上立即移除方块
        :param: record 是否记录方块更改(在 add_block 破坏后放置时不记录)
        """
        chunk = sectorize(position)
        self.chunk[chunk[0], chunk[2]].remove_block(position, immediate, record)

    def remove_chunk(self, position):
        if position in self.chunk:
            del self.chunk[position]

    def check_neighbors(self, position):
        """
        检查 position 周围所有的方块, 确保它们的状态是最新的.
        这意味着将隐藏不可见的方块, 并显示可见的方块.
        通常在添加或删除方块时使用.
        """
        chunk = sectors(position)
        self.chunk[chunk[0], chunk[2]].check_neighbors(position)

    def show_chunk(self, chunk):
        # 确保该区域中的方块都会被绘制
        if chunk in self.chunk:
            self.chunk[chunk].show_blocks()
        else:
            self.add_chunk(chunk)
            self.chunk[chunk].show_blocks()

    def hide_chunk(self, chunk):
        # 隐藏区域
        self.remove_chunk(chunk)

    def change_chunk(self, before, after):
        """
        改变玩家所在区域

        :param: before 之前的区域
        :param: after 现在的区域
        """
        before_set = set()
        after_set = set()
        pad = 4
        for dx in range(-pad, pad + 1):
            for dy in [0]:
                for dz in range(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        else:
            show = after_set - before_set
            hide = before_set - after_set
            for chunk in show:
                self.show_chunk(chunk)
            for sector in hide:
                self.hide_chunk(chunk)

    def draw(self):
        for chunk in self.chunk.values():
            chunk.batch3d.draw()

    def process_queue(self):
        # 处理事件
        for chunk in self.chunk.values():
            chunk.process_queue()

    def process_entire_queue(self):
        # 处理所有事件
        for chunk in self.chunk.values():
            chunk.process_entire_queue()
