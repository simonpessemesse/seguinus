# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chambres', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tache',
            name='priorite',
            field=models.CharField(default='M', max_length=2, choices=[('B', 'Basse'), ('M', 'Moyenne'), ('H', 'Haute')]),
            preserve_default=True,
        ),
    ]
