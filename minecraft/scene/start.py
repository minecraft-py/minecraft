from minecraft.gui.loading import LoadingBackground
from minecraft.scene import Scene
from minecraft.sources import resource_pack
from minecraft.utils.utils import *
from pyglet.shapes import Circle


class StartScene(Scene):

    def __init__(self, game):
        # 开始场景, 这是游戏启动后的第一个场景
        super().__init__(game)
        self._game = game
        self._back = LoadingBackground()

    def on_draw(self):
        self._back.draw()

    def on_resize(self, width, height):
        self._back.resize(width, height)
