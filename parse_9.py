# -*- coding: utf-8 -*-
SCAdict={'f':('subjectdata','FarVisionSCA'),
              'n':('subjectdata','NearVisionSCA'),
              'F':('finalprescriptiondata','FarVisionSCA)'),
              'N':('finalprescriptiondata','NearVisionSCA'),
              'O':('ARdata','ObjectiveSCA'),
               }
keysOR = ('sph_od','cyl_od','axe_od')
keysOS = ('sph_os','cyl_os','axe_os')

# Les points de coupures semblent etre toujours les memes
# les données recherchées peuvent etre récupérée par l'index
# S=morceaux[1] C=morceaux[2] A=Morceaux[3]
#constant
coupures = [28, 30, 36, 42, 45] 

try:
    file=open('/home/lof/rt5100rs232/tmp.log','r')
    for line in file.readlines():
        if line.find('FR') != -1 or line.find('FL')!=-1:
            morceaux=[line[i:j] for i,j in zip([0] +coupures,coupures+[None])]
            values=morceaux[1:5]
            if values[0] == '':
                valuesOD=dict(zip(keysOR,values))
            print '-'*6
            print 'line:{}'.format(line)
            print 'morceaux:%s ' % (morceaux)
            print "morceaux[1:5]:{}".format(morceaux[1:5])
            print '{} SCA:{},{},{}'.format(morceaux[1],morceaux[2],morceaux[3],morceaux[4])
            
except IOError, (error,strerror):
    print "I/O Error(%s): %s" % (error,strerror)

