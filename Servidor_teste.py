import socket
import select
import pickle
import traceback

HEADER_LENGTH = 4096
IP = "127.0.0.1"
PORT = 1234

tipos_navios = {}

# Todas as coordenadas de todos os navios
jogador_1 = []
jogador_2 = []

# Coordenadas em seus respectivos navios
navios_1 = {}
navios_2 = {}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]

clients = {}
lastClient = {}

def get_info(client_socket):
    try:
        _dict = client_socket.recv(HEADER_LENGTH)
        if not len(_dict):
            return False
        pick_dict = pickle.loads(_dict)
        return pick_dict
    except Exception as e:
        print('Erro ao descompactar arquivo:')
        traceback.print_exc() 

print("Servidor iniciado. O jogo está prestes a começar.")

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = get_info(client_socket)
            if not user:
                continue
            
            sockets_list.append(client_socket)

            clients[client_socket] = user

            print('O usuário {} acabou de se conectar'.format(user['username']))
            
            if not len(clients) % 2 == 0:
                print('Ainda não há jogadores o suficiente para iniciar o jogo.')
            else:
                clients[client_socket]['oponent'] = lastClient
                clients[lastClient]['oponent'] = client_socket
                
                client_socket.send(
                        pickle.dumps(
                                {
                                    'message': 'Oponente {} encontrado. O jogo irá iniciar'.format(clients[lastClient]['username']),
                                    'code': 0,
                                    'type': 'connection'
                                }))
    
                lastClient.send(
                        pickle.dumps(
                                {
                                    'message': 'Oponente {} encontrado. O jogo irá iniciar'.format(clients[lastClient]['username']),
                                    'code': 0,
                                    'type': 'connection'
                                }))
    
                lastClient.send(
                        pickle.dumps(
                                {
                                    'message': 'Sua vez de jogar',
                                    'code': 1,
                                    'type': 'game'
                                }))
    
            lastClient = client_socket
        
        else:  
            message = get_info(notified_socket)

            if not message:
                print('Conexão encerrada com {}'.format(clients[notified_socket]['username']))
                sockets_list.remove(notified_socket)
                clients[notified_socket]["oponent"].send(
                        pickle.dumps(
                                {
                                    "message": '{} saiu da partida.'.format(clients[notified_socket]['username']),
                                    "code": 0,
                                    "type": 'inform'
                                }))
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            
            # Se o tipo de mensagem for game com o código 1, quer dizer que o jogador
            # fez um jogada e será necessário verificar a chave "message" 
            if message['type'] == 'game' and message['code'] == 1:
                move = message["message"] # A posição virá neste campo
                print('O usuário {} jogou na posição {}'.format(user['username'], move))
                
                #oponent = clients[user["oponent"]]
                oponent_socket = user["oponent"]
                
                if move in oponent["ships"]:
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
