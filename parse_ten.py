# -*- coding: utf-8 -*-
"""
"""
SCAdict={'f':('subjectdata','FarVisionSCA'),
              'n':('subjectdata','NearVisionSCA'),
              'F':('finalprescriptiondata','FarVisionSCA)'),
              'N':('finalprescriptiondata','NearVisionSCA'),
              'O':('ARdata','ObjectiveSCA'),
               }
keysOR = ('sph_od','cyl_od','axe_od')
keysOS = ('sph_os','cyl_os','axe_os')
#print 'hello'
# Les points de coupures semblent etre toujours les memes
# les données recherchées peuvent etre récupérée par l'index
# S=morceaux[1] C=morceaux[2] A=Morceaux[3]
#constant
coupures = [28, 30, 36, 42, 45] 

SCAdict={'f':('subjectdata','FarVisionSCA'),
              'n':('subjectdata','NearVisionSCA'),
              'F':('finalprescriptiondata','FarVisionSCA)'),
              'N':('finalprescriptiondata','NearVisionSCA'),
              'O':('ARdata','ObjectiveSCA'),
               }

def get_values(filter):
    """Return a dictionnary of the values
    
        filter(str) : the letter from the interface manual rs-232 of RT-5100
        
    """
    coupures = [28, 30, 36, 42, 45] 
    filterR = filter+'R'
    filterL = filter+'L'
   
    if filter not in ['f','n','F','N','O']:
        print "print there is a problem with your filter:{}".format(filter)
        print "{} is not a code for RT-5100 datas".format(filter)
    else:
        try:
            file = open('tmp.log', 'r')
            for line in file.readlines():
                if line.find(filterR) != -1 or line.find(filterL) != -1:
                    morceaux = [line[i:j] for i, j in zip([0] + coupures, coupures + [None])]
                    values=morceaux[1:5]
                    print '-' * 6
                    print 'line:{}'.format(line)
                    print 'morceaux:%s ' % (morceaux)
                    print 'values:{}'.format(values)
                    print '{} SCA:{},{},{}'.format(morceaux[1], morceaux[2], morceaux[3], morceaux[4])
                    if values[0] == filterR:
                        valuesOD=dict(zip(keysOR,values[1:]))
                        print 'valuesOD:{}'.format(valuesOD)
                    else:
                        valuesOS=dict(zip(keysOS,values[1:]))
                        print 'valuesOS:{}'.format(valuesOS)
            
        except IOError, (error, strerror):
            print "I/O Error(%s): %s" % (error, strerror)

if __name__ == '__main__':
    for i in SCAdict.keys():
        print '='*10
        get_values(i)
       
   
