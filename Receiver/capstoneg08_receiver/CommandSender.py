# -*- coding: utf-8 -*-
# CommandSender.py code is based on Python-Xbee Libary SendDataSample example found in 
# https://github.com/digidotcom/xbee-python/tree/master/examples/communication/SendDataSample
from digi.xbee.exception import TimeoutException
import json

START_COMMAND = "START"
REMOTE_NODE_ID = "REMOTE"


class CommandSender():
    def __init__(self, device, dBManager):
        self.device = device
        self.dBManager = dBManager
        self.remonte_device = ''
        self.currCmd = ''
        
    def initSender(self):
        try:
            if not self.device.is_open():
                self.device.open()
    
            # Obtain the remote XBee device from the XBee network.
            xbee_network = self.device.get_network()
            self.remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
            if self.remote_device is None:
                print("Could not find the remote device")
                exit(1)
        except TimeoutException as to:
            print("Unable to get device from Xbee network, because ", repr(to))
    
    def packageCmd(self, cmd):
        data = {}
        data['cmd'] = cmd
        jsonData = json.dumps(data)
        return jsonData
    
    def runCommandSender(self):
        dataToSend = ''
        try:
            if(self.currCmd != START_COMMAND):
                currCmd = self.dBManager.readCommand()
                dataToSend = self.packageCmd(currCmd)
                print("Sending data to %s >> %s..." % (self.remote_device.get_64bit_addr(), currCmd))
                self.device.send_data(self.remote_device, dataToSend)
                print("Success")
        finally:
            if self.device is not None and self.device.is_open():
               self.device.close() 
               self.currCmd = ''
