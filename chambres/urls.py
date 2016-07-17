from django.conf.urls import patterns, include, url
from chambres import planning
from chambres import futur
from chambres import tourOperateurs
from chambres import magie
from django.contrib import admin
from chambres import views

urlpatterns = [
    url(r'^today$', views.today, name="today"),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)$', views.stats, name="stats"),

    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/plusSemaine/(?P<Rid>\d+)$', views.plusSemaine,
        name="plusSemaine"),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/confirmeOpt/(?P<Rid>\d+)$', views.confirmeOpt,
        name="confirmeOpt"),

    # url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)$',  views.stats),
    url(r'^agenda/today$', views.globalStatToday, name="agendaToday"),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/$',
        views.globalStat, name="globalStat"),
    url(r'^today$', views.today),
    url(r'^planning/today$', planning.planningToday, name="planningToday"),
    url(r'^agenda/today/print$', views.globalStatTodayPrint, name="agendaTodayPrint"),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/print$',
        views.globalStatPrint),

    url(r'^planning/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)$',
        planning.planning, name="planning"),
    url(r'^attribue/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)$',
        planning.attribue),
    url(r'^futur/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)$',
        futur.futur),
    url(r'^tourOp$', tourOperateurs.index, name="tourOp"),

    url(r'^vuePapier/courant$', views.vuePapierCourante, name="vuePapierCourante"),
    url(r'^vuePapier/prochain$', views.vuePapierProchaine, name="vuePapierProchaine"),
    url(r'^vuePapier/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/$',
        views.vuePapier, name="vuePapier"),
    url(
        r'^vuePapier/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/etatResas/$',
        views.etatResas, name="etatResas"),
    url(
        r'^vuePapier/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/etatResas/conf/(?P<idConfiance>\d+)$',
        views.faireConfiance, name="faireConfiance"),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/arrive/(?P<id>\d+)$', views.arrive),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/parti/(?P<id>\d+)$', views.parti),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/prepareFacture/(?P<id>\d+)$', views.prepareFacture),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/imprimerCh$', views.imprimerCh),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/imprimerArrivees$', views.imprimerArrivees),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/imprimerRepas$', views.imprimerRepas),
    url(r'^(?P<client>\d+)/$', views.editClient),

    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/print$',
        views.globalStatPrint, name="globalStatPrint"),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/futur$',
        views.globalStatFutur),
    url(r'^magie/(?P<resa>\d+)$', magie.index),

]
