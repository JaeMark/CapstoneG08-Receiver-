# -*- coding: utf-8 -*-
import threading
import json
import time
import datetime

START_COMMAND = "START"

class DatabaseManager(threading.Thread):
    def __init__(self, databaseConn):
        threading.Thread.__init__(self)
        self.databaseConn = databaseConn;

                            
    def initDatabase(self):
        self.cursor = self.databaseConn.cursor()
        self.mcuCommand = ''
        self.indexStart = 0
        
        sql = "SELECT COUNT(*) FROM imports"
        self.cursor.execute(sql)
        self.indexStart = self.cursor.fetchone()[0]       
        
        return
    
    def storeData(self, volt, curr, micros):        
     #   sql = "INSERT INTO imports (ImID, Instant, Volt, Curr, Processed) VALUES (?, ?, ?, ?, ?);"
     #   self.cursor.execute(sql, ImID, instant, volt, curr, 0)
        sql = "INSERT INTO imports (Volt, Curr, Micros, Processed) VALUES (?, ?, ?, ?);"
        self.cursor.execute(sql, volt, curr, micros, 0)
        self.databaseConn.commit()
     #   print("Inserting (" + str(ImID) + ", " + instant + ", " + str(volt) + ", " + str(curr) +  ", " + str(micros) +")")
        return
    
    def printImportsTable(self):
        sql = "SELECT * FROM imports"
        self.cursor.execute(sql)
        for row in self.cursor:
            print (row)
        self.databaseConn.commit()
        
    def printMcuCmdsTable(self):
        sql = "SELECT * FROM mcuCmds"
        self.cursor.execute(sql)
        for row in self.cursor:
            print (row)
        self.databaseConn.commit()
        
    def checkIfSamplingIsDone(self, numSamples):
        sql = "SELECT COUNT(*) FROM imports"
        self.cursor.execute(sql)
        currentMaxIndex = self.cursor.fetchone()[0]   
        if((currentMaxIndex % numSamples) == 0):
            print("All " + str(numSamples) + " samples have been inserted into the imports database."
                   + " Entering Sleep Mode...")
            return True
        else:
            return False
        
    def searchStartCommand(self):
        waitingForStart = True;
        while (waitingForStart):
            sql = "SELECT COUNT(*) FROM mcuCmds WHERE Handshake = 0"
            self.cursor.execute(sql)
            numStartRequest = self.cursor.fetchone()[0]
            if(numStartRequest > 0):
                # there is a start request
                waitingForStart = False;
            self.databaseConn.commit()
        return True
        
    def handshake(self):
        sql = "UPDATE mcuCmds SET Handshake = 1 WHERE Handshake = 0;"
        self.cursor.execute(sql)
        self.databaseConn.commit()
        return
    
    def getCommand(self):
        return self.mcuCommand
                