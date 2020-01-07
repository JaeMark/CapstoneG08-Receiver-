# -*- coding: utf-8 -*-
from digi.xbee.exception import TimeoutException
from SerialMsgParser import SerialMsgParser
import threading

REMOTE_NODE_ID = "XBEE_T"

class XBeeTransceiver(threading.Thread):
    def __init__(self, device, dBManager):
        threading.Thread.__init__(self)
        self.device = device
        self.dBManager = dBManager
        
    def initTransceiver(self):
        self.mySerialMsgParser = SerialMsgParser(self.dBManager)
        
        try:
            if self.device is not None and not self.device.is_open():
                self.device.open()
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
                
                
    def run(self):
        try:
            threading.Thread(target = self.dBManager.searchCommand()).start()
            dataToSend = self.dBManager.getCommand()
            print("Sending data %s..." % (dataToSend))
            self.device.send_data_broadcast(dataToSend)
            print("Success")
            #while(True):
            #    threading.Thread(target = self.dBManager.handshake()).start()    
        except TimeoutException as to:
            print("Unable to send command, because ", repr(to))
            if self.device is not None and self.device.is_open():
                self.device.close()
                
        try: 
            self.device.flush_queues()
            print("Waiting for data...\n")
            data = ''
            trailingData = ''
            msgToParse = ''
            while(True):
                threading.Thread(target = self.dBManager.handshake()).start()    
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
    