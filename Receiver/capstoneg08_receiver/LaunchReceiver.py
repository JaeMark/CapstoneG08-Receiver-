# -*- coding: utf-8 -*-
from digi.xbee.devices import XBeeDevice
from DatabaseManager import DatabaseManager
from CommandSender import CommandSender
from SerialReader import SerialReader

PORT = "COM1"
BAUD_RATE = 9600

def initReceiver():
    dBManager = DatabaseManager('')
    
    device = XBeeDevice(PORT, BAUD_RATE)
    myCommandSender = CommandSender(device, dBManager)
    mySerialReader = SerialReader(device, dBManager)
    
    myCommandSender.initSender()
    mySerialReader.initReceiver()
    
    myCommandSender.start()
    mySerialReader.start()
    return
    
initReceiver()