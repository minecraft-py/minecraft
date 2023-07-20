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

from minecraft import assets
from PIL import Image
from PIL.Image import Resampling
from pyglet.font import create_font
from pyglet import image

NORMAL_SIZE = 16
BIG_SIZE = 24

source = assets.loader.file("textures/font/ascii.png", "rb")
special_width = {
    " ": 0.375, ",": 0.5, "!": 0.5,
    "F": 0.625, "I": 0.5,
    "f": 0.625, "i": 0.25, "l": 0.375, "t": 0.5,
    "\"": 0.5, "'": 0.25, ".": 0.375, ":": 0.375, ";": 0.375,
    "[": 0.5, "]": 0.5, "{": 0.5, "|": 0.5, "}": 0.5
}
for size, metrics in {
    NORMAL_SIZE: [14, 2],
    BIG_SIZE: [21, 3]
}.items():
    source_image = Image.open(source)
    source_image = source_image.resize(
        (size * 16, size * 16), Resampling.NEAREST)
    resized_image = BytesIO()
    source_image.save(resized_image, format="png")
    resized_image.seek(0)
    font_image = image.load("ascii.png", file=resized_image)

    mappings = {}
    for c in " " + string.ascii_letters + string.digits + string.punctuation:
        x, y = ord(c) % 16 * size, size * 16 - (ord(c) // 16 + 1) * size
        w = (special_width[c] if c in special_width else 0.75) * size
        mappings[c] = font_image.get_region(
            x, y, int(w), size).get_image_data()
    create_font(name="minecraft", mappings=mappings, default_char=" ",
                ascent=metrics[0], descent=metrics[1], size=size)

__all__ = ("NORMAL_SIZE", "BIG_SIZE")
