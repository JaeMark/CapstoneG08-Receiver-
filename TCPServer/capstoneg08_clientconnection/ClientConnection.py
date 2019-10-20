# -*- coding: utf-8 -*-
import threading
import socket

from capstoneg08_clientmessagehandler import ClientMessageHandler

class ClientConnection(threading.Thread):
    def __init__(self, clientSocket, myClientMessageHandler, myTCPServer):
        threading.Thread.__init__(self)
        
        self.clientSocket = clientSocket
        self.myClientMessageHandler = myClientMessageHandler
        self.myTCPServer = myTCPServer
        
        self.stopThisThread = False
        
        self.myClientCommandHandler = ClientMessageHandler(self.myTCPServer)
        
    def disconnectClient(self):
        try:
            self.stopThisThread = True
            self.clientSocket.close()
            self.clientSocket is None
        except socket.error as SocketError:
            print("Unable to disconnect from server, because ", repr(SocketError))
    
    def run(self):
        clientMsg = ''
        while not self.stopThisThread:
            try:
                msg = self.clientSocket.read()
                clientMsg = str(msg)
                self.myClientMessageHandler(self, clientMsg)
            except BlockingIOError:
                print("Unable to read message, because ", repr(BlockingIOError))
                self.disconnectClient