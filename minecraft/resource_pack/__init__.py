import os
from zipfile import is_zipfile

from minecraft.resource_pack.directory import DirectoryResourcePack
from minecraft.resource_pack.zipfile import ZipfileResourcePack
from minecraft.utils.utils import *


class ResourcePackManager():

    def __init__(self):
        self._packs = list()

    def add(self, name):
        resource_pack_dir = os.path.join(search_mcpy(), 'resource-pack')
        if os.path.exists(os.path.join(resource_pack_dir, name)) or (name == '(default)'):
            if os.path.isdir(os.path.join(resource_pack_dir, name)) and (not name.endswith('.zip')):
                self._packs.append(DirectoryResourcePack(os.path.join(resource_pack_dir, name)))
                return
            if name == '(default)':
                self._packs.append(DirectoryResourcePack(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))))
                return
            if os.path.isfile(os.path.join(resource_pack_dir, name)) and is_zipfile(os.path.join(resource_pack_dir, name)):
                self._packs.append(ZipfileResourcePack(os.path.join(resource_pack_dir, name)))
            else:
                log_err("Not a zipfile: '%s', exit" % os.path.join(resource_pack_dir, name))
                exit(1)
        else:
            log_err("No such file or directory: '%s', exit" % os.path.join(resource_pack_dir, name))
            exit(1)

    def set_lang(self, lang):
        for pack in self._packs:
            pack.set_lang(lang)
        return True

    def get_translation(self, name):
        return self._packs[0].get_translation(name)

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
            raise FileNotFoundError("No such resource: '%s'" % path)

    def make_block_atlas(self):
        pass
