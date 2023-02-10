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

from logging import getLogger

from minecraft.utils.utils import *
from minecraft import resource_pack, player
from pyglet.image.atlas import TextureAtlas

logger = getLogger(__name__)
atlas = None
coords = None


def gen_atlas():
    atlas = TextureAtlas(256, 256)
    coords = {}
    logger.info("Create %dx%d texture atlas" %
                (atlas.texture.width, atlas.texture.height))
    for name in resource_pack.get_all_block_textures():
        pos = atlas.add(resource_pack.get_resource("textures/block/" + name))
        coords[name] = tex_coord(pos, atlas.texture.width)
