import os
import sys
import traceback
from os import environ, getpid

import pyglet
from pyglet.gl import gl_info

from minecraft.scene import GameWindow
from minecraft.scene.start import StartScene
from minecraft.utils.test import test
from minecraft.utils.utils import *


def exist_game(p):
    # 检测是否还有其它的 python 进程运行该程序
    for process_name in ['python', 'py', 'python3', 'py3']:
        if (p.name() == process_name) and (p.cmdline()[:3] == [process_name, '-m', 'minecraft']) and (p.pid != getpid()):
            return True

def start():
    # 游戏从这里开始
    try:
        game = GameWindow(800, 600, resizable=True)
        game.add_scene('start', StartScene)
        game.switch_scene('start')
        pyglet.app.run()
    except SystemExit:
        pass
    except:
        name = time.strftime('error-%Y-%m-%d_%H.%M.%S.log')
        log_err('Catch error, saved in: log/%s' % name)
        with open(os.path.join(search_mcpy(), 'log', name), 'a+') as err_log:
            err_log.write('Minecraft version: %s\n' % VERSION['str'])
            err_log.write('python version: %s for %s\n' % ('.'.join([str(s) for s in sys.version_info[:3]]), sys.platform))
            err_log.write('pyglet version: %s(OpenGL %s)\n' % (pyglet.version, gl_info.get_version()))
            err_log.write('time: %s\n' % time.ctime())
            err_log.write('traceback:\n' + '=' * 34 + '\n')
            traceback.print_exc(file=err_log)
            err_log.write('=' * 34 + '\n')
        with open(os.path.join(search_mcpy(), 'log', 'error-latest.log'), 'w+') as latest_log:
            with open(os.path.join(search_mcpy(), 'log', name), 'r+') as err_log:
                latest_log.write(err_log.read())
        exit(1)

if __name__ == '__main__':
    try:
        import psutil
        for p in psutil.process_iter():
            if exist_game(p):
                log_err('Minecraft process(pid: %d) exist, exit' % p.pid, where='c')
                exit(1)
    except ModuleNotFoundError:
        pass
    finally:
        test()
        start()
