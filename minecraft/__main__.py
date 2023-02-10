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

import pyglet

from minecraft.scene import GameWindow
from minecraft.scene.start import StartScene
from minecraft.utils.opengl import setup_opengl
from minecraft.utils.prepare import prepare
from minecraft.utils.utils import *

logger = getLogger(__name__)


def start():
    """游戏从这里开始。

    创建窗口、进入场景、开始游戏。
    """
    try:
        setup_opengl()
        game = GameWindow(800, 600, resizable=True)
        game.add_scene("minecraft:start", StartScene)
        game.switch_scene("minecraft:start")
        pyglet.app.run()
    except SystemExit:
        pass
    except:
        logger.error("Game raise an error", exc_info=True, stack_info=True)


if __name__ == "__main__":
    # 准备工作
    prepare()
    # 开始游戏！
    start()
