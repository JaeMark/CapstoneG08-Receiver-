# -*- coding: utf-8 -*-
from digi.xbee.exception import TimeoutException
import threading
import time

#==============================================================================
# CONSTANT VARIABLES
#==============================================================================
DEFAULT_COMMAND = 0
START_RECEIVING_COMMAND = 1
WAIT_FOR_WAKE_UP_COMMAND = 2

REMOTE_NODE_ID = 'XBEE_T'

DEFAULT_NUM_SAMPLES = 0
HANDSHAKE_TIMEOUT = 120 #s
SAMPLE_TIMEOUT = 60 #s

class XBeeTransceiver(threading.Thread):
    def __init__(self, device, dBManager, SerialMsgManager):
        self.device = device
        self.myDBManager = dBManager
        self.mySerialMsgManager = SerialMsgManager
        
    def initTransceiver(self):
        # initialize the transceiver program
        try:
            # open XBee device
            if self.device is not None and not self.device.is_open():
                self.device.open()
                self.device.flush_queues()
            # Obtain the remote XBee device from the XBee network.
#            xbee_network = self.device.get_network()
#            self.remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
#            if self.remote_device is None:
#                print("Could not find the remote device")
#                exit(1)
             
        except TimeoutException as to:
            print("Unable to get device from Xbee network, because ", repr(to))
            if self.device is not None and self.device.is_open():
                self.device.close()

    def runTransceiver(self):
        # run the transceiver program
        TransCommand = DEFAULT_COMMAND
        numSamples = DEFAULT_NUM_SAMPLES
        
        while(True):
            if TransCommand is DEFAULT_COMMAND:  
                try:
                    # get the start command from the database, then send it
                    self.device.flush_queues
                    startCommandToSend = self.mySerialMsgManager.getStartCommand()
                    print("Sending data %s..." % (startCommandToSend))
                    self.device.send_data_broadcast(startCommandToSend)
                    #print("Sending data to %s >> %s..." % (remote_device.get_64bit_addr(), startCommandToSend))
                    #self.device.send_data(self.remote_device, startCommandToSend)
                except TimeoutException as to:
                    print("Unable to send command, because ", repr(to))
                    if self.device is not None and self.device.is_open():
                        self.device.close()         
                try:
                    # wait for a notification that the microcontroller has received the start command
                    handshakeTimeout = time.monotonic() + HANDSHAKE_TIMEOUT
                    while time.monotonic() < handshakeTimeout:
                        packet = self.device.read_data()
                        if packet is not None:
                            # the handshake has been received
                            data = packet.data.decode()
                            print("The handshake data is: " + data)
                            TransCommand, numSamples = self.mySerialMsgManager.parseHandshake(data)
                            break
                except TimeoutException as to:
                    print("Unable to receive data, because ", repr(to))
                    if self.device is not None and self.device.is_open():
                        self.device.close()
                if TransCommand is not START_RECEIVING_COMMAND:    
                    # the handshake was not received; resend the start command
                    print("There was no response from the remote device. Resending start command...")
                    
            elif TransCommand is START_RECEIVING_COMMAND:                    
                try: 
                    print("\nThe Transceiver is now waiting for data...\n")
                    data = ''
                    trailingData = ''
                    msgToParse = ''
                    lastSampleTime = time.monotonic()
                    while(True):
                        # receive samples from the microcontroller
                        packet = self.device.read_data()
                        if packet is not None:
                            decodedData = packet.data.decode()
                            data = trailingData + decodedData   
                            msgToParse = self.mySerialMsgManager.getMsgToParse(data)
                            trailingData = self.mySerialMsgManager.getTrailingData(data)
                            #print("The data is: " + data)
                            #print("The message to parse is: " + msgToParse)
                            #print("The trailing data is: " + trailingData)
                            threading.Thread(target = self.mySerialMsgManager.parseReadingData(msgToParse, numSamples)).start() 
                            lastSampleTime = time.monotonic()
                        elif self.mySerialMsgManager.getSampleNumParsed() == numSamples:
                            # all samples have been received; send a sleep command
                            sleepCommandToSend = self.mySerialMsgManager.getSleepCommand()
                            print("Parsed all sample data. Time to sleep!\nSending sleep command %s...\n" % (sleepCommandToSend))
                            #self.device.send_data_broadcast(sleepCommandToSend)   
                            self.mySerialMsgManager.setSampleNumToParse(DEFAULT_NUM_SAMPLES)
                            TransCommand = WAIT_FOR_WAKE_UP_COMMAND
                            self.device.flush_queues
                            break  
                        elif time.monotonic() > lastSampleTime + SAMPLE_TIMEOUT:
                            print("Data sample was not received within the expected time. Restarting transmission...")
                            TransCommand = DEFAULT_COMMAND
                            break
                except TimeoutException as to:
                    print("Unable to receive data, because ", repr(to))
                    if self.device is not None and self.device.is_open():
                        self.device.close()
                        
            elif TransCommand is WAIT_FOR_WAKE_UP_COMMAND:
               try: 
                    print("The Transceiver is now waiting for wake up command...\n")
                    while(True):
                        # wait until the microcontroller is awake  
                        packet = self.device.read_data()
                        if packet is not None:
                            decodedData = packet.data.decode() 
                            if self.mySerialMsgManager.parseWakeUpCommand(decodedData):
                                # received the wake up handshake
                                print("The Teensy is now awake!\n")
                                TransCommand = DEFAULT_COMMAND
                                break
               except TimeoutException as to:
                    print("Unable to receive data, because ", repr(to))
                    if self.device is not None and self.device.is_open():
                        self.device.close()