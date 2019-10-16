from algoritmos import read_ships, generate_coordinate, ships_validation
from ast import literal_eval as make_tuple

import socket
import errno
import sys
import pickle

HEADER_LENGTH = 4096
IP = "127.0.0.1"
PORT = 1234
SHIPS = read_ships()

# if ships_validation(SHIPS): # apenas validação
if ships_validation(SHIPS,verbose=True): # validação com comentários
    print('Navios carregados com sucesso')
else:
    exit()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = input("Username: ")
choices = set()

isMyTurn = False
gameover = False

toSend = pickle.dumps(
    {
        "username": username,
        "ships": SHIPS
    }
)

client_socket.send(toSend) # envia dicionário com nome e navios, seguindo o template do ships.json

while True:
    if gameover: break

    while isMyTurn: # executa enquanto for seu turno e não enviar a jogada
        move = make_tuple(input("Insira as coordenadas (x,y): ")) # leia e converte a jogada em tupla

        # se o movimento existe, possui apenas dois valores (x e y) e ainda não foi realizado
        if move and len(move)==2 and not move in choices:
            choices.add(move)
            client_socket.send(pickle.dumps({"move": move})) # envia a jogada
            isMyTurn = False
        else:
            print("\nCoordenadas inválidas!\n")
    
    # CONTINUAR DAQUI
    try:
        while True:
            #receive things
            data = client_socket.recv(HEADER_LENGTH)

            if(not data): continue

            pick_dict = pickle.loads(data)

            if not pick_dict:
                print("connection closed by the server")
                sys.exit()

            if "turn" in pick_dict:
                isMyTurn = pick_dict["turn"]
            
            if "end" in pick_dict:
                if pick_dict["end"]:
                    gameover = True
                    break

            if "message" in pick_dict:
                print(pick_dict['message'])

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        pass