import socket
import threading
import datetime
import json
from scripts.gather_configs import GatherConfigs
from scripts.gather_profiles import GatherProfiles
from scripts.logging import Log

class Server:
    # Get configurations
    def get_configs(self):
        print("Loading configs")
        return GatherConfigs().get_configs()
        
    # Get default profile
    def get_default_profile(self):
        print("Loading default profile")
        return GatherProfiles().get_default_profile()

    # Get client profiles
    def get_profiles(self):
        print("Loading user profiles")
        return GatherProfiles().get_user_profiles()

    # Handle new connection
    def new_connection(self, client_socket, address):
        message = client_socket.recv(1024).decode('ascii')
        if message == "zmgdw":
            client_socket.send("zmgdw".encode("ascii"))
            print(f'Handshake seccsessfull with {address}')
            Log.log(f'Handshake seccsessfull with {address}', Log.SUCCSESS)
            self.manage_client(client_socket, address)
        else:
            print(f'Handshake fail with {address}')
            Log.log(f'Handshake fail with {address}', Log.WARNING)

    # Manage client
    def manage_client(self, client_socket, address):
        who = self.who_is(client_socket)
        if who[0] == 'client':
            self.post_data(client_socket, self.profiles[who[1]]["list_of_programs"])
        elif who[0] == 'admin':
            print("got admin")
        elif who[0] == 'new':
            print(f'Generating new profile for user {address}')
            Log.log(f'Generating new profile for user {address}', Log.SUCCSESS)
            self.profiles[who[1]] = {
                "last_time_used": str(datetime.datetime.now().date()),
                "role": "client",
                "list_of_programs": self.default_profile["user"]["list_of_programs"] 
            }
            json.dump(self.profiles, open("./profiles/profiles.json", "w"))
            self.post_data(client_socket, self.profiles[who[1]]["list_of_programs"])
        else:
            print(f'Can\'t decide who from {address}')
            Log.log(f'Can\'t decide who from {address}', Log.WARNING)
        
    # Get information of client
    def who_is(self, client_socket):
        who = client_socket.recv(1024).decode('ascii')
        if who in self.profiles.keys():
            return (self.profiles[who]["role"], who)
        else:
            return ("new", who)
    
    # Post data to client
    def post_data(self, client_socket, list_of_programs):
        print(f'Sending list of programs to client')
        Log.log(f'Sending list of programs to client', Log.SUCCSESS)
        client_socket.send(str(list_of_programs).encode('ascii'))
        client_socket.close()
    
    # Start server service
    def start_server(self):
        print("Opening socket")
        self.main_socket = socket.socket()
        self.port = int(self.configs['sockets']['client_socket'])
        self.main_socket.bind(('', self.port))
        print(f'Socket opened, port - {self.port}')
        Log.log(f'Socket opened, port = {self.port}', Log.SUCCSESS)
        self.main_socket.listen(24)
        self.run = True
        while self.run:
            connection, address = self.main_socket.accept()
            print(f'New connection from {address}')
            Log.log(f'New connection from {address}', Log.SUCCSESS)
            thread = threading.Thread(target=self.new_connection, args=(connection, address))
            thread.start()
        self.main_socket.close()

    # Initiate the server
    def __init__(self):
        print("Starting server")
        Log.log("----- Starting server -----", Log.SUCCSESS)
        
        try:
            self.configs = self.get_configs()
            Log.log("Loaded configs", Log.SUCCSESS)
        except:
            print("Failed to load configs")
            Log.log("Failed to load configs", Log.FAIL)
            exit()

        try:
            self.default_profile = self.get_default_profile()
            Log.log("Loaded default profile", Log.SUCCSESS)
        except:
            print("Failed to load default profile")
            Log.log("Failed to load default profile", Log.FAIL)
            exit()
        
        try:
            self.profiles = self.get_profiles()
            Log.log("Loaded clients' profiles", Log.SUCCSESS)
        except:
            print("Failed to load clients profiles")
            Log.log("Failed to load clients profiles", Log.FAIL)
            exit()
        
        try:
            self.start_server()
        except:
            Log.log("Faildet to start server", Log.FAIL)
            exit()


if __name__ == "__main__":
    Server()