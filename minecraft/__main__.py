import atexit
import os
import sys
import traceback
from os import remove
from os.path import isfile, join

import pyglet
from pyglet.gl import gl_info

from minecraft.scene import GameWindow
from minecraft.scene.start import StartScene
from minecraft.utils.opengl import setup_opengl
from minecraft.utils.test import test
from minecraft.utils.utils import *


def start():
    # 游戏从这里开始
    try:
        setup_opengl()
        game = GameWindow(800, 600, resizable=True)
        game.add_scene("start", StartScene)
        game.switch_scene("start")
        pyglet.app.run()
    except SystemExit:
        pass
    except:
        # 这里负责处理不知道谁引发的异常
        name = time.strftime("error-%Y-%m-%d_%H.%M.%S.log")
        log_err("Catch error, saved in: log/%s" % name)
        with open(os.path.join(search_mcpy(), "log", name), "a+") as err_log:
            err_log.write("Minecraft version: %s\n" % VERSION["str"])
            err_log.write("Python version: %s for %s\n" % (".".join([str(s) for s in sys.version_info[:3]]), sys.platform))
            err_log.write("Pyglet version: %s(OpenGL %s)\n" % (pyglet.version, gl_info.get_version()))
            err_log.write("Time: %s\n" % time.ctime())
            err_log.write("Traceback:\n\n")
            traceback.print_exc(file=err_log)
        with open(os.path.join(search_mcpy(), "log", "error-latest.log"), "w+") as latest_log:
            with open(os.path.join(search_mcpy(), "log", name), "r+") as err_log:
                latest_log.write(err_log.read())

if __name__ == "__main__":
    if isfile(join(search_mcpy(), "mcpy.lock")):
        # 检测程序是否重复启动
        log_info("Minecrft-in-python is running now!", where="c")
    else:
        with open(join(search_mcpy(), "mcpy.lock"), "w+") as f:
            pass
        # 注册退出处理器
        atexit.register(on_exit)
        # 打印运行环境等基本信息
        test()
        # 开始游戏
        start()
        if isfile(join(search_mcpy(), "mcpy.lock")):
            remove(join(search_mcpy(), "mcpy.lock"))
