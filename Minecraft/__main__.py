from os import environ
from Minecraft.launcher import *
from Minecraft.utils import *

if __name__ == '__main__':
    if 'MCPYPATH' in environ:
        MinecraftLauncher().mainloop()
    else:
        log_err("path 'MCPYPATH' not found")
