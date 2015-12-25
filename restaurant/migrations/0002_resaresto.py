# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chambres', '0003_auto_20150116_2148'),
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResaResto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=500)),
                ('date', models.DateField()),
                ('nbEnfants', models.PositiveSmallIntegerField()),
                ('nbNouveaux', models.PositiveSmallIntegerField()),
                ('nbAnciens', models.PositiveSmallIntegerField()),
                ('nbPassagers', models.PositiveSmallIntegerField()),
                ('nbPiquesNiques', models.PositiveSmallIntegerField()),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
                ('reservationEcrasee', models.ForeignKey(blank=True, to='chambres.Reservation', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
