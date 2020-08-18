# 区块系统

from noise import snoise2 as noise2

class Zone(object):

    def __init__(self, x, z):
        self.base = 40 + round(noise2(x, y) * 50)
        self.x_start, self.z_start = 16 * x, 16 * z
        self.x_end, self.z_end = 16 * (x + 1), 16 * (z + 1)
        self.x_range, self.z_range = range(self.x_start, self.x_end + 1), range(self.x_start, z_end + 1)
        self.world = {}

    def __del__(self):
        for x in self.x_range:
            for y in range(0, 257):
                for z in self.z_range:
                    self.remove_block((x, y, z), record=False)

    def add_block(position, texture, immediate=True, record=True):
        self._add_block_function(position, texture, immediate, record)
        self.world[position] = texture

    def remove_block(position, immediate=True, record=True):
        self._remove_block_function(position, immediate, record)
        if position in self.world:
            del self.world[position]

    def generate(self):
        for x in self.x_range:
            for z in self.z_range:
                # 生成基岩
                self.add_block((x, 0, z), 'bedrock', record=False)
        for x in self.x_range:
            for y in range(1, 40):
                for z in self.z_range:
                    # 生成石头
                    self.add_block((x, y, z), 'stone', record=False)

    def set_add_function(self, function):
        self._add_block_function = function

    def set_remove_function(self, function):
        self._remove_block_function = function


class ZoneGroup(object):
    
    def __init__(self):
        pass
