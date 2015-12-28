from django.conf.urls import include, url
from django.contrib import admin

from easyPoS import views


urlpatterns = [
		url(r'^facture/(?P<facture_id>\d+)/$',  views.detail),
	url(r'^facture/(?P<facture_id>\d+)/show$',  views.show),
	url(r'^facture/(?P<facture_id>\d+)/print$',  views.detailP),
	url(r'^facture/(?P<facture_id>\d+)/printDevis$',  views.detailPDevis),
	url(r'^$',  views.index, name="facturation"),
	url(r'^produits/$',  views.produits),
	url(r'^produits/stats$',  views.stats),
    url(r'^produits/stats/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)$',  views.stats),
    url(r'^produits/stats/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)$',  views.stats),
	url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/$',  views.resumeQuotidien,name="resumeQuotidien"),
	url(r'^factures/cherche/(?P<cherche>.+)$',  views.cherche),
	url(r'^factures/chercheValeur/(?P<cherche>.+)$',  views.chercheValeur),
	url(r'^factures/cherchePaiement/(?P<cherche>.+)$',  views.cherchePaiement),
	url(r'^factures/chercheNumero/(?P<cherche>.+)$',  views.chercheNumero),
    url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/imprimer$',  views.imprimer),
	url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/valide$',  views.valide),
	url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/remisesCheque$',  views.remisesCheque),
	url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/cherche/(?P<cherche>.+)$',  views.recapJour),
	url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/cherche$',  views.recapJour),
	url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/$',  views.resumeMensuel),
	url(r'^factures/encaissementsParPeriode/(?P<annee>\d+)/(?P<mois>\d+)/$',  views.encaissementsParPeriode),
    url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)$',  views.resumePerso),
    url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/$',  views.resumePerso),

	url(r'^factures/doubles/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/$',  views.doublesQuotidien),
	url(r'^factures/doubles/(?P<annee>\d+)/(?P<mois>\d+)/$',  views.doublesMensuels),
	url(r'^factures/doubles/printHier$',  views.doublesQuotidienPrint),

    url(r'^arrhes/$',  views.arrhes),
    url(r'^arrhes/ajoutBonCadeau$',  views.ajoutkdo),
    url(r'^arrhes/(?P<clientId>\d+)/$',  views.editArrhes),
    url(r'^arrhes/(?P<arrheId>\d+)/chColor$',  views.chCouleur),
    url(r'^arrhes/(?P<arrheId>\d+)/encaisse$',  views.encaisse),
    url(r'^arrhes/(?P<arrheId>\d+)/detruit$',  views.detruit),
    url(r'^arrhes/(?P<clientId>\d+)/(?P<arrheId>\d+)$',  views.encaisseArrhes),
    url(r'^arrhes/(?P<clientId>\d+)/sup/(?P<arrheId>\d+)$',  views.detruitArrhes),



 #   url(r'^factures/doubles/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)$',  views.doublesPerso),

]
