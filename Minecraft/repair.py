import json
from os.path import join
from time import ctime

from Minecraft.source import path

def repair_archive(name):
    # 修复世界信息
    info = json.load(open(join(path['save'], name, 'info.json')))
    data = {'seed': hash(ctime()), 'type': 'normal', 'day': 0, 'time': 4}
    for key, value in data.items():
        if key not in info:
            info[key] = value
    else:
        json.dump(info, open(join(path['save'], name, 'info.json'), 'w+'), indent='\t')
    # 修复玩家数据
    player = json.load(open(join(path['save'], name, 'player.json')))
    data = {'position': '0 4 0', 'respawn': '0 4 0', 'now_block': 0}
    for key, value in data.items():
        if key not in player:
            player[key] = value
    else:
        json.dump(player, open(join(path['save'], name, 'player.json'), 'w+'), indent='\t')
