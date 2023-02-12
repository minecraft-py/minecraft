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

import argparse
import json
import re
import sys
from locale import getdefaultlocale
from logging import getLogger
from os import pathsep
from os.path import isdir, isfile, join
from pkgutil import find_loader
from zipfile import is_zipfile

import minecraft.utils.logging
from minecraft.resource_pack import ResourcePackManager
from minecraft.utils.utils import *

logger = getLogger(__name__)
mcpypath = storage_dir()
parser = argparse.ArgumentParser(
    description="A sandbox game", prog="minecraft")
parser.add_argument("--extlib", help="add extra lib", metavar="LIB")
parser.add_argument(
    "--include", help="add paths to `sys.path`", metavar="PATH")
parser.add_argument("--player", type=argparse.FileType("r", encoding="utf-8"),
                    help="player information", metavar="FILE")
parser.add_argument("--settings", type=argparse.FileType("r", encoding="utf-8"),
                    help="game settings", metavar="FILE")
parser.add_argument("-V", "--version", action="version",
                    version="%(prog)s " + VERSION["str"] + ("(stable)" if isinstance(VERSION["data"], int) else "(in develop)"))
args = parser.parse_args()

# 游戏设置
settings = {}
if args.settings is not None:
    settings = json.load(args.settings)
elif isfile(join(mcpypath, "settings.json")):
    settings = json.load(
        open(join(mcpypath, "settings.json"), encoding="utf-8"))
# 限制视场
settings["fov"] = max(50, min(100, settings.get("fov", 70)))
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

# 读取玩家信息
if args.player is not None:
    player = json.load(args.player)
elif isfile(join(mcpypath, "player.json")):
    player = json.load(
        open(join(mcpypath, "player.json"), encoding="utf-8"))
else:
    logger.error("No \"player.json\" found")
    exit(1)
# 检验之
if ("uuid" not in player) or ("name" not in player):
    logger.error("Invalid player information")
    exit(1)
if not re.match("^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$", player["uuid"]):
    logger.error("Invalid player id: %s" % player["id"])
    exit(1)

libs = []
sys.path.insert(0, join(storage_dir(), "lib", VERSION["str"]))
# 将路径添加到sys.path
if args.include is not None:
    for path in args.lib.split(pathsep):
        if isdir(path) or (isfile(path) and is_zipfile(path)):
            sys.path.insert(0, path)
            logger.info("Add new lib path: `%s`" % path)
        else:
            logger.warning("Lib path \"%s\" is not available" % path)
# 导入外部库
if args.extlib is not None:
    for lib in args.extlib.split(","):
        if (loader := find_loader(lib)) is not None:
            logger.info("Loading extra lib: \"%s\"" % lib)
            libs.append(loader.load_module())
        else:
            logger.warning("Extra lib \"%s\" not found" % lib)
