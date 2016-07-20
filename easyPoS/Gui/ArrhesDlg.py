#!/usr/bin/env python
# Copyright (c) 2007-8 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from easyPoS.models import Arrhe, Paiement

MAC = "qt_mac_set_native_menubar" in dir()


class PaiementItem(QListWidgetItem):
    def __init__(self, paiement):
        QListWidgetItem.__init__(self)
        self.setText(paiement.arrhe.client.nom + "\t" + str(paiement.montant) + " euros")
        self.id = paiement.id
        self.paiement = paiement


class ArrhesDlg(QDialog):
    def __init__(self, name, parent=None):
        super(ArrhesDlg, self).__init__(parent)

        self.name = name

        self.searchBox = QLineEdit()
        self.connect(self.searchBox, SIGNAL("textChanged (const QString&)"), self.change)
        bigV = QVBoxLayout()

        self.listWidget = QListWidget()
        #		self.connect(self.listWidget,SIGNAL("itemActivated (QListWidgetItem *)"),self.cliquete)
        self.connect(self.listWidget, SIGNAL("itemClicked (QListWidgetItem *)"), self.cliquete)
        self.remplisListe("")

        buttonLayout = QVBoxLayout()
        button = QPushButton("Annuler")
        button.setFocusPolicy(Qt.NoFocus)
        buttonLayout.addWidget(button)
        buttonLayout.addStretch()
        self.connect(button, SIGNAL("clicked()"), self.reject)

        layout = QHBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addLayout(buttonLayout)
        bigV.addWidget(self.searchBox)
        bigV.addLayout(layout)
        self.setLayout(bigV)
        self.setWindowTitle("%s" % self.name)

    def cliquete(self, item):
        self.accept(item.paiement)

    def remplisListe(self, filtre):
        filtre = str(filtre).lower()
        ps = Paiement.objects.filter(arrhe__isnull=False).filter(facture__isnull=True)
        liste = []
        for p in ps:
            if filtre in p.arrhe.client.nom.lower():
                liste.append(p)

        self.listWidget.clear()
        for p in liste:
            self.listWidget.addItem(PaiementItem(p))
        #			self.listWidget.setCurrentRow(0)

    def change(self, stri):
        self.remplisListe(stri)

    def accept(self, paiement):
        self.paiement = paiement
        QDialog.accept(self)
