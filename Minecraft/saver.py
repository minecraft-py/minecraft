# 读取和写入游戏进度

import json
from os.path import join
from Minecraft.source import path

def load_block(name, add_block, remove_block):
    """
    读取游戏方块数据(该 API 将在下一个版本中废除)

    :param: name 存档名, 为 JSON 文件
    :param: add_block 添加方块的函数, 函数原型为 Minecraft.game.Model.add_block
    :param: remove_block 移除方块的函数, 函数原型为 Minecraft.game.Model.remove_block
    """
    blocks = json.load(open(join(path['save'], '%s/%s.world' % ((name,) * 2))))
    for position, block in blocks.items():
        position = tuple([int(i) for i in position.split(' ')])
        if block == 'air':
            remove_block(position)
        else:
            add_block(position, block)

def load_player(name):
    """
    读取玩家数据

    :param: name 存档名, 为 JSON 文件
    """
    data = json.load(open(join(path['save'], '%s/%s.player' % ((name,) * 2))))
    return {
                'position': tuple([float(i) for i in data['position'].split(' ')]),
                'respawn': tuple([float(i) for i in data['respawn'].split(' ')]),
                'now_block': int(data['now_block'])
            }

def save_block(name, change, full=True):
    """
    将方块数据存入文件

    :param: name 存档名, 为 JSON 文件
    :param: change 方块数据, 符合 JSON 标准的 python 字典
    :param: full 是否全部写入
    """
    if not full:
        data = json.load(open(join(path['save'], '%s/%s' % ((name,) * 2))))
        for position, block in change.items():
            data[position] = block
    else:
        data = change
    json.dump(data, open(join(path['save'], '%s/%s.world' % ((name,) * 2)), 'w+'), indent='\t')

def save_player(name, position, respawn, now_block):
    """将玩家数据存入文件
    :param: name 存档名, 为 JSON 文件
    """
    data = {}
    data['position'] = ' '.join([('%.1f' % i) for i in position])
    data['respawn'] = ' '.join([('%.1f' % i) for i in respawn])
    data['now_block'] = now_block
    json.dump(data, open(join(path['save'], '%s/%s.player' % ((name,) * 2)), 'w+'), indent='\t')
