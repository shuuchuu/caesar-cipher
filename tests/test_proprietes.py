from string import ascii_letters

from hypothesis import given
from hypothesis import strategies as st

from chiffre_cesar.chiffre_cesar import decale


@given(st.text(), st.integers())
def test_decale_garde_la_longueur(texte, cle):
    assert len(decale(texte, cle)) == len(texte)


@given(st.text(), st.integers(), st.integers())
def test_decale_compose_cles(texte, cle1, cle2):
    assert decale(decale(texte, cle1), cle2) == decale(texte, cle1 + cle2)


@given(st.text(st.characters(exclude_characters=ascii_letters)), st.integers())
def test_decale_garde_les_non_lettres(texte, cle):
    assert decale(texte, cle) == texte
