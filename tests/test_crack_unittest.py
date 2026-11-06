import unittest

from caesar_cipher.caesar_cipher import crack, rotate


class CrackTest(unittest.TestCase):
    def setUp(self):
        self.message = "rendez-vous à la gare à midi"
        self.key = 7
        self.ciphertext = rotate(self.message, self.key)

    def test_finds_key(self):
        self.assertEqual(crack(self.ciphertext, "gare"), self.key)

    def test_decrypts_message(self):
        key = crack(self.ciphertext, "midi")
        self.assertEqual(rotate(self.ciphertext, -key), self.message)

    def test_unknown_word(self):
        with self.assertRaises(ValueError):
            crack(self.ciphertext, "train")
