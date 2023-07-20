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
from logging import getLogger
from os import path

from minecraft import assets
from minecraft.gui.frame import GUIFrame
from minecraft.utils import *
from pyglet.event import EventDispatcher
from pyglet.image import get_buffer_manager
from pyglet.window import Window, key

logger = getLogger(__name__)


class Scene(EventDispatcher):
    """A scene that is used to render different parts of the game."""

    def __init__(self):
        super().__init__()
        self.window: GameWindow = get_game_window_instance()
        self.frame = GUIFrame(self.window)

    def on_scene_enter(self):
        """The callback function on entering the scene."""
        self.frame.enable = True

    def on_scene_leave(self):
        """The callback function when leaving the scene."""
        self.frame.enable = False


class GameWindow(Window):
    """Game main window."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_caption("Minecraft")
        self.set_minimum_size(600, 450)
        self.set_icon(
            assets.loader.image("textures/icon/icon_16x16.png"),
            assets.loader.image("textures/icon/icon_32x32.png")
        )
        self.__scenes: dict[str, Scene] = {}
        self.__now = ""
        self.assets = assets

    @property
    def scene(self) -> str:
        return self.__now

    @scene.setter
    def scene(self, name: str):
        self.switch_scene(name)

    def add_scene(self, name: str, scene: Scene, *args, **kwargs):
        """Add a scene."""
        self.__scenes[name] = scene(*args, **kwargs)

    def switch_scene(self, name: str):
        """Switch to another scene."""
        assert is_namespace(name)
        if name not in self.__scenes:
            raise NameError("scene \"%s\" not found" % name)
        if self.__now != "":
            self.remove_handlers(self.__scenes[self.__now])
            self.__scenes[self.__now].on_scene_leave()
        self.__now = name
        self.push_handlers(self.__scenes[self.__now])
        if hasattr(self.__scenes[self.__now], "on_resize"):
            self.__scenes[self.__now].on_resize(self.width, self.height)
        self.__scenes[self.__now].on_scene_enter()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.F2:
            name = path.join(get_storage_path(), "screenshot",
                             time.strftime('%Y-%m-%d_%H.%M.%S.png'))
            get_buffer_manager().get_color_buffer().save(name)
            logger.info("Screenshot saved in: %s" % name)
        elif symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)


__all__ = ("Scene", "GameWindow")
