# -*- coding: utf-8 -*-
import re
import sys

constantes={'@LM':'Lensmeter',
                    '@lm':'Lensmeter nigthttime',
                    '@RM':'Autorefractometer',
                    '@rm':'Autorefractometer nighttime',
                    '@WF':'Wave front',
                    '@wf':'Wave Front nighttime',
                    '@RT':'Refractor',
                    '@rt':'Refractor nighttime',
                    'KT':'Keratometer',
                    'NT':'Tonometer',
                    }
#constant
# i  faut que j'arrive à récuperer dans un tuple les lignes entre deux @"
res=[] # j'initie une liste vide qui va contenir les lignes qui m'interessent entre deux @
switch = False #j'initie le switch à False
try:
    #open the file
    file=open('/home/lof/rt5100rs232/tmp.log','r')
    for line in file.readlines():
       if line.find('@')!=-1 and switch==False:
           print 'switch:%s' %(switch,)
           print "Set switch to True"
           switch = True
           print 'I set it to True because I found a @'
       elif switch == True: #le switch et sur On je dois récuperer les lignes
            res.append(line)
            print res
           
       else:
          # je ne trouve pas de @ ois récuperer la ligne
          print line.find('@')
          print 'there is a ' 
          res.append(line)
          print 'res is:%s' % (res)
          
except IOError, (error,strerror):
    print "I/O Error(%s): %s" % (error,strerror)
