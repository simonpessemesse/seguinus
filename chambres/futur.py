# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from datetime import datetime, date, timedelta
from chambres.models import Chambre, Souci, Client, Reservation, Tache, Amour, CacheJour
import calendar


@login_required
def futur(request, annee, mois, jour, anneeF, moisF, jourF):
    dateDeb = date(int(annee), int(mois), int(jour))
    dateFin = date(int(anneeF), int(moisF), int(jourF))
    listeJours = []
    for i in range((dateFin - dateDeb).days + 1):
        jour = dateDeb + timedelta(i)
        listeJours.append(jour)

    listeTotale = []
    monthList = []
    weekList = []
    for k in range(dateDeb.weekday()):
        weekList.append(None)
    for i in listeJours:
        #		if i.day==1:
        #			monthList.append(weekList)
        #			listeTotale.append(monthList)
        #			newWeekList=[]
        #			lenWeekList=len(weekList)
        #			for k in range(lenWeekList,7):
        #				weekList.append(None)
        #			if lenWeekList!=7:
        #				for k in range(0,lenWeekList):
        #					newWeekList.append(None)
        #			monthList=[]
        #			weekList=newWeekList
        if i.weekday() == 0:
            monthList.append(weekList)
            weekList = []
        cache = CacheJour.objects.filter(jour=i)
        if len(cache) < 1:
            cache = CacheJour(jour=i)
            cache.nbCh = 0
            cache.nbTotal = 0
            cache.nbDortoir = 0
            cache.nbanc = 0
            cache.save()
        else:
            cache = cache[0]
        weekList.append(cache)
    monthList.append(weekList)
    listeTotale.append(monthList)
    return render_to_response('chambres/futur.html', {'an': listeTotale})
