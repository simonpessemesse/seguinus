from django.db import models

jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

class JourneePensionComplete(models.Model):
    platMidi = models.TextField(blank=True)
    dessertMidi = models.TextField(blank=True)
    entreeSoir = models.TextField(blank=True)
    platSoir = models.TextField(blank=True)
    dessertSoir = models.TextField(blank=True)
    jour = models.DateField('Jour')
    def __str__(self):
	    return jours[self.jour.weekday()]+" "+str(self.jour.day)+"/"+str(self.jour.month)+" pension complete"
    def date(self):
        return jours[self.jour.weekday()]+" "+str(self.jour.day)+"/"+str(self.jour.month)


class Journee(models.Model):
    entree = models.TextField(blank=True)
    plat = models.TextField(blank=True)
    dessert= models.TextField(blank=True)
    jour = models.DateField('Jour')


    def __str__(self):
	    return jours[self.jour.weekday()]+" "+str(self.jour.day)+"/"+str(self.jour.month)+" "+self.entree+" et "+self.plat+" et "+self.dessert
    def date(self):
	    return jours[self.jour.weekday()]+" "+str(self.jour.day)+"/"+str(self.jour.month)

class MatierePremiere(models.Model):
	nom=models.CharField(max_length=50)

class Ingredient(models.Model):
	nom=models.CharField(max_length=50)
	ingredient=models.ForeignKey(MatierePremiere)
	grammesParPersonnee=models.PositiveSmallIntegerField(default=0)
	unitesParPersonne=models.FloatField(default=0)

class Plat(models.Model):
	nom=models.CharField(max_length=50)
	ingredients=models.ManyToManyField(Ingredient)

class Accompagnement(models.Model):
	nom=models.CharField(max_length=50)
	ingredients=models.ManyToManyField(Ingredient)

	


