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


from minecraft.gui.widgets import WidgetBase
from pyglet.shapes import Rectangle


class Scrollable(WidgetBase):
    """
    Strictly speaking, Scrollable is not a widget, it is a container
    that holds other widgets.
    The widgets in the Scrollable only have their initial absolute positions,
    and they all retain their relative positions after the scrolling operation.
    If you need to change the position of the widgets inside the
    container (x, y properties), you should use the `+=` operator.
    """

    pass


class ScrollBar(WidgetBase):
    def __init__(self, x: int, y: int, height: int):
        super().__init__(x, y, 10, height)


__all__ = ("Scrollable", "ScrollBar")
