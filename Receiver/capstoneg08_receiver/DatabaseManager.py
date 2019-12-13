# -*- coding: utf-8 -*-
import threading
import json
import time

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
    
    def storeData(self, jsonPacket):
        dataPacket = json.loads(jsonPacket)
        ImID = dataPacket['sampleNum']
        time = dataPacket['time']
        volt = dataPacket['volt']
        curr = dataPacket['curr']
        
        sql = "INSERT INTO imports (ImID, Instant, Volt, Curr, Processed) VALUES (?, ?, ?, ?, ?);"
        self.cursor.execute(sql, ImID, time, volt, curr, 0)
        self.databaseConn.commit()
        print("Inserting (" + str(ImID) + ", " + time + ", " + str(volt) + ", " + str(curr) + ")")
# =============================================================================
#         print("Data packet containing the values: sample number = " + str(ImID) + ", voltage = " + str(volt) + 
#               ", current = " + str(curr) + ", timestamp = "
#               + time + " has been stored")
# =============================================================================
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
        
    def searchCommand(self):
        waitingForStart = True;
        while (waitingForStart):
            sql = "SELECT COUNT(*) FROM mcuCmds WHERE Handshake = 0"
            self.cursor.execute(sql)
            numStartRequest = self.cursor.fetchone()[0]
            if(numStartRequest > 0):
                # there is a start request
                waitingForStart = False;
            self.databaseConn.commit()
        dataToSend = {}
        dataToSend['command'] = START_COMMAND   
        dataToSend['sampleNum'] = self.indexStart
        jsonData = json.dumps(dataToSend)
        self.mcuCommand = jsonData
       # self.mcuCommand = 's'
        return 
        
    def handshake(self):
        sql = "UPDATE mcuCmds SET Handshake = 1 WHERE Handshake = 0;"
        self.cursor.execute(sql)
        self.databaseConn.commit()
        time.sleep(3)
        return
    
    def getCommand(self):
        return self.mcuCommand
                
# =============================================================================
#     def processesCommands(self):
#         return "START"
#         sql = "SELECT * FROM COMMAND WHERE Handshake = 1"
#         self.cursor.execute(sql)
#         ###
#         self.databaseConn.commit()
#         if cmd == 0:
#             self.handshake(self, RxID)
#             data = {}
#             data['cmd'] = cmd
#             packet = json.dumps(data)
#             self.MCUCommand = packet
# =============================================================================
    