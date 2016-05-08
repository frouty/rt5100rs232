# -*- coding: utf-8 -*-
with open('/home/lof/rt5100rs232/tmp.log','r') as infile:
    for line in infile:
        #if line.find('FR') !=-1:
         #   print line.find('FR')
        
        for token in ('F','O','f'):
            if token in line:
            #print line
                print 'formated line:%s' % (line[line.find(token):])
            # je voudrais parser dans un dictionnaire
            #FinalSCA={'sph_od':'value','cyl_od':'value','axe_od:'value'}
                fl=line[line.find(token):].rstrip()
                (s,c,a)=(fl[2:8],fl[8:14],fl[14:])
                print 'SCA:%s %s %s' % (s,c,a)
                k=('sph_od','cyl_od','axe_od')
                FinalSCA=dict(zip(k,(s,c,a)))
                print 'FinalSCA:%s' % (FinalSCA)
        