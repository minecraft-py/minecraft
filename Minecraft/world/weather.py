import random

from Minecraft.utils.utils import *

import pyglet
from pyglet.gl import *
import pyglet.graphics


class RainDrop():

    def __init__(self, position):
        self._data = {}
        self._data['color'] = (0, 0, random.randint(128, 255), 128)
        self._data['position'] = (position[0], 128, position[1])
        self._data['shown'] = True
        self._data['dy'] = 0

    def __getitem__(self, item):
        return self._data.get(item, None)

    def __setitem__(self, item, value):
        if item in self._data:
            self._data[item] = value

    def draw(self):
        if self._data['shown']:
            p1 = self._data['position'][0], self._data['position'][1] + 0.1, self._data['position'][2]
            p2 = self._data['position'][0], self._data['position'][1] - 0.1, self._data['position'][2]
            glLineWidth(3)
            pyglet.graphics.draw(2, GL_LINES,
                    ('v3f/static', p1 + p2),
                    ('c4B/static', self._data['color'] * 2))
            glLineWidth(1)

    def update(self, dt):
        self._data['dy'] = dt * 3
        self._data['position'] = self._data['position'][0], self._data['position'][1] - self._data['dy'], self._data['position'][2]


class Weather():

    def __init__(self):
        pass

    def change(self):
        pass

    def leave(self):
        pass

    def update(self, dt):
        pass

    def draw(self):
        paas


class RainyDay(Weather):

    def __init__(self):
        super().__init__()
        self._drops = []

    def change(self):
        glFogf(GL_FOG_START, 20.0)

    def leave(self):
        self._drops = []

    def update(self, dt):
        for i in range(16):
            if len(self._drops) < 128:
                px, _, py = get_game().player['position']
                self._drops.append(RainDrop((px + random.randint(-5, 5) + random.random(),
                    py + random.randint(-5, 5) + random.random())))
        for drop in self._drops:
            if get_game().world.get(normalize(drop['position'])) is not None or drop['position'][2] < 0:
                drop['shown'] = False
            else:
                drop.update(dt)
        self._drops = [drop for drop in self._drops if drop['shown']]

    def draw(self):
        for drop in self._drops:
            drop.draw()


class SunnyDay(Weather):

    def __init__(self):
        super().__init__()

    def change(self):
        glFogf(GL_FOG_START, 50.0)


weather = {
        'rainy': RainyDay(),
        'sunny': SunnyDay(),
        'now': 'sunny'
    }
