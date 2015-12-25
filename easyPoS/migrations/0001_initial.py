# -*- coding: utf-8 -*-


from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chambres', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arrhe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=1000)),
                ('divers', models.TextField(blank=True)),
                ('montantChequeNonEncaisse', models.DecimalField(null=True, max_digits=15, decimal_places=5, blank=True)),
                ('dateArrivee', models.DateField(default=datetime.datetime(2014, 11, 27, 21, 19, 7, 564996))),
                ('date', models.DateTimeField(default=datetime.datetime(2014, 11, 27, 21, 19, 7, 565017))),
                ('estBleu', models.BooleanField(default=False)),
                ('client', models.ForeignKey(to='chambres.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=1000)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DonneesEntreprise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('denomination', models.CharField(max_length=1000)),
                ('siret', models.CharField(max_length=1000)),
                ('numeroTva', models.CharField(max_length=1000)),
                ('email', models.CharField(max_length=1000)),
                ('telephone', models.CharField(max_length=1000)),
                ('fax', models.CharField(max_length=1000)),
                ('adresse', models.TextField()),
                ('numeroFactureCourante', models.PositiveIntegerField()),
                ('numeroUrssaf', models.CharField(max_length=1000)),
                ('actif', models.BooleanField(default=True)),
                ('derniereSauvegarde', models.DateTimeField()),
                ('dernierEnvoiCaisses', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1000, blank=True)),
                ('clientNomFinal', models.CharField(max_length=1000, blank=True)),
                ('clientDiversFinal', models.TextField(blank=True)),
                ('numero', models.PositiveIntegerField(null=True, blank=True)),
                ('dateVente', models.DateTimeField(null=True, blank=True)),
                ('dateReglement', models.DateTimeField(null=True, blank=True)),
                ('toujoursVisible', models.BooleanField(default=False)),
                ('etat', models.CharField(max_length=1, choices=[(b'B', b'Brouillon'), (b'V', b'Valide'), (b'C', b'Cache')])),
                ('cacheTotalDu', models.DecimalField(null=True, max_digits=15, decimal_places=5, blank=True)),
                ('cacheTotal', models.DecimalField(null=True, max_digits=15, decimal_places=5, blank=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, to='chambres.Client', null=True)),
                ('entreprise', models.ForeignKey(to='easyPoS.DonneesEntreprise')),
                ('factureAssociee', models.ForeignKey(blank=True, to='easyPoS.Facture', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Famille',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LigneFacture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('libelle', models.CharField(max_length=5000, blank=True)),
                ('famille', models.CharField(max_length=1000, blank=True)),
                ('nomProduitFinal', models.CharField(max_length=1000, blank=True)),
                ('tauxTvaFinal', models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)),
                ('prixUnitaireFinal', models.DecimalField(null=True, max_digits=10, decimal_places=5, blank=True)),
                ('quantite', models.IntegerField(default=1)),
                ('position', models.FloatField()),
                ('facture', models.ForeignKey(to='easyPoS.Facture')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LogFacture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1000, blank=True)),
                ('moment', models.DateTimeField()),
                ('action', models.CharField(max_length=1, choices=[(b'S', b'Suppression'), (b'A', b'Ajout'), (b'U', b'Mise a jour')])),
                ('facture', models.ForeignKey(to='easyPoS.Facture')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoyenPaiement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('montant', models.DecimalField(max_digits=15, decimal_places=5)),
                ('numero', models.PositiveIntegerField(null=True, blank=True)),
                ('valide', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=datetime.datetime(2014, 11, 27, 21, 19, 7, 565626))),
                ('arrhe', models.ForeignKey(blank=True, to='easyPoS.Arrhe', null=True)),
                ('entreprise', models.ForeignKey(to='easyPoS.DonneesEntreprise')),
                ('facture', models.ForeignKey(blank=True, to='easyPoS.Facture', null=True)),
                ('moyenPaiement', models.ForeignKey(to='easyPoS.MoyenPaiement')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PreparationFacture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resaId', models.IntegerField(null=True, blank=True)),
                ('resa', models.ForeignKey(blank=True, to='chambres.Reservation', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=1000)),
                ('prix', models.DecimalField(max_digits=10, decimal_places=5)),
                ('actif', models.BooleanField(default=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
                ('categories', models.ManyToManyField(to='easyPoS.Categorie', blank=True)),
                ('famille', models.ForeignKey(to='easyPoS.Famille')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelationReservationFacture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('facture', models.ForeignKey(to='easyPoS.Facture')),
                ('reservation', models.ForeignKey(to='chambres.Reservation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RemiseCheque',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('commentaire', models.TextField(blank=True)),
                ('date', models.DateTimeField()),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=1000)),
                ('taux', models.DecimalField(max_digits=10, decimal_places=4)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='produit',
            name='tva',
            field=models.ForeignKey(to='easyPoS.Tva'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lignefacture',
            name='produit',
            field=models.ForeignKey(blank=True, to='easyPoS.Produit', null=True),
            preserve_default=True,
        ),
    ]
