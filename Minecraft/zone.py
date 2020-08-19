# 区块系统

import json
from noise import snoise2 as noise2
import Minecraft.saver as saver

class Zone(object):

    def __init__(self, x, z):
        self.base = 40 + round(noise2(x, y) * 50)
        self.x, self.z = x, z
        self.x_start, self.z_start = 16 * x, 16 * z
        self.x_end, self.z_end = 16 * (x + 1), 16 * (z + 1)
        self.x_range, self.z_range = range(self.x_start, self.x_end + 1), range(self.x_start, z_end + 1)
        self.world = {}

    def __del__(self):
        data = {}
        for position, block in self.world.items():
            data[' '.join([str(i) for i in position])] = block
        else:
            saver.save_block('demo', self.world, full=False)
        for x in self.x_range:
            for y in range(0, 257):
                for z in self.z_range:
                    self.remove_block((x, y, z), record=False)

    def add_block(position, texture, immediate=True, record=True):
        # add_block 方法, 不要手动调用
        self._add_block_function(position, texture, immediate, record)
        self.world[position] = texture

    def remove_block(position, immediate=True, record=True):
        # remove_block 方法, 不要手动调用
        if position in self.world:
            del self.world[position]
            self._remove_block_function(position, immediate, record)

    def generate(self):
        # 生成区块
        for x in self.x_range:
            for y in range(0, 41):
                for z in self.z_range:
                    if y == 0:
                        # 生成基岩
                       self.add_block((x, y, z), 'bedrock', record=False)
                    else:
                        # 生成石头
                        self.add_block((x, y, z), 'stone', record=False)
        self.load_block()

    def load_block(self):
        blocks = json.load(open('resource/save/demo/demo.world'))
        for x in self.x_range:
            for y in range(0, 257):
                for z in z_range:
                    if (position := ' '.join([str(i) for i in (x, y, z)])) in blocks:
                        block = blocks[position]
                        if block = 'air':
                            self.remove_block((x, y, z))
                        else:
                            self.add_block((x, y, z), block)

    def set_add_function(self, function):
        self._add_block_function = function

    def set_remove_function(self, function):
        self._remove_block_function = function


class ZoneGroup(object):
    
    def __init__(self, max_sight=5):
        self.max_sight = max_sight - 1

    def setxy(self, x, z):
        """
        设置玩家所在的区块

        @param x 玩家所在的 x 轴位置
        @param z 玩家所在的 z 轴位置
        """
        self.x = x // 16
        self.z = z // 16
