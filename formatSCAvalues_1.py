# -*- coding: utf-8 -*-

#Les selections pour sph, cyl et axes
import settings
import re

def seq(start, stop, step = 1):
        n = int(round((stop - start) / float(step)))
        if n > 1:
            return([start + step * i for i in range(n + 1)])
        else:
            return([])
def _get_sph():
        """
        Return a tuple of tuple
        of str with + if positive
        Wich will be cleaner for Rx prescription than without the + sign
        confusing with or without + could be - minus sign for opticiens
        """
        seq_sph = seq(settings.CONST.START_SPH, settings.CONST.STOP_SPH, settings.CONST.STEP_SPH)
        seq_sph = ['+' + str(i) if i >= 0 else str(i) for i in seq_sph ]
        # seq_sph = [str(i) for i in seq_sph]
        sph_selection = zip(seq_sph, seq_sph)
        return tuple(sph_selection)
    
def _get_axis():
        suffixe = '°'
        seq_axis = seq(settings.CONST.START_AXIS, settings.CONST.STOP_AXIS, settings.CONST.STEP_AXIS)
        seq_axis_suffixed = [str(i) + '°' for i in seq_axis]
        seq_axis = [str(i) for i in seq_axis]
        axis_selection = zip(seq_axis, seq_axis_suffixed)
        return tuple(axis_selection)   
 
def _get_cyl():
        seq_cyl = seq(settings.CONST.START_CYL, settings.CONST.STOP_CYL, settings.CONST.STEP_CYL)
        seq_cyl = [str(i) for i in seq_cyl]
        seq_cyl.reverse()
        cyl_selection = zip(seq_cyl, seq_cyl)
        return tuple(cyl_selection)    

def formatSCA(val):
    val=val.strip()
    res=val
    for idx, c in enumerate(val):
        if c == ' ':
            res = val[:idx]+val[(idx+1):]
        else:
            res=val
        if c=='.':
            pointpos=idx
            if len(res[pointpos+1:]) == 2 and res[-1]==0:
                pass
    return res, pointpos

def trimspace(val):
    idx=1
    if val[1]== ' ':
        res=val[:idx]+val[(idx+1):]
    else:
        res=val
    return res
                    
def formatValregex(val):
    regex=r'\.\d+00'
    regex=r'\.\d0' # je pense que celle là est meilleure. 
    if re.search(regex,val,flags=0):
        match=re.search(regex,val,flags=0)
        print 'match: start:{}--end:{}'.format(match.start(), match.end())
        print 'match group(0):{}'.format(match.group(0))
    
    return True
        
if __name__ == '__main__':
    #print '_get_sph():{}'.format(_get_sph())
    val='+ 6.00 '
    print trimspace(val)
    res = formatValregex(val)
    print res
    
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
