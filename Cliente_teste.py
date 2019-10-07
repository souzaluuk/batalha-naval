import socket
import select
import errno
import sys
import pickle

HEADER_LENGTH = 4096
IP = "127.0.0.1"
PORT = 1234
username = str(input("Insira um nome de usuário: "))
NUM_NAVIOS = 4
navios = dict()

def get_coordenadas_navio(self, inicio, fim):
    #TO DO: Verificar a reta que forma o navio 

def write(self, text):
    # Apenas um print mais informativo (dizendo qual usuário está falando)
    print('[{}]: {}'.format(username, text))    

for i in range(NUM_NAVIOS):

    inicio = input("Insira a coordenada inicial no formato (x,y): ")
    fim = input("Insira a coordenada final no formato (x,y): ")

    navios = 'id_{i}': {
        'inicio': isinstance(inicio, tuple),
        'fim': isinstance(fim, tuple),
        'coordenadas': [], # TO DO: obter a partir do get_coordenadas_navio
        'type': '', # TO DO: Verificar a partir do objeto retornado em get_coordenadas_navio
        'hitted': False
    }

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)
data = {
    'user': username,
    'navios': navios
}
client_socket.send(pickle.dumps(data))

"""
    TO DO: O cliente agora deve ficar 'escutando o servidor' para agir conforme ele instruir.
    Ele deve esperar um dicionário com 3 chaves, sendo estas:
    {'turn': True (ou False), 'end_game': False  } 
"""

message = pickle.loads(RESPOSTA_SERVIDOR)
jogadas = set()

if message['end_game'] == False:
    if message['turn'] == True:

        # Se o jogo não terminou e é meu turno, então, eu jogo!
        jogada = input('Insira uma coordenada para atacar: ')
        # Tenta adicionar a coordenada na lista de jogadas, mas, só aceita
        # coordenadas que são uma tupla e que não sejam repetidas
        try:
            jogadas.append(isinstance(jogada, tuple))
        except Exception as e:
            self.write('Jogada inválida.')
    
else:
    # TO DO: Encerra a comunicação       