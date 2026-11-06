import pytest

from caesar_cipher.caesar_cipher import rotate


@pytest.mark.parametrize(
    ("text", "key", "expected"),
    [
        pytest.param("abc", 3, "def", id="shift"),
        pytest.param("xyz", 3, "abc", id="wrap-z-to-a"),
        pytest.param("VENI VIDI VICI", 3, "YHQL YLGL YLFL", id="uppercase"),
        pytest.param("à l'aube, 6 h !", 1, "à m'bvcf, 6 i !", id="punctuation-accents"),
        pytest.param("def", -3, "abc", id="negative-key"),
        pytest.param("abc", 29, "def", id="key-over-25"),
    ],
)
def test_rotate(text, key, expected):
    assert rotate(text, key) == expected
