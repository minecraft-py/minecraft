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
