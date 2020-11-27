import json
from os.path import join
from sys import platform
import time

from server.utils import *

path = {}
path['mcpypath'] = search_mcpy()
path['save'] = join(path['mcpypath'], 'save', '_server')

settings = json.load(open(join(path['mcpypath'], 'server.json'), encoding='utf-8'))
for key in ['spawn_position', 'password', 'port']:
    if key not in settings:
        log_err("server.json: missing '%s' key" % key)
        exit(1)
