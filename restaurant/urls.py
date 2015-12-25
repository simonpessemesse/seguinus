
from django.conf.urls import patterns, include, url
from django.contrib import admin
from restaurant import views


urlpatterns = patterns('restaurant.views',
	    url(r'^$', 'index', name="restaurant"),
    url(r'^plats$', 'plats'),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)$', 'jour'),
    url(r'^(?P<fournisseur>\d+)/$', 'fournisseur'),
    url(r'^(?P<fournisseur>\d+)/reset$', 'fournisseurReset'),
    url(r'^c/(?P<lon>\d+)/$', 'compose'),
    url(r'^c/(?P<lon>\d+)/reset$', 'composeReset'),
    url(r'^(?P<fournisseur>\d+)/(?P<produit>\d+)/up$', 'up'),
    url(r'^(?P<fournisseur>\d+)/(?P<produit>\d+)/down$', 'down'),
	url(r'^ajoutModif/(?P<client_id>\d+)/$', views.ajouteModifResa, name='ajouteModifResa'),
	url(r'^supprime/(?P<resaResto_id>\d+)/$', views.supprimeModifResa, name='supprime'),
	)
