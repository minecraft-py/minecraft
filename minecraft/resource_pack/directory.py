import json
import os

from minecraft.resource_pack.base import ResourcePack
from minecraft.utils.utils import *

import pyglet
from pyglet.image import load as load_image


class DirectoryResourcePack(ResourcePack):

    def __init__(self, name):
        super().__init__(name)
        self.base_dir = os.path.join(search_mcpy(), 'resource-pack', self.name)

    def set_lang(self, lang):
        lang_file = os.path.join(self.base_dir, 'lang', '%s.json' % lang)
        if os.path.exists(lang_file):
            try:
                self.lang = json.load(open(lang_file, 'r+', encoding='utf-8'))
                return True
            except:
                return False
        else:
            return False

    def get_pack_info(self):
        info = json.load(open(os.path.join(self.base_dir, 'pack.json'), 'r+', encoding='utf-8'))
        image = load_image('pack.png', file=open(os.path.join(self.base_dir, 'pack.png'), 'rb'))
        return (info, image)

    def get_resource(self, path):
        if path.find('/') != -1:
            file_type = path.split('/')[0]
            if file_type == 'textures':
                return load_image('image.png', file=open(os.path.join(self.base_dir, path + '.png'), 'rb'))
            else:
                return json.load(open(os.path.join(self.base_dir, path + '.json'), 'r+', encoding='utf-8'))
        else:
            raise FileNotFoundError("No such resource: '%s'" % path)
