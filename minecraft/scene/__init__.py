# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from minecraft.sources import *
from minecraft.utils.utils import *
from pyglet.event import EventDispatcher
from pyglet.window import Window

# GameWindow的实例是否创建了呢？
_has_gamewin = False


class Scene(EventDispatcher):
    """一个场景。"""

    def __init__(self):
        super().__init__()

    def on_scene_enter(self):
        """进入场景时调用。"""
        pass

    def on_scene_leave(self):
        """离开场景时调用。"""
        pass


class GameWindow(Window):
    """游戏的主窗口。

    只能有一个主场口，否则会报错。
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
        # 一些变量, 可通过minecraft.utils.utils.get_game()获取
        self.resource_pack = resource_pack
        self.settings = settings

    def add_scene(self, name, scene, *args, **kwargs):
        """添加场景。

        :param name: 场景的名字
        :param scene: 场景类
        """
        assert isinstance(scene, Scene)
        self._scenes[name] = scene(*args, **kwargs)

    def switch_scene(self, name):
        """切换至一个场景。

        在切换时会调用前一个场景的`on_scene_leave()`方法，并调用当前场景的`on_scene_enter()`方法。

        :param name: 场景的名字
        """
        if name not in self._scenes:
            pass
        if self._now != "":
            self.pop_handlers()
            self._scenes[self._now].on_scene_leave()
        self._now = name
        self.push_handlers(self._scenes[self._now])
        self._scenes[self._now].on_scene_enter()
