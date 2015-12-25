# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collectage', '0002_auto_20141209_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrat',
            name='typeDuContrat',
            field=models.CharField(max_length=1, choices=[('S', 'Saisonnier'), ('P', 'Saisonnier Temps Partiel'), ('E', 'Extra'), ('I', 'Indetermine'), ('D', 'Determine'), ('X', 'Determine Temps Partiel'), ('A', 'Avenant')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employe',
            name='sexe',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[('M', 'Masculin'), ('F', 'Feminin')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='individu',
            name='denomination',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[('M', 'Monsieur'), ('L', 'Mademoiselle'), ('A', 'Madame')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='individu',
            name='sexe',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[('M', 'Masculin'), ('F', 'Feminin')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='individu',
            name='situationDeFamille',
            field=models.CharField(blank=True, max_length=1, choices=[('C', 'Celibataire'), ('M', 'Marie')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personne',
            name='heureNormaleDebutTravailAprem',
            field=models.TimeField(null=True, verbose_name="heure habituelle de debut l'aprem", blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personne',
            name='heureNormaleDebutTravailMatin',
            field=models.TimeField(null=True, verbose_name='heure habituelle de debut le matin', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personne',
            name='nbHeuresParSemaine',
            field=models.PositiveIntegerField(null=True, verbose_name="nombre d'heures par semaine", blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plage',
            name='heureDebut',
            field=models.DateTimeField(null=True, verbose_name='heure debut service', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plage',
            name='heureFin',
            field=models.DateTimeField(null=True, verbose_name='heure fin service', blank=True),
            preserve_default=True,
        ),
    ]
