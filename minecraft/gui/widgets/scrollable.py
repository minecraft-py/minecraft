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

from typing import List, Optional, Tuple, Union

from minecraft.gui.widgets import WidgetBase
from pyglet import gl
from pyglet.gui.widgets import WidgetBase as PygletWidgetBase
from pyglet.shapes import Rectangle, ShapeBase


class ScrollableLayout(WidgetBase):
    """
    Strictly speaking, ScrollableLayout is not a widget, it is a container
    that holds other widgets.

    The widgets in the ScrollableLayout only have their initial absolute positions,
    and they all retain their relative positions after the scrolling operation.
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
        if self._content_height < self._height:
            self._content_height = self._height
        self._offset_y = 0
        self._value: float = 0
        self._hscroll: Optional[ScrollBar] = None
        self._elements: List[Union[PygletWidgetBase, ShapeBase]] = []

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
        if self._content_height < self._height:
            self._content_height = self._height
        if self._content_height > self._height:
            self._hscroll.visiable = True
        else:
            self.offset_y = 0
            self._hscroll.visiable = False
        self._update_position()

    @property
    def content_height(self):
        return self._content_height

    @content_height.setter
    def content_height(self, value):
        if value < self._height:
            value = self._height
        self._content_height = value
        if self._content_height > self._height:
            self._hscroll.visiable = True
        else:
            self.offset_y = 0
            self._hscroll.visiable = False

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
        if self._offset_y == 0:
            self._hscroll.value = 0
        else:
            self._hscroll.value = self._offset_y / (self._content_height - self._height)

    def add(self, *elements: Union[PygletWidgetBase, ShapeBase]):
        """
        Add some elements to ScrollableLayout.

        Objects that are instanced in `pyglet.gui.widget.WidgetBase` and
        `pyglet.shapes.ShapeBase` are recommended.

        Otherwise, the objects need to have `x`, `y` attributes and
        `draw` method and cannot be `ScrollableLayout` or `ScrollBar`.
        """
        for obj in elements:
            if obj not in self._elements:
                assert (
                    hasattr(obj, "x") and hasattr(obj, "y") and hasattr(obj, "draw")
                ), "must have x, y attributes and draw method"
                if isinstance(obj, (ScrollableLayout, ScrollBar)):
                    raise TypeError(
                        f"{obj.__class__.__name__} cannot add to ScrollableLayout"
                    )
                self._elements.append(obj)

    def draw(self):
        gl.glEnable(gl.GL_SCISSOR_TEST)
        gl.glScissor(self._x, self._y, self._width, self._height)
        for obj in self._elements:
            obj.draw()
        gl.glDisable(gl.GL_SCISSOR_TEST)

    def get_point(self, x: int, y: int) -> Tuple[int, int]:
        """
        Get the absolute position of `(x, y)` after the ScrollableLayout has been scrolled.

        Returns `(x, y)` itself when it is outside the widget.
        """
        if not self._check_hit(x, y):
            return (x, y)
        return (x, y + self._offset_y)

    def scroll(self, dx: int, dy: int):
        for obj in self._elements:
            obj.y += dy

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for obj in self._elements:
            if hasattr(obj, "on_mouse_drag"):
                obj.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for obj in self._elements:
            if hasattr(obj, "on_mouse_motion"):
                obj.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, buttons, modifiers):
        for obj in self._elements:
            if hasattr(obj, "on_mouse_press"):
                obj.on_mouse_press(x, y, buttons, modifiers)

    def on_mouse_release(self, x, y, buttons, modifiers):
        for obj in self._elements:
            if hasattr(obj, "on_mouse_release"):
                obj.on_mouse_release(x, y, buttons, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self._hscroll.visiable and self._check_hit(x, y):
            self.offset_y -= 8 * scroll_y

    def on_scrollbar_scroll(self, vx, vy):
        self.offset_y = vy * (self._content_height - self._height)


ScrollableLayout.register_event_type("on_scrollbar_scroll")


class ScrollBar(WidgetBase):
    def __init__(
        self, x: int, y: int, height: int, scrollable_layout: ScrollableLayout
    ):
        super().__init__(x, y, 12, height)
        self._press = False
        self._value: float = 0
        self._visiable = True
        self._scrollable_layout = scrollable_layout
        self._scrollable_layout.hscroll = self
        if self._scrollable_layout.content_height <= self._scrollable_layout.height:
            self._visiable = False

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
            self._height
            * self._scrollable_layout.height
            / self._scrollable_layout.content_height
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

    @property
    def visiable(self):
        return self._visiable

    @visiable.setter
    def visiable(self, value: bool):
        self._visiable = bool(value)
        if not self._visiable:
            self.value = 0
        else:
            self._update_position()

    def draw(self):
        if self._visiable:
            self._scrolling_area.draw()
            self._bbar.draw()
            self._fbar.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._visiable and self._check_hit(x, y) and (x, y) in self._bbar:
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
            self._scrollable_layout.dispatch_event(
                "on_scrollbar_scroll", 0, self._value
            )


__all__ = ("ScrollableLayout", "ScrollBar")
