from typing import Any

from hypothesis import given
from hypothesis import strategies as st

from caesar_cipher.caesar_cipher import rotate


def test_rotate_a_by_0_same_output_as_input() -> None:
    assert rotate("a", 0) == "a"


def test_rotate_a_by_1() -> None:
    assert rotate("a", 1) == "b"


def test_rotate_m_by_13() -> None:
    assert rotate("m", 13) == "z"


def test_rotate_n_by_13_with_wrap_around_alphabet() -> None:
    assert rotate("n", 13) == "a"


def test_rotate_capital_letters() -> None:
    assert rotate("OMG", 5) == "TRL"


def test_rotate_spaces() -> None:
    assert rotate("O M G", 5) == "T R L"


def test_rotate_numbers() -> None:
    assert rotate("Testing 1 2 3 testing", 4) == "Xiwxmrk 1 2 3 xiwxmrk"


def test_rotate_punctuation() -> None:
    assert rotate("Let's eat, Grandma!", 21) == "Gzo'n zvo, Bmviyhv!"


def test_rotate_all_letters() -> None:
    assert (
        rotate("The quick brown fox jumps over the lazy dog.", 13)
        == "Gur dhvpx oebja sbk whzcf bire gur ynml qbt."
    )


@given(st.characters())
def test_double_rotate(characters: str) -> None:
    assert characters == rotate(rotate(characters, 13), 13)


@given(st.characters())
def test_length(characters: str) -> None:
    assert len(characters) == len(rotate(characters, 13))


@st.composite
def keys(draw: Any) -> list[int]:
    keys = draw(st.lists(st.integers()))
    keys.append(26 - (sum(keys) % 26))
    return keys


@given(keys(), st.characters())
def test_many_rotate(keys: list[int], characters: str) -> None:
    current = characters
    for key in keys:
        current = rotate(current, key)
    assert characters == current
