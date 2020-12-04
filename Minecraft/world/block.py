from os.path import join

from Minecraft.source import path
from Minecraft.utils.cube import *
from Minecraft.utils.utils import *

from pyglet import image
from pyglet.image.atlas import TextureAtlas
from pyglet.graphics import Group
from pyglet.gl import *

block_texture = {}


class BlockTextureGroup(Group):

    def __init__(self, names, width=1.0, height=1.0):
        super(BlockTextureGroup, self).__init__()
        i = 0
        self.atlas = None
        self.texture_data = []
        self.block_texture = {}
        for name in names:
            if name not in block_texture:
                self.block_texture[name] = block_texture[name] = image.load(join(path['texture'], 'block', name + '.png'))
            else:
                self.block_texture[name] = block_texture[name]
            size = self.block_texture[name].width 
            if self.atlas == None:
                self.atlas = TextureAtlas(size * len(names), size)
                self.texture = self.atlas.texture
            subtex = self.atlas.add(self.block_texture[name])
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

    def __init__(self, top=(), side=(), bottom=(), mode='', width=1.0, height=1.0):
        self.top_texture = top
        self.side_texture = side
        self.bottom_texture = bottom
        self.mode = mode
        self.width = width
        self.height = height
        self.set_texture_data()

    def get_texture_data(self):
        return self.texture_group.texture_data

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
        if self.mode == 'c':
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

    def set_texture_data(self):
        self.textures = ()
        self.textures += self.top_texture + self.bottom_texture + self.side_texture
        if self.mode != 'c':
            self.textures += self.side_texture * 2
        self.texture_group = BlockTextureGroup(self.textures)
