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

from importlib import import_module
from logging import getLogger

from minecraft.gui.background import BackGround
from minecraft.gui.widgets import ImageButton, Label, TextButton
from minecraft.resource import REGION
from minecraft.scenes import Scene
from minecraft.utils import VERSION
from pyglet import app
from pyglet.sprite import Sprite
from pyglet.window import key

logger = getLogger(__name__)


class StartScene(Scene):
    def __init__(self):
        super().__init__()
        width, height = self.window.width, self.window.height
        self._widgets_texture = self.window.assets.loader.image(
            "textures/gui/widgets.png"
        )
        self.background = BackGround(self.window)
        self.title_minec = Sprite(
            self.window.assets.loader.image(
                "textures/gui/title/minecraft.png"
            ).get_region(*REGION["title_minec"])
        )
        self.title_minec.image.anchor_x = 137
        self.title_minec.image.anchor_y = 22
        self.title_minec.image = self.title_minec.image
        self.title_minec.scale = 2
        self.title_minec.position = (width // 2, height // 1.25, 0)
        self.title_raft = Sprite(
            self.window.assets.loader.image(
                "textures/gui/title/minecraft.png"
            ).get_region(*REGION["title_raft"])
        )
        self.title_raft.image.anchor_x = -18
        self.title_raft.image.anchor_y = 22
        self.title_raft.image = self.title_raft.image
        self.title_raft.scale = 2
        self.title_raft.position = (width // 2 - 2, height // 1.25, 0)
        self.label_version = Label(
            f"Minecraftpy {VERSION['str']}",
            x=width,
            y=0,
            anchor_x="right",
            anchor_y="bottom",
        )
        self.button_singleplayer = TextButton(
            self.window.assets.translate("menu.singleplayer"),
            width // 2 - 200,
            height // 2,
            400,
            40,
        )
        self.button_multiplayer = TextButton(
            self.window.assets.translate("menu.multiplayer"),
            width // 2 - 200,
            height // 2 - 50,
            400,
            40,
            False,
        )
        self.button_options = TextButton(
            self.window.assets.translate("menu.options"),
            width // 2 - 200,
            height // 2 - 120,
            195,
            40,
        )
        self.button_quit = TextButton(
            self.window.assets.translate("menu.quit"),
            width // 2 + 5,
            height // 2 - 120,
            195,
            40,
        )
        self.button_accessibility = ImageButton(
            self._widgets_texture.get_region(*REGION["accessibility_normal"]),
            self._widgets_texture.get_region(*REGION["accessibility_hover"]),
            width // 2 + 205,
            height // 2 - 120,
            40,
            40,
        )
        self.button_language = ImageButton(
            self._widgets_texture.get_region(*REGION["language_normal"]),
            self._widgets_texture.get_region(*REGION["language_hover"]),
            width // 2 - 245,
            height // 2 - 120,
            40,
            40,
        )

        self.button_singleplayer.push_handlers(on_release=self.on_singleplayer_click)
        self.button_quit.push_handlers(on_release=lambda: app.exit())
        self.frame.add_widget(
            self.button_singleplayer,
            self.button_multiplayer,
            self.button_options,
            self.button_quit,
            self.button_accessibility,
            self.button_language,
        )

    def on_singleplayer_click(self):
        if not self.window.has_scene("minecraft:singleplayer"):
            singleplayer = import_module(
                "minecraft.scenes.singleplayer"
            ).SingleplayerScene
            self.window.add_scene("minecraft:singleplayer", singleplayer)
        self.window.switch_scene("minecraft:singleplayer")

    def on_draw(self):
        self.window.clear()
        self.background.draw()
        self.title_minec.draw()
        self.title_raft.draw()
        self.label_version.draw()
        self.button_singleplayer.draw()
        self.button_multiplayer.draw()
        self.button_options.draw()
        self.button_quit.draw()
        self.button_accessibility.draw()
        self.button_language.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            return True

    def on_resize(self, width, height):
        self.background.resize(width, height)
        self.title_minec.position = (width // 2, height // 1.25, 0)
        self.title_raft.position = (width // 2 - 2, height // 1.25, 0)
        self.label_version.position = (width, 0, 0)
        with self.frame.update():
            self.button_singleplayer.position = (width // 2 - 200, height // 2)
            self.button_multiplayer.position = (width // 2 - 200, height // 2 - 50)
            self.button_options.position = (width // 2 - 200, height // 2 - 120)
            self.button_quit.position = (width // 2 + 5, height // 2 - 120)
            self.button_accessibility.position = (width // 2 + 205, height // 2 - 120)
            self.button_language.position = (width // 2 - 245, height // 2 - 120)


__all__ = "StartScene"
