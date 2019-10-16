import socket
import select
import pickle
import traceback
import algoritmos as alg

HEADER_LENGTH = 4096
IP = "127.0.0.1"
PORT = 1234

partidas = {}

# Todas as coordenadas de todos os navios
coordenadas = {}

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

def get_navio(coordenada, ships):
    for ship in ships:
        if coordenada in ship['coordinates']:
            return ship['name']

# Retorna um dicionário contendo todas as coordenadas de cada um dos navios
def get_coordenadas(ships):

    all_coordenadas = dict()
    names = []
    [names.append(ship_name) for ship_name in ships.keys()] # Obtém as chaves dos navios pois estas serão usadas como nome para eles
    i = 0
    for ship in ships:
        inicio = tuple(ship['start'])
        fim = tuple(ship['end'])
        ship['coordinates'] = alg.generate_coordinate(inicio, fim)
        ship['state'] = len(ship['coordinates']) # indica quantas posições do navio ainda não foram derrubadas
        # Adiciona a chave dos navios como sendo um "nome" para ele
        ship['name'] = names[i]
        i = i + 1
    
    return ships

# Adiciona as coordenadas do usuário no dicionário coordenadas
def set_coordinates(username, user_ships):
    
    super coordenadas
    coordenadas[username] = {}
    coordenadas[username]['all'] = []
    coordenadas[username]['hitted'] = {}

    for ships in user_ships.itens():
         coordenadas[username]['all'].extend(ships['coordinates'])

    # Adiciona o estado de "False"
    [coordenadas[username]['hitted'][coordenada] = False for coordenada in coordenadas[username]]


print("Servidor iniciado. O jogo está prestes a começar.")

while True:

    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:

        if notified_socket == server_socket:

            client_socket, client_address = server_socket.accept()

            # Obtém os dados da mensagem aqui
            user = get_info(client_socket)

            if not user:
                continue
            
            # Adiciona o usuário à lista de sockets
            sockets_list.append(client_socket)

            clients[client_socket] = user

            print('O usuário {} acabou de se conectar'.format(user['username']))
            
            if not len(clients) % 2 == 0:
                print('Ainda não há jogadores o suficiente para iniciar o jogo.')
            
            else:

                clients[client_socket]['oponent'] = lastClient
                clients[lastClient]['oponent'] = client_socket

                # Obtém as coordenadas dos navios
                clients[client_socket]['ships'] = get_coordenadas(clients[client_socket]['message']['ships'])
                clients[lastClient]['ships'] = get_coordenadas(clients[lastClient]['message']['ships'])

                # Armazena as coordenadas dos navios dos usuários
                set_coordinates(clients[client_socket]['message']['username'], clients[client_socket]['ships'])
                set_coordinates(clients[lastClient]['message']['username'], clients[lastClient]['ships'])
                
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
                                    'message': 'Oponente {} encontrado. O jogo irá iniciar'.format(clients[client_socket]['username']),
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
                
                oponent = clients[user['oponent']]
                oponent_socket = user['oponent']

                # Verifica se a jogada está dentro das coordenadas do oponente
                if move in coordenadas[oponent]['all']:

                    coordenadas[oponent]['hitted'][move] = True # Esta coordenada foi atingida
                    coordenadas[oponent]['all'].pop(index(move)) # Remove da lista do usuário

                    #if move in clients[oponent]['ships']['coordinates'].items():

                    #if oponent["totalShipACC"] == 0: #Se o jogo acabou
                    if coordenadas[oponent]['all'] == None:
                        notified_socket.send(
                            pickle.dumps(
                                 {
                                    'message': 'Você derrubou todos os navios de {}. Parabéns, você venceu!'.format(oponent['username']),
                                    'code': 0,
                                    'type': 'end-game'
                                }))
                                
                        oponent_socket.send(
                            pickle.dumps(
                                 {
                                    'message': 'Todos os seus navios foram derrubados por {}. Infelizmente, você perdeu!'.format(user['username']),
                                    'code': 0,
                                    'type': 'end-game'
                                }))
                    else:
                        # Avisa ao usuário que ele atingiu o navio oponente
                        notified_socket.send(
                            pickle.dumps(
                                 {
                                    'message': 'Você acertou um navio {}.'.format(get_navio(move, clients[oponent]['ships'])),
                                    'code': 1,
                                    'type': 'game'
                                }))
                        # Avisa o oponente que um navio seu foi acertado
                        oponent_socket.send(
                            pickle.dumps(
                                 {
                                    'message': 'O usuário {} acertou o navio.'.format(user['username'], get_navio(move, clients[oponent]['ships'])),
                                    'code': 0,
                                    'type': 'game'
                                }))                             
                else:
                    # Avisa ao usuário que ele errou o palpite dele
                    notified_socket.send(
                        pickle.dumps(
                            {
                                'message': 'Água! Você errou seu tiro!',
                                'code': 0,
                                'type': 'game'
                        })) 
                    # Avisa ao oponente que o adversário errou o palpite e que é sua vez de jogar
                    oponent_socket.send(
                        pickle.dumps(
                            {
                                'message': 'O oponente acertou na água!',
                                'code': 1,
                                'type': 'game'
                        })) 
        
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
