# -*- coding: utf-8 -*-

from digi.xbee.exception import TimeoutException
import threading
import sys

START_COMMAND = "START"
REMOTE_NODE_ID = "XBEE_T"


class CommandSender(threading.Thread):
    def __init__(self, device, dBManager):
        threading.Thread.__init__(self)
        self.device = device
        self.dBManager = dBManager
        self.remote_device = ''
        
    def initSender(self):
        try:
            if not self.device.is_open():
                self.device.open()
            # Obtain the remote XBee device from the XBee network.
            xbee_network = self.device.get_network()
            self.remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
            if self.remote_device is None:
                print("Could not find the remote device")
                sys.exit(1)
        except TimeoutException as to:
            print("Unable to get device from Xbee network, because ", repr(to))
    
    
    def runCommandSender(self):
        try:
            threading.Thread(target = self.dBManager.searchCommand()).start()
            dataToSend = self.dBManager.getCommand()
            print("Sending data to %s >> %s..." % (self.remote_device.get_64bit_addr(), dataToSend))
            self.device.send_data(self.remote_device, dataToSend)
            print("Success")
            #while(True):
            #    threading.Thread(target = self.dBManager.handshake()).start()    
        finally:
            if self.device is not None and self.device.is_open():
               self.device.close() 
