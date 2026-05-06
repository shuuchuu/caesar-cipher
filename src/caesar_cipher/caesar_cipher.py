from string import ascii_lowercase, ascii_uppercase

import deal


def make_table(characters: str, key: int) -> dict[int, int]:
    key %= 26
    return str.maketrans(characters, characters[key:] + characters[:key])


@deal.ensure(lambda text, key, result: len(text) == len(result))
def rotate(text: str, key: int) -> str:
    table = {**make_table(ascii_lowercase, key), **make_table(ascii_uppercase, key)}
    return text.translate(table)
