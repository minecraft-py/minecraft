# 区块系统

import json
from noise import snoise2 as noise2
import Minecraft.saver as saver

class Zone(object):

    def __init__(self, x, z):
        self.base = 40 + round(noise2(x, z) * 50)
        self.x, self.z = x, z
        self.x_start, self.z_start = 16 * x, 16 * z
        self.x_end, self.z_end = 16 * (x + 1), 16 * (z + 1)
        self.x_range, self.z_range = range(self.x_start, self.x_end + 1), range(self.x_start, self.z_end + 1)
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

    def add_block(self, position, texture, immediate=True, record=True):
        # add_block 方法, 不要手动调用
        self._add_block_function(position, texture, immediate, record)
        self.world[position] = texture

    def remove_block(self, position, immediate=True, record=True):
        # remove_block 方法, 不要手动调用
        if self.world[position] != 'air':
            self.world[position] = 'air'
            self._remove_block_function(position, immediate, record)

    def generate(self):
        # 生成区块
        for x in self.x_range:
            for y in range(0, 11):
                for z in self.z_range:
                    if y == 0:
                        # 生成基岩
                       self.add_block((x, y, z), 'bedrock', record=False)
                    elif y < 6:
                        # 生成石头
                        self.add_block((x, y, z), 'stone', record=False)
                    elif 6 < y < 10:
                        # 生成泥土
                        self.add_block((x, y, z), 'dirt', record=False)
                    elif y == 10:
                        # 生成草
                        self.add_block((x, y, z), 'grass', record=False)
        self.load_block()

    def load_block(self):
        # Minecraft.saver.load_block 的重写, 读取一个区块的更改
        blocks = json.load(open('resource/save/demo/demo.world'))
        for x in self.x_range:
            for y in range(0, 257):
                for z in self.z_range:
                    if (position := ' '.join([str(i) for i in (x, y, z)])) in blocks:
                        block = blocks[position]
                        if block == 'air':
                            self.remove_block((x, y, z))
                        else:
                            self.add_block((x, y, z), block)

    def set_function(self, add, remove):
        self._add_block_function = add
        self._remove_block_function = remove


class ZoneGroup(object):
    
    def __init__(self, max_sight=5, add_block=lambda: False, remove_block=lambda: False):
        # max_sight 是玩家的最大视距
        self.max_sight = max_sight - 1
        # zones 是玩家可见的区块列表: {(x, z): zone}
        self.zones = {}
        # ticking_area 是常加载区块, 最多16个
        self.ticking_area = []
        # 添加, 删除方块的函数
        self.add = add_block
        self.remove = remove_block

    def set_ticking_area(self, x, z):
        """设置常加载区块

        @param x 区块 x 轴位置
        @param z 区块 z 轴位置
        """
        if len(self.ticking_area) <= 16:
            self.ticking_area.append((x, z))
            self.zones[(x, z)] = Zone(x, z)
            self.zones[(x, z)].set_function(self.add, seld.remove)
            self.zones[(x, z)].generate()

    def setxy(self, x, z):
        """
        设置玩家所在的区块

        @param x 玩家所在的 x 轴位置
        @param z 玩家所在的 z 轴位置
        """
        self.x = x // 16
        self.z = z // 16
        zone_x_start, zone_x_end = self.x - self.max_sight, self.x + self.max_sight
        zone_z_start, zone_z_end = self.z - self.max_sight, self.z + self.max_sight
        zone = {}
        for x in range(zone_x_start, zone_x_end + 1):
            for z in range(zone_z_start, zone_z_end + 1):
                if (x, z) in self.zones:
                    zone[(x, z)] = self.zones[(x, z)]
                elif (x, z) not in self.ticking_area:
                    zone[(x, z)] = Zone(x, z)
                    zone[(x, z)].set_function(self.add, self.remove)
                    zone[(x, z)].generate()
                else:
                    zone[(x, z)] = self.zones[(x, z)]
        else:
            for position in self.zones:
                del self.zones[position]
            else:
                self.zones = zone
