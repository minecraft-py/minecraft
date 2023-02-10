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

import json
import os

from minecraft.resource_pack.base import ResourcePack
from minecraft.utils.utils import *
from pyglet.image import load as load_image


class DirectoryResourcePack(ResourcePack):
    """文件系统中的资源包。"""

    def __init__(self, name):
        super().__init__(name)
        self.base_dir = name
        self.language = ""

    def set_lang(self, lang):
        lang_file = os.path.join(self.base_dir, "lang", "%s.json" % lang)
        if os.path.exists(lang_file):
            try:
                self.lang = json.load(open(lang_file, "r+", encoding="utf-8"))
                self.language = lang
            except:
                pass
        lang_file = os.path.join(self.base_dir, "lang", "en_us.json")
        if os.path.exists(lang_file):
            try:
                self.lang_en_us = json.load(
                    open(lang_file, "r+", encoding="utf-8"))
            except:
                pass
    
    def get_all_block_textures(self):
        for f in os.listdir(os.path.join(self.base_dir, "textures", "block")):
            yield f.rsplit(".", 1)[0]

    def get_pack_info(self):
        info = json.load(
            open(os.path.join(self.base_dir, "pack.json"), "r+", encoding="utf-8"))
        image = load_image("pack.png", file=open(
            os.path.join(self.base_dir, "pack.png"), "rb"))
        return (info, image)

    def get_resource(self, path):
        if path.find("/") != -1:
            file_type = path.split("/")[0]
            if file_type == "texts":
                if os.path.isfile(os.path.join(self.base_dir, path + "-%s.txt" % self.language)):
                    return open(os.path.join(self.base_dir, path + "-%s.txt" % self.language), "r+").read()
                else:
                    return open(os.path.join(self.base_dir, path + "-en_us.txt"), "r+").read()
            elif file_type == "textures":
                return load_image("image.png", file=open(os.path.join(self.base_dir, path + ".png"), "rb"))
            else:
                return json.load(open(os.path.join(self.base_dir, path + ".json"), "r+", encoding="utf-8"))
        else:
            raise FileNotFoundError("No such resource: \"%s\"" % path)
