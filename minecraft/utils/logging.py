# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from sys import argv
from time import strftime
from os import path
import logging as __logging

from minecraft.utils.utils import search_mcpy


log_file = strftime("%Y-%m-%d_%H.%M.%S.log")


def get_logger(name):
    logger = __logging.getLogger(name)
    logger.setLevel(__logging.DEBUG)
    formatter = __logging.Formatter("[%(asctime)s %(levelname)-8s] %(message)s",
                                    datefmt="%Y-%m-%d %H:%M:%S")
    ch = __logging.StreamHandler()
    ch.setLevel(__logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    if "--no-save-log" not in argv:
        fh = __logging.FileHandler(path.join(search_mcpy(), "log", log_file))
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
