# -*- coding: utf-8 -*-
import settings

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
        print 'seq_sph: {}'.format(seq_sph)
        seq_sph=['{:.2f}'.format(i) for i in seq_sph]
        #seq_sph = ['+' + str(i) if i >= 0 else str(i) for i in seq_sph ]
        # add +
        print 'after format : {} '.format(seq_sph)
        seq_sph=['+'+i if float(i) >=0 else i for i in seq_sph]
        print 'seq_sph:{}'.format(seq_sph)
        # seq_sph = [str(i) for i in seq_sph]
    
        sph_selection = zip(seq_sph, seq_sph)
        print 'sph_selection: {}'.format(sph_selection)
        return tuple(sph_selection)

def _get_cyl():

        seq_cyl = seq(settings.CONST.START_CYL, settings.CONST.STOP_CYL, settings.CONST.STEP_CYL)
        #seq_cyl = [str(i) for i in seq_cyl]
        seq_cyl=['{:.2f}'.format(i) for i in seq_cyl]
        print 'formated : {}'.format(seq_cyl)
        seq_cyl.reverse()
        cyl_selection = zip(seq_cyl, seq_cyl)
        return tuple(cyl_selection)


if __name__ == "__main__":
    #print seq(1,10, step=0.5)
    print _get_cyl()