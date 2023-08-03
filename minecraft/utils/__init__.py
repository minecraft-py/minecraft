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

import sys
from inspect import getmodule
from pathlib import Path
from typing import Union

import pyglet

VERSION = {
    "major": 0,
    "minor": 0,
    "patch": 1,
    "str": "0.0.1",
    "data": 1,
    "stable": False,
}
STORAGE_DIR: Union[Path, None] = None
_GAME_WINDOW = None


def get_caller() -> str:
    """Get the package name of the penultimate function in the call stack.

    The call stack:

    1. function 1 (which calls function 2)
    2. function 2 (called this function)
    3. this function (return the name of the package where function 1 is located)
    """
    module = getmodule(sys._getframe().f_back.f_back.f_code)
    if module is not None:
        return module.__name__
    else:
        return "unknow"


def get_game_window_instance():
    """Get an instance of the `GameWindow` class, which is the main window
    of the game.
    """
    global _GAME_WINDOW
    if _GAME_WINDOW is not None:
        return _GAME_WINDOW
    for w in pyglet.app.windows:
        if hasattr(w, "minecraft_gamewindow") and w.minecraft_gamewindow == 0x1BF52:
            _GAME_WINDOW = w
            return _GAME_WINDOW
    raise RuntimeError("no GameWindow found")


def get_storage_path() -> Path:
    """Return the file storage location."""
    if STORAGE_DIR is None:
        return Path(pyglet.resource.get_script_home(), ".minecraft")
    else:
        return STORAGE_DIR


def is_namespace(s: str, /) -> bool:
    """Determines if a string is a namespace.

    The namespace should satisfy
    `[top-level namespace]:<sub-namespace1>.<sub-namespace2>...<sub-namespace n>`.

    The top-level namespace may be omitted, defaulting to `minecraft`; sub-namespaces
    are separated by `.`.

    Use `str.partition()` to detect if a namespace is legal.
    """
    l = s.partition(":")
    if s.partition(":")[1]:
        return l[0].isidentifier() and all(
            [sub.isidentifier() for sub in l[2].split(".")]
        )
    else:
        return all([sub.isidentifier() for sub in l[0].split(".")])


def romanisation(num: int, /) -> str:
    """Convert an inreger to its roman numeral.
    `num` should be within the range from 1 to 999.

    Referred from https://github.com/keon/algorithms
    """
    assert 1 <= num <= 999
    c = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    x = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "LC"]
    i = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    return c[(num % 1000) // 100] + x[(num % 100) // 10] + i[num % 10]


__all__ = (
    "VERSION",
    "get_caller",
    "get_game_window_instance",
    "get_storage_path",
    "is_namespace",
    "romanisation",
)
