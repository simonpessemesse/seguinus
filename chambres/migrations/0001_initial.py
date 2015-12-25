# -*- coding: utf-8 -*-


from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(unique=True)),
                ('nomUnion', models.CharField(max_length=500)),
                ('mangentPas', models.BooleanField(default=False)),
                ('personnesSupplementaires', models.IntegerField(default=0)),
                ('commentaire', models.TextField(blank=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CacheJour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jour', models.DateField()),
                ('nbCh', models.IntegerField(null=True, blank=True)),
                ('nbDortoir', models.IntegerField(null=True, blank=True)),
                ('nbanc', models.IntegerField(null=True, blank=True)),
                ('nbTotal', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Chambre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=50)),
                ('petitsLits', models.IntegerField()),
                ('grandsLits', models.IntegerField()),
                ('avecWC', models.BooleanField(default=False)),
                ('note', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=5000)),
                ('protege', models.BooleanField(default=False)),
                ('surbooking', models.BooleanField(default=False)),
                ('telephone', models.CharField(max_length=15, blank=True)),
                ('divers', models.TextField(blank=True)),
                ('arrhes', models.BooleanField(default=False)),
                ('optionJusquau', models.DateField(null=True, blank=True)),
                ('aConfiance', models.BooleanField(default=False)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=500)),
                ('cacherPremierPlan', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateArrivee', models.DateField()),
                ('dateDepart', models.DateField()),
                ('chambres', models.IntegerField(default=0)),
                ('chambresSingle', models.IntegerField(default=0)),
                ('chambresDoubles', models.IntegerField(default=0)),
                ('chambresTwin', models.IntegerField(default=0)),
                ('chambresTriples', models.IntegerField(default=0)),
                ('chambresQuadruples', models.IntegerField(default=0)),
                ('chambresQuintuples', models.IntegerField(default=0)),
                ('placesDortoir', models.IntegerField(default=0)),
                ('arrives', models.BooleanField(default=False)),
                ('partis', models.BooleanField(default=False)),
                ('aEtePrepare', models.BooleanField(default=False)),
                ('nbAnciens', models.IntegerField(default=0)),
                ('nbNouveaux', models.IntegerField(default=0)),
                ('nbEnfants', models.IntegerField(default=0)),
                ('passagersMidi', models.IntegerField(default=0)),
                ('passagersSoir', models.IntegerField(default=0)),
                ('piqueNique', models.IntegerField(default=0)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
                ('chambresAssignees', models.ManyToManyField(to='chambres.Chambre', blank=True)),
                ('client', models.ForeignKey(to='chambres.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Souci',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('repare', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
                ('chambre', models.ForeignKey(to='chambres.Chambre')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('date', models.DateField(default=datetime.date.today, null=True)),
                ('expiration', models.DateField(null=True, blank=True)),
                ('rappel', models.TimeField(null=True, blank=True)),
                ('chaqueLundi', models.BooleanField(default=False)),
                ('chaqueMardi', models.BooleanField(default=False)),
                ('chaqueMercredi', models.BooleanField(default=False)),
                ('chaqueJeudi', models.BooleanField(default=False)),
                ('chaqueVendredi', models.BooleanField(default=False)),
                ('chaqueSamedi', models.BooleanField(default=False)),
                ('chaqueDimanche', models.BooleanField(default=False)),
                ('executee', models.BooleanField(default=False)),
                ('priorite', models.CharField(default=b'M', max_length=2, choices=[('B', 'Basse'), ('M', 'Moyenne'), ('H', 'Haute')])),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
                ('entite', models.ManyToManyField(to='chambres.Entite', blank=True)),
                ('tachePapa', models.ForeignKey(blank=True, to='chambres.Tache', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TacheLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('tache', models.ForeignKey(to='chambres.Tache')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TourOperateur',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=500)),
                ('commentaire', models.TextField(blank=True)),
                ('actif', models.BooleanField(default=True)),
                ('nbJoursAnnulationAllotement', models.IntegerField(null=True, blank=True)),
                ('prixParPersonne', models.DecimalField(null=True, max_digits=15, decimal_places=5, blank=True)),
                ('gratuiteAccompagnateurSiGroupe', models.BooleanField(default=False)),
                ('seuilGroupe', models.IntegerField(null=True, blank=True)),
                ('picnicSiGroupe', models.BooleanField(default=False)),
                ('tarifReduit', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='client',
            name='tourOperateur',
            field=models.ForeignKey(blank=True, to='chambres.TourOperateur', null=True),
            preserve_default=True,
        ),
    ]
