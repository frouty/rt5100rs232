# -*- coding: utf-8 -*-

try:
    #open the fil
    file=open('/home/lof/rt5100rs232/tmp.log','r')
    for line in file.readlines():
        print 'line:%s' %(line,)
        print 'line.split():%s' % (line.split())
        print 'type(line.split()[-1]):{}'.format(type(line.split()[-1]))
        print 'line.split()[-1]: {}'.format(line.split()[-1])
        if len(line.split()[-1]) == 1:
            print "{0:02x}".format(ord(line.split()[-1])) # get the hexadecimal code
            print line.split()[-1].encode("hex") # get hexadecimal code same as above.
        else: print 'skip'
except IOError, (error,strerror):
    print "I/O Error(%s): %s" % (error,strerror)
