from .seguinus.easyPoS.models import DonneesEntreprise, LigneFacture, PreparationFacture, Produit, LogFacture
from .seguinus.chambres.models import Client
from .seguinus.chambres.models import Reservation, TourOperateur, CacheJour
from .seguinus.easyPoS.models import Facture
from .seguinus.collectage.models import Employe, Personne
from datetime import datetime, date, timedelta, time
from django.contrib.admin.models import LogEntry
import os

from django.conf import settings


def vacuum_db():
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("VACUUM")
    connection.close()


def vacu():
    print("Vacuuming database...")
    before = os.stat(settings.DATABASE_NAME).st_size
    print("Size before: %s bytes" % before)
    vacuum_db()
    after = os.stat(settings.DATABASE_NAME).st_size
    print("Size after: %s bytes" % after)
    print("Reclaimed: %s bytes" % (before - after))


def delTout(tout):
    tout.delete()


def allege():
    today = date.today()
    delTout(Reservation.objects.filter(dateDepart__lt=today))
    delTout(Facture.objects.filter(etat='C'))
    delTout(LogFacture.objects.all())
    delTout(CacheJour.objects.all())
    delTout(Employe.objects.all())
    delTout(Personne.objects.all())
    delTout(LogEntry.objects.all())
    vacu()
