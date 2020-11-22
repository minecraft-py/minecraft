import socket

class Console():

    def __init__(self):
        pass

    def start(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(('localhost', 32768))
        self.socket.send('console'.encode())
        while True:
            data = self.socket.recv(1024).decode()
            if data == 'refused':
                break
            print(data)
            command = input('> ')
            if command == 'stop':
                self.socket.close()
                break
            self.socket.send(command.encode())
