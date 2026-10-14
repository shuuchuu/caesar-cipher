# Tests d'un algorithme de chiffrement

*[English version](README.md)*

Le projet des travaux pratiques *Tests d'un algorithme de chiffrement*. Leur énoncé est
ci-dessous, pour les faire dans un Codespace GitHub ou un clone local&nbsp;; c'est le même
que celui du notebook des travaux pratiques, en
[français](https://colab.research.google.com/github/shuuchuu/labs/blob/main/testing-hands-on-fr.ipynb)
ou en
[anglais](https://colab.research.google.com/github/shuuchuu/labs/blob/main/testing-hands-on-en.ipynb),
qui les fait dans Colab.

Nous allons nous intéresser à l'implémentation du
[chiffre de César](https://fr.wikipedia.org/wiki/Chiffrement_par_d%C3%A9calage).

Ce chiffrement simple effectue une rotation des caractères de l'alphabet (et ne touche
pas aux autres caractères, comme la ponctuation ou les espaces).

## Mise en place de l'environnement de travail

Ouvrez le dépôt dans un Codespace&nbsp;: sur GitHub, **Code** > **Codespaces** > **Create
codespace on main**, ou [ce lien](https://codespaces.new/shuuchuu/caesar-cipher). Le
Codespace installe les dépendances à sa création, dans le `.venv` du projet.

Dans un clone local, installez [uv](https://docs.astral.sh/uv/getting-started/installation/),
puis lancez `uv sync` à la racine du dépôt.

Les commandes ci-dessous se lancent dans un terminal à la racine du dépôt (**Terminal** >
**Nouveau terminal** dans le Codespace), avec `uv run`, qui les exécute dans
l'environnement du projet.

## Tests à partir de la spécification

Sans regarder le fichier `src/caesar_cipher/caesar_cipher.py`, et d'après la description
du chiffre de César sur Wikipédia (en particulier les exemples donnés), écrivez quelques
tests simples (sous forme de fonctions) qui vérifient le chiffrement d'une chaîne par la
fonction `rotate` fournie, puis exécutez-les.

Écrivez-les dans un nouveau fichier `exercises.py` à la racine du dépôt, qui commence
par&nbsp;:

```python
from caesar_cipher.caesar_cipher import rotate
```

et exécutez-le avec `uv run python exercises.py`.

## Démarche TDD (Test Driven Development)

On veut ajouter une fonction `crack(ciphertext, known_word)` qui retrouve la clé d'un
message chiffré dont on connaît un mot. Développez-la dans `exercises.py`, en suivant le
cycle du TDD&nbsp;:

1. Écrivez un test qui vérifie que `crack(rotate("attaque à l'aube", 3), "aube")` vaut
   `3`, et exécutez-le&nbsp;: il doit échouer, puisque `crack` n'existe pas encore.
2. Écrivez le code minimal qui le fait passer.
3. Ajoutez un test qui vérifie que `crack` lève une `ValueError` quand aucune clé ne fait
   apparaître le mot, voyez-le échouer, puis faites-le passer.
4. Remaniez votre code si besoin, en vérifiant que les tests passent toujours.

<details>
<summary>Solution</summary>

```python
def test_crack_finds_key():
    assert crack(rotate("attaque à l'aube", 3), "aube") == 3


def test_crack_without_key():
    try:
        crack("bonjour", "xyz")
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError expected")


def crack(ciphertext: str, known_word: str) -> int:
    for key in range(26):
        if known_word in rotate(ciphertext, -key):
            return key
    raise ValueError(f"No key reveals {known_word!r}")


test_crack_finds_key()
test_crack_without_key()
```

</details>

## Utilisation de `pytest`

Créez un fichier `tests/test_caesar_cipher.py` puis adaptez les fonctions qui testent
`rotate` pour les rendre compatibles avec `pytest`, en regroupant les exemples dans un
seul test avec `@pytest.mark.parametrize`.

Utilisez ensuite `pytest` pour exécuter les tests&nbsp;:

```console
uv run pytest
```

Enfin, complétez votre fichier de tests pour atteindre 5 cas de test.

## Simulacres avec `unittest.mock`

La fonction `encrypt_with_random_key` ci-dessous chiffre un texte avec une clé tirée au
hasard&nbsp;: son résultat change à chaque appel, ce qui la rend difficile à tester.
Copiez-la dans `exercises.py`&nbsp;:

```python
import random

from caesar_cipher.caesar_cipher import rotate


def encrypt_with_random_key(text: str) -> tuple[str, int]:
    key = random.randint(1, 25)
    return rotate(text, key), key
```

Écrivez un test qui remplace `random.randint` par un simulacre qui renvoie toujours `3`,
avec
[`unittest.mock.patch`](https://docs.python.org/fr/3/library/unittest.mock.html#unittest.mock.patch),
puis qui vérifie le texte chiffré et la clé renvoyés, et que `random.randint` a été
appelée une seule fois, avec les arguments `(1, 25)`.

<details>
<summary>Solution</summary>

```python
from unittest import mock


def test_encrypt_with_random_key():
    with mock.patch("random.randint", return_value=3) as randint:
        assert encrypt_with_random_key("abc") == ("def", 3)
    randint.assert_called_once_with(1, 25)


test_encrypt_with_random_key()
```

</details>

## Pour aller plus loin

### Tests par génération

Utilisez [`hypothesis`](https://hypothesis.readthedocs.io/en/latest/) pour tester la
fonction `rotate` avec des données aléatoires.

### Contrats

Finalement, intégrez un contrat de pré-condition au code de
`src/caesar_cipher/caesar_cipher.py`. Pour cela, utilisez la librairie
[`deal`](https://deal.readthedocs.io/).

### Tests par mutations

Utilisez [`mutmut`](https://mutmut.readthedocs.io/) pour trouver les comportements que
vos tests ne vérifient pas&nbsp;: chaque mutation qui passe votre suite de tests en révèle
un.

Itérez pour réduire le nombre de mutations qui passent votre suite de tests&nbsp;:

```console
uv run mutmut run
uv run mutmut results
```

## Solution

Les solutions des exercices qui créent des fichiers de tests sont sur la
[branche `solution`](https://github.com/shuuchuu/caesar-cipher/tree/solution) du dépôt.
