# 读取和写入游戏进度

import json

def load_block(name, add_block, remove_block):
    """
    读取游戏方块数据

    @param name 存档名, 为 JSON 文件
    @param add_block 添加方块的函数, 函数原型为 Minecraft.game.Model.add_block
    @param remove_block 移除方块的函数, 函数原型为 Minecraft.game.Model.remove_block
    """
    blocks = json.load(open('resource/save/%s' % name))
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
    pass

def save(name, change):
    """
    将游戏进度存入文件

    @param name 存档名, 为 JSON 文件
    @param change 游戏进度, 符合 JSON 标准的 python 字典
    """
    json.dump(change, open('resource/save/%s' % name, 'w+'), indent='\t')
