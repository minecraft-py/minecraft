from sys import platform, version_info

from pyglet import version
from pyglet.gl import gl_info

from minecraft.utils.utils import *

def test():
    # 在游戏最开始时输出的调试信息, 在报告 issue 时应该附带这些信息
    log_info("** Start Minecraft-in-python **")
    log_info("This is not official Minecraft product.", where="c")
    log_info("Not approved by or associated with Mojang.", where="c")
    log_info("Operation system: %s" % platform)
    log_info("Python version: %s" % ".".join([str(s) for s in version_info[:3]]))
    log_info("Pyglet version: %s(OpenGL %s)" % (version, gl_info.get_version()))
    log_info("Minecraft-in-python version: %s(data version: %s)" % (VERSION["str"], VERSION["data"]))
