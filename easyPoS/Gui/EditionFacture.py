#!/usr/bin/python3
# coding: utf-8
import sys
import collections
import preferences
import time
import random
from datetime import datetime, date
import webbrowser
import ArrhesDlg
from threading import Lock
from decimal import Decimal
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QThread, SIGNAL, SLOT
from log.models import Log
from easyPoS.models import Facture, Categorie, Produit, LigneFacture, Paiement, MoyenPaiement, DonneesEntreprise, Arrhe, \
    LogFacture, RelationReservationFacture
from chambres.models import Client

import logging


def joli(chiffre):
    s = str(chiffre)
    li = s.split(".")
    if len(li) > 1:
        a, b = li
        if b[0:2] == "00":
            return a
        else:
            return a + "." + b[0:2]
    else:
        return s


class MetteurAJourTotal(QThread):
    def __init__(self, parent=None, editFacture=None):
        QThread.__init__(self, parent)
        self.actif = True
        self.editFacture = editFacture

    def run(self):
        time.sleep(2)
        if (self.editFacture.fact.etat in ['V', 'C']):
            pass
        else:
            self.emit(SIGNAL("enableEdit()"))
        #			self.editFacture.enableEdit()
        time.sleep(19)
        while self.actif:
            self.emit(SIGNAL("calcule()"))
            #			self.editFacture.calcule()
            time.sleep(19)

    def arreteToi(self):
        self.actif = False


class CategorieItem(QtGui.QListWidgetItem):
    def __init__(self, cat=None, type=None):
        QtGui.QListWidgetItem.__init__(self)
        if cat:
            self.setText(str(cat.nom))
            self.id = cat.id
        else:
            self.setText("Tout")
            self.id = None


class ProduitItem(QtGui.QListWidgetItem):
    def __init__(self, prod):
        QtGui.QListWidgetItem.__init__(self)
        nom = prod.nom
        j = 27
        if (len(nom) > j):
            nom = nom[0:j]
        k = len(nom)
        nbTab = j + 2 - k
        self.setText(nom + " " * nbTab + joli(prod.prix) + " ")
        self.id = prod.id


class EditFacture(QtGui.QMainWindow):
    def choppeString(self, string):
        #		return string)
        return string

    #		print unicode(string.toUtf8(),encoding="utf-8")
    #		print smart_str(unicode(string.toUtf8(),encoding="utf8"),encoding="utf-8")
    #		t=smart_unicode(string,encoding="utf-8")
    #		return t
    def sauveNom(self):
        if self.fact.client:
            self.fact.clientNomFinal = self.choppeString(self.nomClient.text())
        else:
            cl = Client(nom=self.choppeString(self.nomClient.text()))
            cl.save()
            self.fact.client = cl
        #		self.fact.clientNomFinal=self.nomClient.text()
        self.fact.save()
        self.fact.client.save()
        self.listeModel.totalChange(self.fact)
        self.updateTitle()

    def catClicked(self, cat):
        if not cat.id:
            prods = Produit.objects.filter(actif=True).order_by('nom')
        else:
            prods = Categorie.objects.get(id=cat.id).produit_set.filter(actif=True).order_by('nom')
        self.listeProduits.clear()
        for i in prods:
            self.listeProduits.addItem(ProduitItem(i))

    def updateTotal(self):
        #		return
        self.updateTotalReglement()
        self.lblTotal.setText(joli(self.fact.total()) + " Eur")
        self.listeModel.totalChange(self.fact)
        self.updateTitle()

    #	def pasDeFaussesInfo(self):
    #		if self.montantMontre:
    #			self.lblTotal.setText(" ")
    #			self.setWindowTitle(" ")
    #			self.lblReglementRestantDu.setText(" ")


    def prodClicked(self, prod):
        pr = Produit.objects.get(id=prod.id)
        ligne = LigneFacture(produit=pr, famille=pr.famille.nom, facture=self.fact, prixUnitaireFinal=pr.prix,
                             nomProduitFinal=pr.nom, tauxTvaFinal=pr.tva.taux, position=time.time())
        ligne.save()
        ligne.position = ligne.id
        ligne.save()
        log = Log(facture=self.fact, description="Ajout de " + str(pr.nom) + " num " + str(ligne.id))

        log.save()
        self.addLog(log)
        #		self.pasDeFaussesInfo()


        nb = self.lignes.rowCount() - 1
        self.lignes.insertRow(nb)
        self.fillRow(ligne, nb)
        self.updateTotal()

    def downLigne(self):
        li = self.sender().ligne
        n = self.sender().row
        auDessous = self.lignes.cellWidget(n + 1, 0)
        auDessousDessous = self.lignes.cellWidget(n + 2, 0)
        if not auDessous:
            return
        if not auDessousDessous:
            li.position = auDessous.ligne.position + 1
        else:
            li.position = (auDessous.ligne.position + auDessousDessous.ligne.position) / 2
        li.save()
        self.initLignes()
        self.updateTotal()

    def upLigne(self):
        li = self.sender().ligne
        n = self.sender().row
        auDessus = self.lignes.cellWidget(n - 1, 0)
        auDessusDessus = self.lignes.cellWidget(n - 2, 0)
        if not auDessus:
            return
        if not auDessusDessus:
            li.position = auDessus.ligne.position - 1
        else:
            li.position = (auDessus.ligne.position + auDessusDessus.ligne.position) / 2
        li.save()
        self.initLignes()
        self.updateTotal()

    def supprimeLigne(self):
        # self.l.acquire()
        li = self.sender().ligne
        n = self.sender().row
        #		self.lignes.removeRow(n)
        if li.produit:
            log = Log(facture=self.fact,
                      description="Suppression de " + str(li.quantite) + " " + li.produit.nom + " a " + str(
                          li.prixUnitaireFinal) + " euros num " + str(li.id))
            log.save()
            self.addLog(log)
        li.delete()
        self.initLignes()
        #		self.pasDeFaussesInfo()
        self.updateTotal()

    # self.l.release()

    def chQuantite(self, newVal):
        li = self.sender().ligne
        tot = self.sender().tot
        log = Log(facture=self.fact, description="Changement Quantite de " + str(li.quantite) + " a " + str(
            newVal) + " " + li.produit.nom + " num " + str(li.id))

        log.save()
        self.addLog(log)
        li.quantite = newVal
        li.save()
        tot.setText(joli(Decimal(li.prixUnitaireFinal) * li.quantite))
        #		self.pasDeFaussesInfo()
        self.updateTotal()

    def chPrix(self, newVal):
        li = self.sender().ligne
        tot = self.sender().tot
        if li.produit and (li.produit.id == 173 or li.produit.id == 175):
            return
        log = Log(facture=self.fact, description="Changement prix de " + str(li.prixUnitaireFinal) + " a " + str(
            newVal) + " " + li.produit.nom + " num " + str(li.id))

        log.save()
        self.addLog(log)
        li.prixUnitaireFinal = str(newVal)
        li.save()
        tot.setText(joli(Decimal(li.prixUnitaireFinal) * li.quantite))
        #		self.pasDeFaussesInfo()
        self.updateTotal()

    def supprimeMoyenPaiement(self):
        li = self.sender().paiement
        if li.arrhe:
            li.facture = None
            li.save()
        else:
            li.delete()
        # TODO quand on supprime le moyen de paiement ne pas supprimer l'arrhe eventueellement liee
        self.initListeReglements()
        self.updateTotalReglement()

    def encaisseCheque(self):
        arrhe = self.sender().arrhe
        p = arrhe.encaisseChequeNonEncaisse()
        p.facture = self.fact
        p.save()
        self.initListeReglements()
        self.updateTotalReglement()

    def supprimeCheque(self):
        arrhe = self.sender().arrhe
        arrhe.detruitCheque()
        self.initListeReglements()
        self.updateTotalReglement()

    def remplisLigneChequeNonEncaisse(self, arrhe, n):
        cell1 = QtGui.QLabel(joli(arrhe.montantChequeNonEncaisse) + " en cheque")
        cell2 = QtGui.QPushButton("ENCAISSER")
        cell3 = QtGui.QPushButton("SUPPRIMER")
        cell2.arrhe = arrhe
        cell3.arrhe = arrhe
        QtCore.QObject.connect(cell2, SIGNAL("clicked()"), self.encaisseCheque)
        QtCore.QObject.connect(cell3, SIGNAL("clicked()"), self.supprimeCheque)
        self.listeReglements.setCellWidget(n, 0, cell1)
        self.listeReglements.setCellWidget(n, 1, cell2)
        self.listeReglements.setCellWidget(n, 2, cell3)

    def remplisLigneReglement(self, paiement, n, chequeNonEncaisse=False):
        cell1 = QtGui.QLabel(joli(paiement.montant))
        if paiement.arrhe:
            self.listeReglements.setCellWidget(n, 1, QtGui.QLabel(paiement.moyenPaiement.nom + " d'arrhes"))
        else:
            self.listeReglements.setCellWidget(n, 1, QtGui.QLabel(paiement.moyenPaiement.nom))
        cell3 = QtGui.QPushButton("Supprimer")
        tod = datetime.today()
        if (tod - paiement.date).days > 30 and not paiement.arrhe:
            cell3.setEnabled(False)
        cell3.paiement = paiement
        cell3.row = n
        QtCore.QObject.connect(cell3, SIGNAL("clicked()"), self.supprimeMoyenPaiement)
        self.listeReglements.setCellWidget(n, 0, cell1)
        self.listeReglements.setCellWidget(n, 2, cell3)

    def addSupprimmerUpDown(self, ligne, n):
        it1 = QtGui.QPushButton("Supprimer")
        it1.ligne = ligne
        it1.row = n
        QtCore.QObject.connect(it1, SIGNAL("clicked()"), self.supprimeLigne)
        self.lignes.setCellWidget(n, 4, it1)

        it1 = QtGui.QPushButton("Up")
        it1.ligne = ligne
        it1.row = n
        QtCore.QObject.connect(it1, SIGNAL("clicked()"), self.upLigne)
        self.lignes.setCellWidget(n, 5, it1)

        it1 = QtGui.QPushButton("Down")
        it1.ligne = ligne
        it1.row = n
        QtCore.QObject.connect(it1, SIGNAL("clicked()"), self.downLigne)
        self.lignes.setCellWidget(n, 6, it1)

    def lblChange(self, st):
        envoyeur = self.sender().ligne
        envoyeur.libelle = st
        envoyeur.save()

    def fillRow(self, ligne, n):
        tot = QtGui.QLabel()
        self.addSupprimmerUpDown(ligne, n)
        if not ligne.produit:  # c'est un libelle
            it1 = QtGui.QLineEdit(ligne.libelle)
            QtCore.QObject.connect(it1, SIGNAL("textChanged(const QString&)"), self.lblChange)
            it1.ligne = ligne
            self.lignes.setCellWidget(n, 0, it1)
            return
        it1 = QtGui.QLabel(ligne.produit.nom)
        it1.ligne = ligne
        self.lignes.setCellWidget(n, 0, it1)
        it1 = QtGui.QSpinBox(self.lignes)
        it1.ligne = ligne
        it1.tot = tot
        it1.setMaximum(100000)
        if self.fact.factureAssociee:
            it1.setMinimum(-1000000)
        it1.setValue(ligne.quantite)
        QtCore.QObject.connect(it1, SIGNAL("valueChanged (int)"), self.chQuantite)
        self.lignes.setCellWidget(n, 1, it1)
        it1 = QtGui.QDoubleSpinBox(self.lignes)
        it1.setLocale(QtCore.QLocale(QtCore.QLocale.C))  # TODO used to use dot instead of comma with numpad
        it1.ligne = ligne
        it1.tot = tot
        it1.setMaximum(100000)
        it1.setValue(ligne.prixUnitaireFinal)
        QtCore.QObject.connect(it1, SIGNAL("valueChanged (double)"), self.chPrix)
        self.lignes.setCellWidget(n, 2, it1)
        tot.setText(joli(float(ligne.montant())))
        self.lignes.setCellWidget(n, 3, tot)

    def initLignes(self):
        facts = self.fact.lignefacture_set.all().order_by("position")
        n = 0
        self.lignes.clear()
        self.lignes.setRowCount(len(facts) + 1)
        self.lignes.setColumnCount(7)
        self.lignes.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Nom"))
        self.lignes.horizontalHeader().resizeSection(0, 170)
        self.lignes.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Quantite"))
        self.lignes.horizontalHeader().resizeSection(1, 60)
        self.lignes.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("Prix"))
        self.lignes.horizontalHeader().resizeSection(2, 90)
        self.lignes.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem("Sous Total"))
        self.lignes.horizontalHeader().resizeSection(3, 80)
        self.lignes.setHorizontalHeaderItem(4, QtGui.QTableWidgetItem("Supprimer"))
        self.lignes.horizontalHeader().resizeSection(4, 80)
        self.lignes.setHorizontalHeaderItem(5, QtGui.QTableWidgetItem("Up"))
        self.lignes.horizontalHeader().resizeSection(5, 40)
        self.lignes.setHorizontalHeaderItem(6, QtGui.QTableWidgetItem("Down"))
        self.lignes.horizontalHeader().resizeSection(6, 40)

        for ligne in facts:
            if not ligne.position:
                ligne.position = ligne.id
                ligne.save()
            self.fillRow(ligne, n)
            n += 1
        self.lblTotal = QtGui.QLabel()
        self.lblTotallbl = QtGui.QLabel("Total:")
        self.lignes.setCellWidget(n, 2, self.lblTotallbl)
        self.lignes.setCellWidget(n, 3, self.lblTotal)
        self.updateTotal()

    def getReglement(self, parDefaut=100):
        QtCore.QLocale.setDefault(QtCore.QLocale(QtCore.QLocale.C))  # TODO used to use dot instead of comma with numpad
        if parDefaut == 100:
            try:
                parDefaut = self.dernierReglement
            except AttributeError:
                dudu = self.fact.totalDu()
                if dudu < 0:
                    parDefaut = dudu
                else:
                    parDefaut = dudu / 2
        d, ok = QtGui.QInputDialog.getDouble(self, self.tr("Reglement"), self.tr("Combien:"), parDefaut, -1000000,
                                             1000000, 2)
        if ok:
            self.dernierReglement = d
        return d, ok

    def updateTotalReglement(self):
        self.lblReglementRestantDu.setText(joli(self.fact.total() - self.fact.totalPaye()) + " Eur")

    def initListeReglements(self):

        arrhes = self.fact.client.arrhe_set.all()
        ars = []
        for a in arrhes:
            if a.montantChequeNonEncaisse:
                ars.append(a)

        regls = self.fact.paiement_set.all()

        sizeBox = len(regls) + len(ars)
        n = 0
        self.listeReglements.clear()
        self.listeReglements.setRowCount(sizeBox + 1)
        self.listeReglements.setColumnCount(3)
        self.listeReglements.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Montant"))
        self.listeReglements.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Moyen"))
        self.listeReglements.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("Suppr"))
        for a in ars:
            self.remplisLigneChequeNonEncaisse(a, n)
            n += 1
        for ligne in regls:
            self.remplisLigneReglement(ligne, n)
            n += 1
        self.lblReglementRestantDu = QtGui.QLabel()
        self.lblReglementRestant = QtGui.QLabel("Restant Du:")
        if len(regls) > -1:
            self.listeReglements.setCellWidget(n, 0, self.lblReglementRestant)
            self.listeReglements.setCellWidget(n, 1, self.lblReglementRestantDu)
        self.updateTotalReglement()
        self.updateTitle()
        if self.fact.total() > 0:
            if self.fact.totalDu() == 0:
                rs = RelationReservationFacture.objects.filter(facture=self.fact)
                for r in rs:
                    r.reservation.partis = True
                    r.reservation.save()
                if self.fenetrePrincipale.fermeAutomatique:
                    print("on va valide et ferme")
                    if self.fact.etat == "B":
                        self.valideSansConfirmer()
                    self.close()
                else:
                    print("on fait rien")

    def addCB(self, montant):
        moyCB = MoyenPaiement.objects.get(nom="CB")
        ent = self.fact.entreprise
        p = Paiement(entreprise=ent, montant=Decimal(montant), moyenPaiement=moyCB, facture=self.fact,
                     date=datetime.now())
        p.save()
        self.initListeReglements()

    def RCB(self):
        du = self.fact.totalDu()
        if (du > 0):
            self.addCB(du)

    def CCB(self):
        d, ok = self.getReglement()
        if ok:
            self.addCB(Decimal(str(d)))

    def addCheque(self, montant):
        moyCheque = MoyenPaiement.objects.get(nom="Cheque")
        ent = self.fact.entreprise
        p = Paiement(entreprise=ent, montant=Decimal(montant), moyenPaiement=moyCheque, facture=self.fact,
                     date=datetime.now())
        p.save()
        self.initListeReglements()

    def RCheque(self):
        du = self.fact.totalDu()
        if (du > 0):
            self.addCheque(du)

    def CCheque(self):
        d, ok = self.getReglement()
        if ok:
            self.addCheque(Decimal(str(d)))

    def addEspece(self, montant):
        moyEspece = MoyenPaiement.objects.get(nom="Espece")
        ent = self.fact.entreprise
        p = Paiement(entreprise=ent, montant=Decimal(montant), moyenPaiement=moyEspece, facture=self.fact,
                     date=datetime.now())
        p.save()
        self.initListeReglements()

    def REspece(self):
        du = self.fact.totalDu()
        if (du > 0):
            self.addEspece(du)

    def CEspece(self):
        d, ok = self.getReglement()
        if ok:
            self.addEspece(Decimal(str(d)))

    def Dvirement(self):
        moyANCV = MoyenPaiement.objects.get(nom="Virement")
        du = self.fact.totalDu()
        d, ok = self.getReglement(parDefaut=du)
        if ok:
            ent = self.fact.entreprise
            p = Paiement(entreprise=ent, montant=Decimal((str(d))), moyenPaiement=moyANCV, facture=self.fact,
                         date=datetime.now())
            p.save()
            self.initListeReglements()

    def addANCV(self, montant):
        moyANCV = MoyenPaiement.objects.get(nom="ANCV")
        ent = self.fact.entreprise
        p = Paiement(entreprise=ent, montant=Decimal(montant), moyenPaiement=moyANCV, facture=self.fact,
                     date=datetime.now())
        p.save()
        self.initListeReglements()

    def CANCV(self):
        du = self.fact.totalDu()
        mod = du % 10
        if mod != 0:
            du += (10 - mod - 10)
        d, ok = self.getReglement(parDefaut=du)
        if ok:
            self.addANCV(Decimal(str(d)))

    def createReglement(self):
        self.CB = QtGui.QHBoxLayout()
        self.resteCB = QtGui.QPushButton("detail CB")
        self.customCB = QtGui.QPushButton("CB")
        self.CB.addWidget(self.resteCB)
        self.CB.addWidget(self.customCB)
        self.connect(self.resteCB, QtCore.SIGNAL("clicked()"), self.CCB)
        self.connect(self.customCB, QtCore.SIGNAL("clicked()"), self.RCB)

        self.Cheque = QtGui.QHBoxLayout()
        self.resteCheque = QtGui.QPushButton("detail Cheque")
        self.customCheque = QtGui.QPushButton("Cheque")
        self.Cheque.addWidget(self.resteCheque)
        self.Cheque.addWidget(self.customCheque)
        self.connect(self.resteCheque, QtCore.SIGNAL("clicked()"), self.CCheque)
        self.connect(self.customCheque, QtCore.SIGNAL("clicked()"), self.RCheque)

        self.Espece = QtGui.QHBoxLayout()
        self.resteEspece = QtGui.QPushButton("detail Espece")
        self.customEspece = QtGui.QPushButton("Espece")
        self.Espece.addWidget(self.resteEspece)
        self.Espece.addWidget(self.customEspece)
        self.connect(self.resteEspece, QtCore.SIGNAL("clicked()"), self.CEspece)
        self.connect(self.customEspece, QtCore.SIGNAL("clicked()"), self.REspece)

        self.ChequeVacance = QtGui.QHBoxLayout()
        self.resteChequeVacance = QtGui.QPushButton("ANCV")
        self.ChequeVacance.addWidget(self.resteChequeVacance)
        self.connect(self.resteChequeVacance, QtCore.SIGNAL("clicked()"), self.CANCV)

        self.renduMonnaieBox = QtGui.QHBoxLayout()
        self.ultimeBox = QtGui.QHBoxLayout()
        self.arrhes = QtGui.QPushButton("Arrhes")
        self.renduMonnaie = QtGui.QPushButton("Rendu monnaie")
        self.ajouterLibelle = QtGui.QPushButton("Ajout libelle")
        self.ajouterLibelle.setShortcut("Ctrl+l")
        self.virement = QtGui.QPushButton("Virement")
        self.renduMonnaieBox.addWidget(self.renduMonnaie)
        # self.renduMonnaieBox.addWidget(self.virement)
        self.ChequeVacance.addWidget(self.virement)
        self.ultimeBox.addWidget(self.ajouterLibelle)
        self.ultimeBox.addWidget(self.arrhes)
        self.connect(self.renduMonnaie, QtCore.SIGNAL("clicked()"), self.rendMonnaie)
        self.connect(self.arrhes, QtCore.SIGNAL("clicked()"), self.montreArrhes)
        self.connect(self.virement, QtCore.SIGNAL("clicked()"), self.Dvirement)
        self.connect(self.ajouterLibelle, QtCore.SIGNAL("clicked()"), self.ajouteLibelle)

        self.listeReglements = QtGui.QTableWidget()
        self.initListeReglements()

        self.Reglements = QtGui.QVBoxLayout()
        self.Reglements.addLayout(self.CB)
        self.Reglements.addLayout(self.Cheque)
        self.Reglements.addLayout(self.Espece)
        self.Reglements.addLayout(self.ChequeVacance)
        self.Reglements.addLayout(self.renduMonnaieBox)
        self.Reglements.addLayout(self.ultimeBox)

    def ajouteLibelle(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Ajoute')
        if ok:
            ligne = LigneFacture(produit=None, libelle=text, facture=self.fact, position=time.time())
            ligne.save()
            ligne.position = ligne.id
            ligne.save()
            nb = self.lignes.rowCount() - 1
            self.lignes.insertRow(nb)
            self.fillRow(ligne, nb)

    def montreArrhes(self):
        r = ArrhesDlg.ArrhesDlg("Choisissez des Arrhes", self)
        r.exec_()
        if r.result():
            p = r.paiement
            p.facture = self.fact
            p.save()
            self.initListeReglements()

    def rendMonnaie(self):
        totalDu = self.fact.totalDu()
        if (totalDu < 0):
            rendu = MoyenPaiement.objects.get(nom="Espece")
            ent = self.fact.entreprise
            p = Paiement(entreprise=ent, montant=Decimal(totalDu), moyenPaiement=rendu, facture=self.fact,
                         date=datetime.now())
            p.save()
            self.initListeReglements()

    def createComponents(self):
        self.createReglement()
        self.lblTotal = QtGui.QLabel()
        self.listeCategories = QtGui.QListWidget()
        f = QtGui.QFont('Helvetica', 15)
        self.listeCategories.setFont(f)
        cat = Categorie.objects.all()
        self.listeCategories.addItem(CategorieItem(type="all"))
        for i in cat:
            self.listeCategories.addItem(CategorieItem(i))
        self.listeProduits = QtGui.QListWidget()
        self.listeProduits.setAlternatingRowColors(True)
        f = QtGui.QFont('Courier', 10)
        f.setStretch(QtGui.QFont.Condensed)
        f.setFixedPitch(True)
        self.listeProduits.setFont(f)
        #	self.listeProduits.setSpacing(5)
        # pro=Produit.objects.all().order_by('nom').filter(actif=True)
        pro = Categorie.objects.get(id=1).produit_set.filter(actif=True).order_by(
            'nom')  # choppe les produits frequemment vendu
        for j in pro:
            self.listeProduits.addItem(ProduitItem(j))
        self.lignes = QtGui.QTableWidget()
        self.nomClient = QtGui.QLineEdit()
        if self.fact.clientNomFinal:
            self.nomClient.setText((self.fact.clientNomFinal))
        elif self.fact.client:
            self.nomClient.setText((self.fact.client.nom))
        self.initLignes()
        QtCore.QObject.connect(self.nomClient, SIGNAL("editingFinished ()"), self.sauveNom)
        QtCore.QObject.connect(self.listeCategories, SIGNAL("itemClicked (QListWidgetItem *)"), self.catClicked)
        QtCore.QObject.connect(self.listeProduits, SIGNAL("itemClicked (QListWidgetItem *)"), self.prodClicked)

    def imprimeValide(self):
        webbrowser.open(preferences.URL + "/easyPoS/facture/" + str(self.facture) + "/print")
        if self.fact.etat == "B":
            self.valideSansConfirmer()

    def imprimeDevis(self):
        webbrowser.open(preferences.URL + "/easyPoS/facture/" + str(self.facture) + "/printDevis")

    def imprime(self):

        webbrowser.open(preferences.URL + "/easyPoS/facture/" + str(self.facture) + "/print")
        if self.fact.etat == "B":
            self.valide()

    def remplisDefinitivement(self, fact):
        if fact.client and not fact.clientNomFinal:
            fact.clientNomFinal = fact.client.nom
        for l in fact.lignefacture_set.all():
            if l.produit:
                if not l.nomProduitFinal:
                    l.nomProduitFinal = l.produit.nom
                if not l.tauxTvaFinal:
                    l.tauxTvaFinal = l.produit.tva.taux
                # if not l.prixUnitaireFinal:
                #		l.prixUnitaireFinal=l.produit.prix
                l.save()
        fact.save()

    def enableEdit(self):
        self.listeProduits.setEnabled(True)
        self.lignes.setEnabled(True)
        self.ajouterLibelle.setEnabled(True)

    def disableUnintentionalEdit(self):
        self.listeProduits.setEnabled(False)
        self.lignes.setEnabled(False)

    def disableEdit(self):
        self.listeProduits.setEnabled(False)
        self.factorise.setEnabled(False)
        self.lignes.setEnabled(False)
        self.valider.setEnabled(False)
        self.supprimer.setEnabled(False)
        self.ajouterLibelle.setEnabled(False)

    def valideMoiCa(self):
        if "devis" in str(self.fact.clientNomFinal).lower():
            QtGui.QMessageBox.warning(self, "Ouala", "impossible valider un devis, veuillez enlever devis du nom")
            return
        estHotel, nbPers, nbTs = self.fact.estFactureHotel()
        if estHotel:
            if nbPers != nbTs:
                ret = QtGui.QMessageBox.warning(self, "..", "Attention, il y a peut être " + str(
                    nbPers) + " qui dorment dans cette facture et vous avez facturé " + str(
                    nbTs) + " taxe(s) de séjour", QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                                                QtGui.QMessageBox.Ok);

                if ret == QtGui.QMessageBox.Cancel:
                    return

        self.valideFacture(self.fact)
        if (self.fact.totalDu() == 0):
            self.listeModel.supprime(self.fact)
        self.disableEdit()
        paiements = self.fact.paiement_set.all()
        for p in paiements:
            if not p.arrhe:
                p.date = datetime.now()
                p.save()
            # self.deleteLater()
            #		self.close()

    def valideSansConfirmer(self):
        self.valideMoiCa()

    def valide(self):

        ret = QtGui.QMessageBox.warning(self, "Attention",
                                        "Etes vous sur de vouloir valider\n ",
                                        QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                                        QtGui.QMessageBox.Ok);

        if ret == QtGui.QMessageBox.Cancel:
            return
        self.valideMoiCa()

    # dans une transaction attribuer n definitif
    def valideFacture(self, fact):
        donnees = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
        fact.numero = donnees.numeroFactureCourante
        donnees.numeroFactureCourante += 1
        donnees.save()
        fact.etat = 'V'
        fact.dateVente = datetime.today()
        fact.save()
        self.remplisDefinitivement(fact)
        log = Log(facture=self.fact, description="VALIDATION")
        log.save()

    def supprime(self):
        paiements = self.fact.paiement_set.all()
        for p in paiements:
            if p.arrhe:
                QtGui.QMessageBox.warning(self, "Attention",
                                          "Il y a des arrhes associees, veuillez les supprimer avant de supprimer la facture",
                                          QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok);
                return
        ret = QtGui.QMessageBox.warning(self, "Attention",
                                        "Etes vous sur de vouloir supprimer\n",
                                        QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                                        QtGui.QMessageBox.Ok);

        if ret == QtGui.QMessageBox.Cancel:
            return
        self.supprimeFacture(self.fact)
        self.listeModel.supprime(self.fact)
        self.disableEdit()
        self.close()

    def supprimeFacture(self, fact):
        fact.etat = 'C'
        fact.save()
        self.remplisDefinitivement(fact)

    def calcule(self):
        self.fact.updateCache()

    #		self.updateTotalReglement()
    #		self.lblTotal.setText(joli(self.fact.total())+" Eur")
    #		self.listeModel.totalChange(self.fact)
    #		self.updateTitle()
    #		self.montantMontre=True
    def cloneMoiCa(self):
        self.fenetrePrincipale.cloneMoiCa(self.fact)

    def tupleProdPrix(self, ligne):
        return (ligne.produit, ligne.prixUnitaireFinal)

    def ecrireProdQuantite(self, prodQuantite):
        for key, item in list(prodQuantite.items()):
            (prod, prix) = key
            ligne = LigneFacture(produit=prod, famille=prod.famille.nom, facture=self.fact, prixUnitaireFinal=prix,
                                 nomProduitFinal=prod.nom, tauxTvaFinal=prod.tva.taux, quantite=item,
                                 position=time.time())
            ligne.save()
            ligne.position = ligne.id
            ligne.save()

    def factoriseLignes(self):
        lignes = self.fact.lignefacture_set.all().order_by("position")
        prodQuantite = collections.OrderedDict()
        for l in lignes:
            if l.libelle:
                self.ecrireProdQuantite(prodQuantite)
                ligne = LigneFacture(produit=None, facture=self.fact, libelle=l.libelle, position=time.time())
                ligne.save()
                ligne.position = ligne.id
                ligne.save()
                prodQuantite = collections.OrderedDict()
            elif l.quantite < 0:
                ligne = LigneFacture(produit=l.produit, facture=self.fact, famille=l.famille,
                                     prixUnitaireFinal=l.prixUnitaireFinal, nomProduitFinal=l.nomProduitFinal,
                                     tauxTvaFinal=l.tauxTvaFinal, quantite=l.quantite, position=time.time())
                ligne.save()
                ligne.position = ligne.id
                ligne.save()

            else:
                t = self.tupleProdPrix(l)
                if t in prodQuantite:
                    prodQuantite[t] += l.quantite
                else:
                    prodQuantite[t] = l.quantite
        self.ecrireProdQuantite(prodQuantite)
        for l in lignes:
            l.delete()
        self.initLignes()

    def addLog(self, i):
        self.logList.insertItem(0, QtGui.QListWidgetItem(i.description + " le " + str(i.creation)))

    def creeAvoir(self):
        if not self.fact.etat == 'V':
            QtGui.QMessageBox.warning(self, "Epa", "Il faut que cette facture soit validee")
            return
        self.fact.creeAvoir()
        QtGui.QMessageBox.warning(self, "Ouala", "Facture creee")

    def tjsVisible(self):
        self.fact.toujoursVisible = self.calculeTot.isChecked()
        self.fact.save()

    def placeComponents(self):
        tabs = QtGui.QTabWidget()
        imp = QtGui.QPushButton("Imprimer")
        impDevis = QtGui.QPushButton("Devis")
        self.calculeTot = QtGui.QCheckBox("Toujours Visible")
        self.calculeTot.setChecked(self.fact.toujoursVisible)
        clone = QtGui.QPushButton("Clone")
        creeAvoir = QtGui.QPushButton("Creer facture d'avoir")
        self.factorise = QtGui.QPushButton("Factorise")
        self.connect(imp, QtCore.SIGNAL('clicked()'), self.imprimeValide)
        self.connect(impDevis, QtCore.SIGNAL('clicked()'), self.imprimeDevis)
        self.connect(self.calculeTot, QtCore.SIGNAL('clicked()'), self.tjsVisible)
        self.connect(clone, QtCore.SIGNAL('clicked()'), self.cloneMoiCa)
        self.connect(creeAvoir, QtCore.SIGNAL('clicked()'), self.creeAvoir)
        self.connect(self.factorise, QtCore.SIGNAL('clicked()'), self.factoriseLignes)
        self.valider = QtGui.QPushButton("Valider")
        self.connect(self.valider, QtCore.SIGNAL('clicked()'), self.valide)
        self.supprimer = QtGui.QPushButton("Supprimer")
        self.connect(self.supprimer, QtCore.SIGNAL('clicked()'), self.supprime)
        hbox = QtGui.QHBoxLayout()
        hbox2 = QtGui.QHBoxLayout()
        total = QtGui.QHBoxLayout()
        catTotalBox = QtGui.QVBoxLayout()
        catTotalBox.addWidget(self.listeCategories, 10)
        catTotalBox.addLayout(self.Reglements, 1)
        listeProdBox = QtGui.QVBoxLayout()
        listeProdBox.addWidget(self.listeProduits, 3)
        listeProdBox.addWidget(self.listeReglements, 1)
        hbox2.addLayout(catTotalBox, 1)
        hbox2.addLayout(listeProdBox, 8)
        hbox2.addWidget(self.lignes, 14)
        hbox.addWidget(imp)
        hbox.addWidget(impDevis)
        hbox.addWidget(self.factorise)
        hbox.addWidget(clone)
        hbox.addWidget(creeAvoir)
        hbox.addWidget(self.calculeTot)
        hbox.addStretch(1)
        hbox.addWidget(self.valider)
        hbox.addWidget(self.supprimer)
        vbox = QtGui.QVBoxLayout()

        vClient = QtGui.QVBoxLayout()
        vl = QtGui.QHBoxLayout()
        vl.addWidget(QtGui.QLabel("Nom"))
        vl.addWidget(self.nomClient)
        vClient.addLayout(vl)
        vClient.addStretch()

        vDetail = QtGui.QVBoxLayout()
        vl = QtGui.QHBoxLayout()
        vl.addWidget(QtGui.QLabel("Date Creation"))
        vl.addWidget(QtGui.QLabel("Etat"))
        vDetail.addLayout(vl)
        vl = QtGui.QHBoxLayout()
        vl.addWidget(QtGui.QLabel("Etat"))
        vl.addWidget(QtGui.QLabel("Adresse"))
        vDetail.addLayout(vl)
        vl = QtGui.QHBoxLayout()
        vl.addWidget(QtGui.QLabel("Logs"))
        self.logList = QtGui.QListWidget()

        log2 = LogFacture.objects.filter(facture=self.fact)
        logFact = Log.objects.filter(facture=self.fact)

        for i in logFact:
            self.addLog(i)
        vl.addWidget(self.logList)
        vDetail.addLayout(vl)
        #	vl.addWidget(QtGui.QTextEdit())
        #		vClient.addLayout(vl)
        #		vl=QtGui.QHBoxLayout()
        #		vl.addWidget(QtGui.QLabel("Date de vente"))
        #		vl.addWidget(QtGui.QCalendarWidget())
        #		vClient.addLayout(vl)
        #		vl=QtGui.QHBoxLayout()
        #		vl.addWidget(QtGui.QLabel("Date de Reglement"))
        #		vl.addWidget(QtGui.QCalendarWidget())
        #		vClient.addLayout(vl)


        vPlusGrandeBox = QtGui.QVBoxLayout()
        vPlusGrandeBox.addLayout(vClient, 1)
        #		vPlusGrandeBox.addStretch()
        vPlusGrandeBox.addLayout(hbox2, 250)

        tabFact = QtGui.QWidget()
        tabFact.setLayout(vPlusGrandeBox)

        tabClient = QtGui.QWidget()
        tabClient.setLayout(vDetail)

        tabs.addTab(tabFact, "Facture")
        tabs.addTab(tabClient, "Info Detaillees")

        vbox.addWidget(tabs, 10)
        #		vbox.addLayout(vPlusGrandeBox,10)
        vbox.addLayout(hbox, 1)
        wi = QtGui.QWidget()
        wi.setLayout(vbox)
        self.setCentralWidget(wi)
        self.nomClient.setFocus(True)

    def updateTitle(self):
        if self.fact.factureAssociee:
            pre = "Avoir: "
        else:
            pre = ""
        if self.fact.clientNomFinal:
            pre += self.fact.clientNomFinal + " "
        elif self.fact.client:
            if self.fact.client.nom != "":
                pre += self.fact.client.nom + " "
        if self.fact.totalDu() != self.fact.total():
            post = " Du:" + joli(self.fact.totalDu())
        else:
            post = ""
        titre = pre + joli(self.fact.total()) + "\u20AC" + post  # le u20AC est le signe euro
        tit = (titre)
        #		tit=str(pre)+str(joli(self.fact.total()))+str(("€"))+str(post)
        self.setWindowTitle(tit)  # Num. "+str(self.fact.id))

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2 - 45)

    def stop(self):
        self.calcule()
        self.metteurAJourTotal.arreteToi()

    def __init__(self, parent=None, facture=None, listeModel=None, fenetrePrincipale=None):
        QtGui.QMainWindow.__init__(self, parent)
        #		self.montantMontre=False
        self.metteurAJourTotal = MetteurAJourTotal(editFacture=self)
        QtCore.QObject.connect(self.metteurAJourTotal, SIGNAL("enableEdit()"), self.enableEdit)
        QtCore.QObject.connect(self.metteurAJourTotal, SIGNAL("calcule()"), self.calcule)
        self.l = Lock()
        self.fenetrePrincipale = fenetrePrincipale
        self.resize(1200, 670)
        self.center()
        self.facture = facture
        self.listeModel = listeModel
        self.fact = Facture.objects.get(id=self.facture)
        self.createComponents()
        self.placeComponents()
        self.updateTitle()
        if self.fact.cacheTotal and self.fact.cacheTotal > 0:
            self.disableUnintentionalEdit()
        if (self.fact.etat in ['V', 'C']):
            self.disableEdit()
        self.metteurAJourTotal.start()
        icone = QtGui.QIcon("ic2.png")
        self.setWindowIcon(icone)

    #		textEdit = QtGui.QListWidget()

# self.setCentralWidget(textEdit)
