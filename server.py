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

clients = {}

lastClient = {}

'''
usuario = {
    "username": "",
    "choices": [(),()],
    "ships": {(x,y): {
        "type": "",
        "hitted": bool,
        "ship": number, #Quantidade de peças desse navio. Para ajudar a identificar se é um vaio de 2 peças, 3 peças e afins.
    },
    "totalShipACC": 30, #Contador de navios derrubados. Serve para ajudar a acabar a partida.
    "oponent": Socket. #usar clients para acessar o usuário
}
'''

def getInfo(client_socket):
    try:
        _dict = client_socket.recv(HEADER_LENGTH)
        print(_dict)

        if not len(_dict):
            return False
        
        pick_dict = pickle.loads(_dict)

        print(pick_dict)      

        return pick_dict
    except Exception as e:
        print(e)
        return False

# def getMove(client_socket):
#     try:
#         message_header = client_socket.recv(HEADER_LENGTH)

#         if not len(message_header):
#             return False
        
#         message_length = int(message_header.decode("utf-8").strip())

#         return {"header": message_header, "data": client_socket.recv(message_length)}
#     except:
#         return False

print("Jogo vai iniciar!")
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = getInfo(client_socket)
            if user is False:
                continue
            
            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['username']}")
            if len(clients) % 2 == 0:
                clients[client_socket]['oponent'] = lastClient
                clients[lastClient]['oponent'] = client_socket
                client_socket.send(pickle.dumps({"message": f"Você tem um oponente: {clients[lastClient]['username']}"}))
                lastClient.send(pickle.dumps({"message": f"Você tem um oponente: {clients[client_socket]['username']}"}))
                lastClient.send(pickle.dumps({"turn": True}))
            else:
                client_socket.send(pickle.dumps({"message": "Ainda não há oponentes para você!"}))
            
            lastClient = client_socket
        
        else:
            message = getInfo(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['username']}")
                sockets_list.remove(notified_socket)
                clients[notified_socket]["oponent"].send({"message": f"{clients[notified_socket]['username']} saiu da partida."})
                del clients[notified_socket]
                continue

            user = clients[notified_socket]

            if "move" in message:
                move = message["move"]

                #TODO: Validar Jogadas repetidas no cliente e retirar isso.
                if move not in user["choices"]:
                    user["choices"].append(move)
                
                print(f"O usuário {user['username']} jogou na posição {move}")
                
                oponent = clients[user["oponent"]]
                oponent_socket = user["oponent"]
                
                if(move in oponent["ships"]):
                    oponent["ships"][move]["hitted"] = True
                    oponent["totalShipACC"] -= 1

                    if oponent["totalShipACC"] == 0: #Se o jogo acabou
                        notified_socket.send(
                            pickle.dumps(
                                {"message": f"Você derrubou todos os navios de {oponent['username']}. Parabéns! Você venceu!",
                                "end": True}
                            )
                        )
                        oponent_socket.send(
                            pickle.dumps(
                                {
                                    "message": f"{user['username']} derrubou todos os seus navios. Infelizmente, você perdeu!",
                                    "end": True
                                }
                            )
                        )  
                    else:
                        #Por enquanto, vai ser uma vez de cada, independente de acertou ou não, mas se quiser mudar isso, basta mandar um "turn"
                        notified_socket.send(
                            pickle.dumps(
                                {"message": f"Você acertou um navio {oponent['ships'][move]['type']}"}
                            )
                        )
                        oponent_socket.send(
                            pickle.dumps(
                                {
                                    "message": f"{user['username']} acertou um navio {oponent['ships'][move]['type']}",
                                    "turn": True
                                }
                            )
                        )             
                else:
                    notified_socket.send(
                        pickle.dumps(
                            {"message": "Água! Você errou seu tiro!"}
                        )
                    )
                    oponent_socket.send(
                        pickle.dumps(
                            {
                                "message": f"{user['username']} atirou na água.",
                                "turn": True
                            }
                        )
                    )
                #Lógica do jogo.

            # for client_socket in clients:
            #     if client_socket != notified_socket:
            #         client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
        
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]