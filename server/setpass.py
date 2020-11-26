from hashlib import sha256
import json
from getpass import getpass
from os.path import join

from server.source import path, settings

def set_password():
    old = settings['password']
    p = getpass('old password: ')
    if sha256(p.encode()).hexdigest() != old:
        print('old password not correct')
        exit(1)
    if (new := getpass('new password: ')) == getpass('confirm: '):
        save_password(new)
        print('set new password successfully')
        exit(0)
    else:
        print('not same')
        exit(1)

def save_password(password):
    data = json.load(open(join(path['mcpypath'], 'server.json')))
    data['password'] = sha256(password.encode()).hexdigest()
    json.dump(data, open(join(path['mcpypath'], 'server.json'), 'w+'), indent='\t')
