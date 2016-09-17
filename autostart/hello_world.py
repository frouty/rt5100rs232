#!/usr/bin/python
from time import sleep
import logging

logging.warning( 'Starts Hello World' )
try:
    while True:
        print "Hello World"
        sleep( 60 )
except KeyboardInterrupt, e:
    logging.warning( "Stopping..." )
