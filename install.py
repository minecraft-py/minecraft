#!/usr/bin/env python3

import sys
from os import path, mkdir
from shutil import copyfile, copytree 
import pip
import runpy
from register import register_user, environ

print("[Install Requirements]")
sys.argv = ['pip', 'install', '-r', 'requirements.txt']
runpy.run_module("pip", run_name="__main__")

print("[Register]")
register_user()

print("\n[Copy lib]")
for lib in [
            [['data', 'json', 'settings.json'], ['settings.json']],
            [['data', 'json', 'window.json'], ['window.json']], 
            [['data', 'texture'], ['texture', 'default']]
            ]:
    if '.' in lib[-1][-1]:  # Copy file
        copyfile(path.join(*lib[0]), path.join(environ['MCPYPATH'], *lib[1]))
    else:  # Copy dir
        copytree(path.join(*lib[0]), path.join(environ['MCPYPATH'], *lib[1]))


for xdir in ['screenshot', 'save']:
    if not path.isdir(xdir):
        mkdir(path.join(environ['MCPYPATH'], xdir))


print("[Done]")