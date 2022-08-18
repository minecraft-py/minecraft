# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

class ResourcePack():
    """The base class of resource pack."""

    def __init__(self, name):
        self.name = name
        self.lang = {}
        self.lang_en_us = {}

    def set_lang(self, lang):
        """Set language."""
        pass

    def get_translation(self, name):
        """Return translation.

        本地化字符串通过以下的顺序来获取：

        1. language chose by player
        2. English
        3. argument `name`
        """
        return self.lang.get(name, self.lang_en_us.get(name, name))

    def get_pack_info(self):
        """Get resource pack information."""
        pass

    def get_resource(self, path):
        """Get resource in `path`."""
        pass
