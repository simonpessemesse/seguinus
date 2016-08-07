# Create your views here.
import collections
from django.template import RequestContext
import calendar
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from easyPoS.models import Facture, DonneesEntreprise, Paiement, MoyenPaiement, PortionTVA, Arrhe, Produit, Tva, \
    Famille, Categorie, RemiseCheque, LigneFacture, LogFacture, PreparationFacture
import preferences
from datetime import datetime, date, timedelta
from chambres.models import Client
from restaurant.models import ResaResto

nomMois = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre",
           "Decembre"]
nomJour = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


@login_required
def arrhes(request):
    if ("kdo" in request.GET):
        arrhes = Arrhe.objects.all().order_by('-id').filter(
            client__reservation__isnull=True)  # .filter(paiement__facture__isnull=True)
        res = set()
        for a in arrhes:
            ps = a.paiement_set.all()

            if len(ps) == 0:
                res.add(a)
            else:
                for p in ps:
                    if not p.facture:
                        res.add(a)
        res = list(res)
        res.sort(key=lambda a: -a.id)
        arrhes = res
        titre = "Seulement Bon Cadeau"
    elif ("tout" in request.GET):
        arrhes = Arrhe.objects.all().order_by('-id')
        titre = "Tout"
    elif ("enorp" in request.GET):
        ps = Paiement.objects.filter(arrhe__isnull=False).filter(facture__isnull=True)
        arrhes = []
        for p in ps:
            arrhes.append(p.arrhe)
        arrhes.sort(key=lambda a: -a.id)
        titre = "Seulement Paiement non associe a une facture"

    else:
        arrhes = Arrhe.objects.filter(montantChequeNonEncaisse__isnull=False).order_by('-id')
        titre = "Seulement Cheque Non Encaisse"

    for a in arrhes:
        for r in a.client.reservation_set.all():
            if r.dateDepart < date.today():
                a.passe = True
            else:
                a.passe = False
        if a.date < datetime.now() - timedelta(300):
            a.vieux = True
        else:
            a.vieux = False
    totalMontant = sum([a.montantChequeNonEncaisse for a in arrhes if a.montantChequeNonEncaisse])
    return render_to_response("easyPoS/arrhe_list.html", {"object_list": arrhes, "titre": titre, "total": totalMontant})


@login_required
def chCouleur(request, arrheId):
    arrhe = Arrhe.objects.get(pk=arrheId)
    arrhe.estBleu = not arrhe.estBleu
    arrhe.save()
    return HttpResponseRedirect("..")


@login_required
def detruit(request, arrheId):
    arrhe = Arrhe.objects.get(pk=arrheId)
    arrhe.detruitCheque()
    arrhe.montantChequeNonEncaisse = None
    arrhe.save()
    return HttpResponseRedirect("..")


@login_required
def encaisse(request, arrheId):
    arrhe = Arrhe.objects.get(pk=arrheId)
    arrhe.encaisseChequeNonEncaisse()
    arrhe.save()
    return HttpResponseRedirect("..")


@login_required
def detruitArrhes(request, clientId, arrheId):
    arrhe = Arrhe.objects.get(pk=arrheId)
    arrhe.detruitCheque()
    return HttpResponseRedirect("..")


@login_required
def encaisseArrhes(request, clientId, arrheId):
    arrhe = Arrhe.objects.get(pk=arrheId)
    arrhe.encaisseChequeNonEncaisse()
    return HttpResponseRedirect(".")


@login_required
def ajoutkdo(request):
    from .ArrhesForm import NonEncaissesForm, PaiementForm, BonKdoForm

    ent = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)

    if request.method == 'POST':
        form = BonKdoForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['client']
            client = Client(nom=nom)
            client.save()

        form = NonEncaissesForm(request.POST)
        if form.is_valid():
            montant = form.cleaned_data['montantCheque']
            a = Arrhe(client=client, montantChequeNonEncaisse=montant)
            a.save()

        form = PaiementForm(request.POST)
        if form.is_valid():
            montant = form.cleaned_data['montant']
            moyen = form.cleaned_data['moyen']
            a = Arrhe(client=client)
            a.save()
            p = Paiement(entreprise=ent, arrhe=a, montant=montant, moyenPaiement=moyen)
            p.date = datetime.now()
            p.save()
        return HttpResponseRedirect(".?kdo=True")

    return render_to_response("easyPoS/addBonKdo.html",
                              {'nonEncaissesForm': NonEncaissesForm, 'paiementForm': PaiementForm,
                               'bonKdoForm': BonKdoForm}, context_instance=RequestContext(request))


def confirmeClient(c):
    c.optionJusquau = None
    c.save()


def listeModifResasAssociees(client):
    modifs = ResaResto.objects.filter(reservationEcrasee=client)
    return modifs


@login_required
def editArrhes(request, clientId):
    from .ArrhesForm import NonEncaissesForm, PaiementForm
    client = Client.objects.get(pk=clientId)

    if request.method == 'POST':
        form = NonEncaissesForm(request.POST)
        if form.is_valid():
            montant = form.cleaned_data['montantCheque']
            a = Arrhe(client=client, montantChequeNonEncaisse=montant)
            a.date = datetime.now()
            a.save()
            confirmeClient(client)

        form = PaiementForm(request.POST)
        if form.is_valid():
            montant = form.cleaned_data['montant']
            moyen = form.cleaned_data['moyen']
            a = Arrhe(client=client)
            a.date = datetime.now()
            a.save()
            ent = DonneesEntreprise.objects.get(pk=preferences.ENTREPRISE)
            p = Paiement(entreprise=ent, arrhe=a, montant=montant, moyenPaiement=moyen)
            p.date = datetime.now()
            p.save()
            confirmeClient(client)

    modifs = listeModifResasAssociees(client)
    arrhes = Arrhe.objects.filter(client=client)
    paiements = list(Paiement.objects.filter(arrhe__in=arrhes))
    arrhes = arrhes.filter(montantChequeNonEncaisse__isnull=False)
    return render_to_response('easyPoS/editArrhes.html',
                              {'nonEncaissesForm': NonEncaissesForm, 'paiementForm': PaiementForm, 'client': client,
                               'arrhes': arrhes, 'paiements': paiements, 'modifs': modifs},
                              context_instance=RequestContext(request))


@login_required
def show(request, facture_id):
    pf = PreparationFacture(resaId=int(facture_id))
    pf.save()
    return HttpResponseRedirect("/easyPoS/")


@login_required
def detailP(request, facture_id):
    return detail(request, facture_id, imprime=True)


@login_required
def detailPDevis(request, facture_id):
    return detail(request, facture_id, imprime=True, devis=True)


@login_required
def detail(request, facture_id, imprime=False, devis=False):
    p = None
    try:
        p = Facture.objects.get(pk=facture_id)
    except Facture.DoesNotExist:
        raise Http404
    donnees = p.entreprise
    return render_to_response('easyPoS/detail.html',
                              {'f': p, 'donnees': donnees, 'imprime': imprime, 'today': date.today(), 'devis': devis})


@login_required
def produits(request):
    #	paies=LigneFacture.objects.all()
    #	for i in paies:
    #		i.date=i.creation
    #		i.save()
    prods = Produit.objects.all().order_by('nom')
    return render_to_response('easyPoS/produits.html', {"prods": prods})


@login_required
def stats(request, annee=None, mois=None, jour=None, anneeF=None, moisF=None, jourF=None):
    if annee:
        dateD = date(int(annee), int(mois), int(jour))
    if annee and not anneeF:
        suiv = dateD + timedelta(1)
        factures = Facture.objects.filter(dateVente__gte=dateD).filter(dateVente__lte=suiv).filter(etat='V')
    elif annee and anneeF:
        dateF = date(int(anneeF), int(moisF), int(jourF))
        factures = Facture.objects.filter(dateVente__gte=dateD).filter(dateVente__lte=dateF).filter(etat='V')
    else:
        factures = Facture.objects.filter(dateVente__gte=date.today()).filter(
            dateVente__lte=date.today() + timedelta(1)).filter(etat='V')
    prods = Produit.objects.all().order_by('nom')
    parProd = dict([(p, (0, 0)) for p in prods])
    for f in factures:
        lignes = f.lignefacture_set.all()
        for l in lignes:
            if l.produit:
                (n, nb) = parProd[l.produit]
                parProd[l.produit] = (n + 1, nb + l.quantite)
    prods = []
    for p, tup in parProd.items():
        (nb, qua) = tup
        p.nb = nb
        p.qua = qua
        prods.append(p)
    prods.sort(key=lambda x: -x.nb)
    return render_to_response('easyPoS/stats.html', {"prods": prods})


def montreAnomalies():
    ent = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
    fact = Facture.objects.filter(entreprise=ent).filter(etat="V")
    deb = ""
    for f in fact:
        paie = f.paiement_set.all()
        for p in paie:
            if p.date < f.dateVente - timedelta(0.3):
                deb += "pb av fact " + str(f.numero) + " du " + str(f.dateVente) + " qui a un paiement du " + str(
                    p) + "\n"
    return deb


def nettoieFactures():
    pass


@login_required
def index(request):
    auj = datetime.today()

    #	lignes=LigneFacture.objects.all()
    #	for l in lignes:
    #		if not l.position:
    #			l.position=l.id
    #			l.save()

    #	pa=Paiement.objects.all()
    #	for p in pa:
    #		if p.date < datetime(2010,7,1):
    #			deb+=str(pa)+"\n"
    #	tot=0
    #	tor=0
    deb = ""
    deb += chercheTrou()
    #	nettoieLogsFacture()
    #	deb+=montreAnomalies()
    #	deb+=nettoieFactures()
    #	from django.db import connection, transaction
    #	cursor = connection.cursor()

    # cursor.execute("SELECT sum(quantite*prixUnitaireFinal) from easyPoS_ligneFacture" )
    #	row = cursor.fetchone()

    # for l in Paiement.objects.raw('SELECT sum(montant) from easyPoS_paiement'):
    #	deb+=str(row)
    #	ls=LigneFacture.objects.all()
    #	for l in ls:
    #		if not l.prixUnitaireFinal:
    #			if l.prixUnitaireFinal!=0:
    #				deb+=str(l)+" OKI "+str(l.id) + " KK "+str(l.libelle)


    #		if f.dateVente.month==7:
    #			tor+=f.total()
    #		if f.totalDu()!=0:
    #			deb+="XXXXX"+str(f)+str(f.numero)+str(f.id)+"\n"
    #	deb+=" VOIIIIIL "+str(tot)+"\n"
    #	deb+=" VOIIIIIL "+str(tor)


    return render_to_response('easyPoS/index.html', {"date": auj, "debug": deb, "hier": auj - timedelta(1)})


def chercheTrou():
    ent = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
    facturesDuJour = Facture.objects.filter(entreprise=ent).filter(etat='V').order_by('numero')
    if len(facturesDuJour) == 0:
        return ""
    tout = ""
    #	for f in facturesDuJour:
    #		tout+=str(f.numero)+" du "+str(f.dateVente)+"\n"
    tout += " ou \n\n\n"
    last = facturesDuJour[0].numero
    lastMom = facturesDuJour[0].dateVente
    for i in range(1, len(facturesDuJour)):
        f = facturesDuJour[i]
        if f.numero != last + 1 or f.dateVente < lastMom:
            tout += " ERREUR " + str(f.numero) + " du " + str(f.dateVente) + "\n"
        last = f.numero
        lastMom = f.dateVente

    return tout


class FamilleRapport():
    pass


class MoyenRapport():
    pass


class RapportGeneral():
    def __init__(self, paiements, facturesDuJour):

        self.pClasse = {}
        for p in paiements:
            if (p.facture and p.facture.etat == 'V') or p.arrhe:
                if p.moyenPaiement in self.pClasse:
                    self.pClasse[p.moyenPaiement].append(p)
                else:
                    self.pClasse[p.moyenPaiement] = [p]

        self.imprimeP = []
        for m, p in self.pClasse.items():
            self.imprimeP.append((m, p))
        self.imprimeP = reversed(self.imprimeP)

        self.moyens = []
        for moyen, paiements in self.pClasse.items():
            totalSurFacture = 0
            totalSurArrhes = 0
            totalTropPercus = 0
            for p in paiements:
                if p.montant < 0 and moyen.nom != "Espece":
                    print("trop percu", moyen)
                    totalTropPercus += p.montant
                elif p.arrhe:
                    totalSurArrhes += p.montant
                elif p.facture:
                    totalSurFacture += p.montant
                else:
                    raise Exception("Erreur paiement sans arrhes ni facture")
            paiements.sort(key=lambda x: x.montant)

            m = MoyenRapport()
            m.moyen = moyen
            m.totalSurFacture = totalSurFacture
            m.totalSurArrhes = totalSurArrhes
            m.totalTropPercus = totalTropPercus
            m.total = m.totalSurFacture + m.totalSurArrhes + m.totalTropPercus
            self.moyens.append(m)

        totalParTaux = {}
        ligneParFamille = {}
        self.taxeSejour = 0
        self.taxeSejourExoneree = 0
        for f in facturesDuJour:
            portions = f.portions()
            for p in portions:
                if p.taux in totalParTaux:
                    totalParTaux[p.taux].append(p)
                else:
                    totalParTaux[p.taux] = [p]
            for ligne in f.lignefacture_set.all():
                if ligne.produit:
                    famNom = ligne.famille
                    #	if f.estFactureHotel():
                    #		famNom="Hotel"
                    #	else:
                    #		famNom="Autre"
                    if famNom in ligneParFamille:
                        ligneParFamille[famNom].append(ligne)
                    else:
                        ligneParFamille[famNom] = [ligne]
                    if ligne.produit.id == 173:
                        self.taxeSejour += ligne.quantite
                    if ligne.produit.id == 175:
                        self.taxeSejourExoneree += ligne.quantite

        self.totalTotaux = 0
        for m in self.moyens:
            self.totalTotaux += m.totalSurFacture
            self.totalTotaux += m.totalSurArrhes

        for m in self.moyens:
            if self.totalTotaux != 0:
                m.pourcent = (m.totalSurFacture + m.totalSurArrhes) / self.totalTotaux * 100

        self.familles = []
        for famille, ligne in ligneParFamille.items():
            ttParTva = {}
            sommeTout = (sum([l.montant() for l in ligne]))
            for l in ligne:
                if l.tauxTvaFinal in ttParTva:
                    ttParTva[l.tauxTvaFinal].append(l)
                else:
                    ttParTva[l.tauxTvaFinal] = [l]
            totalParTva = {}
            for tva, lignes in ttParTva.items():
                totalParTva[tva] = (sum([l.montant() for l in lignes]), sum([l.montantHT() for l in lignes]))

            f = FamilleRapport()
            f.famille = famille
            f.total = sommeTout
            f.tva = totalParTva
            self.familles.append(f)

        self.sommePortions = []
        for taux, portions in totalParTaux.items():
            somme = 0
            for p in portions:
                somme += p.TTC
            self.sommePortions.append(PortionTVA(taux, somme))

        self.totalValide = 0
        for f in facturesDuJour:
            self.totalValide += f.total()

        self.totBase = self.totTVA = self.totTTC = 0
        for p in self.sommePortions:
            self.totBase += p.BaseHT
            self.totTVA += p.TVA
            self.totTTC += p.TTC

        for f in self.familles:
            if self.totTTC:
                f.pourcent = f.total / self.totTTC * 100


class StatDuet:
    pass


@login_required
def recapJour(request, annee, mois, jour, cherche=None):
    ent = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
    if cherche:
        factures = Facture.objects.filter(entreprise=ent).filter(clientNomFinal__icontains=cherche).exclude(etat="C")
    else:
        factures = Facture.objects.filter(entreprise=ent).filter(etat="V").filter(dateVente__year=int(annee)).filter(
            dateVente__month=int(mois)).filter(dateVente__day=int(jour))
    lignes = {}
    for f in factures:
        for l in f.lignefacture_set.all():
            if l.produit:
                prix, article = l.prixUnitaireFinal, l.produit
                duet = (prix, article)
                if duet in lignes:
                    lignes[duet].quantite += l.quantite
                    lignes[duet].lignes.append(l)
                else:
                    sd = StatDuet()
                    sd.prix = prix
                    sd.article = article
                    sd.lignes = [l]
                    sd.quantite = l.quantite
                    lignes[duet] = sd
    ll = [v for k, v in lignes.items()]

    ll = sorted(ll, key=lambda sd: sd.prix)
    return render_to_response('easyPoS/recapJour.html', {"rapport": None, "factures": factures, "lignes": ll})


class Remise:
    pass


@login_required
def remisesCheque(request, annee, mois, jour):
    rems = RemiseCheque.objects.order_by('-date')[:15]
    if len(rems) < 2:
        return
    rs = []
    premier = True
    for i in range(len(rems)):
        r = Remise()
        if premier:
            r.rCour = datetime.now()
            premier = False
        else:
            r.rCour = rems[i - 1].date
        r.rPrec = rems[i].date
        touts = Paiement.objects.filter(date__gt=r.rPrec).filter(date__lt=r.rCour).filter(
            moyenPaiement=3)  # pour cheque
        r.chs = []
        for t in touts:
            if (t.arrhe or t.facture.etat == 'V') and t.montant > 0:
                r.chs.append(t)
        r.chs.sort(key=lambda x: x.montant)
        mnt = [c.montant for c in r.chs]
        r.total = sum(mnt)
        r.nb = len(mnt)
        rs.append(r)

    return render_to_response('easyPoS/remiseCheque.html', {"remises": rems, "rs": rs})


@login_required
def valide(request, annee, mois, jour):
    rem = RemiseCheque(date=datetime.now())
    rem.save()
    return HttpResponseRedirect("/easyPoS/factures/" + annee + "/" + mois + "/" + jour)


def formatteJour(jour):
    return nomJour[jour.weekday()] + " " + str(jour.day) + " " + nomMois[jour.month - 1] + " " + str(jour.year)


class ResumePersonnalise:
    def __init__(self, jourDepart, jourFin, afficheEncaissementsDetailles=False):
        self.dateD = jourDepart
        self.dateF = jourFin
        self.prev = ""
        self.prochain = ""
        self.titre = " du " + formatteJour(jourDepart) + " au " + formatteJour(jourFin)
        self.extras = {"afficheCheques": False}
        if (jourDepart.day == 1) and jourFin.day == 1 and (jourDepart.month + 1) % 12 == jourFin.month % 12:
            self.prev, self.prochain = self.moisPrevNext(jourDepart.year, jourDepart.month)  # c'est un mois
        if jourDepart + timedelta(1) == jourFin:
            self.prev, self.prochain = self.jourPrevNext(jourDepart)
            self.remisesCheque()
        self.afficheEncaissementsDetailles = afficheEncaissementsDetailles

    def remisesCheque(self):
        r = RemiseCheque.objects.order_by('-date')
        if len(r) == 0:
            return
        remise = r[0]
        touts = Paiement.objects.filter(date__gt=remise.date).filter(moyenPaiement=3)  # pour cheque
        self.chs = []
        for t in touts:
            if (t.arrhe or t.facture.etat == 'V') and t.montant > 0:
                self.chs.append(t)
        self.chs.sort(key=lambda x: x.montant)
        mnt = [c.montant for c in self.chs]
        self.total = sum(mnt)
        self.nb = len(mnt)
        chequeParMontant = collections.OrderedDict()
        for i in self.chs:
            if i.montant in chequeParMontant:
                chequeParMontant[i.montant] += 1
            else:
                chequeParMontant[i.montant] = 1
        chtt = []
        for k, v in chequeParMontant.items():
            chtt.append((k, v))
        self.extras = {"afficheCheques": True, "nb": self.nb, "total": self.total, "cheques": self.chs,
                       "chequeParMontant": chtt}

    def jourPrevNext(self, jourDepart):
        prochainDay = jourDepart + timedelta(1)
        prochain = str(prochainDay.year) + "/" + str(prochainDay.month) + "/" + str(prochainDay.day)
        prevDay = jourDepart - timedelta(1)
        prev = str(prevDay.year) + "/" + str(prevDay.month) + "/" + str(prevDay.day)
        self.titre = " du " + formatteJour(jourDepart)
        return prev, prochain

    def moisPrevNext(self, annee, mois):
        dateD = date(int(annee), int(mois), 15)
        prochainDay = dateD + timedelta(30)
        prochain = str(prochainDay.year) + "/" + str(prochainDay.month)
        prevDay = dateD - timedelta(30)
        prev = str(prevDay.year) + "/" + str(prevDay.month)
        self.titre = " du mois de " + nomMois[dateD.month - 1] + " " + str(annee)
        return prev, prochain

    def rapportEtFactures(self):
        ent = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
        paiements = Paiement.objects.filter(entreprise=ent).filter(date__gte=self.dateD).filter(date__lte=self.dateF)
        facturesDuJour = Facture.objects.filter(entreprise=ent).filter(dateVente__gte=self.dateD).filter(
            dateVente__lte=self.dateF).order_by('numero').filter(etat='V')
        r = RapportGeneral(paiements, facturesDuJour)
        return r, facturesDuJour

    def resultat(self, request):

        r, facturesDuJour = self.rapportEtFactures()
        if request:
            user = request.user
        else:
            user = None

        debiteurs = 0
        ent = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
        factNonPaye = Facture.objects.filter(entreprise=ent).filter(cacheTotalDu__gt=0).filter(etat='V')
        factNonPaye2 = set(Facture.objects.filter(entreprise=ent).filter(cacheTotalDu__lt=0).filter(etat='V')).union(
            set(factNonPaye))
        for f in factNonPaye2:
            debiteurs += f.totalDu()

        arguments = {"prochain": self.prochain, "prev": self.prev, "date": self.dateD, "rapport": r,
                     "factures": facturesDuJour, "afficheEncaissementsDetailles": self.afficheEncaissementsDetailles,
                     "titre": self.titre, "user": user, "debiteurs": debiteurs}
        arguments.update(self.extras)

        return render_to_response('easyPoS/resumeQuotidien.html', arguments)

    def imprimerCaisse(self):
        r, tmp = self.rapportEtFactures()
        return render_to_response('easyPoS/imprimerCaisse.html', {"rapport": r, "date": self.date})


@login_required
def imprimer(request, annee, mois, jour):
    dateD = date(int(annee), int(mois), int(jour))
    prochainDay = dateD + timedelta(1)

    r = ResumePersonnalise(dateD, prochainDay, afficheEncaissementsDetailles=True)
    r.date = dateD
    return r.imprimerCaisse()


@login_required
def cherche(request, cherche):
    ent = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
    factures = Facture.objects.filter(entreprise=ent).filter(clientNomFinal__icontains=cherche).exclude(etat="C")
    return render_to_response('easyPoS/cherche.html', {"factures": factures})


@login_required
def chercheValeur(request, cherche):
    ent = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
    factures = Facture.objects.filter(entreprise=ent).filter(cacheTotal=cherche).exclude(etat="C")
    return render_to_response('easyPoS/chercheValeur.html', {"factures": factures})


@login_required
def chercheNumero(request, cherche):
    ent = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
    factures = Facture.objects.filter(entreprise=ent).filter(numero=cherche).filter(etat="V")
    return render_to_response('easyPoS/cherche.html', {"factures": factures})


@login_required
def cherchePaiement(request, cherche):
    paiements = Paiement.objects.filter(montant=cherche).exclude(facture__etat="C")
    return render_to_response('easyPoS/cherchePaiement.html', {"paiements": paiements})


@login_required
def resumeQuotidien(request, annee, mois, jour):
    dateD = date(int(annee), int(mois), int(jour))
    prochainDay = dateD + timedelta(1)

    r = ResumePersonnalise(dateD, prochainDay, afficheEncaissementsDetailles=True)
    return r.resultat(request)


def resumeMensuelInsecure(request, annee, mois):
    dateD = date(int(annee), int(mois), 15)
    prochainDay = dateD + timedelta(30)
    premierJour = date(int(annee), int(mois), 1)
    dernierJour = date(prochainDay.year, prochainDay.month, 1)

    r = ResumePersonnalise(premierJour, dernierJour)
    return r.resultat(request)


@login_required
def resumeMensuel(request, annee, mois):
    return resumeMensuelInsecure(request, annee, mois)


@login_required
def resumePerso(request, annee, mois, jour, anneeF, moisF, jourF):
    dateD = date(int(annee), int(mois), int(jour))
    dateF = date(int(anneeF), int(moisF), int(jourF))

    r = ResumePersonnalise(dateD, dateF)
    return r.resultat(request)


def encaissementsInsecure(annee, mois):
    dateD = date(int(annee), int(mois), 15)
    prochainDay = dateD + timedelta(30)
    prochain = str(prochainDay.year) + "/" + str(prochainDay.month)
    prevDay = dateD - timedelta(30)
    prev = str(prevDay.year) + "/" + str(prevDay.month)

    joursAEtudier = []
    numberDaysInMonth = calendar.monthrange(dateD.year, dateD.month)[1]
    encaissements = []
    for i in range(numberDaysInMonth):
        joursAEtudier.append(date(dateD.year, dateD.month, i + 1))
    for j in joursAEtudier:
        (jour, mois, annee) = (j.day, j.month, j.year)
        ent = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
        paiements = Paiement.objects.filter(entreprise=ent).filter(date__month=mois).filter(date__year=annee).filter(
            date__day=jour)
        facturesDuJour = Facture.objects.filter(entreprise=ent).filter(dateVente__month=mois).filter(
            dateVente__year=annee).filter(dateVente__day=jour).order_by('numero').filter(etat='V')
        rj = RapportGeneral(paiements, facturesDuJour)
        encaissements.append((j, rj.moyens, rj.totalTotaux))
    total = {}
    totalGeneral = 0
    for j, parMoyen, parJour in encaissements:
        for m in parMoyen:
            if m.moyen in total:
                total[m.moyen][0] += m.totalSurFacture
                total[m.moyen][1] += m.totalSurArrhes
                total[m.moyen][2] += m.totalTropPercus
            else:
                total[m.moyen] = [m.totalSurFacture, m.totalSurArrhes, m.totalTropPercus]
        totalGeneral += parJour
    #	encaissements.reverse()
    return render_to_response('easyPoS/encaissementParPeriodes.html',
                              {"date": dateD, "prochain": prochain, "prev": prev, "encaissements": encaissements,
                               "total": total, "totalGeneral": totalGeneral})


@login_required
def encaissementsParPeriode(request, annee, mois):
    return encaissementsInsecure(annee, mois)


def getCols(factures):
    nbFact = len(factures)
    nbParCol = nbFact / 3
    col1 = []
    col2 = []
    col3 = []
    for i in range(0, nbFact):
        if i <= nbParCol:
            col1.append(factures[i])
        elif i <= nbParCol * 2:
            col2.append(factures[i])
        else:
            col3.append(factures[i])

    return col1, col2, col3


@login_required
def doublesQuotidienPrint(request):
    tod = date.today() - timedelta(1)
    return doublesQuotidien(request, tod.year, tod.month, tod.day, imprime=True)


@login_required
def doublesQuotidien(request, annee, mois, jour, imprime=False):
    dateD = date(int(annee), int(mois), int(jour))
    prochainDay = dateD + timedelta(1)
    prochain = str(prochainDay.year) + "/" + str(prochainDay.month) + "/" + str(prochainDay.day)
    prevDay = dateD - timedelta(1)
    prev = str(prevDay.year) + "/" + str(prevDay.month) + "/" + str(prevDay.day)

    ent = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
    factures = Facture.objects.filter(entreprise=ent).filter(dateVente__month=mois).filter(
        dateVente__year=annee).filter(dateVente__day=jour).order_by('numero').filter(etat='V')
    col1, col2, col3 = getCols(factures)

    return render_to_response('easyPoS/doublesQuotidien.html',
                              {"date": dateD, "prochain": prochain, "prev": prev, "factures": factures, "col1": col1,
                               "col2": col2, "col3": col3, "all": factures, "imprime": imprime})


@login_required
def doublesMensuels(request, annee, mois):
    dateD = date(int(annee), int(mois), 15)
    prochainDay = dateD + timedelta(30)
    prochain = str(prochainDay.year) + "/" + str(prochainDay.month)
    prevDay = dateD - timedelta(30)
    prev = str(prevDay.year) + "/" + str(prevDay.month)

    ent = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
    factures = Facture.objects.filter(entreprise=ent).filter(dateVente__month=mois).filter(
        dateVente__year=annee).order_by('numero').filter(etat='V')
    col1, col2, col3 = getCols(factures)

    return render_to_response('easyPoS/doublesQuotidien.html',
                              {"date": dateD, "prochain": prochain, "prev": prev, "month": True, "factures": factures,
                               "col1": col1, "col2": col2, "col3": col3, "all": factures})
