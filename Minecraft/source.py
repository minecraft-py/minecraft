import json
from os import environ
from os.path import isfile, join
import re

from Minecraft.utils.utils import *
from register import search_mcpy

from pyglet import resource

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

path = {}

path['mcpypath'] = search_mcpy()
path['json'] = 'data/json'
path['json.lang'] = join(path['json'], 'lang')

settings = json.load(open(join(path['mcpypath'], 'settings.json'), encoding='utf-8'))
# 检查 settings.json 的正确性
for key in ['lang']:
    if key not in settings:
        log_err("settings.json: missing '%s' key" % key)
        exit(1)
if not isfile(join(path['json.lang'], settings['lang'] + '.json')):
    log_err("settings.json: language '%s' not found" % settings['lang'])
    exit(1)

if isfile(join(path['mcpypath'], 'player.json')):
    player = json.load(open(join(path['mcpypath'], 'player.json'), encoding='utf-8'))
    if not re.match('^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$', player['id']):
        log_err('invalid player id: %s' % player['id'])
        exit(1)
else:
    log_err('you have not registered, exit')
    exit(1)

path['texture'] = join(path['mcpypath'], 'texture/default')
path['texture.hud'] = join(path['texture'], 'hud')
path['texture.ui'] = join(path['texture'], 'ui')
path['shaders'] = 'data/shaders'
path['save'] = join(path['mcpypath'], 'save')
path['screenshot'] = join(path['mcpypath'], 'screenshot')

lang = json.load(open(join(path['json.lang'], settings['lang'] + '.json'), encoding='utf-8'))
