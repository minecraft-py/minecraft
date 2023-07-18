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

from collections import UserDict
from json import dump, load

from minecraft.utils import *


class Setting(UserDict):
    """Game setting."""

    def __init__(self):
        self._file = get_storage_path() / "setting.json"
        self.data = load(open(self._file, "r", encoding="utf-8"))

    def __missing__(self, key):
        return None

    def __repr__(self) -> str:
        return f"Setting({self.data})"

    def save(self):
        dump(self.data, open(self._file, "w+", encoding="utf-8"), ensure_ascii=False)


__all__ = ("Setting")
