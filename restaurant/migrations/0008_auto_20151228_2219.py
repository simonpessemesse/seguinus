# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_resaresto_estlemidi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fournisseur',
            name='contacts',
            field=models.ManyToManyField(to='telephones.Contact', blank=True),
        ),
    ]
