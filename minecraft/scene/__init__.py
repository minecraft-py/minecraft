# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from minecraft.sources import *
from minecraft.utils.utils import *
from pyglet.event import EventDispatcher
from pyglet.window import Window

# Did GameWindow created?
_has_gamewin = False


class Scene(EventDispatcher):
    """A sene."""

    def __init__(self):
        super().__init__()

    def on_scene_enter(self):
        """Call this function when enter the scene."""
        pass

    def on_scene_leave(self):
        """Call this function when leave the scene."""
        pass


class GameWindow(Window):
    """The main window of game.

    `RuntimeError` will be raised when more than one `GameWindow` created.
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
        # Some variables, use minecraft.utils.utils.get_game() to get them.
        self.resource_pack = resource_pack
        self.settings = settings

    def add_scene(self, name: str, scene: Scene, *args, **kwargs):
        """Add a scene."""
        self._scenes[name] = scene(*args, **kwargs)

    def switch_scene(self, name: str):
        """Switch to another scene."""
        if name not in self._scenes:
            pass
        if self._now != "":
            self.pop_handlers()
            self._scenes[self._now].on_scene_leave()
        self._now = name
        self.push_handlers(self._scenes[self._now])
        self._scenes[self._now].on_scene_enter()
