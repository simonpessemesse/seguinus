from django.conf.urls import patterns, include, url
from django.contrib import admin
from taches import views

urlpatterns = [
    #	url(r'^today$', 'chambres.views.today', name="today"),

    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/0$', views.resume),
    url(r'^today$', views.today),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<entite>\d+)$', views.resume),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<entite>\d+)/print$', views.resumePrint),

    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/delEx/(?P<id>\d+)/(?P<cat>\d+)$', views.delId),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/up/(?P<id>\d+)/(?P<cat>\d+)$', views.up),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/down/(?P<id>\d+)/(?P<cat>\d+)$', views.down),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/aSuivre/(?P<id>\d+)/(?P<cat>\d+)$', views.aSuivre),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/report/(?P<id>\d+)/(?P<cat>\d+)$', views.report),

]
