import socket

from J255_Variable import (GetVariableValue,
                           SetVariableValue,
                           DeclaredVariable)

mySocket: socket.socket
clientSocket: socket.socket = None
isServer: bool = False

# Execute network(socket)
def ExecuteNet(args: list[str]):
    global mySocket
    global clientSocket
    global isServer

    args = args[1].split(" ", 1)

    if args[0] == "init":
        datas = args[1].split(", ", 1)

        for i in range(0, len(datas)):
            if DeclaredVariable(datas[i]):
                datas[i] = GetVariableValue(datas[i])

        if datas[0] == "AF_INET":
            if datas[1] == "TCP":
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            elif datas[1] == "UDP":
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    elif args[0] == "connect":
        isServer = False
        datas = args[1].split(", ", 1)

        for i in range(0, len(datas)):
            if DeclaredVariable(datas[i]):
                datas[i] = GetVariableValue(datas[i])

        address = (datas[0], int(datas[1]))

        mySocket.connect(address)
    elif args[0] == "bind":
        isServer = True
        datas = args[1].split(", ", 1)

        for i in range(0, len(datas)):
            if DeclaredVariable(datas[i]):
                datas[i] = GetVariableValue(datas[i])

        address = (datas[0], int(datas[1]))

        mySocket.bind(address)
    elif args[0] == "listen":
        mySocket.listen()
    elif args[0] == "accept":
        client, address = mySocket.accept()

        clientSocket = client
    elif args[0] == "send":
        if DeclaredVariable(args[1]):
            args[1] = GetVariableValue(args[1])

        if isServer:
            clientSocket.send(args[1].encode())
        else:
            mySocket.send(args[1].encode())
    elif args[0] == "receive":
        datas = args[1].split(", ", 1)

        for i in range(0, len(datas) - 1):
            if DeclaredVariable(datas[i]):
                datas[i] = GetVariableValue(datas[i])

        if isServer:
            SetVariableValue(datas[1], clientSocket.recv(int(datas[0])).decode())
        else:
            SetVariableValue(datas[1], mySocket.recv(int(datas[0])).decode())
    elif args[0] == "close":
        if isServer:
            clientSocket.close()

        mySocket.close()