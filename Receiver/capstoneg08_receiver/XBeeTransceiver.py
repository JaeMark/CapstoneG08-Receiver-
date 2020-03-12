# -*- coding: utf-8 -*-
from digi.xbee.exception import TimeoutException
import threading
import time

#===============================================================
# CONSTANT VARIABLES
#===============================================================
DEFAULT_COMMAND = 0
START_RECEIVING_COMMAND = 1
WAIT_FOR_WAKE_UP_COMMAND = 2

DEFAULT_NUM_SAMPLES = 0
HANDSHAKE_TIMEOUT = 30 #s
SAMPLE_TIMEOUT = 30 #s

class XBeeTransceiver(threading.Thread):
    def __init__(self, device, SerialMsgManager):
        self.device = device
        self.mySerialMsgManager = SerialMsgManager
        
    def initTransceiver(self):
        # initialize the transceiver program
        try:
            # open XBee device
            if self.device is not None and not self.device.is_open():
                self.device.open()
                self.device.flush_queues()                         
        except TimeoutException as to:
            print("Unable to get device from Xbee network, because ", repr(to))
            if self.device is not None and self.device.is_open():
                self.device.close()

    def runTransceiver(self):
        # run the transceiver program
        transceiverCmd = DEFAULT_COMMAND
        numSamplesToReceive = DEFAULT_NUM_SAMPLES
        
        while(True):
            if transceiverCmd is DEFAULT_COMMAND:  
                try:
                    # get the start command from the database, then send it
                    self.device.flush_queues
                    startCommandToSend = self.mySerialMsgManager.getStartCommand()
                    print("Sending data %s..." % (startCommandToSend))
                    self.device.send_data_broadcast(startCommandToSend)
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
                            transceiverCmd, numSamplesToReceive = self.mySerialMsgManager.parseHandshake(data)
                            break
                except TimeoutException as to:
                    print("Unable to receive data, because ", repr(to))
                    if self.device is not None and self.device.is_open():
                        self.device.close()
                if transceiverCmd is not START_RECEIVING_COMMAND:    
                    # the handshake was not received; resend the start command
                    print("There was no response from the remote device. Resending start command...")
                    
            elif transceiverCmd is START_RECEIVING_COMMAND:                    
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
                            threading.Thread(target = self.mySerialMsgManager.parseReadingData(msgToParse)).start() 
                            lastSampleTime = time.monotonic()                        
                        if self.mySerialMsgManager.getSampleNumParsed() == numSamplesToReceive:
                            # all samples have been received; send a sleep command
                            self.device.flush_queues
                            self.mySerialMsgManager.setSampleNumToParse(DEFAULT_NUM_SAMPLES)
                            sleepCommandToSend = self.mySerialMsgManager.getSleepCommand()
                            print("Parsed all sample data. Time to sleep!\nSending sleep command %s...\n" % (sleepCommandToSend))
                            self.device.send_data_broadcast(sleepCommandToSend)   
                            transceiverCmd = WAIT_FOR_WAKE_UP_COMMAND
                            break  
                        elif time.monotonic() > lastSampleTime + SAMPLE_TIMEOUT:
                            # timeout has occured; restart transmission
                            print("Data sample was not received within the expected time. Restarting transmission...")
                            transceiverCmd = DEFAULT_COMMAND
                            self.mySerialMsgManager.deleteSampleParsed(numSamplesToReceive)
                            self.mySerialMsgManager.setSampleNumToParse(DEFAULT_NUM_SAMPLES)
                            self.device.flush_queues
                            break
                except TimeoutException as to:
                    print("Unable to receive data, because ", repr(to))
                    if self.device is not None and self.device.is_open():
                        self.device.close()
                        
            elif transceiverCmd is WAIT_FOR_WAKE_UP_COMMAND:
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
                                transceiverCmd = DEFAULT_COMMAND
                                break
               except TimeoutException as to:
                    print("Unable to receive data, because ", repr(to))
                    if self.device is not None and self.device.is_open():
                        self.device.close()