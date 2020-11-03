#!/usr/bin/env python3

from os import environ, mkdir, path, system
from shutil import copyfile, copytree
from register import register_user

print("[Install Requirements]")
system("pip install -r requirements.txt")

print("[Register]")
register_user()

print("\n[Copy lib]")
for lib in [
            [['data', 'json', 'settings.json'], ['settings.json']],
            [['data', 'json', 'window.json'], ['window.json']], 
            [['data', 'texture'], ['texture', 'default']]
            ]:
    if '.' in lib[-1][-1]:  # copy file
        copyfile(path.join(*lib[0]), path.join(environ['MCPYPATH'], *lib[1]))
    else:  # copy dir
        copytree(path.join(*lib[0]), path.join(environ['MCPYPATH'], *lib[1]))

for xdir in ['screenshot', 'save']:
    if not path.isdir(xdir):
        mkdir(path.join(environ['MCPYPATH'], xdir))

print("[Done]")
