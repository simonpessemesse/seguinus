# -*- coding: utf-8 -*-


from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contrat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateDebut', models.DateField(null=True, blank=True)),
                ('dateFin', models.DateField(null=True, blank=True)),
                ('qualification', models.CharField(max_length=200, blank=True)),
                ('motifContrat', models.CharField(max_length=200, blank=True)),
                ('emploi', models.CharField(max_length=200)),
                ('typeDuContrat', models.CharField(max_length=1, choices=[(b'S', b'Saisonnier'), (b'P', b'Saisonnier Temps Partiel'), (b'E', b'Extra'), (b'I', b'Indetermine'), (b'D', b'Determine'), (b'X', b'Determine Temps Partiel'), (b'A', b'Avenant')])),
                ('contratAide', models.BooleanField()),
                ('nombreHeuresSemaine', models.DecimalField(max_digits=7, decimal_places=3)),
                ('nbRepasJour', models.SmallIntegerField()),
                ('fonction', models.CharField(max_length=200, blank=True)),
                ('coefficient', models.CharField(max_length=200, blank=True)),
                ('tauxHoraireBrut', models.DecimalField(default=9.53, null=True, max_digits=10, decimal_places=4, blank=True)),
                ('congeLundi', models.BooleanField()),
                ('congeMardi', models.BooleanField()),
                ('congeMercredi', models.BooleanField()),
                ('congeJeudi', models.BooleanField()),
                ('congeVendredi', models.BooleanField()),
                ('congeSamedi', models.BooleanField()),
                ('congeDimanche', models.BooleanField()),
                ('surcroitActiviteWE', models.BooleanField()),
                ('demiJourneeConge', models.SmallIntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DonPourboire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('montant', models.DecimalField(max_digits=7, decimal_places=2)),
                ('commentaire', models.CharField(max_length=300, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=200, blank=True)),
                ('prenom', models.CharField(max_length=200, blank=True)),
                ('dateNaissance', models.DateField(null=True, blank=True)),
                ('sexe', models.CharField(blank=True, max_length=1, null=True, choices=[(b'M', b'Masculin'), (b'F', b'Feminin')])),
                ('nationalite', models.CharField(max_length=200, blank=True)),
                ('qualification', models.CharField(max_length=200, blank=True)),
                ('adresse', models.TextField(blank=True)),
                ('numeroSecuriteSociale', models.CharField(max_length=200, blank=True)),
                ('emploi', models.CharField(max_length=200, blank=True)),
                ('typeDuContrat', models.CharField(max_length=200, blank=True)),
                ('evenementsPosterieursALembauche', models.CharField(max_length=200, blank=True)),
                ('dateEntree', models.DateField(null=True, blank=True)),
                ('dateSortie', models.DateField(null=True, blank=True)),
                ('nombreHeuresMois', models.DecimalField(null=True, max_digits=7, decimal_places=3, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HeurePlanifiee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jour', models.DateField()),
                ('heureDebut', models.TimeField(null=True, blank=True)),
                ('heureFin', models.TimeField(null=True, blank=True)),
                ('tempsTravaille', models.IntegerField(null=True, blank=True)),
                ('nbRepasPris', models.SmallIntegerField(default=0)),
                ('absence', models.BooleanField(default=False)),
                ('commentaire', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Individu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=200)),
                ('prenom', models.CharField(max_length=200)),
                ('denomination', models.CharField(blank=True, max_length=1, null=True, choices=[(b'M', b'Monsieur'), (b'L', b'Mademoiselle'), (b'A', b'Madame')])),
                ('nomJeuneFille', models.CharField(max_length=200, blank=True)),
                ('dateNaissance', models.DateField(null=True, blank=True)),
                ('communeNaissance', models.CharField(max_length=200, blank=True)),
                ('paysNaissance', models.CharField(max_length=200, blank=True)),
                ('sexe', models.CharField(blank=True, max_length=1, null=True, choices=[(b'M', b'Masculin'), (b'F', b'Feminin')])),
                ('situationDeFamille', models.CharField(blank=True, max_length=1, choices=[(b'C', b'Celibataire'), (b'M', b'Marie')])),
                ('nationalite', models.CharField(max_length=200, blank=True)),
                ('adresse', models.TextField(blank=True)),
                ('numeroSecuriteSociale', models.CharField(max_length=200, blank=True)),
                ('numeroTelephone', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(unique=True, max_length=200)),
                ('heureNormaleDebutTravailMatin', models.TimeField(null=True, verbose_name=b'heure habituelle de debut le matin', blank=True)),
                ('heureNormaleDebutTravailAprem', models.TimeField(null=True, verbose_name=b"heure habituelle de debut l'aprem", blank=True)),
                ('nbHeuresParSemaine', models.PositiveIntegerField(null=True, verbose_name=b"nombre d'heures par semaine", blank=True)),
                ('actif', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heureDebut', models.DateTimeField(null=True, verbose_name=b'heure debut service', blank=True)),
                ('heureFin', models.DateTimeField(null=True, verbose_name=b'heure fin service', blank=True)),
                ('commentaire', models.CharField(max_length=200, blank=True)),
                ('personne', models.ForeignKey(to='collectage.Individu')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pourboire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('montant', models.DecimalField(max_digits=7, decimal_places=2)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('commentaire', models.CharField(max_length=300, blank=True)),
                ('individus', models.ManyToManyField(to='collectage.Individu')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='heureplanifiee',
            name='employe',
            field=models.ForeignKey(to='collectage.Individu'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='donpourboire',
            name='individu',
            field=models.ForeignKey(to='collectage.Individu'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contrat',
            name='individu',
            field=models.ForeignKey(to='collectage.Individu'),
            preserve_default=True,
        ),
    ]
