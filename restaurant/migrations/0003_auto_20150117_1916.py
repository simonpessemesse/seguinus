# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_resaresto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resaresto',
            name='nbAnciens',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resaresto',
            name='nbEnfants',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resaresto',
            name='nbNouveaux',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resaresto',
            name='nbPassagers',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resaresto',
            name='nbPiquesNiques',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
