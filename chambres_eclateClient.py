# coding: utf-8
import configureEnvironnement
configureEnvironnement.setup()
import django

django.setup()

from datetime import datetime, date, timedelta
from chambres.models import Reservation, Client, TourOperateur
from chambres.views import OneDayStats

nomSuivant = input("nouveau Nom?  ")
first = input("Quel Numero?   ")
# first=22146
c = Client.objects.get(id=first)
for r in c.reservation_set.all():
    #	print r
    #	nbCh=ch.nbCh()
    #	nbReel=len(r.chambresAssignees.all())
    #	if nbReel>nbCh:
    #		nbCh=NbReel
    for ch in r.chambresAssignees.all():
        print(ch.nom + " du " + str(r.dateArrivee) + " au " + str(r.dateDepart))
        cc = Client(nom="~" + nomSuivant + " ")
        cc.save()
        rr = Reservation(client=cc, dateArrivee=r.dateArrivee, dateDepart=r.dateDepart, chambres=1)
        rr.save()
        rr.chambresAssignees.add(ch)
        rr.save()
