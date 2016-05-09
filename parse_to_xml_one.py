# -*- coding: utf-8 -*-
from lxml import  etree




with open('/home/lof/rt5100rs232/tmp.log','r') as infile:
    for line in infile:
        

root=etree.Element("data", )                  
#element are organise in an XML Tree structure
#pour creer un child on peut utiliser la méthode append
rt5100=etree.SubElement(root,'rt100')
va_type=etree.SubElement(rt5100,'va_type')
#element are organise in an XML Tree structure
#pour creer un child on peut utiliser la méthode append
rt5100=etree.SubElement(root,'rt100')
va_type=etree.SubElement(rt5100,'va_type')
va_od=etree.SubElement(va_type,'va_od')
va_os=etree.SubElement(va_type,'va_os',)

print etree.tostring(root,pretty_print=True)

print etree.tostring(root,pretty_print=True)
print '-'*6
print "va_od.get('name'): %s" %(va_od.get('name')) # --> 1/10
print " va_od.set('name','10/10'): %s" %(va_od.set('name','10/10')) # --> None !
va_od.set('name','10/10')
print "the new value is: %s" %(va_od.get('name'))
print "root.set('name','hellodata'): %s" %(root.set('name','hellodata'))
print '-'*6
print 'Some info on attrib'
attributes =va_od.attrib


#Tout chgt dans le Element se verra dans l'objet attrib et reciproquement
#le tree XML reste en vie en mémoire temps que l'attrib d'un seul de ces Element
# est utilisé.
# pour avoir un snapshot indépendant de ces atttributes qui ne dépend pas du XML tree il faut 
# faire une copie de ce dictionnaire.op),k
d=dict(va_od.attrib)
print d.items() 

print 'let\'s make some changes in attributes'
print 'attrib name is: %s' %(attributes.get('name'))
try:
    print 'attrib name is now: %s' %(attributes.set('name','10/10')) # ne marche pas
except AttributeError:
    print "cette methode ne marche pas" 
    print 'va_od name is now: %s ' %(va_od.set('name', '10/10'))
