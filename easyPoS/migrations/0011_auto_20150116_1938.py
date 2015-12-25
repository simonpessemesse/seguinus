# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('easyPoS', '0010_auto_20141210_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='etat',
            field=models.CharField(max_length=1, choices=[('B', 'Brouillon'), ('V', 'Valide'), ('C', 'Cache')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='logfacture',
            name='action',
            field=models.CharField(max_length=1, choices=[('S', 'Suppression'), ('A', 'Ajout'), ('U', 'Mise a jour')]),
            preserve_default=True,
        ),
    ]
