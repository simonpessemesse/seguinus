from PyQt4 import QtCore, QtGui
from datetime import datetime, timedelta
import preferences
import webbrowser
from chambres.models import joliePeriode
from easyPoS.models import DonneesEntreprise, LigneFacture, PreparationFacture, Produit, LogFacture, \
    RelationReservationFacture
from chambres.models import Client
from chambres.models import Reservation, TourOperateur
import traceback
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QThread, SIGNAL
from easyPoS.models import Facture
import time
import EditionFacture
import sys


def getLibelle(resa):
    chs = resa.chambresAssignees.all()
    libelle = ""
    for ch in chs:
        libelle += " " + ch.nom
    if resa.placesDortoir > 0:
        libelle += " Dortoir"
    if libelle == "":
        libelle = resa.client.nom
    return libelle + " du " + joliePeriode(resa.dateArrivee, resa.dateDepart)


def getNom(resa):
    return resa.client.nom + " du " + joliePeriode(resa.dateArrivee, resa.dateDepart)


def ajouterNProd(n, prod, fact, prix=None):
    if n > 0:
        if prix:
            pr = prix
        else:
            pr = prod.prix
        ligne = LigneFacture(produit=prod, facture=fact, famille=prod.famille.nom, prixUnitaireFinal=pr,
                             nomProduitFinal=prod.nom, tauxTvaFinal=prod.tva.taux, quantite=n, position=time.time())
        ligne.save()
        ligne.position = ligne.id
        ligne.save()
    # TODO add log


def ajoutePrestations(fact, resa, prixReduit=False):
    picnicAjoute = False
    if resa.client.tourOperateur:

        tourOp = resa.client.tourOperateur
        nbPers = resa.nbPersonnes()

        if tourOp.seuilGroupe and nbPers >= tourOp.seuilGroupe:
            groupe = True
        else:
            groupe = False

        if groupe and tourOp.gratuiteAccompagnateurSiGroupe:
            nbPers = nbPers - 1

        if groupe and tourOp.picnicSiGroupe:
            ajouterNProd(nbPers * resa.nbNuits(), Produit.objects.get(pk=4), fact, prix=7.5)
            picnicAjoute = True

        if tourOp.prixParPersonne:
            demiPensionChambrePartagee = Produit.objects.get(pk=107)
            if resa.chambresSingle > 0:
                ajouterNProd(resa.chambresSingle, Produit.objects.get(pk=154), fact)
            ajouterNProd(nbPers, demiPensionChambrePartagee, fact, prix=tourOp.prixParPersonne)
            return

    nbNuits = resa.nbNuits()
    if resa.client.asPicnicDansLeNom() and not picnicAjoute:
        ajouterNProd(resa.nbPersonnes() * nbNuits, Produit.objects.get(pk=4), fact)

    if "nodp" in resa.client.nom or "no dp" in resa.client.nom:
        dortoir = Produit.objects.get(pk=142)
        single = Produit.objects.get(pk=136)
        double = Produit.objects.get(pk=136)
        triple = Produit.objects.get(pk=137)
        quadruple = Produit.objects.get(pk=138)
        quintuple = Produit.objects.get(pk=139)
        petitDej = Produit.objects.get(pk=133)
        ajouterNProd(resa.nbPersonnes() * nbNuits, petitDej, fact)
    else:
        dortoir = Produit.objects.get(pk=148)
        single = Produit.objects.get(pk=149)
        double = Produit.objects.get(pk=150)
        triple = Produit.objects.get(pk=11)
        quadruple = Produit.objects.get(pk=151)
        quintuple = Produit.objects.get(pk=12)
    ajouterNProd(nbNuits * resa.placesDortoir, dortoir, fact)
    ajouterNProd(nbNuits * resa.chambresQuintuples, quintuple, fact)
    if prixReduit:
        ajouterNProd(nbNuits * resa.chambresSingle, single, fact, prix=82)
        ajouterNProd(nbNuits * (resa.chambres + resa.chambresDoubles + resa.chambresTwin), double, fact, prix=124)
        ajouterNProd(nbNuits * resa.chambresTriples, triple, fact, prix=163)
        ajouterNProd(nbNuits * resa.chambresQuadruples, quadruple, fact, prix=200)
    else:
        ajouterNProd(nbNuits * resa.chambresSingle, single, fact)
        ajouterNProd(nbNuits * (resa.chambres + resa.chambresDoubles + resa.chambresTwin), double, fact)
        ajouterNProd(nbNuits * resa.chambresTriples, triple, fact)
        ajouterNProd(nbNuits * resa.chambresQuadruples, quadruple, fact)

    taxeDeSejour = Produit.objects.get(pk=173)
    ajouterNProd(nbNuits * resa.nbPersonnes(), taxeDeSejour, fact)


def prepare(resa):
    ent = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
    if not ent.actif:
        return
    if resa.client.tourOperateur:
        nomTourOp = resa.client.tourOperateur.nom
        facts = Facture.objects.filter(entreprise=ent).filter(etat='B').filter(client__nom=nomTourOp)
        if (len(facts) > 1):
            raise Exception("trop de factures avec ce nom")
        else:
            if (len(facts) == 0):
                fact = Facture(entreprise=ent, etat='B')
                fact.clientNomFinal = nomTourOp
                c = Client(nom=nomTourOp)
                c.save()
                fact.client = c
                fact.save()
            else:
                fact = facts[0]
            libelle = getNom(resa)
            ligne = LigneFacture(libelle=libelle, facture=fact, position=time.time())
            ligne.save()
            ligne.position = ligne.id
            ligne.save()

            if resa.client.tourOperateur.tarifReduit:
                prixReduit = True
            else:
                prixReduit = False

            ajoutePrestations(fact, resa, prixReduit)
    else:
        nom = getLibelle(resa)
        fact = Facture(entreprise=ent, etat='B')
        c = Client(nom=nom)
        c.save()
        fact.client = resa.client
        fact.clientNomFinal = nom
        fact.save()
        if resa.nbNuits() >= 3:
            prixReduit = True
        else:
            prixReduit = False
        ajoutePrestations(fact, resa, prixReduit)

        arrhes = resa.client.arrhe_set.all()
        for a in arrhes:
            paiements = a.paiement_set.all()
            for p in paiements:
                if not p.facture:
                    p.facture = fact
                    p.save()

                p.save()

    r = RelationReservationFacture(reservation=resa, facture=fact)
    r.save()
    return fact
