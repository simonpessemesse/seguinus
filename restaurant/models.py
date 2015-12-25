from django.db import models
from telephones.models import Contact
from chambres.models import Client

class ResaResto(models.Model):
	nom = models.CharField(max_length=500,blank=True)
	reservationEcrasee=models.ForeignKey(Client,blank=True,null=True)
	date=models.DateField()
	nbEnfants=models.PositiveSmallIntegerField(default=0)
	nbNouveaux=models.PositiveSmallIntegerField(default=0)
	nbAnciens=models.PositiveSmallIntegerField(default=0)
	nbPassagers=models.PositiveSmallIntegerField(default=0)
	nbPiquesNiques=models.PositiveSmallIntegerField(default=0)
	mangentPas=models.BooleanField(default=False)
	estLeMidi=models.BooleanField(default=False)
	creation=models.DateTimeField(auto_now_add=True)
	modification=models.DateTimeField(auto_now=True)
	def __str__(self):
		deb=""
		if self.nom != "":
			deb=str(self.nom)
		if self.reservationEcrasee:
			deb+=str(self.reservationEcrasee.nom)+" "
		fin="  "
		if self.nbEnfants:
			fin+=str(self.nbEnfants)+" enfants "
		if self.nbNouveaux:
			fin+=str(self.nbNouveaux)+" nvx "
		if  self.nbAnciens: 
			fin+=str(self.nbAnciens)+" anc "
		if self.nbPassagers: 
			fin+=str(self.nbPassagers)+" pass "
		if   self.nbPiquesNiques:
			fin+=str(self.nbPiquesNiques)+" picnic "
		if self.mangentPas:
			fin+="MANGENT PAS"

		return deb+ "le "+str(self.date)+fin
	def nomJoli(self):
		if self.nom:
			return self.nom
		if self.reservationEcrasee:
			return self.reservationEcrasee.nom
		else:
			return "NOM INCONNU"

class Resa(models.Model):
	nom = models.CharField(max_length=500)
	nb = models.PositiveSmallIntegerField()
	nbEnfants = models.PositiveSmallIntegerField()
	jour = models.DateField()
	def __str__(self):
		return str(self.nb)+"("+str(self.nbEnfants)+") p "+self.nom+" le "+str(self.jour)

class Fournisseur(models.Model):
	nom = models.CharField(max_length=500)
	adresse = models.CharField(max_length=500,blank=True)
	telephone = models.CharField(max_length=500,blank=True)
	contacts=models.ManyToManyField(Contact,blank=True,null=True)
	def __str__(self):
		return self.nom

class Fourniture(models.Model):
	nom = models.CharField(max_length=500)
	fournisseur=models.ForeignKey(Fournisseur)
	prix=models.CharField(max_length=500,blank=True)
	note=models.FloatField()
	dateDebut = models.DateField(blank=True,null=True)
	dateFin = models.DateField(blank=True,null=True)
	def __str__(self):
		return self.nom

class Plat(models.Model):
	FONCTION = (
        ('E', 'Entree'),
        ('V', 'Viande'),
        ('F', 'Feculent'),
        ('L', 'Legume'),
        ('FL', 'Feculent Legume'),
        ('D', 'Dessert'),
        ('M', 'Midi'),
    )
	nom=models.CharField(max_length=500)
	titreIngredientPrincipal=models.CharField(max_length=500,null=True,blank=True)
	quantiteRequiseParPersonne=models.FloatField(null=True,blank=True)
	difficulte=models.FloatField(null=True,blank=True)
	fourniture=models.ForeignKey(Fourniture,null=True,blank=True)
	tempsDePreparation=models.FloatField(null=True,blank=True)
	fonction=models.CharField(max_length=2,choices=FONCTION)
	def __str__(self):
		return self.nom

class Menu(models.Model):
	jour=models.DateField()
	midi=models.ManyToManyField(Plat,blank=True,related_name="menu_midi")
	entree=models.ManyToManyField(Plat,blank=True,related_name="menu_entree")
	plat=models.ManyToManyField(Plat,blank=True,related_name="menu_plat")
	dessert=models.ManyToManyField(Plat,blank=True,related_name="menu_dessert")
	def __str__(self):
		return str(self.jour)

