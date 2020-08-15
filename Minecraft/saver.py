# 读取和写入游戏进度

import json

def load(name, add_block, remove_block):
    """
    读取游戏进度

    @param name 存档名, 为 JSON 文件: {name}.json
    @param add_block 添加方块的函数, 函数原型为 Minecraft.min.Model.add_block
    @param remove_block 移除方块的函数, 函数原型为 Minecraft.main.Model.remove_block
    """
    pass

def save(name, change):
    """
    将游戏进度存入文件

    @param name 存档名, 为 JSON 文件: {name}.json
    @param change 游戏进度, 符合 JSON 标准的 python 字典
    """
    jason.dump(change, open('resource/%s.json' % name, 'w+'), indent='\t')
