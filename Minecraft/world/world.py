from collections import deque
import math
import os
import random
import time

import Minecraft.archiver as archiver
from Minecraft.source import get_lang
from Minecraft.world.block import blocks
from Minecraft.utils.utils import *

msg = "module '{0}' not found, run `pip install {0}` to install, exit"

try:
    from opensimplex import OpenSimplex
except ModuleNotFoundError:
    log_err(msg.format('opensimplex'))
    exit(1)

import pyglet
from pyglet.gl import *

class World(object):

    def __init__(self, name):
        # Batch 是用于批处理渲染的顶点列表的集合
        self.batch3d = pyglet.graphics.Batch()
        # 透明方块
        self.batch3d_transparent = pyglet.graphics.Batch()
        # 为了分开绘制3D物体和2D的 HUD, 我们需要两个 Batch
        self.batch2d = pyglet.graphics.Batch()
        # 存档名
        self.name = name
        # 种子
        self.seed = archiver.load_info(name)['seed']
        # Simplex 噪声函数
        self.simplex = OpenSimplex(seed=self.seed)
        # world 存储着世界上所有的方块
        self.world = {}
        # 类似于 world, 但它只存储要显示的方块
        self.shown = {}
        self._shown = {}
        # 记录玩家改变的方块
        self.change = {}
        self.sectors = {}
        self.queue = deque()
        # 初始化是否完成
        self.is_init = True

    def init_world(self):
        # 放置所有方块以初始化世界, 非常耗时
        get_game().loading.draw()
        if archiver.load_info(self.name)['type'] == 'flat':
            self.init_flat_world()
        else:
            self.init_random_world()
        archiver.load_block(self.name, self.add_block, self.remove_block)
        self.is_init = False

    def init_flat_world(self):
        # 生成平坦世界
        for x in range(-MAX_SIZE, MAX_SIZE + 1):
            for z in range(-MAX_SIZE, MAX_SIZE + 1):
                self.add_block((x, 0, z), 'bedrock', record=False)
        for x in range(-MAX_SIZE, MAX_SIZE + 1):
            for y in range(1, 6):
                for z in range(-MAX_SIZE, MAX_SIZE + 1):
                    if y == 5:
                        self.add_block((x, y, z), 'grass', record=False)
                    else:
                        self.add_block((x, y, z), 'dirt', record=False)

    def init_random_world(self):
        # 生成随机世界
        for x in range(-MAX_SIZE, MAX_SIZE + 1):
            for z in range(-MAX_SIZE, MAX_SIZE + 1):
                self.add_block((x, 0, z), 'bedrock', record=False)
        for x in range(-MAX_SIZE, MAX_SIZE + 1):
            for z in range(-MAX_SIZE, MAX_SIZE + 1):
                h = int(self.simplex.noise2d(x=x / 20, y=z / 20) * 5 + SEA_LEVEL)
                for y in range(1, h):
                    self.add_block((x, y, z), 'dirt', record=False)
                else:
                    self.add_block((x, h, z), 'grass', record=False)

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
            pos = (x + dx, y + dy, z + dz)
            if  pos not in self.world:
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
        if position in self.world:
            self.remove_block(position, immediate, record=False)
        if -64 <= position[1] < 512:
            # 建筑限制为-64格以上, 512格以下
            if record == True:
                self.change[pos2str(position)] = block
            if block in blocks:
                self.world[position] = blocks[block]
                self.world[position].on_build(get_game(), position)
            else:
                # 将不存在的方块替换为 missing
                self.world[position] = blocks['missing']
            self.sectors.setdefault(sectorize(position), []).append(position)
            if self.exposed(position):
                self.show_block(position)
            if not self.world[position].transparent:
                self.check_neighbors(position)
        else:
            if position[1] >= 256:
                get_game().dialogue.add_dialogue(get_lang('game.text.build_out_of_world')[0] % 512)
            else:
                get_game().dialogue.add_dialogue(get_lang('game.text.build_out_of_world')[1])

    def remove_block(self, position, immediate=True, record=True):
        """
        在 position 处移除一个方块

        :param: position 长度为3的元组, 要移除方块的位置
        :param: immediate 是否要从画布上立即移除方块
        :param: record 是否记录方块更改(在 add_block 破坏后放置时不记录)
        """
        if position in self.world:
            # 不加这个坐标是否存在于世界中的判断有极大概率会抛出异常
            self.world[position].on_destroy(get_game(), position)
            del self.world[position]
            if record:
                self.change[pos2str(position)] = 'air'
            self.sectors[sectorize(position)].remove(position)
            if position in self.shown:
                self.hide_block(position)
            self.check_neighbors(position)

    def get(self, position):
        return self.world.get(position, None)

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
                    self.world[key].on_neighbor_change(self.world, key, position)
                    self.show_block(key)
            else:
                if key in self.shown:
                    self.world[key].on_neighbor_change(self.world, key, position)
                    self.hide_block(key)

    def show_block(self, position, immediate=True):
        """
        在 position 处显示方块, 这个方法假设方块在 add_block() 已经添加

        :param: position 长度为3的元组, 要显示方块的位置
        :param: immediate 是否立即显示方块
        """
        block = self.world[position]
        self.shown[position] = block
        if immediate:
            self._show_block(position, block)
        else:
            self._enqueue(self._show_block, position, block)

    def _show_block(self, position, block):
        """
        show_block() 方法的私有实现

        :param: position 长度为3的元组, 要显示方块的位置
        :param: block 方块
        """
        vertex_data = list(block.get_vertices(*position))
        texture_data = list(block.texture_data)
        color_data = None
        if hasattr(block, 'get_color'):
            _, y, _ = position
            if y <= 10:
                t = 0.8
            else:
                t = 0.8 - (y - 0.8) * 1/600
            h = 0.35
            color_data = block.get_color(t, h)
        count = len(texture_data) // 2
        batch = self.batch3d
        if block.transparent:
            batch = self.batch3d_transparent
        if color_data is None:
            self._shown[position] = batch.add(count, GL_QUADS, block.group,
                    ('v3f/static', vertex_data),
                    ('t2f/static', texture_data))
        else:
            self._shown[position] = batch.add(count, GL_QUADS, block.group,
                    ('v3f/static', vertex_data),
                    ('t2f/static', texture_data),
                    ('c3f/static', color_data))

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
        if not self.is_init:
            start = time.perf_counter()
            while self.queue and time.perf_counter() - start < 1.0 / TICKS_PER_SEC:
                self._dequeue()

    def process_entire_queue(self):
        # 处理所有事件
        while self.queue:
            self._dequeue()

    def draw(self):
        self.batch3d.draw()
        self.batch3d_transparent.draw()
