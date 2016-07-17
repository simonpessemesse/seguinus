from django.db import models
from chambres.models import Reservation
from chambres.models import Client
from easyPoS.models import Facture


class Log(models.Model):
    description = models.CharField(max_length=10000, blank=True)

    facture = models.ForeignKey(Facture, null=True, blank=True)
    reservation = models.ForeignKey(Reservation, null=True, blank=True)
    client = models.ForeignKey(Client, null=True, blank=True)

    debutImpact = models.DateField(null=True, blank=True)
    finImpact = models.DateField(null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.description + " le " + self.creation.strftime("%d/%m/%y %H:%M")
