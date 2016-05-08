# rt5100rs232
Programme to get and put from and to the RT5100 NIDEK refractor

basic interface specification
---------
connector : DIN 8 pin
synchronous : asynchronus
Line: Half duplex
Baud rate: 2400 bit/sec
Bit lenght : 7 bit 
Parity check : Even parity
stopbit: 2 bit 
Datacode : ASCII
CR code : yes

Pyserial module 
--------
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
un byte peut prendre jusqu'à 256 valeur différentes. et ces systeme peuvent ne peuvent gérer plus de 256 characteres.
Avec unicode il y a bcp de charactere mais il faut gérer plus de un byte.
Dans python les chaines standards sont des chaines 8 bits and des chaines simples.
Dans python on n'a pas besoin de savoir comment sont représentés les characteres unicodes sauf quand on veut les envoyer à des fonctions byte orientées comment des fonctions d'ecriture sur des fichiers, d'utilisation de socket. À ce moment là il faut choisir comment représenter un charactere en byte. Convertir depuis unicode vers une byte string s'appelle encoding la chaine de characteres. De la meme façon si on doit charger des chaines unicodes depuis un fichier, un socket ou tout objet byte-oriented, il faut décoder la chaine de bytes vers unicode.
Il faut toujours faire la conversion bytestring to unicode aux barriers IO.
Donc quand on recoit les données de l'exterieurs (network, file, user input) il faut construire un objet unicode immédiatement. Il faut trouver l'encodage approprié.
Quand le programme envoie des données "à l'extérieur" (vers le net, vers des fichiers, vers l'utilisateur, etc.), il faut déterminer l'encodage et et convertir le text vers une bytestring avec cet encodage.Sinon Python essaie de convertire unicode vers une bytestring ASCII ce qui a toutes les chances de produire une UnicodeDecodeErrors.
Si on a des UnicodeDecodeErrors ou UnicodeEncodeError il faut chercher ou on a oublié de construire un objet unicode, oublié de convertir vers une bytestring ou utilisé un mauvais encodage.
s.decode(encoding) : <type 'str'> to <type 'unicode'>
s.encode(encoding):
<type 'unicode'> to <type 'str'>

----
ASCII est codé en 7 bits.
parfois je lis 8 bits.
---- 