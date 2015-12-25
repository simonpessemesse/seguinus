# coding: utf-8
import configureEnvironnement
import django
django.setup()

nomJour=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
nomMois=["Janvier","Fevrier","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Decembre"]

from datetime import datetime,date,timedelta
from chambres.models import Reservation,Client,TourOperateur
from chambres.views import OneDayStats

def joli(d):
	return nomJour[d.weekday()]+" "+str(d.day)+" "+nomMois[d.month-1]


deb=date(2015,4,15) 
fin=date(2015,5,1)
chambresDispo=12
joursPossible=[0,1,2,3,4,5,6]
dispoTotale=True

nbSem=(fin-deb).days//7+1
for i in range(nbSem):
	for j in joursPossible:
		day=deb+timedelta(i*7+j)
		reserves=OneDayStats(day).chambresReservees
		if dispoTotale:
			print(joli(day)," Chambres dispos: ",25-reserves," places dortoir dispo: ",OneDayStats(day).nbPlacesLibreDortoir)
		elif reserves<24-chambresDispo:
			print (joli(day))

	


