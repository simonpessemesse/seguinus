
from django.conf.urls import patterns, include, url
from django.contrib import admin
from restaurant import views


urlpatterns = [
	    url(r'^$',  views.index, name="restaurant"),
    url(r'^plats$',  views.plats),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)$',  views.jour),
    url(r'^(?P<fournisseur>\d+)/$',  views.fournisseur),
    url(r'^(?P<fournisseur>\d+)/reset$',  views.fournisseurReset),
    url(r'^c/(?P<lon>\d+)/$',  views.compose),
    url(r'^c/(?P<lon>\d+)/reset$',  views.composeReset),
    url(r'^(?P<fournisseur>\d+)/(?P<produit>\d+)/up$',  views.up),
    url(r'^(?P<fournisseur>\d+)/(?P<produit>\d+)/down$',  views.down),
	url(r'^ajoutModif/(?P<client_id>\d+)/$', views.ajouteModifResa,name="ajouteModifResa"),
	url(r'^supprime/(?P<resaResto_id>\d+)/$', views.supprimeModifResa,name="supprime"),
	]
