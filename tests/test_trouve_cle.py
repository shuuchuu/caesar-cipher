import pytest

from chiffre_cesar.chiffre_cesar import decale, trouve_cle


def test_trouve_la_cle():
    assert trouve_cle(decale("attaque à l'aube", 3), "aube") == 3


def test_trouve_une_autre_cle():
    assert trouve_cle(decale("attaque à l'aube", 11), "aube") == 11


def test_sans_cle_possible():
    with pytest.raises(ValueError, match="xyz"):
        trouve_cle("bonjour", "xyz")


@pytest.fixture
def secret():
    message = "rendez-vous à la gare à midi"
    cle = 7
    return message, cle, decale(message, cle)


def test_trouve_la_cle_du_secret(secret):
    _message, cle, texte_chiffre = secret
    assert trouve_cle(texte_chiffre, "gare") == cle


def test_dechiffre_le_secret(secret):
    message, _cle, texte_chiffre = secret
    cle = trouve_cle(texte_chiffre, "midi")
    assert decale(texte_chiffre, -cle) == message


def test_mot_absent_du_secret(secret):
    _message, _cle, texte_chiffre = secret
    with pytest.raises(ValueError):
        trouve_cle(texte_chiffre, "train")
