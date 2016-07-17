from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory

from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from datetime import datetime, date, timedelta, time
from chambres.models import Chambre, Souci, Client, Reservation, Tache, Amour, CacheJour, Entite, TourOperateur, \
    ClientForm
from taches.views import taches
from easyPoS.models import PreparationFacture, Paiement, Arrhe, MoyenPaiement
from django.forms import ModelForm
from django import forms
from . import repas

jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

import colorsys


def avoirCouleurSelonQuantite(quantite):
    c = 355  # couleur de base

    quantiteMax = 40
    piscineDeCouleurs = []
    nbParCoulBase = quantiteMax + 1
    for i in range(nbParCoulBase):
        h = c / 360.
        v = 0.1 + i * 0.9 / float(nbParCoulBase)
        s = 1
        (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
        rr = "%x" % int(r * 255)
        gg = "%x" % int(g * 255)
        bb = "%x" % int(b * 255)
        if len(rr) == 1:
            rr = "0" + rr
        if len(gg) == 1:
            gg = "0" + gg
        if len(bb) == 1:
            bb = "0" + bb
        coull = rr + gg + bb
        piscineDeCouleurs.append("#" + rr + gg + bb)
    if quantite > quantiteMax:
        quantite = quantiteMax
    return piscineDeCouleurs[quantite]


@login_required
def today(request):
    auj = date.today()
    return HttpResponseRedirect(reverse("stats", args=[auj.year, auj.month, auj.day]))


def getDoublons(list):
    liste2 = []
    listeErreurs = []
    for elt in list:
        try:
            ind = liste2.index(elt)
            listeErreurs.append(elt)
        except:
            liste2.append(elt)
    return listeErreurs


def racine(request):
    return render_to_response('racine.html', {})


class OneDayStats:
    def __init__(self, dateDemandee):
        self.nomJour = jours[dateDemandee.weekday()]
        self.dateDemandee = dateDemandee
        self.reservations = Reservation.objects.filter(dateArrivee__lte=dateDemandee).filter(
            dateDepart__gt=dateDemandee).select_related("client").prefetch_related(
            "chambresAssignees").prefetch_related("client__arrhe_set").select_related("client__tourOperateur")
        totalChambres = set([ch for ch in Chambre.objects.all()])
        self.menages = self.reservations.filter(dateDepart__gt=dateDemandee).filter(
            dateArrivee__lt=dateDemandee).select_related("client").prefetch_related(
            "chambresAssignees").prefetch_related("client__arrhe_set").select_related("client__tourOperateur")

        self.blancs = Reservation.objects.filter(dateDepart=dateDemandee).select_related("client").prefetch_related(
            "chambresAssignees").prefetch_related("client__arrhe_set").select_related("client__tourOperateur")

        arriv = Reservation.objects.filter(dateArrivee=dateDemandee).select_related("client").prefetch_related(
            "chambresAssignees").prefetch_related("client__arrhe_set").select_related("client__tourOperateur")

        res = [x for x in self.reservations]
        res.sort(key=lambda r: r.client.nom.lower())
        self.resas = res
        self.nbMenages = 0
        self.nbMenageTheorique = 0
        self.nbMenageDortoir = 0
        for r in self.menages:
            self.nbMenages += len(list(r.chambresAssignees.all()))
            self.nbMenageTheorique += r.nbCh()
            self.nbMenageDortoir += r.placesDortoir
        utilises = []
        self.nbDortoir = self.nbCh = self.nbSingle = self.nbDouble = self.nbTwin = self.nbTriples = self.nbQuadruples = self.nbQuintuples = 0
        self.todo = 0
        self.nbPlacesLibreDortoir = 22
        self.chambresReservees = 0

        for o in self.reservations:
            utilises.extend([x for x in o.chambresAssignees.all()])
            self.chambresReservees += o.nbCh()
            self.nbCh += o.chambres
            self.todo += o.chAAssigner()
            self.nbSingle += o.chambresSingle
            self.nbDouble += o.chambresDoubles
            self.nbTwin += o.chambresTwin
            self.nbTriples += o.chambresTriples
            self.nbQuadruples += o.chambresQuadruples
            self.nbQuintuples += o.chambresQuintuples
            self.nbDortoir += o.placesDortoir
        self.error = getDoublons(utilises)
        self.nbPlacesLibreDortoir -= self.nbDortoir
        self.nbAll = self.nbCh + self.nbSingle + self.nbDouble + self.nbTwin + self.nbTriples + self.nbQuadruples + self.nbQuintuples
        self.utilisesSet = set(utilises)
        self.libre = totalChambres - self.utilisesSet
        self.libreStr = ""
        self.tableauLibres = {}
        for ch in self.libre:
            dest = ch.description()
            if dest in self.tableauLibres:
                self.tableauLibres[dest] += 1
            else:
                self.tableauLibres[dest] = 1
            resas = ch.reservation_set.filter(dateArrivee__gt=dateDemandee)
            if len(resas) < 1:
                ch.occupe = ""
            else:
                ch.occupe = resas[0]
                for i in range(1, len(resas)):
                    resa2 = resas[i]
                    if resa2.dateArrivee < ch.occupe.dateArrivee:
                        ch.occupe = resa2
            self.libreStr += ch.nom
            if ch.occupe:
                self.libreStr += " " + str((ch.occupe.dateArrivee - dateDemandee).days) + " jours"
            self.libreStr += " \n"
        self.libre = list(self.libre)
        self.libre.sort(key=lambda c: c.nom)

        self.nbBlancs = 0
        self.nbBlancsTheoriques = 0
        self.nbBlancsDortoir = 0
        for r in self.blancs:
            self.nbBlancs += len(list(r.chambresAssignees.all()))
            self.nbBlancsTheoriques += r.nbCh()
            self.nbBlancsDortoir += r.placesDortoir

        self.arrivees = (list(arriv))
        self.arrivees.sort(key=lambda a: 1 if a.arrives else -1)

        dep = (list(self.blancs))
        dep.sort(key=lambda a: 1 if a.partis else (0 if a.aEtePrepare else -1))
        self.departs = dep

        self.nouveaux = set(self.arrivees)

        self.changements = []
        for resaDep in self.blancs:
            for resaArr in self.arrivees:
                if resaDep.client.id == resaArr.client.id:
                    self.changements.append((resaDep, resaArr))
                    if resaDep in self.departs and resaDep.nbCh == resaArr.nbCh:
                        self.departs.remove(resaDep)
                    self.nouveaux = self.nouveaux - set([resaArr])

        anciensQuiChangent = set([s for r, s in self.changements])

        self.repas = repas.faisStatsRepasSoir(self.dateDemandee, self.nouveaux, anciensQuiChangent, self.menages,
                                              list(self.reservations))

        self.total = self.repas.total.total


class InfoJour:
    pass


class JourForm(forms.Form):
    resa = forms.CharField()
    date = forms.DateField(widget=forms.HiddenInput, required=False)


def chopeNumeroDevant(st):
    i = 0
    while st[i:i + 1].isdigit():
        i += 1
    if i == 0:
        return None, st
    nb = int(st[0:i])
    st = st[i:]
    return nb, st


# def chopeNumeroDevant(st):
#	dec=1
#	nb=0
#	while st[0:1].isdigit():
#		nb=nb*dec
#		dec=dec*10
#		nb+=int(st[0:1])
#		st=st[1:]
#	return nb,st

def choppeChamps(resa):
    nb, resa = chopeNumeroDevant(resa)
    if nb == 0 or not nb:
        return False, resa, None
    Single = Double = Twin = Dortoir = Triple = Quadruple = Quintuple = indef = Option = 0
    NbNuits = 1
    resa = resa.strip()
    if resa[0:2] == "ch":
        resa = resa[2:]
        resa = resa.strip()
        if resa[0:1] == "x":
            resa = resa[1:]
            resa = resa.strip()
            ta = int(resa[0:1])
            resa = resa[1:]
            resa = resa.strip()
            if ta == 1:
                Single = nb
            elif ta == 3:
                Triple = nb
            elif ta == 4:
                Quadruple = nb
            elif ta == 5:
                Quintuple = nb
            elif ta == 2:
                if resa.startswith("lit"):
                    Twin = nb
                    resa = resa[3:]
                    if resa[0:1] == "s":
                        resa = resa[1:]
                else:
                    Double = nb
        else:
            resa = resa.strip()
            indef = nb
    elif resa.startswith("dortoir"):
        resa = resa[7:]
        resa = resa.strip()
        Dortoir = nb
    elif resa[0:1] == "n":
        resa = resa[1:]
        resa = resa.strip()
        NbNuits = nb
    elif resa[0:1] == "j":
        resa = resa[1:]
        resa = resa.strip()
        Option = nb

    ok = False
    if Single + Double + Twin + Dortoir + indef + Triple + Quadruple + Quintuple + NbNuits + Option - 1 > 0:
        ok = True
    # print "ok:",ok
    resa = resa.strip()
    return ok, resa, [Single, Double, Twin, Dortoir, Triple, Quadruple, Quintuple, indef, NbNuits, Option]


def parseEtAjouteResa(jour, resa):
    resa = resa.strip()

    ok, resa, ll = choppeChamps(resa)
    lls = []

    while ok:
        lls.append(ll)
        ok, resa, ll = choppeChamps(resa)

    resa = resa.strip()
    if not resa:
        return
    c = Client(nom=resa)
    c.save()
    nbMaxNuits = 1
    nOption = 0
    r = Reservation(dateArrivee=jour, dateDepart=jour + timedelta(1), client=c)
    r.save()
    for ll in lls:
        [Single, Double, Twin, Dortoir, Triple, Quadruple, Quintuple, indef, NbNuits, Option] = ll
        if NbNuits > nbMaxNuits:
            nbMaxNuits = NbNuits
        r.chambres += indef
        nOption += Option
        r.chambresSingle += Single
        r.chambresDoubles += Double
        r.chambresTriples += Triple
        r.chambresQuadruples += Quadruple
        r.chambresQuintuples += Quintuple
        r.chambresTwin += Twin
        r.placesDortoir += Dortoir
        r.save()
    r.dateDepart = jour + timedelta(nbMaxNuits)
    if nOption > 0:
        r.client.optionJusquau = r.dateArrivee - timedelta(nOption)
        r.client.save()
    else:
        r.client.optionJusquau = date.today() + timedelta(15)
        r.client.save()
    r.save()


@login_required
def vuePapierProchaine(request):
    tod = date.today()
    fin = date(tod.year, 11, 16)
    if tod > fin:
        deb = date(tod.year + 2, 2, 27)
        fin = date(tod.year + 2, 11, 16)
    else:
        deb = date(tod.year + 1, 2, 27)
        fin = date(tod.year + 1, 11, 16)
    return HttpResponseRedirect(reverse("vuePapier", args=[deb.year, deb.month, deb.day, fin.year, fin.month, fin.day]))


@login_required
def vuePapierCourante(request):
    to = date.today()
    fin = date(to.year, 11, 16)
    if to > fin:
        tod = date(to.year + 1, 2, 27)
        fin = date(to.year + 1, 11, 16)
    elif to < date(to.year, 3, 1):
        tod = date(to.year, 3, 1)
    else:
        tod = date.today()
    return HttpResponseRedirect(reverse("vuePapier", args=[tod.year, tod.month, tod.day, fin.year, fin.month, fin.day]))


@login_required
def faireConfiance(request, annee, mois, jour, anneeF, moisF, jourF, idConfiance):
    c = Client.objects.get(pk=idConfiance)
    c.aConfiance = True
    c.save()
    return HttpResponseRedirect(reverse("etatResas", args=[annee, mois, jour, anneeF, moisF, jourF]))


@login_required
def etatResas(request, annee, mois, jour, anneeF, moisF, jourF):
    return vuePapier(request, annee, mois, jour, anneeF, moisF, jourF, etatResas=True)


@login_required
def vuePapier(request, annee, mois, jour, anneeF, moisF, jourF, etatResas=False):
    if request.method == 'POST':  # If the form has been submitted...
        form = JourForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # print str(form)
            r = form.cleaned_data["resa"]
            j = form.cleaned_data["date"]
            # print r,j
            notOk = parseEtAjouteResa(j, r)
            return HttpResponseRedirect(
                '/chambres/vuePapier/%s/%s/%s/%s/%s/%s#%s' % (annee, mois, jour, anneeF, moisF, jourF, j.isoformat()))

    from .joursFerie import estferie

    dateDeb = date(int(annee), int(mois), int(jour))
    dateFin = date(int(anneeF), int(moisF), int(jourF))

    resas = Reservation.objects.filter(dateArrivee__gte=dateDeb).filter(dateDepart__lte=dateFin).select_related(
        "client", "client__tourOperateur").prefetch_related("client__arrhe_set", "client__arrhe_set__paiement_set")
    resasLimitesAvant = Reservation.objects.filter(dateArrivee__lt=dateDeb).filter(dateDepart__gt=dateDeb).filter(
        dateDepart__lte=dateFin).select_related("client", "client__tourOperateur").prefetch_related("client__arrhe_set",
                                                                                                    "client__arrhe_set__paiement_set")

    resasLimitesApres = Reservation.objects.filter(dateArrivee__lte=dateFin).filter(dateDepart__gt=dateFin).filter(
        dateArrivee__gte=dateDeb).select_related("client", "client__tourOperateur").prefetch_related(
        "client__arrhe_set", "client__arrhe_set__paiement_set")

    resasLimitesAvantApres = Reservation.objects.filter(dateArrivee__lt=dateDeb).filter(
        dateDepart__gt=dateFin).select_related("client", "client__tourOperateur").prefetch_related("client__arrhe_set",
                                                                                                   "client__arrhe_set__paiement_set")

    if etatResas:
        allResas = set(resas)
        allResas.update(resasLimitesApres)
        allResas.update(resasLimitesAvantApres)
        resas = []
        for r in allResas:
            if r.client.tourOperateur == None and r.client.optionJusquau == None and not r.client.arrhesVersees():
                resas.append(r)
        resas = sorted(resas, key=lambda r: r.client.aConfiance)
        return render_to_response('chambres/etatResas.html', {"resas": resas})
    dico = {}
    for i in range(0, (dateFin - dateDeb).days + 1):
        dico[dateDeb + timedelta(i)] = []

    for r in resasLimitesAvant:
        #		print "av",r.client.nom,r
        for i in range((r.dateDepart - dateDeb).days):
            dico[dateDeb + timedelta(i)].append(r)

    for r in resasLimitesApres:
        #		print "ap",r.client.nom,r
        for i in range((dateFin - r.dateArrivee).days + 1):
            dico[dateFin - timedelta(i)].append(r)

    for r in resasLimitesAvantApres:
        #		print "avap",r.client.nom,r
        for i in range((dateFin - dateDeb).days + 1):
            dico[dateDeb + timedelta(i)].append(r)

    for r in resas:
        for i in range((r.dateDepart - r.dateArrivee).days):
            dico[r.dateArrivee + timedelta(i)].append(r)

    jours = sorted(dico.keys())
    tout = []
    for j in jours:
        resas = dico[j]
        jour = InfoJour()
        jour.jour = j
        jour.id = (j - timedelta(4)).isoformat()
        jour.resas = sorted(resas, key=lambda r: r.client.nom.lower())
        jour.tot = sum(r.nbCh() for r in resas)
        jour.totSures = sum(
            r.nbCh() for r in resas if ((not r.client.optionJusquau) and (not "allotement" in r.client.nom)))
        jour.nbDortoir = sum(r.placesDortoir for r in resas)
        jour.form = JourForm({'resa': "1chx2", 'date': j, 'info': "algiht"})

        d = j.weekday()
        if d == 5 or d == 6:
            jour.ferie = True
        else:
            jour.ferie = False
        ferie = estferie(j)
        if ferie:
            jour.ferie = True
            jour.raison = ferie

        tout.append(jour)

    # for i in range(0,(dateFin-dateDeb).days+1):
    #		d=dateDeb+timedelta(i)

    return render_to_response('chambres/vuePapier.html', {'jours': tout, 'largeur': (dateFin - dateDeb).days * 210},
                              context_instance=RequestContext(request))


class StatJour:
    def __init__(self, jour):
        self.jour = jour
        self.nbJoursRepas = 0
        self.repas = 0
        self.dej = 0
        self.men = 0

    def addRepas(self, n):
        self.repas += n
        self.nbJoursRepas += 1

    def addPetitDej(self, n):
        self.dej += n

    def addCoefMenage(self, n):
        self.men += n

    def mRepas(self):
        return self.repas / self.nbJoursRepas

    def mDej(self):
        return self.dej / self.nbJoursRepas

    def mMen(self):
        return self.men / self.nbJoursRepas


@login_required
def globalStatPrint(request, annee, mois, jour, anneeF, moisF, jourF):
    return globalStat(request, annee, mois, jour, anneeF, moisF, jourF, imprime=True)


def globalStatFutur(request, annee, mois, jour, anneeF, moisF, jourF):
    return globalStat(request, annee, mois, jour, anneeF, moisF, jourF, imprime=False, futur=True)


def goFutur(request, jours):
    dateDeb = jours[0].dateDemandee
    dateFin = jours[-1].dateDemandee
    listeJours = []
    for i in range((dateFin - dateDeb).days + 1):
        jour = dateDeb + timedelta(i)
        listeJours.append(jour)

    listeTotale = []
    monthList = []
    weekList = []
    for k in range(dateDeb.weekday()):
        weekList.append(None)
    for i in jours:
        if i.dateDemandee.weekday() == 0:
            monthList.append(weekList)
            weekList = []
        weekList.append(i)
    monthList.append(weekList)
    listeTotale.append(monthList)
    return render_to_response('chambres/futur.html', {'an': listeTotale})


@login_required
def globalStat(request, annee, mois, jour, anneeF, moisF, jourF, imprime=False, futur=False):
    dateDeb = date(int(annee), int(mois), int(jour))
    dateFin = date(int(anneeF), int(moisF), int(jourF))
    result = []
    chs = dict([[ch, 0] for ch in Chambre.objects.all()])
    nbCh = len(Chambre.objects.all())
    nbNuitees = 0
    nbRepas = 0

    joursStat = [StatJour(j) for j in jours]
    for i in range(0, (dateFin - dateDeb).days + 1):
        j = dateDeb + timedelta(i)
        res = OneDayStats(j)
        resVeille = OneDayStats(j + timedelta(-1))
        res.painJour = (res.total / 4. + resVeille.total / 4.) + 2  # 1 pain pour 4 le soir et 1 pour 2 le matin
        res.petitDej = resVeille.total
        res.men = (max(res.nbMenages, res.nbMenageTheorique) * 10 / 2 + max(res.nbBlancs,
                                                                            res.nbBlancsTheoriques) * 10) / 10 + (
                                                                                                                     res.nbBlancsDortoir * 100 / 20 * 4 + res.nbMenageDortoir * 100 / 20 * 2) / 100
        for chh in res.utilisesSet:
            chs[chh] = chs[chh] + 1
        result.append(res)
        nbRepas = nbRepas + res.total
        nbNuitees = nbNuitees + len(res.utilisesSet)

        stat = joursStat[j.weekday()]
        stat.addRepas(res.total)
        stat.addCoefMenage(res.men)
        stat.addPetitDej(resVeille.total)

    if futur:
        return goFutur(request, result)
    chambres = list(chs.items())
    #	chambres.sort(lambda (x,xx),(y,yy): yy-xx)
    chTicks = []
    chGraph = []
    for i in range(len(chambres)):
        chGraph.append("[\"" + str(i) + "\"," + str(chambres[i][1]) + "]")
        chTicks.append("{label:\"" + str(chambres[i][0].nom) + "\",v:" + str(i) + "}")

    graph1 = []
    graph2 = []
    xticks = []
    modulo = len(result) / 25
    if modulo == 0:
        modulo = 1
    for i in range(len(result)):
        graph1.append("[\"" + str(i) + "\"," + str(result[i].nbAll) + "]")
        graph2.append("[\"" + str(i) + "\"," + str(result[i].total) + "]")
        if (i % modulo == 0):
            xticks.append(
                "{label:\"" + str(result[i].dateDemandee.day) + "/" + str(result[i].dateDemandee.month) + "\",v:" + str(
                    i) + "}")
        else:
            xticks.append("{label:\"" + "\",v:" + str(i) + "}")
    xticks = ",".join(xticks)
    chTicks = ",".join(chTicks)
    chGraph = ",".join(chGraph)
    graph1 = ",".join(graph1)
    graph2 = ",".join(graph2)
    return render_to_response('chambres/global.html',
                              {'nbNuitees': nbNuitees, 'nbRepas': nbRepas, 'year': annee, 'month': mois, 'day': jour,
                               'result': result, 'graph1': graph1, 'graph2': graph2, 'xticks': xticks,
                               'chTicks': chTicks, 'chGraph': chGraph, 'lenCh': chambres[0][1] + 1,
                               'minCh': chambres[-1][1] - 1, 'joursStat': joursStat, 'imprime': imprime})


@login_required
def globalStatToday(request):
    suiv = datetime.today() + timedelta(30)
    return HttpResponseRedirect(reverse("globalStat",
                                        args=[datetime.today().year, datetime.today().month, datetime.today().day,
                                              suiv.year, suiv.month, suiv.day]))


@login_required
def globalStatTodayPrint(request):
    suiv = datetime.today() + timedelta(30)
    return HttpResponseRedirect(reverse("globalStatPrint",
                                        args=[datetime.today().year, datetime.today().month, datetime.today().day,
                                              suiv.year, suiv.month, suiv.day]))


def datePremiereArrivee(client):
    dateDebut = date(2100, 1, 1)
    for r in client.reservation_set.all():
        if r.dateArrivee < dateDebut:
            dateDebut = r.dateArrivee
    return dateDebut


def faisStat(annee, mois, jour):
    dateDemandee = date(int(annee), int(mois), int(jour))
    o = OneDayStats(dateDemandee)
    o.dans15 = dateDemandee + timedelta(15)
    o.resasOptionnellesDepassees = list(
        Client.objects.filter(optionJusquau__lte=dateDemandee).filter(tourOperateur__isnull=True).exclude(
            nom__icontains="booking").prefetch_related("reservation_set"))

    for c in o.resasOptionnellesDepassees:
        totalNuitees = 0
        for r in c.reservation_set.all():
            totalNuitees += r.nbPersonnes() * r.nbNuits()
        c.moyen = c.gros = False
        if totalNuitees > 10:
            c.gros = True
        elif totalNuitees > 5:
            c.moyen = True

        c.couleur = avoirCouleurSelonQuantite(totalNuitees)

    o.resasOptionnellesDepassees = sorted(o.resasOptionnellesDepassees, key=datePremiereArrivee)

    tToday = taches(dateDemandee, filtrees=True)

    nextDay = dateDemandee + timedelta(1)
    next = str(nextDay.year) + "/" + str(nextDay.month) + "/" + str(nextDay.day)
    prevDay = dateDemandee - timedelta(1)
    prev = str(prevDay.year) + "/" + str(prevDay.month) + "/" + str(prevDay.day)

    prochainsJours = [date.today() + timedelta(i) for i in range(10)]
    if dateDemandee not in prochainsJours:
        prochainsJours = [dateDemandee + timedelta(i - 3) for i in range(10)]

    dico = {'year': annee, 'month': mois,
            'day': jour, 'reservations': o.resas, 'menages': o.menages, 'blancs': o.blancs, 'arrivees': o.arrivees,
            'next': next, 'prev': prev, 'error': o.error, 'libre': o.libre, 'nbCh': o.nbCh, 'nbSingle': o.nbSingle,
            'nbDouble': o.nbDouble, 'nbTwin': o.nbTwin, 'nbTriples': o.nbTriples, 'nbQuadruples': o.nbQuadruples,
            'nbQuintuples': o.nbQuintuples, 'nbAll': o.nbAll, 'nbPlacesLibreDortoir': o.nbPlacesLibreDortoir,
            'nbDortoir': o.nbDortoir, 'nomJour': o.nomJour, 'taches': tToday, 'repas': o.repas,
            'changements': o.changements, 'departs': o.departs, 'prochainsJours': prochainsJours,
            'dateDemandee': dateDemandee, 'oneDayStat': o}
    return dico


def extendedStats(annee, mois, jour):
    auj = date(int(annee), int(mois), int(jour))
    dem = auj + timedelta(1)
    ap = auj + timedelta(2)
    hier = auj - timedelta(1)

    statsAuj = faisStat(annee, mois, jour)
    statsDemain = faisStat(dem.year, dem.month, dem.day)
    statsAp = faisStat(ap.year, ap.month, ap.day)
    statsHier = faisStat(hier.year, hier.month, hier.day)

    statsAuj["demain"] = statsDemain
    statsAuj["apresDemain"] = statsAp
    statsAuj["hier"] = statsHier

    statsAuj["menDem"] = statsDemain["oneDayStat"].nbMenages
    statsAuj["blcDem"] = statsDemain["oneDayStat"].nbBlancs
    statsAuj["menAp"] = statsAp["oneDayStat"].nbMenages
    statsAuj["blcAp"] = statsAp["oneDayStat"].nbBlancs

    import subprocess
    # out= unicode(subprocess.Popen(["/usr/games/fortune","/home/auberge/Programmation/bla/t"], stdout=subprocess.PIPE, env={"LANG":"fr_FR.utf8"}).communicate()[0],"utf8")
    # out= unicode(subprocess.Popen(["/usr/games/fortune","/usr/share/games/fortunes/fr","/home/auberge/Programmation/bla/t"], stdout=subprocess.PIPE, env={"LANG":"fr_FR.utf8"}).communicate()[0],"utf8")
    statsAuj["fortune"] = ""  # out

    return statsAuj


@login_required
def imprimerArrivees(request, annee, mois, jour):
    return render_to_response('chambres/imprimerArrivees.html', faisStat(annee, mois, jour))


def imprimerCh(request, annee, mois, jour):
    return render_to_response('chambres/imprimerCh.html', extendedStats(annee, mois, jour))


@login_required
def imprimerRepas(request, annee, mois, jour):
    return render_to_response('chambres/imprimerRepas.html', extendedStats(annee, mois, jour))


@login_required
def confirmeOpt(request, annee, mois, jour, Rid):
    client = Client.objects.get(pk=Rid)
    client.optionJusquau = None
    client.save()
    return HttpResponseRedirect(reverse("stats", args=[annee, mois, jour]))


@login_required
def plusSemaine(request, annee, mois, jour, Rid):
    client = Client.objects.get(pk=Rid)
    client.optionJusquau = date.today() + timedelta(7)
    client.save()
    return HttpResponseRedirect(reverse("stats", args=[annee, mois, jour]))


@login_required
def stats(request, annee, mois, jour):
    dico = faisStat(annee, mois, jour)
    dico["user"] = request.user
    dico["aujourdhui"] = date.today()
    return render_to_response('chambres/stats.html', dico)


@login_required
def arrive(request, annee, mois, jour, id):
    resa = Reservation.objects.get(pk=id)
    resa.arrives = True
    resa.save()
    return HttpResponseRedirect("/chambres/" + str(annee) + "/" + str(mois) + "/" + str(jour) + "#arrivees")


@login_required
def prepareFacture(request, annee, mois, jour, id):
    resa = Reservation.objects.get(pk=id)
    resa.aEtePrepare = True
    resa.save()
    p = PreparationFacture(resa=resa)
    p.save()
    return HttpResponseRedirect("/chambres/" + str(annee) + "/" + str(mois) + "/" + str(jour) + "#departs")


@login_required
def parti(request, annee, mois, jour, id):
    resa = Reservation.objects.get(pk=id)
    resa.partis = True
    resa.save()
    return HttpResponseRedirect("/chambres/" + str(annee) + "/" + str(mois) + "/" + str(jour) + "#departs")


@login_required
def editClient(request, client):
    if request.method == 'POST':  # If the form has been submitted...
        form = ClientForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/')  # Redirect after POST
    else:

        c = Client.objects.get(pk=client)
        form = ClientForm(instance=c)
        ResaFormSet = modelformset_factory(Reservation, fields=(
            'dateArrivee', 'dateDepart', 'chambres', 'chambresSingle', 'chambresDoubles', 'chambresTwin',
            'placesDortoir',
            'chambresTriples', 'chambresQuadruples', 'chambresQuintuples', 'chambresAssignees'), can_delete=True)
        formset = ResaFormSet(queryset=Reservation.objects.filter(client=c))

    # BookFormSet = inlineformset_factory(Client, Reservation)
    #		formset = BookFormSet(instance=c)

    return render(request, 'chambres/editClient.html', {
        'form': form, 'formset': formset
    })
