from unittest import mock

from chiffre_cesar import cles
from chiffre_cesar.cles import chiffre_avec_cle_aleatoire


def test_chiffre_avec_cle_aleatoire():
    # Avec mock.patch("random.randint"), cles.randint resterait la vraie fonction :
    # la clef serait aléatoire, et le simulacre ne serait jamais appelé.
    with mock.patch("chiffre_cesar.cles.randint", return_value=3) as randint:
        assert chiffre_avec_cle_aleatoire("abc") == ("def", 3)
    randint.assert_called_once_with(1, 25)


def test_chiffre_avec_cle_aleatoire_monkeypatch(monkeypatch):
    monkeypatch.setattr(cles, "randint", lambda a, b: 3)
    assert chiffre_avec_cle_aleatoire("abc") == ("def", 3)
