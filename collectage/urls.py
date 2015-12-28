from django.conf.urls import patterns, include, url
from django.contrib import admin
from collectage import views

urlpatterns = [
	url(r'^rh$',  views.rhIndex,name="rhIndex"),
	url(r'^dif$',  views.dif),
#    url(r'^rh/(?P<object_id>\d+)/$',  views.indivDetail),
    url(r'^rh/ct/(?P<numContrat>\d+)/$',  views.contrat),
    url(r'^rh/fne/(?P<numContrat>\d+)/$',  views.ficheNouvelleEmbauche),
    url(r'^rh/mutuelle/(?P<numContrat>\d+)/$',  views.ficheMutuelle),
    url(r'^rh/ficheHeures/(?P<numContrat>\d+)/$',  views.ficheHeures),
    url(r'^mois$',  views.moisCourant, name="moisCourant"),
    url(r'^registre$',  views.registre),
    url(r'^mois/(?P<annee>\d+)/(?P<mois>\d+)/$',  views.moisMail),
    url(r'^mois/(?P<annee>\d+)/(?P<mois>\d+)/preremplistout$',  views.preremplistout),
    url(r'^mois/(?P<annee>\d+)/(?P<mois>\d+)/genereTaches$',  views.genereTaches),
	url(r'^pb/$',  views.pb, name="pb"),
    url(r'^pb/(?P<individu>\d+)$',  views.pbInit),
    url(r'^pb/show/(?P<individu>\d+)$',  views.pb),
    url(r'^pb/(?P<individu>\d+)/(?P<don>\d+)$',  views.pbInit),
    url(r'^emploiDuTemps/$',  views.emploiDuTemps),
    url(r'^emploiDuTemps/today$',  views.today),
    url(r'^emploiDuTemps/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/$', views.intervalle),
    url(r'^emploiDuTemps/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/(?P<contrat>\d+)/$', views.intervalleEmploye),
    url(r'^emploiDuTemps/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/(?P<contrat>\d+)/print$', views.intervalleEmployePrint),
    url(r'^emploiDuTemps/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/(?P<contrat>\d+)/copier$', views.copierIntervalleEmploye),
    url(r'^emploiDuTemps/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/(?P<contrat>\d+)/preremplir$', views.preremplir),
    url(r'^emploiDuTemps/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/(?P<contrat>\d+)/reset$', views.reset)
    ]
