# -*- coding: utf-8 -*-
import threading
from capstoneg08_tcpserver.TCPServer import TCPServer

def serverTest():
    myTCPServer = TCPServer('localhost', 8080)
    myTCPServer.startServer()
    myTCPServer.start()
    
    # connection test
    isListening = myTCPServer.isListening
    if isListening:
        print("Server is listening")
    if not isListening:
        print("Server is not listening")    

serverTest()