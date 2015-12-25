# -*- coding: utf-8 -*-


from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('easyPoS', '0004_auto_20141127_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrhe',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 27, 21, 48, 21, 377444)),
        ),
        migrations.AlterField(
            model_name='arrhe',
            name='dateArrivee',
            field=models.DateField(default=datetime.datetime(2014, 11, 27, 21, 48, 21, 377422)),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 27, 21, 48, 21, 378053)),
        ),
    ]
