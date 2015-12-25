from django.conf.urls import patterns, include, url
from django.contrib import admin
from chambres import views

urlpatterns = patterns('',
	url(r'^today$', 'chambres.views.today', name="today"),
	url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)$', 'chambres.views.stats', name="stats"),	

	url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/plusSemaine/(?P<Rid>\d+)$', 'chambres.views.plusSemaine', name="plusSemaine"),	
	url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/confirmeOpt/(?P<Rid>\d+)$', 'chambres.views.confirmeOpt', name="confirmeOpt"),	

	#url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)$', 'chambres.views.stats'),	
	url(r'^agenda/today$', 'chambres.views.globalStatToday', name="agendaToday"),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/$', 'chambres.views.globalStat', name="globalStat"),
    url(r'^today$', 'chambres.views.today'),
    url(r'^planning/today$',		'chambres.planning.planningToday', name="planningToday"),
    url(r'^agenda/today/print$', 'chambres.views.globalStatTodayPrint', name="agendaTodayPrint"),
	 url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/print$', 'chambres.views.globalStatPrint'),
	
	  url(r'^planning/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)$','chambres.planning.planning', name="planning"),
    url(r'^attribue/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)$','chambres.planning.attribue'),
    url(r'^futur/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)$','chambres.futur.futur'),
    url(r'^tourOp$', 'chambres.tourOperateurs.index', name="tourOp"),
	

	 url(r'^vuePapier/courant$', 'chambres.views.vuePapierCourante', name="vuePapierCourante"),
    url(r'^vuePapier/prochain$', 'chambres.views.vuePapierProchaine', name="vuePapierProchaine"),
    url(r'^vuePapier/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/$', 'chambres.views.vuePapier', name="vuePapier"),
    url(r'^vuePapier/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/etatResas/$', 'chambres.views.etatResas',name="etatResas"),
    url(r'^vuePapier/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/etatResas/conf/(?P<idConfiance>\d+)$', 'chambres.views.faireConfiance',name="faireConfiance"),
	  url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/arrive/(?P<id>\d+)$', 'chambres.views.arrive'),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/parti/(?P<id>\d+)$', 'chambres.views.parti'),
  url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/prepareFacture/(?P<id>\d+)$', 'chambres.views.prepareFacture'),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/imprimerCh$', 'chambres.views.imprimerCh'),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/imprimerArrivees$', 'chambres.views.imprimerArrivees'),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/imprimerRepas$', 'chambres.views.imprimerRepas'),
	url(r'^(?P<client>\d+)/$', 'chambres.views.editClient'),
	 
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/print$', 'chambres.views.globalStatPrint',name="globalStatPrint"),
    url(r'^(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/futur$', 'chambres.views.globalStatFutur'),
	 url(r'^magie/(?P<resa>\d+)$', 'chambres.magie.index'),
   

		)
