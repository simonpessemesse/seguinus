import sys
from PyQt4 import QtGui

from chambres.models import Tache
from datetime import date

#!/usr/bin/python3

# simple.py


class InputDialog(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)

		self.setGeometry(300, 300, 350, 80)
		self.setWindowTitle('InputDialog')
		self.showDialog()

		

	
	def showDialog(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Ajoute')
		if ok:
			t=Tache(description=text,date=date.today())
			t.save()
		sys.exit()



app = QtGui.QApplication(sys.argv)
idlg = InputDialog()
idlg.show()
app.exec_()

