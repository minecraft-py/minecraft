# minecraftpy, a sandbox game
# Copyright (C) 2020-2023  minecraftpy team
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

from typing import Dict

from minecraft.resource import REGION
from minecraft import assets
from minecraft.utils import *
from pyglet.gui import WidgetBase
from pyglet.image import TextureRegion
from pyglet.sprite import Sprite
from pyglet.text import Label

GUI_TEXTURE = assets.loader.image("textures/gui/widgets.png", atlas=False)
WHITE = (255, 255, 255, 255)
YELLOW = (255, 255, 85, 255)


class Button(WidgetBase):
    """A button with text."""

    def __init__(self, text: str, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self._images: Dict[str, TextureRegion] = {}
        for status in ["normal", "hover", "unable"]:
            for where in ["left", "middle", "right"]:
                name = "button_" + status + "_" + where
                self._images[name] = GUI_TEXTURE.get_region(*REGION[name])
        self._sprites: Dict[str, Sprite] = {}
        for where in ["left", "middle", "right"]:
            self._sprites[where] = Sprite(
                self._images["button_normal_" + where])
        self._label = Label(text, x=self._x + width // 2, y=self._y + height // 2 - 4,
                            color=WHITE, anchor_x="center", anchor_y="center",
                            font_name="minecraft", font_size=16)
        self._pressed = False
        self._update_position()

    def _update_position(self):
        self._sprites["left"].width = self.height
        self._sprites["left"].height = self.height
        self._sprites["middle"].width = self.width - self.height * 2
        self._sprites["middle"].height = self.height
        self._sprites["right"].width = self.height
        self._sprites["right"].height = self.height

        self._sprites["left"].position = (self._x, self._y, 0)
        self._sprites["middle"].position = (self._x + self._height, self._y, 0)
        self._sprites["right"].position = (self._x + self.width - self.height, self._y, 0)
        self._label.position = (self._x + self._width // 2, self._y + self._height // 2 - 4, 0)

    def __repr__(self) -> str:
        return f"Button(text={self._label.text})"

    @property
    def value(self):
        return self._pressed

    def draw(self):
        for where in ["left", "middle", "right"]:
            self._sprites[where].draw()
        self._label.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if (not self.enabled) or (not self._check_hit(x, y)):
            return
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = self._images["button_unable_" + where]
        self._pressed = True
        self.dispatch_event('on_press')

    def on_mouse_release(self, x, y, buttons, modifiers):
        if (not self.enabled) or (not self._pressed):
            return
        self._label.color = YELLOW if self._check_hit(x, y) else WHITE
        status = "hover" if self._check_hit(x, y) else "normal"
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = self._images["button_" +
                                                      status + "_" + where]
        self._pressed = False
        self.dispatch_event('on_release')

    def on_mouse_motion(self, x, y, dx, dy):
        if (not self.enabled) or self._pressed:
            return
        self._label.color = YELLOW if self._check_hit(x, y) else WHITE
        status = "hover" if self._check_hit(x, y) else "normal"
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = self._images["button_" +
                                                      status + "_" + where]

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if (not self.enabled) or self._pressed:
            return
        self._label.color = YELLOW if self._check_hit(x, y) else WHITE
        status = "hover" if self._check_hit(x, y) else "normal"
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = self._images["button_" +
                                                      status + "_" + where]


Button.register_event_type("on_press")
Button.register_event_type("on_release")
