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

def databaseStoreTest():
    print("============================================================")
    print("DATABASE INSERT TEST")
    print("============================================================")
    print("Connecting to Local Database.")
    conn = pyodbc.connect("Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True")
    dBManager = DatabaseManager(conn)
    
    # test database
    cursor = conn.cursor()    
    cursor.execute('''
                   DROP TABLE imports;
                   ''')
    conn.commit()
    print("Creating Test Table.")
    cursor.execute('''
                   CREATE TABLE imports (
                           ImID bigint NOT NULL,
                           Instant NVARCHAR(255),
                           Volt NVARCHAR(255),
                           Curr NVARCHAR(255),
                           Processed int
                           PRIMARY KEY(ImID)
                   )''')
    conn.commit() 
    print("Inserting Table Rows")
    data = {}
    data['sampleNum'] = 0
    data['time'] = "2019-11-11 10:57:00"
    data['volt'] = 1.23456
    data['curr'] = 0.12345
    jsonData = json.dumps(data)
    threading.Thread(target = dBManager.storeData(jsonData)).start()
    
    data = {}
    data['sampleNum'] = 1
    data['time'] = "2019-11-11 10:57:00"
    data['volt'] = 1.0000
    data['curr'] = 0.13145
    jsonData = json.dumps(data)
    threading.Thread(target = dBManager.storeData(jsonData)).start()
    
    data = {}
    data['sampleNum'] = 2
    data['time'] = "2019-11-11 10:57:00"
    data['volt'] = 0.0
    data['curr'] = 0.0
    jsonData = json.dumps(data)
    threading.Thread(target = dBManager.storeData(jsonData)).start()
    
    data = {}
    data['sampleNum'] = 3
    data['time'] = "2019-11-11 10:57:00"
    data['volt'] = 0.0
    data['curr'] = 0.12345
    jsonData = json.dumps(data)
    threading.Thread(target = dBManager.storeData(jsonData)).start()

    
    print("Printing Imports Table.")
    dBManager.printImportsTable()

    print("\n")
    return
 
def databaseReadTest():
    print("============================================================")
    print("DATABASE READ TEST")
    print("============================================================")
    print("Connecting to Local Database.")
    conn = pyodbc.connect("Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True")
    dBManager = DatabaseManager(conn)
    
    cursor = conn.cursor()
    cursor.execute('''
                   DROP TABLE mcuCmds;
                   ''')
    conn.commit()
    cursor.execute('''
                   CREATE TABLE mcuCmds (
                           RxID bigint NOT NULL,
                           Handshake BIT,
                           PRIMARY KEY(RxID)
                   )''')
    conn.commit()
    cursor.execute('''
                   INSERT INTO mcuCmds (RxID, Handshake)
                   VALUES (0, 0), (1, 0), (2, 1)
                   ''')
    conn.commit()
    
    print("Printing mcuCmds Table.")
    dBManager.printMcuCmdsTable()
    
    threading.Thread(target = dBManager.searchCommand()).start()
    cmd = dBManager.getCommand()
    print("Found user command " + cmd)
    
    print("Begin Handshake Mode")
    threading.Thread(target = dBManager.handshake()).start()
    print("Printing mcuCmds Table.")
    dBManager.printMcuCmdsTable()
    
    print("\n")
    return
    
def initReceiverTest():
    print("============================================================")
    print("WIRELESS COMMUNICATION TEST")
    print("============================================================")
    print("Connecting to Local Database.")
    conn = pyodbc.connect("Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True")
    dBManager = DatabaseManager(conn)

    cursor = conn.cursor()
    cursor.execute('''
                   DROP TABLE mcuCmds;
                   ''')
    conn.commit()
    cursor.execute('''
                   CREATE TABLE mcuCmds (
                           RxID bigint NOT NULL,
                           Handshake BIT,
                           PRIMARY KEY(RxID)
                   )''')
    conn.commit()
    cursor.execute('''
                   INSERT INTO mcuCmds (RxID, Handshake)
                   VALUES (0, 0), (1, 0), (2, 1)
                   ''')
    conn.commit()
    
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
    
    cursor.execute('''
                   DROP TABLE imports;
                   ''')
    conn.commit()
    print("Creating Test Table.")
    cursor.execute('''
                   CREATE TABLE imports (
                           ImID bigint NOT NULL,
                           Instant NVARCHAR(255),
                           Volt NVARCHAR(255),
                           Curr NVARCHAR(255),
                           Processed int
                           PRIMARY KEY(ImID)
                   )''')
    conn.commit() 
    
    print("Initializing Receiver Program.")
    mySerialReader.initReceiver()
    print("Launching Receiver Program.")    
    threading.Thread(target = mySerialReader.runReceiver()).start()
    
    print("\n")
    return


databaseStoreTest() 
databaseReadTest() 
initReceiverTest()