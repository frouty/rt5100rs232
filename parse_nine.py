# -*- coding: utf-8 -*-

#constant
# i  faut que j'arrive à récuperer dans un tuple les lignes entre deux @"
try:
    #open the fil
    file=open('/home/lof/rt5100rs232/tmp.log','r')
    for line in file.readlines():
        print 'raw line: {}'.format(line)
        print "Will try to find the ascii character start of text : \02"
        if line.find('\02') != -1:
            print 'find it'
            print 'line:{}'.format(line[line.find('\02')+1:])
        else:
            print "didn't find it"
        if 'FR' in line:
            print "oui il y a 'FR' dans cette ligne"
            print "met la donnée au bon endroit dans le dictionnaire"
        else:
            print "non il n'y a pas FR"
        print '-'*9


except IOError, (error,strerror):
    print "I/O Error(%s): %s" % (error,strerror)
