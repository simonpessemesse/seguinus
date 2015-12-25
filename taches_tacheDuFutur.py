#!/usr/bin/python3
# coding: utf-8

import configureEnvironnement

import django
django.setup()

from chambres.models import Tache,Entite
from restaurant.models import Fournisseur,Fourniture
from datetime import date,datetime


tod=datetime.now()
ts=Tache.objects.filter(date__gt=tod)
for t in ts:
	print(t.date,t)

