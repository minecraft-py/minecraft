# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

import json
import zipfile

from minecraft.resource_pack.base import ResourcePack
from minecraft.utils.utils import *
from pyglet.image import load as load_image


class ZipfileResourcePack(ResourcePack):

    def __init__(self, name):
        # 以压缩文件作为资源包
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
                return True
            except:
                return False
        else:
            return False

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
