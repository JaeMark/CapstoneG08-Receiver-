# -*- coding: utf-8 -*-
import threading
import socket

from capstoneg08_clientconnection.ClientConnection import ClientConnection
from capstoneg08_clientmessagehandler.ClientMessageHandler import ClientMesssageHandler

class TCPServer(threading.Thread):
    def __init__(self, host, portNumber):
        threading.Thread.__init__(self)
        
        self.host = host
        self.portNumber = portNumber
        
        self.isListening = False
        
        self.myClientMessageHandler = ClientMesssageHandler(self)
    
    def startServer(self):
        if(self.serverSocket is not None):
            self.stopServer()
        else:
            try:
                self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.serverSocket.bind((self.host, self.portNumber))
                self.serverSocket.listen(5)
                self.isListening = True
            except socket.error as SocketError:
                print("Unable to create TCP Server socket, because ", repr(SocketError))
    
    def stopServer(self):
        if (self.serverSocket is None):
            try:
                self.serverSocket.close()
            except socket.error as SocketError:
                print("Unable to close TCP Server socket, because ", repr(SocketError))
    
    def isListening(self):
        return self.isListening
    
    def stopListening(self):
        self.isListening = False
        
    def run(self):
        while True:
            if self.isListening:
                try:
                    self.clientSocket = self.serverSocket.accept()
                    myCC = ClientConnection(self.clientSocket, self.myClientMessageHandler, self)
                    myCC.start()   
                except socket.error as SocketError:
                    print("Unable to connect to client, because ", repr(SocketError))