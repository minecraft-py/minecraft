# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from minecraft.gui.widget import Widget
from minecraft.gui.widget.label import ColorLabel
from minecraft.utils.utils import *
from minecraft.gui.widget import Sprite
from pyglet.window import key


class Button(Widget):
    """一个有文字的按钮。"""

    def __init__(self, text, x, y, width, height, enable=True):
        self._size = win_width, win_height = get_size()
        super().__init__(x, win_height - y, width, height)
        self._width = width
        self._pressed_img = get_game().resource_pack.get_resource(
            "textures/gui/widgets").get_region(0, 150, 200, 20)
        self._depressed_img = get_game().resource_pack.get_resource(
            "textures/gui/widgets").get_region(0, 170, 200, 20)
        self._unable_img = get_game().resource_pack.get_resource(
            "textures/gui/widgets").get_region(0, 190, 200, 20)
        self._sprite = Sprite(
            self._depressed_img if enable else self._unable_img, x, win_height - y, border_width=2)
        self._text = text
        self._label = ColorLabel(self._text, color="white" if enable else "gray", align="center", anchor_x="center", anchor_y="center",
                                 x=x + width / 2, y=win_height - y + height / 2, font_size=16)
        self._pressed = False
        self._enable = enable

    def _update(self):
        self._sprite.position = self._x, self._y
        self._label.x = self._x + self._width / 2
        self._label.y = self._y + self._height / 2

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self._label.text = self._text

    def draw(self):
        self._sprite.scale_x = self._width / 200
        self._sprite.scale_y = self._height / 20
        self._sprite.draw()
        self._label.draw()

    def enable(self, status):
        self._enable = bool(status)
        if self._enable:
            self._label.color = "white"
        else:
            self._label.color = "gray"

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_hit(x, y) and self._enable:
            self._sprite.image = self._pressed_img
            self._pressed = True
            self.dispatch_event("on_press")

    def on_mouse_release(self, x, y, buttons, modifiers):
        # 请注意：由于触发`on_mouse_press`而切换场景时就无法触发该函数
        # 所以会在再切换回场景时调用该函数，而非释放鼠标时
        if self._pressed:
            self._sprite.image = self._depressed_img
            self._pressed = False
            if (x != float("nan")) and (y != float("nan")):
                self.dispatch_event("on_release")

    def on_mouse_motion(self, x, y, dx, dy):
        if self.check_hit(x, y) and self._enable:
            self._sprite.image = self._pressed_img
            self._label.color = "yellow"
        else:
            self._sprite.image = self._depressed_img if self._enable else self._unable_img
            self._label.color = "white" if self._enable else "gray"


Button.register_event_type("on_press")
Button.register_event_type("on_release")


class ImageButton(Widget):
    """以图片作为按钮。"""

    def __init__(self, images, x, y, width, height, enable=True):
        # images = [按下按钮时的图片, 未按下时的图片, 禁用时的图片]
        # 找不到禁用时的图片搞成透明的就行了
        self._size = win_width, win_height = get_size()
        super().__init__(x, y, width, height)
        assert len(images) == 3
        self._width = width
        self._pressed_img = images[0]
        self._depressed_img = images[1]
        self._unable_img = images[2]
        self._sprite = Sprite(
            self._depressed_img if enable else self._unable_img, x, win_height - y, border_width=2)
        self._pressed = False
        self._enable = enable

    def _update(self):
        self._sprite.position = self._x, self._y

    def draw(self):
        self._sprite.scale_x = self._width / self._pressed_img.width
        self._sprite.scale_y = self._height / self._pressed_img.height
        self._sprite.draw()

    def enable(self, status):
        self._enable = bool(status)
        if self._enable:
            self._sprite.image = self._depressed_img
        else:
            self._sprite.image = self._unable_img

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_hit(x, y) and self._enable:
            self._sprite.image = self._pressed_img
            self._pressed = True
            self.dispatch_event("on_press")

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self._pressed:
            self._sprite.image = self._depressed_img
            self._pressed = False
            if (x != float("nan")) and (y != float("nan")):
                self.dispatch_event("on_release")

    def on_mouse_motion(self, x, y, dx, dy):
        if self.check_hit(x, y) and self._enable:
            self._sprite.image = self._pressed_img
        else:
            self._sprite.image = self._depressed_img if self._enable else self._unable_img


ImageButton.register_event_type("on_press")
ImageButton.register_event_type("on_release")


class ChooseButton(Button):
    """一个提供选项的按钮，通过点击来改变所选项。"""

    def __init__(self, x, y, width, height, prefix, values):
        super().__init__(x, y, width, height,
                         text="%s: %s" % (prefix, values[0]))
        self._prefix = prefix
        self._values = values
        self._point = 0

    def on_mouse_press(self, x, y, buttons, modifiers):
        super().on_mouse_press(x, y, buttons, modifiers)
        if self.check_hit(x, y):
            if modifiers == key.MOD_SHIFT:
                self._point -= 1
            else:
                self._point += 1
            if self._point > len(self._values) - 1:
                self._point = 0
            elif self._point < 0:
                self._point = len(self._values) - 1
            self.text("%s: %s" % (self._prefix, self._values[self._point]))

    @property
    def value(self):
        return self._values[self._point]
