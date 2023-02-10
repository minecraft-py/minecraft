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

from minecraft.gui.frame import Frame
from minecraft.gui.widget.button import Button
from minecraft.gui.widget.label import ColorLabel
from minecraft.gui.widget.loading import LoadingBackground
from minecraft.scene import Scene
from minecraft import resource_pack
from minecraft.utils.utils import *
from pyglet.window import key


class NewSaveScene(Scene):
    """新建存档的场景。"""

    def __init__(self):
        super().__init__()
        width, height = get_size()
        self._back = LoadingBackground()
        self._frame = Frame()

    def on_scene_enter(self):
        self._frame.enable()

    def on_scene_leave(self):
        self._frame.disable()

    def on_draw(self):
        self._back.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            get_game().switch_scene("minecraft:single_player")
            return True

    def on_resize(self, width, height):
        self._back.resize(width, height)
