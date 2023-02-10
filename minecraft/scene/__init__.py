# Minecraft-in-python, a sandbox game
# Copyright (C) 2020-2023  Minecraft-in-python team
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

from minecraft import *
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
        self.__scenes = {}
        self.__now = ""
        # 一些变量，可通过`minecraft.utils.utils.get_game()`获得
        self.mouse_position = (0, 0)
        self.resource_pack = resource_pack
        self.settings = settings

    def add_scene(self, name: str, scene: Scene, *args, **kwargs):
        """添加一个场景。"""
        assert is_namespace(name)
        self.__scenes[name] = scene(*args, **kwargs)

    def switch_scene(self, name: str):
        """切换到另一个场景。"""
        if name not in self.__scenes:
            raise NameError("scene '%s' not found" % name)
        if self.__now != "":
            self.remove_handlers(self.__scenes[self.__now])
            self.__scenes[self.__now].on_scene_leave()
        self.__now = name
        self.push_handlers(self.__scenes[self.__now])
        self.__scenes[self.__now].on_resize(*get_size())
        self.__scenes[self.__now].on_scene_enter()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_position = (x, y)
