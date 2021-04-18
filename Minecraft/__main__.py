from os import getpid, environ
from sys import platform

from Minecraft.launcher import *
from Minecraft.utils import *

def exist(p):
    for process_name in ['python', 'py', 'python3', 'py3']:
        if p.name() == process_name and p.cmdline()[:3] == [process_name, '-m', 'Minecraft'] and p.pid != getpid():
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
        if (environ.get('DISPLAY') is not None) and (platform == 'linux'):
            MinecraftLauncher().mainloop()
        else:
            log_err('$DISPLAY not found')
