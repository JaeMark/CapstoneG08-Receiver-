# -*- coding: utf-8 -*-
import pyodbc
import json
import threading
from digi.xbee.devices import XBeeDevice
from DatabaseManager import DatabaseManager
from CommandSender import CommandSender
from SerialReader import SerialReader

PORT = "COM3"
BAUD_RATE = 9600

def initReceiver():
    print("Connecting to Local Database.")
    conn = pyodbc.connect("Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True")
    dBManager = DatabaseManager(conn)
    
    print("Initializing XBee Device.")
    device = XBeeDevice(PORT, BAUD_RATE)
    if device is not None and device.is_open():
       device.close()
    myCommandSender = CommandSender(device, dBManager)
    mySerialReader = SerialReader(device, dBManager)

    print("Initializing Command Sender Program.")
    myCommandSender.initSender()
    print("Launching Command Sender Program.")    
    threading.Thread(target = myCommandSender.runCommandSender()).start()
    
    print("Initializing Receiver Program.")
    mySerialReader.initReceiver()
    print("Launching Receiver Program.")    
    threading.Thread(target = mySerialReader.runReceiver()).start()
    return

initReceiver()