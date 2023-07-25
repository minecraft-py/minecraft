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

from minecraft import assets
from minecraft.gui.widgets import WidgetBase
from minecraft.gui.widgets.label import Label
from minecraft.resource import REGION
from minecraft.utils import *
from pyglet.image import TextureRegion
from pyglet.sprite import Sprite
from pyglet.window.mouse import LEFT

WIDGETS_TEXTURE = assets.loader.image("textures/gui/widgets.png")


class ImageButton(WidgetBase):
    """Using an image as a button."""

    def __init__(self, image_normal, image_hover, x, y, width, height):
        super().__init__(x, y, width, height)
        self._pressed = False
        self._image_normal = image_normal
        self._image_hover = image_hover
        self._sprite = Sprite(self._image_normal, x, y)
        self._sprite.width = width
        self._sprite.height = height

    def _update_position(self):
        self._sprite.width = self._width
        self._sprite.height = self._height
        self._sprite.position = (self._x, self._y, 0)

    @property
    def value(self) -> bool:
        return self._pressed

    def draw(self):
        self._sprite.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons != LEFT:
            return
        if not self.enabled or not self._check_hit(x, y):
            return
        self._sprite.image = self._image_normal
        self._pressed = True
        self.dispatch_event("on_press")

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.enabled or not self._pressed:
            return
        image = self._image_hover if self._check_hit(x, y) else self._image_normal
        self._sprite.image = image
        self._pressed = False
        self.dispatch_event("on_release")

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.enabled or self._pressed:
            return
        image = self._image_hover if self._check_hit(x, y) else self._image_normal
        self._sprite.image = image

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.enabled or self._pressed:
            return
        image = self._image_hover if self._check_hit(x, y) else self._image_normal
        self._sprite.image = image


ImageButton.register_event_type("on_press")
ImageButton.register_event_type("on_release")


class TextButton(WidgetBase):
    """A button with text."""

    def __init__(self, text: str, x: int, y: int, width: int, height: int, enable=True):
        super().__init__(x, y, width, height)
        self.enabled = enable
        self._pressed = False
        self._images: Dict[str, TextureRegion] = {}
        self._sprites: Dict[str, Sprite] = {}
        for status in ["normal", "hover", "unable"]:
            for where in ["left", "middle", "right"]:
                name = "button_" + status + "_" + where
                self._images[name] = WIDGETS_TEXTURE.get_region(*REGION[name])
        for where in ["left", "middle", "right"]:
            self._sprites[where] = Sprite(
                self._images[
                    "button_" + ("normal_" if self.enabled else "unable_") + where
                ]
            )
        self._label = Label(
            text,
            x=self._x + width // 2,
            y=self._y + height // 2 - 4,
            color="white" if self.enabled else "gray",
            anchor_x="center",
            anchor_y="center",
        )
        self._update_position()

    def _update_position(self):
        self._sprites["left"].width = self._height
        self._sprites["left"].height = self._height
        self._sprites["middle"].width = self._width - self._height * 2
        self._sprites["middle"].height = self._height
        self._sprites["right"].width = self._height
        self._sprites["right"].height = self._height

        self._sprites["left"].position = (self._x, self._y, 0)
        self._sprites["middle"].position = (self._x + self._height, self._y, 0)
        self._sprites["right"].position = (
            self._x + self._width - self._height,
            self._y,
            0,
        )
        self._label.position = (
            self._x + self._width // 2,
            self._y + self._height // 2 - 4,
            0,
        )

    @property
    def enable(self) -> bool:
        return self.enabled

    @enable.setter
    def enable(self, value: bool):
        self.enabled = bool(value)
        for where in ["left", "middle", "right"]:
            self._sprites[where] = Sprite(
                self._images[
                    "button_" + ("normal_" if self.enabled else "unable_") + where
                ]
            )
        self._label.color = "white" if self.enabled else "gray"

    @property
    def value(self) -> bool:
        return self._pressed

    def draw(self):
        for where in ["left", "middle", "right"]:
            self._sprites[where].draw()
        self._label.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons != LEFT:
            return
        if not self.enabled or not self._check_hit(x, y):
            return
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = self._images["button_unable_" + where]
        self._pressed = True
        self.dispatch_event("on_press")

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.enabled or not self._pressed:
            return
        self._label.color = "yellow" if self._check_hit(x, y) else "white"
        status = "hover" if self._check_hit(x, y) else "normal"
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = self._images["button_" + status + "_" + where]
        self._pressed = False
        self.dispatch_event("on_release")

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.enabled or self._pressed:
            return
        self._label.color = "yellow" if self._check_hit(x, y) else "white"
        status = "hover" if self._check_hit(x, y) else "normal"
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = self._images["button_" + status + "_" + where]

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.enabled or self._pressed:
            return
        self._label.color = "yellow" if self._check_hit(x, y) else "white"
        status = "hover" if self._check_hit(x, y) else "normal"
        for where in ["left", "middle", "right"]:
            self._sprites[where].image = self._images["button_" + status + "_" + where]


TextButton.register_event_type("on_press")
TextButton.register_event_type("on_release")

__all__ = ("ImageButton", "TextButton")
