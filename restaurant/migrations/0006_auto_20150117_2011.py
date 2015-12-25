# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_resaresto_mangentpas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resaresto',
            name='reservationEcrasee',
            field=models.ForeignKey(blank=True, to='chambres.Client', null=True),
            preserve_default=True,
        ),
    ]
