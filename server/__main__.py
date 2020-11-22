from sys import argv

from server import console
from server import server

if __name__ == '__main__':
    if len(argv) == 1 or argv[1] == 'server':
        server.Server().start()
    elif len(argv) == 2 and argv[1] == 'console':
        console.Console().start()
    else:
        print('usage: python -m server <server|console>')
