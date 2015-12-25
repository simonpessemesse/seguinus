# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accompagnement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=50)),
                ('grammesParPersonnee', models.PositiveSmallIntegerField(default=0)),
                ('unitesParPersonne', models.FloatField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Journee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entree', models.TextField(blank=True)),
                ('plat', models.TextField(blank=True)),
                ('dessert', models.TextField(blank=True)),
                ('jour', models.DateField(verbose_name=b'Jour')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JourneePensionComplete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('platMidi', models.TextField(blank=True)),
                ('dessertMidi', models.TextField(blank=True)),
                ('entreeSoir', models.TextField(blank=True)),
                ('platSoir', models.TextField(blank=True)),
                ('dessertSoir', models.TextField(blank=True)),
                ('jour', models.DateField(verbose_name=b'Jour')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MatierePremiere',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=50)),
                ('ingredients', models.ManyToManyField(to='menus.Ingredient')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='ingredient',
            field=models.ForeignKey(to='menus.MatierePremiere'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accompagnement',
            name='ingredients',
            field=models.ManyToManyField(to='menus.Ingredient'),
            preserve_default=True,
        ),
    ]
