import logging
import preferences

logging.basicConfig(level=preferences.LOGGING_LEVEL)
from django.db import models
from django.forms.models import modelformset_factory
from django.forms import ModelForm
from datetime import datetime, date, timedelta
from django.core.signals import request_finished
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
nomMois = ["zero", "janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre",
           "novembre", "decembre"]


def joliePeriode(dateArrivee, dateDepart, avecJours=False):
    if dateArrivee.month == dateDepart.month:
        if avecJours:
            return jours[dateArrivee.weekday()] + " " + str(dateArrivee.day) + " au " + jours[
                dateDepart.weekday()] + " " + str(dateDepart.day) + " " + nomMois[dateDepart.month]
        else:
            return str(dateArrivee.day) + " au " + str(dateDepart.day) + " " + nomMois[dateDepart.month]
    else:
        if avecJours:
            return jours[dateArrivee.weekday()] + " " + str(dateArrivee.day) + " " + nomMois[
                dateArrivee.month] + " au " + jours[dateDepart.weekday()] + " " + str(dateDepart.day) + " " + nomMois[
                       dateDepart.month]
        else:
            return str(dateArrivee.day) + " " + nomMois[dateArrivee.month] + " au " + str(dateDepart.day) + " " + \
                   nomMois[dateDepart.month]


class Chambre(models.Model):
    nom = models.CharField(max_length=50)
    petitsLits = models.IntegerField()
    grandsLits = models.IntegerField()
    avecWC = models.BooleanField(default=False)
    note = models.FloatField()

    def __str__(self):
        wc = ""
        if self.avecWC is True:
            wc = "WC"
        return self.nom + "  " + str(self.grandsLits) + " gd + " + str(self.petitsLits) + " petits  " + wc + " " + str(
            self.note)

    def capacite(self):
        return self.petitsLits + self.grandsLits * 2

    def nbLits(self):
        return self.petitsLits + self.grandsLits

    def description(self):
        desc = ""
        if self.grandsLits > 0:
            if self.grandsLits == 1:
                desc += str(self.grandsLits) + " lit double "
            else:
                desc += str(self.grandsLits) + " lits doubles "
        if self.petitsLits > 0:
            if self.petitsLits == 1:
                desc += str(self.petitsLits) + " lit simple "
            else:
                desc += str(self.petitsLits) + " lits simples "
        if not self.avecWC:
            desc += " sans WC "
        return desc


class Souci(models.Model):
    description = models.TextField()
    repare = models.BooleanField(default=False)
    date = models.DateField()
    chambre = models.ForeignKey(Chambre)
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chambre.nom + " : " + self.description


class TourOperateur(models.Model):
    nom = models.CharField(max_length=500)
    commentaire = models.TextField(blank=True)
    actif = models.BooleanField(default=True)
    nbJoursAnnulationAllotement = models.IntegerField(blank=True, null=True)
    prixParPersonne = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    gratuiteAccompagnateurSiGroupe = models.BooleanField(default=False)
    seuilGroupe = models.IntegerField(blank=True, null=True)
    picnicSiGroupe = models.BooleanField(default=False)
    tarifReduit = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

    def nettoieAllotements(self):
        auj = date.today()
        aNettoyer = Reservation.objects.filter(client__tourOperateur=self).filter(
            client__nom="allotement " + self.nom).filter(
            dateArrivee__lt=auj + timedelta(self.nbJoursAnnulationAllotement))
        for resa in aNettoyer:
            resa.delete()


class Client(models.Model):
    nom = models.CharField(max_length=5000)
    protege = models.BooleanField(default=False)
    surbooking = models.BooleanField(default=False)
    telephone = models.CharField(max_length=15, blank=True)
    divers = models.TextField(blank=True)
    arrhes = models.BooleanField(default=False)
    tourOperateur = models.ForeignKey(TourOperateur, blank=True, null=True)
    optionJusquau = models.DateField(null=True, blank=True)
    aConfiance = models.BooleanField(default=False)
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        st = "   "
        for r in self.reservation_set.all():
            st += str(r) + " "
        if self.tourOperateur:
            st += "TOUROP: " + str(self.tourOperateur)
        return self.nom + st

    def diversGrand(self):
        if "\n" in self.divers:
            return True
        else:
            return False

    def arrhesVersees(self):
        if self.tourOperateur:
            return True
        oui = False
        for ar in self.arrhe_set.all():
            if ar.montantChequeNonEncaisse or len(ar.paiement_set.all()) > 0:
                oui = True
        return oui

    def asPicnicDansLeNom(self):
        nom = (self.nom.lower())
        if "picnic" in nom or "pn" in nom or "pique nique" in nom or "piquenique" in nom or "piqnic" in nom or "piq niq" in nom:
            return True
        else:
            return False


class Entite(models.Model):
    nom = models.CharField(max_length=500)
    cacherPremierPlan = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class Tache(models.Model):
    PRIORITE = (
        ('B', 'Basse'),
        ('M', 'Moyenne'),
        ('H', 'Haute'),
    )
    description = models.TextField()
    date = models.DateField(null=True, default=date.today)
    expiration = models.DateField(null=True, blank=True)
    entite = models.ManyToManyField(Entite, blank=True)
    rappel = models.TimeField(null=True, blank=True)
    chaqueLundi = models.BooleanField(default=False)
    chaqueMardi = models.BooleanField(default=False)
    chaqueMercredi = models.BooleanField(default=False)
    chaqueJeudi = models.BooleanField(default=False)
    chaqueVendredi = models.BooleanField(default=False)
    chaqueSamedi = models.BooleanField(default=False)
    chaqueDimanche = models.BooleanField(default=False)
    executee = models.BooleanField(default=False)
    priorite = models.CharField(max_length=2, choices=PRIORITE, default='M')
    tachePapa = models.ForeignKey('self', blank=True, null=True)
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description + str(self.executee)

    def multiligne(self):
        return self.description.count("\n") > 0

    def estPeriodique(self):
        if self.chaqueLundi or self.chaqueMardi or self.chaqueMercredi or self.chaqueJeudi or self.chaqueVendredi or self.chaqueSamedi or self.chaqueDimanche:
            return True
        return False


# class ExecutionTacheReguliere(models.Model):
#	tache=models.ForeignKey(Tache)
#	date=models.DateField(null=True,default=date.today)

class TacheLog(models.Model):
    tache = models.ForeignKey(Tache)
    creation = models.DateTimeField(auto_now_add=True)


def joliNb(nb, st):
    if nb > 0:
        if not st:
            return str(nb) + " ch \n"
        else:
            return str(nb) + "ch x " + st + "\n"
    else:
        return ""


def existeChambreCapacite(chs, capacite, litsDifferents=False):
    toDel = None
    if litsDifferents and capacite == 2:
        for ch in chs:
            if ch.petitsLits == 2 and ch.grandsLits == 0:
                toDel = ch
    if not toDel:
        for ch in chs:
            if not litsDifferents:
                if ch.capacite() >= capacite:
                    toDel = ch
            else:
                if ch.nbLits() >= capacite:
                    toDel = ch
    if not toDel:
        return False, chs
    chs.remove(toDel)
    return True, chs


class Reservation(models.Model):
    client = models.ForeignKey(Client)
    dateArrivee = models.DateField()
    dateDepart = models.DateField()
    chambres = models.IntegerField(default=0)
    chambresSingle = models.IntegerField(default=0)
    chambresDoubles = models.IntegerField(default=0)
    chambresTwin = models.IntegerField(default=0)
    chambresTriples = models.IntegerField(default=0)
    chambresQuadruples = models.IntegerField(default=0)
    chambresQuintuples = models.IntegerField(default=0)
    placesDortoir = models.IntegerField(default=0)
    chambresAssignees = models.ManyToManyField(Chambre, blank=True)
    arrives = models.BooleanField(default=False)
    partis = models.BooleanField(default=False)
    aEtePrepare = models.BooleanField(default=False)
    nbEnfants = models.IntegerField(default=0)
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)

    def visuel(self):
        v = ""
        NBP = self.nbPersonnes() * self.nbNuits()
        for i in range(NBP // 30):
            v += "x" * 30 + "<br>"
        v += "x" * (NBP % 30)

        return v  # +str(NBP)

    def assignationsOk(self):
        chs = list(ch for ch in self.chambresAssignees.all())
        for i in range(self.chambresQuintuples):
            ok, chs = existeChambreCapacite(chs, 5)
            if not ok:
                return False, "Erreur Chambres Quintuples"
        for i in range(self.chambresQuadruples):
            ok, chs = existeChambreCapacite(chs, 4)
            if not ok:
                return False, "Erreur Chambres Quadruples"
        for i in range(self.chambresTriples):
            ok, chs = existeChambreCapacite(chs, 3)
            if not ok:
                return False, "Erreur Chambres Triple"
        for i in range(self.chambresTwin):
            ok, chs = existeChambreCapacite(chs, 2, litsDifferents=True)
            if not ok:
                return False, "Erreur Chambres Twin"
        for i in range(self.chambresDoubles):
            ok, chs = existeChambreCapacite(chs, 2)
            if not ok:
                return False, "Erreur Chambres Doubles"
        return True, "TOUT EST OK"

    def nouvelleResa(self):
        if self.client.creation > datetime(2012, 5, 10, 9, 0, 0):
            return True
        else:
            return False

    def vuePapier(self):
        r = ""
        r += joliNb(self.chambres, "")
        r += joliNb(self.chambresSingle, "1")
        r += joliNb(self.chambresDoubles, "2")
        r += joliNb(self.chambresTwin, "2 lit")
        r += joliNb(self.chambresTriples, "3")
        r += joliNb(self.chambresQuadruples, "4")
        r += joliNb(self.chambresQuintuples, "5")
        if self.placesDortoir:
            r += str(self.placesDortoir) + " dort\n"
        return r

    def __str__(self):
        if self.dateDepart <= self.dateArrivee:
            return "ERRRRRRRRRRRREUR DATE DEPART AVANT ARRIVEE"
        st = ""
        if self.chambres > 0:
            st += str(self.chambres) + " chambres "
        if self.chambresSingle > 0:
            st += str(self.chambresSingle) + " single "
        if self.chambresDoubles > 0:
            st += str(self.chambresDoubles) + " double "
        if self.chambresTwin > 0:
            st += str(self.chambresTwin) + " twin "
        if self.chambresTriples > 0:
            st += str(self.chambresTriples) + " triple "
        if self.chambresQuadruples > 0:
            st += str(self.chambresQuadruples) + " quadruple "
        if self.chambresQuintuples > 0:
            st += str(self.chambresQuintuples) + " quintuples "
        if self.placesDortoir > 0:
            st += str(self.placesDortoir) + " dortoir "

        dates = joliePeriode(self.dateArrivee, self.dateDepart, avecJours=True)

        return dates + " de " + st

    def infoSupplementaire(self):
        supp = ""
        # if self.client.tourOperateur:
        #	supp+="Demander Voucher<br />"
        try:
            for ar in self.client.arrhe_set.all():
                supp += "<br /><b>" + ar.description() + "</b>"
        except:
            logging.error("pas d'application d'arrhes")

        return supp

    def nbCh(self):
        return self.chambres + self.chambresSingle + self.chambresDoubles + self.chambresTwin + self.chambresTriples + self.chambresQuadruples + self.chambresQuintuples

    def resaVide(self):
        return self.nbCh() == 0 and self.placesDortoir == 0

    def nbNuits(self):
        return (self.dateDepart - self.dateArrivee).days

    def chAssignees(self):
        return len(self.chambresAssignees.all())

    def nbPersonnes(self):
        nbPers = 0
        nbPers += (self.chambres * 2)
        nbPers += (self.chambresDoubles * 2)
        nbPers += (self.chambresSingle * 1)
        nbPers += (self.chambresTwin * 2)
        nbPers += (self.chambresTriples * 3)
        nbPers += (self.chambresQuadruples * 4)
        nbPers += (self.chambresQuintuples * 5)
        nbPers += self.placesDortoir
        return nbPers

    def chAAssigner(self):
        result = self.nbCh() - self.chAssignees()
        if result < 0:
            return -1
        return result


class CacheJour(models.Model):
    jour = models.DateField()
    nbCh = models.IntegerField(null=True, blank=True)
    nbDortoir = models.IntegerField(null=True, blank=True)
    nbanc = models.IntegerField(null=True, blank=True)
    nbTotal = models.IntegerField(null=True, blank=True)


class Amour(models.Model):
    date = models.DateField(unique=True)
    nomUnion = models.CharField(max_length=500)
    #	amoureux=models.ManyToManyField(Client)
    mangentPas = models.BooleanField(default=False)
    personnesSupplementaires = models.IntegerField(default=0)
    commentaire = models.TextField(blank=True)
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ('nom', 'divers', 'optionJusquau', 'tourOperateur', 'protege')


class ReservationsForm(ModelForm):
    class Meta:
        model = Reservation
        exclude = ()
