from random import randint

from caesar_cipher.caesar_cipher import rotate


def encrypt_with_random_key(text: str) -> tuple[str, int]:
    key = randint(1, 25)
    return rotate(text, key), key
