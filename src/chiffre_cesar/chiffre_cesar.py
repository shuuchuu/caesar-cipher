from string import ascii_lowercase, ascii_uppercase


def cree_table(caracteres: str, cle: int) -> dict[int, int]:
    cle %= 26
    return str.maketrans(caracteres, caracteres[cle:] + caracteres[:cle])


def decale(texte: str, cle: int) -> str:
    table = {**cree_table(ascii_lowercase, cle), **cree_table(ascii_uppercase, cle)}
    return texte.translate(table)


def trouve_cle(texte_chiffre: str, mot_connu: str) -> int:
    for cle in range(26):
        if mot_connu in decale(texte_chiffre, -cle):
            return cle
    message = f"aucune clef ne fait apparaître {mot_connu!r}"
    raise ValueError(message)
