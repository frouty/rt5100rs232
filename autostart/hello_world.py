#!/usr/bin/python
from time import sleep
import logging

logging.warning( 'Starts Hello World' )
try:
    while True:
        print "Hello World"
	logging.warning('Je suis la')
        sleep( 5 )
except KeyboardInterrupt, e:
    logging.warning( "Stopping..." )
