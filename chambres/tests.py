from django.test import TestCase


from chambres.models import Chambre

class ChambreMethodTests(TestCase):

    def test_CalculNombreLits(self):
        """
        on teste le calcul de lits
        """
        chambre= Chambre("test",1,1,True,10)
        self.assertEqual(chambre.capacite(), 3)



