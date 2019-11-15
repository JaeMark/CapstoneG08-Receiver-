# -*- coding: utf-8 -*-
# SerialReader.py code is based on Python-Xbee Libary ReceiveDataSample example found in 
# https://github.com/digidotcom/xbee-python/tree/master/examples/communication/ReceiveDataSample
from digi.xbee.exception import TimeoutException
import threading

class SerialReader():
    def __init__(self, device, dBManager):
        self.device = device
    
    def data_receive_callback(xbee_message):
            print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                     xbee_message.data.decode()))
    def initReceiver(self):
        if not self.device.is_open():
                self.device.open()
        self.device.add_data_received_callback(self.data_receive_callback)
        
    def runReceiver(self):
        try: 
            self.device.flush_queues()
            print("Waiting for data...\n")
            while(True):
                jsonPacket = self.device.read_data()
                if jsonPacket is not None:
                    threading.Thread(target = self.dbManager.storeData(jsonPacket)).start()         
        except TimeoutException as to:
            print("Unable to receive data, because ", repr(to))
        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()
            
