import unittest

from chiffre_cesar.chiffre_cesar import decale, trouve_cle


class TrouveCleTest(unittest.TestCase):
    def setUp(self):
        self.message = "rendez-vous à la gare à midi"
        self.cle = 7
        self.texte_chiffre = decale(self.message, self.cle)

    def test_trouve_la_cle(self):
        self.assertEqual(trouve_cle(self.texte_chiffre, "gare"), self.cle)

    def test_dechiffre_le_message(self):
        cle = trouve_cle(self.texte_chiffre, "midi")
        self.assertEqual(decale(self.texte_chiffre, -cle), self.message)

    def test_mot_absent(self):
        with self.assertRaises(ValueError):
            trouve_cle(self.texte_chiffre, "train")
