# -*- coding: utf-8 -*-

import re


def trimspace(val):
    idx=1
    if val[1]== ' ':
        res=val[:idx]+val[(idx+1):]
    else:
        res=val
    return res
                    
def trimzero(val):
    res = val
    if val[-1] == '0':
        res=val[:-1]
    return res

def formatValregex(val):
    regex=r'\.\d+00'
    regex=r'\.\d0' # je pense que celle là est meilleure.
    res=val
    if re.search(regex,val,flags=0):
        match=re.search(regex,val,flags=0)
        print 'match: start:{}--end:{}'.format(match.start(), match.end())
        print 'match group(0):{}'.format(match.group(0))
        if val[-2]=='0':
            print 'yes there is two 00'
            res=val[:-1]
            return res
        else: return res
    else: return res

        
if __name__ == '__main__':
    #print '_get_sph():{}'.format(_get_sph())
    vals=['+ 6.50','+12.22','+ 6.52','- 6.00','+ 7.50']
    for val in vals:
     print '-'*8
     print 'val:{}'.format(val)
     print 'trim space:{}'.format(trimspace(val))
     print 'trim zero:{}'.format(trimzero(val))
     print 'trim space and zero:{}'.format(trimspace(trimzero(val)))
    #print formatValregex(val)
     val='+ 5.00'
    
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
