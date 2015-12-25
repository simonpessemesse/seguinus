# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chambres', '0002_auto_20150116_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='nbAnciens',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='nbNouveaux',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='passagersMidi',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='passagersSoir',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='piqueNique',
        ),
    ]
