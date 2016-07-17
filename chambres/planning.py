# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from datetime import datetime, date, timedelta
from chambres.models import Chambre, Souci, Client, Reservation, Tache, Amour
from chambres.views import OneDayStats
import colorsys
import random

jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


def faisPlanning(dateDemandee):
    reservations = Reservation.objects.filter(dateArrivee__lte=dateDemandee).filter(
        dateDepart__gt=dateDemandee).prefetch_related("chambresAssignees").select_related("client")
    dico = dict()
    assign = []
    for r in reservations:
        for ch in r.chambresAssignees.all():
            if ch in dico:
                dico[ch].append(r)
            else:
                dico[ch] = [r, ]
        if (r.chAAssigner() > 0):
            assign.append(r)

    return dico, assign


def cell(text):
    return "<td>" + text + "</td>"


def raccourciNom(text):
    t = text
    if len(t) > 6:
        t = t[0:6]
    if text[-1:].isdigit():
        t = t[0:-1] + text[-1:]
    if text.endswith("Haut"):
        t = t[0:-1] + "h"
    if text.endswith("Bas"):
        t = t[0:-1] + "b"
    return t


def cellh(text):
    tooltip = " title=\"" + text + "\""
    t = raccourciNom(text)
    return "<th " + tooltip + " ><small>" + t + "</small></th>"


def cellv(text):
    return "<th ><small>" + text + "</small></th>"


def lienResa(resa, dat=None, ch=None, retourLigne=True):
    ita, li = "", ""
    if resa.client.protege:
        prot = " onclick=\"return protege()\" "
        ita, li = "<i>", "</i>"
    else:
        prot = ""
    nom = resa.client.nom
    if dat:
        tooltip = " title=\"" + nom + " \n" + formateDate(dat) + " \n" + ch.nom + "\""
    else:
        tooltip = " title=\"" + nom + "\""

    if retourLigne:
        rl = "<br />"
    else:
        rl = "&nbsp;"

    if len(resa.client.nom) > 6:
        nom = nom[0:6]
    lr = "<small>" + ita + "<a " + tooltip + " href=\"/admin/chambres/client/" + str(
        resa.client.id) + "\" " + prot + ">" + nom + "</a>" + rl + li + "</small>"
    lc = "<small><small><a href=\"/chambres/magie/" + str(resa.id) + "\" " + prot + ">Magie</a></small></small>"
    return lr + lc


def add0(num):
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)


def formateDate(date):
    return jours[date.weekday()] + " " + add0(date.day) + "/" + add0(date.month)


@login_required
def planningToday(request):
    suiv = datetime.today() + timedelta(31)
    if suiv.month == 12 or (suiv.month == 11 and suiv.month > 16):
        suiv = date(suiv.year, 11, 16)
    return HttpResponseRedirect(
        "/chambres/planning/" + str(datetime.today().year) + "/" + str(datetime.today().month) + "/" + str(
            datetime.today().day) + "/" + str(suiv.year) + "/" + str(suiv.month) + "/" + str(suiv.day))


def cmpResa(x):
    return x.nom.lower()


def hache(nom):
    pass


def calculeCouleursClients(dateDeb, dateFin):
    clients = {}
    for i in range(0, (dateFin - dateDeb).days + 1):
        d = (dateDeb + timedelta(i))
        reservations = Reservation.objects.filter(dateArrivee__lte=d).filter(dateDepart__gt=d).prefetch_related(
            "chambresAssignees").select_related("client")
        for r in reservations:
            if (len(r.chambresAssignees.all()) > 0):
                if not r.client in clients:
                    clients[r.client] = ""

    nbDiff = len(clients)
    coulBase = [40, 180, 240, 300]
    coulBase = [40, 80, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320]
    piscineDeCouleurs = []
    nbParCoulBase = nbDiff / len(coulBase) + 1
    nbParCoulBase = 20
    for c in coulBase:
        for i in range(nbParCoulBase):
            h = c / 360.
            v = 0.1 + i * 0.7 / float(nbParCoulBase)
            #	print s
            s = 1
            #	print (h,s,v)
            (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
            #	print( r,g,b)
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
            #	print "cououc",coull
            if len(coull) < 6:
                print("MER", coull)
            piscineDeCouleurs.append("#" + rr + gg + bb)
        #	random.shuffle(piscineDeCouleurs)

    for i in list(clients.keys()):
        #		print nom, "  ",nom.__hash__()
        hachis = hash(i.nom.lower().strip())
        taillePiscine = len(piscineDeCouleurs)
        clients[i] = piscineDeCouleurs[hachis % taillePiscine]
    #		clients[i]=piscineDeCouleurs.pop()
    #	print piscineDeCouleurs
    return clients


def trieResas(r):
    return str(r.dateArrivee) + "-" + str(1. / r.nbNuits())


def trieChambre(c):
    return -1 * c.note * 10.


def donneUneChambre(resa, libres, nbPers):
    libres = list(libres)
    libres.sort(key=trieChambre)
    for l in libres:
        if l.petitsLits + l.grandsLits * 2 >= nbPers:
            resa.chambresAssignees.add(l)
            resa.save()
            return


@login_required
def attribue(request, annee, mois, jour, anneeF, moisF, jourF):
    dateDeb = date(int(annee), int(mois), int(jour))
    dateFin = date(int(anneeF), int(moisF), int(jourF))
    reservations = Reservation.objects.filter(dateArrivee__gte=dateDeb).filter(dateDepart__lte=dateFin)
    rs = [r for r in reservations]
    rs.sort(key=trieResas)
    st = ""
    for r in rs:
        if r.chAAssigner() > 0 and r.chAssignees() == 0 and r.chambres == 0:
            for n in range(r.chambresQuintuples):
                donneUneChambre(r, OneDayStats(r.dateArrivee).libre, 5)
            for n in range(r.chambresQuadruples):
                donneUneChambre(r, OneDayStats(r.dateArrivee).libre, 4)
            for n in range(r.chambresTriples + r.chambresTwin):
                donneUneChambre(r, OneDayStats(r.dateArrivee).libre, 3)
            for n in range(r.chambresDoubles):
                donneUneChambre(r, OneDayStats(r.dateArrivee).libre, 2)
            for n in range(r.chambresSingle):
                donneUneChambre(r, OneDayStats(r.dateArrivee).libre, 1)
            st += "\n" + str(r) + "<br />"
    return render_to_response('chambres/attribue.html', {'r': st})


@login_required
def planning(request, annee, mois, jour, anneeF, moisF, jourF):
    import locale
    locale.setlocale(locale.LC_ALL, '')
    dateDeb = date(int(annee), int(mois), int(jour))
    dateFin = date(int(anneeF), int(moisF), int(jourF))
    html = "<table border><tr>"
    html += cellh("Date")
    chambres = Chambre.objects.order_by('nom')
    ch = [c for c in chambres]
    ch.sort(key=cmpResa)
    chambres = ch
    for ch in chambres:
        html += cellh(ch.nom)
    html += cellh("Gens a placer")
    html += "</tr>"
    couleurs = calculeCouleursClients(dateDeb, dateFin)
    for i in range(0, (dateFin - dateDeb).days + 1):
        f, assign = faisPlanning(dateDeb + timedelta(i))
        if len(assign) > 0:
            html += "<tr class=\"jaune\">"
        else:
            html += "<tr>"

        html += cellv("<a href=\"/chambres/" + str(dateDeb + timedelta(i)).replace("-", "/") + "\">" + formateDate(
            dateDeb + timedelta(i)) + "</a>")
        for ch in chambres:
            dat = dateDeb + timedelta(i)
            tooltip = "title=\"" + ch.nom + " " + formateDate(dat) + "\""
            if (ch in f):
                if (len(f[ch]) > 1):
                    html += "<td " + tooltip + " class=\"rouge\"> "
                else:
                    html += "<td " + tooltip + " style=\"background-color:" + couleurs[f[ch][0].client] + "\"> "
                for resa in f[ch]:
                    html += lienResa(resa, dat, ch) + "  "
            else:
                html += "<td " + tooltip + " class=\"blanc\"><small>" + raccourciNom(ch.nom) + "</small>"
            html += "</td>"
        html += "<td> "
        for ass in assign:
            html += lienResa(ass, retourLigne=False) + "&nbsp;" + str(ass.chAAssigner()) + "&nbsp;chambre(s) "
        html += "</td>"
        html += "</tr>"

    html += "</table>"
    return render_to_response('chambres/planning.html', {'tableau': html})
