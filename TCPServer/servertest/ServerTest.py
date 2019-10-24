# -*- coding: utf-8 -*-
import threading
from capstoneg08_tcpserver.TCPServer import TCPServer

BUFF_SIZE = 1024

def serverTest():
    myTCPServer = TCPServer(BUFF_SIZE, 'localhost', 8080)
    myTCPServer.startServer()
    myTCPServer.start()
    
    # connection test
    isListening = myTCPServer.isListening
    if isListening:
        print("Server is listening")
    if not isListening:
        print("Server is not listening")    

serverTest()