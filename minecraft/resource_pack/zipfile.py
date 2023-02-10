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
import zipfile

from minecraft.resource_pack.base import ResourcePack
from minecraft.utils.utils import *
from pyglet.image import load as load_image


class ZipfileResourcePack(ResourcePack):
    """以zip文件作为资源包。"""

    def __init__(self, name):
        super().__init__(name)
        self.zipfile = zipfile.ZipFile(name)
        self.language = ""
        self._namelist = self.zipfile.namelist()

    def set_lang(self, lang):
        lang_file = "lang/%s.json" % lang
        if lang_file in self._namelist:
            try:
                self.lang = json.load(self.zipfile.open(lang_file))
                self.language = lang
            except:
                pass
        lang_file = "lang/en_us.json"
        if lang_file in self._namelist:
            try:
                self.lang_en_us = json.load(self.zipfile.open(lang_file))
            except:
                pass
    
    def get_all_block_textures(self):
        for name in self._namelist:
            if name.startswith("textures/block"):
                return name.split("/")[-1].rsplit(".", 1)[0]

    def get_pack_info(self):
        info = json.load(self.zipfile.open("pack.json"))
        image = load_image("pack.png", file=self.zipfile.open("pack.png"))
        return (info, image)

    def get_resource(self, path):
        if path.find("/") != -1:
            file_type = path.split("/")[0]
            if file_type == "texts":
                if (path + "-%s.txt" % self.language) in self._namelist:
                    return self.zipfile.open(path + "-%s.txt" % self.language).read()
                else:
                    return self.zipfile.open(path + "-en_us.txt" % self.language).read()
            elif file_type == "textures":
                return load_image("image.png", file=self.zipfile.open(path + ".png"))
            else:
                return json.load(self.zipfile.open(path + ".json"))
        else:
            raise FileNotFoundError("No such resource: \"%s\"" % path)
