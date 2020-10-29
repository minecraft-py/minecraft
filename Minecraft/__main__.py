from os import environ, getpid
from Minecraft.launcher import *
from Minecraft.utils import *

def exist(p):
    for process_name in ['python', 'py', 'python3', 'py3']:
        if p.name() == process_name and p.cmdline()[:3] == [process_name, '-m', 'Minecraft'] and p.pid != getpid():
            return True

if __name__ == '__main__':
    if 'MCPYPATH' in environ:
        try:
            import psutil
            for p in psutil.process_iter():
                if exist(p):
                    log_err('Minecraft process(pid: %d) exist, exit' % p.pid)
                    exit(1)
        except ModuleNotFoundError:
            MinecraftLauncher().mainloop()
    else:
        log_err("path 'MCPYPATH' not found")
