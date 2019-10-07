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

ships = {
    nav2_1_1 : {
        "type": "tipo1",
        "hitted": False,
        "ship": 2,
    },
    nav2_1_2 : {
        "type": "tipo1",
        "hitted": False,
        "ship": 2,
    },
    nav2_2_1 : {
        "type": "tipo1",
        "hitted": False,
        "ship": 2,
    },
    nav2_2_2 : {
        "type": "tipo1",
        "hitted": False,
        "ship": 2,
    },
    nav2_3_1 : {
        "type": "tipo1",
        "hitted": False,
        "ship": 2,
    },
    nav2_3_2 : {
        "type": "tipo1",
        "hitted": False,
        "ship": 2,
    },
    nav2_4_1 : {
        "type": "tipo1",
        "hitted": False,
        "ship": 2,
    },
    nav2_4_2 : {
        "type": "tipo1",
        "hitted": False,
        "ship": 2,
    }
}

isMyTurn = False

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

toSend = pickle.dumps(
    {
        "username": username,
        "ships": ships,
        "oponent": False,
        "choices": [],
        "totalShipACC": 30
    }
)
client_socket.send(toSend)

gameover = False

while True:

    if gameover: break

    if(isMyTurn):
        #TODO: Fazer validacao
        move = input("Insira as coordenadas: ")

        if move:
            client_socket.send(pickle.dumps({"move": move}))
            isMyTurn = False
    
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

#TODO: Lógica do término do jogo!
