import random

from minecraft.entity.base import EntityBase
from minecraft.source import resource_pack
from minecraft.utils.utils import *

from pyglet import graphics
from pyglet.graphics import Batch, TextureGroup
from pyglet.image.atlas import TextureAtlas
from pyglet.gl import *


class ExplodingTNT(Entity):

    def __init__(self, position, fuse=4):
        super().__init__(position, health=20, max_health=20)
        self._show = True
        self._duration = 0
        self.fuse = fuse
        self.tnt_texture = TextureAtlas(16 * 3, 16 * 3)
        self.make_texture()
        self.tex_coord = tex_coords((0, 0), (0, 1), (0, 2), n=3)
        self.group = TextureGroup(self.tnt_texture.texture)
        self._batch = Batch()
        self._batch.add(24, GL_QUADS, self.group,
                ('v3f/static', cube_vertices(*position, 0.5)),
                ('t2f/static', list(self.tex_coord)))

    def explode(self):
        for pos_x in range(-1, 2):
            for pos_y in range(-1, 2):
                for pos_z in range(-1, 2):
                    block = get_game().world.get((round(self.position[0] + pos_x),
                        round(self.position[1] + pos_y),
                        round(self.position[2] + pos_z)))
                    if block:
                        if block.hardness > 0:
                            if block.name == 'tnt':
                                get_game().world.get((round(self.position[0] + pos_x),
                                    round(self.position[1] + pos_y),
                                    round(self.position[2] + pos_z))).on_use()
                            get_game().world.remove_block((round(self.position[0] + pos_x),
                                round(self.position[1] + pos_y),
                                round(self.position[2] + pos_z)))
        for pos_x in range(-2, 3):
            for pos_y in range(-2, 3):
                for pos_z in range(-2, 3):
                    block = get_game().world.get((round(self.position[0] + pos_x),
                        round(self.position[1] + pos_y),
                        round(self.position[2] + pos_z)))
                    if block:
                        if block.name == 'tnt':
                            get_game().world.get((round(self.position[0] + pos_x),
                                round(self.position[1] + pos_y),
                                round(self.position[2] + pos_z))).on_use(random.randint(5, 15) / 10)
                        if (block.hardness > 0) and (random.randint(0, 9) >= 8):
                            get_game().world.remove_block((round(self.position[0] + pos_x),
                                round(self.position[1] + pos_y),
                                round(self.position[2] + pos_z)))

    def on_update(self, dt):
        super().on_update(dt)
        self._duration += dt
        s = 2 * dt
        if self._duration >= 0.5:
            self._duration = 0
            self._show = not self._show
        if get_game().world.get((int(self.position[0]), int(self.position[1] - 0.1), int(self.position[2]))) is None:
            self.position = (self.position[0], self.position[1] - s, self.position[2])
            del self._batch
            self._batch = Batch()
            self._batch.add(24, GL_QUADS, self.group,
                ('v3f/static', cube_vertices(*self.position, 0.5)),
                ('t2f/static', list(self.tex_coord)))
        if self.alive >= self.fuse:
            self.explode()
            get_game().entities.remove_entity(self.entity_id)

    def on_draw(self):
        if self._show:
            vertex_data = cube_vertices(*self.position, 0.5)
            glColor3f(1.0, 1.0, 1.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glDisable(GL_CULL_FACE)
            graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glEnable(GL_CULL_FACE)
        else:
            self._batch.draw()

    def make_texture(self):
        self.tnt_texture.add(resource_pack.get_resource('textures/block/tnt_top'))
        self.tnt_texture.add(resource_pack.get_resource('textures/block/tnt_bottom'))
        self.tnt_texture.add(resource_pack.get_resource('textures/block/tnt_side'))
