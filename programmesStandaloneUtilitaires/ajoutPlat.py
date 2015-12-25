# coding: utf-8


from . import configureEnvironnement

from .seguinus.restaurant.models import Fourniture,Fournisseur,Plat,Menu
fs=Plat.FONCTION
for f,g in fs:
	print(f,")  "+g)
fonction=input("Entrez le type:  ")
print(("Choisi: "+fonction))

res=input("Entrez le plat:  ")
while len(res)>2:
	fourN=Plat(fonction=fonction,nom=res)
	fourN.save()
	res=input("Entrez Le plat:  ")
