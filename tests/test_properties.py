from string import ascii_letters

from hypothesis import given
from hypothesis import strategies as st

from caesar_cipher.caesar_cipher import rotate


@given(st.text(), st.integers())
def test_rotate_keeps_length(text, key):
    assert len(rotate(text, key)) == len(text)


@given(st.text(), st.integers(), st.integers())
def test_rotate_composes_keys(text, key1, key2):
    assert rotate(rotate(text, key1), key2) == rotate(text, key1 + key2)


@given(st.text(st.characters(exclude_characters=ascii_letters)), st.integers())
def test_rotate_keeps_non_letters(text, key):
    assert rotate(text, key) == text
