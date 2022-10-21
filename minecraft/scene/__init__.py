# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from minecraft.sources import *
from minecraft.utils.utils import *
from pyglet.event import EventDispatcher
from pyglet.window import Window

# GameWindow的实例创建过了吗？
_has_gamewin = False


class Scene(EventDispatcher):
    """一个场景。"""

    def __init__(self):
        super().__init__()

    def on_scene_enter(self):
        """在进入场景时的回调函数。"""
        pass

    def on_scene_leave(self):
        """在离开场景时的回调函数。"""
        pass


class GameWindow(Window):
    """游戏的主场口。

    只能创建一个GameWindow实例！
    """

    def __init__(self, *args, **kwargs):
        global _has_gamewin
        if _has_gamewin:
            raise RuntimeError("GameWindow has existed")
        _has_gamewin = True
        super().__init__(*args, **kwargs)
        self.set_caption("Minecraft in python %s" % VERSION["str"])
        self.set_minimum_size(640, 480)
        self._scenes = {}
        self._now = ""
        # 一些变量，可通过minecraft.utils.utils.get_game()获得
        self.resource_pack = resource_pack
        self.settings = settings

    def add_scene(self, name: str, scene: Scene, *args, **kwargs):
        """添加一个场景。"""
        self._scenes[name] = scene(*args, **kwargs)

    def switch_scene(self, name: str):
        """切换到另一个场景。"""
        if name not in self._scenes:
            pass
        if self._now != "":
            self.pop_handlers()
            self._scenes[self._now].on_scene_leave()
        self._now = name
        self.push_handlers(self._scenes[self._now])
        self._scenes[self._now].on_scene_enter()
