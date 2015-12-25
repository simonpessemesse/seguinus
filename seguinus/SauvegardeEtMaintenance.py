import sys
import preferences
import traceback
import bz2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.encoders import encode_base64
import zipfile
from crypto.crypteEtSauveMonBiniou import Crypteuse
import os
import save
import subprocess
from datetime import timedelta,datetime,date

import logging
logging.basicConfig(level=preferences.LOGGING_LEVEL)




## WE HAVE TO PUT IN .HG/HGRC THE CONFIGFILE WITH NAME OTHERWISE IT DOESNT COMMIT
if os.name=="posix":
	hg="hg"
elif os.name=="nt":
	hg="..\..\EnvironnementDeTravail\Mercurial\hg.exe "


databasePath=os.path.abspath(".."+os.sep+".."+os.sep+"DONNEES")


def zippe(file,archive,nom):
	zfilename = archive
	zout = zipfile.ZipFile(zfilename, "w",zipfile.ZIP_DEFLATED)
	zout.write(file,nom)
	zout.close()

def sendMail(to, subject, text, files=[],server=preferences.SERVEUR_SMTP):
	assert type(to)==list
	assert type(files)==list
	fro = "Expediteur <"+preferences.EXPEDITEUR+">"

	msg = MIMEMultipart()
	msg['From'] = fro
	msg['To'] = COMMASPACE.join(to)
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = subject

	msg.attach( MIMEText(text) )

	for file in files:
		part = MIMEBase('application', "octet-stream")
		part.set_payload( open(file,"rb").read() )
		encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"'
					   % os.path.basename(file))
		msg.attach(part)

	logging.info("le serveur smtp est "+ server )
	smtp = smtplib.SMTP(server)
	smtp.sendmail(fro, to, msg.as_string() )
	smtp.close()


def compresseEtSupprimeFichier(fileToCompress,finalName):
	sToSave= open(fileToCompress,'rb')
	compresse=bz2.compress((sToSave.read()))
	fFinal=open(finalName,"wb")
	fFinal.write(compresse)
	fFinal.close()
	os.remove(fileToCompress)


def EnvoieParMail(fileToSave,crypte=False):
	logging.info("debut envoie par mail")
	import platform
	tex="salutations "+str(platform.uname())
	if(crypte):
		logging.info("On crypte")
		archive="db.gpg"
		c=Crypteuse()
		c.crypteFichier(fileToSave,archive)
	else:
		nomFichier="db"+str(date.today())+".json.bz2"
		logging.info("on compresse 1iere frois "+nomFichier)
		compresseEtSupprimeFichier(fileToSave,nomFichier)
		c=Crypteuse()
		logging.info("on crypte "+nomFichier)
		c.crypteFichier(nomFichier,nomFichier+".gpg")
		os.remove(nomFichier)
		nomFichier=nomFichier+".gpg"
		logging.info("on compresse2Fois "+nomFichier)
		compresseEtSupprimeFichier(nomFichier,nomFichier+".bz2")
		logging.info("on envoie par mail a "+preferences.DESTINATAIRE+" le fic "+nomFichier+".bz2")
	sendMail(
    	    [preferences.DESTINATAIRE],
        	"sauvegarde",tex,
        	[nomFichier+".bz2"]
	    )
	os.remove(nomFichier+".bz2")



def autocommitLesDonnees():
	os.chdir(databasePath)
	os.system(hg+" commit -m \"autoCommit\"")

def autoPushLesDonnees():
	os.chdir(databasePath)
	os.system(hg+" push command ")

def envoieParMailLesDonnees():
	save.EnvoieParMail()

def getLastCodeVersion():
#TODO put real repository
	commandes= [" pull  "," revert --all "," update "]
	for i in commandes:
		os.system(hg+i)

def getLastDatabaseVersion():
#TODO put real repository
	os.chdir(databasePath)
	commandes= [" pull  "," revert --all "," update "]
	for i in commandes:
		os.system(hg+i)

def envoieOccupation(texte):
	pass
#	sendMail([preferences.OFFICE_TOURISME,preferences.CC],"Occupation de l'Auberge des Seguins pour les prochains jours",texte,[])

def envoieCaisses(resume,encaissements,desc):
	nCaisse="caisse "+desc+".html"
	caisse=open(nCaisse,"w")
	caisse.write(encaissements)
	caisse.close()
	nResum="resume "+desc+".html"
	resum=open(nResum,"w")
	resum.write(resume)
	resum.close()
	print(("on devrait envoyer"+str(preferences.DESTINATAIRE_CAISSES)))
	sendMail(
    	    [preferences.DESTINATAIRE_CAISSES],
        	"a envoyer a la comptable","NE PAS OUBLIER DE RAJOUTER LES DEUX DERNIERS RELEVES DE BANQUE \n Voici le resume et les encaissements "+desc,
        	[nCaisse,nResum]
	    )
	os.remove(nCaisse)
	os.remove(nResum)

def dumpDatabase():
	logging.info("on est dans dump")
	logging.info(" path is "+os.getcwd())
	initD=os.getcwd()
	if "Gui" in initD:
		os.chdir("..")

	commande=" manage.py dumpdata "
	fichier=open("data.json","w")
	enfant=subprocess.Popen(["python","manage.py","dumpdata","--indent=1","chambres","restaurant","collectage","easyPoS","menus","taches","telephones","siteweb" ],cwd=os.path.abspath("."),stdout=fichier,stderr=subprocess.STDOUT)
	enfant.wait()
	fichier.close()
#	envoieASelvaListe()
	EnvoieParMail("data.json")
	os.chdir(initD)

def envoieASelvaListe():
	import urllib.request, urllib.error, urllib.parse
	joursFichiers=[(1,"demain.html"),(2,"apresDemain.html")]
	for (j,f) in joursFichiers:
		dem=datetime.now()+timedelta(j)
		urll="http://127.0.0.1:8000/chambres/"+str(dem.year)+"/"+str(dem.month)+"/"+str(dem.day)+"/"+"imprimerCh"
		logging.info(urll)
		res=urllib.request.urlopen(urll)
#	logging.info res.read()
		fii=open(f,"w")
		fii.write(res.read())
		fii.flush()
	fich=[f for (j,f) in joursFichiers]
#	sendMail(
 #   	    [""],
  #      	"menage","voila!! ",
   #     	fich
	#    )
	

	 #os.system(commande)

paramAndFunction={'commitD':autocommitLesDonnees,'pushD':autoPushLesDonnees,'mailD':envoieParMailLesDonnees,'getLastVer':getLastCodeVersion,'getDBVer':getLastDatabaseVersion,'dump':dumpDatabase,'selva':envoieASelvaListe}

def showErr():
	logging.info("GEEEE path " +os.getcwd())
	print("params are:\n")
	print(("\n".join(list(paramAndFunction.keys()))))
if __name__=='__main__':
	if(len(sys.argv)<2):
		print("No parameter passed\n ")
		showErr()
	else:
		param=sys.argv[1]
		if(param in list(paramAndFunction.keys())):
			paramAndFunction[param]()
			print("trouve")
		else:
			print("bad param\n ")
			showErr()
#	autocommitLesDonnees()
