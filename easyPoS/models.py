from django.db import models
import preferences
from datetime import datetime
from decimal import Decimal
from chambres.models import Reservation,TourOperateur
from chambres.models import Client 

class DonneesEntreprise(models.Model):
    denomination=models.CharField(max_length=1000)
    siret=models.CharField(max_length=1000)
    numeroTva=models.CharField(max_length=1000)
    email=models.CharField(max_length=1000)
    telephone=models.CharField(max_length=1000)
    fax=models.CharField(max_length=1000)
    adresse=models.TextField()
    numeroFactureCourante=models.PositiveIntegerField()
    numeroUrssaf=models.CharField(max_length=1000)
    actif=models.BooleanField(default=True)
    derniereSauvegarde=models.DateTimeField()
    dernierEnvoiCaisses=models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return self.denomination

class PreparationFacture(models.Model):
    resa=models.ForeignKey(Reservation,null=True,blank=True)
    resaId=models.IntegerField(null=True,blank=True)

class Tva(models.Model):
    nom = models.CharField(max_length=1000)
    taux=models.DecimalField(max_digits=10, decimal_places=4)
    creation=models.DateTimeField(auto_now_add=True)
    modification=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.nom)+" a "+str(self.taux)

class Famille(models.Model):
    nom = models.CharField(max_length=1000)
    def __str__(self):
        return self.nom 
    
class RemiseCheque(models.Model):
    commentaire=models.TextField(blank=True)
    date=models.DateTimeField()
    creation=models.DateTimeField(auto_now_add=True)
    modification=models.DateTimeField(auto_now=True)
    

class Categorie(models.Model):
    nom = models.CharField(max_length=1000)
    creation=models.DateTimeField(auto_now_add=True)
    modification=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.nom)


class Produit(models.Model):
    nom = models.CharField(max_length=1000)
    prix=models.DecimalField(max_digits=10, decimal_places=5)
    tva=models.ForeignKey(Tva)
    famille=models.ForeignKey(Famille)
    categories = models.ManyToManyField(Categorie,blank=True)
    actif=models.BooleanField(default=True)
    creation=models.DateTimeField(auto_now_add=True)
    modification=models.DateTimeField(auto_now=True)
    def __str__(self):
        try:
            return str(self.nom)+":"+str(self.prix)+" euros; TVA:"+str(self.tva.taux)
        except:
            return "ERREUR ENCODAGE"
    def prixHT(self):
        return 100*self.prix/(100+self.tva.taux)


class MoyenPaiement(models.Model):
    nom = models.CharField(max_length=1000)
    def __str__(self):
        return str(self.nom)


ETAT = (
    ('B', 'Brouillon'),
    ('V', 'Valide'),
    ('C', 'Cache'),
)
ACTION=( 
        ('S','Suppression'),
        ('A','Ajout'),
        ('U','Mise a jour'),
        )


TYPEFACTURE=(
        ('N','Normale'),
        ('A','Avoir'),
        )


class Facture(models.Model):
    entreprise=models.ForeignKey(DonneesEntreprise)
    description = models.CharField(max_length=1000,blank=True)
    client=models.ForeignKey(Client,null=True,blank=True)
    clientNomFinal= models.CharField(max_length=1000,blank=True)
    clientDiversFinal=models.TextField(blank=True)
    numero=models.PositiveIntegerField(blank=True,null=True)
    factureAssociee=models.ForeignKey('self',null=True,blank=True)
    dateVente=models.DateTimeField(blank=True,null=True)
    dateReglement=models.DateTimeField(blank=True,null=True)
    toujoursVisible=models.BooleanField(default=False)
    etat = models.CharField(max_length=1, choices=ETAT)
    cacheTotalDu=models.DecimalField(max_digits=15,decimal_places=5,null=True,blank=True)
    cacheTotal=models.DecimalField(max_digits=15,decimal_places=5,null=True,blank=True)
    creation=models.DateTimeField(auto_now_add=True)
    def __str__(self):        
        if self.client:
            return self.entreprise.denomination+self.etat+" "+self.client.nom+" du "+str(self.dateVente)
        else:
            return self.etat+" du "+str(self.dateVente)
    def nomJoli(self):
        nom=""
        if self.factureAssociee:
            nom+="Avoir "+str(self.numero)+" de la facture "+str(self.factureAssociee.numero)
        else:
            nom+="Facture "+str(self.numero)
        return nom

    def updateCache(self):
        self.cacheTotalDu=self.totalDu()
        self.cacheTotal=self.total()
        self.save()
    def estFactureHotel(self):
        nombrePersonneParLigne=[(1,[2,9,10,13,107,108,118,119,136,142,143,148,149,169]),(2,[7,8,120,121,134,135,150]),(3,[11,137,157]),(4,[12,138,139,151]),(5,[163])]
        idDesLignesDhotel=[]
        gensParId={}
        for i in nombrePersonneParLigne:
            ids=i[1]
            idDesLignesDhotel.extend(i[1])
            for chaqueId in ids:
                gensParId[chaqueId]=i[0]
#        print(idDesLignesDhotel)
#        print(gensParId)
    #    idDesLignesDhotel=[2,7,8,9,10,11,12,13,134,135,136,137,138,142,118,119,120,121,3,133,143,149,150,151]
        idTaxeSejour=173
        idTaxeSejourMineur=175
        nombreGensDormant=0
        nombreTaxeSejourDansCetteFacture=0
        retour=False
        for l in self.lignefacture_set.all():
            if l.produit:
                if l.produit.id in idDesLignesDhotel:
                #    print(l.produit,l.quantite,gensParId[l.produit.id])
                    nombreGensDormant+=l.quantite*gensParId[l.produit.id]
                    retour=True
                elif l.produit.id==idTaxeSejour or l.produit.id==idTaxeSejourMineur:
                    nombreTaxeSejourDansCetteFacture+=l.quantite
#        print (nombreGensDormant)
        return retour,nombreGensDormant,nombreTaxeSejourDansCetteFacture
    def totalPaye(self):
        somme=0
        for i in self.paiement_set.all():
            somme+=i.montant
        return somme
    def total(self):
        somme=0
        for i in self.lignefacture_set.all():
            if i.produit:
                if i.prixUnitaireFinal or i.prixUnitaireFinal==0:
                    pr=i.prixUnitaireFinal
                else:
                    pr=i.produit.prix
                somme+=i.quantite*pr
        return somme
    def nomClient(self): # a supprimer un jour, ca sert a rien
        if self.clientNomFinal:
            return self.clientNomFinal
        elif(self.client):
            return self.client.nom
        else:
            return ""
    def totalDu(self):
        return self.total()-self.totalPaye()
    def HtTva(self):
        portions=self.portions()

        sommeHT=0
        for i in portions:
            sommeHT+=100*i.TTC/(100+i.taux)

        return sommeHT,self.total()-sommeHT

    def montantHT(self):
        a,b=self.HtTva()
        return a
    def montantTVA(self):
        a,b=self.HtTva()
        return b

    def asDeuxPortions(self):
        if len(self.portions())>1:
            return True
        else:
            return False

    def portions(self):
        dictParTaux={}
        differentes=self.lignefacture_set.all()
        for l in differentes:
            if l.produit:
                if l.tauxTvaFinal in dictParTaux:
                    dictParTaux[l.tauxTvaFinal].append(l)
                else:
                    dictParTaux[l.tauxTvaFinal]=[l]
        lesPortions=[]
        for t,p in dictParTaux.items():
            sommeParTaux=0
            for ligne in p:
                sommeParTaux+=ligne.montant()

            portion=PortionTVA(t,sommeParTaux)
            lesPortions.append(portion)
        return lesPortions

    def creeAvoir(self,aZero=False):
        ent=DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
        f=Facture(entreprise=ent,etat="B",client=self.client)
        f.factureAssociee=self
        f.save()
        for i in self.lignefacture_set.all().order_by("position"):
            if not i.libelle:
                ligne=LigneFacture(produit=i.produit,facture=f,famille=i.famille,prixUnitaireFinal=i.prixUnitaireFinal,nomProduitFinal=i.nomProduitFinal,tauxTvaFinal=i.tauxTvaFinal,position=i.position,quantite=-i.quantite)
                ligne.save()
            else:
                ligne=LigneFacture(position=i.position,facture=f,libelle=i.libelle)
                ligne.save()
        if aZero:
            for i in self.lignefacture_set.all().order_by("position"):
                if not i.libelle:
                    ligne=LigneFacture(produit=i.produit,facture=f,famille=i.produit.famille.nom,prixUnitaireFinal=i.prixUnitaireFinal,nomProduitFinal=i.nomProduitFinal,tauxTvaFinal=i.produit.tva.taux,position=i.position+100,quantite=i.quantite)
                    ligne.save()
        f.save()
        pf=PreparationFacture(resaId=f.id)
        pf.save()
        return f

class RelationReservationFacture(models.Model):
    reservation=models.ForeignKey(Reservation)
    facture=models.ForeignKey(Facture)

class LogFacture(models.Model):
    description = models.CharField(max_length=1000,blank=True)
    facture=models.ForeignKey(Facture)
    moment=models.DateTimeField()
    action = models.CharField(max_length=1, choices=ACTION)
    def __str__(self):
        return self.description+ " le "+self.moment.strftime("%d/%m/%y %H:%M")

class PortionTVA:
    def __init__(self,t,sommeTotale):
        self.taux=t
        self.TTC=sommeTotale
        self.BaseHT=Decimal("%.2f" % float(round(100*sommeTotale/(100+t),2)))
        self.TVA=sommeTotale-self.BaseHT
    #    self.TVA=round(float(Decimal(sommeTotale)*Decimal(t.taux)/100),2)
    def imprime(self):
        return str(self.taux)+" TVA: "+str(self.TVA)


class Arrhe(models.Model):
    nom=models.CharField(max_length=1000)
    client=models.ForeignKey(Client)
    divers=models.TextField(blank=True)
    montantChequeNonEncaisse=models.DecimalField(max_digits=15,decimal_places=5,blank=True,null=True)
    dateArrivee=models.DateField(default=datetime.now)
    date=models.DateTimeField(default=datetime.now)
    estBleu=models.BooleanField(default=False)
#    encaisse=models.BooleanField(default=True)
#    moyenPaiement=models.ForeignKey(MoyenPaiement)
    def __str__(self):
        txt=""
        if self.montantChequeNonEncaisse:
            txt+=" cheque non encaisse de "+str(self.montantChequeNonEncaisse)
        for p in self.paiement_set.all():
            txt+=" paiement: "+str(p)
        return self.client.nom+" : "+txt
    def description(self):
        rep=""
        if self.divers:
            rep+="Description "+self.divers+"<br/ >"
        if self.montantChequeNonEncaisse:
            rep+="Cheque non encaisse de "+str(self.montantChequeNonEncaisse)+" Euros"
        for p in self.paiement_set.all():
            if p.facture:
                rep+="Arrhes ENCAISSEES deja associes a la facture ({0}): {1}".format(p.facture.numero,p)
            else:
                rep+="Arrhes ENCAISSEES:" +str(p)
        return rep
    def encaisseChequeNonEncaisse(self):
        if not self.montantChequeNonEncaisse or self.montantChequeNonEncaisse==0:
            return
        cheque=MoyenPaiement.objects.get(nom="Cheque")
        ent=DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
        paiement=Paiement(entreprise=ent,moyenPaiement=cheque,montant=self.montantChequeNonEncaisse,arrhe=self)
        paiement.date=datetime.now()
        paiement.save()
        self.montantChequeNonEncaisse=None
        self.save()
        return paiement
    def detruitCheque(self):
        if not self.montantChequeNonEncaisse or self.montantChequeNonEncaisse==0:
            return
        if len(self.paiement_set.all())==0:
            self.delete()
        else:
            self.montantChequeNonEncaisse=None
            self.save()




class Paiement(models.Model):
    entreprise=models.ForeignKey(DonneesEntreprise)
    montant=models.DecimalField(max_digits=15, decimal_places=5)
    moyenPaiement=models.ForeignKey(MoyenPaiement)
    numero=models.PositiveIntegerField(blank=True,null=True)
    facture=models.ForeignKey(Facture,blank=True,null=True)
    arrhe=models.ForeignKey(Arrhe,null=True,blank=True)
    valide=models.BooleanField(default=False)
    date=models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.entreprise.denomination+str(self.montant)+" Euros en "+str(self.moyenPaiement)+" le "+str(self.date.strftime("%A %d %B %Y"))

class LigneFacture(models.Model):
    produit=models.ForeignKey(Produit,null=True,blank=True)
    libelle=models.CharField(max_length=5000,blank=True)
    famille=models.CharField(max_length=1000,blank=True)
    nomProduitFinal=models.CharField(max_length=1000,blank=True)
    tauxTvaFinal=models.DecimalField(max_digits=10, decimal_places=4,blank=True,null=True)
    prixUnitaireFinal=models.DecimalField(max_digits=10, decimal_places=5,blank=True,null=True)
    quantite=models.IntegerField(default=1)
    facture=models.ForeignKey(Facture)
    position=models.FloatField()
    def __str__(self):
        return str(self.quantite)+" x "+str(self.produit)
    def montant(self):
        return Decimal(self.prixUnitaireFinal)*self.quantite
    def montantHT(self):
        if self.tauxTvaFinal:
            return 100*self.montant()/(100+self.tauxTvaFinal)
        elif self.produit:
            return 100*self.montant()/(100+self.produit.tva.taux)
        else:
            return 0



