# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20150117_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resaresto',
            name='nom',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
    ]
