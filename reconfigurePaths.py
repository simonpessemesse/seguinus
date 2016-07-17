import os
import fileinput
import preferences
import logging


def reconfigureEffectivement():
    positionnementRelatif = False
    if preferences.POSITIONNEMENT_RELATIF:
        databasePath = os.path.abspath(".." + os.sep + ".." + os.sep + "DONNEES" + os.sep + "baseDeDonnees.db")
    else:
        if os.name == "posix":
            databasePath = os.path.abspath("/dos/baseDeDonnees.db")
        else:
            databasePath = os.path.abspath("D:" + os.sep + "baseDeDonnees.db")
    if preferences.DUMMY_DB:
        databasePath = os.path.abspath("baseDeDonnees.db")

    logging.debug("db is in " + databasePath)

    for line in fileinput.FileInput("settings.py", inplace=1):
        #	if "DATABASE_NAME" in line:
        #		r="DATABASE_NAME = '"+databasePath+"'"
        #		r=r.replace("\\","/")
        #		print(r)
        if "TEMPLATE_DIRS" in line:
            r = "TEMPLATE_DIRS = ( '" + os.path.abspath(".." + os.sep + "templates") + "',"
            r = r.replace("\\", "/")
            logging.debug("template dir: " + r)
            print(r)
        else:
            print(line, end=' ')

    for line in fileinput.FileInput("urls.py", inplace=1):
        if "document_root" in line:
            print((line), end=' ')
        #		if not "media" in line:
        #			newl="{'document_root':'"+os.path.abspath(".."+os.sep+"static")+"'}),"
        #			newl=newl.replace("\\","/")
        #			logging.debug("document root "+newl)
        #			print(newl)
        #		else:
        #			print(line),
        else:
            print((line), end=' ')

    for line in fileinput.FileInput("save.py", inplace=1):
        if "fileToSave=" in line:
            newl = "fileToSave=\"" + databasePath + "\""
            newl = newl.replace("\\", "/")
            print(newl)
        else:
            print((line), end=' ')

# reconfigureEffectivement()
