import socket
import select
import pickle
import algoritmos as alg

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
    "all_coordinates": (x,y): "type_x-index",
    "ships": {"type_x": [
        {
            "coordinates": [(x,y),(a,b)]
            "type": x
        },
        {
            "coordinates": [(d,f),(t,s)]
            "type": x
        }
    ]
        
    },
    "oponent": Socket. #usar clients para acessar o usuário
}
'''

def getInfo(client_socket):
    try:
        _dict = client_socket.recv(HEADER_LENGTH)

        if not len(_dict):
            return False
        
        pick_dict = pickle.loads(_dict)  

        return pick_dict
    except Exception as e:
        print(e)
        return False

def get_coordinates(ships):

    all_coordinates = dict()

    for name, types in ships.items():
        for ship in range(len(types)):

            ship_index = f"{name}-{ship}"

            start = tuple(types[ship]['start'])
            ending = tuple(types[ship]['end'])

            coordinates = alg.generate_coordinate(start, ending)

            for coordinate in range(len(coordinates)):
                all_coordinates[coordinates[coordinate]] = ship_index

            del types[ship]['start']
            del types[ship]['end']
            types[ship]['coordinates'] = coordinates
    
    return [ships, all_coordinates]

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

            user["ships"], user["all_coordinates"] = get_coordinates(user["ships"])

            clients[client_socket] = user

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['username']}")
            print(user)

            if len(clients) % 2 == 0:
                clients[client_socket]['oponent'] = lastClient
                clients[lastClient]['oponent'] = client_socket
                client_socket.send(
                    pickle.dumps(
                        {
                            "code": 2,
                            "params": {
                                "oponent": clients[lastClient]['username'],
                                "turn": False
                            }
                        }
                    )
                )
                lastClient.send(
                    pickle.dumps(
                        {
                            "code": 2,
                            "params": {
                                "oponent": clients[client_socket]['username'],
                                "turn": True
                            }
                        }
                    )
                )
            else:
                client_socket.send(pickle.dumps({"code": 1}))
            
            lastClient = client_socket
        
        else:
            message = getInfo(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['username']}")
                sockets_list.remove(notified_socket)
                clients[notified_socket]["oponent"].send(pickle.dumps({"code": 3}))
                del clients[notified_socket]
                continue

            user = clients[notified_socket]

            if "move" in message:
                move = message["move"]
                
                print(f"O usuário {user['username']} jogou na posição {move}")
                
                oponent = clients[user["oponent"]]
                oponent_socket = user["oponent"]
                
                if(move in oponent["all_coordinates"]):
                    ship_index = oponent["all_coordinates"].pop(move).split("-")
                    oponent["ships"][ship_index[0]][int(ship_index[1])]["coordinates"].remove(move)
                    print(ship_index)
                    print(oponent["ships"][ship_index[0]][int(ship_index[1])]["coordinates"])
                    if len(oponent["all_coordinates"]) == 0: #Se o jogo acabou
                        notified_socket.send(pickle.dumps({"code": 10}))
                        oponent_socket.send(pickle.dumps({"code": 11}))  
                    else:
                        if len(oponent["ships"][ship_index[0]][int(ship_index[1])]["coordinates"]) == 0: #Se o navio foi derrubado
                            notified_socket.send(pickle.dumps({
                                "code": 8,
                                "params": {
                                    "type": int(ship_index[0].split("_")[1])
                                }
                            }))
                            oponent_socket.send(pickle.dumps({
                                "code": 9,
                                "params": {
                                    "type": int(ship_index[0].split("_")[1])
                                }
                            }))
                        else:
                            notified_socket.send(pickle.dumps({"code": 4}))
                            oponent_socket.send(pickle.dumps({"code": 5}))          
                else:
                    notified_socket.send(pickle.dumps({"code": 6}))
                    oponent_socket.send(pickle.dumps({"code": 7}))
        
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]