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

from __future__ import annotations
from functools import lru_cache
import string
from io import BytesIO
from typing import Dict, Optional, Tuple

from PIL import Image
from PIL.Image import Resampling
from pyglet.image import ImageData, load as load_image
from pyglet.font import base, create_font

from minecraft import assets

SIZE16 = 16
SIZE24 = 24
SIZE32 = 32

fonts = {}
image_cache = {}
special_width = {
    " ": 0.375,
    ",": 0.5,
    "!": 0.5,
    "F": 0.625,
    "I": 0.5,
    "f": 0.625,
    "i": 0.25,
    "l": 0.375,
    "t": 0.5,
    '"': 0.5,
    "'": 0.25,
    ".": 0.375,
    ":": 0.375,
    ";": 0.375,
    "[": 0.5,
    "]": 0.5,
    "{": 0.5,
    "|": 0.5,
    "}": 0.5,
}


class UserGlyphRenderer(base.GlyphRenderer):
    def __init__(self, font: UserDefinedFont):
        self._font = font
        self._font.glyphs[self._font.default_char] = self.render(
            self._font.default_char
        )
        super().__init__(font)

    def render(self, text: str):
        image_data = self._font.find_glyph(text, self._font.size)
        glyph = self._font.create_glyph(image_data)
        glyph.set_bearings(-self._font.descent, 0, image_data.width)
        return glyph


class UserDefinedFont(base.Font):
    glyph_renderer_class = UserGlyphRenderer

    def __init__(
        self,
        mappings: Dict[str, ImageData],
        default_char: str,
        name: str,
        ascent: int,
        descent: int,
        size: int,
        bold: Optional[bool] = False,
        italic: Optional[bool] = False,
        stretch: Optional[bool] = False,
        dpi: Optional[int] = None,
        locale: Optional[str] = None,
    ):
        super().__init__()
        self._name = name
        self.ascent = ascent
        self.descent = descent
        self.default_char = default_char
        self.bold = bold
        self.italic = italic
        self.stretch = stretch
        self.dpi = dpi
        self.size = size
        self.locale = locale

    @property
    def name(self):
        return self._name

    @lru_cache(4096)
    def find_glyph(self, char: str, size: int):
        if ord(char) > 0xFFFF:
            return None
        code = ord(char)
        left, right = code >> 8, code % 256
        if char in string.printable:
            left = -1
        if (size, left) not in image_cache:
            if left == -1:
                original = assets.loader.file("textures/font/ascii.png", "rb")
            else:
                original = assets.loader.file(
                    f"textures/font/unicode_page_{left:02x}.png", "rb"
                )
            source = Image.open(original)
            source = source.resize((size * 16,) * 2, Resampling.NEAREST)
            resized_source = BytesIO()
            source.save(resized_source, format="png")
            resized_source.seek(0)
            image_font = load_image("image.png", file=resized_source)
            image_cache[(size, left)] = image_font
        font_image = image_cache[(size, left)]
        x, y = (
            right % 16 * size,
            size * 16 - (right // 16 + 1) * size,
        )
        if char in special_width:
            a = special_width[char]
        elif char in string.printable:
            a = 0.75
        else:
            a = 1
        return font_image.get_region(x, y, int(a * size), size).get_image_data()

    def get_glyphs(self, text):
        glyph_renderer = None
        glyphs = []
        for c in base.get_grapheme_clusters(str(text)):
            if c == "\t":
                c = " "
            if c not in self.glyphs:
                if not glyph_renderer:
                    glyph_renderer = self.glyph_renderer_class(self)
                if self.find_glyph(c, self.size) is None:
                    c = self.default_char
                else:
                    self.glyphs[c] = glyph_renderer.render(c)
            glyphs.append(self.glyphs[c])
        return glyphs


for size, metrics in {SIZE16: [14, 2], SIZE24: [21, 3], SIZE32: [28, 4]}.items():
    fonts[("minecraft", size)] = create_font(
        name="minecraft",
        mappings={},
        default_char=" ",
        ascent=metrics[0],
        descent=metrics[1],
        size=size,
        font_class=UserDefinedFont,
    )

__all__ = ("SIZE16", "SIZE24", "SIZE32", "fonts")
