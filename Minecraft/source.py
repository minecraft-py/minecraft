import json
from os import environ
from os.path import abspath, dirname, isdir, isfile, join
import re

from Minecraft.utils.utils import *

from pyglet import resource

path = {}

path['mcpypath'] = search_mcpy()
path['data'] = 'data'
path['json'] = join(path['data'], 'json')
path['json.lang'] = join(path['json'], 'lang')

settings = json.load(open(join(path['mcpypath'], 'settings.json'), encoding='utf-8'))
# 检查 settings.json 的正确性
for key in ['fov', 'lang', 'use-theme']:
    if key not in settings:
        log_err("settings.json: missing '%s' key" % key)
        exit(1)
# fov 设置
if settings['fov'] < 50:
    settings['fov'] = 50
elif settings['fov'] > 100:
    settings['fov'] = 100
# lang 设置
if not isfile(join(path['json.lang'], settings['lang'] + '.json')):
    log_err("settings.json: language '%s' not found" % settings['lang'])
    exit(1)
# theme 设置
if not isdir(join(dirname(__file__), 'theme', settings['use-theme'])) and settings['use-theme'] != 'ttk':
    log_err("settings.json: theme '%s' not found" % settings['use-theme'])
    exit(1)

if isfile(join(path['mcpypath'], 'player.json')):
    player = json.load(open(join(path['mcpypath'], 'player.json'), encoding='utf-8'))
    if not re.match('^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$', player['id']):
        log_err('invalid player id: %s' % player['id'])
        exit(1)
else:
    log_err('you have not registered, exit')
    exit(1)

path['log'] = join(path['mcpypath'], 'log')
path['texture'] = join(path['mcpypath'], 'texture', 'default')
path['texture.hud'] = join(path['texture'], 'hud')
path['texture.ui'] = join(path['texture'], 'ui')
path['shaders'] = join(path['data'], 'shaders')
path['save'] = join(path['mcpypath'], 'save')
path['screenshot'] = join(path['mcpypath'], 'screenshot')

lang = json.load(open(join(path['json.lang'], settings['lang'] + '.json'), encoding='utf-8'))
