#!/usr/bin/env python3

from json import dump
from os import environ, path, mkdir
from re import match
from sys import platform
import uuid

def search_mcpy():
    if 'MCPYPATH' in environ:
        MCPYPATH = environ['MCPYPATH']
    elif platform.startswith('win'):
        MCPYPATH = path.join(path.expanduser('~'), 'mcpy')
    else:
        MCPYPATH = path.join(path.expanduser('~'), '.mcpy')
    return MCPYPATH

def register_user(): 
    if 'MCPYPATH' not in environ:
        environ['MCPYPATH'] = search_mcpy()
    if not path.isdir(environ['MCPYPATH']):
        mkdir(environ['MCPYPATH'])
    if not path.isfile(path.join(environ['MCPYPATH'], 'player.json')):
        player_id = str(uuid.uuid4())
        print('Your uuid is %s, do not change it' % player_id)
        player_name = ''
        while not match(r'^([a-z]|[A-Z]|_)\w+$', player_name):
            player_name = input('Your name: ')
        dump({'id': player_id, 'name': player_name}, open(path.join(environ['MCPYPATH'], 'player.json'), 'w+'), indent='\t')
        print('Regsitered successfully, you can use your id to play multiplayer game!')
    else:
        print('You have regsitered!')

if __name__ == '__main__':
    register_user()
