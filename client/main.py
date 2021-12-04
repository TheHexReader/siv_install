import socket
import os
import random
import ast
import json

class Client:
    
    PATH_TO_KEY = './profile.key'
    key_length = 128

    socket = socket.socket()
    server_port = 42069
    hello_message = 'zmgdw'

    alpha = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    local_net = "192.168.0."
    server_address = ""
    
    def __init__(self):
        print("Starting the program.")
        self.find_server()
        self.handshake()
        self.get_key()
        self.recive_profile()
        self.install_programs()
    
    def handshake(self):
        self.socket.send(self.hello_message.encode('ascii'))
        if self.socket.recv(1024).decode('ascii') != self.hello_message:
            print('Wrong message from server')
            self.socket.close()
            return False
        return True

    def get_key(self):
        if os.path.isfile(self.PATH_TO_KEY):
            key = open(self.PATH_TO_KEY, 'r').read()
        else:
            key = self.generate_key()
        self.key = key

    def generate_key(self):
        key = ''
        for _ in range(self.key_length):
            key += self.alpha[random.randrange(0, len(self.alpha))]
        open(self.PATH_TO_KEY, 'w').write(key)
        return key

    def recive_profile(self):
        self.socket.send(self.key.encode('ascii'))
        self.list_of_programms = ast.literal_eval(self.socket.recv(4096).decode('ascii'))
        print('Recived profile.')

    def install_programs(self):
        pass

    def find_server(self):
        print('Trying to connect to last used ip.')
        try:
            self.socket.connect((json.load(open("./config.json", 'r'))['server']['ip'], self.server_port))
            
            return
        except Exception as e:
            print(f'Failed to connect to last used server. Error:{e} Finding new.')
        for i in range(1,256):
            print(f"Trying to connect to {self.local_net}{i}:{self.server_port}", end='\r')
            try:
                self.socket.connect((f'{self.local_net}{i}', self.server_port))
            except Exception:
                continue
            print(f"Found server on {self.local_net}{i}:{self.server_port}, saving for future connections.")
            open('./config.json', 'w').write(json.dumps({"server":{"ip":f'{self.local_net}{i}'}}))
            return
        print('\nCan\'t find server, exiting.')
        exit()

if __name__ == "__main__":
    Client()
