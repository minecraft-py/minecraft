# Minecraft 资源

import json
from os.path import join
from pyglet import media

def tex_coord(x, y, n=4):
    #返回纹理正方形绑定的顶点
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

def tex_coords(top, bottom, side):
    # 返回纹理正方形的顶面, 底面, 侧面
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result

def tex_coords_all(top, bottom, side0, side1, side2, side3):
    # 返回纹理正方形所有的面
    # 同 tex_coords() 类似, 但是要传入全部的四个侧面
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side0, side1 = tex_coord(*side0), tex_coord(*side1)
    side2, side3 = tex_coord(*side2), tex_coord(*side3)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side0)
    result.extend(side1)
    result.extend(side2)
    result.extend(side3)
    return result

block = {}
block['grass'] = tex_coords((1, 0), (0, 1), (0, 0))
block['dirt'] = tex_coords((0, 1), (0, 1), (0, 1))
block['sand'] = tex_coords((1, 1), (1, 1), (1, 1))
block['stone'] = tex_coords((0, 2), (0, 2), (0, 2))
block['log'] = tex_coords((1, 2), (1, 2), (2, 2))
block['leaf'] = tex_coords((3, 1), (3, 1), (3, 1))
block['brick'] = tex_coords((2, 0), (2, 0), (2, 0))
block['plank'] = tex_coords((3, 0), (3, 0), (3, 0))
block['craft_table'] = tex_coords((0, 3), (3, 0), (1, 3))
block['bedrock'] = tex_coords((2, 1), (2, 1), (2, 1))
block['undefined'] = tex_coords((3, 2), (3, 2), (3, 2))

# 从这里到文件末尾处, 你可以更改资源文件或目录, 以指向不同的位置
path = {}
path['lang'] = join('resource/json/lang', 'en' + '.json')
path['texture'] = 'resource/texture/default'
path['hud'] = join(path['texture'], 'hud')
path['save'] = 'resource/save'
path['sound'] = 'resource/sound/default'

sound = {}
sound['build'] = media.load(join(path['sound'], 'build.wav'), streaming=False)
sound['destroy'] = media.load(join(path['sound'], 'destroy.wav'), streaming=False)

lang = json.load(open(path['lang']))
