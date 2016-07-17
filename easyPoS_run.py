import preferences
import logging

logging.basicConfig(level=preferences.LOGGING_LEVEL)

import fcntl
import sys

pid_file = '.program.pid'
fp = open(pid_file, 'w')
try:
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    print("ca court deja")
    # another instance is running
    sys.exit(0)

import configureEnvironnement
configureEnvironnement.setup()
import reconfigurePaths
import os

if preferences.LANCER_SERVEUR:
    child_pid = os.fork()
    if child_pid == 0:
        os.chdir("..")
        os.system("python manage.py runserver")
        sys.exit()

os.chdir(".." + os.sep + "easyPoS" + os.sep + "Gui")
logging.debug("current dir: " + os.getcwd())
logging.debug("lauching auberge.pyw")
if os.name == "posix":
    os.system("python3 auberge.pyw")
elif os.name == "nt":
    os.system("C:\python26\python.exe auberge.pyw")
# os.system("..\..\python26\python.exe auberge.pyw")
