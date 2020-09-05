# Minecraft 资源

import json
from os import environ
from os.path import join, isfile
from pyglet import media
from Minecraft.utils import *

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
path['mcpypath'] = environ['MCPYPATH']
path['json'] = 'data/json'
path['json.lang'] = join(path['json'], 'lang')

settings = json.load(open(join(path['mcpypath'], 'settings.json')))
if isfile(join(path['mcpypath'], 'player.json')):
    player = json.load(open(join(path['mcpypath'], 'player.json')))
else:
    log_info('you have not registered, exit')
    exit(1)

path['texture'] = 'data/texture/default'
path['texture.hud'] = join(path['texture'], 'hud')
path['shaders'] = 'data/shaders'
path['save'] = join(path['mcpypath'], 'save')
path['screenshot'] = join(path['mcpypath'], 'screenshot')
path['sound'] = 'data/sound/default'

sound = {}
sound['build'] = media.load(join(path['sound'], 'build.wav'), streaming=False)
sound['destroy'] = media.load(join(path['sound'], 'destroy.wav'), streaming=False)

lang = json.load(open(join(path['json.lang'], settings['lang'] + '.json')))
