from sys import platform, version_info

from minecraft.utils.utils import *

from pyglet import version
from pyglet.gl import gl_info

log_info('** Start Minecraft-in-python **')
log_info('This is not official Minecraft product.')
log_info('Not approved by or associated with Mojang.')
log_info('Operation system: %s' % platform, where='l')
log_info('python version: %s' % '.'.join([str(s) for s in version_info[:3]]), where='l')
log_info('pyglet version: %s(OpenGL %s)' % (version, gl_info.get_version()), where='l')
log_info('Minecraft-in-python version: %s(data version: %s)' % (VERSION['str'], VERSION['data']), where='l')
