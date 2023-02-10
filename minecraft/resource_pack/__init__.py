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

import os
from typing import Any
from logging import getLogger
from zipfile import is_zipfile

from minecraft.resource_pack.directory import DirectoryResourcePack
from minecraft.resource_pack.zipfile import ZipfileResourcePack
from minecraft.utils.utils import *

logger = getLogger(__name__)


class ResourcePackManager():
    """资源包管理器。

    使用它对游戏的资源包进行添加、读取等操作。
    """

    def __init__(self):
        self._packs = []

    def add(self, name: str):
        """添加资源包。

        支持以zip压缩文件作为资源包或直接使用文件系统上的资源包。

        同时定义了几个特殊量：

        1. `${default}`：默认的资源包, 在游戏源代码的`minecraft/assert`处
        2. `${game}`：存放游戏数据目录下的`resource-pack`目录
        """
        if name.startswith("${game}"):
            name.replace("${game}", os.path.join(
                storage_dir(), "resource-pack"))
        if os.path.exists(os.path.join(name)) or (name == "${default}"):
            if os.path.isdir(os.path.join(name)) and (not name.endswith(".zip")):
                self._packs.append(DirectoryResourcePack(name))
            elif name == "${default}":
                self._packs.append(DirectoryResourcePack(os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", "assets"))))
            elif os.path.isfile(name) and is_zipfile(name):
                self._packs.append(ZipfileResourcePack(name))
            else:
                logger.warning("Not a zipfile: \"%s\"" % name)
        else:
            logger.warning("No such file or directory: \"%s\"" % name)

    def set_lang(self, lang: str):
        for pack in self._packs:
            pack.set_lang(lang)
    
    def get_all_block_textures(self):
        l = set()
        for pack in self._packs:
            l.update(pack.get_all_block_textures())
        return l

    def get_translation(self, name: str) -> str:
        for pack in self._packs:
            if pack.get_translation(name) != name:
                return pack.get_translation(name)
        else:
            return name

    def get_pack_info(self) -> list:
        l = []
        for pack in self._packs:
            l.append(pack.get_pack_info())
        return l

    def get_resource(self, path: str) -> Any:
        for pack in self._packs:
            try:
                return pack.get_resource(path)
            except:
                pass
        else:
            raise FileNotFoundError("No such resource: \"%s\"" % path)
