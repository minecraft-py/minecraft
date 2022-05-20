import pyglet
from minecraft.gui.frame import Frame
from minecraft.gui.widget.button import Button
from minecraft.gui.widget.label import ColorLabel
from minecraft.gui.widget.loading import LoadingBackground
from minecraft.scene import Scene
from minecraft.sources import resource_pack
from minecraft.utils.utils import *
from pyglet.sprite import Sprite
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
        # 该场景中的所有GUI
        self._frame = Frame(get_game())
        self._singleplayer_btn = Button(width // 2 - 200, 0.5 * height, 400, 40, resource_pack.get_translation("text.start_scent.single_player"))
        self._multiplayer_btn = Button(width // 2 - 200, 0.5 * height - 50, 400, 40, resource_pack.get_translation("text.start_scent.multi_player"))
        self._options_btn = Button(width // 2 - 200, 0.5 * height - 110, 195, 40, resource_pack.get_translation("text.start_scent.options"))
        self._exit_btn = Button(width // 2 + 5, 0.5 * height - 110, 195, 40, resource_pack.get_translation("text.start_scent.quit_game"))
        self._frame.add_widget(self._singleplayer_btn, self._multiplayer_btn, self._options_btn, self._exit_btn)

        @self._singleplayer_btn.event
        def on_press():
            log_info("You press a button")

        @self._exit_btn.event
        def on_press():
            pyglet.app.exit()

    def on_scene_enter(self):
        self._frame.enable()

    def on_scene_leave(self):
        self._frame.enable(False)

    def on_draw(self):
        self._back.draw()
        self._title.draw()
        self._title_edition.draw()
        self._version_label.draw()
        self._frame.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            return True

    def on_resize(self, width, height):
        self._back.resize(width, height)
        self._title.position = (width // 2, 0.8 * height)
        self._title_edition.position = (width // 2, 0.8 * height - self._title.image.height - self._title_edition.image.height - 3)
        self._version_label.x = width - 2
        self._singleplayer_btn.position = (width // 2 - 200, 0.5 * height)
        self._multiplayer_btn.position = (width // 2 - 200, 0.5 * height - 50)
        self._options_btn.position = (width // 2 - 200, 0.5 * height - 110)
        self._exit_btn.position = (width // 2 + 5, 0.5 * height - 110)
