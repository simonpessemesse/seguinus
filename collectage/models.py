from django.db import models
from datetime import datetime,date

jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


SEXE = (
	('M', 'Masculin'),
	('F', 'Feminin'),
)

DENOMINATION=(
	('M','Monsieur'),
	('L','Mademoiselle'),
	('A','Madame'),

	)

ETAT_CIVIL=(
	('C','Celibataire'),
	('M','Marie'),
	)

class Employe(models.Model):
	nom = models.CharField(max_length=200,blank=True)
	prenom = models.CharField(max_length=200,blank=True)
	dateNaissance = models.DateField(blank=True,null=True)
	sexe = models.CharField(max_length=1, choices=SEXE,blank=True,null=True)
	nationalite = models.CharField(max_length=200,blank=True)
	emploi = models.CharField(max_length=200,blank=True)
	qualification = models.CharField(max_length=200,blank=True)
	adresse=models.TextField(blank=True)
	numeroSecuriteSociale = models.CharField(max_length=200,blank=True)
	emploi = models.CharField(max_length=200,blank=True)
	typeDuContrat = models.CharField(max_length=200,blank=True)
	evenementsPosterieursALembauche = models.CharField(max_length=200,blank=True)
	dateEntree = models.DateField(blank=True,null=True)
	dateSortie = models.DateField(blank=True,null=True)
	nombreHeuresMois=models.DecimalField(max_digits=7,decimal_places=3,null=True,blank=True)
	def __str__(self):
		return self.prenom#+" "+self.no




class Individu(models.Model):
	nom = models.CharField(max_length=200)
	prenom = models.CharField(max_length=200)
	denomination = models.CharField(max_length=1, choices=DENOMINATION,blank=True,null=True)
	nomJeuneFille = models.CharField(max_length=200,blank=True)
	dateNaissance = models.DateField(blank=True,null=True)
	communeNaissance = models.CharField(max_length=200,blank=True)
	paysNaissance =models.CharField(max_length=200,blank=True)
	sexe = models.CharField(max_length=1, choices=SEXE,blank=True,null=True)
	situationDeFamille=models.CharField(max_length=1,choices=ETAT_CIVIL,blank=True)
	nationalite = models.CharField(max_length=200,blank=True)
	adresse=models.TextField(blank=True)
	numeroSecuriteSociale = models.CharField(max_length=200,blank=True)
	numeroTelephone=models.CharField(max_length=100,blank=True)
	def __str__(self):
		return self.prenom+" "+self.nom
	def denom(self):
		try:
			dem=self.get_denomination_display()
			if dem is None:
				dem=""
		except:
			dem=""
		return dem+" "+self.prenom+" "+self.nom
	def anniv(self,year):
		if not self.dateNaissance:
			return "inconnu"
		age=year-self.dateNaissance.year
		anniv=date(year,self.dateNaissance.month,self.dateNaissance.day)
		st=self.prenom+" "+self.nom+" a "+str(age)+" ans le "+jours[anniv.weekday()]+" "+str(anniv.day)+"/"+str(anniv.month)
		return st
	def age(self):
		if not self.dateNaissance:
			return "inconnu"
		age=date.today()-self.dateNaissance
		return age.days/365


TYPE_CONTRAT=(
	('S','Saisonnier'),
	('P','Saisonnier Temps Partiel'),
	('E','Extra'),
	('I','Indetermine'),
	('D','Determine'),
	('X','Determine Temps Partiel'),
	('A','Avenant'),
	)

class Pourboire(models.Model):
	montant=models.DecimalField(max_digits=9,decimal_places=2)
	individus=models.ManyToManyField(Individu)
	date=models.DateTimeField(default=datetime.now)
	commentaire=models.CharField(max_length=300,blank=True)
	def __str__(self):
		return str(self.montant)+" le "+str(self.date)

class DonPourboire(models.Model):
	date=models.DateTimeField(default=datetime.now)
	montant=models.DecimalField(max_digits=9,decimal_places=2)
	individu=models.ForeignKey(Individu)
	commentaire=models.CharField(max_length=300,blank=True)
	def __str__(self):
		return str(self.date)+" pour "+str(self.individu)

class Contrat(models.Model):
	individu=models.ForeignKey(Individu)
	dateDebut=models.DateField(blank=True,null=True)
	dateFin=models.DateField(blank=True,null=True)
	qualification = models.CharField(max_length=200,blank=True)
	motifContrat = models.CharField(max_length=200,blank=True)
	emploi = models.CharField(max_length=200)
	typeDuContrat = models.CharField(max_length=1,choices=TYPE_CONTRAT)
	contratAide=models.BooleanField(default=False)
	nombreHeuresSemaine=models.DecimalField(max_digits=7,decimal_places=3)
	nbRepasJour=models.SmallIntegerField()
	fonction = models.CharField(max_length=200,blank=True)
	coefficient = models.CharField(max_length=200,blank=True)
	tauxHoraireBrut=models.DecimalField(max_digits=10, decimal_places=4,blank=True,null=True,default=9.53)
	congeLundi=models.BooleanField(default=False)
	congeMardi=models.BooleanField(default=False)
	congeMercredi=models.BooleanField(default=False)
	congeJeudi=models.BooleanField(default=False)
	congeVendredi=models.BooleanField(default=False)
	congeSamedi=models.BooleanField(default=False)
	congeDimanche=models.BooleanField(default=False)
	surcroitActiviteWE=models.BooleanField(default=False)
	demiJourneeConge=models.SmallIntegerField(null=True,blank=True)# de 1 a 7 pour lundi a dimanche
#	heureDebutJournee=models.TimeField(null=True,blank=True)
#	heureDebutDeuxiemeService=models.TimeField(null=True,blank=True)
	def __str__(self):
		return self.get_typeDuContrat_display()+" du "+str(self.dateDebut)+" jusqu'au "+str(self.dateFin)
	def hMois(self):
		return str(float(self.nombreHeuresSemaine)*52./12)
	def hPremiereColonne(self):
		if self.nombreHeuresSemaine<=35:
			return str(self.nombreHeuresSemaine*52/12)
		else:
			return str(35.*52/12)
	def hSupplementaire10pourcent(self):
		if self.nombreHeuresSemaine>35 and self.nombreHeuresSemaine<=39:
			return (self.nombreHeuresSemaine-35)*52/12
		elif self.nombreHeuresSemaine>35:
			return 4.*52/12
		else:
			return 0
	def hSupplementaire20pourcent(self):
		if self.nombreHeuresSemaine>39 and self.nombreHeuresSemaine<=43:
			return (self.nombreHeuresSemaine-39)*52/12
		elif self.nombreHeuresSemaine>39:
			return 3.*52/12
		else:
			return 0

	def duree(self):
		if not self.dateDebut or not self.dateFin:
			return 0;
		return self.dateFin-self.dateDebut
	def dureePeriodeEssai(self):
		duree=self.duree()
		if duree.days/30.5>=6:
			return 30
		return min(duree.days/7,14)
	def nbMois(self):
		if not self.dateDebut or not self.dateFin:
			return 0
		duree=self.duree()
		return duree.days/30.5
	def congesPayes(self):
		mois=self.nbMois()
		return mois*2.5
	def dif(self):
		premierJanvier=date(datetime.today().year,1,1)
		if self.dateDebut:
			return (premierJanvier-self.dateDebut).days/365*20

class HeurePlanifiee(models.Model):
	employe=models.ForeignKey(Individu)
	jour=models.DateField()
	heureDebut=models.TimeField(blank=True,null=True)
	heureFin=models.TimeField(blank=True,null=True)
	tempsTravaille=models.IntegerField(blank=True,null=True) # en minutes
	nbRepasPris=models.SmallIntegerField(default=0)
	absence=models.BooleanField(default=False)
	commentaire = models.CharField(max_length=200,blank=True)

	def __str__(self):
		return str(self.employe)+" "+str(self.jour)
	
		

class Personne(models.Model):
	nom = models.CharField(max_length=200,unique=True)
	heureNormaleDebutTravailMatin=models.TimeField('heure habituelle de debut le matin',blank=True,null=True)
	heureNormaleDebutTravailAprem=models.TimeField('heure habituelle de debut l\'aprem',blank=True,null=True)
	nbHeuresParSemaine=models.PositiveIntegerField('nombre d\'heures par semaine',blank=True,null=True)
	actif= models.BooleanField(default=True)
	def __str__(self):
		return self.nom
	

class Plage(models.Model):
	heureDebut = models.DateTimeField('heure debut service',blank=True,null=True)
	heureFin = models.DateTimeField('heure fin service',blank=True,null=True)
	personne = models.ForeignKey(Individu)
	commentaire = models.CharField(max_length=200,blank=True)
		
	def __str__(self):
		jour = ""
		deb="non specifie"
		fin="non specifie"
		if self.heureDebut:
			jour=str(self.heureDebut.day)+"/"+str(self.heureDebut.month)
			deb=self.formatNum(self.heureDebut.hour)+":"+self.formatNum(self.heureDebut.minute)
		
		if self.heureFin:
			jour=str(self.heureFin.day)+"/"+str(self.heureFin.month)
			fin=self.formatNum(self.heureFin.hour)+":"+self.formatNum(self.heureFin.minute)

		return self.personne.nom+" le "+jour+" de "+deb+" a "+fin

	def formatNum(self,num):
	    if(num<10):
		    return "0"+str(num)
	    else:
		    return str(num)


