import os.path
import os
import shutil
import sys
import unittest

from . import gnupg

KEYS_TO_IMPORT = """-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1.4.12 (GNU/Linux)

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
a2ooXfC2b0bSZZRH
=XfPQ
-----END PGP PUBLIC KEY BLOCK-----"""


class Crypteuse():
    def __init__(self):
        print("coucou")
        gpgPath = 'gpg'
        if (os.name == "nt"):
            gpgPath = '..\..\EnvironnementDeTravail\GnuPG\gpg.exe'
        print(gpgPath)
        print((os.path.realpath(".")))
        self.gpg = gnupg.GPG(gnupghome=".", gpgbinary=gpgPath)
        print(gpgPath)
        self.gpg.import_keys(KEYS_TO_IMPORT)
        print(gpgPath)

    def crypteFichier(self, fichier, outputFichier):
        cleDeChiffrement = self.gpg.list_keys()[0]
        #		print(dir(self.gpg))
        #		print(public_keys[0])
        result = self.gpg.encrypt_file(open(fichier, "rb"), cleDeChiffrement["fingerprint"], always_trust=True)
        output = open(outputFichier, "wb")
        output.write(result.data)
        output.close()

# print(dir(g))
#		print(g)
#		print(g.ok)
