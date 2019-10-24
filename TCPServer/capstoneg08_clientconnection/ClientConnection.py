# -*- coding: utf-8 -*-
import threading
import socket

from capstoneg08_clientmessagehandler.ClientMessageHandler import ClientMesssageHandler

class ClientConnection(threading.Thread):
    def __init__(self, clientSocket, myClientMessageHandler, myTCPServer, buffSize):
        threading.Thread.__init__(self)
        
        self.clientSocket = clientSocket
        self.myClientMessageHandler = myClientMessageHandler
        self.myTCPServer = myTCPServer
        self.buffSize = buffSize
        
        self.stopThisThread = False
        
    def disconnectClient(self):
        try:
            self.stopThisThread = True
            self.clientSocket.close()
            self.clientSocket is None
        except socket.error as SocketError:
            print("Unable to disconnect from server, because ", repr(SocketError))
    
    def sendMessageToClient(self, msg):
        self.clientSocket.sendall(msg)
    
    def run(self):
        while not self.stopThisThread:
            try:
                msg = self.clientSocket.recv(self.buffSize)
                self.myClientMessageHandler.handleClientMessage(self, msg)
            except BlockingIOError:
                print("Unable to read message, because ", repr(BlockingIOError))
                self.disconnectClient