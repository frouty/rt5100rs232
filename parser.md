Je sais récuperer le SCA et le mettre dans un dictionnaire: 

- (s,c,a)=('val1','val2','val3')
- ou SCA = {'sph':'val1','cyl'='val2','axe'='val3'}
- Ce SCA il correspond à un oeil droit ou un oeil gauche:

	- soit on crée deux dictionnaires SCA_OR et SCA_OS
	- soit on crée un dictionnaire de dictionnaire: SCA={OR:{'sph':'val1','cyl'='val2','axe'='val3'}, OS:{'sph':'val1','cyl'='val2','axe'='val3'}
	Dans ce cas là pour appeler le SCA OD : SCA[OD]
	- On a des SCA OR et OS mais on a aussi des SCA pour différentes mesures:
			- Subjective data
					- Far Vision SCA : f
					- Near Vision SCA : n
					- ADD : a
			- Final prescription data:
					- Far Vision SCA : F
					- Near Vision SCA : N
					- ADD : A
Ce qui pourrait donner:

* SubjectData={'FarVisionSCA':
												{'OR':{'sph':'val1od','cyl':'val2od','axe':'val3od'},
												 'OS':{'sph':'val1os','cyl':'val2os','axe':'val3os'}
												 },
						  'NearVisionSCA':
						  						{'OR':{'sph':'val1od','cyl':'val2od','axe':'val3od'},
												 'OS':{'sph':'val1os','cyl':'val2os','axe':'val3os'}
							'Add':
										{'OR':'valod'
										  'OS':'valos'}
							}
	- pour atteindre FarVisionSCA des data subjectives OD: SubjectData['FarVisionSCA']['OR']

* FinalPrescriptionData= exactement les memes clefs

Finalement
=====
Je choisi deux dictionnaires
	- valuesOD: keys: sph_od, cyl_od, axe_od
	-valuesOG : keys: sph_os, cyl_os, axe_os
	Avec des noms de clefs explicites et qui correspondent au nom de champ dans les tables ODOO je me dis que cela sera plus simple pour les y insérer.
	
et on récupere le tye de valeurs mesurée avec la variable 'filter'. On sait ce que l'on demande et ce que l'on demande c'est ce que l'on récupère.

ZIP
===
a = [1, 2, 3, 4, 5]

b = [2, 2, 9, 0, 9]

zip(a,b) 

[
    (1, 2),
    (2, 2),
    (3, 9),
    (4, 0),
    (5, 9)
]

MAP
===
map prend une fonction, et un iterable et applique à chaque itérable la fonction.

map(some_fonction, some_iterable)

Comme fonction on peut utiliser une fonction lambda.

LAMBDA
===
lambda <input>: <expression>

new_dict = {k: v for k, v in zip(keys, values)}