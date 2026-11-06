import pytest

from chiffre_cesar.chiffre_cesar import decale


@pytest.mark.parametrize(
    ("texte", "cle", "attendu"),
    [
        pytest.param("abc", 3, "def", id="decalage"),
        pytest.param("xyz", 3, "abc", id="z-reboucle-sur-a"),
        pytest.param("VENI VIDI VICI", 3, "YHQL YLGL YLFL", id="majuscules"),
        pytest.param("à l'aube, 6 h !", 1, "à m'bvcf, 6 i !", id="ponctuation-accents"),
        pytest.param("def", -3, "abc", id="cle-negative"),
        pytest.param("abc", 29, "def", id="cle-au-dela-de-25"),
    ],
)
def test_decale(texte, cle, attendu):
    assert decale(texte, cle) == attendu
