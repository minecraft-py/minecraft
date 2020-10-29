#!/usr/bin/python3

from json import dump
from os import environ, path
from random import randint
from re import match
from time import time
import uuid

if __name__ == '__main__':
    if 'MCPYPATH' in environ:
        if not path.isfile(path.join(environ['MCPYPATH'], 'player.json')):
            player_id = str(uuid.uuid4())
            print('Your uuid is %s, do not change it' % player_id)
            player_name = ''
            while not match(r'^([a-z]|[A-Z]|_)\w+$', player_name):
                player_name = input('Your name: ')
            dump({'id': player_id, 'name': player_name}, open(path.join(environ['MCPYPATH'], 'player.json'), 'w+'),
                    indent='\t')
            print('Regsitered successfully, you can use your id to play multiplayer game!')
        else:
            print('You have regsitered!')
    else:
        print("'$MCPYPATH' not found")
