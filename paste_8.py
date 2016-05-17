# -*- coding: utf-8 -*-
#constants
R=('sph_od','cyl_od','axe_od')
L=('sph_os','cyl_os','axe_os')
        
RTdata=('subjectdata','finalprescriptiondata')
datatype=('FarVisionSCA','NearVisionSCA','ADD')
SCAdict={'f':('subjectdata','FarVisionSCA'),
              'n':('subjectdata','NearVisionSCA'),
              'F':('finalprescriptiondata','FarVisionSCA)'),
              'N':('finalprescriptiondata','NearVisionSCA'),
              'O':('ARdata','ObjectiveSCA'),
               }

with open('/home/lof/rt5100rs232/tmp.log','r') as infile:
    for line in infile:
        #if line.find('FR') !=-1:
         #   print line.find('FR')
        #constants
        
        #print 'SCAdict: {}'.format(SCAdict.keys())
        #MyDict={'FinalPrescriptionData':['FarVisionSCA','NearVisionSCA','ADD'],'SubjectiveData':['FarVisionSCA','NearVisionSCA','ADD']}
        for token in SCAdict.keys(): #with those leading character there is always a SCA data template
            if token in line:
                #print 'formated line:%s' % (line[line.find(token):])
                fl=line[line.find(token):].rstrip()
                #print "after rstriping:{}".format(fl)
                #print "lenght of line:{}".format(len(fl))
                (s,c,a)=(fl[2:8],fl[8:14],fl[14:]) # c'est toujours comme cela. En fonction de la valeur des deux premiers character on va associer ce SCA à une clef diférente
                print 'SCA:%s %s %s' % (s,c,a)
                print 'SCA:{sph}, {cyl},{axe}'.format(sph=s,cyl=c,axe=a)
                
                #select the side 
                if fl[1] == 'R':
                    print "c'est l'oeil droit"
                    
                else:
                    print "c'est l'oeil gauche"
                FinalSCA=dict(zip(R,(s,c,a)))
                print 'FinalSCA:%s' %  (FinalSCA)
                print '-'*6
infile.close()

### est ce que je veux un dictionnaire du genre 
## result =
## keys=()