Il y a tjs le symbole "SH" dans la doc qui commence chaque dont je ne comprends pas a quoi cela correspond dans l'output. 
SH pour le début des datas 
SX ensuite

pour info 'SCA'= Sphere Cylindre Axe
SCA c'est toujours SPH 6bits, Cyl=6bits Axis=3bits.

DATA SOURCE
On a toujours : @
ensuite une ligne qui commence avec une lettre qui décrit les datas qui suivent sur la ligne:
'f' far vision SCA
le côté: 'R' oi 'L'
les donnés avec signe +/- 
- RM autorefractometer (objective data)
- RT refractor (unaided,  subjective and final prescription data) (comment je peux faire la différence entre unaided, subjective et prescription data)

@RM 
'O' objective SCA
O|L/R|SCA(663)|CR
@RT
f pour far vision
F pour Far Vision SCA

Si je veux récupérer les final data prescription il faudra récupérer les lignes

F pour les far vision SCA
N pour les near vision SCA
A pour l'ADD


--------
les subjectives data 

'f' pour la far vision SCA
n pour la near vision SCA
a pour l'ADD

2016-05-02T05:37:02.300510	NIDEK RT-5100 ID             DA2016/ 5/ 2
2016-05-02T05:37:02.323509	@RM
2016-05-02T05:37:02.410503	OR- 2.75  0.00  0
2016-05-02T05:37:02.496502	OL- 2.75  0.00  0
2016-05-02T05:37:02.569500	PD64.0        
2016-05-02T05:37:02.592499	@RT
2016-05-02T05:37:02.679501	fR- 0.25  0.00  0
2016-05-02T05:37:02.766493	fL- 0.25  0.00  0
2016-05-02T05:37:02.839491	pD64.0        
2016-05-02T05:37:02.862528	@RT
2016-05-02T05:37:02.948488	FR+ 2.00  0.00  0
2016-05-02T05:37:03.035488	FL+ 2.00  0.00  0
2016-05-02T05:37:03.108491	PD64.0        
2016-05-02T05:37:03.136484	WD35
2016-05-02T05:37:03.172483	TT 013
2016-05-02T05:37:03.182482	

2016-05-02T05:37:33.215423	
2016-05-02T05:37:34.216576	
2016-05-02T05:37:34.844529	NIDEK RT-5100 ID             DA2016/ 5/ 2
2016-05-02T05:37:34.866531	@RM
2016-05-02T05:37:34.953530	OR+ 2.25  0.00  0
2016-05-02T05:37:35.040526	OL+ 2.25  0.00  0
2016-05-02T05:37:35.113519	PD64.0        
2016-05-02T05:37:35.136518	@RT
2016-05-02T05:37:35.222517	fR- 0.25  0.00  0
2016-05-02T05:37:35.309514	fL- 0.25  0.00  0
2016-05-02T05:37:35.382512	pD64.0        
2016-05-02T05:37:35.405512	@RT
2016-05-02T05:37:35.492509	FR+ 3.75  0.00  0
2016-05-02T05:37:35.579507	FL+ 3.75  0.00  0
2016-05-02T05:37:35.652505	PD64.0        
2016-05-02T05:37:35.679515	WD35
2016-05-02T05:37:35.716511	TT 001
2016-05-02T05:37:35.725511	
2016-05-02T05:37:36.726600	

2016-05-02T05:39:00.819981	
2016-05-02T05:39:01.334911	NIDEK RT-5100 ID             DA2016/ 5/ 2
2016-05-02T05:39:01.356908	@RT
2016-05-02T05:39:01.443904	FR+10.00- 5.00 90
2016-05-02T05:39:01.530898	FL+10.00- 5.00 90
2016-05-02T05:39:01.603899	PD64.0        
2016-05-02T05:39:01.631897	WD35
2016-05-02T05:39:01.640899	

2016-05-02T05:41:10.778596	
2016-05-02T05:41:11.779744	
2016-05-02T05:41:12.228910	NIDEK RT-5100 ID             DA2016/ 5/ 2
2016-05-02T05:41:12.251909	@RM
2016-05-02T05:41:12.337905	OR- 1.00  0.00  0
2016-05-02T05:41:12.424903	OL- 1.00  0.00  0
2016-05-02T05:41:12.497901	PD64.0        
2016-05-02T05:41:12.520902	@RT
2016-05-02T05:41:12.607897	fR- 3.00  0.00  0
2016-05-02T05:41:12.693895	fL- 3.00  0.00  0
2016-05-02T05:41:12.767892	pD64.0        
2016-05-02T05:41:12.789901	@RT
2016-05-02T05:41:12.876893	FR- 2.00  0.00  0
2016-05-02T05:41:12.963885	FL- 2.00  0.00  0
2016-05-02T05:41:13.036885	PD64.0        
2016-05-02T05:41:13.064883	WD35
2016-05-02T05:41:13.100924	TT 004
2016-05-02T05:41:13.110883	

2016-05-02T05:44:17.782334	
2016-05-02T05:44:18.783482	
2016-05-02T05:44:19.784631	
2016-05-02T05:44:20.785256	
2016-05-02T05:44:21.646058	NIDEK RT-5100 ID             DA2016/ 5/ 2
2016-05-02T05:44:21.668071	@RM
2016-05-02T05:44:21.755055	OR+ 5.50- 1.25125
2016-05-02T05:44:21.842052	OL+ 5.50- 1.25125
2016-05-02T05:44:21.915053	PD64.0        
2016-05-02T05:44:21.938053	@RT
2016-05-02T05:44:22.024046	FR+ 2.50- 3.25 90
2016-05-02T05:44:22.111046	FL+ 2.50- 3.25 90
2016-05-02T05:44:22.157051	AR+ 1.50
2016-05-02T05:44:22.203045	AL+ 1.50
2016-05-02T05:44:22.276041	PD64.0        
2016-05-02T05:44:22.349034	Pd59.5        
2016-05-02T05:44:22.376036	WD35
2016-05-02T05:44:22.408034	wd 35
2016-05-02T05:44:22.417030	


Probleme avec les near vision SCA
===
Les données de near vision SCA : nrNr et nlNl sont décrites dans le manuel
Mais je n'ai jamais réussi à les obtenir. Le RT5100 Nidek ne les crache pas.
C'est bien dommage car cela aurait été pratique.
J'ai essayé parametre - SPH loin --> Pres : SPH + ADD ne marche pas.

Donc on va les calculer.  
On calcule uniquement : sph_near_vision  
qui n'est utile que pour l'impression de la formule en vision de pres.
on va l'afficher dans une vue form, uniquement pour des besoins de deboggage. 

recupérations des données du RT5100 
on récupere une ligne refraction prescription  
qui est une copie de la ligne MACV
on peut modifier on the fly cette ligne "refraction prescription" pour faire un ajustement final
il va falloir alors que le champ sph_near_vison soit modifié si on change la sphere ou l'add.
les datas de cette ligne "refraction prescription" sont utilisées pour l'impression de la formule : de loin, progressive de pres. 

 

On peut les calculer au moment ou l'on parse les données crachées par le RT5100 Nidek.
J'ai l'impression que ce n'est pas le plus pratiquement car là les données ne sont pas facilement extractibles ceux sont des listes de tuples. 
Finalement je le fait lors de la création du finalDict dans la méthode get_5100 de oph_agenda.py.
Mais la modification dans la form view de la sph ou de l'ADD ne modifie pas le champ sph_near. 
Il va falloir faire une méthode.
 