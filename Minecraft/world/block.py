from math import floor
from os.path import isfile, join

from Minecraft.source import path
from Minecraft.utils.utils import *

from pyglet import image
from pyglet.image.atlas import TextureAtlas
from pyglet.graphics import Group
from pyglet.gl import *


def get_texture_coord(x, y, size=16):
    if x == -1 and y == -1:
        return ()
    m = 1.0 / size
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


class BlockTextureGroup(Group):

    def __init__(self, names, width=1.0, height=1.0, bgcolor=None):
        super(BlockTextureGroup, self).__init__()
        self.atlas = None
        self.texture_data = []
        self.block_texture = {}
        for name in names:
            if name == 'missing':
                self.block_texture[name] = image.load(join(path['texture'], 'misc', 'missing_texture.png'))
            else:
                self.block_texture[name] = image.load(join(path['texture'], 'block', name + '.png'))
            size = self.block_texture[name].width
            if bgcolor is not None:
                data = bytearray(self.block_texture[name].get_image_data().get_data('RGBA', size * 4))
                for i in range(len(data)):
                    if data[i] == bgcolor:
                        data[i] = 0
                else:
                    self.block_texture[name].get_image_data().set_data('RGBA', size * 4, bytes(data))
            if self.atlas == None:
                self.atlas = TextureAtlas(size * len(names), size)
                self.texture = self.atlas.texture
            subtex = self.atlas.add(self.block_texture[name])
            i = 0
            for value in subtex.tex_coords:
                i += 1
                if i % 3 != 0:
                    self.texture_data.append(value)
        if self.atlas == None:
            self.atlas = TextureAtlas(1, 1)
        self.texture = self.atlas.texture
        self.texture_data += self.texture_data[-8:] * (6 - len(names))
        # 调整贴图大小
        if height != 1.0 or width != 1.0:
            if len(self.texture_data) == 0:
                return
            else:
                tex_width = tex_height = self.texture_data[2] - self.texture_data[0]
                w_margin = tex_height * (1.0 - width) / 2
                h_margin = tex_height * (1.0 - height)
                # 顶部和底部
                for i in (0, 1):
                    for j in (0, 1, 3, 6):
                        self.texture_data[i * 8 + j] += w_margin
                    for j in (2, 4, 5, 7):
                        self.texture_data[i * 8 + j] -= w_margin
                # 四边
                for i in range(2, 6):
                    for j in (0, 6):
                        self.texture_data[i * 8 + j] += w_margin
                    for j in (2, 4):
                        self.texture_data[i * 8 + j] -= w_margin
                    for j in (5, 7):
                        self.texture_data[i * 8 + j] -= h_margin
    
    def set_state(self):
        if self.texture:
            glBindTexture(self.texture.target, self.texture.id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glEnable(self.texture.target)

    def unset_state(self):
        if self.texture:
            glDisable(self.texture.target)


class Block():

    textures = ()
    # 顶部贴图
    top_texture = ()
    # 底部贴图
    bottom_texture = ()
    # 前方贴图
    front_texture = None
    # 四边贴图
    side_texture = ()
    # 硬度
    hardness = 1

    def __init__(self, name, width=1.0, height=1.0, mode=''):
        self.name = name
        self.width = width
        self.height = height
        self.mode = mode
        self.update_texture()

    def get_texture_data(self):
        textures = self.top_texture + self.bottom_texture + self.front_texture + self.side_texture
        if self.mode != 'x':
            textures += self.side_texture * 2
        return list(textures)

    def get_vertices(self, x, y, z):
        w = self.width / 2.0
        h = self.height / 2.0
        y -= (1.0 - self.height) / 2
        xm = x - w
        xp = x + w
        ym = y - h
        yp = y + h
        zm = z - w
        zp = z + w
        vertices = ()
        if len(self.top_texture) > 0 or len(self.side_texture) == 0:
            vertices += (
                xm, yp, zm,   xm, yp, zp,   xp, yp, zp,   xp, yp, zm    # 顶部
            )
        if len(self.bottom_texture) > 0 or len(self.side_texture) == 0:
            vertices += (
                xm, ym, zm,   xp, ym, zm,   xp, ym, zp,   xm, ym, zp    # 底部
            )
        if self.mode == 'x':
            vertices += (
                xm, ym, zm,   xp, ym, zp,   xp, yp, zp,   xm, yp, zm,
                xm, ym, zp,   xp, ym, zm,   xp, yp, zm,   xm, yp, zp,
            )
        elif self.mode == 'g':
            xm2 = x - w / 2.0
            xp2 = x + w / 2.0
            zm2 = z - w / 2.0
            zp2 = z + w / 2.0
            vertices += (
                xm2, ym, zm,   xm2, ym, zp,   xm2, yp, zp,   xm2, yp, zm,   # 左边
                xp2, ym, zp,   xp2, ym, zm,   xp2, yp, zm,   xp2, yp, zp,   # 右边
                xm, ym, zp2,   xp, ym, zp2,   xp, yp, zp2,   xm, yp, zp2,   # 前面
                xp, ym, zm2,   xm, ym, zm2,   xm, yp, zm2,   xp, yp, zm2,   # 后面
            )
        else:
            vertices += (
                xm, ym, zm,   xm, ym, zp,   xm, yp, zp,   xm, yp, zm,   # 左边
                xp, ym, zp,   xp, ym, zm,   xp, yp, zm,   xp, yp, zp,   # 右边
                xm, ym, zp,   xp, ym, zp,   xp, yp, zp,   xm, yp, zp,   # 前面
                xp, ym, zm,   xm, ym, zm,   xm, yp, zm,   xp, yp, zm,   # 后面
            )
        return vertices

    def update_texture(self):
        if self.textures:
            self.group = BlockTextureGroup(self.textures)
        if self.group:
            self.texture_data = self.group.texture_data
        if self.top_texture == ():
            return
        if self.front_texture is None:
            self.front_texture = self.side_texture
        if not self.texture_data:
            for k in ('top_texture', 'bottom_texture', 'side_texture', 'front_texture'):
                v = getattr(self, k)
                if v:
                    setattr(self, k, get_texture_coord(*v))
            else:
                self.texture_data = self.get_texture_data()


class BlockColorizer:
    def __init__(self, name):
        self.color_data = image.load(join(path['texture'], 'colormap', name + '.png'))
        if self.color_data is None:
            return
        self.color_data = self.color_data.get_data('RGB', self.color_data.width * 3)

    def get_color(self, temperature, humidity):
        temperature = 1 - temperature
        if temperature + humidity > 1:
            delta = (temperature + humidity - 1) / 2
            temperature -= delta
            humidity -= delta
        if self.color_data is None:
            return 1, 1, 1
        pos = int(floor(humidity * 255) * 768 + 3 * floor((temperature) * 255))
        return (float(self.color_data[pos]) / 255,
                float(self.color_data[pos + 1]) / 255,
                float(self.color_data[pos + 2]) / 255)


class Bedrock(Block):
    textures = 'bedrock',
    hardness = -1


class Brick(Block):
    textures = 'brick',


class CraftTable(Block):
    textures = 'crafting_table_top', 'planks_oak', 'crafting_table_front', 'crafting_table_side'

    def on_use(self, world):
        pass


class Dirt(Block):
    textures = 'dirt',


class Grass(Block):
    textures = 'grass_top',
    colorizer = BlockColorizer('grass')

    def get_color(self, temperature, humidity):
        color = []
        color.extend(list(self.colorizer.get_color(temperature, humidity)) * 24)
        return color


class Leaf(Block):
    textures = 'leaves_oak',
    colorizer = BlockColorizer('foliage')

    def get_color(self, temperature, humidity):
        color = []
        color.extend(list(self.colorizer.get_color(temperature, humidity)) * 24)
        return color


class Log(Block):
    textures = 'log_oak_top', 'log_oak'


class Missing(Block):
    textures = 'missing',
    hardness = -1


class Plank(Block):
    textures = 'planks_oak',


class Sand(Block):
    textures = 'sand',


blocks = {}
blocks['bedrock'] = Bedrock('bedrock')
blocks['brick'] = Brick('brick')
blocks['craft_table'] = CraftTable('craft_table')
blocks['dirt'] = Dirt('dirt')
blocks['grass'] = Grass('grass')
blocks['leaf'] = Leaf('leaf')
blocks['log'] = Log('log')
blocks['missing'] = Missing('missing')
blocks['plank'] = Plank('plank')
blocks['sand'] = Sand('sand')
