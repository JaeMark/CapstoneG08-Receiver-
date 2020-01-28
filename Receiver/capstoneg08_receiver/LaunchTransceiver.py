# -*- coding: utf-8 -*-
import pyodbc
from digi.xbee.devices import XBeeDevice
from DatabaseManager import DatabaseManager
from XBeeTransceiver import XBeeTransceiver
from SerialMsgManager import SerialMsgManager

#==============================================================================
# CONSTANT VARIABLES
#==============================================================================
SAMPLE_NUM = 128
TRANS_DELIM = 16
SMALL_TRANS_DELAY = 250
BIG_TRANS_DELAY = 750
#SLEEP_TIME = 3600000
SLEEP_TIME = 60000

DATABASE_STRING = "Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True"

PORT = "COM3"
BAUD_RATE = 115200

def initTransceiver():
    print("============================================================")
    print("WIRELESS COMMUNICATION TEST")
    print("============================================================")
    print("Connecting to Local Database.")
    conn = pyodbc.connect(DATABASE_STRING)
    
    myDBManager = DatabaseManager(conn)
    
    mySerialMsgManager = SerialMsgManager(myDBManager, SAMPLE_NUM, TRANS_DELIM, SMALL_TRANS_DELAY, BIG_TRANS_DELAY, SLEEP_TIME)
        
    print("Initializing XBee Device.")
    device = XBeeDevice(PORT, BAUD_RATE)
    myTransceiver = XBeeTransceiver(device, myDBManager, mySerialMsgManager)
    print("Initializing Transceiver Program.")
    myTransceiver.initTransceiver()
    print("Launching Transceiver Program.\n")   
    myTransceiver.runTransceiver()
    
    print("\n")
    return

initTransceiver()