from os import environ
from Minecraft.launcher import *
from Minecraft.utils import *

if __name__ == '__main__':
    if 'MCPYPATH' in environ:
        try:
            import psutil
        except ModuleNotFoundError:
            pass
        else:
            for p in psutil.process_iter():
                if p.name() == 'python' and p.cmdline()[:3] == ['python', '-m', 'Minecraft']:
                    log_err('Minecraft process(pid: %d) exist, exit' % p.pid)
                    exit(1)
            else:
                MinecraftLauncher().mainloop()
    else:
        log_err("path 'MCPYPATH' not found")
