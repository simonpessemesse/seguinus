from django.conf.urls import patterns, include, url
from django.contrib import admin
from chambres import views

urlpatterns = patterns('',   
url(r'^menus/$', 'menus.views.index'),
    url(r'^menus/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)$', 'menus.views.semaine'),
    url(r'^menuspensioncomplete/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)$', 'menus.views.semainecomplete'),
)
   
