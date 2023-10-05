# minecraftpy, a sandbox game
# Copyright (C) 2020-2023 minecraftpy team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
from contextlib import contextmanager
from logging import getLogger

from pyglet.event import EventDispatcher
from pyglet.image import get_buffer_manager
from pyglet.window import Window, key

from minecraft import assets
from minecraft.gui.frame import GUIFrame
from minecraft.utils import *
from minecraft.utils.namespace import is_namespace

logger = getLogger(__name__)


class Scene(EventDispatcher):
    """A scene that is used to render different parts of the game."""

    def __init__(self):
        super().__init__()
        self.window: GameWindow = get_game_window_instance()
        self.frame = GUIFrame(self.window)

    def on_language_change(self):
        """The callback function on changing the language."""
        pass

    def on_scene_enter(self):
        """The callback function on entering the scene."""
        pass

    def on_scene_leave(self):
        """The callback function when leaving the scene."""
        pass


class GameWindow(Window):
    """Game main window."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_caption("Minecraft")
        self.set_minimum_size(640, 480)
        self.set_icon(
            assets.loader.image("textures/icon/icon_16x16.png"),
            assets.loader.image("textures/icon/icon_32x32.png"),
        )
        self.minecraft_gamewindow = 0x1BF52
        self._scenes: dict[str, Scene] = {}
        self._now = ""
        self.assets = assets

    @property
    def scene(self) -> str:
        return self._now

    @scene.setter
    def scene(self, name: str):
        self.switch_scene(name)

    def add_scene(self, name: str, scene: Scene, *args, **kwargs):
        """Add a scene."""
        self._scenes[name] = scene(*args, **kwargs)

    def has_scene(self, name: str) -> bool:
        """Whether a scene is added."""
        return name in self._scenes

    def remove_scene(self, name: str):
        """
        Remove a scene.

        You cannot remove the active one!
        """
        if self._now == name:
            return
        del self._scenes[name]

    def switch_scene(self, name: str):
        """Switch to another scene."""
        assert is_namespace(name)
        if name not in self._scenes:
            raise NameError('scene "%s" not found' % name)
        if self._now != "":
            self._scenes[self._now].frame.on_mouse_motion(0, 0, 0, 0)
            self._scenes[self._now].frame.enable = False
            self._scenes[self._now].on_scene_leave()
            self.remove_handlers(self._scenes[self._now])
        self._now = name
        self.push_handlers(self._scenes[self._now])
        self._scenes[self._now].frame.enable = True
        if hasattr(self._scenes[self._now], "on_resize"):
            self._scenes[self._now].on_resize(self.width, self.height)
        self._scenes[self._now].on_scene_enter()

    def change_language(self):
        for scene in self._scenes.values():
            scene.on_language_change()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.F2:
            filename = (
                get_storage_path()
                / "screenshot"
                / time.strftime("%Y-%m-%d_%H.%M.%S.png")
            )
            get_buffer_manager().get_color_buffer().save(filename)
            logger.info("Screenshot saved in: %s" % filename)
        elif symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)


__all__ = ("Scene", "GameWindow")
