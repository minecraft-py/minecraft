from sys import argv

from server import console
from server import server
from server.utils import *

if __name__ == '__main__':
    if len(argv) == 1 or argv[1] == 'server':
        server.Server().start()
    elif len(argv) == 2 and argv[1] == 'console':
        console.Console().start()
    elif len(argv) == 2 and argv[1] == 'help':
        print('Minecraft server version %s' % VERSION)
        print('usage: python -m server <server|console|help>\n')
        print('arguments:')
        print('  server  - start a server(default)')
        print('  console - run a console')
        print('  help    - show this help')
    else:
        print('usage: python -m server <server|console|help>')
