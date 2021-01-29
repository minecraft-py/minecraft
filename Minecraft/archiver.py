import json
from os.path import join

from Minecraft.source import path
from Minecraft.utils.utils import *

def load_block(name, add_block, remove_block):
    """
    读取游戏方块数据(该 API 将在下一个版本中废除)

    :param: name 存档名, 为 JSON 文件
    :param: add_block 添加方块的函数, 函数原型为 Minecraft.world.World.add_block
    :param: remove_block 移除方块的函数, 函数原型为 Minecraft.world.World.remove_block
    """
    blocks = json.load(open(join(path['save'], name, 'world.json')))
    for position, block in blocks.items():
        position = str2pos(position)
        if block == 'air':
            remove_block(position)
        else:
            add_block(position, block)

def load_info(name):
    # 读取世界信息
    return json.load(open(join(path['save'], name, 'info.json')))

def load_player(name):
    # 读取玩家数据
    data = json.load(open(join(path['save'], name, 'player.json')))
    position = str2pos(data.get('position', (0, 0, 0)), True)
    if len(position) == 3:
        position = position[0], position[1] + 1, position[2]
    return {
                'position': position,
                'respawn': str2pos(data.get('respawn', (0, 0, 0)), True),
                'rotation': data.get('rotation', (0, 0)),
                'now_block': int(data.get('now_block', 1))
            }

def load_window():
    # 读取游戏窗口信息
    data = json.load(open(join(path['mcpypath'], 'settings.json')))['viewport']
    return {
                'width': data['width'],
                'height': data['height']
            }

def save_block(name, change, full=True):
    """
    将方块数据存入文件

    :param: change 方块数据, 符合 JSON 标准的 python 字典
    :param: full 是否全部写入
    """
    if not full:
        data = json.load(open(join(path['save'], name, 'world.json')))
        for position, block in change.items():
            data[position] = block
    else:
        data = change
    json.dump(data, open(join(path['save'], name, 'world.json'), 'w+'))

def save_info(name, day, time):
    # 将世界信息存入文件
    data = json.load(open(join(path['save'], name, 'info.json')))
    data['day'] = day
    data['time'] = time
    json.dump(data, open(join(path['save'], name, 'info.json'), 'w+'))


def save_player(name, position, respawn, rotation, now_block):
    # 将玩家数据存入文件
    data = {}
    data['position'] = pos2str(position)
    data['respawn'] = pos2str(respawn)
    data['rotation'] = rotation
    data['now_block'] = now_block
    json.dump(data, open(join(path['save'], name, 'player.json'), 'w+'))

def save_window(width, height):
    data = json.load(open(join(path['mcpypath'], 'settings.json')))
    data['viewport'] = {
                'width': width,
                'height': height
            }
    json.dump(data, open(join(path['mcpypath'], 'window.json'), 'w+'))
