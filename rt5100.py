#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import os
import time

#Set baud rate
br=2400
#Set timeout
to=15

# Open file to write to it
if os.path.isfile('log_rs232.txt'):
    fid=open('log_rs232.txt', )

ser=serial.Serial('/dev/ttyUSB0', 
                        baudrate=br,
                        parity=serial.PARITY_EVEN,
                        stopbits=serial.STOPBITS_TWO,
                        bytesize=serial.SEVENBITS,
                        timeout=to)    

