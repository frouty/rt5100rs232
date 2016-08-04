# -*- coding: utf-8 -*-
"""
TODO fix the problem for 0 sphere, cyl, axis
"""
import re, os
import logging

# constants
SCAdict = {'f':('subjectdata', 'FarVisionSCA'),
                'n':('subjectdata', 'NearVisionSCA'),
                'F':('finalprescriptiondata', 'FarVisionSCA)'),
                'N':('finalprescriptiondata', 'NearVisionSCA'),
                'O':('ARdata', 'ObjectiveSCA'),
               }

cuttingSCA = [0, 2, 8, 14, 17]
cuttingADD = [0, 2, 8]
cuttingVA = [0, 2, 7]

# dict use by merge and substitute method.
# keys ('a','A','f','F','n','N') are the first character that code the line of the
# output file from rt5100

# RT datas after a line @RT before an other @:
# AR datas (autorefractometer datas)
#     O objective SCA
#     V corrected visual acuity
#     U corrected visual acuity extended format

# After à @RM before an other @
# Unaided visual acuity datas
#    W unaided visual acuity
#    M unaided visual acuity extended format

# Final prescription datas : F, N,  A, V
#     F: far vision SCA datas
#     N: near vision SCA datas
#     A: ADD
#     V: Visual acuity
#     U: visual acuity with extended format
#
# Subjective datas
#     f : far vision SCA
#     n : near vision SCA
#     a : ADD
#     v : visual acuity
#     u : visual acuity extended format

# for the left and right,  rt5100 append "L" or "R" to this letter.
# eg vL visual acuity for left eye.
# for binoculare rt5100 append the character "B":
# eg  UB for

mapvatype = {
             'a':'BCVA',
             'A':'Rx',
             'f':'BCVA',
             'F':'Rx',
             'n':'BCVA',
             'N': 'Rx',
              }
# not used
mappedvatype = {
                'BCVA':('a', 'f', 'n'),  # ceux sont les deux seuls valeurs qui ont besoins de SCA et ADD. Pour les verres portes ce n'est pas le RT5100 qui le donne.
                'Rx':('F', 'N', 'A')
                }

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

regexADD = r'[Aa][RL]'  # regex to get the line with ADD datas
# regexSCA = r'[OfFnN][RL]'  # regex tp get the line with SCA datas.
regexSCA = r'[OfFnN ][RL]'  # regex tp get the line with SCA datas.
regexVA = r'[VUWMvu][RLB]'  # regex to catch datas for VA


# map regex and the way to cut the line to get the datas
cuttingDict = { regexADD:cuttingADD,
                regexSCA:cuttingSCA,
                regexVA:cuttingVA,
                  }

def zero2none(val):
    """Set val to None if val is 0.00, + 0.00, - 0.00
    """
    logging.info('in zero2none')

    rx = '[1-9]|[a-zA-Z]'
    if not re.search(rx, val, flags = 0):  # si je n'ai que des zero alors set val to none
        val = None

    logging.info('return val : %s', val)

    return val

def trimzero(val):
    """Trim zero value if there is one at the 2nd decimal
    needed if there is a selection fields with no zero at the 2nd decimal
    in Odoo
    
    val : string from the rt5100
    
    example: '+ 2.20' return '+ 2.2'
    example: '100' return '100'
    """
    logging.info('in trimzero')
    res = val
    logging.info('val:%s', val)
    regex = r'\.\d0'
    if re.search(regex, val, flags = 0):
        # match = re.search(regex, val, flags = 0)
        # print 'match:{}'.format(match)
        if val[-1] == '0':
            res = val[:-1]
    logging.info('return res: %s', res)
    return res

def trimspace_regex(val):
    """Trim the space after sign +/- if there is one in val
    val : string from rt-5100
    eg val = '+ 2,00'  --> return '+2.00'
    eg val ='  0,00'   --> return '  0.00'

    return the trimed string
    """
    logging.info('in trimspace_regex')

    regex = r'^[+-] '  # don't forget the space at the end of the regex
    if re.search(regex, val, flags = 0):
        # match = re.search(regex, val, flags = 0)
        # print 'match:{}'.format(match)
        val = val[:1] + val[2:]
    logging.info('return val:%s', val)
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


def getandformat_values(rxlist = [regexSCA, regexADD, regexVA], log_path = os.path.expanduser('~') + '/rt5100rs232/tmp.log'):
    """ Get the values and format them ready to write in odoo
    
    rxlist : list of regex from specification of datas RT5100
    log_path: str path to file with datas from rt5100
    
    return : dictionnary of datas
    eg: return 
    UCVA [['MB', '1.25'], ['WB', '1.25'], ['ML', '0.63'], ['WL', '0.63'], ['MR', '0.1'], ['WR', '0.1']]
    AR [['UB', '<0.04'], ['VB', '<0.04'], ['UL', '0.8'], ['VL', '0.8'], ['UR', '0.4'], ['VR', '0.4'], ['OL', '-0.5', '-6.75', '25'], ['OR', '+6.0', '-6.25', '175']]
    Rx [['UB', '0.32'], ['VB', '0.32'], ['UL', '0.32'], ['VL', '0.32'], ['UR', '0.25'], ['VR', '0.25'], ['AL', '+4.50'], ['AR', '+3.75'], ['FL', '+16.0', '-4.75', '130'], ['FR', '+11.75', '-3.5', '175']]
    BCVA [['uB', '1.6'], ['vB', '1.6'], ['uL', '2.0'], ['vL', '2.0'], ['uR', '0.32'], ['vR', '0.32'], ['aL', '+3.50'], ['aR', '+3.50'], ['fL', '-1.25', '-5.25', '130'], ['fR', '+5.25', '-8.75', '175']]
    CVA [['UB', '<0.04'], ['VB', '<0.04'], ['UL', '0.4'], ['VL', '0.4'], ['UR', '0.8'], ['VR', '0.8'], ['AL', '+1.50'], ['AR', '+1.50'], ['L', '+2.0', '-4.0', '25'], ['R', '+2.25', '-2.75', '120']]

    Those datas could be inserted in the database except that you need to map them to field names.
    """
    logging.info('in getandformat_values')
    res = []
    final = {}
    first = []
    for line in reversed(open(log_path).readlines()):# read each line starting by the end
        if line.find('NIDEK') == -1:  # Tant que je ne trouve pas le motif 'NIDEK' je traite la ligne.
            logging.info('brut line:%s', line)
            if line.find('@RT') != -1:  # la ligne est un @RT.
                logging.info('find an @RT')
                #final['@RT']=res
                logging.info('final:%s',final)
                logging.info('final.values():%s', final.values())
                for item in final.values():
                    for i in item:
                        logging.info('values:%s', i)
                        logging.info('%s',i[0][0])
                        first.append(i[0][0]) # i[0][0] is the first character of the first list of the intrecated
                    mystring="".join(first)
# =======
#                 for item in res:
#                     logging.info('item:%s', item)
#                     first.append(item[0][0])
#                     logging.info('first :%s', first)
#                     mystring = "".join(first)
# >>>>>>> 1864103cef37ce19f55c0e116714d191416a8b65
#                     logging.info('mystring:%s', mystring)
#                 # je test l'existence de M et W
#                 if mystring.find('MW') != -1:
#                     va_type = 'UCVA'
#                     first = []
#                     final[va_type] = res
#                     logging.info('final:%s', final)
#                 # je teste si mystring est upper
#                 if mystring.isupper()and mystring.find('MW') == -1:
#                     va_type = 'Rx'
#                     first = []
#                     logging.info('va_type:%s', va_type)
#                     logging.info('res:%s', res)
#                     final[va_type] = res
#                     logging.info('final:%s', final)
#                 if mystring.islower()and mystring.find('MW') == -1:
#                     va_type = 'BCVA'
#                     logging.info('va_type:%s', va_type)
#                     final[va_type] = res
# <<<<<<< HEAD
#                     mystring=[]
#                 #on test si le premier caractere est upper
#                 # si c'est le cas si c'est donc upper 
# =======
#                     logging.info('final:%s', final)
#                     first = []
#                 # on test si le premier caractere est upper
#                 # si c'est le cas si c'est donc upper
# >>>>>>> 1864103cef37ce19f55c0e116714d191416a8b65
#                 # alors on sait que l'on a .un va_type = 'Rx'
#                 # si c'est minuscule alors on va_type = 'BCVA"
#                 # comment on fait pour savoir si on upper ou lower.
#                 #
#                 # a partir de là il faut lancer la méthode qui va nous enregistrer les données.
#                 res = []  # on remet à zero la liste

            if line.find('@RM') != -1:
                logging.info('find an @RM')
                va_type = 'AR'
                final[va_type] = res  # ce dictionnaire n'est pas tres informatif.
                # sous @RM c'est toujours  'va_type' = 'AR'
                logging.info('final:%s', final)
                res = []

            if line.find('@LM') != -1:
                logging.info('find an @LM')
                va_type = 'CVA'
                final[va_type] = res
                logging.info('final:%s', final)
                # les lignes sous '@LM' c'est toujours 'CVA'
                res = []

            line = trim_timestamp(line)
            logging.info('no timestamp line: %s', line)
            for rx in rxlist:
                if re.search(rx, line, flags = 0):
                    values = cutting(line, cuttingDict[rx])
                    logging.info('cutting values: %s', values)
                    values = [val.strip() for val in values]
                    values = [trimspace_regex(val) for val in values]
                    logging.info('formated trimspaced values: %s', values)
                    if re.search(rxlist[0], line, flags = 0):  # don't trimzero ADD values.
                        values = [trimzero(val) for val in values]
                        logging.info('trimzero: %s', values)
                    values = [zero2none(val) for val in values]
                    logging.info('zero2none: %s', values)
                    res.append(values)
                    logging.info('append res: %s', res)
#                    values=[trimzero(val)  if re.search(rxlist[1],val,flags=0) else val for val in values  ] # Don't do that for ADD
                    logging.info('**res**: %s', res)
            logging.info('---END OF IF---')
        else: break
    logging.info('getandformatvalues method return:%s', res)
    for k, v in final.iteritems():
        print k, v
    return final


def mergeADD2SCA(res):
    """Merge the ADD dict into the SCA dict
    
        res: dict comming from the maptoodoofieldV2
        res: eg :{'A': {'add_od': '+9.00', 'add_os': '+9.00'}, 'a': {'add_od': '+5.00', 'add_os': '+5.00'}, 'F': {'sph_os': '+3.25', 'sph_od': '-0.75', 'cyl_od': '-3.00', 'axis_os': '100', 'axis_od': '150', 'cyl_os': '-7.75'}}
        
        return : dict {'F': {'sph_os': '+3.25', 'add_od': '+9.00', 'add_os': '+9.00', 'sph_od': '-0.75', 'cyl_od': '-3.00', 'axis_os': '100', 'axis_od': '150', 'cyl_os': '-7.75'}, 'f': {'sph_os': '+10.50', 'add_od': '+5.00', 'add_os': '+5.00', 'sph_od': '+7.75', 'cyl_od': '-5.00', 'axis_os': '100', 'axis_od': '65', 'cyl_os': '-5.50'}}
    """
    print 'passing in MERGEANDSUBSTITUTE'
    for key in res.keys():
        print 'key : {}'.format(key)
        if key == 'A' :
            if 'F' in res.keys():
                print "before update:{}".format(res)
                res['F'].update(res[key])
                print 'after update: {}'.format(res)
                res.pop(key)
                print 'after pop:{}'.format(res)
                # res[mapvatype['F']] = res.pop('F')
        if key == 'a':
            if 'f' in res.keys():
                res['f'].update(res[key])
                res.pop(key)
                # res[mapvatype['f']] = res.pop('f')
    return res

# def substitute(res):
#     """Substitute keys (f,F,N,n)with selection values from Odoo
#
#     res : dict return by mergeADD2SCA
#
#     return : dict
#     return eg:
#     """
#
#     for key in res.keys():
#         res[mapvatype[key]] = res.pop[key]
#     print 'in substitute return : {}'.format(res)
#     return res
def map2odoofieldsV2(raw):
    """Map datas to ODOO field names
    
    raw dict of  datas return by getandformat_values method
    it's a dict with raw datas from rt5100
    
    
    raw eg: UCVA [['MB', '1.25'], ['WB', '1.25'], ['ML', '0.63'], ['WL', '0.63'], ['MR', '0.1'], ['WR', '0.1']]
    AR [['UB', '<0.04'], ['VB', '<0.04'], ['UL', '0.8'], ['VL', '0.8'], ['UR', '0.4'], ['VR', '0.4'], ['OL', '-0.5', '-6.75', '25'], ['OR', '+6.0', '-6.25', '175']]
    Rx [['UB', '0.32'], ['VB', '0.32'], ['UL', '0.32'], ['VL', '0.32'], ['UR', '0.25'], ['VR', '0.25'], ['AL', '+4.50'], ['AR', '+3.75'], ['FL', '+16.0', '-4.75', '130'], ['FR', '+11.75', '-3.5', '175']]
    BCVA [['uB', '1.6'], ['vB', '1.6'], ['uL', '2.0'], ['vL', '2.0'], ['uR', '0.32'], ['vR', '0.32'], ['aL', '+3.50'], ['aR', '+3.50'], ['fL', '-1.25', '-5.25', '130'], ['fR', '+5.25', '-8.75', '175']]
    CVA [['UB', '<0.04'], ['VB', '<0.04'], ['UL', '0.4'], ['VL', '0.4'], ['UR', '0.8'], ['VR', '0.8'], ['AL', '+1.50'], ['AR', '+1.50'], ['L', '+2.0', '-4.0', '25'], ['R', '+2.25', '-2.75', '120']]
    """

    res = {}
    list_int = []

    # use a correspondance table between model fieds and rt5100 character coding
    va_or = re.compile('(VR|WR|vR)')
    va_ol = re.compile('(VL|WL|vL)')

    va_or_extended = re.compile('(MR|UR|uR)')
    va_ol_extended = re.compile('(ML|UL|uL)')

    va_bin = re.compile('(WB|vB|VB)')
    va_bin_extended = re.compile('(MB|UB|uB)')

    add_od = re.compile('(aR|AR)')
    add_os = re.compile('(aL|AL)')

    sca_or = re.compile('(^R|OR|fR|FR)')
    sca_os = re.compile('(^L|OL|fL|FL)')

    sca_near_or = re.compile('(nR|NR)')
    sca_near_os = re.compile('(nL|NL)')
#     sph_od = re.compile('(R|OR|fR|FR)')
#     cyl_od = re.compile('(R|OR|fR|FR)')
#     axis_od = re.compile('()')
#
#     sph_os = re.compile('()')
#     cyl_os = re.compile('()')
#     axis_os = re.compile('()')
#

#     sph_near_or = re.compile('()')
#     cyl_near_or = re.compile('()')
#     axis_near_or = re.compile('()')
#
#     sph_near_os = re.compile('()')
#     cyl_near_os = re.compile('()')
#     axis_near_os = re.compile('()')


    mapregex = {
              va_or:'va_or',
              va_ol:'va_ol',
              va_or_extended: 'va_or_extended',
              va_ol_extended:'va_ol_extended',

              va_bin:'va_bin',
              va_bin_extended:'va_bin_extended',

#               add_od: 'add_od',
#               add_os: 'add_os',
#
#               sca_or :'sca_or',
#               sca_os : 'sca_os',
#               sca_near_or:'sca_near_or',
#               sca_near_os :'sca_nera_os',

#             sph_od:'sph_od',
#             cyl_od:'cyl_od',
#             axis_od:'axis_od',
#
#             sph_os:'sph_os',
#             cyl_os:'cyl_os',
#             axis_os:'axis_os',
#
#             sph_near_or:'sph_near_or',
#             cyl_near_or:'cyl_near_or',
#             axis_near_or:'axis_near_or',
#
#             sph_near_os:'sph_near_os',
#             cyl_near_os:'cyl_near_os',
#             axis_near_os:' axis_near_os',
              }


    # substitute characters coding rt5100 by model fields name
    # only for va datas
    for key in raw.keys():  # j'itere sur chaque key de raw datas. J'obtiens une liste de liste
        # res[key] = list_int
        list_int = []
        print 'res:{}'.format(res)
        print '=' * 10
        print 'key:{}'.format(key)
        print 'raw[{}]:{}'.format(key, raw[key])
        for item in raw[key]:  # J'itere sur chaque item de la liste. item contient les datas.
            # print 'item:{}'.format(item)
            for k, v in mapregex.iteritems():
                item[0] = re.sub(k, v, item[0])  # je substitue le codage du RT5100 par les fields name
            # print 'item after sub:{}'.format(item)
            list_int.append(item)
            # print 'list_int : {}'.format(list_int)
            # print'-' * 5
            # for item in list_int:
            #    print item
            # print '-' * 5
        print '-' * 10
        print 'liste intermédiaire:{}'.format(list_int)
        print 'res:{}'.format(res)
        res[key] = list_int
        print 'res updated with list intermediaire:{}'.format(res)
        print '=' * 10
    print 'res final en sotie de boucle:{}'.format(res)
    print 'keys:{}'.format(res.keys())
    for v in res.itervalues():
        print 'value:{}'.format(v)
#     print "res:{}".format(res)
#     print res.values()
#     for k in res.keys():
#         print 'key of res:{}'.format(k)
#     for k, v in res.iteritems():
#         print k
#         print v
#         #


                # print v

        # replaced = [va_or.sub('va_or', w) for w in final[key][0]]
        # print 'replaced:{}'.format(replaced)
#         for v in final[key]:
#             print v


    logging.info('final :%s', raw)
    return res


def map2odoofields(values):
    """Map datas to ODOO field names
    
    values list of datas from rt5100 after parsing
    values eg: [['AL', '+6.50'], ['AR', '+1.50'], ['FL', '-2.00', '0.00', '0'], ['FR', '-2.00', '0.00', '9'], ['fL', '-3.00', '0.00', '0'], ['fR', '-3.00', '0.00', '0'],]
    values is returned by getandformat_values function
    """
    print 'in map2fields'
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

    logging.basicConfig(format = '%(asctime)s %(message)s', datefmt = '%m/%d/%Y %I:%M:%S /', level = logging.INFO)

#     datas = getandformat_values()
#     print 'getandformat_values return :{}'.format(datas)

    datas = {'UCVA': [['MB', '1.25'], ['WB', '1.25'], ['ML', '0.63'], ['WL', '0.63'], ['MR', '0.1'], ['WR', '0.1']], 'AR': [['UB', '<0.04'], ['VB', '<0.04'], ['UL', '0.8'], ['VL', '0.8'], ['UR', '0.4'], ['VR', '0.4'], ['OL', '-0.5', '-6.75', '25'], ['OR', '+6.0', '-6.25', '175']], 'Rx': [['UB', '0.32'], ['VB', '0.32'], ['UL', '0.32'], ['VL', '0.32'], ['UR', '0.25'], ['VR', '0.25'], ['AL', '+4.50'], ['AR', '+3.75'], ['FL', '+16.0', '-4.75', '130'], ['FR', '+11.75', '-3.5', '175']], 'BCVA': [['uB', '1.6'], ['vB', '1.6'], ['uL', '2.0'], ['vL', '2.0'], ['uR', '0.32'], ['vR', '0.32'], ['aL', '+3.50'], ['aR', '+3.50'], ['fL', '-1.25', '-5.25', '130'], ['fR', '+5.25', '-8.75', '175']], 'CVA': [['UB', '<0.04'], ['VB', '<0.04'], ['UL', '0.4'], ['VL', '0.4'], ['UR', '0.8'], ['VR', '0.8'], ['AL', '+1.50'], ['AR', '+1.50'], ['L', '+2.0', '-4.0', '25'], ['R', '+2.25', '-2.75', '120']]}

    map2odoofieldsV2(datas)


#     res = mergeandsubstitute(map2odoofields(datas))
#     print "map2odoofields(datasV2, ) : {}".format(res)

#     res= mergeandsubstitute(res)
#     print 'mergeandsubstitute return : {}'.format(res)










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
