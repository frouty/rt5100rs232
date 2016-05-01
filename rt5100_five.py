#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
 
port = "/dev/ttyUSB0"
baud = 2400
parity=serial.PARITY_EVEN
bitlenght=serial.SEVENBITS
stopbits=serial.STOPBITS_TWO

 
ser = serial.Serial(port, 
                            baudrate=baud,
                            bytesize=bitlenght,
                            parity=parity,
                            stopbits=stopbits,
                            timeout=1)

# open the serial port
if ser.isOpen():
    print ser.name + ' is open...'
    print 'Open: ' + ser.portstr    #Quelle est la différence entre ser.portstr et ser.name.
    try:
        ser.flushInput() # def flushInput(self):Clear input buffer, discarding all that is in the buffer.
        ser.flushOutput()
    except Exeption, e1:
        print "Error " + str(e1) 

while True:
   
    bytesToRead=ser.inWaiting()  ##  Return the number of characters currently in the input buffer.def inWaiting(self):
    donnees=ser.read(bytesToRead)
    if len(donnees) > 0:
        print 'Got:', donnees
    time.sleep(5) # sleep 5 seconde
ser.close()
