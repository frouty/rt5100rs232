# rt5100rs232
Programme to get and put from and to the RT5100 NIDEK refractor

Principe 
====
l'executable  qui va lire les données et les envoyer vers un fichier 
qui sera ensuite parsé pour que les données soient intégrer dans odoo est:
 
listener_rt5100.py

basic interface specification
====
- connector : DIN 8 pin
- synchronous : asynchronus
- Line: Half duplex
- Baud rate: 2400 bit/sec
- Bit lenght : 7 bit 
- Parity check : Even parity
- stopbit: 2 bit 
- Datacode : ASCII
- CR code : yes

DATA FORMAT. The RT to the PC
====
heading
----
SH NIDEK_RT-5100 ID...
SH semble correspondre au character ascii \x01 qui correspond au character ascii :'soh' qui veut dire "start of heading"

Data source
----
Ensuite vient data source
SX @ bit bit CR
SX ==  \02 qui correspond au caractere ascii 'stx' : 'Start of Text'

CR carriage return : /0D (0xOD) 

Fin de transmission des datas
----
\x04 qui correspond au caractere ascii EOT = 'End Of Transmission'

Pyserial module 
=====
To get info on this module go to the source tree:
documentation/pyserial_api.rst

----
Est-ce que le RT51000 recoit des 7bit ascii code?
Est-ce qu'il faut lui envoyer des chaines de code ascii ? ou est ce qu'il faut lui du two-digit hexadecimal commande comme 'EF' '9A'?


----
hex(nombre entier) --->  valeur hexadecimale
pour connaitre le charactere associé à un ordinal i : chr(i)
ex: 
chr(13) --> '\r'
chr(18) --> '\x12'
chr(81) --> Q

---------
différence entre byte et charactere
=====
un byte peut prendre jusqu'à 256 valeur différentes. 
Et ces systeme ne peuvent gérer plus de 256 characteres.
Avec unicode il y a bcp de characteres mais il faut gérer plus de un byte.
Dans python les chaines standards sont des chaines 8 bits and des chaines simples.
Dans python on n'a pas besoin de savoir comment sont représentés les characteres unicodes sauf quand on veut les envoyer à des fonctions byte orientées comment des fonctions d'ecriture sur des fichiers, d'utilisation de socket. À ce moment là il faut choisir comment représenter un charactere en byte. Convertir depuis unicode vers une byte string s'appelle encoding la chaine de characteres. De la meme façon si on doit charger des chaines unicodes depuis un fichier, un socket ou tout objet byte-oriented, il faut décoder la chaine de bytes vers unicode.
Il faut toujours faire la conversion bytestring to unicode aux barriers IO.
Donc quand on recoit les données de l'exterieurs (network, file, user input) il faut construire un objet unicode immédiatement. Il faut trouver l'encodage approprié.
Quand le programme envoie des données "à l'extérieur" (vers le net, vers des fichiers, vers l'utilisateur, etc.), il faut déterminer l'encodage et et convertir le text vers une bytestring avec cet encodage.Sinon Python essaie de convertire unicode vers une bytestring ASCII ce qui a toutes les chances de produire une UnicodeDecodeErrors.

UnicodeDecodeErrors et UnicodeEncodeError
----
Si on a des UnicodeDecodeErrors ou UnicodeEncodeError il faut chercher ou on a oublié de construire un objet unicode, oublié de convertir vers une bytestring ou utilisé un mauvais encodage.

*s.decode(encoding) : <type 'str'> to <type 'unicode'>

*s.encode(encoding):
<type 'unicode'> to <type 'str'>

----
ASCII est codé en 7 bits.
parfois je lis 8 bits.

---- 

Les valeurs de SCA
======

Sphere
----
Si la sphere est plane est ce que la valeur renvoyée est 0 ou null?
le systeme renvoie 6 bit pour la sphere : _ _ 0.00
Si je ne met rien dans la console rt5100 pour la sphere qu'elle est la valeur renvoyée? Quel est son type, sa longueur, True, False, None?
Renvoie toujours _ _ 0 0 . 0 0
Ca ne renvoie  rien si on oublie de cliquer sur AR/FINAL/SUBJECTIVE

Cylindre
----
Si je ne mets rien dans la console RT51000 pour le cylindre qu'est ce qui est renvoyé?

Si je ne mets rien dans la console du RT5100 est ce que cela veut dire que le cylindre est à zéro? Cela veut dire qu'il n'y a pas de cylindre donc pas d'astigmatisme.

Est ce que cela veut dire qu'il n'y a pas d'astigmatisme et que donc il ne faut rien noter dans ODOO pour le cylindre.

Est ce que je peux avoir une valeur de cylindre et pas d'axe?

Qu'est ce que cela veut dire si cela arrive?

Qu'est ce qu'il faut faire au niveau du script?

Axe
---
Si l'axe est 0° qu'est ce qui est renvoyé?
Si je ne mets rien dans la console RT5100 est ce que cela veut dire que l'axe est à zéro?
 
 Est ce qu'on peut avoir une valeur d'axe et rien pour le cylindre?
 
 Qu'est ce que cela veut dire?
 
 Qu'est ce qu'il faut faire dans ce cas au niveau du script?
 
 Si on met un axe et que l'on ne met rien dans le cylindre, l'axe renvoyé sera nul.
 
 
 exemple ou AR/FINAL/SUBJECTIVE est à zéro pour toutes les valeurs.
 ====
 
 NIDEK RT-5100 ID             DA2016/ 5/23
2016-05-23T00:23:47.685446  @LM
2016-05-23T00:23:47.772447   R  0.00  0.00  0
2016-05-23T00:23:47.859444   L  0.00  0.00  0
2016-05-23T00:23:47.882445  @RM
2016-05-23T00:23:47.968443  OR  0.00  0.00  0
2016-05-23T00:23:48.055444  OL  0.00  0.00  0
2016-05-23T00:23:48.128441  PD64.0        
2016-05-23T00:23:48.151441  @RT
2016-05-23T00:23:48.238442  fR  0.00  0.00  0
2016-05-23T00:23:48.325435  fL  0.00  0.00  0
2016-05-23T00:23:48.398432  pD64.0        
2016-05-23T00:23:48.420438  @RT
2016-05-23T00:23:48.507444  FR  0.00  0.00  0
2016-05-23T00:23:48.594441  FL  0.00  0.00  0
2016-05-23T00:23:48.667436  PD64.0        
2016-05-23T00:23:48.695432  WD35
2016-05-23T00:23:48.731430  TT 005
2016-05-23T00:23:48.740429  
2016-05-23T00:23:49.741531  
2016-05-23T00:23:50.742683  

Vision plus globale du probleme
====
1 je lis le fichier en commencant par la fin

```python
for line in reversed(open('tmp.log').readlines()):
    if line.find('NIDEK') == -1: # il n'y a pas le motif Nidek
        print 'line:{}'.format(line) # je manipule la chaine
```
2 je lis chaque ligne:
	- s'il n'y a que le timestamp je passe à ligne suivant
	- s'il une des lettres autorisée j'applique la bonne méthode pour couper: partie gauche timestamp et data text et datas
	

mapping entre les données du RT et les fields de odoo
-------
	datas: [['AL', '+1.50'], ['AR', '+1.50'], ['FL', '-2.00', '0.00'], ['FR', '-2.00', '0.00'], ['fL', '-3.00', '0.00'], ['fR', '-3.00', '0.00'], ['OL', '-1.00', '0.00'], ['OR', '-1.00', '0.00']]
	
'A', 'a', 'F','f' cela correspond dans odoo au field **va\_type** de l'objet oph\_measurement
```python

def _get_va_type(self, cr, uid, context = None):
        va_type_selection = (
                            ('UCVA', _('UCVA')),  # uncorrected visual acuity
                            ('CVA', _('CVA')),
                            ('BCVA', _('BCVA')),  # best corrected visual acuity
                            ('MAVC sous cycloplegique', 'MAVC sous cycloplegique'),
                            ('Rx', _('Refraction prescription')),  # refraction prescrite
                            ('AR',_('AutoRefractometer')),
                            )
        return va_type_selection
```
        
 je veux obtenir un dictionnaire de la forme:
 
 vals_measurement:{
 
- 'type\_id' : 2 # c'est le type_id de la refraction. Il est fixe il ne bouge pas
- 'va\_type' : qui doit etre mappé avec la premiere lettre de la premiere str 
- 'sph\_od'
- 'sph\_os'
- 'cyl .....
}

Pour chaque item  de la liste datas je dois créer ce dictionnaire et je dois crée le record correspondant à cet item.

Essayons déja de créer ce dictionnaire.

Si j'ai 'a' 'A' 'f' 'F' ... vont déterminer la valeur du champ va_type alors on a le field va_type. Donc on peut faire un mapping entre la premiere lettre et la valeur du  odoo fields va\_type

Il me faut une méthode qui me récupere les données de la forme et cela pour chaque va\_type :
res={'field_odoo':'value', 'va\_type
mapvatype={'a':

pour chaque va\_type je peux aller chercher les datas du RT5100 et les mettre dans un meme dictionnaire pour les écrire ensuite dans la database.

==========
 [['AL', '+6.50'], ['AR', '+1.50'], ['FL', '-2.00', '0.00', '0'], ['FR', '-2.00', '0.00', '9'], ['fL', '-3.00', '0.00', '0'], ['fR', '-3.00', '0.00', '0'],]'

 A partir de la liste ci dessus je voudrais obtenir:
 
 {
 'A' : {'add\_os':'+6.50','add\_od':'+1.50'},
 'F' : {'sph\_os':'-2.00','cyl\_os':'0.00','axis\_os':'0'},
 'f' : {....},
 ....
 }
 
 la liste des va_type est :
 ```python 
 def _get_va_type(self, cr, uid, context = None):
        va_type_selection = (
                            ('UCVA', _('UCVA')),  # uncorrected visual acuity
                            ('CVA', _('CVA')),
                            ('BCVA', _('BCVA')),  # best corrected visual acuity
                            ('MAVC sous cycloplegique', 'MAVC sous cycloplegique'),
                            ('Rx', _('Refraction prescription')),  # refraction prescrite
                            ('AR',_('AutoRefractometer')),
                            )
        return va_type_selection
```
 Ne serait-il pas plus utile d'avoir un dictionnaire final de la forme:
 
 {
 'BCVA': {'sphod':'+2.0', 'cylod':'+5', 'axisod':'+5', og, 'addod':'+5','addos':'+5'},
 'Rx': .......
 }
 
 Comment transformer : ['AL', '+6.50'], ['AR', '+1.50']
en :

{'A':{'add_od':'+6.50','add_og':'+6.50'}
}

en intermediaire on peut faire
{'A':{'L':'+6.50','R':'+6.50'}
}
Ca ca va pour les additions mais pas si SCA car il y a trois valeurs pour R et L

J'ai pas une liste de keys et une liste de values mais une list keys, values

{'A': {'add_od': '+0.75', 'add_os': '+0.75'}, 'F': {'sph_os': '0.00', 'sph_od': '-1.25', 'cyl_od': '-0.75', 'axis_os': '0', 'axis_od': '30', 'cyl_os': '0.00'}}
Avec ce dictionnaire c'est pas fini car il faut merger le valeur de 'A' et la valeur de "F" et la valeur de 'f' avec 'a'.

     def get_rt5100(self,cr,uid,ids,context=None):
        """Get the datas from the RT-5100
        """
        datas=rt5100.getandformat_values()
				res= rt5100.lamethodequidonneledictionnaireapartirdesdatas(datas)
				je boucle sur les clefs de ce dictionnaire.
				for k in res.keys():
					

        records=self.browse(cr,uid,ids,context)
        for record in records:
            vals_measurement = {
                            #'type_id.code' : 'ref', #TODO
                            'type_id' : 2, 
                            'meeting_id' : record.id, #TODO
                            'sph_od' : FinalSCA[0]['sph_od'],
                            'cyl_od': FinalSCA[0]['cyl_od'],
                            'axis_od':FinalSCA[0]['axis_od'],
                            'sph_os' : FianlSCA[1]['sph_os'],
                            'cyl_os':FinalSCA[1]['cyl_os'],
                            'axis_os':FinalSCA[1]['axis_os'],
                            'add_od': todo,
                            'add_os':todo,
                            'va_type': todo
                            }
        oph_measurement_obj =  self.pool.get('oph.measurement').create(cr, uid, vals_measurement, context = context)
        return True