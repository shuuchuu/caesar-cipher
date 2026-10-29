import pytest

from caesar_cipher.caesar_cipher import crack, rotate


def test_crack_finds_key():
    assert crack(rotate("attaque à l'aube", 3), "aube") == 3


def test_crack_finds_other_key():
    assert crack(rotate("attaque à l'aube", 11), "aube") == 11


def test_crack_without_key():
    with pytest.raises(ValueError, match="xyz"):
        crack("bonjour", "xyz")


@pytest.fixture
def secret():
    message = "rendez-vous à la gare à midi"
    key = 7
    return message, key, rotate(message, key)


def test_finds_key_of_secret(secret):
    _message, key, ciphertext = secret
    assert crack(ciphertext, "gare") == key


def test_decrypts_secret(secret):
    message, _key, ciphertext = secret
    key = crack(ciphertext, "midi")
    assert rotate(ciphertext, -key) == message


def test_unknown_word_in_secret(secret):
    _message, _key, ciphertext = secret
    with pytest.raises(ValueError):
        crack(ciphertext, "train")
