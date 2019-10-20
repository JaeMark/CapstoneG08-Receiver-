# -*- coding: utf-8 -*-

DELIM = '\n'

class ClientMesssageHandler():
    def __init__(self, myTCPServer):
        self.myTCPServer = myTCPServer
        
    def handleClientMessage(self, myClientConncetion, msg):
        if msg == 'c':
            print("The message %d from client was successuffly received", msg)
        else:
            print("Command does not exist")
    
    