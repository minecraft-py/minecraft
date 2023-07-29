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
from pyglet import gl
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
    gl.glEnable(gl.GL_CULL_FACE)
    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glEnable(gl.GL_POLYGON_SMOOTH)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    Texture.default_min_filter = gl.GL_NEAREST
    Texture.default_mag_filter = gl.GL_NEAREST


if __name__ == "__main__":
    start()
