from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from datetime import datetime, date, timedelta, time
from restaurant.models import Resa, Fournisseur, Fourniture, Plat, Menu, ResaResto
from chambres.models import Client


def listeModifResasAssociees(client):
    modifs = ResaResto.objects.filter(reservationEcrasee=client)
    return modifs


@login_required
def supprimeModifResa(request, resaResto_id):
    r = ResaResto.objects.get(pk=resaResto_id)
    r.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def ajouteModifResa(request, client_id):
    client = Client.objects.get(pk=client_id)
    auj = datetime.today().date()
    resas = client.reservation_set.all()
    for r in resas:
        if r.dateArrivee > auj:
            auj = r.dateArrivee
    modif = ResaResto(reservationEcrasee=client, date=auj)
    modif.save()
    return HttpResponseRedirect("/admin/restaurant/resaresto/" + str(modif.id))


@login_required
def plats(request):
    tout = []
    fs = Plat.FONCTION
    for l, n in fs:
        pp = Plat.objects.filter(fonction=l)
        if pp:
            tout.append((n, list(pp)))

    return render_to_response('restaurant/plats.html', {'year': datetime.today().year, 'month': datetime.today().month,
                                                        'day': datetime.today().day, "tout": tout})


@login_required
def index(request):
    fs = Fournisseur.objects.all()
    return render_to_response('restaurant/index.html', {'year': datetime.today().year, 'month': datetime.today().month,
                                                        'day': datetime.today().day, 'fournisseurs': fs})


@login_required
def down(request, fournisseur, produit):
    pro = Fourniture.objects.get(pk=produit)
    pro.note -= 1
    pro.save()
    return HttpResponseRedirect("/restaurant/" + fournisseur)


@login_required
def up(request, fournisseur, produit):
    pro = Fourniture.objects.get(pk=produit)
    pro.note += 1
    pro.save()
    return HttpResponseRedirect("/restaurant/" + fournisseur)


def cmpTu(x):
    return len(x[1])


def cmpFour(x):
    return str(x.note) + ":" + x.nom


def resetFournisseur(num):
    f, fureSorted = getTupleFournisseur(num)
    toDel = []
    for truc in fureSorted:
        if truc.dateDebut:
            toDel.append(truc)
    for t in toDel:
        t.delete()


@login_required
def composeReset(request, lon):
    for i in str(lon):
        resetFournisseur(int(i))
    return compose(request, lon)


@login_required
def compose(request, lon):
    tu = []
    for i in str(lon):
        tupless = getTupleFournisseur(int(i))
        if len(tupless[1]) > 40:
            tu.extend(getTupleFournisseur(int(i), double=True))
        else:
            tu.append(tupless)
    tu.sort(key=cmpTu)
    now = datetime.now()
    return render_to_response('restaurant/fournisseur.html', {"tuples": tu, "print": True, "now": now})


def getTupleFournisseur(fournisseur, double=False):
    f = Fournisseur.objects.get(pk=fournisseur)
    fure = f.fourniture_set.all()
    fureSorted = list(fure)
    fureSorted.sort(key=cmpFour)
    if double:
        moit = fureSorted[0:len(fureSorted) // 2]
        moit2 = fureSorted[len(fureSorted) // 2:]
        return (f, moit), (f, moit2)
    return (f, fureSorted)


@login_required
def fournisseurReset(request, fournisseur):
    resetFournisseur(fournisseur)
    return render_to_response('restaurant/fournisseur.html',
                              {"tuples": [getTupleFournisseur(fournisseur)], "print": False})


@login_required
def fournisseur(request, fournisseur):
    return render_to_response('restaurant/fournisseur.html',
                              {"tuples": [getTupleFournisseur(fournisseur)], "print": False})


class Total():
    pass


def renvoieParNb(resas):
    parNb = {}
    for i in resas:
        if i.nb in parNb:
            parNb[i.nb].append(i)
        else:
            parNb[i.nb] = [i]
    parNbClasse = []
    for a, b in parNb.items():
        parNbClasse.append((a, b))

    # parNbClasse.sort(key=lambda (a,b):a)
    return parNbClasse


@login_required
def jour(request, annee, mois, jour):
    jou = date(int(annee), int(mois), int(jour))
    prochainsJours = [date.today() + timedelta(i) for i in range(10)]
    if jou not in prochainsJours:
        prochainsJours = [jou + timedelta(i - 3) for i in range(10)]
    resas = Resa.objects.filter(jour=jou)

    t = Total()
    t.total = sum([r.nb for r in resas])
    t.totalEnfants = sum([r.nbEnfants for r in resas])
    t.adultes = t.total - t.totalEnfants

    t.totalPensio = sum([r.nb for r in resas if "#" in r.nom])
    t.totalEnfantsPensio = sum([r.nbEnfants for r in resas if "#" in r.nom])
    t.adultesPensio = t.totalPensio - t.totalEnfantsPensio

    t.totalPassage = sum([r.nb for r in resas if "#" not in r.nom])
    t.totalEnfantsPassage = sum([r.nbEnfants for r in resas if "#" not in r.nom])
    t.adultesPassage = t.totalPassage - t.totalEnfantsPassage

    nbResa = len(resas)
    parNbClasse = renvoieParNb(resas)
    pensClass = renvoieParNb([r for r in resas if "#" in r.nom])
    passClass = renvoieParNb([r for r in resas if "#" not in r.nom])
    return render_to_response('restaurant/jour.html',
                              {'year': datetime.today().year, 'month': datetime.today().month, 'day': date.today(),
                               "resas": resas, 'dateDemandee': jou, 'prochainsJours': prochainsJours, 'total': t,
                               "nbResa": nbResa, "parNb": parNbClasse, "pensClass": pensClass, "passClass": passClass})
