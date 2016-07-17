# coding: utf-8
import configureEnvironnement
configureEnvironnement.setup()


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if not s1:
        return len(s2)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


nomJour = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
nomMois = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre",
           "Decembre"]

from datetime import datetime, date, timedelta
from chambres.models import Reservation, Client


def forDate(deb):
    return nomJour[deb.weekday()] + " " + str(deb.day) + " " + nomMois[deb.month - 1]


def readNumberInBeginning(ss):
    c = ss[0:1]
    if c.isdigit():
        number = int(c)
        ss = ss[1:]
        c = ss[0:1]
    else:
        raise
    while (c.isdigit()):
        number *= 10
        number += int(c)
        ss = ss[1:]
        c = ss[0:1]
    return number, ss


deb = datetime.today()
fin = datetime.today() + timedelta(1)

while True:
    res = input("deb: " + forDate(deb) + " au " + forDate(fin) + " : ")
    if res[0:1] == "+":
        res = res[1:]
        number, res = readNumberInBeginning(res)
        deb += timedelta(number)
        fin += timedelta(number)
    elif res[0:1] == "-":
        res = res[1:]
        number, res = readNumberInBeginning(res)
        deb -= timedelta(number)
        fin -= timedelta(number)
    elif res[0:2] == "f+":
        res = res[2:]
        number, res = readNumberInBeginning(res)
        fin += timedelta(number)
    elif res[0:2] == "f-":
        res = res[2:]
        number, res = readNumberInBeginning(res)
        fin -= timedelta(number)
    elif res[0:2] == "d+":
        res = res[2:]
        number, res = readNumberInBeginning(res)
        deb += timedelta(number)
    elif res[0:2] == "d-":
        res = res[2:]
        number, res = readNumberInBeginning(res)
        deb -= timedelta(number)
    else:

        print(("deb: " + forDate(deb) + " au " + forDate(fin) + " : "))

        veille = deb - timedelta(1)
        resasVeille = Reservation.objects.filter(dateArrivee__lte=veille).filter(dateDepart__gt=veille)
        resasAuj = Reservation.objects.filter(dateArrivee__lte=deb).filter(dateDepart__gt=deb)
        resasVeille = [r for r in resasVeille if r not in resasAuj]

        tab = []
        for r in resasVeille:
            if r.client.nom.lower().startswith(res.lower()):
                tab.append([0, r])
            tab.append([levenshtein(res, r.client.nom), r])
        tab.sort(cmp=lambda a, b: a[0] - b[0])
        tab = [[t[0], t[1]] for t in tab if t[0] < 3]
        for i in range(len(tab)):
            print(str(i) + ") :" + str(tab[i][0]) + " : " + tab[i][1].client.nom)

        if res != "":
            if tab:
                go = input("premier OK?")
                if go == "":
                    ind = 0
                elif go[0:1].isdigit():
                    ind = int(go[0:1])
                else:
                    res = go
                    ind = 1000
                if ind < len(tab):
                    tab[ind][1].dateDepart = fin
                    tab[ind][1].save()
                else:
                    tab = []

            if not tab:
                re = input("pas trouve... ajouter " + res + " ???")
                if re.lower().startswith("y"):
                    c = Client(nom=res)
                    c.save()
                    r = Reservation(dateArrivee=deb, dateDepart=fin, chambres=1, client=c)
                    r.save()

fs = Reservation.objects.all()
for f in fs:
    print(f.id, ")  " + f.client.nom)
res = input("Entrez le num fournisseur:  ")
idee = int(res)
f = Fournisseur.objects.get(id=idee)
print(("Choisi: " + f.nom))

res = input("Entrez le prod:  ")
while len(res) > 2:
    fourN = Fourniture(nom=res, note=15, fournisseur=f)
    fourN.save()
    res = input("Entrez Le prod:  ")
