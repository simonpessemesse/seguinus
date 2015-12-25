# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telephones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=500)),
                ('adresse', models.CharField(max_length=500, blank=True)),
                ('telephone', models.CharField(max_length=500, blank=True)),
                ('contacts', models.ManyToManyField(to='telephones.Contact', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fourniture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=500)),
                ('prix', models.CharField(max_length=500, blank=True)),
                ('note', models.FloatField()),
                ('dateDebut', models.DateField(null=True, blank=True)),
                ('dateFin', models.DateField(null=True, blank=True)),
                ('fournisseur', models.ForeignKey(to='restaurant.Fournisseur')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jour', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=500)),
                ('titreIngredientPrincipal', models.CharField(max_length=500, null=True, blank=True)),
                ('quantiteRequiseParPersonne', models.FloatField(null=True, blank=True)),
                ('difficulte', models.FloatField(null=True, blank=True)),
                ('tempsDePreparation', models.FloatField(null=True, blank=True)),
                ('fonction', models.CharField(max_length=2, choices=[('E', 'Entree'), ('V', 'Viande'), ('F', 'Feculent'), ('L', 'Legume'), ('FL', 'Feculent Legume'), ('D', 'Dessert'), ('M', 'Midi')])),
                ('fourniture', models.ForeignKey(blank=True, to='restaurant.Fourniture', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=500)),
                ('nb', models.PositiveSmallIntegerField()),
                ('nbEnfants', models.PositiveSmallIntegerField()),
                ('jour', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='menu',
            name='dessert',
            field=models.ManyToManyField(related_name=b'menu_dessert', to='restaurant.Plat', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menu',
            name='entree',
            field=models.ManyToManyField(related_name=b'menu_entree', to='restaurant.Plat', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menu',
            name='midi',
            field=models.ManyToManyField(related_name=b'menu_midi', to='restaurant.Plat', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menu',
            name='plat',
            field=models.ManyToManyField(related_name=b'menu_plat', to='restaurant.Plat', blank=True),
            preserve_default=True,
        ),
    ]
