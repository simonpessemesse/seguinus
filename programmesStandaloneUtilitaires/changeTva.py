from . import configureEnvironnement
from datetime import datetime
import os
from . import preferences
from .seguinus.easyPoS.models import Facture, DonneesEntreprise, Paiement, MoyenPaiement, PortionTVA, Arrhe, Produit, \
    Tva, Famille, Categorie, RemiseCheque, LigneFacture, LogFacture, PreparationFacture

ls = LigneFacture.objects.filter(tauxTvaFinal__isnull=True)
for l in ls:
    if l.produit:
        print(l, l.id)
        l.tauxTvaFinal = l.produit.tva.taux
        l.nomProduitFinal = l.produit.nom
        l.save()

tva = Tva.objects.filter(taux="5.5")
for t in tva:
    print("on change le taux de tva")
    t.taux = 7
    t.save()


def val(fact):
    donnees = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
    fact.numero = donnees.numeroFactureCourante
    donnees.numeroFactureCourante += 1
    donnees.save()
    fact.etat = 'V'
    fact.dateVente = datetime.today()
    fact.save()


fs = Facture.objects.filter(dateVente__year=2012).filter(etat='V')
for f in fs:
    fa = f.creeAvoir(aZero=True)
    val(fa)
