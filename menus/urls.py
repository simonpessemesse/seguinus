from django.conf.urls import patterns, include, url
from django.contrib import admin
from menus import views

urlpatterns = [
url(r'^menus/$',  views.index),
    url(r'^menus/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)$',  views.semaine),
    url(r'^menuspensioncomplete/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)$',  views.semainecomplete),
]
   
