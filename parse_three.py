# -*- coding: utf-8 -*-
import re
import sys

#constant
# i  faut que j'arrive à récuperer dans un tuple les lignes entre deux @"
res=[] # j'initie une liste vide qui va contenir les lignes qui m'interessent entre deux @
try:
    #open the file
    file=open('/home/lof/rt5100rs232/tmp.log','r')
    for line in file.readlines():
        print '-'*6
        print line
        atpos=line.find('@')
        print 'will return index of @ if found in the string or -1'
        print 'atpos:%s' % (atpos)
        Opos=line.find('O')
        print 'Opos:%s' % (Opos)
        Endlinepos=line.find('\n')
        print 'Endlinepos:%s' % (Endlinepos)
        if line.find('@') == -1:
            r=False
            print 'there is no @ in the line'
        else:
            r=True
            print 'find a @ at index %s in line' %(line.find('@'))
      
except IOError, (error,strerror):
    print "I/O Error(%s): %s" % (error,strerror)
