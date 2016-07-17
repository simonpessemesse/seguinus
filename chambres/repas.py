from datetime import datetime, date, timedelta, time
import re
import collections
from chambres.models import Reservation
from restaurant.models import ResaResto


def trouveNomSpecialSiIlExiste(nom):
    if "mariage" in nom:
        nom = "mariage"
    if "~" in nom:
        [a, b] = nom.split("~", 1)
        nomGroupe = ""
        i = 0
        while (i < len(b) and b[i].isspace()):
            i += 1
        while (i < len(b) and not b[i].isspace()):
            nomGroupe += b[i]
            i += 1
        nom = nomGroupe
    return nom


class Repas:
    pass


class ReservationDeResto:
    def __init__(self, nom, nbPersonnes, chambresAssignees, dateDepart, dateArrivee, nbEnfants=0):
        self.nom = nom
        self.nbPersonnes = nbPersonnes
        self.chambresAssignees = chambresAssignees
        self.dateDepart = dateDepart
        self.dateArrivee = dateArrivee
        self.nbEnfants = nbEnfants


def chi(a):
    s = str(a)
    return int(re.search(r'\d+', s).group())


class StatRepas():
    def __init__(self, resas, booking=False, nodp=False):
        dicParNom = {}
        for resa in resas:
            nom = resa.nom.lower().strip()

            if booking:
                if "booking" in nom and (("nodp" in nom) or ("no dp" in nom)):
                    onRajoute = True
                else:
                    onRajoute = False
            else:
                if nom.find("nodp") < 0 and nom.find(
                        "no dp") < 0 and "allotement" not in nom:  # si il n'y a pas no dp (pas de demi pension) dans le nom
                    onRajoute = True
                else:
                    onRajoute = False
            if nodp:
                if "nodp" in nom or "no dp" in nom:
                    onRajoute = True
                else:
                    onRajoute = False

            if onRajoute:
                nom = trouveNomSpecialSiIlExiste(nom)
                if nom in dicParNom:
                    (nb, ch, vieillard, depart, enfants) = dicParNom[nom]
                    nb += resa.nbPersonnes
                    ch.extend(list(resa.chambresAssignees))
                    if (depart < resa.dateDepart):
                        depart = resa.dateDepart
                    if (vieillard > resa.dateArrivee):
                        vieillard = resa.dateArrivee
                    dicParNom[nom] = (nb, ch, vieillard, depart, enfants + resa.nbEnfants)
                else:
                    dicParNom[nom] = (
                        resa.nbPersonnes, list(resa.chambresAssignees), resa.dateArrivee, resa.dateDepart,
                        resa.nbEnfants)
        dicParNb = {}
        total = 0
        totalKid = 0
        for k, (v, x, vieil, depart, enfants) in dicParNom.items():
            total += v
            if enfants > 0:
                v = str(v) + "(" + str(enfants) + ")"
                totalKid += enfants
            if v in dicParNb:
                dicParNb[v].append((k, x, vieil, depart, enfants))
            else:
                dicParNb[v] = [(k, x, vieil, depart, enfants), ]

        newDic = collections.OrderedDict()
        for i in sorted(dicParNb.keys(), key=chi):
            newDic[i] = dicParNb[i]
        dicParNb = newDic

        self.stat = dicParNb
        self.total = total
        self.totalKid = totalKid


def essaieDenlever(liste, resa):
    if resa in liste:
        liste.remove(resa)


def convertisResaEnReservationDeResto(resa):
    r = ReservationDeResto(resa.client.nom, resa.nbPersonnes(), resa.chambresAssignees.all(), resa.dateDepart,
                           resa.dateArrivee, resa.nbEnfants)
    return r


def faisStatsRepasSoir(dateDemandee, nouveaux, anciensQuiChangent, menages, resas):
    menages = list(menages)

    resaRestoJour = ResaResto.objects.filter(date=dateDemandee)
    anciensByPass = []
    nouveauxByPass = []
    for r in resaRestoJour:
        if r.nbAnciens > 0:
            anciensByPass.append(
                ReservationDeResto(r.nomJoli(), r.nbAnciens, [], dateArrivee=dateDemandee, dateDepart=dateDemandee,
                                   nbEnfants=r.nbEnfants))
        if r.nbNouveaux > 0:
            nouveauxByPass.append(
                ReservationDeResto(r.nomJoli(), r.nbNouveaux, [], dateArrivee=dateDemandee, dateDepart=dateDemandee,
                                   nbEnfants=r.nbEnfants))
        if r.reservationEcrasee:
            client = r.reservationEcrasee
            for resa in client.reservation_set.all():
                essaieDenlever(resas, resa)
                essaieDenlever(nouveaux, resa)
                essaieDenlever(menages, resa)
                essaieDenlever(anciensQuiChangent, resa)

    che = set()
    nouveauxSansCheminDesSud = list(nouveaux)
    for r in nouveaux:
        # on va voir si il y a des chemins des sud qui sont deja passes dans la semaine
        if r.client.tourOperateur:
            if r.client.tourOperateur.nom == "Chemins des suds" and r.nbPersonnes() >= 5:
                if dateDemandee.weekday() == 3:
                    lundi = Reservation.objects.filter(dateArrivee=dateDemandee - timedelta(4)).filter(
                        dateDepart=dateDemandee - timedelta(3))
                    for rr in lundi:
                        if rr.client.tourOperateur:
                            if rr.client.tourOperateur.nom == "Chemins des suds" and r.nbPersonnes() >= 5:
                                try:
                                    nouveauxSansCheminDesSud.remove(r)
                                    che = set([r])
                                except:
                                    pass

    anciens = set(menages) | anciensQuiChangent | che
    anciens = [convertisResaEnReservationDeResto(resa) for resa in anciens]
    nvx = [convertisResaEnReservationDeResto(resa) for resa in nouveauxSansCheminDesSud]
    tout = [convertisResaEnReservationDeResto(resa) for resa in resas]

    anciens.extend(anciensByPass)
    nvx.extend(nouveauxByPass)
    tout.extend(anciensByPass)
    tout.extend(nouveauxByPass)

    repas = Repas()
    repas.anciens = StatRepas(anciens)
    repas.nouveaux = StatRepas(nvx)
    repas.nouveauxBooking = StatRepas(nvx, True)
    repas.anciensBooking = StatRepas(anciens, True)
    repas.total = StatRepas(tout)
    repas.lesNoDp = StatRepas(tout, False, True)
    repas.minimum = repas.total.total
    repas.maximum = repas.minimum + repas.lesNoDp.total - 2

    return repas
