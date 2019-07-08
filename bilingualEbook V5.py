# coding: utf-8
import os # On importe le module os qui dispose de variables 
          # et de fonctions utiles pour dialoguer avec votre 
          # système d'exploitation
import math
# coeur du programme
def ouvrelelivre(nomdufichier):
	livreA = open(nomdufichier, "r", encoding="utf8")
	contenu = livreA.read()
	livreA.close()	
	return contenu

def splitAuxBalises(texte):
	texteAjuste=[]
	indexligne=0
	while indexligne<len(texte):
		debutBalise=0
		finBalise=0
		texteBalise=""
		debutBalise2=0
		finBalise2=0
		texteBalise2=""
			
		debutBalise = texte.find("<", indexligne)
		if debutBalise>=0:
			finBalise = texte.find(">", debutBalise)
			if finBalise-debutBalise > 1:
				texteBalise = texte[debutBalise+1:finBalise]
			if texteBalise == "p" or texteBalise == "v" or texteBalise == "subtitle":
				debutBalise2 = texte.find("</"+texteBalise, finBalise+1)
				finBalise2 = texte.find(">", debutBalise2)
				texteBalise2=""
				if finBalise2-debutBalise2 > 1:
					texteBalise2 = texte[debutBalise2+1:finBalise2]
				texteAjuste.append("   "+texte[debutBalise:finBalise2+1])
				indexligne=finBalise2+1			
			else:
				if finBalise<len(texte)-1:
					debutBalise2 = texte.find("<", finBalise+1)
					if debutBalise2>=0:
						finBalise2 = texte.find(">", debutBalise2)
						texteBalise2=""
						if finBalise2-debutBalise2 > 1:
							texteBalise2 = texte[debutBalise2+1:finBalise2]
						if "/"+texteBalise == texteBalise2 or texteBalise == "p" or texteBalise == "v" or texteBalise == "subtitle":
							texteAjuste.append(" "+texte[debutBalise:finBalise2+1])
							indexligne=finBalise2+1
						else:
							texteAjuste.append(" "+texte[debutBalise:finBalise+1])
							indexligne=finBalise+1
					else: 
						indexligne=len(texte)
						#ligne finie
				else:
					indexligne=len(texte)
					#fin du bouquin
		else:
			indexligne=len(texte)
	
	return texteAjuste

def findSectionBalises(listeTexte):
	balisesDesSections=[]
	i=0
	sectionouverte=0
	vecteurainjecter=[]
	vecteurainjecterTitle=[]
	#numeroDeSection=1
	while i<len(listeTexte):
		if sectionouverte == 0:
			indexBody = listeTexte[i].find("<section>")
			if indexBody >= 0:
				#vecteurainjecter.append(numeroDeSection)
				#numeroDeSection+=1
				vecteurainjecter.append(i)
				sectionouverte = 1
			
		else:
			indexTitle1 = listeTexte[i].find("<title>")
			indexTitle2 = listeTexte[i].find("</title>")
			if indexTitle1 >= 0 or indexTitle2 >= 0:
				vecteurainjecterTitle.append(i)
			
			indexBody = listeTexte[i].find("</section>")
			if indexBody >= 0:
				vecteurainjecter.append(i)
				sectionouverte = 0
				balisesDesSections.append([vecteurainjecter,vecteurainjecterTitle])
				vecteurainjecter=[]
				vecteurainjecterTitle=[]
			
		i+=1
		
	return balisesDesSections

def danslasection(i, balisesDesSections):
	numeroDeSection=-1
	isTitle = 0
	
	z=0
	while z < len(balisesDesSections):
		if balisesDesSections[z][0][0] <= i and i <=balisesDesSections[z][0][1]:
			numeroDeSection=z
			if balisesDesSections[z][1][0] <= i and i <= balisesDesSections[z][1][1]:
				isTitle=1
			return [numeroDeSection,isTitle]
		z+=1	
	return [numeroDeSection,isTitle]

def jListeTexteTOjData(j, DataB):
	jData=0
	while jData<len(DataB):
		if DataB[jData][0] == j:
			return jData
		jData+=1
	
	jData=0 #si j n'est pas dans Data (une balise <cite> par exemple) alors on donne un résultat inexacte
	while jData<len(DataB):
		if DataB[jData][0] in [j-1,j+1]:
			return jData
		jData+=1
	
	return 50000
	
def findBodyBalise(listeTexte):
	i=0
	while i<len(listeTexte):
		indexBody = listeTexte[i].find("<body>")
		i+=1
		if indexBody >= 0:
			return i
	return 0
	
def ispORvMethode(ligneatester):
	indexbalise = ligneatester.find("<")
	if indexbalise >=0:
		if ligneatester[indexbalise:(indexbalise+3)] in("<p>", "<v>", "<subtitle>"):
			return 1
		else:
			return 0
	else:
		return 0

def isParoleMethode(ligneatester, strParoleType):
	indexbalise = ligneatester.find("<")
	i=0
	j=0
	while i==0 and j<=len(ligneatester):
		if ligneatester[indexbalise+3+j]in(" ", "	"):
			j+=1
		elif ligneatester[indexbalise+3+j] == "<" : #deuxieme balise
			j = ligneatester[indexbalise+3+j:].find(">") + 1 - (indexbalise+3)
			
		else:
			i=1
	
	if ligneatester[indexbalise+3+j] == strParoleType:
		return 1
	else:
		return 0
	
def determineStrParole(listeTexte):
	i=0
	listecandidat=[]
	while i<len(listeTexte):
		ispORv = ispORvMethode(listeTexte[i])
		if ispORv == 1:
			indexbalise = listeTexte[i].find("<")
			#print("indexbalise = "+str(indexbalise))
			k=0
			j=0
			while k==0 and j<len(listeTexte[i]):
				if listeTexte[i][indexbalise+3+j]in(" ", "	"):
					j+=1
				else:
					k=1
			candidati = listeTexte[i][indexbalise+3+j]
			existe=0
			existei=0
			while  existei < len(listecandidat):
				if listecandidat[existei][0] == candidati:
					existe = 1
					nombreoccurence = 1+listecandidat[existei][1]
					del listecandidat[existei]
					listecandidat.append([candidati,nombreoccurence])
					existei = len(listecandidat)
				else:
					existei += 1
			if existe==0:
				listecandidat.append([candidati,1])
			
		i+=1
	#listecandidattxt = open("listecandidattxt.txt", "a", encoding="utf8")
	#m=0
	#while m <len(listecandidat):
	#	listecandidattxt.write(str(listecandidat[m][0])+" => "+ str(listecandidat[m][1])+"\n")
	#	m+=1
	#listecandidattxt.close()
	
	candidatfinal=0
	m=0
	while m <len(listecandidat):
		if listecandidat[m][1] > listecandidat[candidatfinal][1]:
			candidatfinal=m
		m+=1
	straretourner = listecandidat[candidatfinal][0]
	return straretourner

def determineLongueurSTR(Data):
	LongueurSTR=[0,0]
	SommeLongueurs = 0
	MaxLongueur = 0
	i=0
	while i<len(Data):
		SommeLongueurs = SommeLongueurs + Data[i][3]
		if Data[i][3] > MaxLongueur:
			MaxLongueur = Data[i][3]
		i+=1
	LongueurSTR = [math.floor(SommeLongueurs/len(Data)),MaxLongueur]
	return LongueurSTR

def CalculBonusLongueur(DataAki,DataBkj,LongueurTexteA,LongueurTexteB):
	bonus=0
	Longueuri=math.floor(DataAki[3]*LongueurTexteB[0]/LongueurTexteA[0])
	Longueurj=DataBkj[3]
	LongueurMaxi = math.floor(LongueurTexteA[1]*LongueurTexteB[0]/LongueurTexteA[0])
	LongueurMaxj = LongueurTexteB[1]
	if (Longueurj > math.floor(Longueuri*0.8) and Longueurj < math.floor(Longueuri*1.2)) or (Longueurj > Longueuri-math.floor(0.05*LongueurMaxi) and Longueurj < Longueuri+math.floor(0.05*LongueurMaxi)): 
		bonus = 2
	elif (Longueurj > math.floor(Longueuri*0.6) and Longueurj < math.floor(Longueuri*1.4)) or (Longueurj > Longueuri-math.floor(0.10*LongueurMaxi) and Longueurj < Longueuri+math.floor(0.10*LongueurMaxi)):
		bonus = 0
	else: 
		bonus = -2
	return bonus
	
def calculeduscoreMethode(i,j,DataA,DataB,LongueurTexteA,LongueurTexteB,NumSectioni,balisesDesSectionsA,balisesDesSectionsB):
	score = 0
	Longueuri=math.floor(DataA[i][3]*LongueurTexteB[0]/LongueurTexteA[0])
	p=0
	changements=0
	ScoreVersLeHaut=0
	IsErrorYet=0
	IsParoleTourPrecedent=DataA[i][2]
	ki=i-1
	kj=j-1
	bonusCredibilite = 1
	bonusCredibilite2=0
	if i>5 and j>5:
		if (DataA[i-1][4] > j and DataA[i-2][4] > j and DataA[i-3][4] > j and (DataA[i-1][4]==DataA[i-2][4]-1 or DataA[i-2][4]==DataA[i-3][4]-1 )) or (DataA[i-4][4] > j and DataA[i-2][4] > j and DataA[i-3][4] > j and (DataA[i-2][4]==DataA[i-3][4]-1 or DataA[i-3][4]==DataA[i-4][4]-1 )):
			# si les 3 bestmatch précédents sont plus grand que j alors c'est impossible
			bonusCredibilite = 0.25
		#if DataA[i-1][4] == j-1:
		#	ki=ki
		#	if DataA[i-2][4] == j-2 and DataA[i-3][4] == j-3 and DataA[i-4][4] == j-4:
		#		bonusCredibilite = 1.5
		#		bonusCredibilite2 = 50
		#elif DataA[i-2][4] == j-1: # and DataA[i-3][4] == j-2:
		#	ki=ki-1
			#if DataA[i-3][4] == j-2 and DataA[i-4][4] == j-3 and DataA[i-5][4] == j-4:
				#bonusCredibilite = 1.5
				#bonusCredibilite2 = 40
		#elif DataA[i-1][4] == j-2: # and DataA[i-2][4] == j-3:
		#	kj=kj-1
			#if DataA[i-2][4] == j-3 and DataA[i-3][4] == j-4 and DataA[i-4][4] == j-5:
			#	bonusCredibilite = 1.5
			#	bonusCredibilite2 = 40
		#elif DataA[i-2][4] == j-2:
		#	ki=ki-1
		#	kj=kj-1
			#if DataA[i-3][4] == j-3 and DataA[i-4][4] == j-4 and DataA[i-5][4] == j-5:
			#	bonusCredibilite = 1.3
			#	bonusCredibilite2 = 30
		#elif DataA[i-3][4] == j-3:
		#	ki=ki-2
		#	kj=kj-2
			#if DataA[i-4][4] == j-4 and DataA[i-5][4] == j-5:
			#	bonusCredibilite = 1
			#	bonusCredibilite2 = 10
		#elif DataA[i-4][4] == j-4:
		#	ki=ki-3
		#	kj=kj-3
		#elif DataA[i-5][4] == j-5:
		#	ki=ki-4
		#	kj=kj-4
			#bonusCredibilite = 1.5
		#elif DataA[i-3][4] == j-1 and DataA[i-4][4] == j-2:
		#	ki=ki-2
		#elif DataA[i-4][4] == j-1 and DataA[i-5][4] == j-2:
		#	ki=ki-3
		#elif DataA[i-5][4] == j-1 and DataA[i-6][4] == j-2:
		#	ki=ki-4
		#elif DataA[i-1][4] == j-3 and DataA[i-2][4] == j-4:
		#	kj=kj-2
		#elif DataA[i-1][4] == j-4 and DataA[i-2][4] == j-5:
		#	kj=kj-3
		#elif DataA[i-1][4] == j-5 and DataA[i-2][4] == j-6:
		#	kj=kj-4
		
	while kj>=jListeTexteTOjData(balisesDesSectionsB[NumSectioni[0]][1][1]+1, DataB) and ki>=jListeTexteTOjData(balisesDesSectionsA[NumSectioni[0]][1][1]+1, DataA) and (p<=15 or changements<3) and IsErrorYet==0:
		if DataA[ki][2] == DataB[kj][2]:
			ScoreVersLeHaut+=1#*changements
			#if DataA[ki][4] == DataB[kj][0]:
			#	ScoreVersLeHaut = ScoreVersLeHaut+1
			Bonuslongueur = CalculBonusLongueur(DataA[ki],DataB[kj],LongueurTexteA,LongueurTexteB)
			ScoreVersLeHaut+= Bonuslongueur*(changements/3+1) #intérêt pas confirmé du multiplicateur
			if DataA[ki][2]!= IsParoleTourPrecedent:
				changements+=1
				IsParoleTourPrecedent=DataA[ki][2]
		else: 
			IsErrorYet=1
		p+=1
		kj-=1
		ki-=1
	ScoreVersLeHaut = ScoreVersLeHaut*(1+changements)+5*changements
	
	p=0
	changements=0
	ScoreVersLebas=0
	IsErrorYet=0
	IsParoleTourPrecedent=DataA[i][2]
	ki=i+1
	kj=j+1
	while kj<jListeTexteTOjData(balisesDesSectionsB[NumSectioni[0]][0][1]-1,DataB) and ki<jListeTexteTOjData(balisesDesSectionsA[NumSectioni[0]][0][1]-1,DataA) and (p<=20 or changements<3) and IsErrorYet==0:
		#if i==129:
		#	LivreDesScores4 = open("LivreDesScores4.txt", "a", encoding="utf8")
		#	LivreDesScores4.write(" i : "+str(i)+" j : "+str(j)+" ki-kj : " +str(ki)+"-"+str(kj)+ "\n")
		#	LivreDesScores4.close()
		if DataA[ki][2] == DataB[kj][2]:
			ScoreVersLebas+=1#*changements
			Bonuslongueur = CalculBonusLongueur(DataA[ki],DataB[kj],LongueurTexteA,LongueurTexteB)
			ScoreVersLeHaut+= Bonuslongueur*(changements/3+1)
			if DataA[ki][2]!= IsParoleTourPrecedent:
				changements+=1
				IsParoleTourPrecedent=DataA[ki][2]
		else: 
			IsErrorYet=1
		p+=1
		kj+=1
		ki+=1
	ScoreVersLebas = ScoreVersLebas*(1+changements)+5*changements
	score = ScoreVersLeHaut+ScoreVersLebas
	
	Bonuslongueur=0
	if i>4 and j>4:
		if (DataA[i-1][4] != j) and (DataA[i-2][4] == j-1 and DataA[i-3][4] == j-2):
			Bonuslongueur=0
		else:
			Bonuslongueur = CalculBonusLongueur(DataA[i],DataB[j],LongueurTexteA,LongueurTexteB)*15
	score = score * bonusCredibilite + Bonuslongueur + bonusCredibilite2
	
	return score

def actualiseInaROW(DataA):
	i=0
	inaRow=0
	while i<len(DataA):
	
		if i>2:
			if DataA[i-1][4] == DataA[i][4]-1 or (DataA[i-1][4] == DataA[i][4] and DataA[i-2][4] == DataA[i][4]-1) or (DataA[i-1][4] == DataA[i][4] and DataA[i-2][4] == DataA[i][4] and DataA[i-3][4] == DataA[i][4]-1):
				inaRow+=1
			else:
				inaRow=0
		del DataA[i][6]
		DataA[i].append(inaRow)
		i+=1
	i=1
	while i<len(DataA):
		if DataA[i][6]!= DataA[i-1][6]+1:
			j=1
			while j<=DataA[i-1][6]:
			
				del DataA[i-1-j][6]
				DataA[i-1-j].append(DataA[i-1][6])
				j+=1
		
		i+=1
		
	return DataA

texteA = ouvrelelivre("garri.fb2") #grosse str
texteB = ouvrelelivre("harry.fb2")#grosse str

listeTexteA = splitAuxBalises(texteA)
listeTexteB = splitAuxBalises(texteB)
#listeTexteA = texteA.splitlines()
#listeTexteB = texteB.splitlines()
DataA = []
DataB = []
strParoleTypeA = determineStrParole(listeTexteA)
strParoleTypeB = determineStrParole(listeTexteB)
STRLUES = open("strlues.txt", "w", encoding="utf8")
STRLUES.write("winer is livre A : "+ strParoleTypeA+"\n" + "winer is livre B : "+ strParoleTypeB+"\n")
STRLUES.close()

balisesDesSectionsA = findSectionBalises(listeTexteA)
i=findBodyBalise(listeTexteA)
print("find body balise A : i = "+str(i))
while i<len(listeTexteA):
	ispORv = ispORvMethode(listeTexteA[i])
	isParole = 0
	if ispORv == 1:
		isParole = isParoleMethode(listeTexteA[i], strParoleTypeA)
		lenLigne=len(listeTexteA[i])
		DataA.append([i,ispORv,isParole,lenLigne])
	
	i+=1

balisesDesSectionsB = findSectionBalises(listeTexteB)
i=findBodyBalise(listeTexteB)
print("find body balise B : i = "+str(i))
while i<len(listeTexteB):
	ispORv = ispORvMethode(listeTexteB[i])
	isParole = 0
	if ispORv == 1:
		isParole = isParoleMethode(listeTexteB[i], strParoleTypeB)
		lenLigne=len(listeTexteB[i])
		DataB.append([i,ispORv,isParole,lenLigne])
		
	i+=1

LongueurTexteA = determineLongueurSTR(DataA)
LongueurTexteB = determineLongueurSTR(DataB)	
print( str(LongueurTexteA[0]) + " " +str(LongueurTexteA[1]) + "     " +  str(LongueurTexteB[0]) + " " +str(LongueurTexteB[1]) )	
print("datas len : " + str(len(DataA))+"  "  +str(len(DataB)))
print("nombre sections A et B : " + str(len(balisesDesSectionsA))+"  "  +str(len(balisesDesSectionsB)))
iii=0
while iii<len(balisesDesSectionsA) and iii<len(balisesDesSectionsB):
	print("section "+ str(iii)+"  pour A : "+ str(balisesDesSectionsA[iii][0]) + " tot=" + str(balisesDesSectionsA[iii][0][1]-balisesDesSectionsA[iii][1][1]) + " pour B : " + str(balisesDesSectionsB[iii][0]) + " tot=" + str(balisesDesSectionsB[iii][0][1]-balisesDesSectionsB[iii][1][1]))
	iii+=1
os.system("pause")
################################################### Matching principal ####################################################
LivreDesScores = open("LivreDesScores.txt", "w", encoding="utf8")
i=0
inaRow=0
while i<len(DataA):
	print("matching numero : "+str(i)+"\n")
	matchpoint = []
	j=0
	jend=len(DataB)	
	NumSectioni=danslasection(DataA[i][0], balisesDesSectionsA) #vecteur type [ numero section, istitle ]
	if NumSectioni[0]<0:
		matchpoint.append([0, -1])
	elif NumSectioni[1]== 1:
		#traiter un titre
		numeroLigneTitre = DataA[i][0]-balisesDesSectionsA[NumSectioni[0]][1][0]
		if numeroLigneTitre < (balisesDesSectionsB[NumSectioni[0]][1][1]-balisesDesSectionsB[NumSectioni[0]][1][0]):
			matchpoint.append([jListeTexteTOjData(balisesDesSectionsB[NumSectioni[0]][1][0] + numeroLigneTitre, DataB), 10000])
		else: 
			matchpoint.append([0, -1])
	else :
		#traiter une ligne normale : tester que dans la meme section + les lignes alentours
		
		
		DifferenceAmoinsB = (balisesDesSectionsA[NumSectioni[0]][0][1]-balisesDesSectionsA[NumSectioni[0]][1][1]) - (balisesDesSectionsB[NumSectioni[0]][0][1]-balisesDesSectionsB[NumSectioni[0]][1][1])
		ip = DataA[i][0] - balisesDesSectionsA[NumSectioni[0]][1][1]
		jp = max(min(ip, ip - DifferenceAmoinsB)-2,1)
		j =  jListeTexteTOjData(jp + balisesDesSectionsB[NumSectioni[0]][1][1],DataB)
		jpend = min(max(ip, ip - DifferenceAmoinsB)+2,balisesDesSectionsB[NumSectioni[0]][0][1]-balisesDesSectionsB[NumSectioni[0]][1][1]-1)
		jend = 1+jListeTexteTOjData(jpend + balisesDesSectionsB[NumSectioni[0]][1][1],DataB)
		jend = min(jend,jListeTexteTOjData(balisesDesSectionsB[NumSectioni[0]][0][1]-1,DataB))
		LivreDesScores.write("j-jend["+str(j)+", "+str(jend)+"] ")
		while j < jend:
			if DataA[i][2] == DataB[j][2]: # or (DataA[i-1][4] == j-1 and DataA[i-2][4] == j-2 and DataA[i-3][4] == j-3) or (DataA[i-4][4] == j-4 and DataA[i-2][4] == j-2 and DataA[i-3][4] == j-3):
				#SI c'est du meme signe ou si c'est dans un row on fait le calcul du score
				scoredematching = calculeduscoreMethode(i,j,DataA,DataB,LongueurTexteA,LongueurTexteB,NumSectioni,balisesDesSectionsA,balisesDesSectionsB)
				matchpoint.append([j, scoredematching])
			
			j+=1
	
	
	bestmatch = [0,-1]
	var1 = 0
	while var1 < len(matchpoint):
		if matchpoint[var1][1] >= bestmatch[1] and matchpoint[var1][0]<len(DataB):
			bestmatch = matchpoint[var1]
		var1 += 1
		
	DataA[i].append(bestmatch[0]) #DataB[bestmatch[0]][0]
	DataA[i].append(bestmatch[1])
	if i>2:
		if DataA[i-1][4] == bestmatch[0]-1 or (DataA[i-1][4] == bestmatch[0] and DataA[i-2][4] == bestmatch[0]-1) or (DataA[i-1][4] == bestmatch[0] and DataA[i-2][4] == bestmatch[0] and DataA[i-3][4] == bestmatch[0]-1):
			inaRow+=1
		else:
			inaRow=0
	DataA[i].append(inaRow)
	LivreDesScores.write(str(DataA[i][0]) + " dataA["+str(i)+"] : " "   paragraphe B : "+str(DataB[bestmatch[0]][0])+ "     score : "+str(math.floor(bestmatch[1]))+ "  inaROW "+str(inaRow) +"\n")
	i+=1

LivreDesScores.close()

##################################################  Relissage ######################################
i=1
while i<len(DataA):
	if DataA[i][6]!= DataA[i-1][6]+1:
		j=1
		while j<=DataA[i-1][6]:
			
			del DataA[i-1-j][6]
			DataA[i-1-j].append(DataA[i-1][6])
			j+=1
		
	i+=1
jo=0
while jo<2:	
	i=3
	while i<len(DataA)-3:
		NumSectioni=danslasection(DataA[i][0], balisesDesSectionsA) #vecteur type [ numero section, istitle
		if (DataA[i][4]!= DataA[i-1][4]+1) and DataA[i][6]<=1 and NumSectioni[1]!= 1:
			# 235 - X - 237
			if (DataA[i-1][4] == DataA[i+1][4]-2) and (DataA[i-1][6]>0 or DataA[i+1][6]>0):
				del DataA[i][4]
				DataA[i].insert(4, DataA[i-1][4]+1)
				del DataA[i][5]
				DataA[i].insert(5, 11)
			#235 - X - 236
			elif (DataA[i-1][4] == DataA[i+1][4]-1) and (DataA[i-1][6]>2 or DataA[i+1][6]>2):
				del DataA[i][4]
				DataA[i].insert(4, DataA[i-1][4])
				del DataA[i][5]
				DataA[i].insert(5, 11)
			#235 - X - 238
			elif (DataA[i-1][4] == DataA[i+1][4]-3) and (DataA[i-1][6]>2 or DataA[i+1][6]>2):
				del DataA[i][4]
				DataA[i].insert(4, DataA[i-1][4]+1)
				del DataA[i][5]
				DataA[i].insert(5, 11)
			#235 - X - 235
			elif (DataA[i-1][4] == DataA[i+1][4]) and (DataA[i-1][6]>2 or DataA[i+1][6]>2):
				del DataA[i][4]
				DataA[i].insert(4, DataA[i-1][4])
				del DataA[i][5]
				DataA[i].insert(5, 11)
			#235 - X - Y - 238
			elif (DataA[i-1][4] == DataA[i+2][4]-3) and DataA[i+1][6]<=1 and (DataA[i-1][6]>2 or DataA[i+2][6]>2):
				del DataA[i][4]
				DataA[i].insert(4, DataA[i-1][4]+1)
				del DataA[i][5]
				DataA[i].insert(5, 11)
			#235 - X - Y - 237
			elif (DataA[i-1][4] == DataA[i+2][4]-2) and DataA[i+1][6]<=1 and (DataA[i-1][6]>2 or DataA[i+2][6]>2):
				del DataA[i][4]
				DataA[i].insert(4, DataA[i-1][4])
				del DataA[i+1][4]
				DataA[i+1].insert(4, DataA[i-1][4]+1)
				del DataA[i][5]
				DataA[i].insert(5, 11)
				del DataA[i+1][5]
				DataA[i+1].insert(5, 11)
			#235 - null - null - ...
			elif DataA[i][5]==-1 and DataA[i-1][6]>2:
				del DataA[i][4]
				DataA[i].insert(4, DataA[i-1][4]+1)
				del DataA[i][5]
				DataA[i].insert(5, 11) 
		i+=1
		DataA = actualiseInaROW(DataA)
	jo+=1
	
i=3
while i<len(DataA)-3:
	NumSectioni=danslasection(DataA[i][0], balisesDesSectionsA) #vecteur type [ numero section, istitle
	if (DataA[i][4]!= DataA[i-1][4]+1) and NumSectioni[1]!= 1:
		# 235 - X - 237
		if (DataA[i-1][4] == DataA[i+1][4]-2) and (DataA[i-1][6]>0 or DataA[i+1][6]>0):
			del DataA[i][4]
			DataA[i].insert(4, DataA[i-1][4]+1)
			del DataA[i][5]
			DataA[i].insert(5, 11)
		#235 - 235 - 237 ??????????????????????????????????????????????????????????????????????,,
		elif (DataA[i][4] == DataA[i+1][4]-2) and (DataA[i-1][4] == DataA[i][4]):
			del DataA[i][4]
			DataA[i].insert(4, DataA[i-1][4]+1)
			del DataA[i][5]
			DataA[i].insert(5, 11)
	i+=1
DataA = actualiseInaROW(DataA)
		
LivreDesScores2 = open("LivreDesScores2.txt", "w", encoding="utf8")
i=0
while i<len(DataA):
	LivreDesScores2.write(str(DataA[i][0]) + " dataA["+str(i)+"] : " "   paragraphe B : "+str(DataB[DataA[i][4]][0])+ "     score : "+str(math.floor(DataA[i][5]))+ "  inaROW "+str(DataA[i][6]) +"\n")
	i+=1

LivreDesScores2.close()

##################################################  Edition du livre  ##############################
listeTexteAVecteur = []	
i=0
while i<len(listeTexteA):
	listeTexteAVecteur.append([listeTexteA[i], -1])
	i+=1

i=0
while i<len(DataA):
	if DataA[i][5]> 10 or DataA[i][6]>3 : #si le score est plus grand que 10
		nouveauvecteur=[listeTexteA[DataA[i][0]], DataB[DataA[i][4]][0]] #DataA[i][4]	
		del listeTexteAVecteur[DataA[i][0]]
		listeTexteAVecteur.insert(DataA[i][0], nouveauvecteur)
	i+=1
		
	
livreFinal = open("LivreFinal.fb2", "w", encoding="utf8")

i=0
while i<len(listeTexteAVecteur):
	if listeTexteAVecteur[i][1]<0:
		livreFinal.write(listeTexteAVecteur[i][0] + "\n")
	else :
		livreFinal.write(listeTexteAVecteur[i][0] + "\n" + listeTexteB[listeTexteAVecteur[i][1]] + "\n")
	i+=1

#livreFinal.write(listeTexteA[5])
#livreFinal.write(str(len(listeTexteA)))
livreFinal.close()
	
	

# On met le programme en pause pour éviter qu'il ne se referme (Windows)
os.system("pause")