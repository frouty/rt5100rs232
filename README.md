# rt5100rs232
Programme to get and put from and to the RT5100 NIDEK refractor

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

Si je ne met rien dans la console rt5100 pour la sphere qu'elle est la valeur renvoyée? Quel est son type, sa longueur, True, False, None?

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
 
 