from os.path import join
import pyglet
from pyglet.shapes import Rectangle

class Bag():
    # 按 E 键打开的背包

    def __init__(self, width, height):
        self._element = {}
        self._element['panel-up'] = Rectangle(x=(width - 600) // 2, y=(height - 400) // 2,
                width=598, height=398, color=(192, 192, 192))
        self._element['panel-down'] = Rectangle(x=(width - 600) // 2, y=(height - 400) // 2,
                width=600, height=400, color=(182, 182, 182))

    def draw(self):
        self._element['panel-down'].draw()
        self._element['panel-up'].draw()

    def resize(self, width, height):
        self._element['panel-up'].position = (width - 600) // 2, (height - 400) // 2
        self._element['panel-down'].position = (width - 600) // 2, (height - 400) // 2
