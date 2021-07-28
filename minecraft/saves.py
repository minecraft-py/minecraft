import json
from os.path import isfile, join

from minecraft.source import saves_path, player
from minecraft.utils.utils import *


def load_block(name):
    """
    读取游戏方块数据(该 API 将在下一个版本中废除)

    :param: name 存档名, 为 JSON 文件
    """
    blocks = json.load(open(join(saves_path, name, 'world.json')))
    for position, block in blocks.items():
        position = str2pos(position)
        if block == 'air':
            get_game().world.remove_block(position)
        else:
            get_game().world.add_block(position, block)

def load_level(name):
    # 读取世界信息
    return json.load(open(join(saves_path, name, 'level.json')))

def load_player(name):
    # 读取玩家数据
    if isfile(join(saves_path, name, 'players', '%s.json' % player['id'])):
        data = json.load(open(join(saves_path, name, 'players', '%s.json' % player['id'])))
        position = str2pos(data.get('position', (0, 0, 0)), True)
        if len(position) == 3:
            position = position[0], position[1], position[2]
        return {
                    'position': position,
                    'respawn': str2pos(data.get('respawn', (0, 0, 0)), True),
                    'rotation': data.get('rotation', [0, 0]),
                    'now_block': int(data.get('now_block', 0))
                }
    else:
        return {
                    'position': '0',
                    'respawn': '0',
                    'rotation': [0, 0],
                    'now_block': 0
                }

def load_window():
    # 读取游戏窗口信息
    data = json.load(open(join(search_mcpy(), 'settings.json')))['viewport']
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
    data = dict()
    if not full:
        data = json.load(open(join(saves_path, name, 'world.json')))
        for position, block in change.items():
            data[position] = block
    else:
        data = change
    json.dump(data, open(join(saves_path, name, 'world.json'), 'w+'))

def save_entity(name, data):
    # 将实体信息存入文件
    json.dump(data, open(join(saves_path, name, 'entities.json'), 'w+'))

def save_level(name, time, weather):
    # 将世界信息存入文件
    data = json.load(open(join(saves_path, name, 'level.json')))
    data['time'] = int(time)
    data['weather'] = {'now': weather['now'], 'duration': int(weather['duration'])}
    json.dump(data, open(join(saves_path, name, 'level.json'), 'w+'))


def save_player(name, position, respawn, rotation, now_block):
    # 将玩家数据存入文件
    data = {}
    data['position'] = pos2str(position)
    data['respawn'] = pos2str(respawn)
    data['rotation'] = rotation
    data['now_block'] = now_block
    json.dump(data, open(join(saves_path, name, 'players', '%s.json' % player['id']), 'w+'))

def save_window(width, height):
    data = json.load(open(join(search_mcpy(), 'settings.json')))
    data['viewport'] = {
                'width': width,
                'height': height
            }
    json.dump(data, open(join(search_mcpy(), 'settings.json'), 'w+'))
