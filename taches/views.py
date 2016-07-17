from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from datetime import datetime, date, timedelta
from chambres.models import Chambre, Souci, Client, Reservation, Tache, TacheLog, Amour, Entite
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django import forms


def cmpEx(x):
    clef = ""
    if x.priorite == "B":
        clef += "1"
    elif x.priorite == "M":
        clef += "2"
    else:
        clef += "3"
    clef += str(x.date)
    clef += str(x.modification)
    return clef


def montrerTache(t):
    entites = t.entite.all()
    if len(entites) < 1:
        return True
    for e in entites:
        if not e.cacherPremierPlan:
            return True
    return False


def ajouterTacheSiTacheRecurrente(jour):
    jourTache = [Tache.objects.filter(chaqueLundi=True).prefetch_related("entite"),
                 Tache.objects.filter(chaqueMardi=True).prefetch_related("entite"),
                 Tache.objects.filter(chaqueMercredi=True).prefetch_related("entite"),
                 Tache.objects.filter(chaqueJeudi=True).prefetch_related("entite"),
                 Tache.objects.filter(chaqueVendredi=True).prefetch_related("entite"),
                 Tache.objects.filter(chaqueSamedi=True).prefetch_related("entite"),
                 Tache.objects.filter(chaqueDimanche=True).prefetch_related("entite")
                 ]
    taches = jourTache[jour.weekday()]
    #	print "debut",taches
    if jour == date.today():
        toutes = []
        for t in taches:
            tToday = Tache.objects.filter(tachePapa=t).filter(date=jour)
            if not tToday and t.rappel:
                tacheACreer = Tache(description=t.description, date=jour, rappel=t.rappel, tachePapa=t)
                tacheACreer.save()
                toutes.append(tacheACreer)
            else:
                for t in tToday:
                    if not t.executee:
                        toutes.append(t)
        return set(toutes)
    else:
        return set(taches)


def taches(jour, entite=None, filtrees=False, periodiques=False):
    thisDay = set()
    thisDay = thisDay | ajouterTacheSiTacheRecurrente(jour)

    if entite:
        thisDay = thisDay | set(entite.tache_set.filter(executee=False).filter(date__lte=jour))
        thisDay = [t for t in thisDay if entite in t.entite.all()]
    elif periodiques:
        jourTache = [Tache.objects.filter(chaqueLundi=True).prefetch_related("entite"),
                     Tache.objects.filter(chaqueMardi=True).prefetch_related("entite"),
                     Tache.objects.filter(chaqueMercredi=True).prefetch_related("entite"),
                     Tache.objects.filter(chaqueJeudi=True).prefetch_related("entite"),
                     Tache.objects.filter(chaqueVendredi=True).prefetch_related("entite"),
                     Tache.objects.filter(chaqueSamedi=True).prefetch_related("entite"),
                     Tache.objects.filter(chaqueDimanche=True).prefetch_related("entite")
                     ]
        thisDay = set()
        for jt in jourTache:
            thisDay = thisDay | set(jt)

    else:
        thisDay = thisDay | set(Tache.objects.filter(executee=False).filter(date__lte=jour).prefetch_related("entite"))

        if filtrees:
            toRemove = []
            for t in thisDay:
                if not montrerTache(t) or (t.expiration and t.expiration < jour):
                    toRemove.append(t)
            for t in toRemove:
                thisDay.remove(t)

    listTaches = list(thisDay)
    listTaches.sort(key=cmpEx, reverse=True)

    return listTaches


@login_required
def today(request):
    tod = date.today()
    return HttpResponseRedirect("/taches/{0}/{1}/{2}/0".format(tod.year, tod.month, tod.day))


@login_required
def resumePrint(request, annee, mois, jour, entite=None):
    if entite == "0":
        entite = None
    return resume(request, annee, mois, jour, entite, imprime=True)


@login_required
def resume(request, annee, mois, jour, entite=None, imprime=False):
    dateDemandee = date(int(annee), int(mois), int(jour))
    if ("Recent" in request.GET):
        li = list(Tache.objects.filter(executee=True).order_by('-modification')[:600])
        tToday = (li)
    elif ("Modif" in request.GET):
        lis = list(TacheLog.objects.order_by('-creation')[:600])
        li = []
        for i in lis:
            li.append(i.tache)
        tToday = (li)
    else:
        if entite and entite != "999999999":
            entite = Entite.objects.get(pk=entite)
        if entite == "999999999":
            tToday = taches(dateDemandee, filtrees=True, periodiques=True)
        else:
            tToday = taches(dateDemandee, entite=entite, filtrees=True)

    entites = list(Entite.objects.all())
    toDel = []
    for e in entites:

        tts = e.tache_set.filter(executee=False).filter(date__lte=dateDemandee)
        #		if e.id in [13,11,6]:
        #			prog=Entite.objects.get(pk=14)
        #			for t in tts:
        #				t.entite.add(prog)
        #				t.save()
        hautes = tts.filter(priorite='H')
        moy = tts.filter(priorite='M')
        bas = tts.filter(priorite='B')
        e.h = len(hautes)
        e.m = len(moy)
        e.b = len(bas)
        if len(tts) < 1:
            toDel.append(e)
    for toD in toDel:
        entites.remove(toD)

    if not entite:
        tachesASupp = []
        for t in tToday:
            if len(t.entite.all()) > 0 or (t.expiration and t.expiration < dateDemandee):
                tachesASupp.append(t)
        for tt in tachesASupp:
            tToday.remove(tt)

    nextDay = dateDemandee + timedelta(1)
    next = str(nextDay.year) + "/" + str(nextDay.month) + "/" + str(nextDay.day)
    prevDay = dateDemandee - timedelta(1)
    prev = str(prevDay.year) + "/" + str(prevDay.month) + "/" + str(prevDay.day)
    prochainsJours = [date.today() + timedelta(i) for i in range(5)]
    if dateDemandee not in prochainsJours:
        prochainsJours = [dateDemandee + timedelta(i - 3) for i in range(5)]
    if entite and not ("Recent" in request.GET) and not ("Modif" in request.GET) and entite != "999999999":
        cat = entite.id
    elif entite == "999999999":
        cat = 999999999
    else:
        cat = 0
    temp = "resume.html"
    if imprime:
        temp = "resumeImprime.html"
    return render_to_response('taches/' + temp,
                              {'year': annee, 'month': mois, 'entites': entites, 'day': jour, 'next': next,
                               'prev': prev, 'date': dateDemandee, 'taches': tToday, 'prochainsJours': prochainsJours,
                               'dateDemandee': dateDemandee, 'cat': cat})


@login_required
def report(request, annee, mois, jour, id, cat):
    t = Tache.objects.get(pk=id)
    demain = date.today() + timedelta(1)
    t.date = demain
    t.executee = False
    t.save()
    return HttpResponseRedirect("/taches/" + str(annee) + "/" + str(mois) + "/" + str(jour) + "/" + str(cat))


@login_required
def delId(request, annee, mois, jour, id, cat):
    t = Tache.objects.get(pk=id)
    t.executee = True
    t.save()
    return HttpResponseRedirect("/taches/" + str(annee) + "/" + str(mois) + "/" + str(jour) + "/" + str(cat))


@login_required
def aSuivre(request, annee, mois, jour, id, cat):
    t = Tache.objects.get(pk=id)
    t.entite.clear()
    t.entite.add(Entite.objects.get(pk=17))  # A suivre
    t.save()
    return HttpResponseRedirect("/taches/" + str(annee) + "/" + str(mois) + "/" + str(jour) + "/" + str(cat))


@login_required
def down(request, annee, mois, jour, id, cat):
    t = Tache.objects.get(pk=id)
    if t.priorite == 'M':
        t.priorite = 'B'
    elif t.priorite == 'H':
        t.priorite = 'M'
    t.save()
    return HttpResponseRedirect("/taches/" + str(annee) + "/" + str(mois) + "/" + str(jour) + "/" + str(cat))


@login_required
def up(request, annee, mois, jour, id, cat):
    t = Tache.objects.get(pk=id)
    if t.priorite == 'B':
        t.priorite = 'M'
    elif t.priorite == 'M':
        t.priorite = 'H'
    else:
        t.date = date.today()
        t.modification = datetime.now()

    t.save()
    return HttpResponseRedirect("/taches/" + str(annee) + "/" + str(mois) + "/" + str(jour) + "/" + str(cat))
