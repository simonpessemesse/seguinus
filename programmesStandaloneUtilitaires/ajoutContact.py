# coding: utf-8
import configureEnvironnement


def isDebutDeNumero(ab):
	if ab[0]=="0":
		if ab[1].isdigit():
			return True
	return False
res=input("Entrez Le contact ")
from telephones.models import Contact
while len(res)>5:
	nom=""
	while not isDebutDeNumero(res[0:2]):
		nom=nom+res[:1]
		res=res[1:]
	num=res
	r=Contact(nomTags=nom,numero=num)
	r.save()

	res=input("Entrez le contact:  ")
