from algoritmos import read_ships, generate_coordinate, ships_validation, validMove
from ast import literal_eval as make_tuple

import socket
import errno
import sys
import pickle
import random

HEADER_LENGTH = 4096
IP = "127.0.0.1"
PORT = 1234
SHIPS = read_ships("./Tabuleiros/ships"+str(random.randint(1, 6))+".json") # indique um arquivo customizado se quiser

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
        move = None
        try:
            move = make_tuple(input("Insira as coordenadas (x,y): ")) # lê e converte a jogada em tupla
            # se o movimento existe, se possui apenas dois valores (x e y) e ainda não foi realizado
            if move in choices:
                print("\nJogada já realizada!\n")
            elif not validMove(move):
                print("\nCoordenadas inválidas!\n")
            else:
                choices.add(move)
                client_socket.send(pickle.dumps({"move": move})) # envia a jogada
                isMyTurn = False
        except:
            print("Isso nem é uma coordenada!")
            
    try:
        while True:
            #receive things
            data = client_socket.recv(HEADER_LENGTH)

            if(not data): continue

            pick_dict = pickle.loads(data)

            if not pick_dict:
                print("connection closed by the server")
                sys.exit()
            
            # print(pick_dict)
            code = pick_dict.get("code")
            params = pick_dict.get("params")

            if code == 2:
                isMyTurn = params["turn"] if params.get("turn") else False
                print("Foi encontrado um oponente para você\n")
                if isMyTurn:
                    print("É sua vez!\n")
                else:
                    print("É a vez do oponente! Aguarde sua vez!\n")

            elif code == 3:
                print("Oponente abandonou a partida, conexão perdida!")
                exit()
            elif code == 4:
                print("Você atingiu um navio do oponente. Jogue novamente!")
                isMyTurn = True
            elif code == 5:
                print("Oponente atingiu um navio. Ainda é a vez do oponente!")
                isMyTurn = False
            elif code == 6:
                print("Tiro na água. Vez do oponente.")
                isMyTurn = False
            elif code == 7:
                print("Oponente atingiu a água. É a sua vez!")
                isMyTurn = True
            elif code == 8:
                print("Você abateu um navio do tipo:",params.get("type"))
                isMyTurn = True
            elif code == 9:
                print("Você teve um navio abatido do tipo:",params.get("type"))
                isMyTurn = False
            elif code == 10:
                print("Você é o vencedor, parabéns!")
                exit()
            elif code == 11:
                print("Você é o perdedor, tente novamente!")
                exit()

            if code == 1 or not isMyTurn:
                print("\nAguardando oponente")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        pass
