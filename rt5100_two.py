#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import os
import time


ser.Serial()

ser.port='/dev/ttyUSB0'
ser.baudrate = 24001  # Set baud rate
ser.bytesize=7
ser.parity=serial.PARITY_EVEN
ser.stopbits=serial.STOPBITS_TWO

# ser.timeout = None          #block read
ser.timeout = 1  # non-block read
# ser.timeout = 2              #timeout block read

ser.xonxoff = False  # disable software flow control
ser.rtscts = False  # disable hardware (RTS/CTS) flow control
ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control