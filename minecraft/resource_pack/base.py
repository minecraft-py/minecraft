# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

class ResourcePack():

    def __init__(self, name):
        self.name = name
        self.lang = {}
        self.lang_en_us = {}

    def set_lang(self, lang):
        pass

    def get_translation(self, name):
        # 返回对应语言的翻译, 否则返回英语翻译
        return self.lang.get(name, self.lang_en_us.get(name, name))

    def get_pack_info(self):
        # 返回一个 (pack.json, pack.png) 
        pass

    def get_resource(self, path):
        # path 为用 "/" 分隔的路径名
        # lang/*     - *.json(不建议)
        # sounds/*   - *.ogg
        # text/*     - *.txt
        # textures/* - *.png
        pass
