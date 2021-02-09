import random

from Minecraft.utils.utils import *

import pyglet
from pyglet.gl import *
import pyglet.graphics


class RainDrop():

    def __init__(self, position):
        self._data = {}
        self._data['color'] = (0, 0, random.randint(128, 255), 128)
        self._data['position'] = (position[0], min(128, get_game().player['position'][1] + 20), position[1])
        self._data['shown'] = True
        self._data['dy'] = 0

    def __getitem__(self, item):
        return self._data.get(item, None)

    def __setitem__(self, item, value):
        if item in self._data:
            self._data[item] = value

    def draw(self):
        if self._data['shown']:
            p1 = self._data['position'][0], self._data['position'][1] + 0.3, self._data['position'][2]
            p2 = self._data['position'][0], self._data['position'][1] - 0.3, self._data['position'][2]
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
        # 持续时间(最短, 最长)
        self.duration = (0, 0)
        # 天气被选中的权重
        self.weight = 0

    def change(self):
        pass

    def leave(self):
        pass

    def update(self, dt):
        pass

    def draw(self):
        pass


class Clear(Weather):

    def __init__(self):
        super().__init__()
        self.duration = (600, 1200)
        self.weight = 70

    def change(self):
        glFogf(GL_FOG_START, 50.0)


class Rain(Weather):

    def __init__(self):
        super().__init__()
        self.duration = (300, 1200)
        self.weight = 30
        self._drops = []

    def change(self):
        glFogf(GL_FOG_START, 20.0)

    def leave(self):
        self._drops = []

    def update(self, dt):
        for i in range(8):
            if len(self._drops) < 256:
                px, _, py = get_game().player['position']
                self._drops.append(RainDrop((px + random.randint(-10, 10) + random.random(),
                    py + random.randint(-10, 10) + random.random())))
        for drop in self._drops:
            if get_game().world.get(normalize(drop['position'])) is not None or drop['position'][2] < 0:
                drop['shown'] = False
            else:
                drop.update(dt)
        self._drops = [drop for drop in self._drops if drop['shown']]

    def draw(self):
        for drop in self._drops:
            drop.draw()


weather = {
        'clear': Clear(),
        'rain': Rain()
    }

def choice_weather():
    global weather
    weathers, weight = [], []
    for k, v in weather.items():
        weathers.append(k)
        weight.append(v.weight)
    else:
        return random.choices(weathers, weight)[0]
