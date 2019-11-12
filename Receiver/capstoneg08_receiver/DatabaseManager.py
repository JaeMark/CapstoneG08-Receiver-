# -*- coding: utf-8 -*-
import threading

class DatabaseManager(threading.Thread):
    def __init__(self, databaseConn):
        threading.Thread.__init__(self)
        self.databaseConn = databaseConn;
        self.cursor = databaseConn.cursor()
        
    def createTestTable(self):
        self.cursor.execute('''
                            CREATE TABLE imports (
                                    ImID bigint NOT NULL,
                                    Instant NVARCHAR(255),
                                    Volt NVARCHAR(255),
                                    Curr NVARCHAR(255),
                                    Processed int
                                    PRIMARY KEY(ImID)
                            )''')
        self.databaseConn.commit()
                            
    
    def storeData(self, ImID, volt, curr, time):
        toSQL = "INSERT INTO imports (ImID, Instant, Volt, Curr, Processed) VALUES (?, ?, ?, ?, ?);"
        self.cursor.execute(toSQL, ImID, time, volt, curr, 0)
        self.databaseConn.commit()
        print("Data packet containing the values: voltage = " + str(volt) + 
              " current = " + str(curr) + " timestamp = "
              + time + " has been stored")
        return
    
    def printDatabase(self):
        toSQL = "SELECT * FROM imports"
        self.cursor.execute(toSQL)
        for row in self.cursor:
            print (row)
        self.databaseConn.commit()
                
    def getCommand(self):
        # fake command
        cmd = "START"
        return cmd
    
    def sendResponce(self):
        return