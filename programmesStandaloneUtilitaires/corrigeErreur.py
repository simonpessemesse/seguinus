from . import configureEnvironnement
import os
from . import preferences
from .easyPoS.models import Facture,DonneesEntreprise,Paiement,MoyenPaiement,PortionTVA,Arrhe,Produit,Tva,Famille,Categorie,RemiseCheque,LigneFacture,LogFacture,PreparationFacture
from .chambres.models import Reservation,Client,TourOperateur

rs=Client.objects.all()
tt=TourOperateur.objects.all()

fs=Facture.objects.all()
for f in fs:
	if f.factureAssociee:
		if f.factureAssociee.id==10459:
			print(f,f.id)

#for c in tt:
#	tou= (c.nom.replace(" ","")).lower()
#	for r in rs:
#		if tou in r.nom.replace(" ","").lower() and not r.tourOperateur:
		#	r.tourOperateur=c
		#	r.save()
		#	print r
#	print c

			
