# coding: utf-8
import configureEnvironnement
configureEnvironnement.setup()

import django

django.setup()

from datetime import datetime, date, timedelta
from chambres.models import Reservation, Client
from chambres.views import OneDayStats

rs = Reservation.objects.all()
for r in rs:
    if r.dateArrivee > r.dateDepart:
        print(r, r.id, r.client.id)
