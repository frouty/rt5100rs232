# -*- coding: utf-8 -*-
"""
"""
import formatSCAvalues_final as trimSCA

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

def get_values(filter):
    """Return a dictionnary of the values
    
        filter(str) : the letter from the interface manual rs-232 of RT-5100
        Il y a un probleme quand il n'y a aucune ligne qui correspond au filtre
        log_path : path to the file with the datas given by RT-5100 device
        
        return : tuple .vals:({'cyl_od': '- 1.25', 'axe_od': '125', 'sph_od': '+ 5.50'}, {'sph_os': '+ 5.50', 'axe_os': '125', 'cyl_os': '- 1.25'})
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
                    morceaux = [line[i:j] for i, j in zip([0] + coupures, coupures + [None])] # on coupe les lignes en morceaux qui isolent les champs.
                    values=morceaux[1:5] # on élimine le champ date et on récupere que les champs datas.
                    #print '-' * 6
                    #print 'line:{}'.format(line)
                    #print 'morceaux:%s ' % (morceaux)
                    #print 'values:{}'.format(values)
                    #print '{} SCA:{},{},{}'.format(morceaux[1], morceaux[2], morceaux[3], morceaux[4])
                    if values[0] == filterR: # On filtre pour l'oeil droit
                        valuesOD=dict(zip(keysOR,values[1:]))
                        #print 'valuesOD:{}'.format(valuesOD)
                    else:
                        valuesOS=dict(zip(keysOS,values[1:])) #on filtre pour l'oeil gauche
                        #print 'valuesOS:{}'.format(valuesOS)

        except IOError, (error, strerror):
            print "I/O Error(%s): %s" % (error, strerror)
   # print 'locals():{}'.format(locals())
    #print 'done'
   # print '-'*10
    res=[valuesOD, valuesOS]
    return res

def trim(vals):
    """Trim the values of the dictionnary
    
    delete the space after '+' or '-' if there is one
    delete the 0 if there is on on second decimal
    
    vals: param tuple of dictionnaries
    return a tuple of dictionnaries with trimed values
    
    """
    for i in vals:
        for k,v in i.itertems():
            i[k]=trim.trimspace(v)
    return True

if __name__ == '__main__':
    vals = get_values("O")
    print 'vals:{}'.format(vals)
    print 'OD:{}'.format(vals[0])
    print 'OG:{}'.format(vals[1])
    print '='*10
    print "now let's trim"
    for i in vals: #j'itere sur chaque dictionnaire.
        print 'i:{}'.format(i) # dict pour un oeil . vals[0] dictionnaire 1 et vals[1] dictionnaire 2
        print 'values:{}'.format(i.values()) # list des values
        for k, v in i.iteritems(): # est un value
            print 'v :{}'.format(v)
            i[k]=trimSCA.main_trim(v)
            #[k]=trimSCA.trimspace(trimSCA.trimzero(v))
#             i[k]=trimSCA.trimspace(v)
#             i[k]=trimSCA.trimzero(i[k])
            #i[k]=trim.trimzero(i[k])
            #trimed = trim.trimspace(v)
            #print 'trim space : {}'.format(i[k])
            #trimed = trim.trimzero(trimed)
            #print 'trim zero : {}'.format(trimed)
        print '-'*10
        print i.values()
        print i
    #===========================================================================
    # for i in SCAdict.keys():
    #     print '='*10
    #     get_values(i)
    #===========================================================================
       
   
