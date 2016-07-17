# coding: utf-8
import configureEnvironnement
configureEnvironnement.setup()

import django

django.setup()

from datetime import datetime, date, timedelta
from chambres.models import Reservation, Client
from chambres.views import OneDayStats


def beauJour(j):
    return str(j.day) + "/" + str(j.month) + "/" + str(j.year)


def resa(jour, doucheSeulement=False):
    c = Client(nom="Chemins des suds")
    if doucheSeulement:
        c.divers = "(d) ok"
    c.save()
    r = Reservation(client=c, dateArrivee=jour, dateDepart=jour + timedelta(1), chambres=8)
    r.save()
    return r


def rep(jour):
    o = OneDayStats(jour)
    print(jour, o.nbAll)
    if o.nbAll >= 25:
        return beauJour(jour) + " PAS OK"
    elif o.nbAll < 18 and jour.month not in [7, 8]:
        resa(jour)
        return beauJour(jour) + " c'est bon"
    else:
        res = input("SI OK ENTREE SINON..  ")
        if res:
            if res == "d":
                print("(d)")
                resa(jour, True)
                return beauJour(jour) + " c'est bon DOUCHE SEULEMENT"
            else:
                print("PAS OK")
                return beauJour(jour) + " PAS OK"
        else:
            print("ok")
            resa(jour)
            return beauJour(jour) + " c'est bon"


deb = date(2015, 3, 29)
fin = date(2015, 11, 16)
txtFinal = ""
resas = []
for i in range((fin - deb).days // 7):
    j = deb + timedelta(i * 7)
    j2 = j + timedelta(4)
    txt = rep(j)
    txtFinal += txt + "\n"
    txt2 = rep(j2)
    txtFinal += txt2 + "\n"

print(" ")
print(" ")
print(" ")
print(" ")
print(txtFinal)
