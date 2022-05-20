import json
import re
import sys
from locale import getdefaultlocale
from os.path import isdir, isfile, join

from minecraft.resource_pack import ResourcePackManager
from minecraft.utils.utils import *

mcpypath = search_mcpy()
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
lang = ""
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
    elif args.startswith("--extlib="):
        # 如果没有下面的for循环, 那么即使有模组加载器也没有任何用处
        for lib in args[9:].split(";"):
            if isdir(join(lib_path, lib)) or isfile(join(lib_path, lib + ".py")):
                log_info("Loading extra lib: `%s`" % lib)
                libs.append(__import__(lib))
            else:
                log_warn("Extra lib `%s` not found" % lib)
