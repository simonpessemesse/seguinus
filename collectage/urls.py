from django.conf.urls import patterns, include, url
from django.contrib import admin
from chambres import views

urlpatterns = patterns('collectage.views',
	url(r'^rh$', 'rhIndex',name="rhIndex"),
	url(r'^dif$', 'dif'),
#    url(r'^rh/(?P<object_id>\d+)/$', 'indivDetail'),
    url(r'^rh/ct/(?P<numContrat>\d+)/$', 'contrat'),
    url(r'^rh/fne/(?P<numContrat>\d+)/$', 'ficheNouvelleEmbauche'),
    url(r'^rh/mutuelle/(?P<numContrat>\d+)/$', 'ficheMutuelle'),
    url(r'^rh/ficheHeures/(?P<numContrat>\d+)/$', 'ficheHeures'),
    url(r'^mois$', 'moisCourant', name="moisCourant"),
    url(r'^registre$', 'registre'),
    url(r'^mois/(?P<annee>\d+)/(?P<mois>\d+)/$', 'moisMail'),
    url(r'^mois/(?P<annee>\d+)/(?P<mois>\d+)/preremplistout$', 'preremplistout'),
    url(r'^mois/(?P<annee>\d+)/(?P<mois>\d+)/genereTaches$', 'genereTaches'),
	url(r'^pb/$', 'pb', name="pb"),
    url(r'^pb/(?P<individu>\d+)$', 'pbInit'),
    url(r'^pb/show/(?P<individu>\d+)$', 'pb'),
    url(r'^pb/(?P<individu>\d+)/(?P<don>\d+)$', 'pbInit'),
    url(r'^emploiDuTemps/$', 'emploiDuTemps'),
    url(r'^emploiDuTemps/today$', 'today'),
    url(r'^emploiDuTemps/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/$','intervalle'),
    url(r'^emploiDuTemps/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/(?P<contrat>\d+)/$','intervalleEmploye'),
    url(r'^emploiDuTemps/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/(?P<contrat>\d+)/print$','intervalleEmployePrint'),
    url(r'^emploiDuTemps/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/(?P<contrat>\d+)/copier$','copierIntervalleEmploye'),
    url(r'^emploiDuTemps/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/(?P<contrat>\d+)/preremplir$','preremplir'),
    url(r'^emploiDuTemps/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/(?P<contrat>\d+)/reset$','reset')
)
