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

from pyglet.window import key

from minecraft.gui.background import BackGround
from minecraft.gui.shapes import BorderedRectangle
from minecraft.gui.widgets import Label, ScrollableLayout, ScrollBar, TextButton
from minecraft.scenes import Scene

logger = getLogger(__name__)


class SingleplayerScene(Scene):
    def __init__(self):
        super().__init__()
        width, height = self.window.width, self.window.height
        self.background = BackGround(self.window)
        self.title = Label(
            self.window.assets.translate("selectWorld.title"),
            x=width // 2,
            y=height - 32,
            anchor_x="center",
            anchor_y="center",
        )
        self.rect = BorderedRectangle(
            -10,
            130,
            width + 20,
            height - 180,
            border=10,
            # The original class has been overwritten to support
            # different opacities.
            color=(0, 0, 0, 192),
            border_color=(0, 0, 0, 255),
        )
        self.button_select = TextButton(
            self.window.assets.translate("selectWorld.select"),
            width // 2 - 310,
            70,
            300,
            40,
            False,
        )
        self.button_create = TextButton(
            self.window.assets.translate("selectWorld.create"),
            width // 2 + 10,
            70,
            300,
            40,
        )
        self.button_edit = TextButton(
            self.window.assets.translate("selectWorld.edit"),
            width // 2 - 310,
            20,
            145,
            40,
            False,
        )
        self.button_delete = TextButton(
            self.window.assets.translate("selectWorld.delete"),
            width // 2 - 155,
            20,
            145,
            40,
            False,
        )
        self.button_recreate = TextButton(
            self.window.assets.translate("selectWorld.recreate"),
            width // 2 + 10,
            20,
            145,
            40,
            False,
        )
        self.button_back = TextButton(
            self.window.assets.translate("gui.back"),
            width // 2 + 165,
            20,
            145,
            40,
        )
        self.chooser_layout = ScrollableLayout(
            width // 2 - 310,
            130,
            608,
            height - 180,
            content_height=480,
        )
        self.scrollbar = ScrollBar(
            width // 2 + 298, 130, height - 180, scrollable_layout=self.chooser_layout
        )

        self.button_back.push_handlers(
            on_release=lambda: self.window.switch_scene("minecraft:start")
        )
        self.frame.add_widget(
            self.button_select,
            self.button_create,
            self.button_edit,
            self.button_delete,
            self.button_recreate,
            self.button_back,
            self.chooser_layout,
            self.scrollbar,
        )

    def on_draw(self):
        self.window.clear()
        self.background.draw()
        self.title.draw()
        self.rect.draw()
        self.button_select.draw()
        self.button_create.draw()
        self.button_edit.draw()
        self.button_delete.draw()
        self.button_recreate.draw()
        self.button_back.draw()
        self.chooser_layout.draw()
        self.scrollbar.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            return True

    def on_resize(self, width, height):
        self.background.resize(width, height)
        self.title.position = (width // 2, height - 32, 0)
        self.rect.width = width + 20
        self.rect.height = height - 180
        with self.frame.update():
            self.button_select.position = (width // 2 - 310, 70)
            self.button_create.position = (width // 2 + 10, 70)
            self.button_edit.position = (width // 2 - 310, 20)
            self.button_delete.position = (width // 2 - 155, 20)
            self.button_recreate.position = (width // 2 + 10, 20)
            self.button_back.position = (width // 2 + 165, 20)
            self.chooser_layout.position = (width // 2 - 310, 130)
            self.chooser_layout.height = height - 180
            self.scrollbar.position = (width // 2 + 298, 130)
            self.scrollbar.height = height - 180

    def on_scene_leave(self):
        self.chooser_layout.offset_y = 0


__all__ = "SingleplayerScene"
