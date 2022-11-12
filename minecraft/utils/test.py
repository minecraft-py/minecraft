# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from platform import platform, python_version_tuple

from pyglet import version
from pyglet.gl import gl_info

from minecraft.utils.logging import get_logger
from minecraft.utils.utils import VERSION


logger = get_logger(__name__)


def test():
    # 在游戏最开始时输出的调试信息, 在报告issue时应该附带这些信息
    logger.info("** Start Minecraft-in-python **")
    logger.info("Operation system: %s" % platform())
    logger.info("Python version: %s" % ".".join(
        [str(s) for s in python_version_tuple()[:3]]))
    logger.info("Pyglet version: %s(OpenGL %s)" %
             (version, gl_info.get_version()))
    logger.info("Minecraft-in-python version: %s(data version: %s)" %
             (VERSION["str"], VERSION["data"]))
