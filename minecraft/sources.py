# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

import json
import re
import sys
from importlib import import_module
from locale import getdefaultlocale
from os import pathsep
from os.path import isdir, isfile, join
from zipfile import is_zipfile

from minecraft.resource_pack import ResourcePackManager
from minecraft.utils.utils import *

mcpypath = search_mcpy()
sys.path.insert(0, join(mcpypath, "lib", VERSION["str"]))
lib_path = sys.path[0]
libs = []
settings = json.load(open(join(mcpypath, "settings.json"), encoding="utf-8"))

# 设置资源包
# 如果设置里的"resource-pack"键没有设置或者为空列表则设置为默认资源包
resource_pack = ResourcePackManager()
if (settings.get("resource-pack") is None) or (len(settings.get("resource-pack", [])) == 0):
    resource_pack.add("${default}")
else:
    for pack in settings["resource-pack"]:
        resource_pack.add(pack)

# 设置语言
# 如果设置里的"lang"键没有设置默认为系统语言
if settings.get("lang", "${auto}") == "${auto}":
    lang = getdefaultlocale()[0].lower()
else:
    lang = settings.get("lang", "en_us").lower()
resource_pack.set_lang(lang)

# 设置视角
# 在50~100之间, 默认70
settings["fov"] = max(50, min(100, settings.get("fov", 70)))

# 读取玩家信息
if isfile(join(mcpypath, "player.json")):
    player = json.load(open(join(mcpypath, "player.json"), encoding="utf-8"))
    if not re.match("^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$", player["id"]):
        log_err("Invalid player id: %s" % player["id"])
        exit(1)
else:
    log_err("You have not registered, exit")
    exit(1)

# 解析命令行参数
# 就不用argparse了，毕竟参数比较少
for args in sys.argv:
    if args.startswith("--include="):
        # 将某一路径添加到sys.path，zip文件亦受支持
        for lib in args[10:].split(pathsep):
            if isdir(lib) or (isfile(lib) and is_zipfile(lib)):
                sys.path.insert(0, lib)
                log_info("Add new lib path: `%s`" % lib)
            else:
                log_warn("Lib path \"%s\" is not available" % lib)
    elif args.startswith("--extlib="):
        # 如果没有下面的for循环, 那么即使有模组加载器也没有任何用处，对吧
        for lib in args[9:].split(pathsep):
            if isdir(join(lib_path, lib)) or isfile(join(lib_path, lib + ".py")):
                log_info("Loading extra lib: \"%s\"" % lib)
                libs.append(import_module(lib))
            else:
                log_warn("Extra lib \"%s\" not found" % lib)
