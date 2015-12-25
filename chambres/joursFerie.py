#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
def datepaques(an):
	"""Calcule la date de Paques d'une annee donnee an (=nombre entier)"""
	a=an//100
	b=an%100
	c=(3*(a+25))//4
	d=(3*(a+25))%4
	e=(8*(a+11))//25
	f=(5*a+b)%19
	g=(19*f+c-e)%30
	h=(f+11*g)//319
	j=(60*(5-d)+b)//4
	k=(60*(5-d)+b)%4
	m=(2*j-k-g+h)%7
	n=(g-h+m+114)//31
	p=(g-h+m+114)%31
	jour=p+1
	mois=n
	return [jour, mois, an]
def datechaine(d, sep='/'):
	"""Transforme une date liste=[j,m,a] en une date chaîne 'jj/mm/aaaa'"""
	return ("%02d" + sep + "%02d" + sep + "%0004d") % (d[0], d[1], d[2])

def dateliste(c, sep='/'):
	"""Transforme une date chaîne 'j/m/a' en une date liste [j,m,a]"""
	j, m, a = c.split(sep)
	return [int(j), int(m), int(a)]

def jourplus(d, n=1):
	"""Donne la date du nième jour suivant d=[j, m, a] (n>=0)"""
	j, m, a = d
	fm = [0,31,28,31,30,31,30,31,31,30,31,30,31]
	if (a%4==0 and a%100!=0) or a%400==0:  # bissextile?
		fm[2] = 29
	for i in range(0,n):
		j += 1
		if j > fm[m]:
			j = 1
			m += 1
			if m>12:
				m = 1
				a += 1
	return [j,m,a]
def jourmoins(d, n=-1):
	"""Donne la date du nième jour précédent d=[j, m, a] (n<=0)"""
	j, m, a = d
	fm = [0,31,28,31,30,31,30,31,31,30,31,30,31]
	if (a%4==0 and a%100!=0) or a%400==0:  # bissextile?
		fm[2] = 29
	for i in range(0,abs(n)):
		j -= 1
		if j < 1:
			m -= 1
			if m<1:
				m = 12
				a -= 1
			j = fm[m]
	return [j,m,a]
def numjoursem(d):
	"""Donne le numero du jour de la semaine d'une date d=[j,m,a]
	   lundi=1, mardi=2, ..., dimanche=7
	   Algorithme de Maurice Kraitchik (1882–1957)"""
	j, m, a = d
	if m<3:
		m += 12
		a -= 1
	n = (j +2*m + (3*(m+1))//5 +a + a//4 - a//100 + a//400 +2) % 7
	return [6, 7, 1, 2, 3, 4, 5][n]
 
def joursem(d):
	"""Donne le jour de semaine en texte a partir de son numero
	   lundi=1, mardi=2, ..., dimanche=7"""
	return ["", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi",
			 "dimanche"][numjoursem(d)]
def joursferiesliste(an, sd=0):
	"""Liste des jours feries France en date-liste de l'annee an (nb entier). 
		 sd=0 (=defaut): tous les jours feries. 
		 sd=1: idem sans les sammedis-dimanches. 
		 sd=2: tous + les 2 jours feries supplementaires d'Alsace-Moselle. 
		 sd=3: idem sd=2 sans les samedis-dimanches"""
	F = []  # =liste des dates des jours feries en date-liste d=[j,m,a]
	L = []  # =liste des libelles du jour ferie
	dp = datepaques(an)
 
	# Jour de l'an
	d = [1,1,an]
	nj = numjoursem(d)
	if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
		F.append(d)
		L.append("Jour de l'an")
 
	# Vendredi saint (pour l'Alsace-Moselle)
	d = jourmoins(dp, -2)
	if sd>=2:
		F.append(d)
		L.append("Vendredi saint")
 
	# Dimanche de Paques
	d = dp
	if (sd==0) or (sd==2):
		F.append(d)
		L.append("Dimanche de Paques")
 
	# Lundi de Paques
	d = jourplus(dp, +1)
	F.append(d)
	L.append("Lundi de Paques")
 
	# Fete du travail
	d = [1,5,an]
	nj = numjoursem(d)
	if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
		F.append(d)
		L.append("Fete du travail")
 
	# Victoire des allies 1945
	d = [8,5,an]
	nj = numjoursem(d)
	if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
		F.append(d)
		L.append("Victoire des allies 1945")
 
	# Jeudi de l'Ascension
	d = jourplus(dp, +39)
	F.append(d)
	L.append("Jeudi de l'Ascension")
 
	# Dimanche de Pentecote
	d = jourplus(dp, +49)
	if (sd==0) or (sd==2):
		F.append(d)
		L.append("Dimanche de Pentecote")
 
	# Lundi de Pentecote
	d = jourplus(d, +1)
	F.append(d)
	L.append("Lundi de Pentecote")
 
	# Fete Nationale
	d = [14,7,an]
	nj = numjoursem(d)
	if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
		F.append(d)
		L.append("Fete Nationale")
 
	# Assomption
	d = [15,8,an]
	nj = numjoursem(d)
	if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
		F.append(d)
		L.append("Assomption")
 
	# Toussaint
	d = [1,11,an]
	nj = numjoursem(d)
	if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
		F.append(d)
		L.append("Toussaint")
 
	# Armistice 1918
	d = [11,11,an]
	nj = numjoursem(d)
	if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
		F.append(d)
		L.append("Armistice 1918")
 
	# Jour de Noel
	d = [25,12,an]
	nj = numjoursem(d)
	if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
		F.append(d)
		L.append("Jour de Noel")
 
	# Saint Etienne (pour l'Alsace-Moselle)
	d = [26,12,an]
	nj = numjoursem(d)
	if (sd==2) or (sd==3 and nj<6):
		F.append(d)
		L.append("Saint Etienne")
 
	return F, L

def estferie(d,sd=0):
	"""estferie(d,sd=0): => dit si une date d=[j,m,a] donnee est feriee France
	   si la date est feriee, renvoie son libelle
	   sinon, renvoie une chaine vide"""
	j,m,a = d.day,d.month,d.year
	F, L = joursferiesliste(a, sd)
	for i in range(0, len(F)):
		if j==F[i][0] and m==F[i][1] and a==F[i][2]:
			return L[i]
	return ""
