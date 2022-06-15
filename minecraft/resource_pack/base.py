# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

class ResourcePack():
    """资源包的基类。"""
    def __init__(self, name):
        self.name = name
        self.lang = {}
        self.lang_en_us = {}

    def set_lang(self, lang):
        """设置游戏显示的语言。

        如果设置的语言不存在，会直接使用英语。
        
        :param lang: 某语言
        """
        pass

    def get_translation(self, name):
        """返回翻译。

        本地化字符串通过以下的顺序来获取：

        1) 用户设置的语言
        2) 英语
        3) 该函数的`name`参数

        :param name: 某翻译字符串的命名空间
        :return: 本地化的翻译
        """
        return self.lang.get(name, self.lang_en_us.get(name, name))

    def get_pack_info(self):
        """获取资源包信息。

        :return: 一个包含资源包图标和描述的元组
        """
        pass

    def get_resource(self, path):
        """获取特定的资源。
        
        :param path: 资源包路径
        :return: 返回的资源
        """
        pass
