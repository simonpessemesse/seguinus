# coding: utf-8

import configureEnvironnement
configureEnvironnement.setup()

from easyPoS.models import PreparationFacture

p = PreparationFacture(resaId=-1)
p.save()
