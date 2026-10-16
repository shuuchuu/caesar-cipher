from string import ascii_lowercase, ascii_uppercase

import deal


def make_table(characters: str, key: int) -> dict[int, int]:
    key %= 26
    return str.maketrans(characters, characters[key:] + characters[:key])


def rotate(text: str, key: int) -> str:
    table = {**make_table(ascii_lowercase, key), **make_table(ascii_uppercase, key)}
    return text.translate(table)


@deal.pre(lambda ciphertext, known_word: known_word != "")
def crack(ciphertext: str, known_word: str) -> int:
    for key in range(26):
        if known_word in rotate(ciphertext, -key):
            return key
    msg = f"aucune clé ne fait apparaître {known_word!r}"
    raise ValueError(msg)
