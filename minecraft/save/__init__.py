# Copyright 2020-2023 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from json import dump
from logging import getLogger
from os import mkdir, path

from minecraft.utils.utils import *

logger = getLogger(__name__)


def new(name: str):
    """新建存档。"""
    data = {"name": name, "data": VERSION["data"]}
    dirname = name
    # 这些字符由于某些文件系统不支持，故替换
    for c in "/\\:?\"<>|":
        dirname.replace(c, "_")
    mkdir(path.join(storage_dir(), "saves", dirname))
    dump(data, open(path.join(storage_dir(), "saves", dirname, "info.json"), "w"))
    logger.info("Save \"%s\" was created" % name)
