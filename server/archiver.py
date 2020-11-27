import json
import os

from Minecraft.source import path
from Minecraft.utils import *

def new_world(seed='minecraft', type_='flat'):
    if not os.path.isdir(path['save']):
        os.mkdir(path['save'])
        os.mkdir(os.path.join(path['save'], 'players'))
        info = {'seed': hash(seed), 'type': type_, 'time': 4}
        json.dump(info, open(os.path.join(path['save'], 'info.json'), 'w+'), indent='\t')
        json.dump({}, open(os.path.join(path['save'], 'world.json'), 'w+'), indent='\t')
    else:
        pass
