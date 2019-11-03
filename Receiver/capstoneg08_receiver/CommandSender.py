# -*- coding: utf-8 -*-
# CommandSender.py code is based on Python-Xbee Libary SendDataSample example found in 
# https://github.com/digidotcom/xbee-python/tree/master/examples/communication/SendDataSample
import threading

DATA_TO_SEND = "Hello XBee!"
REMOTE_NODE_ID = "REMOTE"


class CommandSender(threading.Thread):
    def __init__(self, device, dBManager):
        threading.Thread.__init__(self)
        self.device = device
        self.remonte_device = ''
        
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
        except BlockingIOError as error:
            print("Unable to get device from Xbee network, because ", repr(error))
    
    def run(self):
        try:
            print("Sending data to %s >> %s..." % (self.remote_device.get_64bit_addr(), DATA_TO_SEND))
            self.device.send_data(self.remote_device, DATA_TO_SEND)
            print("Success")
        finally:
            if self.device is not None and self.device.is_open():
               self.device.close() 
