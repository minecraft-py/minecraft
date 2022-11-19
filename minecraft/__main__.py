# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from logging import getLogger

import pyglet

import minecraft.utils.logging
from minecraft.scene import GameWindow
from minecraft.scene.start import StartScene
from minecraft.utils.opengl import setup_opengl
from minecraft.utils.test import test
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
    # 打印运行环境等基本信息
    test()
    # 开始游戏！
    start()
