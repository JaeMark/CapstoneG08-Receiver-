# -*- coding: utf-8 -*-
import threading

class DatabaseManager(threading.Thread):
    def __init__(self, databaseConn):
        threading.Thread.__init__(self)
        self.databaseConn = databaseConn
        self.cursor = self.databaseConn.cursor()
    
    def storeData(self, volt, curr):   
        # store the data sample in the imports table
        sql = "INSERT INTO imports (Volt, Curr, Processed) VALUES (?, ?, ?);"
        self.cursor.execute(sql, volt, curr, 0)
        self.databaseConn.commit()
        return
    
    def printImportsTable(self):
        # print the contents of the imports table
        sql = "SELECT * FROM imports"
        self.cursor.execute(sql)
        for row in self.cursor:
            print (row)
        self.databaseConn.commit()
        
#    def checkIfSamplingIsDone(self, numSamples):
#        sql = "SELECT COUNT(*) FROM imports"
#        self.cursor.execute(sql)
#        currentMaxIndex = self.cursor.fetchone()[0]   
#        if((currentMaxIndex % numSamples) == 0):
#            print("All " + str(numSamples) + " samples have been inserted into the imports database."
#                   + " Entering Sleep Mode...")
#            return True
#        else:
#            return False
        
#    def printMcuCmdsTable(self):
#        sql = "SELECT * FROM mcuCmds"
#        self.cursor.execute(sql)
#        for row in self.cursor:
#            print (row)
#        self.databaseConn.commit()       
#    def searchStartCommand(self):
#        waitingForStart = True;
#        while (waitingForStart):
#            sql = "SELECT COUNT(*) FROM mcuCmds WHERE Handshake = 0"
#            self.cursor.execute(sql)
#            numStartRequest = self.cursor.fetchone()[0]
#            if(numStartRequest > 0):
#                # there is a start request
#                waitingForStart = False;
#            self.databaseConn.commit()
#        return True
        
#    def handshake(self):
#        sql = "UPDATE mcuCmds SET Handshake = 1 WHERE Handshake = 0;"
#        self.cursor.execute(sql)
#        self.databaseConn.commit()
#        return
    