# 读取和写入游戏进度

import json

def load_block(name, add_block, remove_block):
    """
    读取游戏方块数据

    @param name 存档名, 为 JSON 文件
    @param add_block 添加方块的函数, 函数原型为 Minecraft.game.Model.add_block
    @param remove_block 移除方块的函数, 函数原型为 Minecraft.game.Model.remove_block
    """
    blocks = json.load(open('resource/save/%s/%s.world' % (name, name)))
    for position, block in blocks.items():
        position = tuple([int(i) for i in position.split(' ')])
        if block == 'air':
            remove_block(position)
        else:
            add_block(position, block)

def load_player(name):
    """
    读取玩家数据

    @param name 存档名, 为 JSON 文件
    """
    data = json.load(open('resource/save/%s/%s.player' % (name, name)))
    return tuple([float(i) for i in data['position'].split(' ')]), data['bag']

def save_block(name, change):
    """
    将方块数据存入文件

    @param name 存档名, 为 JSON 文件
    @param change 方块数据, 符合 JSON 标准的 python 字典
    """
    data = json.load(open('resource/save/%s/%s' % (name, name)))
    for position, block in change.items():
        data[position] = block
    json.dump(data, open('resource/save/%s/%s.world' % (name, name), 'w+'), indent='\t')

def save_player(name, position, bag):
    """将玩家数据存入文件
    @param name 存档名, 为 JSON 文件
    """
    data = {}
    data['position'] = ' '.join([str(i) for i in position])
    data['bag'] = bag
    json.dump(data, open('resource/save/%s/%s.player' % (name, name), 'w+'), indent='\t')
