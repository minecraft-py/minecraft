#!/usr/bin/env python3

from json import dump, load
from os import chmod, environ, mkdir, makedirs, path, system
from re import match
from shutil import copyfile, copytree, rmtree
from sys import executable, platform, argv
from stat import S_IXUSR
import uuid
from zipfile import ZipFile

VERSION = '0.3.2'

def main():
    # 下载依赖项
    install()
    # 注册玩家
    register_user()
    # 复制运行所需的文件
    copy()
    # 创建启动脚本
    gen_script()
    # 完成!
    print('[Done]')

def copy():
    print('[(3/3) Copy lib]')
    MCPYPATH = search_mcpy()
    if not path.isdir(MCPYPATH):
        mkdir(MCPYPATH)
    install_json('settings.json')
    for name in ['log', 'saves', 'screenshot', 'resource-pack']:
        if not path.isdir(path.join(MCPYPATH, name)):
            mkdir(path.join(MCPYPATH, name))
    if not path.isdir(path.join(MCPYPATH, 'lib', VERSION)):
        makedirs(path.join(MCPYPATH, 'lib', VERSION))
    if path.isdir(path.join(MCPYPATH, 'resource-pack', 'default-%s' % VERSION)):
        rmtree(path.join(MCPYPATH, 'resource-pack', 'default-%s' % VERSION))
    ZipFile(path.join(get_file('data'), 'default.zip')).extractall(path.dirname(__file__))
    copytree(get_file('default'), path.join(MCPYPATH, 'resource-pack', 'default-%s' % VERSION))
    rmtree(get_file('default'))

def gen_script():
    if '--gen-script':
        print('[(4/3) Generate startup script]')
        script = str()
        name = get_file('run.sh')
        if platform.startswith('win'):
            name = get_file('run.bat')
            script += '@echo off\n'
        else:
            script += '#!/usr/bin/env sh\n'
        script += 'cd %s\n' % path.dirname(get_file('install.py'))
        script += '%s -m Minecraft\n' % executable
        with open(name, 'w+') as f:
            f.write(script)
            print("startup script is '%s'" % name)
        if not platform.startswith('win'):
            chmod(name, S_IXUSR)

def get_file(f):
    # 返回文件目录下的文件名
    return path.abspath(path.join(path.dirname(__file__), f))

def install():
    if '--skip-install-requirements' not in argv:
        print('[(1/3) Install requirements]')
        pip = executable + ' -m pip'
        if '--hide-output' in argv:
            code = system('%s install -U -r %s >> %s' % (pip, get_file('requirements.txt'), path.devnull))
        else:
            code = system('%s install -U -r %s' % (pip, get_file('requirements.txt')))
        if code != 0:
            print('pip raise error code: %d' % code)
            exit(1)
        else:
            print('install successfully')
    else:
        print('[(1/3) Skip install requirements]')

def install_json(f):
    MCPYPATH = search_mcpy()
    source = load(open(path.join(get_file('data'), f)))
    target = {}
    if path.isfile(path.join(MCPYPATH, f)):
        target = load(open(path.join(MCPYPATH, f)))
    else:
        target = {}
    for k, v in source.items():
        if k not in target or not isinstance(target[k], type(v)):
            target[k] = v
    dump(target, open(path.join(MCPYPATH, f), 'w+'))

def register_user():
    # 注册
    if '--skip-register' not in argv:
        print('[(2/3) Register]')
        MCPYPATH = search_mcpy()
        if not path.isdir(MCPYPATH):
            mkdir(MCPYPATH)
        if not path.isfile(path.join(MCPYPATH, 'player.json')):
            player_id = str(uuid.uuid4())
            print('Your uuid is %s, do not change it' % player_id)
            player_name = ''
            while not match(r'^([a-z]|[A-Z]|_)\w+$', player_name):
                player_name = input('Your name: ')
            dump({'id': player_id, 'name': player_name}, open(path.join(MCPYPATH, 'player.json'), 'w+'), indent='\t')
            print('Regsitered successfully, you can use your id to play multiplayer game!')
        else:
            print('You have regsitered!')
    else:
        print('[(2/3) Skip regsiter]')

def search_mcpy():
    # 搜索文件存储位置
    if 'MCPYPATH' in environ:
        MCPYPATH = environ['MCPYPATH']
    elif platform == 'darwin':
        MCPYPATH = path.join(path.expanduser('~'), 'Library', 'Application Support', 'mcpy')
    elif platform.startswith('win'):
        MCPYPATH = path.join(path.expanduser('~'), 'mcpy')
    else:
        MCPYPATH = path.join(path.expanduser('~'), '.mcpy')
    return MCPYPATH

if __name__ == '__main__':
    main()
