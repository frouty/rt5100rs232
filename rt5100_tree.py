#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
 
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
    print(ser.name + ' is open...')

while True:
    cmd = raw_input("Enter command or 'exit':")
        # for Python 2
    # cmd = input("Enter command or 'exit':")
        # for Python 3
    if cmd == 'exit':
        ser.close()
        exit()
    else:
        ser.write(cmd.encode('ascii')+'\r\n')
        out = ser.read()
        print('Receiving...'+out)

