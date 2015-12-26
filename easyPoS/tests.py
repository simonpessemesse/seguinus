from django.test import TestCase
from django.test import TestCase


from easyPoS.models import Facture
#from easyPoS.Gui.FenetrePrincipale import Fenetre

class easyPoSMethodTests(TestCase):

    def test_fenetre(self):
        """
        on teste le calcul de lits
        """
        fact=Facture()

        self.assertEqual(3, 3)




# Create your tests here.
