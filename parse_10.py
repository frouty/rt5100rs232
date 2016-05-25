# -*- coding: utf-8 -*-
"""
"""
import formatSCAvalues_final as trimSCA
import re

SCAdict={'f':('subjectdata','FarVisionSCA'),
              'n':('subjectdata','NearVisionSCA'),
              'F':('finalprescriptiondata','FarVisionSCA)'),
              'N':('finalprescriptiondata','NearVisionSCA'),
              'O':('ARdata','ObjectiveSCA'),
               }
keysOR = ('sph_od','cyl_od','axe_od','add_od')
keysOS = ('sph_os','cyl_os','axe_os','add_os')
#print 'hello'
# Les points de coupures semblent etre toujours les memes
# les données recherchées peuvent etre récupérée par l'index
# S=morceaux[1] C=morceaux[2] A=Morceaux[3]
#constant
coupures = [28, 30, 36, 42, 45] 



def trimzero(val):
    """Trim zero value if there is one at the 2nd decimal
    needed if there is a selection fields with no zero at the 2nd decimal
    in Odoo
    
    val : string from the rt5100
    
    example: '+ 2.20' return '+ 2.2'
    example: '100' return '100'
    """
    res = val
    regex = r'\.\d0'
    if re.search(regex, val, flags = 0):
        #match = re.search(regex, val, flags = 0)
        #print 'match:{}'.format(match)
        if val[-1] == '0':
            res = val[:-1]
    return res

def trimspace_regex(val):
    """Trim the space after sign +/- if there is one in val
    val : string from rt-5100
    eg val = '+ 2,00'  --> return '+2.00'
    eg val ='  0,00'   --> return '  0.00'

    return the trimed string
    """
    regex=r'^[+-] ' # don't forget the space at the end of the regex
    if re.search(regex, val, flags = 0):
        #match = re.search(regex, val, flags = 0)
        #print 'match:{}'.format(match)
        val=val[:1]+val[2:]
    return val

def cut_timestamp(line,lenght=28):
    """Trim the timestamp
    
    because I don't need it and the timestamp is always the same lengh 
    exept if you change the code in the getting program from the rt5100
    
    line : str line from the data file
    lenght : int lenght of the timestamp
    
    return : str the line without the timestamp.
    """
    res=line[lenght:]
    return res

def cutting(line,coupures):
    """ Cut the line in a list fields of datas
    
    line : str
    coupures: list with size for cutting. depends on description of datas
    
    return: list of fields of datas 
    eg return: values:['FR', '- 2.00', '  0.00', '  0']; ['AL', '+ 1.50']
    """
    morceaux = [line[i:j] for i, j in zip([0] + coupures, coupures + [None])] # on coupe les lignes en morceaux qui isolent les champs.
    values=morceaux[1:-1] # on élimine le champ date et on récupere que les champs datas.SCA dans une liste
    #print 'values:{0} ; morceaux:{1}'.format(values,morceaux)
    return values

def get_value(line):
    """Cut the line from file with rt5100 datas
    into a list of fields
    
    The cutting is different depending on the type of data text
    
    return : list
    """
    cuttingDict={  'a':[28,30,36], # a if for add. 28 cut the timpstamp, 30 the data type and R or L, 36 the value= '+' 'dizaine unité' 'dot' 'decimal1' 'decimal2'
                    'A':[28,30,36], # A for addition
                    'f':[28, 30, 36, 42, 45],
                    'F':[1,7,13,16],
                    'O':[1,7,13,16],
                    'n': [28, 30, 36, 42, 45],
                    'N': [28, 30, 36, 42, 45],
                    }
    regexADD=r'[Aa][RL]'
    regexSCA=r'[OfFnN][RL]'
    
    values=[]
    
    if re.search(regexSCA,line, flags=0): # j'ai une ligne avec des datas de type SCA attention il n'y plus de timstamp je coupe en consequence
        values= cutting(line, coupures=[28, 30, 36, 42, 45])
        values=[val.strip() for val in values]
        values=[trimspace_regex(val) for val in values]
    if re.search(regexADD,line,flags=0):
        values=cutting(line,coupures=[28,30,36])
        values=[val.strip() for val in values]
        values=[trimspace_regex(val) for val in values]
        
    else:pass
    
    res=[valuesOD, valuesOS]
    print 'res:{}'.format(res)
    return res
    
    
    #===========================================================================
    # if values[0][1] == 'R': # On filtre pour l'oeil droit
    #         valuesOD=dict(zip(keysOR,values[1:]))
    #         print 'valuesOD:{}'.format(valuesOD)
    #     else:
    #         valuesOS=dict(zip(keysOS,values[1:])) #on filtre pour l'oeil gauche
    #         print 'valuesOS:{}'.format(valuesOS)
    #     values =[valuesOD, valuesOS]
    #     print 'values:{}'.format(res)
    # 
    #===========================================================================
    
#     if line.find(filterR) != -1 or line.find(filterL) != -1:
#         morceaux = [line[i:j] for i, j in zip([0] + coupures, coupures + [None])] # on coupe les lignes en morceaux qui isolent les champs.
#         values=morceaux[1:5]
#     else : return True
#     return morceaux, values
    
def get_values_ori(filter):
    """Return a dictionnary of the values
    
        filter(str) : the letter from the interface manual rs-232 of RT-5100
        Il y a un probleme quand il n'y a aucune ligne qui correspond au filtre
        log_path : path to the file with the datas given by RT-5100 device
        
        values: eg : values:['OR', '- 2.75', '  0.00', '  0']
        
        morceaux : eg : ['2016-05-02T05:37:02.410503\t\x02', 'OR', '- 2.75', '  0.00', '  0', '\r\n']
        return : tuple .vals:({'cyl_od': '- 1.25', 'axe_od': '125', 'sph_od': '+ 5.50'}, {'sph_os': '+ 5.50', 'axe_os': '125', 'cyl_os': '- 1.25'})
    """
    coupures = [28, 30, 36, 42, 45] 
    filterR = filter+'R'
    print 'filterR:{}'.format(filterR)
    filterL = filter+'L'
    print 'filterL;{}'.format(filterL)
   
    if filter not in ['f','n','F','N','O']:
        print "print there is a problem with your filter:{}".format(filter)
        print "{} is not a code for RT-5100 datas".format(filter)
    else:
        try:
            file = open('tmp.log', 'r')
            for line in file.readlines():
                if line.find(filterR) != -1 or line.find(filterL) != -1:
                    morceaux = [line[i:j] for i, j in zip([0] + coupures, coupures + [None])] # on coupe les lignes en morceaux qui isolent les champs.
                    values=morceaux[1:5] # on élimine le champ date et on récupere que les champs datas.SCA dans une liste
                    # morceaux[2] --> sph 6 bits datas
                    # morceaux[3] --> cyl 6 bits datas
                    # morceaux[4] --> axes 6 bits datas
                    # morceaux[2:5] donne ['S','C','A']
                    # lets format the str to fit the odoo selection for SCA
                    values=[val.strip() for val in values]
                    print 'values stripped:{}'.format(values)
                    values=[trimspace_regex(val) for val in values]
                    print 'values trimspace:{}'.format(values)
                    values=[trimzero(val) for val in values]
                    print 'values trimzero:{}'.format(values)
                    print 'formated values:{}'.format(values)
                    
                    if values[0] == filterR: # On filtre pour l'oeil droit
                        valuesOD=dict(zip(keysOR,values[1:]))
                        print 'valuesOD:{}'.format(valuesOD)
                    else:
                        valuesOS=dict(zip(keysOS,values[1:])) #on filtre pour l'oeil gauche
                        print 'valuesOS:{}'.format(valuesOS)

        except IOError, (error, strerror):
            print "I/O Error(%s): %s" % (error, strerror)

    res=[valuesOD, valuesOS]
    print 'res:{}'.format(res)
    return res

def trimspace(val):
    idx = 1
    val = val.strip()
    if val[1] == ' ':
        res = val[:idx] + val[(idx + 1):]
    else:
        res = val
    return res

def trimzero(val):
    res = val
    regex = r'\.\d0'
    if re.search(regex, val, flags = 0):
        match = re.search(regex, val, flags = 0)
        print 'match:{}'.format(match)
        if val[-1] == '0':
            res = val[:-1]
    return res

def main_trim(val):
    """ Apply trimzero and trimspace
    
        return: string the trimed val
    """
    print 'in main_trim val is {}'.format(val)
    res = trimspace(trimzero(val))
    print 'in main_trim res is {}'.format(res)
    return res

def main_get(vals):
    """Get the SCA values ready for ODOO
    
        vals tuple of dictionnaries from get values
        
        return: tuple of dictionnaryes of values trimed
    """
    for i in vals:
        for k, v in i.iteritems():
            i[k] = main_trim(v)
    return vals


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
    
    try:
            file = open('tmp.log', 'r')
            for line in file.readlines():
                print get_value(line)
                
    except IOError, (error, strerror):
            print "I/O Error(%s): %s" % (error, strerror)
    #===========================================================================
    # for i in SCAdict.keys():
    #     print '='*10
    #     get_values(i)
    #===========================================================================
       
   
