# -*- coding: utf-8 -*-

from digi.xbee.exception import TimeoutException
import threading

class SerialReader(threading.Thread):
    def __init__(self, device, dBManager):
        self.device = device
        self.dBManager = dBManager
    
    def initReceiver(self):
        try:
            if not self.device.is_open():
                self.device.open()
        except TimeoutException as to:
            print("Unable to open device, because ", repr(to))
    
    def runReceiver(self):
        try: 
            self.device.flush_queues()
            print("Waiting for data...\n")
            while(True):
                jsonPacket = self.device.read_data()
                if jsonPacket is not None:
                    print("From %s >> %s" % (jsonPacket.remote_device.get_64bit_addr(),
                                         jsonPacket.data.decode()))
                    #threading.Thread(target = self.dBManager.storeData(jsonPacket.data.decode())).start()  
        except TimeoutException as to:
            print("Unable to receive data, because ", repr(to))
        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()
            
