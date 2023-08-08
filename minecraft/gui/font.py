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

import string
from io import BytesIO
from typing import Dict, Tuple

from PIL import Image
from PIL.Image import Resampling
from pyglet import image
from pyglet.font import base, create_font

from minecraft import assets

SIZE16 = 16
SIZE24 = 24
SIZE32 = 32

source = assets.loader.file("textures/font/ascii.png", "rb")
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
fonts: Dict[Tuple[str, int], base.Font] = {}
for size, metrics in {SIZE16: [14, 2], SIZE24: [21, 3], SIZE32: [28, 4]}.items():
    image_source = Image.open(source)
    image_source = image_source.resize((size * 16, size * 16), Resampling.NEAREST)
    image_resized = BytesIO()
    image_source.save(image_resized, format="png")
    image_resized.seek(0)
    image_font = image.load("ascii.png", file=image_resized)

    mappings = {}
    for c in " " + string.ascii_letters + string.digits + string.punctuation:
        x, y = ord(c) % 16 * size, size * 16 - (ord(c) // 16 + 1) * size
        w = (special_width[c] if c in special_width else 0.75) * size
        mappings[c] = image_font.get_region(x, y, int(w), size).get_image_data()
    fonts[("minecraft", size)] = create_font(
        name="minecraft",
        mappings=mappings,
        default_char=" ",
        ascent=metrics[0],
        descent=metrics[1],
        size=size,
    )

__all__ = ("SIZE16", "SIZE24", "SIZE32", "fonts")
