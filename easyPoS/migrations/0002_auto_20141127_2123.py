# -*- coding: utf-8 -*-


from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('easyPoS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrhe',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 27, 21, 23, 4, 445989)),
        ),
        migrations.AlterField(
            model_name='arrhe',
            name='dateArrivee',
            field=models.DateField(default=datetime.datetime(2014, 11, 27, 21, 23, 4, 445968)),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 27, 21, 23, 4, 446591)),
        ),
    ]
