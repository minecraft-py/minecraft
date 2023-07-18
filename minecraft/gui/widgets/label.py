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

from typing import Dict, List, Tuple

# https://minecraft.fandom.com/wiki/Formatting_codes#Formatting_codes
COLOR: Dict[str, List[Tuple[int, ...]]] = {
    "black": [(0, 0, 0), (255, 255, 255)],
    "dark_blue": [(0, 0, 170), (0, 0, 42)],
    "dark_green": [(0, 170, 0), (0, 42, 0)],
    "dark_aqua": [(0, 170, 170), (0, 42, 42)],
    "dark_red": [(170, 0, 0), (42, 0, 0)],
    "dark_purple": [(170, 0, 170), (42, 0, 42)],
    "gold": [(255, 170, 0), (64, 42, 0)],
    "gray": [(170, 170, 170), (42, 42, 42)],
    "dark_gray": [(85, 85, 85), (21, 21, 21)],
    "blue": [(85, 85, 255), (21, 21, 63)],
    "aqua": [(85, 255, 255), (21, 63, 63)],
    "red": [(255, 85, 85), (66, 21, 21)],
    "light_purple": [(255, 85, 255), (63, 21, 63)],
    "yellow": [(255, 255, 85), (63, 63, 21)],
    "white": [(255, 255, 255), (63, 63, 63)]
}
