# -*- coding: utf-8 -*-
"""
TODO fix the problem for 0 sphere, cyl, axis
"""
import re, os
import logging
import pprint

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

regexADD = r'[Aa][RL]'  # regex to get the line with ADD datas
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

def converttuple(val):
    """"
    @arg : val is a list
    eg ['add_od', '+3.75']
    
    @return : same list but with a tuple
     eg [('add_od', '+3.75')]
    
    usufull when i want to make a dict : dict (list)
    """
    
    val1=[]
    val1.append(val)
    res=[tuple(i) for i in val1]
    return res

def getandformat_values(rxlist = [regexSCA, regexADD, regexVA], log_path = os.path.expanduser('~') + '/rt5100rs232/tmp.log.1'):
    """ Get the values from rt5100 log file  and format them 
    
    rxlist : list of regex from specification of datas RT5100
    log_path: str path to file with datas from rt5100
    
    return : dictionnary of datas
    eg: return 
    UCVA [['MB', '1.25'], ['WB', '1.25'], ['ML', '0.63'], ['WL', '0.63'], ['MR', '0.1'], ['WR', '0.1']]
    AR [['UB', '<0.04'], ['VB', '<0.04'], ['UL', '0.8'], ['VL', '0.8'], ['UR', '0.4'], ['VR', '0.4'], ['OL', '-0.5', '-6.75', '25'], ['OR', '+6.0', '-6.25', '175']]
    Rx [['UB', '0.32'], ['VB', '0.32'], ['UL', '0.32'], ['VL', '0.32'], ['UR', '0.25'], ['VR', '0.25'], ['AL', '+4.50'], ['AR', '+3.75'], ['FL', '+16.0', '-4.75', '130'], ['FR', '+11.75', '-3.5', '175']]
    BCVA [['uB', '1.6'], ['vB', '1.6'], ['uL', '2.0'], ['vL', '2.0'], ['uR', '0.32'], ['vR', '0.32'], ['aL', '+3.50'], ['aR', '+3.50'], ['fL', '-1.25', '-5.25', '130'], ['fR', '+5.25', '-8.75', '175']]
    CVA [['UB', '<0.04'], ['VB', '<0.04'], ['UL', '0.4'], ['VL', '0.4'], ['UR', '0.8'], ['VR', '0.8'], ['AL', '+1.50'], ['AR', '+1.50'], ['L', '+2.0', '-4.0', '25'], ['R', '+2.25', '-2.75', '120']]

    This returned dict must be substitute by the fields name
    and items of the list converted to tuple for built in method dict.
    map2odoofields method and converttotuple will do that  
    """
    logging.info('in getandformat_values')
    res = {}
    val1 = []
    first = []
    for line in reversed(open(log_path).readlines()):# read each line starting by the end
        if line.find('NIDEK') == -1:  # Tant que je ne trouve pas le motif 'NIDEK' je traite la ligne.
            logging.info('brut line:%s', line)
            
            if line.find('@RT') != -1:  # la ligne est un @RT.
                logging.info('find an @RT')
                logging.info('res:%s',res)
                logging.info('val1:%s',val1)
                first=[item[0][0] for item in val1]
                mystring="".join(first)
                logging.info('mystring:%s', mystring)
                logging.info('type mystring:%s', type(mystring))
                
                # je test l'existence de M et W. M,W is for 'UCVA'
                if mystring.find('MW') != -1:
                    va_type = 'UCVA'
                    first = []
                    res[va_type] = val1
                    logging.info('set val to an empty list')
                    val1=[]
                    logging.info('res:%s', res)
#              # je teste si mystring est upper and not 'M' or 'W'
                if mystring.isupper()and mystring.find('MW') == -1:
                    va_type = 'Rx'
                    first = []
                    logging.info('va_type:%s', va_type)
                    logging.info('val1:%s',val1)
                    res[va_type] = val1
                    logging.info('set val to an empty list')
                    val1=[]
                    logging.info('res:%s', res)
                    
                if mystring.islower() and mystring.find('MW') == -1:
                    va_type = 'BCVA'
                    logging.info('va_type:%s', va_type)
                    res[va_type] = val1
                    logging.info('set val to an empty list')
                    val1=[]
                    logging.info('res:%s', res)
            

            if line.find('@RM') != -1: # sous @RM c'est toujours  'va_type' = 'AR'
                logging.info('find an @RM')
                va_type = 'AR'
                res[va_type] = val1
                logging.info('set val to an empty list')
                val1=[]
                logging.info('res:%s', res)
                val1 = []

            if line.find('@LM') != -1:# les lignes sous '@LM' c'est toujours 'CVA'
                logging.info('find an @LM')
                va_type = 'CVA'
                res[va_type] = val1
                logging.info('set val to an empty list')
                val1=[]
                logging.info('res:%s', res)

            line = trim_timestamp(line) # delete the timestamp
            logging.info('no timestamp line: %s', line)
            for rx in rxlist: # boucle on rxlist to cut the line at the right place.
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
                    val1.append(values)
                    logging.info('**val1**: %s',val1)
            logging.info('---END OF IF---')
        else: break
    logging.info('getandformatvalues method return:%s', res)
    for k, v in res.iteritems():
        print k, v
    return res



def makeSCAdict(val):
    """make a SCA dict
    
    @arg: val is a list of values 
    eg: ['sca_os', '+16.0', '-4.75', '130']
    eg:['va_ol_extended', '1.0'],
    
    @return: list 
    eg: [['sph_os','+16.0'],['cyl_os','-4.75'],['axis_os', '130']]
    eg:['va_ol_extended', '1.0'],
    """
    sca_or=['sph_od','cyl_od','axis_od']
    sca_os=['sph_os','cyl_os','axis_os']
    res=[]
    print 'val is:{}'.format(val)
    if val[0] == 'sca_or':
        res=zip(sca_or,val[1:])
    elif val[0] == 'sca_os':
        res=zip(sca_os,val[1:])
    else:
        res=converttuple(val)
        
    print 'makeSCAdict return res;{}'.format(res)
    return res



def map2fields(raw):
    """Map datas to ODOO field names
    
    @arg: raw dict of  datas return by getandformat_values method
    it's a dict with raw datas from rt5100
    
    raw eg: UCVA [['MB', '1.25'], ['WB', '1.25'], ['ML', '0.63'], ['WL', '0.63'], ['MR', '0.1'], ['WR', '0.1']]
    AR [['UB', '<0.04'], ['VB', '<0.04'], ['UL', '0.8'], ['VL', '0.8'], ['UR', '0.4'], ['VR', '0.4'], ['OL', '-0.5', '-6.75', '25'], ['OR', '+6.0', '-6.25', '175']]
    Rx [['UB', '0.32'], ['VB', '0.32'], ['UL', '0.32'], ['VL', '0.32'], ['UR', '0.25'], ['VR', '0.25'], ['AL', '+4.50'], ['AR', '+3.75'], ['FL', '+16.0', '-4.75', '130'], ['FR', '+11.75', '-3.5', '175']]
    BCVA [['uB', '1.6'], ['vB', '1.6'], ['uL', '2.0'], ['vL', '2.0'], ['uR', '0.32'], ['vR', '0.32'], ['aL', '+3.50'], ['aR', '+3.50'], ['fL', '-1.25', '-5.25', '130'], ['fR', '+5.25', '-8.75', '175']]
    CVA [['UB', '<0.04'], ['VB', '<0.04'], ['UL', '0.4'], ['VL', '0.4'], ['UR', '0.8'], ['VR', '0.8'], ['AL', '+1.50'], ['AR', '+1.50'], ['L', '+2.0', '-4.0', '25'], ['R', '+2.25', '-2.75', '120']]
   
   @return:
   eg 
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
    
    mapregex = {
            va_or:'va_or',
            va_ol:'va_ol',
            va_or_extended: 'va_or_extended',
            va_ol_extended:'va_ol_extended',

            va_bin:'va_bin',
            va_bin_extended:'va_bin_extended',

            add_od: 'add_od',
            add_os: 'add_os',
#
            sca_or :'sca_or',
            sca_os : 'sca_os',
            sca_near_or:'sca_near_or',
            sca_near_os :'sca_near_os',
            }

    # substitute characters coding rt5100 by model fields name
    for key in raw.keys():  # j'itere sur chaque key de raw datas. J'obtiens une liste de liste
        list_int = []
        print 'res:{}'.format(res)
        print '=' * 10
        print 'key:{}'.format(key)
        print 'raw[{}]:{}'.format(key, raw[key])
        for item in raw[key]:  # J'itere sur chaque item de la liste. item contient les datas.
            print 'item:{}'.format(item)
            for k, v in mapregex.iteritems():
                item[0] = re.sub(k, v, item[0])  # je substitue le codage du RT5100 par les fields name
                print 'item after sub:{}'.format(item)
            list_int.append(item)
            print 'list_int : {}'.format(list_int)
            print'-' * 5
            for item in list_int:
                print item
                print '-' * 5
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
        print 'res:{}'.format(res)
    return res

def map2odoofields():
    datas=getandformat_values()
    datas=map2fields(datas)
    for key in datas.keys():
        print 'key, datas[key]:{},{}'.format(key,datas[key])
        vals=[makeSCAdict(val) for val in datas[key]]
        datas[key]=vals
       
    return datas


if __name__ == '__main__':

    logging.basicConfig(format = '%(asctime)s %(message)s', datefmt = '%m/%d/%Y %I:%M:%S /', level = logging.INFO)
    
    datas = map2odoofields()
    print "map2odoofields return"
    pprint.pprint(datas)
#     print 'map2odoofields() return'
#     pprint.pprint(datas) 

#     datas = getandformat_values()
#     print 'getandformat_values return :{}'.format(datas)
# 
# #     datas = {'UCVA': [['MB', '1.25'], ['WB', '1.25'], ['ML', '0.63'], ['WL', '0.63'], ['MR', '0.1'], ['WR', '0.1']], 'AR': [['UB', '<0.04'], ['VB', '<0.04'], ['UL', '0.8'], ['VL', '0.8'], ['UR', '0.4'], ['VR', '0.4'], ['OL', '-0.5', '-6.75', '25'], ['OR', '+6.0', '-6.25', '175']], 'Rx': [['UB', '0.32'], ['VB', '0.32'], ['UL', '0.32'], ['VL', '0.32'], ['UR', '0.25'], ['VR', '0.25'], ['AL', '+4.50'], ['AR', '+3.75'], ['FL', '+16.0', '-4.75', '130'], ['FR', '+11.75', '-3.5', '175']], 'BCVA': [['uB', '1.6'], ['vB', '1.6'], ['uL', '2.0'], ['vL', '2.0'], ['uR', '0.32'], ['vR', '0.32'], ['aL', '+3.50'], ['aR', '+3.50'], ['fL', '-1.25', '-5.25', '130'], ['fR', '+5.25', '-8.75', '175']], 'CVA': [['UB', '<0.04'], ['VB', '<0.04'], ['UL', '0.4'], ['VL', '0.4'], ['UR', '0.8'], ['VR', '0.8'], ['AL', '+1.50'], ['AR', '+1.50'], ['L', '+2.0', '-4.0', '25'], ['R', '+2.25', '-2.75', '120']]}
# #  
#     datas = map2fields(datas)
#     print "map2odoofields return:"
#     pprint.pprint(datas) 
#     
#     print "-=-"* 10
#     print 'test makeSCAdict'
#     for values in datas.values():
#         datas=[makeSCAdict(val) for val in values]
#     print "makeSCAdict return:"
#     pprint.pprint(datas) 
