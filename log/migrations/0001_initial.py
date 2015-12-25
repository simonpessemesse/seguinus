# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chambres', '0001_initial'),
        ('easyPoS', '0003_auto_20141127_2134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=10000, blank=True)),
                ('debutImpact', models.DateField(null=True, blank=True)),
                ('finImpact', models.DateField(null=True, blank=True)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(blank=True, to='chambres.Client', null=True)),
                ('facture', models.ForeignKey(blank=True, to='easyPoS.Facture', null=True)),
                ('reservation', models.ForeignKey(blank=True, to='chambres.Reservation', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
