from PyQt4 import QtCore, QtGui
from chambres.models import Client, Reservation
import webbrowser
from PyQt4.QtCore import SIGNAL
import datetime
from datetime import date


class Ajouteur(QtGui.QMainWindow):
    def test2(self, plop):
        myModel = plop.model()
        row = plop.row()
        id = myModel.getId(row)
        self.montreFenetre(id)

    def montreFenetre(self, plop):
        id = plop
        if id in self.facturettes:
            self.facturettes[id].setFocus()
            self.facturettes[id].setWindowState(QtCore.Qt.WindowActive)
            self.facturettes[id].activateWindow()
            self.facturettes[id].show()
        else:
            self.facturettes[id] = EditionFacture.EditFacture(facture=id, listeModel=self.listePrincipaleModel)
            self.facturettes[id].show()

    def nouvo(self):
        nom = self.nom.text()
        divers = self.divers.text()
        if nom == "":
            self.erreur()
            return
        print(nom)

        s = self.arrivee.selectedDate()
        arrivee = date(s.year(), s.month(), s.day())
        s = self.depart.selectedDate()
        depart = date(s.year(), s.month(), s.day())
        sin = self.single.value()
        double = self.double.value()
        twin = self.twin.value()
        triple = self.triple.value()
        quadruple = self.quadruple.value()
        quintuple = self.quintuple.value()
        dortoir = self.dortoir.value()
        if sin + double + twin + triple + quadruple + quintuple + dortoir == 0:
            self.erreur()
            return

        client = Client(nom=str(nom), divers=str(divers))
        client.save()
        resa = Reservation(client=client, dateArrivee=arrivee, dateDepart=depart, chambresSingle=sin,
                           chambresDoubles=double, chambresTwin=twin, chambresTriples=triple,
                           chambresQuadruples=quadruple, chambresQuintuples=quintuple, placesDortoir=dortoir)
        resa.save()

        self.risette()

    def erreur(self):
        print("ERREUR")

    def risette(self):
        self.nom.setText("")
        self.single.setValue(0)
        self.double.setValue(1)
        self.twin.setValue(0)
        self.triple.setValue(0)
        self.quadruple.setValue(0)
        self.quintuple.setValue(0)
        self.dortoir.setValue(0)
        self.divers.setText("")

    def chkChanged(self):
        bro = False
        if self.bro.isChecked():
            bro = True
        val = False
        if self.val.isChecked():
            val = True
        self.listePrincipaleModel = ListePrincipaleModel(self, valides=val, brouillons=bro)
        self.lv.setModel(self.listePrincipaleModel)

    def getNom(self):
        self.noml = QtGui.QLabel("Nom")
        self.nom = QtGui.QLineEdit()
        nomBox = QtGui.QHBoxLayout()
        nomBox.addWidget(self.noml)
        nomBox.addWidget(self.nom)
        return nomBox

    def getArrivee(self):
        self.noml = QtGui.QLabel("Arrivee")
        self.arrivee = QtGui.QCalendarWidget()
        nomBox = QtGui.QHBoxLayout()
        nomBox.addWidget(self.noml)
        nomBox.addWidget(self.arrivee)
        return nomBox

    def getDepart(self):
        self.noml = QtGui.QLabel("Depart")
        self.depart = QtGui.QCalendarWidget()
        nomBox = QtGui.QHBoxLayout()
        nomBox.addWidget(self.noml)
        nomBox.addWidget(self.depart)
        return nomBox

    def getSingle(self):
        self.noml = QtGui.QLabel("Single")
        self.single = QtGui.QSpinBox()
        nomBox = QtGui.QHBoxLayout()
        nomBox.addWidget(self.noml)
        nomBox.addWidget(self.single)
        return nomBox

    def getDouble(self):
        self.noml = QtGui.QLabel("Double")
        self.double = QtGui.QSpinBox()
        nomBox = QtGui.QHBoxLayout()
        self.double.setValue(1)
        nomBox.addWidget(self.noml)
        nomBox.addWidget(self.double)
        return nomBox

    def getTwin(self):
        self.noml = QtGui.QLabel("Twin")
        self.twin = QtGui.QSpinBox()
        nomBox = QtGui.QHBoxLayout()
        nomBox.addWidget(self.noml)
        nomBox.addWidget(self.twin)
        return nomBox

    def getTriple(self):
        self.noml = QtGui.QLabel("Triple")
        self.triple = QtGui.QSpinBox()
        nomBox = QtGui.QHBoxLayout()
        nomBox.addWidget(self.noml)
        nomBox.addWidget(self.triple)
        return nomBox

    def getQuadruple(self):
        self.noml = QtGui.QLabel("Quadruple")
        self.quadruple = QtGui.QSpinBox()
        nomBox = QtGui.QHBoxLayout()
        nomBox.addWidget(self.noml)
        nomBox.addWidget(self.quadruple)
        return nomBox

    def getQuintuple(self):
        self.noml = QtGui.QLabel("Quintuple")
        self.quintuple = QtGui.QSpinBox()
        nomBox = QtGui.QHBoxLayout()
        nomBox.addWidget(self.noml)
        nomBox.addWidget(self.quintuple)
        return nomBox

    def getDortoir(self):
        self.noml = QtGui.QLabel("Dortoir")
        self.dortoir = QtGui.QSpinBox()
        nomBox = QtGui.QHBoxLayout()
        nomBox.addWidget(self.noml)
        nomBox.addWidget(self.dortoir)
        return nomBox

    def getTourOp(self):
        self.noml = QtGui.QLabel("TourOp")
        self.tourOp = QtGui.QComboBox()
        nomBox = QtGui.QHBoxLayout()
        nomBox.addWidget(self.noml)
        nomBox.addWidget(self.tourOp)
        return nomBox

    def getDivers(self):
        self.noml = QtGui.QLabel("Divers")
        self.divers = QtGui.QLineEdit()
        nomBox = QtGui.QHBoxLayout()
        nomBox.addWidget(self.noml)
        nomBox.addWidget(self.divers)
        return nomBox

    def createComponents(self):
        self.hbox = QtGui.QHBoxLayout()
        vbox = QtGui.QVBoxLayout()
        self.bro = QtGui.QCheckBox("Afficher Brouillons")
        self.bro.setChecked(True)
        vbox.addLayout(self.getNom())
        vbox.addLayout(self.getArrivee())
        vbox.addLayout(self.getDepart())
        vbox.addLayout(self.getDivers())
        vbox2 = QtGui.QVBoxLayout()
        vbox2.addLayout(self.getSingle())
        vbox2.addLayout(self.getDouble())
        vbox2.addLayout(self.getTwin())
        vbox2.addLayout(self.getTriple())
        vbox2.addLayout(self.getQuadruple())
        vbox2.addLayout(self.getQuintuple())
        vbox2.addLayout(self.getDortoir())
        vbox2.addLayout(self.getTourOp())
        #	vbox.addWidget(QtGui.QCheckBox("Afficher Oublies"))
        vbox2.addStretch()
        self.add = QtGui.QPushButton("Sauver et ajouter")
        vbox2.addWidget(self.add)
        self.hbox.addLayout(vbox)
        self.hbox.addLayout(vbox2)

        new = QtGui.QAction('Sauver et ajouter', self)
        new.setShortcut('Ctrl+W')
        self.connect(new, QtCore.SIGNAL('triggered()'), self.nouvo)
        self.new = new
        exit = QtGui.QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.exit = exit

    def resume(self):
        webbrowser.open("http://127.0.0.1:8000/factures")

    def placeComponents(self):
        wi = QtGui.QWidget()
        wi.setLayout(self.hbox)
        self.setCentralWidget(wi)

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        #		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.resize(200, 500)
        self.setWindowTitle('Ajouteur')

        self.createComponents()
        self.placeComponents()

        self.statusBar()
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(self.new)
        file.addAction(self.exit)
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(self.new)
        toolbar.addAction(self.exit)
