# -*- coding: utf-8 -*-
import threading
import socket

from ClientConnection import ClientConnection
from ClientMessageHandler import ClientMesssageHandler

class TCPServer(threading.Thread):
    def __init__(self, buffSize, host, portNumber):
        threading.Thread.__init__(self)
        
        self.host = host
        self.portNumber = portNumber
        self.buffSize = buffSize
        
        self.isListening = False
        
        self.serverSocket = None
        self.myClientMessageHandler = ClientMesssageHandler(self)
    
    def startServer(self):
        if(self.serverSocket is not None):
            try:
                self.isListening = False
                self.serverSocket.close()
            except socket.error as SocketError:
                print("Unable to close TCP Server socket, because ", repr(SocketError))
        
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.serverSocket.bind((self.host, self.portNumber))
            self.serverSocket.listen(5)
            self.isListening = True
        except socket.error as SocketError:
            print("Unable to create TCP Server socket, because ", repr(SocketError))
    
    def isListening(self):
        return self.isListening
    
    def stopListening(self):
        self.isListening = False
        
    def run(self):
        while True:
            if self.isListening:
                try:
                    self.clientSocket, addr = self.serverSocket.accept()
                    myCC = ClientConnection(self.clientSocket, self.myClientMessageHandler, self, self.buffSize)
                    myCC.start()   
                except socket.error as SocketError:
                    print("Unable to connect to client, because ", repr(SocketError))