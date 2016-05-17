# -*- coding: utf-8 -*-
import re

def trimspace(val):
    idx=1
    val=val.strip()
    if val[1]== ' ':
        res=val[:idx]+val[(idx+1):]
    else:
        res=val
    return res
                    
def trimzero(val):
    res = val
    regex=r'\.\d0'
    if re.search(regex,val,flags=0):
        match=re.search(regex,val,flags=0)
        print 'match:{}'.format(match)
        if val[-1] == '0':
            res=val[:-1]
    return res

def main_trim(val):
    """Call of the trimspace and trimzero functions
        val : string
        return : string
    """
    print 'in main_trim val is {}'.format(val)
    res = trimspace(trimzero(val))
    print 'in main_trim res is {}'.format(res)
    return res

        
if __name__ == '__main__':
    #print '_get_sph():{}'.format(_get_sph())
    vals=['+ 6.50','+12.22','+ 6.52','- 6.00','+ 7.50','120','100','- 7.50', ' 90','105']
    for val in vals:
        print '-'*10
        print 'len(val): {}'.format(len(val))
        print 'val.strip() : {}'.format(val.strip())
        print 'len(val.strip()) : {}'.format(len(val.strip()))
        print 'main_trim() : {}'.format(main_trim(val))
    #===========================================================================
    #     print '-'*8
    #     print 'val:{}'.format(val)
    #     print 'main_trim(val) : {}'.format(main_trim(val))
    # 
    #===========================================================================
    #===========================================================================
    # for val in vals:
    #     print '-'*8
    #     print 'val:{}'.format(val)
    #     print 'trim space:{}'.format(trimspace(val))
    #     print 'val:{}'.format(val)
    #     print 'trim zero:{}'.format(trimzero(val))
    #     print 'val:{}'.format(val)
    #     res=trimspace(trimzero(val))
    #     print 'trim space and zero:{}'.format(trimspace(trimzero(val)))
    #     print "res : {}".format(res)
    #     print 'val:{}'.format(val)
    #===========================================================================
    #print formatValregex(val)
     
     
    
#===============================================================================
# A l'entrée j'ai des str à la sortie des str
# je recupere le premier caractere s'il est dans ['+','-'] je le garde sinon je l'envele
# je recupere le 2eme caractere s'il est dans [0-9] ou .' je le garde sinon je le l'enleve
# 'je recupere le 3eme caractere s'il est dans [0-9] ou . ' je le garde sinon je le l'enleve
# ainsi de suite
# le dernier caractere s'il est = 0 je l'enleve.

# Si le charactere n'est pas dans + - [0-9] alors enleve le 
# et si le dernier character est zero enleve le zero.'
# 
# Il pourrait etre aussi intéressant de modifier la liste de selection. Est-ce que c'est possible?
# Qu'est ce qui se passe pour les anciennes data déja enregistrées.
# Est ce que Odoo va s'en plaindre"'

#Je veux supprimer le dernier zero s'il est précéde de '.0''
#===============================================================================
#===============================================================================
# https://regex101.com/#python    
# 
# To replace a specific position:
# 
# s = s[:pos] + s[(pos+1):]
# 
# To replace a specific character:
# 
# s = s.replace('M','')
#===============================================================================
