from PyQt4 import QtCore, QtGui
from kronos import 	ThreadedScheduler
import FenetreTache
import taches.views as taaaches

from datetime import datetime,timedelta,date
import preferences
import webbrowser
from chambres.models import joliePeriode
from easyPoS.models import DonneesEntreprise,LigneFacture,PreparationFacture,Produit,LogFacture
from chambres.models import Client

from chambres.models import Reservation,TourOperateur
import traceback
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QThread,SIGNAL
from easyPoS.models import Facture
import time
import EditionFacture
import sys


import logging


	
class GuetteNouvelles(QThread):
	def __init__(self, parent = None ):
		QThread.__init__(self, parent)
		self.minuteur=None
	def run(self):
		if self.minuteur:
			self.minuteur.stop()
		self.minuteur=ThreadedScheduler()
		today=date.today()
		executions=taaaches.taches(today)
		for t in executions:
			if(t.rappel):
				rap=str(t.rappel).split(":")
				diff=datetime(today.year,today.month,today.day,int(rap[0]),int(rap[1]))-datetime.now()
				if(abs(diff)==diff):
					print(t," pour ",str(t.rappel))
					self.minuteur.add_single_task( self.montreFenetre, "test action 1", diff.days*24*60*60+diff.seconds, "threaded", [t.id], None )
				else:
					pass
		self.minuteur.add_single_task(self.run,"malin le fauve",600,"threaded",[],None)

		self.minuteur.start()
	def montreFenetre(self,id):
		print("montre",id)
		self.emit(SIGNAL("showTache(int)"),id)



class TachesListe(QtGui.QMainWindow):

	def nettoie(self):
		toDelete=[]
		for key,item in self.facturettes.items():
			if not item.isVisible():
				item.stop()
				item.deleteLater()
				toDelete.append(key)
		for i in toDelete:
			del self.facturettes[i]




	def montreFenetre(self,plop):
		id=plop
		if id in self.facturettes:
			self.facturettes[id].setFocus()
			self.facturettes[id].setWindowState(QtCore.Qt.WindowActive)
			self.facturettes[id].activateWindow()
			self.facturettes[id].show()
		else:
			self.facturettes[id]=FenetreTache.EditTache(tache=id,parent=self)
			self.facturettes[id].show()



	def nouvo(self,idFact=0):
		self.montreFenetre(idFact)
		return 
		if idFact<1:
			facture=Facture(etat='B')
			c=Client()
			c.save()
			facture.client=c
			facture.save()
			self.listePrincipaleModel.ajoute(facture)
		else:
			facture=Facture.objects.get(pk=idFact)
			self.listePrincipaleModel.ajoute(facture)



         

		

	def montreTache(self):
		today=date.today()
		executions=taaaches.taches(today)
		for t in executions:
			if(t.rappel):
				rap=str(t.rappel).split(":")
				diff=datetime(today.year,today.month,today.day,int(rap[0]),int(rap[1]))-datetime.now()
				if(abs(diff)==diff) and t.date==date.today():
					pass
				else:
					if not t.estPeriodique():
						self.montreFenetre(t.id)



	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.minuteur=None
		self.guetteNouvelles=GuetteNouvelles()
		self.facturettes={}
#		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.resize(600, 500)
		self.setWindowTitle('Taches')

	
		QtCore.QObject.connect(self.guetteNouvelles, SIGNAL("showTache(int)"), self.nouvo)
		self.guetteNouvelles.start()
		self.montreTache()



