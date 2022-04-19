import json
import re
import sys
from os import environ
from os.path import abspath, dirname, isdir, isfile, join

from pyglet import resource

from minecraft.utils.utils import *

mcpypath = search_mcpy()
sys.path.insert(0, join(mcpypath, "lib", VERSION["str"]))
lib_path = sys.path[0]
libs = []
settings = json.load(open(join(mcpypath, "settings.json"), encoding="utf-8"))

# fov 设置
settings["fov"] = max(50, min(100, settings.get("fov", 70)))

# 读取玩家信息
if isfile(join(mcpypath, "player.json")):
    player = json.load(open(join(mcpypath, "player.json"), encoding="utf-8"))
    if not re.match("^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$", player["id"]):
        log_err("invalid player id: %s" % player["id"])
        exit(1)
else:
    log_err("you have not registered, exit")
    exit(1)

# 解析命令行参数
for args in sys.argv:
    if args.startswith("--include="):
        for lib in args[10:].split(";"):
            if isdir(lib):
                sys.path.insert(0, lib)
                log_info("Add new lib path: `%s`" % lib)
            else:
                log_warn("Lib path `%s` is not available" % lib)

for args in sys.argv:
    if args.startswith("--extlib="):
        for lib in args[9:].split(";"):
            if isdir(join(lib_path, lib)) or isfile(join(lib_path, lib + ".py")):
                log_info("Loading extra lib: `%s`" % lib)
                libs.append(__import__(lib))
            else:
                log_warn("Extra lib `%s` not found" % lib)

