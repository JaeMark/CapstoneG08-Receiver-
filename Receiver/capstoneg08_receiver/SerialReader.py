# -*- coding: utf-8 -*-
# SerialReader.py code is based on Python-Xbee Libary ReceiveDataSample example found in 
# https://github.com/digidotcom/xbee-python/tree/master/examples/communication/ReceiveDataSample
import threading

class SerialReader(threading.Thread):
    def __init__(self, device, dBManager):
        threading.Thread.__init__(self)
        self.device = device
    
    def data_receive_callback(xbee_message):
            print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                     xbee_message.data.decode()))
    def initReceiver(self):
        if not self.device.is_open():
                self.device.open()
        self.device.add_data_received_callback(self.data_receive_callback)
        
    def run(self):
        try:
            
            print("Waiting for data...\n")
            input()
        except BlockingIOError as error:
            print("Unable to receive data, because ", repr(error))
        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()
            
