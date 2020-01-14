# -*- coding: utf-8 -*-
from digi.xbee.exception import TimeoutException
from SerialMsgParser import SerialMsgParser
import threading
import time
import json

REMOTE_NODE_ID = "XBEE_T"

DEFAULT_COMMAND = 0
START_RECEIVING_COMMAND = 1
DEFAULT_NUM_SAMPLES = 0

class XBeeTransceiver(threading.Thread):
    def __init__(self, device, dBManager):
       # threading.Thread.__init__(self)
        self.device = device
        self.dBManager = dBManager
        
    def initTransceiver(self):
        self.mySerialMsgParser = SerialMsgParser(self.dBManager)
        
        try:
            if self.device is not None and not self.device.is_open():
                self.device.open()
                self.device.flush_queues()
            # Obtain the remote XBee device from the XBee network.
#            xbee_network = self.device.get_network()
#            self.remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
#            if self.remote_device is None:
#                print("Could not find the remote device")
#                if self.device is not None and self.device.is_open():
#                    self.device.close()
#                sys.exit(1)
        except TimeoutException as to:
            print("Unable to get device from Xbee network, because ", repr(to))
            if self.device is not None and self.device.is_open():
                self.device.close()
            
    def runDataSender(self):
        try:
            threading.Thread(target = self.dBManager.searchCommand()).start()
            dataToSend = self.dBManager.getCommand()
            print("Sending data %s..." % (dataToSend))
            self.device.send_data_broadcast(dataToSend)
            print("Success")
            #while(True):
            #    threading.Thread(target = self.dBManager.handshake()).start()    
        finally:
        #    if self.device is not None and self.device.is_open():
        #       self.device.close() 
            return
    
    def runDataReceiver(self):
        try: 
            self.device.flush_queues()
            print("Waiting for data...\n")
            data = ''
            trailingData = ''
            msgToParse = ''
            while(True):
                packet = self.device.read_data()
                if packet is not None:
                    data = packet.data.decode()
                    #print("From %s >> %s" % (packet.remote_device.get_64bit_addr(), data))
                    data = trailingData + data    
                    msgToParse = self.mySerialMsgParser.getMsgToParse(data)
                    trailingData = self.mySerialMsgParser.getTrailingData(data)
                    #print("The data is: " + data)
                    #print("The message to parse is: " + msgToParse)
                    #print("The trailing data is: " + trailingData)
                    threading.Thread(target = self.mySerialMsgParser.parseMsg(msgToParse)).start()  
        except TimeoutException as to:
            print("Unable to receive data, because ", repr(to))
            if self.device is not None and self.device.is_open():
                self.device.close()
        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()
                
                
    def runTransceiver(self):
        TransCommand = DEFAULT_COMMAND
        numSamples = DEFAULT_NUM_SAMPLES
        
        while(TransCommand != START_RECEIVING_COMMAND):
            try:
                if self.dBManager.searchStartCommand():
                    dataToSend = self.mySerialMsgParser.getStartCommand()
                print("Sending data %s..." % (dataToSend))
                self.device.send_data_broadcast(dataToSend)
            except TimeoutException as to:
                print("Unable to send command, because ", repr(to))
                if self.device is not None and self.device.is_open():
                    self.device.close()
            
            try: 
                #self.device.flush_queues()
                timeout = time.monotonic() + 60 * 5 # timeout afer 30 minutes
                while time.monotonic() < timeout:
                    packet = self.device.read_data()
                    if packet is not None:
                            data = packet.data.decode()
                            print("The handshake data is: " + data)
                            dataPacket = json.loads(data)
                            TransCommand = dataPacket["command"]
                            numSamples  =  dataPacket["sampleNum"]
                            #self.mySerialMsgParser.setSampleNumtoParse(self, numSamples)
                            break
            except TimeoutException as to:
                print("Unable to receive data, because ", repr(to))
                if self.device is not None and self.device.is_open():
                    self.device.close()
                    
            if(TransCommand == DEFAULT_COMMAND):
                print("There was no response from the remote device. Resending command...")
                                
        try: 
            #self.device.flush_queues()
            print("\nThe Transceiver is now waiting for data...\n")
            data = ''
            trailingData = ''
            msgToParse = ''
            while(True):
                threading.Thread(target = self.dBManager.handshake()).start()    
                packet = self.device.read_data()
                if packet is not None:
                    decodedData = packet.data.decode()
                    #print("From %s >> %s" % (packet.remote_device.get_64bit_addr(), data))
                    data = trailingData + decodedData   
                    msgToParse = self.mySerialMsgParser.getMsgToParse(data)
                    trailingData = self.mySerialMsgParser.getTrailingData(data)
                    #print("The data is: " + data)
                    #print("The message to parse is: " + msgToParse)
                    #print("The trailing data is: " + trailingData)
                    threading.Thread(target = self.mySerialMsgParser.parseReadingData(msgToParse, numSamples)).start() 
                    if(self.mySerialMsgParser.getSampleNumParsed() == numSamples):
                        dataToSend = self.mySerialMsgParser.getSleepCommand()
                        print("Parsed all sample data. Time to sleep!\nSending sleep command %s..." % (dataToSend))
                        self.device.send_data_broadcast(dataToSend)   
                        self.mySerialMsgParser.setSampleNumToParse(DEFAULT_NUM_SAMPLES)
        except TimeoutException as to:
            print("Unable to receive data, because ", repr(to))
            if self.device is not None and self.device.is_open():
                self.device.close()
        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()
    