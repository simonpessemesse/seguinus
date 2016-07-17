from django.http import HttpResponse
from django.shortcuts import render_to_response
from datetime import datetime, date, timedelta
from menus.models import Journee, JourneePensionComplete


def index(request):
    latest_poll_list = {}  # Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('menus/index.html', {'year': datetime.today().year, 'month': datetime.today().month,
                                                   'day': datetime.today().day})


def semaine(request, annee, mois, jour):
    dateDemandee = date(int(annee), int(mois), int(jour))
    dateLundi = dateDemandee - timedelta(dateDemandee.weekday())
    dateDimanche = dateDemandee + timedelta(6 - dateDemandee.weekday())
    nextSem = dateDemandee + timedelta(7)
    next = str(nextSem.year) + "/" + str(nextSem.month) + "/" + str(nextSem.day)
    prevSem = dateDemandee - timedelta(7)
    prev = str(prevSem.year) + "/" + str(prevSem.month) + "/" + str(prevSem.day)

    # journees = Journee.objects.all()#Poll.objects.all().order_by('-pub_date')[:5]
    journees = Journee.objects.filter(jour__lte=dateDimanche).filter(jour__gte=dateLundi).order_by('jour')
    return render_to_response('menus/semaine.html',
                              {'year': annee, 'month': mois, 'day': jour, 'journees': journees, 'next': next,
                               'prev': prev})


def semainecomplete(request, annee, mois, jour):
    dateDemandee = date(int(annee), int(mois), int(jour))
    dateLundi = dateDemandee - timedelta(dateDemandee.weekday())
    dateDimanche = dateDemandee + timedelta(6 - dateDemandee.weekday())
    nextSem = dateDemandee + timedelta(7)
    next = str(nextSem.year) + "/" + str(nextSem.month) + "/" + str(nextSem.day)
    prevSem = dateDemandee - timedelta(7)
    prev = str(prevSem.year) + "/" + str(prevSem.month) + "/" + str(prevSem.day)

    # journees = Journee.objects.all()#Poll.objects.all().order_by('-pub_date')[:5]
    journees = JourneePensionComplete.objects.filter(jour__lte=dateDimanche).filter(jour__gte=dateLundi).order_by(
        'jour')
    return render_to_response('menus/semaineComplete.html',
                              {'year': annee, 'month': mois, 'day': jour, 'journees': journees, 'next': next,
                               'prev': prev})

# def index(request):
#    return HttpResponse("Hello, world. You're at the poll index.")
