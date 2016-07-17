# coding: utf-8
import configureEnvironnement

first = input("Quelle date? (rien==aujourd'hui)  ")

from datetime import date, timedelta


def getDate(prems):
    if prems.isdigit():
        try:
            jour = int(prems[0:2])
            mois = int(prems[2:4])
            result = date(date.today().year, mois, jour)
        except:
            return False, None
        return True, result
    return False, None


if first == "":
    res = True
    d = date.today()
else:
    prems = first[0:4]
    res, d = getDate(prems)
while not res:
    first = input("Veuillez rentrer la date sous la forme ddmm\nQuelle date?   ")
    prems = first[0:4]
    res, d = getDate(prems)

jou = d

res = input("Entrez La resa:  ")
from restaurant.models import Resa

while len(res) > 3:
    nb = "0"
    while res[:1].isdigit():
        nb = nb + res[:1]
        res = res[1:]
    nbEnfants = "0"
    if (res[:1] == '('):
        res = res[1:]
        #	print "parent"
        while res[:1].isdigit():
            nbEnfants = nbEnfants + res[:1]
            res = res[1:]
        #		print "nbEnfants",nbEnfants
        if res[:1] == ')':
            res = res[1:]
    nom = res
    #	print "nb",nb
    #	print "res",res
    #	print "nbe",nbEnfants
    r = Resa(nom=nom, jour=jou, nb=int(nb), nbEnfants=int(nbEnfants))
    r.save()

    res = input("Entrez La resa:  ")
