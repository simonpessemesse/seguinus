#!/usr/bin/python3
# coding: utf-8

import configureEnvironnement
configureEnvironnement.setup()

import django

django.setup()

first = input("Quelle tache?   ")

from datetime import date, timedelta, time, datetime

priorite = 'M'
jour = date.today()
if first.startswith('B'):
    priorite = 'B'
    first = first[1:]
elif first.startswith('H'):
    priorite = 'H'
    first = first[1:]
while first.startswith('D'):
    jour = jour + timedelta(1)
    first = first[1:]
if first.startswith('R'):
    rappel = None
    first = first[1:]
else:
    rappel = (datetime.now() + timedelta(0, 1200)).time()

from chambres.models import Tache, Entite
from restaurant.models import Fournisseur, Fourniture
from datetime import date

first.strip()
prem = first.rsplit()[0]
ents = Entite.objects.filter(nom__istartswith=prem)
fourn = Fournisseur.objects.filter(nom__istartswith=prem)
if len(fourn) == 1:
    print("diable un fournisseur")
    print(("on va le mettre chez le fournisseur: " + str(fourn[0])))
    r = input("appuyer sur entree pour ok, n sinon?")
    if not r:
        f = Fourniture(nom=first, fournisseur=fourn[0], note=1000, dateDebut=date.today())
        f.save()
        exit()

t = Tache(description=first, date=jour, priorite=priorite, rappel=rappel)
t.save()
if len(ents) == 1:
    print(("on va le mettre dans l'entite: " + str(ents[0])))
    r = input("appuyer sur entree pour ok, n sinon?")
    if not r:
        t.entite.add(ents[0])
        t.save()
# os.system("..\..\python26\python.exe auberge.pyw")
