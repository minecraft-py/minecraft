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

from logging import getLogger

from minecraft.gui.font import NORMAL_SIZE
from minecraft.scenes import Scene
from pyglet.gl import *
from pyglet.text import Label
from pyglet.window import key

logger = getLogger(__name__)


class StartScene(Scene):

    def __init__(self):
        super().__init__()
        width, height = self.window.width, self.window.height
        self.label = Label("Font test\n{\"str\":'minecraft:foo.bar'}",
                           x=width // 2, y=height // 2, width=width,
                           anchor_x="center", align="center", multiline=True,
                           font_name="minecraft", font_size=NORMAL_SIZE)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        self.label.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            return True

    def on_resize(self, width, height):
        self.label.position = width // 2, height // 2, 0
        self.label.width = width


__all__ = ("StartScene")
