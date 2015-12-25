# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('easyPoS', '0006_auto_20141209_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrhe',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 22, 37, 34, 5595)),
        ),
        migrations.AlterField(
            model_name='arrhe',
            name='dateArrivee',
            field=models.DateField(default=datetime.datetime(2014, 12, 9, 22, 37, 34, 5563)),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 22, 37, 34, 6447)),
        ),
    ]
