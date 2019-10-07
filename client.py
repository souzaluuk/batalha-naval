import socket
import select
import errno
import sys
import pickle

HEADER_LENGTH = 4096
IP = "127.0.0.1"
PORT = 1234

username = input("Username: ")
# TODO: validar o formato.
nav2_1_1 = input("Insira a coordenada 1 formato: (x,y) navio 1 que ocupa 2 posições: ")
nav2_1_2 = input("Insira a coordenada 2 formato: (x,y) navio 1 que ocupa 2 posições: ")
nav2_2_1 = input("Insira a coordenada 1 formato: (x,y) navio 2 que ocupa 2 posições: ")
nav2_2_2 = input("Insira a coordenada 2 formato: (x,y) navio 2 que ocupa 2 posições: ")
nav2_3_1 = input("Insira a coordenada 1 formato: (x,y) navio 3 que ocupa 2 posições: ")
nav2_3_2 = input("Insira a coordenada 2 formato: (x,y) navio 3 que ocupa 2 posições: ")
nav2_4_1 = input("Insira a coordenada 1 formato: (x,y) navio 4 que ocupa 2 posições: ")
nav2_4_2 = input("Insira a coordenada 2 formato: (x,y) navio 4 que ocupa 2 posições: ")

isMinhaVez = False

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

toSend = pickle.dumps(
    {
        "username": username,
        "ships": [
            nav2_1_1, nav2_1_2, nav2_2_1, nav2_2_2, nav2_3_1, nav2_3_2, nav2_4_1, nav2_4_2
        ],
        "oponent": False,
        "choices": [],
        "totalShipACC": 30
    }
)
sending_header = f"{len(toSend):<{10}}".encode('utf-8')
client_socket.send(sending_header + toSend)

data_arr = []

while True:
    # if(isMinhaVez):
    #     message = input("Insira as coordenadas.")

    #     if message:
    #         message = message.encode('utf-8')
    #         message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    #         client_socket.send(message_header + message)
    #         isMinhaVez = False
    
    try:
        while True:
            #receive things
            data = client_socket.recv(HEADER_LENGTH)
            # print(data)
            # if data:
            #     data_arr.append(data)
            #     data = False
            #     continue
            
            # mounted = b"".join(data_arr)
            if not data: continue

            mess_dict = pickle.loads(data)
            if not mess_dict:
                print("connection closed by the server")
                sys.exit()

            print(mess_dict['message'])


            # username = pickle.loads(client_socket.recv(username_length).decode('utf-8'))

            # message_header = client_socket.recv(HEADER_LENGTH)
            # message_length = int(message_header.decode("utf-8").strip())
            # message = client_socket.recv(message_length).decode('utf-8')

            isMinhaVez = True

            # print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        pass
