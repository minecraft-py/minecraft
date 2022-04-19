import os
from os import environ, getpid

from minecraft.utils.utils import *
from minecraft.utils.test import test

def exist_game(p):
    # 检测是否还有其它的 python 进程运行该程序
    for process_name in ['python', 'py', 'python3', 'py3']:
        if (p.name() == process_name) and (p.cmdline()[:3] == [process_name, '-m', 'minecraft']) and (p.pid != getpid()):
            return True

if __name__ == '__main__':
    try:
        import psutil
        for p in psutil.process_iter():
            if exist_game(p):
                log_err('Minecraft process(pid: %d) exist, exit' % p.pid, where='c')
                exit(1)
    except ModuleNotFoundError:
        pass
    else:
        test()
        # 游戏从这里开始运行
