# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from importlib import import_module

import pyglet
from minecraft.gui.frame import Frame
from minecraft.gui.widget.button import Button, ImageButton
from minecraft.gui.widget.label import ColorLabel
from minecraft.gui.widget.loading import LoadingBackground
from minecraft.scene import Scene
from minecraft.sources import resource_pack
from minecraft.utils.utils import *
from pyglet.gl import *
from pyglet.sprite import Sprite
from pyglet.window import key


class StartScene(Scene):
    """这是第一个场景，供玩家选择游戏模式和更改游戏设置。"""

    def __init__(self):
        super().__init__()
        width, height = get_size()
        self._back = LoadingBackground()
        # 在窗口从上往下的20%处居中绘制Minecraft标题
        self._title = Sprite(get_game().resource_pack.get_resource(
            "textures/gui/title/minecraft"), x=width // 2, y=0.8 * height)
        self._title.image.anchor_x = self._title.image.width // 2
        self._title.image.anchor_y = self._title.image.height // 2
        self._title.scale = 2
        # 在Minecraft标题下面隔3个像素居中绘制副标题
        self._title_edition = Sprite(
            get_game().resource_pack.get_resource("textures/gui/title/edition"))
        self._title_edition.position = (
            width // 2, 0.8 * height - self._title.image.height - self._title_edition.image.height - 3)
        self._title_edition.image.anchor_x = self._title_edition.image.width // 2
        self._title_edition.image.anchor_y = self._title_edition.image.height // 2
        self._title_edition.scale = 2
        self._version_label = ColorLabel(
            "Minecraft in python %s" % VERSION["str"], x=width - 2, y=3, anchor_x="right", bold=True)
        # 场景中所有GUI
        self._frame = Frame()
        self._singleplayer_btn = Button(resource_pack.get_translation(
            "text.start_scent.single_player"), width // 2 - 200, 0.5 * height, 400, 40)
        self._multiplayer_btn = Button(resource_pack.get_translation("text.start_scent.multi_player"),
                                       width // 2 - 200, 0.5 * height - 50, 400, 40, False)
        self._options_btn = Button(resource_pack.get_translation("text.start_scent.options"),
                                   width // 2 - 200, 0.5 * height - 110, 195, 40)
        self._exit_btn = Button(resource_pack.get_translation("text.start_scent.quit_game"),
                                width // 2 + 5, 0.5 * height - 110, 195, 40)
        self._language_select_btn = ImageButton([
            get_game().resource_pack.get_resource(
                "textures/gui/widgets").get_region(0, 110, 20, 20),
            get_game().resource_pack.get_resource(
                "textures/gui/widgets").get_region(0, 130, 20, 20),
            get_game().resource_pack.get_resource(
                "textures/gui/widgets").get_region(20, 130, 20, 20)
        ], width // 2 + 205, 0.5 * height - 110, 40, 40)
        self._frame.add_widget(self._singleplayer_btn, self._multiplayer_btn, self._options_btn, self._exit_btn,
                               self._language_select_btn)

        @self._singleplayer_btn.event
        def on_press():
            single_player = import_module(
                "minecraft.scene.single_player").SinglePlayerScene
            get_game().add_scene("single_player", single_player)
            get_game().switch_scene("single_player")

        @self._exit_btn.event
        def on_press():
            pyglet.app.exit()

    def on_scene_enter(self):
        self._frame.enable()

    def on_scene_leave(self):
        self._frame.disable()

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
        self._title_edition.position = (
            width // 2, 0.8 * height - self._title.image.height - self._title_edition.image.height - 3)
        self._version_label.x = width - 3
        self._singleplayer_btn.position = (width // 2 - 200, 0.5 * height)
        self._multiplayer_btn.position = (width // 2 - 200, 0.5 * height - 50)
        self._options_btn.position = (width // 2 - 200, 0.5 * height - 110)
        self._language_select_btn.position = (
            width // 2 + 205, 0.5 * height - 110)
        self._exit_btn.position = (width // 2 + 5, 0.5 * height - 110)
