from random import randint

from chiffre_cesar.chiffre_cesar import decale


def chiffre_avec_cle_aleatoire(texte: str) -> tuple[str, int]:
    cle = randint(1, 25)
    return decale(texte, cle), cle
