# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collectage', '0003_auto_20150116_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donpourboire',
            name='montant',
            field=models.DecimalField(max_digits=9, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pourboire',
            name='montant',
            field=models.DecimalField(max_digits=9, decimal_places=2),
            preserve_default=True,
        ),
    ]
