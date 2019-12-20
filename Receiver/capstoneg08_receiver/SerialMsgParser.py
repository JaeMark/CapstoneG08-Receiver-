# -*- coding: utf-8 -*-

import threading

class SerialMsgParser(threading.Thread):
    def __init__(self, dBManager):
        self.dBManager = dBManager
    
    def getTrailingData(self, msg):
        lastOpeningIndex = msg.rfind("{")
        lastClosingIndex = msg.rfind("}")
        if lastOpeningIndex > lastClosingIndex:
            trailingDataIndex = msg.rfind("{")
            trailingData = msg[trailingDataIndex:]   
        else:
            trailingData = ""
        return trailingData
    
    def getMsgToParse(self, msg):
        msgToParseEndIndex = msg.rfind("}")
        msgToParse = msg[:msgToParseEndIndex+1]       
        return msgToParse
    
    def parseMsg(self, msg):
        jsonIndexStart = 0
        jsonIndexEnd = 0
        jsonIndexEndIndex = msg.rfind("}")
        #print("The json end index final is: " + str(jsonIndexEndIndex))
            
        while True:
            if jsonIndexEnd == jsonIndexEndIndex:
                return
            jsonIndexEnd = msg.find("}", jsonIndexStart+1)
            jsonData = msg[jsonIndexStart:jsonIndexEnd+1]
            #print("The json index end is: " +  str(jsonIndexEnd))
            #print("The json data is: " + jsonData)
            if jsonData is not None:
                #print("The json data is: " + jsonData)
                threading.Thread(target = self.dBManager.storeData(jsonData)).start()
                #self.dBManager.storeData(jsonData)
            jsonIndexStart = jsonIndexEnd+1
        return
