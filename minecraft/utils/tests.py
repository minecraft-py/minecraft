from sys import platform, version_info

from minecraft.utils.utils import *

from pyglet import version
from pyglet.gl import gl_info

log_info('Start minecraft %s' % VERSION['str'])
log_info('Operation system: %s' % platform)
log_info('python version: %s' % '.'.join([str(s) for s in version_info[:3]]))
log_info('pyglet version: %s(OpenGL %s)' % (version, gl_info.get_version()))
log_info('Minecraft version: %s(data version: %s)' % (VERSION['str'], VERSION['data']))
