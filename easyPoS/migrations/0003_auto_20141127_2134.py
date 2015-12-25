# -*- coding: utf-8 -*-


from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('easyPoS', '0002_auto_20141127_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrhe',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 27, 21, 34, 2, 250667)),
        ),
        migrations.AlterField(
            model_name='arrhe',
            name='dateArrivee',
            field=models.DateField(default=datetime.datetime(2014, 11, 27, 21, 34, 2, 250646)),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 27, 21, 34, 2, 251272)),
        ),
    ]
