#!/usr/bin/python3
# coding: utf-8

import configureEnvironnement
configureEnvironnement.setup()

import django
django.setup()

from chambres.models import Tache,Entite,TourOperateur,Client,Reservation
from datetime import date,datetime,timedelta



def ajouteAllotementTousLesJours(dateDeb,dateFin,tourOp):
    for i in range(0,(dateFin-dateDeb).days+1):
        j=dateDeb+timedelta(i)
        c=Client(nom="allotement "+tourOp.nom)
        c.tourOperateur=tourOp
        c.save()
        r=Reservation(dateArrivee=j,dateDepart=j+timedelta(1),client=c,chambres=2)
        r.save()


inn=TourOperateur.objects.get(nom="Inn Travel")
print(inn)
#	ajouteAllotementTousLesJours(dateDeb,dateFin,inn) #rajoute des allotements sur toute la periode demandee DANGER
#ajouteAllotementTousLesJours(date(2017,4,1),date(2017,7,10),inn) #rajoute des allotements
#ajouteAllotementTousLesJours(date(2017,9,1),date(2017,11,1),inn) #rajoute des allotements
