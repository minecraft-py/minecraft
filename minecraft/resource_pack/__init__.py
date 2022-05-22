import os
from zipfile import is_zipfile

from minecraft.resource_pack.directory import DirectoryResourcePack
from minecraft.resource_pack.zipfile import ZipfileResourcePack
from minecraft.utils.utils import *


class ResourcePackManager():

    def __init__(self):
        # 资源包管理器
        self._packs = []

    def add(self, name):
        name.replace("${game}", os.path.join(search_mcpy(), "resource-pack"))
        if os.path.exists(os.path.join(name)) or (name == "${default}"):
            if os.path.isdir(os.path.join(name)) and (not name.endswith(".zip")):
                self._packs.append(DirectoryResourcePack(name))
            elif name == "${default}":
                self._packs.append(DirectoryResourcePack(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))))
            elif os.path.isfile(name) and is_zipfile(name):
                self._packs.append(ZipfileResourcePack(name))
            else:
                log_warn("Not a zipfile: \"%s\"" % name)
        else:
            log_warn("No such file or directory: \"%s\"" % name)

    def set_lang(self, lang):
        for pack in self._packs:
            pack.set_lang(lang)
        return True

    def get_translation(self, name):
        for pack in self._packs:
            if pack.get_translation(name) != name:
                return pack.get_translation(name)
        else:
            return name

    def get_pack_info(self):
        l = list()
        for pack in self._packs:
            l.append(pack.get_pack_info())
        return l

    def get_resource(self, path):
        for pack in self._packs:
            try:
                return pack.get_resource(path)
            except:
                pass
        else:
            raise FileNotFoundError("No such resource: \"%s\"" % path)

    def make_block_atlas(self):
        pass
