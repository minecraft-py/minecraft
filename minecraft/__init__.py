# Copyright 2020-2023 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

import json
import re
import sys
from logging import getLogger
from locale import getdefaultlocale
from os import pathsep
from os.path import isdir, isfile, join
from pkgutil import find_loader
from zipfile import is_zipfile

from minecraft.resource_pack import ResourcePackManager
from minecraft.utils.utils import *

logger = getLogger(__name__)
mcpypath = storage_dir()
sys.path.insert(0, join(mcpypath, "lib", VERSION["str"]))
lib_path = sys.path[0]
libs = []
settings = json.load(open(join(mcpypath, "settings.json"), encoding="utf-8"))

# 设置资源包
resource_pack = ResourcePackManager()
if (settings.get("resource-pack") is None) or (len(settings.get("resource-pack", [])) == 0):
    resource_pack.add("${default}")
else:
    for pack in settings["resource-pack"]:
        resource_pack.add(pack)

# 设置语言
if settings.get("lang", "${auto}") == "${auto}":
    lang = getdefaultlocale()[0].lower()
else:
    lang = settings.get("lang", "en_us").lower()
resource_pack.set_lang(lang)

# 设置视场
settings["fov"] = max(50, min(100, settings.get("fov", 70)))

# 读取并检验玩家信息
if isfile(join(mcpypath, "player.json")):
    player = json.load(open(join(mcpypath, "player.json"), encoding="utf-8"))
    for key, _ in player.items():
        if not re.match("^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$", key):
            logger.error("Invalid player id: %s" % player["id"])
            exit(1)
else:
    logger.error("You have not registered, exit")
    exit(1)

# 解析命令行参数
for args in sys.argv:
    if args.startswith("--include="):
        # 将路径添加到sys.path
        for lib in args[10:].split(pathsep):
            if isdir(lib) or (isfile(lib) and is_zipfile(lib)):
                sys.path.insert(0, lib)
                logger.info("Add new lib path: `%s`" % lib)
            else:
                logger.warning("Lib path \"%s\" is not available" % lib)
    elif args.startswith("--extlib="):
        # 添加外部库
        for lib in args[9:].split(pathsep):
            if (loader := find_loader(lib)) is not None:
                logger.info("Loading extra lib: \"%s\"" % lib)
                libs.append(loader.load_module())
            else:
                logger.warning("Extra lib \"%s\" not found" % lib)
