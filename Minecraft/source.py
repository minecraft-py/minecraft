import json
from os import environ
from os.path import abspath, dirname, isdir, isfile, join
import re
import sys

from Minecraft.resource_pack import load
from Minecraft.utils.utils import *

from pyglet import resource

mcpypath = search_mcpy()
sys.path.insert(0, join(mcpypath, 'lib', VERSION['str']))
lib_path = sys.path[0]
libs = []
settings = json.load(open(join(mcpypath, 'settings.json'), encoding='utf-8'))
saves_path = join(mcpypath, 'saves')
resource_pack = None

# 解析命令行参数
for args in sys.argv:
    if args.startswith('--include='):
        for lib in args[10:].split(';'):
            if isdir(lib):
                sys.path.insert(0, lib)
                log_info("Add new lib path: '%s'" % lib)
            else:
                log_warn("Lib path '%s' not available" % lib)

for args in sys.argv:
    if args.startswith('--extlib='):
        for lib in args[9:].split(';'):
            if isdir(join(lib_path, lib)) or isfile(join(lib_path, lib + '.py')):
                log_info("Loading extra lib: '%s'" % lib)
                libs.append(__import__(lib))
            else:
                log_warn("Extra lib '%s' not found, pass" % lib)

# 检查 settings.json 的正确性
for key in ['fov', 'lang', 'resource-pack', 'use-theme']:
    if key not in settings:
        log_err("settings.json: missing '%s' key" % key)
        exit(1)

# fov 设置
if settings['fov'] < 50:
    settings['fov'] = 50
elif settings['fov'] > 100:
    settings['fov'] = 100

# resource-pack 设置
if settings['resource-pack'].startswith('default'):
    settings['resource-pack'] += '-' + VERSION['str']
resource_pack = load(settings['resource-pack'])

# lang 设置
if not resource_pack.set_lang(settings['lang']):
    log_err("settings.json: language '%s' not found" % settings['lang'])
    exit(1)

# theme 设置
if not isdir(join(dirname(__file__), 'theme', settings['use-theme'])) and settings['use-theme'] != 'ttk':
    log_err("settings.json: theme '%s' not found" % settings['use-theme'])
    exit(1)

# 读取玩家信息
if isfile(join(mcpypath, 'player.json')):
    player = json.load(open(join(mcpypath, 'player.json'), encoding='utf-8'))
    if not re.match('^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$', player['id']):
        log_err('invalid player id: %s' % player['id'])
        exit(1)
else:
    log_err('you have not registered, exit')
    exit(1)

