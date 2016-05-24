# -*- coding: utf-8 -*-
import re, mmap, time

with open('tmp.log','r') as f:
    m = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)  
    i = m.rfind('NIDEK')
    m.seek(i)
    line = m.readline()
    print 'line:{}'.format(line)
    f.close()
    
print '-'*6
# ======================
with open('tmp.log','r') as input:
    with open('newlog.txt','wb') as output:
        for line in input:
            print 'line:{}'.format(line)
            #if line != 'to delete':
             #   output.write(line)
            output.close()
        input.close()
# Je peux faire des tests sur 'line' et décider ou non d'ecrire dans un fichier'

print '='*10

time.sleep(2) # delays for 5 secondssleep(5)
for line in reversed(open('tmp.log').readlines()):
    if line.find('NIDEK') == -1: # il n'y a pas le motif Nidek
        print 'line:{}'.format(line) # je manipule la chaine
    else: break
    
1 je lis les chaines depuis la fin du fichier
2 je suppose que dans le fichier il n'y a que des lignes avec des datas
3 je '

#===============================================================================
# Ca a l'air sympa
# bad_words = ['bad', 'naughty']
# 
# with open('oldfile.txt') as oldfile, open('newfile.txt', 'w') as newfile:
#     for line in oldfile:
#         if not any(bad_word in line for bad_word in bad_words):
#             newfile.write(line)        
#===============================================================================