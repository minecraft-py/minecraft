from sys import argv

from server import console
from server import server

if __name__ == '__main__':
    if argv[1] == 'server':
        server.Server().start()
    elif argv[1] == 'console':
        console.Console().start()
