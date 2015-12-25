import smtplib

import preferences

from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase

from email.mime.text import MIMEText

from email.utils import COMMASPACE, formatdate

import email.encoders 

import os

import zipfile

from crypto.crypteEtSauveMonBiniou import Crypteuse



def zippe(file,archive,nom):

	zfilename = archive

	zout = zipfile.ZipFile(zfilename, "w",zipfile.ZIP_DEFLATED)

	zout.write(file,nom)

	zout.close()





def sendMail(to, subject, text, files=[],server=preferences.SERVEUR_SMTP):

    assert type(to)==list

    assert type(files)==list

    fro = "sauvegardeur <"+preferences.EXPEDITEUR+">"



    msg = MIMEMultipart()

    msg['From'] = fro

    msg['To'] = COMMASPACE.join(to)

    msg['Date'] = formatdate(localtime=True)

    msg['Subject'] = subject



    msg.attach( MIMEText(text) )



    for file in files:

        part = MIMEBase('application', "octet-stream")

        part.set_payload( open(file,"rb").read() )

        Encoders.encode_base64(part)

        part.add_header('Content-Disposition', 'attachment; filename="%s"'

                       % os.path.basename(file))

        msg.attach(part)



    smtp = smtplib.SMTP(server)

    smtp.sendmail(fro, to, msg.as_string() )

    smtp.close()







fileToSave="/dos/baseDeDonnees.db"




def EnvoieParMail(crypte=False):

	if(crypte):

		archive="db.gpg"

		c=Crypteuse()

		c.crypteFichier(fileToSave,archive)

	else:

		archive="db.zip"

		zippe( fileToSave,archive,"heures.db")

	sendMail(

    	    [preferences.DESTINATAIRE],

        	"sauvegarde","salutations",

        	[archive]

	    )

	os.remove(archive)





if __name__ == '__main__':

	EnvoieParMail()

