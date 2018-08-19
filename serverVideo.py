from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


HOST = "192.168.157.206"
PORT = 4000
BufferSize = 4096
addresses = {}

def Connections():
    while True:
        try:
            client, addr = server.accept()
            print("{} is connected!!".format(addr))
            addresses[client] = addr
            Thread(target=ClientConnection, args=(client, )).start()
        except:
            continue

def ClientConnection(client):
    while True:
        data = b''
        # print("In client Connections...")
        try:
            data = client.recv(BufferSize).decode("utf-8")
            if data == "Sending Audio From Client":
                client.send(("Sending Audio From Client Confirmed"))
                data = client.recv(BufferSize)
                if not data:
                    break
                broadcast(client, "SOUND", data)
            elif data == "Sending Video From Client":
                client.send(("Sending Video From Client Confirmed"))
                data = client.recv(BufferSize)
                if not data:
                    break
                broadcast(client, "VIDEO", data)
        except:
            continue
        break

def broadcast(clientSocket, format, data_to_be_sent):
    if format == "SOUND":
        clientSocket.send(("Broadcasting Sound").encode("utf-8"))
        temp = clientSocket.recv(BufferSize).decode("utf-8")
        if temp == "Broadcast Sound":
            for client in addresses:
                if client != clientSocket:
                    # print("Broadcasting...")
                    client.sendall(data_to_be_sent)

    elif format == "VIDEO":
        clientSocket.send(("Broadcasting Video").encode("utf-8"))
        temp = clientSocket.recv(BufferSize).decode("utf-8")
        if temp == "Broadcast Video":
            for client in addresses:
                if client != clientSocket:
                    # print("Broadcasting...")
                    client.sendall(data_to_be_sent)


server = socket(family=AF_INET, type=SOCK_STREAM)
try:
    server.bind((HOST, PORT))
except OSError:
    print("Server Busy")

server.listen(2)
print("Waiting for connection..")
AcceptThread = Thread(target=Connections)
AcceptThread.start()
AcceptThread.join()
