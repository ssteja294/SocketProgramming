# New socket server

import socket as Socket
import threading as Threading

Client_sockets_dict = {}
HOST = '138.68.140.83'
PORT = 5123

Server_socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)

Server_socket.bind((HOST, PORT))
Server_socket.listen(5)
print("Server is listening on ", HOST, ":", PORT)

def Handle_client(Client_socket):
    try:
        Name = Client_socket.recv(1024)
        Client_sockets_dict[Client_socket] = Name.decode()
        while True:

            Data = Client_socket.recv(1024)
            if not Data:
                break

            Message = Data.decode()

            if Message == 'exit':

                Client_socket.send(Message.encode())
                Client_sockets_dict.pop(Client_socket)
            else:

                print("Received message: \n" + Client_sockets_dict[Client_socket] + ": " + Message + "\n")

                for Key in Client_sockets_dict.keys():
                    if Key != Client_socket:
                        Key.send(((Client_sockets_dict[Client_socket] + ": " + Message).encode()))
    except ConnectionResetError:
        print("Conection closed")
        Client_sockets_dict.pop(Client_socket)
        Client_socket.close()

while True:

    Client_socket, Client_address = Server_socket.accept()
    print("Accepted connection from", Client_address)

    client_handler = Threading.Thread(target = Handle_client, args = (Client_socket,))
    client_handler.start()

