# -*- coding: utf-8 -*-

class DatabaseManager():
    def __init__(self, database):
        self.database = database;
        
    def storeData(self, packet):
        #fake store
        print("Data has been stored")
        return
    
    def readCommand(self):
        # fake command
        return "start"
    
    def sendResponce(self):
        return