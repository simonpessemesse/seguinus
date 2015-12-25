from django.conf.urls import patterns, include, url
from django.contrib import admin




urlpatterns = patterns('easyPoS.views',
		url(r'^facture/(?P<facture_id>\d+)/$', 'detail'),
	url(r'^facture/(?P<facture_id>\d+)/show$', 'show'),
	url(r'^facture/(?P<facture_id>\d+)/print$', 'detailP'),
	url(r'^facture/(?P<facture_id>\d+)/printDevis$', 'detailPDevis'),
	url(r'^$', 'index', name="facturation"),
	url(r'^produits/$', 'produits'),
	url(r'^produits/stats$', 'stats'),
    url(r'^produits/stats/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)$', 'stats'),
    url(r'^produits/stats/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)$', 'stats'),
	url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/$', 'resumeQuotidien',name="resumeQuotidien"),
	url(r'^factures/cherche/(?P<cherche>.+)$', 'cherche'),
	url(r'^factures/chercheValeur/(?P<cherche>.+)$', 'chercheValeur'),
	url(r'^factures/cherchePaiement/(?P<cherche>.+)$', 'cherchePaiement'),
	url(r'^factures/chercheNumero/(?P<cherche>.+)$', 'chercheNumero'),
    url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/imprimer$', 'imprimer'),
	url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/valide$', 'valide'),
	url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/remisesCheque$', 'remisesCheque'),
	url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/cherche/(?P<cherche>.+)$', 'recapJour'),
	url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/cherche$', 'recapJour'),
	url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/$', 'resumeMensuel'),
	url(r'^factures/encaissementsParPeriode/(?P<annee>\d+)/(?P<mois>\d+)/$', 'encaissementsParPeriode'),
    url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)$', 'resumePerso'),
    url(r'^factures/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)/$', 'resumePerso'),

	url(r'^factures/doubles/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/$', 'doublesQuotidien'),
	url(r'^factures/doubles/(?P<annee>\d+)/(?P<mois>\d+)/$', 'doublesMensuels'),
	url(r'^factures/doubles/printHier$', 'doublesQuotidienPrint'),

    url(r'^arrhes/$', 'arrhes'),
    url(r'^arrhes/ajoutBonCadeau$', 'ajoutkdo'),
    url(r'^arrhes/(?P<clientId>\d+)/$', 'editArrhes'),
    url(r'^arrhes/(?P<arrheId>\d+)/chColor$', 'chCouleur'),
    url(r'^arrhes/(?P<arrheId>\d+)/encaisse$', 'encaisse'),
    url(r'^arrhes/(?P<arrheId>\d+)/detruit$', 'detruit'),
    url(r'^arrhes/(?P<clientId>\d+)/(?P<arrheId>\d+)$', 'encaisseArrhes'),
    url(r'^arrhes/(?P<clientId>\d+)/sup/(?P<arrheId>\d+)$', 'detruitArrhes'),



 #   url(r'^factures/doubles/(?P<annee>\d+)/(?P<mois>\d+)/(?P<jour>\d+)/(?P<anneeF>\d+)/(?P<moisF>\d+)/(?P<jourF>\d+)$', 'doublesPerso'),

	)
