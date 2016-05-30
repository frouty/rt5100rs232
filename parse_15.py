# -*- coding: utf-8 -*-
import re, os

# constants
SCAdict = {'f':('subjectdata', 'FarVisionSCA'),
              'n':('subjectdata', 'NearVisionSCA'),
              'F':('finalprescriptiondata', 'FarVisionSCA)'),
              'N':('finalprescriptiondata', 'NearVisionSCA'),
              'O':('ARdata', 'ObjectiveSCA'),
               }
keysSCAOR = ('sph_od', 'cyl_od', 'axe_od')
keysSCAOS = ('sph_os', 'cyl_os', 'axe_os')
keysADDOR = ('add_od')
keysADDOS = ('add_os')

cuttingSCA = [0, 2, 8, 14, 17]
cuttingADD = [0, 2, 8]

# dict use by merge and substitute method.
mapvatype = {'a':'BCVA',
                    'A':'Rx',
                    'f':'BCVA',
                    'F':'Rx',
                    'n':'BCVA',
                    'N': 'Rx',
                    }
# not used
mappedvatype = {'BCVA':('a', 'f', 'n'),  # ceux sont les deux seuls valeurs qui ont besoins de SCA et ADD. Pour les verres portes ce n'est pas le RT5100 qui le donne.
                         'Rx':('F', 'N', 'A')}

#===============================================================================
# Pour l'instant dans ODOO je n'utilise les valeurs de 'nN' qui est la formule SCA de pres (=avec l'ADD')
#===============================================================================





#===============================================================================
# cuttingDict={  'a':[28,30,36], # a if for add. 28 cut the timpstamp, 30 the data type and R or L, 36 the value= '+' 'dizaine unité' 'dot' 'decimal1' 'decimal2'
#                     'A':[28,30,36], # A for addition
#                     'f':[28, 30, 36, 42, 45],
#                     'F':[1,7,13,16],
#                     'O':[1,7,13,16],
#                     'n': [28, 30, 36, 42, 45],
#                     'N': [28, 30, 36, 42, 45],
#                     }
#===============================================================================

regexADD = r'[Aa][RL]'
regexSCA = r'[OfFnN][RL]'

cuttingDict = { regexADD:cuttingADD,
                    regexSCA:cuttingSCA,
                  }
def zero2none(val):
    """Set val to None if val is 0.00, + 0.00, - 0.00
    """
    rx='[1-9]|[a-zA-Z]'
    if not re.search(rx,val,flags=0):
        val=None
    else:
        return val
    return val


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
        # match = re.search(regex, val, flags = 0)
        # print 'match:{}'.format(match)
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
    regex = r'^[+-] '  # don't forget the space at the end of the regex
    if re.search(regex, val, flags = 0):
        # match = re.search(regex, val, flags = 0)
        # print 'match:{}'.format(match)
        val = val[:1] + val[2:]
    return val

def trim_timestamp(line, lenght = 28):
    """Trim the timestamp
    
    because I don't need it and the timestamp is always the same lengh 
    exept if you change the code in the getting program from the rt5100
    
    line : str line from the data file
    lenght : int lenght of the timestamp
    
    return : str the line without the timestamp.
    """
    res = line[lenght:]
    return res

def cutting(line, coupures):
    """ Cut the line into a list fields of datas
    
    line : str from the datas file fetched from rt5100
    
    coupures: list with size for cutting. depends on description of datas
    
    return: list of fields of datas 
    eg return: values:['FR', '- 2.00', '  0.00', '  0']; ['AL', '+ 1.50']
    the item can't be used like that in odoo database they must be formated.
    You can use the return of this function in list comprehénsion to format the items
    """
    morceaux = [line[i:j] for i, j in zip([0] + coupures, coupures + [None])]  # on coupe les lignes en morceaux qui isolent les champs.
    values = morceaux[1:-1]  # on élimine le champ date et on récupere que les champs datas.SCA dans une liste
    # print 'values:{0} ; morceaux:{1}'.format(values,morceaux)
    return values

def getandformat_values(rxlist = [regexSCA, regexADD], log_path = os.path.expanduser('~') + '/rt5100rs232/tmp.log'):
    """ Get the values and format them ready to write in odoo
    
    rxlist : list of regex from specification of datas RT5100
    log_path: str path to file with datas from rt5100
    
    return : list of datas
    eg: return [['FL', '+20.75', '-6.00'], ['FR', '+20.75', '-6.00']]
    Those datas could be inserted in the database except that you need to map them to field names.
    """
    res = []
    for line in reversed(open(log_path).readlines()):
        if line.find('NIDEK') == -1:  # il n'y a pas le motif Nidek
            print 'brut line:{}'.format(line)  # je manipule la chaine
            line = trim_timestamp(line)
            print 'no timestamp line:{}'.format(line)
            for rx in rxlist:
                if re.search(rx, line, flags = 0): # map type of data and cutting format
                    values = cutting(line, cuttingDict[rx])
                    print 'cutting values: {}'.format(values)
                    values = [val.strip() for val in values]
                    values = [trimspace_regex(val) for val in values]
                    print 'formated trimspaced values: {}'.format(values)
                    values = [zero2none(val) for val in values]                 # selection is none for value = zero
                    print 'zero2None: {}'.format(values)
                    if re.search(rxlist[0],line,flags=0): # don't trimzero ADD values.
                        values = [trimzero(val) for val in values]
                        print 'trimzero: {}'.format(values)
                    res.append(values)
                    print 'append res:{}'.format(res)
            print '---END OF IF---'
        else: break
    # print 'final res from getandformat_values : {}'.format(res)
    return res

def mergeandsubstitute(res):
    """Merge the ADD dict into the SCA dict
    
        val: dict comming from the maptoodoofieldV2
        val: eg :{'A': {'add_od': '+9.00', 'add_os': '+9.00'}, 'a': {'add_od': '+5.00', 'add_os': '+5.00'}, 'F': {'sph_os': '+3.25', 'sph_od': '-0.75', 'cyl_od': '-3.00', 'axis_os': '100', 'axis_od': '150', 'cyl_os': '-7.75'}}
        
        return : dict {'Rx': {'sph_os': '+3.25', 'add_od': '+9.00', 'add_os': '+9.00', 'sph_od': '-0.75', 'cyl_od': '-3.00', 'axis_os': '100', 'axis_od': '150', 'cyl_os': '-7.75'}, 'BCVA': {'sph_os': '+10.50', 'add_od': '+5.00', 'add_os': '+5.00', 'sph_od': '+7.75', 'cyl_od': '-5.00', 'axis_os': '100', 'axis_od': '65', 'cyl_os': '-5.50'}}
    """
    for key in res.keys():
        #print 'key : {}'.format(key)
        if key == 'A' :
            if 'F' in res.keys():
                res['F'].update(res[key])
                res.pop(key)
                res[mapvatype['F']]=res.pop('F')
        if key == 'a':
            if 'f' in res.keys():
                res['f'].update(res[key])
                res.pop(key)
                res[mapvatype['f']]=res.pop('f')
    return res

def map2odoofields(values):
    """Map datas to ODOO field names
    
    values list of datas from rt5100 after parsing
    values eg: [['AL', '+6.50'], ['AR', '+1.50'], ['FL', '-2.00', '0.00', '0'], ['FR', '-2.00', '0.00', '9'], ['fL', '-3.00', '0.00', '0'], ['fR', '-3.00', '0.00', '0'],]
    values is returned by getandformat_values function
    """
    print 'in maptofields'
    res = {}
    for item in values:  # 1ere pass on populate le dictionnary avec les clefs primaires : A, a , F, f....and empty dict
#         print 'res {}'.format(res)
#         print 'item:{}'.format(item)
#         print 'item[0][0]: {}'.format(item[0][0])
#         print 'item[0][1]:{}'.format(item[0][1])
#         print 'item[1:]: {}'.format(item[1:])
        res.update({item[0][0]:{}})
#         print 'res after first pass : {}'.format(res)
#         print '-' * 10
#     print 'first pass finished. res is :{}'.format(res)
    for item in values:  # on second : populate empty dict with datas.
        if re.search(r'[aA]', item[0][0], flags = 0):  # on est dans les additions. On peut mapper avec les champs d'addition
            if 'R' in item[0][1]:  # on est à droite
                print 'R:{}'.format(res[item[0][0]])
                res[item[0][0]].update({'add_od':item[1]})
                print 'res after R:{}'.format(res)
            if 'L' in item[0][1]:
                print res[item[0][0]]
                res[item[0][0]].update({'add_os':item[1]})
        if re.search(r'[fFnN]', item[0], flags = 0):  # on est sur du SCA
            if 'R' in item[0]:
                res[item[0][0]].update({'sph_od':item[1],
                                        'cyl_od':item[2],
                                        'axis_od':item[3]
                                         })
            if 'L' in item[0]:
                res[item[0][0]].update({'sph_os':item[1],
                                        'cyl_os':item[2],
                                        'axis_os':item[3]
                                         })
    return res


if __name__ == '__main__':
    print 'ZERO2NONE'
    print zero2none('2')
    datas = getandformat_values()
    print 'getandformat_values return :{}'.format(datas)
  
    res = mergeandsubstitute(map2odoofields(datas))
    print "mergeandsubstitute map2odoofields(datasV2, ) : {}".format(res)
 
    res= mergeandsubstitute(res)
    print 'mergeandsubstitute return : {}'.format(res)










    #===============================================================================
# mapvatype = {'a':'BCVA',
#                     'A':'Rx',
#                     'f':'BCVA',
#                     'F':'Rx',
#                     'n':'BCVA',
#                     'N': 'Rx',
#                     }
# mappedvatype = {'BCVA':('a', 'f', 'n'), 'Rx':('F', 'N', 'A')}
#
# for oldk in res.keys():  # mondict[newk]=mondict.pop([oldk])
#     print oldk
#     res[mapvatype[oldk]] = res.pop(oldk)
#     print res
#     print '---'
# print 'new res is: {}'.format(res)

# On ne peut pas simplementsubstituer les clefs 'A' 'a', 'f', 'n'.... avec les selections de odoo
# Pour cela il faut rentrer les ADD dans les SCA et ce n'est pas simple
# Essayons de rentrer le dictionnaire res dans les tables.
#===============================================================================
