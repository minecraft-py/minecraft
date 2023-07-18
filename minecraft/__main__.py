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

from logging import getLogger

import pyglet
from pyglet.gl import *
from pyglet.image import Texture

from minecraft.scenes import GameWindow
from minecraft.scenes.start import StartScene

logger = getLogger(__name__)


def start():
    """Start the game."""
    try:
        setup_gl()
        game = GameWindow(800, 600, resizable=True)
        game.add_scene("minecraft:start", StartScene)
        game.switch_scene("minecraft:start")
        pyglet.app.run()
    except SystemExit:
        pass
    except:
        logger.error("Game raise an error", exc_info=True)


def setup_gl():
    glEnable(GL_CULL_FACE)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    Texture.default_min_filter = GL_NEAREST
    Texture.default_mag_filter = GL_NEAREST


if __name__ == "__main__":
    start()
