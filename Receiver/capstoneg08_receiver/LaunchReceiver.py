# -*- coding: utf-8 -*-
import pyodbc
import json
from digi.xbee.devices import XBeeDevice
from DatabaseManager import DatabaseManager
from CommandSender import CommandSender
from SerialReader import SerialReader

PORT = "COM1"
BAUD_RATE = 9600

def initReceiver():
    print("Connecting to Local Database.")
    conn = pyodbc.connect("Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True")
    dBManager = DatabaseManager(conn)
    
    print("Initializing XBee Device.")
    device = XBeeDevice(PORT, BAUD_RATE)
    myCommandSender = CommandSender(device, dBManager)
    mySerialReader = SerialReader(device, dBManager)

    print("Initializing Receiver Program.")
    myCommandSender.initSender()
    mySerialReader.initReceiver()

    print("Launching Receiver Program.")    
    myCommandSender.runCommandSender()
    mySerialReader.runReceiver()
    return
 
def dataBaseTest():
    print("Connecting to Local Database.")
    conn = pyodbc.connect("Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True")
    dBManager = DatabaseManager(conn)
    
    # test database
    cursor = conn.cursor()
#    print("Creating Test Table.")
#    cursor.execute('''
#                   CREATE TABLE imports (
#                           ImID bigint NOT NULL,
#                           Instant NVARCHAR(255),
#                           Volt NVARCHAR(255),
#                           Curr NVARCHAR(255),
#                           Processed int
#                           PRIMARY KEY(ImID)
#                   )''')
#    conn.commit()
    
    print("Inserting Table Row")
    data = {}
    data['sampleNum'] = 66
    data['time'] = "2019-11-11 10:57:00"
    data['volt'] = 1.23456
    data['curr'] = 0.12345
    jsonData = json.dumps(data)
    dBManager.storeData(jsonData)
    #dBManager.storeData(16, 1.23456, 0.12345, "2019-11-11 10:57:00")
    
    print("Printing Imports Table.")
    dBManager.printDatabase()
 
#initReceiver()
dataBaseTest()