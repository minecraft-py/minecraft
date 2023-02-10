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

class ResourcePack():
    """资源包的基类。"""

    def __init__(self, name):
        self.name = name
        self.lang = {}
        self.lang_en_us = {}

    def set_lang(self, lang):
        """设置语言。"""
        pass

    def get_all_block_textures(self):
        pass

    def get_translation(self, name):
        """返回翻译

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
