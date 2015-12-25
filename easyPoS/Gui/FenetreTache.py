#!/usr/bin/python3
# coding: utf-8
import sys
import preferences
import random
from datetime import datetime,date,timedelta,time
import webbrowser
import ArrhesDlg
from threading import Lock
from decimal import Decimal
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QThread,SIGNAL,SLOT
from easyPoS.models import Facture,Categorie,Produit,LigneFacture,Paiement,MoyenPaiement,DonneesEntreprise,Arrhe,LogFacture

from chambres.models import Client,Tache,Entite,TacheLog
import logging






class EditTache(QtGui.QMainWindow):


	def texteChange(self,text):
		if not self.tache.estPeriodique():
			self.tache.description=text
			self.tache.save()
		print("texte change",text)
	def createComponents(self):
		self.nomClient=QtGui.QLineEdit()
		self.connect(self.nomClient, QtCore.SIGNAL('textChanged (const QString&)'), self.texteChange)
		self.nomClient.setText((self.tache.description))

	def fait(self):
		tl=TacheLog(tache=self.tache)
		tl.save()

		self.tache.executee=True
		self.tache.save()
		self.close()

	def deuxH(self):
		tl=TacheLog(tache=self.tache)
		tl.save()
		soon=datetime.now()+timedelta(0,60*60*2)
		if self.tache.estPeriodique():
			pass
#			t=Tache(description=ex.description,rappel=ap)
#			t.save()
		else:
			self.tache.rappel=soon.time()
			self.tache.date=soon.date()
			self.tache.save()
			self.close()


	def uneH(self):
		tl=TacheLog(tache=self.tache)
		tl.save()

		soon=datetime.now()+timedelta(0,60*60)
		if self.tache.estPeriodique():
			pass
#			t=Tache(description=ex.description,rappel=ap)
#			t.save()
		else:
			self.tache.rappel=soon.time()
			self.tache.date=soon.date()
			self.tache.save()
			self.close()
	def soir(self):
		tl=TacheLog(tache=self.tache)
		tl.save()

		self.tache.rappel=time(18,0o2,00)
		self.tache.save()
		self.close()
	def demain(self):
		tl=TacheLog(tache=self.tache)
		tl.save()
		soon=datetime.now()+timedelta(1)
		self.tache.rappel=time(8,30,00)
		self.tache.date=soon.date()
		self.tache.save()
		self.close()

	def amelie(self):
		tl=TacheLog(tache=self.tache)
		tl.save()
		if self.tache.tachePapa:
			self.tache.executee=True
		else:
			self.tache.priorite='H'
			amelie=Entite.objects.get(nom="Amelie")
			self.tache.entite.add(amelie)
			self.tache.rappel=None
		self.tache.save()
		self.close()

	def simon(self):
		tl=TacheLog(tache=self.tache)
		tl.save()
		if self.tache.tachePapa:
			self.tache.executee=True
		else:
			self.tache.priorite='H'
			self.tache.rappel=None
		self.tache.save()
		self.close()
	def dateChangee(self,date):
		self.ok.setVisible(True)
	def changeDate(self):
		tl=TacheLog(tache=self.tache)
		tl.save()
		self.tache.rappel=self.rappel.time().toPyTime()
		self.tache.date=self.rappel.date().toPyDate()
		self.tache.save()
		self.close()
	def placeComponents(self):
		tabs=QtGui.QTabWidget()
		fait = QtGui.QPushButton("C'est fait")
		uneH=QtGui.QPushButton("dans 1h")
		deuxH=QtGui.QPushButton("2h")
		soir = QtGui.QPushButton("Ce soir")
		demain = QtGui.QPushButton("Demain matin")
		simon=QtGui.QPushButton("Pour simon")
		amelie=QtGui.QPushButton("Pour amelie")

		r=datetime(self.tache.date.year,self.tache.date.month,self.tache.date.day,self.tache.rappel.hour,self.tache.rappel.minute,self.tache.rappel.second)
		self.rappel=QtGui.QDateTimeEdit(r)
		self.rappel.setCalendarPopup(True)
		self.ok=QtGui.QPushButton("ok")
		self.connect(fait, QtCore.SIGNAL('clicked()'), self.fait)
		self.connect(uneH, QtCore.SIGNAL('clicked()'), self.uneH)
		self.connect(deuxH, QtCore.SIGNAL('clicked()'), self.deuxH)
		self.connect(soir, QtCore.SIGNAL('clicked()'), self.soir)
		self.connect(demain, QtCore.SIGNAL('clicked()'), self.demain)
		self.connect(simon, QtCore.SIGNAL('clicked()'), self.simon)
		self.connect(amelie, QtCore.SIGNAL('clicked()'), self.amelie)
		self.connect(self.ok, QtCore.SIGNAL('clicked()'), self.changeDate)
		self.connect(self.rappel, QtCore.SIGNAL('dateTimeChanged (const QDateTime&)'), self.dateChangee)
		hbox = QtGui.QHBoxLayout()
		hbox2 = QtGui.QHBoxLayout()
		total = QtGui.QHBoxLayout()
		hbox.addWidget(fait)
		hbox.addWidget(uneH)
		hbox.addWidget(deuxH)
		hbox.addWidget(soir)
		hbox.addWidget(demain)
		hbox.addWidget(simon)
		hbox.addWidget(amelie)
		hbox.addWidget(self.rappel)
		hbox.addWidget(self.ok)
		self.ok.setVisible(False)
#		hbox.addWidget(creeAvoir)
		hbox.addStretch(1)
#		hbox.addWidget(self.valider)
#		hbox.addWidget(self.supprimer)
		vbox = QtGui.QVBoxLayout()

		vClient=QtGui.QVBoxLayout()
		vl=QtGui.QHBoxLayout()
#		vl.addWidget(QtGui.QLabel("Nom"))
		vl.addWidget(self.nomClient)
		vClient.addLayout(vl)
		vClient.addStretch()


		vPlusGrandeBox=QtGui.QVBoxLayout()
		vPlusGrandeBox.addLayout(vClient,1)
#		vPlusGrandeBox.addStretch()
		vPlusGrandeBox.addLayout(hbox2,1)

		tabFact=QtGui.QWidget()
		tabFact.setLayout(vPlusGrandeBox)



		vbox.addWidget(tabFact,10)
		vbox.addLayout(hbox,1)
		wi=QtGui.QWidget()
		wi.setLayout(vbox)
		self.setCentralWidget(wi)
		self.nomClient.setFocus(True)


	def center(self):
		screen = QtGui.QDesktopWidget().screenGeometry()
		size =  self.geometry()
		self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2-45)
	
	def stop(self):
		pass
	#	self.calcule()
#		self.metteurAJourTotal.arreteToi()

	def __init__(self,parent=None,tache=None,listeModel=None):
		QtGui.QMainWindow.__init__(self,parent)
		QtGui.QMainWindow.__init__(self)
		icone = QtGui.QIcon('important.png')
		self.setWindowIcon(icone)   
		print(parent)
		print(tache)
		self.l=Lock()
#		self.resize(1200, 670)
		self.center()
		self.tache=Tache.objects.get(id=tache)
	#	self.fact=Facture.objects.get(id=self.facture)
		self.createComponents()
		self.placeComponents()
#		self.updateTitle()
#		self.metteurAJourTotal.start()
#		icone = QtGui.QIcon("ic2.png")
#		self.setWindowIcon(icone)       
	#	self.resize(600, 500)
		self.setWindowTitle(self.tache.description)
		self.setAnimated(True)
		self.activateWindow()

