# -*- coding: utf-8 -*-
import re
import sys

#constant
# i  faut que j'arrive à récuperer dans un tuple les lignes entre deux @"
try:
    #open the fil
    file=open('/home/lof/rt5100rs232/tmp.log','r')
    for line in file.readlines():
        print line
        if line.startswith("2016"):
            print 'it start with 2016'
        print 'line.strip():%s' %(line.strip())
        print 'line.split():%s' %(line.split())
        atpos=line.find('@')
        print 'atpos:%s' % (atpos)
        
    else: print 'nop'
except IOError, (error,strerror):
    print "I/O Error(%s): %s" % (error,strerror)
