# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collectage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrat',
            name='congeDimanche',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='congeJeudi',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='congeLundi',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='congeMardi',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='congeMercredi',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='congeSamedi',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='congeVendredi',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='contratAide',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='surcroitActiviteWE',
            field=models.BooleanField(default=False),
        ),
    ]
