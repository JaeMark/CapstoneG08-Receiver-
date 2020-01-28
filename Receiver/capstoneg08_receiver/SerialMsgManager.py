# -*- coding: utf-8 -*-

import threading
import json

#==============================================================================
# CONSTANT VARIABLES
#==============================================================================
DEFAULT_COMMAND = 0
START_COMMAND = 1
SLEEP_COMMAND = 2
WAKE_UP_COMMAND = 3

class SerialMsgManager(threading.Thread):
    def __init__(self, dBManager, sample_num, trans_delim, small_trans_delay, big_trans_delay, sleep_time):
        threading.Thread.__init__(self)
        self.dBManager = dBManager
        self.sample_num = sample_num
        self.trans_delim = trans_delim
        self.small_trans_delay = small_trans_delay
        self.big_trans_delay = big_trans_delay
        self.sleep_time = sleep_time

        self.sampleParsed  =  0

    def getMsgToParse(self, msg):
        # get a set of complete json object to be parsed
        msgToParseEndIndex = msg.rfind("}")
        msgToParse = msg[:msgToParseEndIndex+1]       
        return msgToParse
    
    def getTrailingData(self, msg): 
        # get the trailing incomplete json object from the data received
        lastOpeningIndex = msg.rfind("{")
        lastClosingIndex = msg.rfind("}")
        if lastOpeningIndex > lastClosingIndex:
            trailingDataIndex = msg.rfind("{")
            trailingData = msg[trailingDataIndex:]   
        else:
            trailingData = ""
        return trailingData
    
    def setSampleNumToParse(self, sampleNum):
        # set the the number of samples to be parsed
        self.sampleParsed == sampleNum
        return 
    
    def getSampleNumParsed(self):
        # get the the number of samples to be parsed
        return self.sampleParsed
    
    def getStartCommand(self):
        # create the start command json object 
        dataToSend = {}
        dataToSend['command'] = START_COMMAND  
        dataToSend['sampleNum'] = self.sample_num
        dataToSend['delim'] = self.trans_delim
        dataToSend['smallDelay'] = self.small_trans_delay
        dataToSend['bigDelay'] = self.big_trans_delay
        jsonData = json.dumps(dataToSend)
        return jsonData
    
    def getSleepCommand(self):
        # create the sleep command json object 
        dataToSend = {}
        dataToSend['command'] = SLEEP_COMMAND   
        dataToSend['sleepTime'] = self.sleep_time 
        jsonData = json.dumps(dataToSend)
        self.parsedAllSamples = False
        return jsonData

    def parseHandshake(self, msg):
        # parse the start command handshake json object 
        dataPacket = json.loads(msg)
        cmd = dataPacket["command"]
        numSamples  =  dataPacket["sampleNum"]
        return cmd, numSamples
    
    def parseWakeUpCommand(self, msg):
        # parse the wakeup handshake json object 
        data = json.loads(msg)
        wakeUpCommand = data['command']
        if(wakeUpCommand == WAKE_UP_COMMAND):
            return True
        return False
                
    def parseReadingData(self, msg, numSamples):
        # parse the data smaples received
        jsonIndexStart = 0
        jsonIndexEnd = 0
        jsonIndexEndIndex = msg.rfind("}")
            
        while True:
            if jsonIndexEnd == jsonIndexEndIndex:
                return
            jsonIndexEnd = msg.find("}", jsonIndexStart+1)
            jsonData = msg[jsonIndexStart:jsonIndexEnd+1]
            if jsonData:
                data = json.loads(jsonData)
                volt = data['volt']
                curr = data['curr']
                # store the data sample in the database
                threading.Thread(target = self.dBManager.storeData(volt, curr)).start()
                self.sampleParsed = data['sampleNum']
            jsonIndexStart = jsonIndexEnd+1   
        return
