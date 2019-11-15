# -*- coding: utf-8 -*-
import threading
import json

class DatabaseManager(threading.Thread):
    def __init__(self, databaseConn):
        threading.Thread.__init__(self)
        self.databaseConn = databaseConn;
        self.cursor = databaseConn.cursor()
                            
    def storeData(self, jsonPacket):
        dataPacket = json.loads(jsonPacket)
        ImID = dataPacket['sampleNum']
        time = dataPacket['time']
        volt = dataPacket['volt']
        curr = dataPacket['curr']
        
        sql = "INSERT INTO imports (ImID, Instant, Volt, Curr, Processed) VALUES (?, ?, ?, ?, ?);"
        self.cursor.execute(sql, ImID, time, volt, curr, 0)
        self.databaseConn.commit()
        print("Data packet containing the values: sample number = " + str(ImID) + ", voltage = " + str(volt) + 
              ", current = " + str(curr) + ", timestamp = "
              + time + " has been stored")
        return
    
    def printDatabase(self):
        sql = "SELECT * FROM imports"
        self.cursor.execute(sql)
        for row in self.cursor:
            print (row)
        self.databaseConn.commit()
                
    def getCommand(self):
        #sql = "SELECT cmd FROM COMMAND"
        #self.cursor.execute(sql)
        #cmd = self.cursor;
        #self.databaseConn.commit()
        
        # fake command
        cmd = 'START'
        return cmd
    
    def sendResponce(self, table, ID, msg):
        sql = "INSERT INTO ? (?, ?) VALUES (?, ?);"
        self.cursor.execute(sql, table, ID, msg)
        self.databaseConn.commit()
        return