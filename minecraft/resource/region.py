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

from typing import Dict, Tuple

REGION: Dict[str, Tuple[int, ...]] = {
    # textures/gui/widgets.png
    "button_unable_left": (0, 190, 20, 20),
    "button_unable_middle": (20, 190, 160, 20),
    "button_unable_right": (180, 190, 20, 20),
    "button_normal_left": (0, 170, 20, 20),
    "button_normal_middle": (20, 170, 160, 20),
    "button_normal_right": (180, 170, 20, 20),
    "button_hover_left": (0, 150, 20, 20),
    "button_hover_middle": (20, 150, 160, 20),
    "button_hover_right": (180, 150, 20, 20),
    "language_normal": (0, 130, 20, 20),
    "language_hover": (0, 110, 20, 20),
    "accessibility_normal": (20, 130, 20, 20),
    "accessibility_hover": (20, 110, 20, 20),
    # textures/gui/title/minecraft.png
    "title_minec": (0, 212, 155, 44),
    "title_raft": (0, 167, 119, 44),
}


__all__ = "REIGON"
