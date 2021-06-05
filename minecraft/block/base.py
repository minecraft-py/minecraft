from ctypes import byref
from math import floor

from minecraft.block.texture import BlockTextureGroup
from minecraft.source import resource_pack
from minecraft.utils.nbt import NBT
from minecraft.utils.utils import *

from pyglet.gl import *


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
    # 大小
    width, height = 1.0, 1.0
    # 位置
    position = (0, 0, 0)
    # 名称
    name = ''
    # 方块信息
    _nbt = NBT()
    # 透明
    transparent = False
    # 硬度
    hardness = 1
    # 名称
    name = 'default'

    def __init__(self):
        self._nbt.set_value('name', self.name)
        self.update_texture()

    def get_texture_data(self):
        textures = self.top_texture + self.bottom_texture + self.front_texture + self.side_texture
        textures += self.side_texture * 2
        return list(textures)

    def get_vertices(self, x, y, z):
        return cube_vertices(x, y, z, 0.5) 

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

    def on_destroy(self, pos):
        # 摧毁方块是的回调函数
        pass

    def on_neighbor_change(self, neighbor_pos, self_pos):
        # 相邻方块发生变化时的回调函数
        pass

    def on_build(self, pos):
        # 放置方块时的回调函数
        pass

    def on_ticking(self, self_pos):
        # 接受到随机刻时的回调函数
        pass

    def on_player_land(self, self_pos):
        # 玩家着陆到方块时的回调函数
        # :return: 玩家的 dy
        return 0


class BlockColorizer():

    def __init__(self, name):
        self.color_data = resource_pack.get_resource('textures/colormap/%s' % name)
        if self.color_data is None:
            return
        self.color_data = self.color_data.get_data('RGB', self.color_data.width * 3)

    def get_color(self, temp, rainfall):
        temp = 1 - temp
        if temp + rainfall > 1:
            delta = (temp + rainfall - 1) / 2
            temp -= delta
            rainfall -= delta
        if self.color_data is None:
            return (1, 1, 1)
        pos = int(floor(rainfall * 255) * 768 + 3 * floor((temp) * 255))
        return (float(self.color_data[pos]) / 255,
                float(self.color_data[pos + 1]) / 255,
                float(self.color_data[pos + 2]) / 255)


_fbo = None

def get_block_icon(block, size):
    # 显示 3D 方块的缩略图
    global _fbo
    if hasattr(block, 'img'):
        if not isinstance(block, Block):
            pass
        else:
            return image.load(join(path['texture'], 'block', block.name + '.png'))
    block_icon = block.group.texture.get_region(
            int(block.texture_data[2 * 8] * 16) * size,
            int(block.texture_data[2 * 8 + 1]) * size,
            size, size)
    if _fbo == None:
        _fbo = GLuint(0)
        glGenFramebuffers(1, byref(_fbo))
    glBindFramebuffer(GL_FRAMEBUFFER, _fbo)
    icon_texture = pyglet.image.Texture.create(size, size, GL_RGBA)
    glBindTexture(GL_TEXTURE_2D, icon_texture.id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_FLOAT, None)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, icon_texture.id, 0)
    viewport = (GLint * 4)()
    glGetIntegerv(GL_VIEWPORT, viewport)
    glViewport(0, 0, size, size)
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(-1.5, 1.5, -1.5, 1.5, -10, 10)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor4f(1.0, 1.0, 1.0, 1.0)
    glRotatef(-45.0, 0.0, 1.0, 0.0)
    glRotatef(-30.0, -1.0, 0.0, 1.0)
    glScalef(1.5, 1.5, 1.5)
    vertex_data = block.get_vertices(0, 0, 0)
    texture_data = block.texture_data
    count = len(texture_data) // 2
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)
    batch = pyglet.graphics.Batch()
    if hasattr(block, 'get_item_color'):
        batch.add(count, GL_QUADS, block.group,
                ('v3f/static', vertex_data),
                ('t2f/static', texture_data),
                ('c3f/static', block.get_item_color()))
    else:
        batch.add(count, GL_QUADS, block.group,
                  ('v3f/static', vertex_data),
                  ('t2f/static', texture_data))
    batch.draw()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glViewport(*viewport)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDisable(GL_DEPTH_TEST)
    return icon_texture.get_image_data()
