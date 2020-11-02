from Minecraft.utils.cube import *
from Minecraft.utils.utils import *

from pyglet.image import *
from pyglet.gl import *

group = TextureGroup(image.load(os.path.join(path['texture'], 'block.png')).get_texture())


class Block(object):

    def __init__(self, hard, texture):
        self.hard = hard
        self.destroyed = 0
        self.has_destroy = False
        self.texture = texture

    def destroy(self, i=0.01):
        if self.destroyed < 0:
            pass
        elif self.destroyed >= self.hard:
            self.has_destroy = True
        else:
            self.destroyed += i

    def show(self, position, batch):
        x, y, z = self.position
        vertex = make_cube(x, y, z, 0.5)
        texture = list(self.texture)
        return batch.add(len(texture) / 3, GL_QUADS, group,
                ('v3f/static', vertex),
                ('t2f/static', texture))


block = {}
block['grass'] = Block(50, tex_coords((1, 0), (0, 1), (0, 0)))
block['dirt'] = Block(50, tex_coords((0, 1), (0, 1), (0, 1)))
