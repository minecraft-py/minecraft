from minecraft.source import resource_pack
from minecraft.utils.utils import *

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
                self.block_texture[name] = resource_pack.get_resource('textures/misc/missing_texture')
            else:
                self.block_texture[name] = resource_pack.get_resource('textures/block/%s' % name)
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
