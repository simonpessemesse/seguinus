from django.http import HttpResponse, HttpResponseRedirect
import preferences
from django.shortcuts import render_to_response
from datetime import datetime, date, timedelta, time
from collectage.models import Personne, Plage, Employe, HeurePlanifiee, Pourboire, DonPourboire, Individu, Contrat
from easyPoS.models import DonneesEntreprise
from chambres.models import Tache, Entite
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.decorators import login_required


def deltaToHeures(td):
    return td.days * 24 + float(td.seconds) / 60. / 60.


class ResumJour:
    pass


class ResumTotal:
    pass


def formatTimeDeltaInHours(td, verbose=False):
    heures = td.days * 24 + td.seconds / 60. / 60.
    #	return str(heures)
    heuresPleines = int(heures)
    minutes = int((heures - heuresPleines) * 60)
    if minutes < 0:
        minutes = -minutes
    h = str(heuresPleines) + "h" + str(minutes) + "m "
    if verbose:
        if heures < 0:
            h += "de temps en moins (heures qui n'ont pas ete faites qui doivent etre faites)"
        else:
            h += "de temps en plus (en trop a payer)"
    return h


def enHeureDecimales(td):
    return td.days * 24 + td.seconds / 60. / 60.


class EnsembleSemaines:
    def __init__(self):
        self.semaines = []

    def ajouteSemaine(self, semaine):
        self.semaines.append(semaine)

    def joli(self):
        entre35et39 = 0
        entre40et43 = 0
        plusDe44 = 0
        for s in self.semaines:
            hs = s.totalH()
            if hs >= 44:
                entre35et39 += 4
                entre40et43 += 3
                plusDe44 += hs - 43
            elif hs >= 40:
                entre35et39 += 4
                entre40et43 += hs - 39
            elif hs >= 35:
                entre35et39 += hs - 35
        return "entre 35 et 39: " + str(entre35et39) + "\n entre 40 et 43: " + str(
            entre40et43) + "\n plus de 44: " + str(plusDe44)


class Semaine:
    def __init__(self):
        self.jours = []

    def ajouteJour(self, jour):
        self.jours.append(jour)

    def joli(self):
        return "Total des heures pour la semaine se terminant le " + str(self.jours[-1].jour) + " " + str(self.totalH())

    def totalEnTD(self):
        t = timedelta(0)
        for j in self.jours:
            t += j.totalParJour
        return t

    def totalH(self):
        hs = enHeureDecimales(self.totalEnTD())
        return hs


def getDicoResumes(dateDeb, dateFin, contrat=None, imprimer=False):
    jours = [dateDeb + timedelta(i) for i in range(0, (dateFin - dateDeb).days)]
    resumes = []
    resumTotal = ResumTotal()
    resumTotal.repas = 0
    resumTotal.absences = timedelta(0)
    resumTotal.repasAbsents = 0
    resumTotal.total = timedelta(0)
    resumTotal.commentaires = ""
    nbRepas = 0
    semaines = EnsembleSemaines()
    semaineEnCours = Semaine()
    for j in jours:
        r = ResumJour()
        r.jour = j
        if contrat:
            resumTotal.contrat = contrat
            r.heuresPlanifiees = HeurePlanifiee.objects.filter(jour=j).filter(employe=contrat.individu).order_by(
                "heureDebut")
            r.totalParJour = timedelta(0)
            if len(r.heuresPlanifiees) > 0:
                nbRepas += 1
            for h in r.heuresPlanifiees:
                if h.heureDebut or h.heureFin:
                    mDeb = datetime(j.year, j.month, j.day, h.heureDebut.hour, h.heureDebut.minute, h.heureDebut.second)
                    if h.heureFin:
                        mFin = datetime(j.year, j.month, j.day, h.heureFin.hour, h.heureFin.minute, h.heureFin.second)
                        difference = mFin - mDeb
                        r.totalParJour += difference
                        resumTotal.total += difference
                        resumTotal.repas += h.nbRepasPris
                else:
                    if h.absence:
                        resumTotal.absences += timedelta(0, h.tempsTravaille * 60)
                        resumTotal.repasAbsents += h.nbRepasPris
                    else:
                        hhs = timedelta(0, h.tempsTravaille * 60)
                        r.totalParJour += hhs
                        resumTotal.total += timedelta(0, h.tempsTravaille * 60)
                        resumTotal.repas += h.nbRepasPris
                        if j.month == 5 and j.day == 1:  # c'est les 1er mai, on paye double
                            resumTotal.commentaires += str(hhs) + " payees doubles travaillees le 1er mai "
        else:
            r.heuresPlanifiees = HeurePlanifiee.objects.filter(jour=j).order_by("heureDebut")

        semaineEnCours.ajouteJour(r)
        if j.weekday() == 6:  ##dimanche
            semaines.ajouteSemaine(semaineEnCours)
            semaineEnCours = Semaine()
        resumes.append(r)
    if contrat:
        resumTotal.nbHeures = formatTimeDeltaInHours(resumTotal.total)
        resumTotal.heuresSansRepas = formatTimeDeltaInHours(resumTotal.total - timedelta(0, 60 * 30) * resumTotal.repas)
        resumTotal.enCours = ""
        if imprimer:
            return {"resumes": resumes, "emp": contrat, "dd": dateDeb, "df": dateFin - timedelta(1),
                    "semaines": semaines, "today": date.today()}
    return {"resumes": resumes, "resumTotal": resumTotal, "today": date.today(), "semaines": semaines}


def getResumes(annee, mois, jour, anneeF, moisF, jourF, contrat=None, imprimer=False):
    dateDeb = date(int(annee), int(mois), int(jour))
    dateFin = date(int(anneeF), int(moisF), int(jourF))
    dico = getDicoResumes(dateDeb, dateFin, contrat, imprimer)
    listeJours = dico["resumes"]

    listeTotale = []
    monthList = []
    weekList = []
    for k in range(dateDeb.weekday()):
        weekList.append(None)
    for i in listeJours:
        if i.jour.day == 1 and i.jour != dateDeb:
            monthList.append(weekList)
            listeTotale.append(monthList)
            newWeekList = []
            lenWeekList = len(weekList)
            for k in range(lenWeekList, 7):
                weekList.append(None)
            if lenWeekList != 7:
                for k in range(0, lenWeekList):
                    newWeekList.append(None)
            monthList = []
            weekList = newWeekList
        elif i.jour.weekday() == 0:
            monthList.append(weekList)
            weekList = []
        weekList.append(i)
    monthList.append(weekList)
    listeTotale.append(monthList)

    if contrat:
        if imprimer:
            dico["an"] = listeTotale
            return render_to_response('collectage/intervallePrint.html', dico)

    return render_to_response('collectage/intervalle.html', dico)


def copierEmployeDeA(contrat, dateFrom, dateTo):
    heures = HeurePlanifiee.objects.filter(jour=dateFrom).filter(employe=contrat.individu)
    heuresTo = HeurePlanifiee.objects.filter(jour=dateTo).filter(employe=contrat.individu)
    if len(heuresTo) < 1:
        for h in heures:
            nvelle = HeurePlanifiee(jour=dateTo, employe=contrat.individu, heureDebut=h.heureDebut, heureFin=h.heureFin)
            nvelle.save()
    else:
        return "deja des heures de " + str(dateTo)
    return ""


def copierIntervalle(annee, mois, jour, anneeF, moisF, jourF, contrat):
    emp = Individu.objects.get(id=contrat)
    dateDeb = date(int(annee), int(mois), int(jour))
    dateFin = date(int(anneeF), int(moisF), int(jourF))
    jours = [dateDeb + timedelta(i) for i in range(0, (dateFin - dateDeb).days)]
    if dateFin.weekday() != 0:
        return "sa finit pas a lundi"
    if dateDeb.weekday() != 0:
        return "sa commence pas a lundi"
    for d in range(7):
        dateFrom = dateDeb + timedelta(d)
        dateTo = dateFin + timedelta(d)
        ret = copierEmployeDeA(emp, dateFrom, dateTo)
        if ret:
            return ret
    return "<html><body><a href=\"/emploiDuTemps\">Retour au resume</a></body></html>"


def faisPreRemplissage(request, annee, mois, jour, anneeF, moisF, jourF, contrat):
    c = Contrat.objects.get(id=contrat)
    deb = date(int(annee), int(mois), int(jour))
    fin = date(int(anneeF), int(moisF), int(jourF))
    j = []
    if c.congeLundi:
        j.append(1)
    if c.congeMardi:
        j.append(2)
    if c.congeMercredi:
        j.append(3)
    if c.congeJeudi:
        j.append(4)
    if c.congeVendredi:
        j.append(5)
    if c.congeSamedi:
        j.append(6)
    if c.congeDimanche:
        j.append(7)
    joursDeConge = j
    if c.surcroitActiviteWE:
        i = 1
    else:
        i = 0
    if not c.demiJourneeConge:
        moyenneParJour = float(c.nombreHeuresSemaine) / (7. - len(joursDeConge) + i) * 60.
    else:
        moyenneParJour = float(c.nombreHeuresSemaine) / (7. - len(joursDeConge) - 0.5 + i) * 60.
    for i in range((fin - deb).days):
        j = deb + timedelta(i)
        if c.dateDebut and j >= c.dateDebut and ((c.dateFin and j <= c.dateFin) or not c.dateFin):
            if not j.isoweekday() in joursDeConge:
                if c.demiJourneeConge and j.isoweekday() == c.demiJourneeConge:
                    nvelle = HeurePlanifiee(jour=j, employe=c.individu, tempsTravaille=moyenneParJour / 2,
                                            nbRepasPris=1)
                    nvelle.save()
                else:
                    if c.surcroitActiviteWE and j.isoweekday() in [6, 7]:
                        mpj = moyenneParJour + moyenneParJour / 2
                        rep = 2
                    else:
                        mpj = moyenneParJour
                        rep = c.nbRepasJour
                    nvelle = HeurePlanifiee(jour=j, employe=c.individu, tempsTravaille=mpj, nbRepasPris=rep)
                    nvelle.save()


@login_required
def reset(request, annee, mois, jour, anneeF, moisF, jourF, contrat):
    c = Contrat.objects.get(id=contrat)
    deb = date(int(annee), int(mois), int(jour))
    fin = date(int(anneeF), int(moisF), int(jourF))
    faisPreRemplissage(request, annee, mois, jour, anneeF, moisF, jourF, contrat)
    for i in range((fin - deb).days):
        j = deb + timedelta(i)
        hps = HeurePlanifiee.objects.filter(jour=j).filter(employe=c.individu)
        for h in hps:
            h.delete()
    return HttpResponseRedirect(".")


@login_required
def genereTaches(request, annee, mois):
    return moisMail(request, annee, mois, preremplis=False, genereTaches=True)


@login_required
def preremplir(request, annee, mois, jour, anneeF, moisF, jourF, contrat):
    faisPreRemplissage(request, annee, mois, jour, anneeF, moisF, jourF, contrat)
    return HttpResponseRedirect(".")


@login_required
def copierIntervalleEmploye(request, annee, mois, jour, anneeF, moisF, jourF, contrat):
    return HttpResponse(copierIntervalle(annee, mois, jour, anneeF, moisF, jourF, contrat))


@login_required
def intervalleEmployePrint(request, annee, mois, jour, anneeF, moisF, jourF, contrat):
    emp = Contrat.objects.get(id=contrat)
    return getResumes(annee, mois, jour, anneeF, moisF, jourF, contrat=emp, imprimer=True)


@login_required
def intervalleEmploye(request, annee, mois, jour, anneeF, moisF, jourF, contrat):
    emp = Contrat.objects.get(id=contrat)
    return getResumes(annee, mois, jour, anneeF, moisF, jourF, contrat=emp)


@login_required
def intervalle(request, annee, mois, jour, anneeF, moisF, jourF):
    return getResumes(annee, mois, jour, anneeF, moisF, jourF)


def formateDeuxDatesPourAfficher(deb, fin):
    return str(deb.year) + "/" + str(deb.month) + "/" + str(deb.day) + "/" + str(fin.year) + "/" + str(
        fin.month) + "/" + str(fin.day) + "/"


@login_required
def today(request):
    deb = datetime.today()
    fin = deb + timedelta(1)
    hophop = formateDeuxDatesPourAfficher(deb, fin)
    return HttpResponseRedirect(hophop)


class IndividuPourboire:
    def __init__(self, individu, montant):
        self.individu = individu
        self.montant = montant

    def estGrand(self):
        return self.montant * self.montant > 1

    def dizaineInferieure(self):
        diz = int(self.montant - self.montant % 10)
        return diz


def calculePourboires(individu=None):
    if individu:
        dpbs = DonPourboire.objects.all().order_by("-date").filter(individu=individu)
        pbs = Pourboire.objects.all().order_by("-date").filter(individus=individu)
    else:
        dpbs = DonPourboire.objects.all().order_by("-date")
        pbs = Pourboire.objects.all().order_by("-date")

    parPersonne = {}
    for pb in pbs:
        nbPersonnes = len(pb.individus.all())
        montant = pb.montant / nbPersonnes
        for i in pb.individus.all():
            if not i in parPersonne:
                parPersonne[i] = montant
            else:
                parPersonne[i] += montant
    for d in dpbs:
        i = d.individu
        if not i in parPersonne:
            parPersonne[i] = -d.montant
        else:
            parPersonne[i] -= d.montant

    indivs = []
    for i, m in parPersonne.items():
        indiv = IndividuPourboire(i, m)
        if not individu or i == individu:
            indivs.append(indiv)
    indivs = sorted(indivs, key=lambda i: -i.montant)

    return pbs, dpbs, parPersonne, indivs


def chopePbDu(individu):
    pbs, dpbs, parPersonne, indivs = calculePourboires()
    for i, montant in parPersonne.items():
        if i == individu:
            return montant
    raise Exception("individu non trouve")


@login_required
def pbInit(request, individu, don=None):
    i = Individu.objects.get(pk=individu)
    add = ""
    if don:
        montant = int(don)
        add = "../"
    else:
        montant = chopePbDu(i)
    if montant != 0:
        dp = DonPourboire(individu=i, date=datetime.now(), montant=montant)
        dp.save()
    return HttpResponseRedirect(add + ".")


class LigneRegistre:
    def __init__(self, typecontrat, debut, fin, contrat, individu):
        self.typecontrat = typecontrat
        self.debut = debut
        self.fin = fin
        self.emploi = contrat.emploi
        self.contrats = [contrat]
        self.individu = individu

    def peutRajouterCeContrat(self, c):
        if not self.fin or c.dateDebut <= self.fin + timedelta(1):
            self.contrats.append(c)
            if self.fin and c.dateFin:
                if self.fin < c.dateFin:
                    self.fin = c.dateFin
            return True
        return False


def registreDuPersonnel():
    lignes = []
    Ids = Individu.objects.all()
    for i in Ids:
        cs = i.contrat_set.all().order_by("dateDebut")
        ligneEnCours = None
        for c in cs:
            if c.dateDebut:
                if not ligneEnCours:
                    ligneEnCours = LigneRegistre(c.get_typeDuContrat_display(), c.dateDebut, c.dateFin, c, c.individu)
                else:
                    if not ligneEnCours.peutRajouterCeContrat(c):
                        lignes.append(ligneEnCours)
                        ligneEnCours = LigneRegistre(c.get_typeDuContrat_display(), c.dateDebut, c.dateFin, c,
                                                     c.individu)

        if ligneEnCours != None:
            lignes.append(ligneEnCours)
    lignes.sort(key=lambda ligne: ligne.debut)
    return lignes


@login_required
def registre(request):
    lignes = registreDuPersonnel()
    return render_to_response('collectage/registre.html', {"lignes": lignes})


@login_required
def moisCourant(request):
    tod = date.today()
    return HttpResponseRedirect("mois/" + str(tod.year) + "/" + str(tod.month))


class PourComptable:
    pass


lesMois = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre",
           "decembre"]


def rangeContratParIndiv(x):
    return x.individu.nom.lower() + x.individu.prenom.lower()


@login_required
def moisMail(request, annee, mois, preremplis=False, genereTaches=False):
    dd = date(int(annee), int(mois), 1)
    jm = dd - timedelta(1)
    jmPlus = date((date(int(annee), int(mois), 15) + timedelta(30)).year,
                  (date(int(annee), int(mois), 15) + timedelta(30)).month, 1)
    dernierJourMoisPrecedent = date(jm.year, jm.month, jm.day)
    premierJourMoisSuivant = date(jmPlus.year, jmPlus.month, jmPlus.day)
    contrats = Contrat.objects.filter(dateDebut__lt=premierJourMoisSuivant)

    commeDhab = []
    nouvellesEmbauches = []
    extras = []
    finContrats = []
    modifs = []
    pourComptable = []

    for c in contrats:
        if (c.dateFin and c.dateFin > dernierJourMoisPrecedent) or not c.dateFin:
            if c.dateDebut > dernierJourMoisPrecedent:
                if c.dateFin < premierJourMoisSuivant:
                    extras.append(c)
                else:
                    if c.typeDuContrat == "A":
                        modifs.append(c)
                    else:
                        nouvellesEmbauches.append(c)
            else:
                if c.dateFin and c.dateFin < premierJourMoisSuivant:
                    finContrats.append(c)
                elif not c.typeDuContrat == "A":
                    pc = PourComptable()
                    pc.individu = c
                    pc.taux = c.tauxHoraireBrut
                    commeDhab.append(c)
                else:
                    commeDhab.append(c)
    commeDhab.extend(nouvellesEmbauches)
    commeDhab.extend(finContrats)
    commeDhab.extend(extras)
    commeDhab.extend(modifs)
    for m in commeDhab:
        toDel = []
        toAdd = []
        for c in commeDhab:
            if c != m and c.individu == m.individu:
                if m.dateDebut > c.dateDebut:
                    toDel.append(c)
                #				toAdd.append(m)
                #	commeDhab.extend(toAdd)
        for d in toDel:
            commeDhab.remove(d)
    commeDhab.sort(key=rangeContratParIndiv)
    moisP = str(dernierJourMoisPrecedent.year) + "/" + str(dernierJourMoisPrecedent.month)
    moisS = str(premierJourMoisSuivant.year) + "/" + str(premierJourMoisSuivant.month)
    jourP = str(dd.year) + "/" + str(dd.month) + "/" + str(dd.day)
    jourS = moisS + "/1"

    indivs = set()
    for c in commeDhab:
        indivs.add(c.individu)
    if genereTaches:
        for i in indivs:
            asi = Entite.objects.get(pk=30)
            desc = str(i) + " en " + lesMois[int(mois) - 1]
            t = Tache(description=desc, date=date.today())
            t.save()
            t.entite.add(asi)
            t.save()

    for c in commeDhab:
        if preremplis:
            faisPreRemplissage(request, dd.year, dd.month, dd.day, premierJourMoisSuivant.year,
                               premierJourMoisSuivant.month, premierJourMoisSuivant.day, c.id)
        dico = getDicoResumes(dd, premierJourMoisSuivant, contrat=c, imprimer=False)
        resumTotal = dico["resumTotal"]
        asbs = resumTotal.absences.days * 24 * 60 + resumTotal.absences.seconds / 60
        if asbs > 0:
            if asbs > 60:
                resumTotal.absencesJoli = str(asbs / 60) + " heures et " + str(asbs % 60) + " minutes"
            else:
                resumTotal.absencesJoli = str(asbs) + " minutes"
        else:
            resumTotal.absencesJoli = ""

        if c.dateDebut and c.dateFin and (
                    c.dateDebut > dd or c.dateFin < premierJourMoisSuivant or c.nombreHeuresSemaine < 35):
            resumTotal.colH = resumTotal.total.days * 24. + resumTotal.total.seconds / 60. / 60.
        else:
            if c.nombreHeuresSemaine <= 35:
                resumTotal.colH = c.nombreHeuresSemaine * 52 / 12
            else:
                resumTotal.colH = (35. * 52 / 12)
        c.resumTotal = resumTotal
    if preremplis or genereTaches:
        return HttpResponseRedirect(".")

    return render_to_response('collectage/salaireMois.html',
                              {"premier": dd, "hab": commeDhab, "nvx": nouvellesEmbauches, "extras": extras,
                               "finsContrats": finContrats, "modifs": modifs, "moisP": moisP, "moisS": moisS,
                               "jourP": jourP, "jourS": jourS})


@login_required
def preremplistout(request, annee, mois):
    return moisMail(request, annee, mois, preremplis=True)


def dateDernierContrat(i):
    contrats = i.contrat_set.all()
    dernier = date(1969, 1, 1)
    for c in contrats:
        if c.dateDebut and c.dateDebut > dernier:
            dernier = c.dateDebut
        if c.dateDebut and not c.dateFin:
            dernier = date.today() - timedelta(100)
    return str(dernier.year) + str(dernier.month) + str(dernier.day)


@login_required
def dif(request):
    contrats = Contrat.objects.filter(dateFin__isnull=True)
    return render_to_response('collectage/dif.html', {'contrats': contrats, 'jour': date(datetime.today().year, 1, 1)})


@login_required
def rhIndex(request):
    ins = Individu.objects.all()
    ins = sorted(ins, key=dateDernierContrat, reverse=True)
    contrats = Contrat.objects.all().order_by('id')
    return render_to_response('collectage/individu_list.html', {'object_list': ins, 'contrats': contrats})


@login_required
def ficheHeures(request, numContrat):
    cc = Contrat.objects.get(pk=numContrat)
    ent = DonneesEntreprise.objects.get(pk=preferences.ENTREPRISE)
    Vraideb = cc.dateDebut
    Vraifin = cc.dateFin
    if not Vraideb or date.today() - timedelta(90) > Vraideb:
        Vraideb = date.today() - timedelta(149)
    if not Vraifin:
        Vraifin = date.today() + timedelta(14 * 7)
    deb = Vraideb - timedelta(Vraideb.weekday())
    fin = Vraifin + timedelta(7 - Vraifin.weekday())
    sems = []
    semaine = []
    for i in range((fin - deb).days):
        jour = deb + timedelta(i)
        semaine.append(jour)
        if jour.weekday() == 6:
            sems.append(semaine)
            semaine = []

    return render_to_response('collectage/ficheHeures.html', {'contrat': cc, 'semaines': sems, 'entreprise': ent})


@login_required
def ficheMutuelle(request, numContrat):
    cc = Contrat.objects.get(pk=numContrat)
    ent = DonneesEntreprise.objects.get(pk=preferences.ENTREPRISE)
    return render_to_response('collectage/ficheMutuelle.html', {'object': cc, 'entreprise': ent})


@login_required
def ficheNouvelleEmbauche(request, numContrat):
    cc = Contrat.objects.get(pk=numContrat)
    ent = DonneesEntreprise.objects.get(pk=preferences.ENTREPRISE)
    return render_to_response('collectage/ficheNouvelleEmbauche.html', {'object': cc, 'entreprise': ent})


@login_required
def contrat(request, numContrat):
    cc = Contrat.objects.get(pk=numContrat)
    ent = DonneesEntreprise.objects.get(pk=preferences.ENTREPRISE)

    return render_to_response('collectage/' + cc.get_typeDuContrat_display() + '.html',
                              {'object': cc, 'entreprise': ent})


@login_required
def pb(request, individu=None):
    if not individu:
        pbs, dpbs, parPersonne, indivs = calculePourboires()
    else:
        i = Individu.objects.get(id=individu)
        pbs, dpbs, parPersonne, indivs = calculePourboires(i)
    return render_to_response('collectage/pb.html', {'pb': pbs, 'pp': parPersonne, 'dons': dpbs, 'indivs': indivs})


@login_required
def emploiDuTemps(request):
    deb = datetime.today()
    debutMoisCourant = datetime(deb.year, deb.month, 1)
    debutMoisPrecedent = datetime((debutMoisCourant - timedelta(15)).year,
                                  (debutMoisCourant - timedelta(15)).month, 1)
    debutMoisSuivant = datetime((debutMoisCourant + timedelta(32)).year,
                                (debutMoisCourant + timedelta(32)).month, 1)
    debutMoisSuivantSuivant = datetime((debutMoisCourant + timedelta(64)).year,
                                       (debutMoisCourant + timedelta(64)).month, 1)
    if (deb.weekday() > 0):
        deb = deb - timedelta(deb.weekday())
    debSemProchaine = deb + timedelta(7)
    finSemProchaine = deb + timedelta(14)
    finSem = deb + timedelta(7)
    preDefinis = []
    curNext = formateDeuxDatesPourAfficher(deb, finSemProchaine)
    prochaine = formateDeuxDatesPourAfficher(debSemProchaine, finSemProchaine)
    cur = formateDeuxDatesPourAfficher(deb, finSem)
    moisPrecedent = formateDeuxDatesPourAfficher(debutMoisPrecedent, debutMoisCourant)
    moisCourant = formateDeuxDatesPourAfficher(debutMoisCourant, debutMoisSuivant)
    moisSuivant = formateDeuxDatesPourAfficher(debutMoisSuivant, debutMoisSuivantSuivant)
    preDefinis.append(("Semaine courante", cur))
    preDefinis.append(("Aujourd'hui", "today"))
    preDefinis.append(("Semaine prochaine", prochaine))
    preDefinis.append(("Semaine precedente", formateDeuxDatesPourAfficher(deb - timedelta(7), deb)))
    preDefinis.append(("Semaine courante+semaineProchaine", curNext))
    preDefinis.append(("Mois precedent", moisPrecedent))
    preDefinis.append(("Mois courant", moisCourant))
    preDefinis.append(("Mois suivant", moisSuivant))

    deb = deb - timedelta(7 * 14)
    for i in range(20):
        dd = deb + timedelta(i * 7)
        ff = dd + timedelta(7)
        aAjouter = formateDeuxDatesPourAfficher(dd, ff)
        preDefinis.append(
            ("Semaine du " + str(dd.day) + "/" + str(dd.month) + " au " + str(ff.day) + "/" + str(ff.month), aAjouter))

    return render_to_response('collectage/emploiDuTemps.html', {"preDefinis": preDefinis})
