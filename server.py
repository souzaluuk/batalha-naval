import socket
import select
import pickle

HEADER_LENGTH = 10
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
    "escolhas": [(),()],
    "navios": {(x,y): {
        "tipo": "",
        "acertado": bool,
        "navio": number,
    },
    "totalNavioACC": 30,
    "adversario": Socket. usar clients para acessar o usuário
}
'''

def getInfo(client_socket):
    try:
        header = client_socket.recv(HEADER_LENGTH)

        if not len(header):
            return False
        
        length = int(header.decode("utf-8").strip())

        coisa = client_socket.recv(length)
        coisapick = pickle.loads(coisa)

        print(coisapick)

        coisapick["header"] = header
        

        return coisapick
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
            else:
                client_socket.send(pickle.dumps({"message": "Ainda não há oponentes para você!"}))
            
            lastClient = client_socket
        
        else:
            message = getInfo(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['username']}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f"O usuário {user['username']} jogou na posição {message['data']}")
            #Lógica do jogo.

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
        
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]