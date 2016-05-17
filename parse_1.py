# -*- coding: utf-8 -*-
import re
import sys

#constant
# i  faut que j'arrive à récuperer dans un tuple les lignes entre deux @"
try:
    #open the fil
    file=open('/home/lof/rt5100rs232/tmp.log','r')
    for line in file.readlines():
        print 'raw line: {}'.format(line)
        if line.startswith("2016"):
            print 'it start with 2016'
        print 'line.strip():%s' %(line.strip())
        print 'line.split():%s' %(line.split())
        atpos=line.find('@')
        print 'atpos:%s' % (atpos)
        print "Will try to find the ascii character start of text : \02"
        if line.find('\02') != -1:
            print 'find it'
            print 'line:{}'.format(line[line.find('\02')+1:])
        else:
            print "didn't find it"
        print 'find : {}'.format(line.find('\x02'))
        print 'strip: {}'.format(line.rstrip('\x02'))
        #print 'rstrip line:{}'.format(line.rstrip(line.find('\x02')+1))
        print 'find : {}'.format(line.find('O'))
        print '-'*6
        
    else: print 'nop'
except IOError, (error,strerror):
    print "I/O Error(%s): %s" % (error,strerror)
