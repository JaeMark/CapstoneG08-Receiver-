# -*- coding: utf-8 -*-

from digi.xbee.exception import TimeoutException
import threading

class SerialReader(threading.Thread):
    def __init__(self, device, dBManager):
        self.device = device
    
    def data_receive_callback(xbee_message):
            print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                     xbee_message.data.decode()))
    def initReceiver(self):
        try:
            if not self.device.is_open():
                self.device.open()
            self.device.add_data_received_callback(self.data_receive_callback)
        except TimeoutException as to:
            print("Unable to open device, because ", repr(to))
    
    def runReceiver(self):
        try: 
            self.device.flush_queues()
            print("Waiting for data...\n")
            while(True):
                jsonPacket = self.device.read_data()
                print(jsonPacket)
                if jsonPacket is not None:
                    threading.Thread(target = self.dbManager.storeData(jsonPacket)).start()  
        except TimeoutException as to:
            print("Unable to receive data, because ", repr(to))
        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()
            
