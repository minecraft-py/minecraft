# Copyright 2020-2023 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from importlib import import_module
from minecraft.gui.frame import Frame
from minecraft.gui.widget.button import Button
from minecraft.gui.widget.label import ColorLabel
from minecraft.gui.widget.loading import LoadingBackground
from minecraft.scene import Scene
from minecraft.save import new
from minecraft import resource_pack
from minecraft.utils.utils import *
from pyglet.window import key


class SinglePlayerScene(Scene):
    """单人游戏选择存档的场景。"""

    def __init__(self):
        super().__init__()
        width, height = get_size()
        self._back = LoadingBackground()
        self._frame = Frame()
        self._save_picker = []
        self._title = ColorLabel(resource_pack.get_translation("text.single_player_scene.choose_a_save"),
                                 font_size=15, x=width // 2, y=0.95 * height, anchor_x="center", anchor_y="center")
        self._new_save_btn = Button(resource_pack.get_translation(
            "text.single_player_scene.new_save"), width // 2 - 305, height - 80, 197, 40, False)
        self._settings_btn = Button(resource_pack.get_translation(
            "lang.common.settings"), width // 2 - 99, height - 80, 197, 40, False)
        self._delete_btn = Button(resource_pack.get_translation(
            "lang.common.delete"), width // 2 + 109, height - 80, 197, 40, False)
        self._play_btn = Button(resource_pack.get_translation(
            "text.single_player_scene.play"), width // 2 - 305, height - 30, 300, 40, False)
        self._back_btn = Button(resource_pack.get_translation(
            "lang.common.go_back"), width // 2 + 5, height - 30, 300, 40)
        for i in range(5):
            self._save_picker.append(Button(
                "- save %d -" % (i + 1), width // 2 - 250, 0.2 * height + 50 * i, 500, 40, onclick=(self.on_picker_click, i + 1)))
        self._frame.add_widget(
            self._new_save_btn, self._settings_btn, self._delete_btn, self._play_btn, self._back_btn, *self._save_picker)

        @self._back_btn.event
        def on_press():
            get_game().switch_scene("minecraft:start")

        @self._new_save_btn.event
        def on_press():
            new_save = import_module(
                "minecraft.scene.new_save").NewSaveScene
            get_game().add_scene("minecraft:new_save", new_save)
            get_game().switch_scene("minecraft:new_save")

    def on_scene_enter(self):
        self._frame.enable()

    def on_scene_leave(self):
        self._frame.disable()

    def on_draw(self):
        self._back.draw()
        self._title.draw()
        self._frame.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            return True

    def on_picker_click(self, i):
        new(str(i))

    def on_resize(self, width, height):
        self._back.resize(width, height)
        self._title.x = width // 2
        self._title.y = 0.95 * height
        self._new_save_btn.position = (width // 2 - 305, height - 80)
        self._settings_btn.position = (width // 2 - 99, height - 80)
        self._delete_btn.position = (width // 2 + 109, height - 80)
        self._play_btn.position = (width // 2 - 305, height - 30)
        self._back_btn.position = (width // 2 + 5, height - 30)
        for i in range(5):
            self._save_picker[i].position = width // 2 - \
                250, 0.2 * height + 50 * i
