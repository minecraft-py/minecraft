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
from platform import platform, python_version_tuple

from minecraft.block import gen_atlas
from minecraft.utils.utils import *
from minecraft.utils.utils import VERSION
from pyglet import version
from pyglet.gl import gl_info

logger = getLogger(__name__)


def prepare():
    # 做准备工作
    logger.info("** Start Minecraft-in-python **")
    logger.info("Operation system: %s" % platform())
    logger.info("Python version: %s" % ".".join(
        [str(s) for s in python_version_tuple()[:3]]))
    logger.info("Pyglet version: %s(OpenGL %s)" %
                (version, gl_info.get_version()))
    logger.info("Minecraft-in-python version: %s(data version: %d)" %
                (VERSION["str"], int(VERSION["data"])))
    gen_atlas()
