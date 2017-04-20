#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import zmq 

continue_reading = True

class ReadRFID(object):
    def __init__(self):
        # Capture SIGINT for cleanup when the script is aborted
        def end_read(signal,frame):
            global continue_reading
            print "Ctrl+C captured, ending read."
            continue_reading = False
            del self.socket
            GPIO.cleanup()

        # Hook the SIGINT
        signal.signal(signal.SIGINT, end_read)

        # Create an object of the class MFRC522
        MIFAREReader = MFRC522.MFRC522()

        # Welcome message
        print "Welcome to the MFRC522 data read example"
        print "Press Ctrl-C to stop."
        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        global continue_reading
        
        #zmq local server for communicating with kivy app
        context = zmq.Context()
        self.socket = context.socket(zmq.PAIR)
        self.socket.bind("tcp://*:5555")

        while continue_reading:
            
            # Scan for cards    
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # If a card is found
            if status == MIFAREReader.MI_OK:
                print "Card detected"
            
            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:

                # Print UID
                UID = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
                print "Card read UID: "+ UID
                
                #send message using zmq server
                self.socket.send(b'%s'%(UID))

                # This is the default key for authentication
                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                
                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                # Check if authenticated
                if status == MIFAREReader.MI_OK:
                    MIFAREReader.MFRC522_Read(8)
                    MIFAREReader.MFRC522_StopCrypto1()
                else:
                    print "Authentication error"



