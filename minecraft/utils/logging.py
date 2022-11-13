# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from sys import argv
from time import strftime
from os import path
import logging as __logging

from minecraft.utils.utils import search_mcpy


log_file = strftime("%Y-%m-%d_%H.%M.%S.log")


def get_logger(name: str, only_console=False):
    """返回一个日志记录器。

    该函数应该总是以`get_logger(__name__)`调用。

    将`only_console`设为`True`可不将该记录器产生的日志存入文件。

    使用`--no-save-log`命令行选项可全局运用上述效果。
    """
    logger = __logging.getLogger(name)
    logger.setLevel(__logging.DEBUG)
    formatter = __logging.Formatter("[%(asctime)s %(levelname)-8s] %(message)s",
                                    datefmt="%Y-%m-%d %H:%M:%S")
    ch = __logging.StreamHandler()
    ch.setLevel(__logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    if ("--no-save-log" not in argv) or only_console:
        fh = __logging.FileHandler(path.join(search_mcpy(), "log", log_file))
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
