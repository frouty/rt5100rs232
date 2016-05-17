# -*- coding: utf-8 -*-
parsing = False
with open('/home/lof/rt5100rs232/tmp.log','r') as infile, open('/home/lof/rt5100rs232/out.log','w') as outfile:
    for line in infile:
        if line.find('@') != -1:
            if parsing:
                parsing=False
                print 'Parsing is: %s Et je fais quoi de cette ligne:%s' % (parsing, line)
            else:
                parsing=True
                print 'Parsing is: %s Et je fais quoi de cette ligne:%s' % (parsing, line)
        if parsing:
           print 'Parsing is: %s Et je fais quoi de cette ligne:%s' % (parsing, line)
