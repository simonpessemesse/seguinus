from PyQt4 import QtCore, QtGui
import django
django.setup()
from datetime import datetime,timedelta
import preferences
import webbrowser
from chambres.models import joliePeriode
from easyPoS.models import DonneesEntreprise,LigneFacture,PreparationFacture,Produit,LogFacture,RelationReservationFacture
from log.models import Log
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
from  PreRemplissageFacture import prepare





def joli(chiffre):
	s=str(chiffre)
	li=s.split(".")
	if len(li)>1:
		a,b=li
		return a+"."+b[0:2]
	else:
		return s
	
class GuetteNouvelles(QThread):
	def __init__(self, parent = None ):
		QThread.__init__(self, parent)
	def run(self):
		while True:
			time.sleep(1)
			prepas=PreparationFacture.objects.all()
			for i in prepas:
				if i.resa:
					f=prepare(i.resa)
					f.updateCache()
					idAVoir=f.id
					f.save()
				else:
					idAVoir=i.resaId
				self.emit(SIGNAL("nouvelleFacture(int)"),idAVoir)
				i.delete()
	


class MetteurAJourListe(QThread):
	def __init__(self, parent = None, liste=None ):
		QThread.__init__(self, parent)
		self.liste=liste
	def run(self):
		while True:
			time.sleep(20)
			self.emit(SIGNAL("notif()"))

class ListePrincipaleModel(QtCore.QAbstractListModel): 
	def __init__(self, parent=None,brouillons=True, fen=None, val50=False,valnp=True,viei=False,devis=False,*args): 
		""" datain: a list where each item is a row
		"""
		QtCore.QAbstractListModel.__init__(self, parent, *args) 
		self.fen=fen
		factsVal=None
		ent=self.fen.entreprise
		if(brouillons):
			facts=Facture.objects.filter(entreprise=ent).filter(etat='B').order_by('id')
		if(val50):
			factsVal=Facture.objects.filter(entreprise=ent).filter(etat='V').order_by('-numero')[:50]
			factsVal=list(factsVal)
			factsVal.reverse()
		if(valnp):
			factNonPaye=Facture.objects.filter(entreprise=ent).filter(cacheTotalDu__gt=0).filter(etat='V')
			factNonPaye2=set(Facture.objects.filter(entreprise=ent).filter(cacheTotalDu__lt=0).filter(etat='V')).union(set(factNonPaye))
			self.listdata=sorted(factNonPaye2,key=lambda f:f.numero)
		else:
			self.listdata=[]
		if(val50):
			self.listdata.extend(list(factsVal))
		if(brouillons):
			self.listdata.extend(list(facts))

		if not devis:
			todel=[]
			for f in self.listdata:
				if "devis" in f.clientNomFinal.lower() or "devis" in f.client.nom.lower():
					todel.append(f)
			for f in todel:
				self.listdata.remove(f)

		if not viei:
			newList=[]
			for i in self.listdata:
				if i.creation > datetime.now()-timedelta(2) or i.toujoursVisible:
					newList.append(i)
			newList=sorted(newList,key=lambda i: i.id)
			self.listdata=newList
	

	def totalChange(self,fact):
		#traceback.print_stack(limit=5)
		ind=0
		for i in range(0,len(self.listdata)):
			if self.listdata[i]==fact:
				ind=i
		modelIndex=self.index(ind)
		self.emit(SIGNAL("dataChanged (const QModelIndex&,const QModelIndex&)"),modelIndex,modelIndex)
	
	def ajoute(self,fact):
		self.listdata.append(fact)
		inddd=len(self.listdata)
		ind=self.createIndex(inddd,inddd)
		self.emit(SIGNAL("rowsInserted (const QModelIndex&,int,int)"),ind,1,1) 

	def rowCount(self, parent=QtCore.QModelIndex()): 
		return len(self.listdata) 


	def supprime(self,fact):
		ind=0
		print((" on supp "+str(ind)))
		for i in range(0,len(self.listdata)):
			if self.listdata[i]==fact:
				ind=i
	#	modelIndex=self.index(ind)
	#	self.emit(SIGNAL("rowsRemoved (const QModelIndex&,int,int)"),modelIndex,i,i+1)
		self.listdata.remove(fact)
		print((" on supp "+str(ind)))
		self.removeRow(ind)



	def getId(self,row):
		return self.listdata[row].id

	def formatteTexte(self,f):
		res=joli(f.cacheTotal)+" Eur\t"
		res+="Du: "+joli(f.cacheTotalDu)+"\t"
		if f.nomClient() != "":
			res+="client: "+f.nomClient()+"\t"
		if f.etat=='V':
			res+=str(f.numero)+" VALIDE "
		#	if f.totalDu()!=0:
		#		res+="NON PAYE "
			if f.cacheTotalDu!=0:
				res+="NON PAYE "
	#	res+=str(f.id)+" du "
	#	if f.dateVente:
	#	res+=str(f.dateVente.day)+"/"+str(f.dateVente.month)+"/"+str(f.dateVente.year)+" "
	#	else: 
	#		res+=str(f.creation.day)+"/"+str(f.creation.month)+"/"+str(f.creation.year)+" "
		#res+=" montant: "+ str(f.total())
		return res
 
	def data(self, index, role): 
		if index.isValid() and role == 0: # 0 est egal a Qt.DisplayRole
			fact=self.listdata[index.row()]
			ss=self.formatteTexte(fact)
			return ss
		elif role==1: # DecorationRole
			fact=self.listdata[index.row()]
			if fact.cacheTotalDu and fact.cacheTotalDu!=0 :
				if fact.cacheTotalDu<0:
					return QtGui.QColor("pink")
				elif fact.etat=='V':
					return QtGui.QColor("black")
				else:
					g=fact.paiement_set.all()
					return QtGui.QColor("red")
			if fact.etat=='V':
				return QtGui.QColor("green")
			if fact.etat=='B':
				g=fact.paiement_set.all()
				return QtGui.QColor("blue")
		else: 
			return None


class Fenetre(QtGui.QMainWindow):

	def nettoie(self):
		toDelete=[]
		for key,item in self.facturettes.items():
			if not item.isVisible():
				item.stop()
				item.deleteLater()
				toDelete.append(key)
		for i in toDelete:
			del self.facturettes[i]



	def test2(self,plop):
		myModel=plop.model()
		row=plop.row()
		id=myModel.getId(row)
		self.montreFenetre(id)

	def montreFenetre(self,plop):
		id=plop
		if id in self.facturettes:
			self.facturettes[id].setFocus()
			self.facturettes[id].setWindowState(QtCore.Qt.WindowActive)
			self.facturettes[id].activateWindow()
			self.facturettes[id].show()
		else:
			self.facturettes[id]=EditionFacture.EditFacture(facture=id,listeModel=self.listePrincipaleModel,fenetrePrincipale=self)
			self.facturettes[id].show()


	def cloneMoiCa(self,fact):
		ent=self.entreprise
		if not ent.actif:
			return
		facture=Facture(entreprise=ent,etat='B')
#		donnees=DonneesEntreprise.objects.get(id=1)
#		facture.numero=donnees.numeroFactureCourante
		facture.save()
		c=Client()
		c.save()
		facture.client=c
		for i in fact.lignefacture_set.all():
			ligne=LigneFacture(produit=i.produit,famille=i.famille,facture=facture,prixUnitaireFinal=i.prixUnitaireFinal,quantite=i.quantite,position=i.position,tauxTvaFinal=i.tauxTvaFinal)
			ligne.save()
		facture.save()

		self.montreFenetre(facture.id)
		self.listePrincipaleModel.ajoute(facture)

	def nouvo(self,idFact=0):
		ent=self.entreprise
		if not ent.actif:
			return
		if idFact<1:
			facture=Facture(entreprise=ent,etat='B')
#		donnees=DonneesEntreprise.objects.get(id=1)
#		facture.numero=donnees.numeroFactureCourante
			c=Client()
			c.save()
			facture.client=c
			facture.save()
			self.listePrincipaleModel.ajoute(facture)
		else:
			facture=Facture.objects.get(pk=idFact)
			self.listePrincipaleModel.ajoute(facture)

		self.montreFenetre(facture.id)


	def chercheLePaiement(self):
		text,ok=QtGui.QInputDialog.getText(self, self.tr("QInputDialog.getText()"),
                                          self.tr("Quelle paiement cherchez vous? "), QtGui.QLineEdit.Normal                                        );
		if (ok and  text!=""):
			webbrowser.open(preferences.URL+"/easyPoS/factures/cherchePaiement/"+text)

	def chercheLeNumero(self):
		text,ok=QtGui.QInputDialog.getText(self, self.tr("QInputDialog.getText()"),
                                          self.tr("Quelle numero vous? "), QtGui.QLineEdit.Normal                                        );
		if (ok and  text!=""):
			webbrowser.open(preferences.URL+"/easyPoS/factures/chercheNumero/"+text)
	def chercheLaValeur(self):
		text,ok=QtGui.QInputDialog.getText(self, self.tr("QInputDialog.getText()"),
                                          self.tr("Quelle valeur vous? "), QtGui.QLineEdit.Normal                                        );
		if (ok and  text!=""):
			webbrowser.open(preferences.URL+"/easyPoS/factures/chercheValeur/"+text)

	def chercheFacture(self):
		text,ok=QtGui.QInputDialog.getText(self, self.tr("QInputDialog.getText()"),
                                          self.tr("Que cherchez vous? "), QtGui.QLineEdit.Normal                                        );
		if (ok and  text!=""):
			webbrowser.open(preferences.URL+"/easyPoS/factures/cherche/"+text)
         

	def chkChanged(self):
		self.nettoie()

		viei=self.viei.isChecked()
		bro= self.bro.isChecked()
		val50= self.val50.isChecked()
		valnp= self.valnp.isChecked()
		devis= self.devis.isChecked()
		self.listePrincipaleModel = ListePrincipaleModel(self,brouillons=bro,fen=self,val50=val50,valnp=valnp,viei=viei,devis=devis)
		self.lv.setModel(self.listePrincipaleModel)
	
	def entrepriseChanged(self):
		boutons=self.checks
		for b,e in boutons:
			if b.isChecked():
				self.entreprise=e
				self.chkChanged()
	def createComponents(self):
		self.tableLabel1 = QtGui.QLabel("Table &1")
		self.tableView1 = QtGui.QTableView()
		self.tableLabel1.setBuddy(self.tableView1)
		header = self.tableView1.horizontalHeader()

		self.listePrincipaleModel = ListePrincipaleModel(self,fen=self)

		self.hbox = QtGui.QHBoxLayout()
		vbox = QtGui.QVBoxLayout()
		self.val50=QtGui.QCheckBox("Afficher 50 Derniers Valides")
		self.bro=QtGui.QCheckBox("Afficher Brouillons")
		self.viei=QtGui.QCheckBox("Afficher Vieilles Factures")
		self.valnp=QtGui.QCheckBox("Afficher Valides Non Paye")
		self.devis=QtGui.QCheckBox("Afficher Devis")
		self.bro.setChecked(True)
		self.valnp.setChecked(True)
		QtCore.QObject.connect(self.val50, SIGNAL("stateChanged (int)"), self.chkChanged)
		QtCore.QObject.connect(self.bro, SIGNAL("stateChanged (int)"), self.chkChanged)
		QtCore.QObject.connect(self.viei, SIGNAL("stateChanged (int)"), self.chkChanged)
		QtCore.QObject.connect(self.valnp, SIGNAL("stateChanged (int)"), self.chkChanged)
		QtCore.QObject.connect(self.devis, SIGNAL("stateChanged (int)"), self.chkChanged)
		vbox.addWidget(self.bro)
		vbox.addWidget(self.valnp)
		vbox.addWidget(self.val50)
		vbox.addWidget(self.viei)
		vbox.addWidget(self.devis)
		vbox.addStretch()
		self.lv = QtGui.QListView()
		self.lv.setAlternatingRowColors(True)
		self.lv.setModel(self.listePrincipaleModel)
		f=QtGui.QFont('Helvetica',8)
		self.lv.setFont(f)

		self.hbox.addWidget(self.lv)
		self.hbox.addLayout(vbox)
		QtCore.QObject.connect(self.lv, SIGNAL("clicked (const QModelIndex&) "), self.test2)

		self.add=QtGui.QPushButton("Nouvelle")
		self.list = QtGui.QListWidget()
		QtCore.QObject.connect(self.list, SIGNAL("itemClicked (QListWidgetItem *)"), self.montreFenetre)
		new=QtGui.QAction('Nouvelle Facture',self)
		self.ref=QtGui.QAction('Rafraichir',self)
		self.cherche=QtGui.QAction('Chercher une facture',self)
		self.chercheNumero=QtGui.QAction('Chercher une facture par numero',self)
		self.chercheValeur=QtGui.QAction('Chercher une valeur',self)
		self.cherchePaiement=QtGui.QAction('Chercher un paiement',self)
		new.setShortcut('Ctrl+N')
		self.nettoieLogs=QtGui.QAction('Nettoie Logs',self)

		self.autoFerme=QtGui.QAction('Auto Fermeture',self,checkable=True)
		self.fermeAutomatique=False

		checks=[]
		entreprises=DonneesEntreprise.objects.all()
		ag=QtGui.QActionGroup(self)
		for e in entreprises:
			ac=QtGui.QAction(e.denomination,self,checkable=True)
			ac.setActionGroup(ag)
			if e.id==preferences.ENTREPRISE:
				ac.setChecked(True)
			self.connect(ac,QtCore.SIGNAL('toggled(bool)'),self.entrepriseChanged)
			checks.append((ac,e))

		self.checks=checks
		self.resum=QtGui.QAction('Resume',self)
		self.clean=QtGui.QAction('Nettoie',self)
		self.connect(new, QtCore.SIGNAL('triggered()'), self.nouvo)
		self.connect(self.ref, QtCore.SIGNAL('triggered()'), self.chkChanged)
		self.connect(self.cherche, QtCore.SIGNAL('triggered()'), self.chercheFacture)
		self.connect(self.chercheValeur, QtCore.SIGNAL('triggered()'), self.chercheLaValeur)
		self.connect(self.chercheNumero, QtCore.SIGNAL('triggered()'), self.chercheLeNumero)
		self.connect(self.cherchePaiement, QtCore.SIGNAL('triggered()'), self.chercheLePaiement)
		self.connect(self.nettoieLogs, QtCore.SIGNAL('triggered()'), self.netLogs)
		self.connect(self.autoFerme, QtCore.SIGNAL('toggled(bool)'), self.fermetureAutomatique)
		self.connect(self.resum, QtCore.SIGNAL('triggered()'), self.resume)
		self.connect(self.clean, QtCore.SIGNAL('triggered()'), self.allege)
		self.new=new
		exit = QtGui.QAction('Exit', self)	
		exit.setShortcut('Ctrl+Q')
		exit.setStatusTip('Exit application')
		self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
		self.exit=exit
		
	def allege(self):
		import cleanDb
		cleanDb.allege()
	def resume(self):
		webbrowser.open(preferences.URL+"/easyPoS/")
	def fermetureAutomatique(self,bol):
		if bol:
			self.fermeAutomatique=True
		else:
			self.fermeAutomatique=False
	def netLogs(self):
		ent=self.entreprise
		fc=Facture.objects.filter(entreprise=ent).filter(etat="C")
		for f in fc:
			f.delete()
			print(f)
		fs=Facture.objects.filter(entreprise=ent)
		for f in fs:
			f.updateCache()
		logs=Log.objects.exclude(facture__etat='B')
		for i in logs:
			if i.facture and i.facture.totalDu()==0:
			#deb+=str(i)+str(i.facture)+"\n"
				i.delete()
		
	def placeComponents(self):
		wi=QtGui.QWidget()
		wi.setLayout(self.hbox)
		self.setCentralWidget(wi)


	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.facturettes={}
		self.metteurAJour=MetteurAJourListe()
		self.guetteNouvelles=GuetteNouvelles()
#		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.resize(600, 500)
		self.setWindowTitle('Easy PoS')

		ent=DonneesEntreprise.objects.get(pk=preferences.ENTREPRISE)
		self.entreprise=ent
		self.createComponents()
		self.placeComponents()
		
	
		self.statusBar()
		menubar = self.menuBar()
		file = menubar.addMenu('&File')
		file.addAction(self.new)
		file.addAction(self.resum)
		file.addAction(self.cherche)
		file.addAction(self.chercheValeur)
		file.addAction(self.cherchePaiement)
		file.addAction(self.chercheNumero)
		file.addAction(self.exit)
		if preferences.MONTRE_NETTOIE:	
			file = menubar.addMenu('&Divers')
	
			file.addAction(self.clean)
		file=menubar.addMenu('&Utilitaires')
		file.addAction(self.nettoieLogs)
		file.addAction(self.autoFerme)
		for b,e in self.checks:
			file.addAction(b)

		toolbar = self.addToolBar('Exit')
		toolbar.addAction(self.new)
		toolbar.addAction(self.resum)
		toolbar.addAction(self.ref)
		toolbar.addAction(self.exit)

		icone = QtGui.QIcon("ic2.png")
		self.setWindowIcon(icone)        
		QtCore.QObject.connect(self.metteurAJour, SIGNAL("notif()"), self.chkChanged)
		QtCore.QObject.connect(self.guetteNouvelles, SIGNAL("nouvelleFacture(int)"), self.nouvo)
		self.metteurAJour.start()
		self.guetteNouvelles.start()

#		setIcon(QIcon('ic2.png'))

