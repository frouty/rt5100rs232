# -*- coding: utf-8 -*-
import re

def GetTheSentences(infile):
    with open(infile) as fp:
        for result in re.findall('NIDEK(.*?)NIDEK',fp.read(), re.S):
            print result





if __name__=='__main__':
    GetTheSentences('tmp.log')
    
    