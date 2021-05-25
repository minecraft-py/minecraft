import os
from zipfile import is_zipfile

from minecraft.resource_pack.directory import DirectoryResourcePack
from minecraft.resource_pack.zipfile import ZipfileResourcePack
from minecraft.utils.utils import *

def load(name):
    resource_pack_dir = os.path.join(search_mcpy(), 'resource-pack')
    if os.path.exists(os.path.join(resource_pack_dir, name)):
        if os.path.isdir(os.path.join(resource_pack_dir, name)) and (not name.endswith('.zip')):
            return DirectoryResourcePack(name)
        if os.path.isfile(os.path.join(resource_pack_dir, name)) and is_zipfile(os.path.join(resource_pack_dir, name)):
            return ZipfileResourcePack(name)
        else:
            log_err("Not a zipfile: '%s', exit" % os.path.join(resource_pack_dir, name))
            exit(1)
    else:
        log_err("No such file or directory: '%s', exit" % os.path.join(resource_pack_dir, name))
        exit(1)
