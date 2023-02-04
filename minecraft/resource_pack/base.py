# Copyright 2020-2023 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

class ResourcePack():
    """资源包的基类。"""

    def __init__(self, name):
        self.name = name
        self.lang = {}
        self.lang_en_us = {}

    def set_lang(self, lang):
        """设置语言。"""
        pass

    def get_translation(self, name):
        """Return translation.

        本地化字符串通过以下的顺序来获取：

        1. 玩家选择的语言
        2. 英语
        3. `name`参数
        """
        return self.lang.get(name, self.lang_en_us.get(name, name))

    def get_pack_info(self):
        """获取资源包信息。"""
        pass

    def get_resource(self, path):
        """在`path`中获取资源。"""
        pass
