#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
from datetime import datetime
 
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
while ser.isOpen():
    datastring=ser.read(size=bitlenght)
    print datetime.utcnow().isoformat(), datastring

ser.close()
