from string import ascii_lowercase, ascii_uppercase


def cree_table(caracteres: str, cle: int) -> dict[int, int]:
    cle %= 26
    return str.maketrans(caracteres, caracteres[cle:] + caracteres[:cle])


def decale(texte: str, cle: int) -> str:
    table = {**cree_table(ascii_lowercase, cle), **cree_table(ascii_uppercase, cle)}
    return texte.translate(table)
