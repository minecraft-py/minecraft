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

from minecraft.gui.background import BackGround
from minecraft.gui.font import NORMAL_SIZE
from minecraft.gui.widgets import Button
from minecraft.resource import REGION
from minecraft.scenes import Scene
from minecraft.utils import VERSION
from pyglet.gl import *
from pyglet.image import create
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.window import key

logger = getLogger(__name__)


class StartScene(Scene):

    def __init__(self):
        super().__init__()
        width, height = self.window.width, self.window.height
        self.background = BackGround(self.window)
        self.title_minec = Sprite(self.window.assets.loader.image(
            "textures/gui/title/minecraft.png", atlas=False).get_region(*REGION["title_minec"]))
        self.title_minec.image.anchor_x = 137
        self.title_minec.image.anchor_y = 22
        self.title_minec.image = self.title_minec.image
        self.title_minec.scale = 2
        self.title_minec.position = (width // 2, height // 1.25, 0)
        self.title_raft = Sprite(self.window.assets.loader.image(
            "textures/gui/title/minecraft.png", atlas=False).get_region(*REGION["title_raft"]))
        self.title_raft.image.anchor_x = -18
        self.title_raft.image.anchor_y = 22
        self.title_raft.image = self.title_raft.image
        self.title_raft.scale = 2
        self.title_raft.position = (width // 2 - 2, height // 1.25, 0)
        self.version_label = Label(f"Minecraft.py {VERSION['str']}",
                                   x=width, y=0, anchor_x="right", anchor_y="bottom",
                                   font_name="minecraft", font_size=NORMAL_SIZE)
        self.button = Button("Minecraft!", width // 2 -
                             100, height // 2 - 20, 200, 40)
        self.frame.add_widget(self.button)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        self.background.draw()
        self.title_minec.draw()
        self.title_raft.draw()
        self.version_label.draw()
        self.button.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            return True

    def on_resize(self, width, height):
        self.background.resize(width, height)
        self.title_minec.position = (width // 2, height // 1.25, 0)
        self.title_raft.position = (width // 2 - 2, height // 1.25, 0)
        self.version_label.position = width, 0, 0
        with self.frame.update():
            self.button.position = (width // 2 - 100, height // 2 - 20)


__all__ = ("StartScene")
