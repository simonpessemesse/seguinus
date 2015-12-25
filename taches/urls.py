from django.conf.urls import patterns, include, url
from django.contrib import admin
from taches import views

urlpatterns = patterns('',
#	url(r'^today$', 'chambres.views.today', name="today"),

	url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/0$', 'taches.views.resume'),
    url(r'^today$', 'taches.views.today'),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<entite>\d+)$', 'taches.views.resume'),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<entite>\d+)/print$', 'taches.views.resumePrint'),


	url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/delEx/(?P<id>\d+)/(?P<cat>\d+)$', 'taches.views.delId'),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/up/(?P<id>\d+)/(?P<cat>\d+)$', 'taches.views.up'),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/down/(?P<id>\d+)/(?P<cat>\d+)$', 'taches.views.down'),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/aSuivre/(?P<id>\d+)/(?P<cat>\d+)$', 'taches.views.aSuivre'),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/report/(?P<id>\d+)/(?P<cat>\d+)$', 'taches.views.report'),

	)
