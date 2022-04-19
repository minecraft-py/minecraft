from minecraft.scene import Scene
from minecraft.utils.utils import *
from pyglet.shapes import Circle


class StartScene(Scene):

    def __init__(self, game):
        # 开始场景, 这是游戏启动后的第一个场景
        # 现在仅仅使用一个居中的圆作占位符
        super().__init__(game)
        self._game = game
        self.circle = Circle(game.width / 2, game.height / 2, 20)
    
    def on_draw(self):
        self._game.clear()
        self.circle.draw()
    
    def on_resize(self, width, height):
        self.circle.x = width / 2
        self.circle.y = height / 2
