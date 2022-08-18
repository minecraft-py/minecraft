# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

import json
import re
import sys
from locale import getdefaultlocale
from os import pathsep
from os.path import isdir, isfile, join
from pkgutil import find_loader
from zipfile import is_zipfile

from minecraft.resource_pack import ResourcePackManager
from minecraft.utils.utils import *

mcpypath = search_mcpy()
sys.path.insert(0, join(mcpypath, "lib", VERSION["str"]))
lib_path = sys.path[0]
libs = []
settings = json.load(open(join(mcpypath, "settings.json"), encoding="utf-8"))

# Set resource pack
resource_pack = ResourcePackManager()
if (settings.get("resource-pack") is None) or (len(settings.get("resource-pack", [])) == 0):
    resource_pack.add("${default}")
else:
    for pack in settings["resource-pack"]:
        resource_pack.add(pack)

# Set language.
if settings.get("lang", "${auto}") == "${auto}":
    lang = getdefaultlocale()[0].lower()
else:
    lang = settings.get("lang", "en_us").lower()
resource_pack.set_lang(lang)

# Set fov, range from 50 to 100, default is 70.
settings["fov"] = max(50, min(100, settings.get("fov", 70)))

# Read player information.
if isfile(join(mcpypath, "player.json")):
    player = json.load(open(join(mcpypath, "player.json"), encoding="utf-8"))
    if not re.match("^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$", player["id"]):
        log_err("Invalid player id: %s" % player["id"])
        exit(1)
else:
    log_err("You have not registered, exit")
    exit(1)

# Parse command line arguments.
for args in sys.argv:
    if args.startswith("--include="):
        # Add some paths to sys.path, zip file is also supported.
        for lib in args[10:].split(pathsep):
            if isdir(lib) or (isfile(lib) and is_zipfile(lib)):
                sys.path.insert(0, lib)
                log_info("Add new lib path: `%s`" % lib)
            else:
                log_warn("Lib path \"%s\" is not available" % lib)
    elif args.startswith("--extlib="):
        for lib in args[9:].split(pathsep):
            if (loader := find_loader(lib)) is not None:
                log_info("Loading extra lib: \"%s\"" % lib)
                libs.append(loader.load_module())
            else:
                log_warn("Extra lib \"%s\" not found" % lib)
