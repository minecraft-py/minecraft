import random

from minecraft.utils.utils import *

import pyglet
from pyglet.gl import *
import pyglet.graphics


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
        glFogf(GL_FOG_START, 30.0)


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
            if len(self._drops) < 512:
                px, py, pz = get_game().player['position']
                self.make_rain_drop((px + random.randint(-16, 16) + random.random(),
                    min(128, py + 20),
                    pz + random.randint(-16, 16) + random.random()))
        for drop in self._drops:
            if (get_game().world.get(normalize(drop['pos'])) is not None) or (drop['pos'][2] < 0):
                drop['shown'] = False
            else:
                drop['pos'] = drop['pos'][0], drop['pos'][1] - dt * 5, drop['pos'][2]
        self._drops = [drop for drop in self._drops if drop['shown']]

    def make_rain_drop(self, pos):
        drop = {
                    'pos': pos,
                    'color': (0, 0, random.randint(200, 255), 128),
                    'shown': True
                }
        self._drops.append(drop)

    def draw(self):
        for drop in self._drops:
            p1 = drop['pos'][0], drop['pos'][1] + 0.3, drop['pos'][2]
            p2 = drop['pos'][0], drop['pos'][1] - 0.3, drop['pos'][2]
            glLineWidth(3)
            pyglet.graphics.draw(2, GL_LINES,
                    ('v3f/static', p1 + p2),
                    ('c4B/static', drop['color'] * 2))
            glLineWidth(1)


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
