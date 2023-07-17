# Minecraft-in-python, a sandbox game
# Copyright (C) 2020-2023  Minecraft-in-python team
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

from pyglet.font.base import Font, GlyphRenderer
from pyglet.gl import *


class FontRenderer(GlyphRenderer):

    def __init__(self, font: "MinecraftFont"):
        self._font = font
        super().__init__(font)
    
    def render(self, char: str):
        pass


class MinecraftFont(Font):
    ascent = 12
    descent = 4
    texture_mag_filter = GL_NEAREST
    texture_min_filter = GL_NEAREST
    glyph_renderer_class = FontRenderer

    @property
    def name(self):
        return "minecraft"
