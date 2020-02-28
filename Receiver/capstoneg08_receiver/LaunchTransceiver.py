# -*- coding: utf-8 -*-
from digi.xbee.devices import XBeeDevice
from DatabaseManager import DatabaseManager
from XBeeTransceiver import XBeeTransceiver
from SerialMsgManager import SerialMsgManager

#===============================================================
# EXTERNAL LIBRARY REFERENCES
#***************************************************************
#*  Title: Digi XBee Python library
#*  Author: Digi International Inc.
#*  Date: 2019
#*  Code version: 1.3.0
#*  Availability: https://github.com/digidotcom/xbee-python
#***************************************************************
#===============================================================

#===============================================================
# CONSTANT VARIABLES
#===============================================================

DATABASE_STRING = "Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True"

SAMPLE_NUM = 2000
TRANS_DELIM = 16
SMALL_TRANS_DELAY = 500
BIG_TRANS_DELAY = 1000
SLEEP_TIME = 3600000

PORT = "COM3"
BAUD_RATE = 115200

def initTransceiver():
    print("========================================================")
    print("Workstation Transceiver Program")
    print("========================================================")
    print("Connecting to Local Database.")
    myDBManager = DatabaseManager(DATABASE_STRING)
    
    mySerialMsgManager = SerialMsgManager(myDBManager, SAMPLE_NUM, TRANS_DELIM, SMALL_TRANS_DELAY, BIG_TRANS_DELAY, SLEEP_TIME)
        
    print("Initializing XBee Device.")
    device = XBeeDevice(PORT, BAUD_RATE)
    myTransceiver = XBeeTransceiver(device, mySerialMsgManager)
    print("Initializing Transceiver Program.")
    myTransceiver.initTransceiver()
    print("Launching Transceiver Program.\n")   
    myTransceiver.runTransceiver()
    
    print("\n")
    return

initTransceiver()