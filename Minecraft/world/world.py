from collections import deque
import math
import os
import random
import time

import Minecraft.saver as saver
from Minecraft.source import block, path, settings
from Minecraft.utils.utils import *

import pyglet
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet import image

class World(object):

    def __init__(self, name):
        # Batch 是用于批处理渲染的顶点列表的集合
        self.batch3d = pyglet.graphics.Batch()
        # 为了分开绘制3D物体和2D的 HUD, 我们需要两个 Batch
        self.batch2d = pyglet.graphics.Batch()
        # 纹理的集合
        self.group = TextureGroup(image.load(os.path.join(path['texture'], 'block.png')).get_texture())
        # 存档名
        self.name = name
        # world 存储着世界上所有的方块
        self.world = {}
        # 类似于 world, 但它只存储要显示的方块
        self.shown = {}
        # Mapping from position to a pyglet `VertextList` for all shown blocks.
        self._shown = {}
        # 记录玩家改变的方块
        self.change = {}
        # Mapping from sector to a list of positions inside that sector.
        self.sectors = {}
        # Simple function queue implementation. The queue is populated with
        # _show_block() and _hide_block() calls
        self.queue = deque()

    def init_world(self):
        # 放置所有方块以初始化世界, 非常耗时
        for x in range(-MAX_SIZE, MAX_SIZE + 1):
            for z in range(-MAX_SIZE, MAX_SIZE + 1):
                self.add_block((x, 0, z), 'bedrock', record=False)
        for x in range(-MAX_SIZE, MAX_SIZE + 1):
            for y in range(1, 3):
                for z in range(-MAX_SIZE, MAX_SIZE + 1):
                    self.add_block((x, y, z), 'dirt', record=False)
        for x in range(-MAX_SIZE, MAX_SIZE + 1):
            for z in range(-MAX_SIZE, MAX_SIZE + 1):
                self.add_block((x, y, z), 'grass', record=False)
        saver.load_block(self.name, self.add_block, self.remove_block)

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
            if key != previous and key in self.world:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        else:
            return None, None

    def exposed(self, position):
        # 如果 position 所有的六个面旁边都有方块, 返回 False. 否则返回 True
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        else:
            return False

    def add_block(self, position, texture, immediate=True, record=True):
        """
        在 position 处添加一个纹理为 texture 的方块

        :param: pssition 长度为3的元组, 要添加方块的位置
        :param: texture 长度为3的列表, 纹理正方形的坐标, 使用 tex_coords() 创建
        :param: immediate 是否立即绘制方块
        :param: record 是否记录方块更改(在生成地形时不记录)
        """
        if position in self.world:
            self.remove_block(position, immediate, record=False)
        if 0 <= position[1] <= 256:
            # 建筑限制为基岩以上, 256格以下.
            if record == True:
                self.change[pos2str(position)] = texture
            if texture in block:
                self.world[position] = texture
            else:
                # 将不存在的方块替换为 undefined
                self.world[position] = 'undefined'
            self.sectors.setdefault(sectorize(position), []).append(position)
            if immediate:
                if self.exposed(position):
                    self.show_block(position)
                self.check_neighbors(position)

    def remove_block(self, position, immediate=True, record=True):
        """
        在 position 处移除一个方块

        :param: position 长度为3的元组, 要移除方块的位置
        :param: immediate 是否要从画布上立即移除方块
        :param: record 是否记录方块更改(在 add_block 破坏后放置时不记录)
        """
        if position in self.world:
            # 不加这个坐标是否存在于世界中的判断有极大概率会抛出异常
            del self.world[position]
            if record:
                self.change[' '.join([str(i) for i in position])] = 'air'
            self.sectors[sectorize(position)].remove(position)
            if immediate:
                if position in self.shown:
                    self.hide_block(position)
                self.check_neighbors(position)

    def check_neighbors(self, position):
        """
        检查 position 周围所有的方块, 确保它们的状态是最新的.
        这意味着将隐藏不可见的方块, 并显示可见的方块.
        通常在添加或删除方块时使用.
        """
        x, y, z = position
        for dx, dy, dz in FACES:
            key = (x + dx, y + dy, z + dz)
            if key not in self.world:
                continue
            if self.exposed(key):
                if key not in self.shown:
                    self.show_block(key)
            else:
                if key in self.shown:
                    self.hide_block(key)

    def show_block(self, position, immediate=True):
        """
        在 position 处显示方块, 这个方法假设方块在 add_block() 已经添加

        :param: position 长度为3的元组, 要显示方块的位置
        :param: immediate 是否立即显示方块
        """
        texture = block[self.world[position]]
        self.shown[position] = texture
        if immediate:
            self._show_block(position, texture)
        else:
            self._enqueue(self._show_block, position, texture)

    def _show_block(self, position, texture):
        """
        show_block() 方法的私有实现

        :param: position 长度为3的元组, 要显示方块的位置
        :param: texture 长度为3的列表, 纹理正方形的坐标, 使用 Minecraft.utils.utils.tex_coords() 创建
        """
        x, y, z = position
        vertex_data = cube_vertices(x, y, z, 0.5)
        texture_data = list(texture)
        # 创建向量列表
        # FIXME 应该使用 add_indexed() 来代替
        self._shown[position] = self.batch3d.add(24, GL_QUADS, self.group,
            ('v3f/static', vertex_data),
            ('t2f/static', texture_data))

    def hide_block(self, position, immediate=True):
        """
        隐藏在 position 处的方块, 它不移除方块

        :param: position 长度为3的元组, 要隐藏方块的位置
        :param: immediate 是否立即隐藏方块
        """
        self.shown.pop(position)
        if immediate:
            self._hide_block(position)
        else:
            self._enqueue(self._hide_block, position)

    def _hide_block(self, position):
        # hide_block() 方法的私有实现
        self._shown.pop(position).delete()

    def show_sector(self, sector):
        # 确保该区域中的方块都会被绘制
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position):
                self.show_block(position, False)

    def hide_sector(self, sector):
        # 隐藏区域
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.hide_block(position, False)

    def change_sectors(self, before, after):
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
            for sector in show:
                self.show_sector(sector)
            for sector in hide:
                self.hide_sector(sector)

    def _enqueue(self, func, *args):
        # 把 func 添加到内部的队列
        self.queue.append((func, args))

    def _dequeue(self):
        # 从内部队列顶部弹出函数并调用之
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self):
        # 处理事件
        start = time.perf_counter()
        while self.queue and time.perf_counter() - start < 1.0 / TICKS_PER_SEC:
            self._dequeue()

    def process_entire_queue(self):
        # 处理所有事件
        while self.queue:
            self._dequeue()
