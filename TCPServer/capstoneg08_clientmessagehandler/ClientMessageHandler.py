# -*- coding: utf-8 -*-

DELIM = '\n'

class ClientMesssageHandler():
    def __init__(self, myTCPServer):
        self.myTCPServer = myTCPServer
    
    def handleClientMessage(self, myClientConnection, msg):
        clientCommand = msg.decode()
        if clientCommand == 'c':
            myClientConnection.sendMessageToClient("The message from client was successuffly received".encode())
            print("The message \'" + clientCommand + "\' from client was successuffly received")
        else if (clientCommand == ''):
            break
        else:   
            print("Command \'" + clientCommand + "\' does not exist")
    
    