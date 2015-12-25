# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_auto_20150117_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='resaresto',
            name='mangentPas',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
