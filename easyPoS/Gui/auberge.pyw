import sys
import traceback
import FenetrePrincipale
import Taches
import AjouteurDeClients
import TachesQuotidiennes 
import EditionFacture
from kronos import     ThreadedScheduler
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QThread,SIGNAL
import subprocess

from chambres.models import Chambre,Souci,Client,Reservation,TacheLog,Tache,Amour,TourOperateur
from collectage.models import Individu
import webbrowser
import os
import time
import urllib
from easyPoS.models import DonneesEntreprise
from datetime import datetime,date,timedelta
from datetime import time as temps
import save
import SauvegardeEtMaintenance
import preferences

import logging

logging.basicConfig(level=preferences.LOGGING_LEVEL)




class MinuteurLanceurDeTaches(QThread):
    def __init__(self, parent = None ):
        """
            init fuction
        """
        logging.info("init shed")
        QThread.__init__(self, parent)
        self.exiting = False
        self.messages=[]
        self.minuteur=None
        self.reinitSched()
        self.demarre=True
    
    def reinitSched(self):
        logging.info("reinit shed")
        if self.minuteur:
            self.minuteur.stop()
        self.minuteur=ThreadedScheduler()
        today=date.today()

        self.minuteur.add_single_task(self.reinitSched,"malin le fauve",600,"threaded",[],None)
        donnees=DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)

        if(donnees.derniereSauvegarde<datetime.now()-timedelta(2) or (donnees.derniereSauvegarde<datetime.now()-timedelta(0.9) and datetime.now().hour>=9)):
            logging.info("On fait maintenance Quotidienne")
            self.minuteur.add_single_task(self.maintenanceQuotidienne,"Truc Quotidien",10,"threaded",[],None)
        if preferences.ENVOIE_CAISSES:
            if donnees.dernierEnvoiCaisses < datetime.now()-timedelta(datetime.now().day) and datetime.now().day>5:
                logging.info("on va envoyer les caisses")
                self.minuteur.add_single_task(self.envoieCaisses,"on envoie les caisses",30,"threaded",[],None)


        self.minuteur.start()
    
    def envoieCaisses(self):
        logging.info("On va envoie caisses")
        from easyPoS.views import encaissementsInsecure,resumeMensuelInsecure,nomMois
        le15DuMoisDernier=date(datetime.now().year,datetime.now().month,15)-timedelta(30)
        resume=str(resumeMensuelInsecure(None,le15DuMoisDernier.year,le15DuMoisDernier.month).content.decode("UTF-8"))
        encaissements=str(encaissementsInsecure(le15DuMoisDernier.year,le15DuMoisDernier.month).content.decode("UTF-8"))
        desc=" de "+nomMois[le15DuMoisDernier.month-1]+" "+str(le15DuMoisDernier.year)
        print(resume)
        SauvegardeEtMaintenance.envoieCaisses(resume,encaissements,desc)
        logging.info("envoi caisses ok")
        donnees=DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
        donnees.dernierEnvoiCaisses=datetime.now()
        donnees.save()


    def maintenanceQuotidienne(self):
        TachesQuotidiennes.go()
    


  
    def __del__(self):
        self.exiting = True
        self.wait()
    
    def affiche(self,t):
        self.messages.append(t)

    def render(self):
        self.start()

    def run(self):
        while not self.exiting :
            if self.demarre:
                time.sleep(5)
                self.emit(SIGNAL("notif()"))
                self.demarre=False
            if self.messages:
                self.emit(SIGNAL("plop(int)"),self.messages.pop())
            else:
                time.sleep(5)
    

class Iconette(QtGui.QWidget):
    """
    petite icone
    """

    def __init__(self, app,parent = None,):
        QtGui.QWidget.__init__(self, parent)
        self.demarreServeur()
        self.app=app
        self.thread=MinuteurLanceurDeTaches()
        self.createActions()
        self.createTrayIcon()
        self.trayIcon.show()
        self.msgBox=[]

    def mmm(self):
        self.trayIcon.showMessage("Bonjour","Bienvenue")
        #self.trayIcon.showMessage("Bonjour","Bienvenue, pour ouvrir le resume du jour double cliquez sur l'icone, ou clic droit+\"ouvrir resume\"\n Si cela ne marche pas, essayer eventuellement clic droit+ Redemarrer serveur")
    


    def demarreServeur(self):
        pass
        if preferences.LANCER_SERVEUR:
            try:
                logging.info("try open localhost")
                urllib2.urlopen("https://127.0.0.1")    
                logging.info("end try open localhost")
            except:
                logging.info("on lance serveur")
                self.enfant=subprocess.Popen(["python","manage.py","runserver"],cwd=os.path.abspath(".."),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                time.sleep(2)
                logging.info(dir(self.enfant))
                logging.info(dir(self.enfant.stdout))
                logging.info(self.enfant.returncode)

    def ouvrir(self):
        webbrowser.open("https://127.0.0.1/chambres/today")
    def heures(self):
        webbrowser.open("https://127.0.0.1/heures")


    def redemarrer(self):
        try:
            self.enfant.kill()
        except:
            pass
        self.demarreServeur()

    def createActions(self):
        self.ouvrirResumAction = QtGui.QAction(self.tr("&Ouvrir resume d'aujourd'hui"), self)
        self.heuresAction = QtGui.QAction(self.tr("&Ouvrir gestions des heures"), self)
#        self.ajouteurClient = QtGui.QAction(self.tr("&Ajouteur de clients"), self)
        self.redemarrerAction = QtGui.QAction(self.tr("&Redemarrer programme"), self)
        self.posAction = QtGui.QAction(self.tr("&Facturation"), self)
        self.quitAction = QtGui.QAction(self.tr("&Quitter"), self)
        QtCore.QObject.connect(self.quitAction, QtCore.SIGNAL("triggered()"),    QtGui.qApp, QtCore.SLOT("quit()"))
        QtCore.QObject.connect(self.redemarrerAction, QtCore.SIGNAL("triggered()"),    self.redemarrer)
        QtCore.QObject.connect(self.heuresAction, QtCore.SIGNAL("triggered()"),    self.heures)
#        QtCore.QObject.connect(self.ajouteurClient, QtCore.SIGNAL("triggered()"),    self.ajouteur)
        QtCore.QObject.connect(self.posAction, QtCore.SIGNAL("triggered()"),    self.montreFenetre)
        QtCore.QObject.connect(self.ouvrirResumAction, QtCore.SIGNAL("triggered()"),    self.ouvrir)
        QtCore.QObject.connect(self.thread, SIGNAL("notif()"), self.mmm)
        self.thread.start()

#    def ajouteur(self):
#        a.show()
    def montreFenetre(self):
        f.show()

    def active(self,reason):
        if reason == QtGui.QSystemTrayIcon.Unknown:
            pass
        elif reason== QtGui.QSystemTrayIcon.Context:
            pass
        elif reason== QtGui.QSystemTrayIcon.DoubleClick:
            self.montreFenetre()
        elif reason== QtGui.QSystemTrayIcon.Trigger:
            pass
        elif reason ==QtGui.QSystemTrayIcon.MiddleClick:
            pass
    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.ouvrirResumAction)
        self.trayIconMenu.addAction(self.heuresAction)
#        self.trayIconMenu.addAction(self.ajouteurClient)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.redemarrerAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.posAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        QtCore.QObject.connect(self.trayIcon,QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),self.active)
        self.trayIcon.setToolTip("Bonjour")
        self.trayIcon.setIcon(QIcon('ic2.png'))

app = QtGui.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
f=FenetrePrincipale.Fenetre()
#a=AjouteurDeClients.Ajouteur()
f.show()
t=Taches.TachesListe()
#t.show()
x = Iconette(app)
#x.show()
sys.exit(app.exec_())

