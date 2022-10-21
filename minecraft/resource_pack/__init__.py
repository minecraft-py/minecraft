# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

import os
from typing import Any
from zipfile import is_zipfile

from minecraft.resource_pack.directory import DirectoryResourcePack
from minecraft.resource_pack.zipfile import ZipfileResourcePack
from minecraft.utils.utils import *


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
                search_mcpy(), "resource-pack"))
        if os.path.exists(os.path.join(name)) or (name == "${default}"):
            if os.path.isdir(os.path.join(name)) and (not name.endswith(".zip")):
                self._packs.append(DirectoryResourcePack(name))
            elif name == "${default}":
                self._packs.append(DirectoryResourcePack(os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", "assets"))))
            elif os.path.isfile(name) and is_zipfile(name):
                self._packs.append(ZipfileResourcePack(name))
            else:
                log_warn("Not a zipfile: \"%s\"" % name)
        else:
            log_warn("No such file or directory: \"%s\"" % name)

    def set_lang(self, lang: str):
        for pack in self._packs:
            pack.set_lang(lang)

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
