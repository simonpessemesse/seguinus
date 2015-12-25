# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journee',
            name='jour',
            field=models.DateField(verbose_name='Jour'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='journeepensioncomplete',
            name='jour',
            field=models.DateField(verbose_name='Jour'),
            preserve_default=True,
        ),
    ]
