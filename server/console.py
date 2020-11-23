import readline
import socket

from server.source import settings


class Console():

    def __init__(self):
        pass

    def start(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(('localhost', settings['port']))
        self.socket.send('console'.encode())
        receive = self.socket.recv(1024).decode()
        if receive == 'refused':
            print('connection refused')
        elif receive == 'welcome':
            while True:
                data = self.socket.recv(1024).decode()
                print(data)
                try:
                    command = input('> ')
                except:
                    self.socket.send('exit'.encode())
                    self.socket.close()
                    print()
                    break
                else:
                    if command == 'exit':
                        self.socket.send('exit'.encode())
                        self.socket.close()
                        break
                    elif command == 'stop':
                        self.socket.send('stop'.encode())
                        self.socket.close()
                        break
                    self.socket.send(command.encode())
