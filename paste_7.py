# -*- coding: utf-8 -*-
with open('/home/lof/rt5100rs232/tmp.log','r') as infile:
    for line in infile:
        #if line.find('FR') !=-1:
         #   print line.find('FR')
        #constants
        R=('sph_od','cyl_od','axe_od')
        L=('sph_os','cyl_os','axe_os')
        
        MyDict={'FinalPrescriptionData':['FarVisionSCA','NearVisionSCA','ADD'],'SubjectiveData':['FarVisionSCA','NearVisionSCA','ADD']}
        for token in ('F','O','f','A'): #with those leading character there is always a SCA data template
            #F is for final prescription data SCA far vision
            #O is for objective SCA from AR
            #F is for Subjective Data Far vision SCA
            #A is for ADD
            if token in line:
            #print line
                print 'formated line:%s' % (line[line.find(token):])
            # je voudrais parser dans un dictionnaire
            #FinalSCA={'sph_od':'value','cyl_od':'value','axe_od:'value'}
                fl=line[line.find(token):].rstrip()
                print "after rstriping:{}".format(fl)
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