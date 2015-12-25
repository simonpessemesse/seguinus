#!/usr/bin/python

import webbrowser
import configureEnvironnement


import django
django.setup()
import sys
import preferences
from telephones.models import Contact
from PyQt4 import QtGui
from PyQt4 import QtCore


class Example(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.initUI()

	def remplisListe(self,text=None):
		print(self.edit.text())
		contacts=Contact.objects.filter(nomTags__icontains=self.edit.text()).order_by("nomTags")
		self.liste.clear()
		for c in contacts:
			item=QtGui.QListWidgetItem(c.nomTags+"\t"+c.numero)
			item.idTruc=c.id
			self.liste.addItem(item)

	def ajoutC(self):
		print("ouvre")
		webbrowser.open(preferences.URL+"/admin/telephones/contact/add/")
	def test(self,item):
		webbrowser.open(preferences.URL+"/admin/telephones/contact/{0}".format(item.idTruc))
	def initUI(self):

#		self.label = QtGui.QLabel(self)
#		self.label.setText("")
		self.edit = QtGui.QLineEdit(self)

		self.liste=QtGui.QListWidget(self)
		self.ajout=QtGui.QPushButton("Ajouter un Contact")


		hbox = QtGui.QVBoxLayout()
		hbox.addWidget(self.ajout)
		hbox.addWidget(self.edit)
		hbox.addWidget(self.liste)
		self.setLayout(hbox)

		self.remplisListe()
		

		self.connect(self.edit, QtCore.SIGNAL('textChanged(QString)'), self.remplisListe)
		self.connect(self.liste,QtCore.SIGNAL('itemClicked (QListWidgetItem *)'),self.test)
		self.connect(self.ajout, QtCore.SIGNAL('clicked()'), self.ajoutC)
		print("bon")

		self.setGeometry(150, 100, 650, 450)
		self.setWindowTitle('Chercheur de numero')

	def onChanged(self, text):
		return
		self.liste.setText(text)
		self.liste.adjustSize()
	

app = QtGui.QApplication(sys.argv)
exm = Example()
exm.show()
app.exec_()
