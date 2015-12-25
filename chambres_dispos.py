# coding: utf-8
import configureEnvironnement
import django
django.setup()

from datetime import datetime,date,timedelta
from chambres.models import Reservation,Client
from chambres.views import OneDayStats

def beauJour(j):
	return str(j.day)+"/"+str(j.month)+"/"+str(j.year)

def resa(jour,doucheSeulement=False):
	c=Client(nom="Chemins des suds")
	if doucheSeulement:
		c.divers="(d) ok"
	c.save()
	r=Reservation(client=c,dateArrivee=jour,dateDepart=jour+timedelta(1),chambres=8)
	r.save()
	return r

def rep(jour):
	o=OneDayStats(jour)
#	print jour,o.nbAll
	if o.nbAll<21:
		return beauJour(jour)+" nous avons 3 chambres"
	else:
		return ""

deb=date(2014,9,1)
fin=date(2014,11,16)
txtFinal=""
resas=[]
for i in range((fin-deb).days):
	j=deb+timedelta(i)
	txt=rep(j)
	txtFinal+=txt+"\n"

print(" ") 
print(" ") 
print(" ") 
print(" ") 
print(txtFinal)
	

