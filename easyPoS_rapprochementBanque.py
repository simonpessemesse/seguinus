#!/usr/bin/python3
# coding: utf-8
from decimal import *
import configureEnvironnement

import django

django.setup()

from datetime import date, timedelta, time, datetime
from chambres.models import Tache, Entite
from restaurant.models import Fournisseur, Fourniture
from easyPoS.models import Facture, Paiement
from datetime import date

import sys

mois = 5
if len(sys.argv) > 1:
    mois = int(sys.argv[1])


class JP():
    pass


cbs = Paiement.objects.filter(date__year=date.today().year).filter(date__month=mois).filter(moyenPaiement=2)
TParJour = {}
for c in cbs:
    if (c.facture and c.facture.etat == 'V') or (c.arrhe):
        jour = date(c.date.year, c.date.month, c.date.day)
        if jour in TParJour:
            TParJour[jour].paiements.append(c)
        else:
            tpj = JP()
            tpj.date = jour
            tpj.paiements = [c]
            TParJour[jour] = tpj
for k, v in TParJour.items():
    #	print(k,v)
    total = 0
    for t in v.paiements:
        total += t.montant
    # print(t)
    v.total = total

# for k,v in TParJour.items():
#	print(k,v.total)

import re

debPath = "/home/auberge/seguinus/"
f = open(debPath + "banque.txt", 'r')
banqueParJour = {}
for line in f:
    m = re.search("(\d+)/(\d+)/(\d+)\D+([\d ]+),(\d+)", line)
    if m:
        jour = date(int("20" + m.group(3)), int(m.group(2)), int(m.group(1)))
        jour = jour - timedelta(1)
        total = Decimal(m.group(4).replace(" ", "") + '.' + m.group(5))
        j = JP()
        j.date = jour
        j.total = total
        banqueParJour[jour] = j


def trouveProb(banque, easy):
    tBanque = len(banque)
    tEasy = len(easy)
    #	print(tBanque)
    iBanque = iEasy = 0
    while (iBanque < tBanque - 1 and iEasy < tEasy - 1):
        #		print(iBanque,iEasy)
        while (banque[iBanque] == easy[iEasy]):
            if iBanque < tBanque - 1 and iEasy < tEasy - 1:
                iBanque += 1
                iEasy += 1
            else:
                break
        while (banque[iBanque] != easy[iEasy]):
            if banque[iBanque] < easy[iEasy]:
                print("dans banque devrait etre present dans la caisse", banque[iBanque])
                if iBanque < tBanque - 1:
                    iBanque += 1
                else:
                    break
            else:
                print("dans le prog mais inconnu de la banque", easy[iEasy])
                if iEasy < tEasy - 1:
                    iEasy += 1
                else:
                    break
    while (iBanque < tBanque - 1):
        print("dans banque devrait etre present dans la caisse", banque[iBanque])
        iBanque += 1
    while (iEasy < tEasy - 1):
        print("dans le prog mais inconnu de la banque", easy[iEasy])
        iEasy += 1


def vieuxTrouveProbleme(easy, banque):
    ASupprimerDeEasy = []
    for ps in easy.paiements:
        ASupprimerDeBanque = False
        if ps.montant in banque.paiements:
            #			print(ps.montant,"dKDK")
            ASupprimerDeEasy.append(ps)
            ASupprimerDeBanque = True
        if ASupprimerDeBanque:
            banque.paiements.remove(ps.montant)
    for i in ASupprimerDeEasy:
        easy.paiements.remove(i)

    for b in easy.paiements:
        print(b.montant, " n'est pas a sa place dans la caisse du " + str(easy.date))
    for b in banque.paiements:
        print(b, " DANS BANQUE le " + str(banque.date))


def ceQuiVaPas(easy, banque):
    import time
    #	a=time.time()
    #	bank=sorted([float(r) for r in banque.paiements])
    #	izi=sorted([float(r.montant) for r in easy.paiements])
    #	trouveProb(bank,izi)
    #	b=time.time()
    vieuxTrouveProbleme(easy, banque)


#	c=time.time()
#	print(b-a)
#	print(c-b)

for j in sorted(banqueParJour.keys()):
    if j in TParJour:
        if TParJour[j].total == banqueParJour[j].total:
            pass
            print(j, banqueParJour[j].total, " OK")
        else:
            fic = str(j)
            import os.path

            if os.path.isfile(debPath + fic):
                print("\nJOUR: ", str(j))
                banqueParJour[j].paiements = []
                f = open(debPath + fic, 'r')
                for line in f:
                    m = re.search("\d+/\d+/\d+\D+([\d ]+),(\d+)", line)
                    total = Decimal(m.group(1).replace(" ", "") + '.' + m.group(2))
                    banqueParJour[j].paiements.append(total)
                ceQuiVaPas(TParJour[j], banqueParJour[j])
            else:
                print(j, " deconne il faut recup le releve de ", banqueParJour[j].total)
