#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial, io
from datetime import datetime
import logging

logging.info('Starts listener')

port = "/dev/ttyUSB0"
baud = 2400
parity = serial.PARITY_EVEN
bitlenght = serial.SEVENBITS
stopbits = serial.STOPBITS_TWO

outputfile = '/home/pi/tmp.log'

ser = serial.Serial(port,
                            baudrate = baud,
                            bytesize = bitlenght,
                            parity = parity,
                            stopbits = stopbits,
                            timeout = 1)


sio = io.TextIOWrapper(
                     io.BufferedRWPair(ser, ser, 1),
                     encoding = 'ascii',
                     newline = '\r'
                     )

with open(outputfile, 'a') as f:  # appends to existing file
    while ser.isOpen():
        datastring = sio.readline()
        if datastring :
            print 'datastring is True: {}'.format(datastring)
        # \t is tab; \n is new line
            f.write(datetime.utcnow().isoformat() + '\t' + datastring + '\n')
            f.flush()  # force the system to write to disk

ser.close()

#===============================================================================
# Voila ce que j'obtient.
# 2016-05-02T05:01:03.768399
# 2016-05-02T05:01:04.769470
# 2016-05-02T05:01:05.770541
# 2016-05-02T05:01:06.771607
# 2016-05-02T05:01:06.958712 NIDEK
# 2016-05-02T05:01:06.989709 RT-5100
# 2016-05-02T05:01:07.021705  ID
# 2016-05-02T05:01:07.053704
# 2016-05-02T05:01:07.085704   DA201
# 2016-05-02T05:01:07.117702 6/ 5/ 2
# WD3505-02T05:01:07.150701
# 2016-05-02T05:01:08.151745 
# 2016-05-02T05:01:09.152818
# 2016-05-02T05:01:10.153895
# 2016-05-02T05:01:11.154970
# 2016-05-02T05:01:12.156040
# 2016-05-02T05:01:13.157120
# 2016-05-02T05:01
#===============================================================================
