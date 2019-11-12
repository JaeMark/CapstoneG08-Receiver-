# -*- coding: utf-8 -*-
import pyodbc
from digi.xbee.devices import XBeeDevice
from DatabaseManager import DatabaseManager
from CommandSender import CommandSender
from SerialReader import SerialReader

PORT = "COM1"
BAUD_RATE = 9600

def initReceiver():
    conn = pyodbc.connect("Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True")
    dBManager = DatabaseManager(conn)
    
    
    device = XBeeDevice(PORT, BAUD_RATE)
    myCommandSender = CommandSender(device, dBManager)
    mySerialReader = SerialReader(device, dBManager)

    myCommandSender.initSender()
    mySerialReader.initReceiver()
    
    myCommandSender.runCommandSender()
    mySerialReader.runReceiver()
    return
 
def dataBaseTest():
    conn = pyodbc.connect("Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True")
    dBManager = DatabaseManager(conn)
    
    # test database
    #dBManager.createTestTable()
    #dBManager.storeData(16, 1.23456, 0.12345, "2019-11-11 10:57:00")
    dBManager.printDatabase()
    
#initReceiver()
dataBaseTest()