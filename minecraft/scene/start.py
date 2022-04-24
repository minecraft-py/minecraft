from minecraft.gui.loading import LoadingBackground
from minecraft.gui.widget.button import Button
from minecraft.scene import Scene
from minecraft.sources import resource_pack
from minecraft.utils.utils import *
from pyglet.shapes import Circle
from pyglet.sprite import Sprite
from minecraft.gui.widget.label import ColorLabel
from pyglet.window import key


class StartScene(Scene):

    def __init__(self):
        # 开始场景, 这是游戏启动后的第一个场景
        super().__init__()
        self.event_types = ()
        width, height = get_size()
        self._back = LoadingBackground()
        # 在窗口从上往下的20%处居中绘制Minecraft标题
        self._title = Sprite(get_game().resource_pack.get_resource("textures/gui/title/minecraft"),
                             x=width // 2, y=0.8 * height)
        self._title.image.anchor_x = self._title.image.width // 2
        self._title.image.anchor_y = self._title.image.height // 2
        self._title.scale = 2
        # 在Minecraft标题下面隔3个像素居中绘制副标题
        self._title_edition = Sprite(get_game().resource_pack.get_resource("textures/gui/title/edition"))
        self._title_edition.position = (width // 2, 0.8 * height - self._title.image.height - self._title_edition.image.height - 3)
        self._title_edition.image.anchor_x = self._title_edition.image.width // 2
        self._title_edition.image.anchor_y = self._title_edition.image.height // 2
        self._title_edition.scale = 2
        self._version_label = ColorLabel("Minecraft in python %s" % VERSION["str"], x=width - 2, y=3,
                                    anchor_x="right", bold=True)
        self._btn = Button(100, 100, 200, 20, "Hello")

    def on_draw(self):
        self._back.draw()
        self._title.draw()
        self._title_edition.draw()
        self._version_label.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            return True

    def on_resize(self, width, height):
        self._back.resize(width, height)
        self._title.position = (width // 2, 0.8 * height)
        self._title_edition.position = (width // 2, 0.8 * height - self._title.image.height - self._title_edition.image.height - 3)
        self._version_label.x = width - 2
