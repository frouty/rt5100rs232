# -*- coding: utf-8 -*-
import re
import sys

#constant
# i  faut que j'arrive à récuperer dans un tuple les lignes entre deux @"
try:
    #open the fil
    file=open('/home/lof/rt5100rs232/tmp.log','r')
    for line in file.readlines():
        print '-'*6
        print line
        atpos=line.find('@')
        print 'atpos:%s' % (atpos)
        Opos=line.find('O')
        print 'Opos:%s' % (Opos)
        Endlinepos=line.find('\n')
        print 'Endlinepos:%s' % (Endlinepos)
        
    else: print 'nop'
except IOError, (error,strerror):
    print "I/O Error(%s): %s" % (error,strerror)
