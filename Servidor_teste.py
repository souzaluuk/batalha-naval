import socket
import select
import pickle

HEADER_LENGTH = 4096
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]

clients = set()

message = client_socket.recv(HEADER_LENGTH)
content = pickle.loads(message)

clients.append(content['user'])

