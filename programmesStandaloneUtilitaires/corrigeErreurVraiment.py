from . import configureEnvironnement
import os
from . import preferences
from .seguinus.easyPoS.models import Facture,DonneesEntreprise,Paiement,MoyenPaiement,PortionTVA,Arrhe,Produit,Tva,Famille,Categorie,RemiseCheque,LigneFacture,LogFacture,PreparationFacture

fs=Facture.objects.filter(etat="V").filter(numero__isnull=True).order_by("dateVente")

de=DonneesEntreprise.objects.get(pk=1)
print(de.numeroFactureCourante)
k=len(fs)
for i in range(len(fs)):
	f=fs[i]
	print(f, de.numeroFactureCourante-k+i)
