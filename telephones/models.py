from django.db import models


class Contact(models.Model):
    nomTags = models.CharField(max_length=200)
    numero = models.CharField(max_length=200)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.nomTags + " : " + self.numero
