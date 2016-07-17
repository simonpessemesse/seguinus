import os
import preferences
import fileinput

import configureEnvironnement
configureEnvironnement.setup()

os.chdir("..")

if os.name == "posix":
    os.system("python telephones_tel.py")
elif os.name == "nt":
    os.system("C:\python26\python.exe telephones_tel.py")
