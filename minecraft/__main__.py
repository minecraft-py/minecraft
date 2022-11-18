# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

import atexit
import logging.config
import sys
import traceback
from os import remove
from os.path import isfile, join

import pyglet

from minecraft.utils.logging import config
from minecraft.scene import GameWindow
from minecraft.scene.start import StartScene
from minecraft.utils.opengl import setup_opengl
from minecraft.utils.test import test
from minecraft.utils.utils import *


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
        pass


if __name__ == "__main__":
    logging.config.dictConfig(config)
    # 打印运行环境等基本信息
    test()
    # 开始游戏！
    start()
