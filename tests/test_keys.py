from unittest import mock

from caesar_cipher import keys
from caesar_cipher.keys import encrypt_with_random_key


def test_encrypt_with_random_key():
    # With mock.patch("random.randint"), keys.randint would stay the real function:
    # the key would be random, and the mock would never be called.
    with mock.patch("caesar_cipher.keys.randint", return_value=3) as randint:
        assert encrypt_with_random_key("abc") == ("def", 3)
    randint.assert_called_once_with(1, 25)


def test_encrypt_with_random_key_monkeypatch(monkeypatch):
    monkeypatch.setattr(keys, "randint", lambda a, b: 3)
    assert encrypt_with_random_key("abc") == ("def", 3)
