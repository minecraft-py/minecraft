import os
from os import getpid, environ

from minecraft.start import *
from minecraft.utils import *

def exist(p):
    for process_name in ['python', 'py', 'python3', 'py3']:
        if p.name() == process_name and p.cmdline()[:3] == [process_name, '-m', 'minecraft'] and p.pid != getpid():
            return True

if __name__ == '__main__':
    try:
        import psutil
        for p in psutil.process_iter():
            if exist(p):
                log_err('Minecraft process(pid: %d) exist, exit' % p.pid)
                exit(1)
    except ModuleNotFoundError:
        pass
    finally:
        StartScreen().mainloop()
