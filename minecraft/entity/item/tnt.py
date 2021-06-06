import random

from minecraft.entity.base import Entity
from minecraft.source import resource_pack
from minecraft.utils.utils import *

from pyglet import graphics
from pyglet.gl import *


class ExplodingTNT(Entity):

    def __init__(self, position, fuse=4, nbt=None):
        super().__init__(position, health=20, max_health=20, nbt=nbt)
        self._show = True
        self._duration = 0
        self._data['name'] = 'exploding_tnt'
        self._data['fuse'] = fuse

    def explode(self):
        for pos_x in range(-1, 2):
            for pos_y in range(-1, 2):
                for pos_z in range(-1, 2):
                    block = get_game().world.get((round(self._data['position'][0] + pos_x),
                        round(self._data['position'][1] + pos_y),
                        round(self._data['position'][2] + pos_z)))
                    if block:
                        if block.hardness > 0:
                            if block.name == 'tnt':
                                get_game().world.get((round(self._data['position'][0] + pos_x),
                                    round(self._data['position'][1] + pos_y),
                                    round(self._data['position'][2] + pos_z))).on_use()
                            get_game().world.remove_block((round(self._data['position'][0] + pos_x),
                                round(self._data['position'][1] + pos_y),
                                round(self._data['position'][2] + pos_z)))
        for pos_x in range(-2, 3):
            for pos_y in range(-2, 3):
                for pos_z in range(-2, 3):
                    block = get_game().world.get((round(self._data['position'][0] + pos_x),
                        round(self._data['position'][1] + pos_y),
                        round(self._data['position'][2] + pos_z)))
                    if block:
                        if block.name == 'tnt':
                            get_game().world.get((round(self._data['position'][0] + pos_x),
                                round(self._data['position'][1] + pos_y),
                                round(self._data['position'][2] + pos_z))).on_use(random.randint(30, 40) / 10)
                        if (block.hardness > 0) and (random.randint(0, 9) >= 5):
                            get_game().world.remove_block((round(self._data['position'][0] + pos_x),
                                round(self._data['position'][1] + pos_y),
                                round(self._data['position'][2] + pos_z)))

    def on_update(self, dt):
        super().on_update(dt)
        self._duration += dt
        s = 2 * dt
        if self._duration >= 0.5:
            self._duration = 0
            self._show = not self._show
        if get_game().world.get((int(self._data['position'][0]), int(self._data['position'][1] - 0.1), int(self._data['position'][2]))) is None:
            self._data['position'] = (self._data['position'][0], self._data['position'][1] - s, self._data['position'][2])
        if self._data['alive'] >= self._data['fuse']:
            self.explode()
            get_game().entities.remove_entity(self.entity_id)

    def on_draw(self):
        vertex_data = cube_vertices(*self._data['position'], 0.5)
        if self._show:
            glColor3f(1.0, 1.0, 1.0)
        else:
            glColor3f(0.64, 0.16, 0.16)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDisable(GL_CULL_FACE)
        graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
        glEnable(GL_CULL_FACE)

