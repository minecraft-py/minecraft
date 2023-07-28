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

from typing import List, Optional, Union

from minecraft.gui.widgets import WidgetBase
from pyglet.gl import *
from pyglet.gui.widgets import WidgetBase as PygletWidgetBase
from pyglet.shapes import Rectangle, ShapeBase


class Scrollable(WidgetBase):
    """
    Strictly speaking, Scrollable is not a widget, it is a container
    that holds other widgets.

    The widgets in the Scrollable only have their initial absolute positions,
    and they all retain their relative positions after the scrolling operation.

    If you need to change the position of the widgets inside the
    container (x, y properties), you should use the `+=` or `-=` operator.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        content_height: Optional[int] = None,
    ):
        super().__init__(x, y, width, height)
        self._content_height = content_height or height
        assert self._content_height >= self._height
        self._offset_y = 0
        self._value: float = 0
        self._hscroll: Optional[ScrollBar] = None
        # The elements in `Scrollable._contents` must have `x` and `y` properties.
        self._contents: List[Union[PygletWidgetBase, ShapeBase]] = []

    def _update_position(self):
        pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self._update_position()

    @property
    def content_height(self):
        return self._content_height

    @content_height.setter
    def content_height(self, value):
        assert value >= self._height
        self._content_height = value

    @property
    def hscroll(self):
        return None

    @hscroll.setter
    def hscroll(self, value: "ScrollBar"):
        self._hscroll = value

    @property
    def offset_y(self):
        return self._offset_y

    @offset_y.setter
    def offset_y(self, value: int):
        value = max(0, min(self._content_height - self._height, value))
        self.scroll(0, value - self._offset_y)
        self._offset_y = value

    def add(self, *elements: Union[PygletWidgetBase, ShapeBase]):
        for element in elements:
            if element not in self._contents:
                assert (
                    hasattr(element, "x")
                    and hasattr(element, "y")
                    and hasattr(element, "draw")
                )
                if isinstance(elements, (Scrollable, ScrollBar)):
                    raise TypeError(
                        f"{element.__class__.__name__} cannot add to Scrollable"
                    )
                self._contents.append(element)

    def draw(self):
        glEnable(GL_SCISSOR_TEST)
        glScissor(self._x, self._y, self._width, self._height)
        for element in self._contents:
            element.draw()
        glDisable(GL_SCISSOR_TEST)

    def scroll(self, dx: int, dy: int):
        for element in self._contents:
            element.y += dy

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self._check_hit(x, y):
            self.offset_y -= 8 * scroll_y
            self._hscroll.value = self._offset_y / (self._content_height - self._height)

    def on_scrollbar_scroll(self, vx, vy):
        self.offset_y = vy * (self._content_height - self._height)


Scrollable.register_event_type("on_scrollbar_scroll")


class ScrollBar(WidgetBase):
    def __init__(self, x: int, y: int, height: int, scrollable: Scrollable):
        super().__init__(x, y, 12, height)
        self._press = False
        self._value: float = 0
        self._scrollable = scrollable
        self._scrollable.hscroll = self

        self._scrolling_area = Rectangle(
            self._x, self._y, self._width, self._height, color=(0, 0, 0, 192)
        )
        self._fbar = Rectangle(
            self._x,
            self._y + self._height - self._height * 0.5 + 3,
            self._width - 3,
            self._height * 0.5 - 3,
            color=(192, 192, 192, 255),
        )
        self._bbar = Rectangle(
            self._x,
            self._y + self._height - self._height * 0.5,
            self._width,
            self._height * 0.5,
            color=(128, 128, 128, 255),
        )

        self._update_position()

    def _refresh_value(self):
        self._value = (self._y + self._height - self._bbar.y - self._bbar.height) / (
            self._height - self._bbar.height
        )
        self._value = max(0, min(1, self._value))

    def _update_position(self):
        self._scrolling_area.position = (self._x, self._y)
        self._scrolling_area.height = self._height

        self._bbar.height = (
            self._height * self._scrollable.height / self._scrollable.content_height
        )
        self._fbar.height = self._bbar.height - 3

        self._bbar.position = (
            self._x,
            self._y
            + self._height
            - self._bbar.height
            - self._value * (self._height - self._bbar.height),
        )
        self._fbar.position = (self._x, self._bbar.y + 3)

    @property
    def value(self):
        return max(0, min(1, self._value))

    @value.setter
    def value(self, value: float):
        self._value = value
        self._update_position()

    def draw(self):
        self._scrolling_area.draw()
        self._bbar.draw()
        self._fbar.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y) and (x, y) in self._bbar:
            self._press = True

    def on_mouse_release(self, x, y, buttons, modifiers):
        self._press = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._press:
            self._bbar.y = max(
                self._y,
                min(self._y + self._height - self._bbar.height, self._bbar.y + dy),
            )
            self._fbar.y = self._bbar.y + 3
            self._refresh_value()
            self._scrollable.dispatch_event("on_scrollbar_scroll", 0, self._value)


__all__ = ("Scrollable", "ScrollBar")
