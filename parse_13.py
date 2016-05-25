# -*- coding: utf-8 -*-
import re

#constants
SCAdict={'f':('subjectdata','FarVisionSCA'),
              'n':('subjectdata','NearVisionSCA'),
              'F':('finalprescriptiondata','FarVisionSCA)'),
              'N':('finalprescriptiondata','NearVisionSCA'),
              'O':('ARdata','ObjectiveSCA'),
               }
keysOR = ('sph_od','cyl_od','axe_od')
keysOS = ('sph_os','cyl_os','axe_os')

cuttingSCA = [0,2,8,14]
cuttingADD = [0,2,8]

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

def trim_timestamp(line,lenght=28):
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
    You can use the return of this function in list comprehénsion to format the items
    """
    morceaux = [line[i:j] for i, j in zip([0] + coupures, coupures + [None])] # on coupe les lignes en morceaux qui isolent les champs.
    values=morceaux[1:-1] # on élimine le champ date et on récupere que les champs datas.SCA dans une liste
    #print 'values:{0} ; morceaux:{1}'.format(values,morceaux)
    return values
res=[]
for line in reversed(open('tmp.log').readlines()):
    if line.find('NIDEK') == -1: # il n'y a pas le motif Nidek
        print 'brut line:{}'.format(line) # je manipule la chaine
        line = trim_timestamp(line)
        print'no timestamp line:{}'.format(line)
        if re.search(regexSCA,line,flags=0):
            values=cutting(line,cuttingSCA)
            print 'cutting values: {}'.format(values)
            values=[val.strip() for val in values]
            values=[trimspace_regex(val) for val in values]
            print 'formated values: {}'.format(values)
            res.append(values)
            print 'res:{}'.format(res)
        elif re.search(regexADD,line,flags=0):
            values = cutting(line,cuttingADD)
            print 'values : {}'.format(values)
            res.append(values)
        print '---END OF IF---'
    else: break
print 'final res : {}'.format(res)