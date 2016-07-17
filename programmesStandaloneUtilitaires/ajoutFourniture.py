# coding: utf-8
import configureEnvironnement

from restaurant.models import Fourniture, Fournisseur

fs = Fournisseur.objects.all()
for f in fs:
    print(f.id, ")  " + f.nom)
res = input("Entrez le num fournisseur:  ")
idee = int(res)
print(idee)
f = Fournisseur.objects.get(id=idee)
print(("Choisi: " + f.nom))

res = input("Entrez le prod:  ")
while len(res) > 2:
    fourN = Fourniture(nom=res, note=15, fournisseur=f)
    fourN.save()
    res = input("Entrez Le prod:  ")
