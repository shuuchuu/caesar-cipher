# Tests d'un algorithme de chiffrement

*[English version](https://github.com/shuuchuu/caesar-cipher/tree/main-en)*

Le projet des travaux pratiques *Tests d'un algorithme de chiffrement*. Leur énoncé est
ci-dessous, pour les faire dans un Codespace GitHub ou un clone local&nbsp;; c'est le
même que celui du notebook des travaux pratiques, en
[français](https://colab.research.google.com/github/shuuchuu/labs/blob/main/testing-hands-on-fr.ipynb)
ou en
[anglais](https://colab.research.google.com/github/shuuchuu/labs/blob/main/testing-hands-on-en.ipynb),
qui les fait dans Colab.

Nous allons nous intéresser à l'implémentation du [chiffre de
César](https://fr.wikipedia.org/wiki/Chiffrement_par_d%C3%A9calage).

Ce chiffrement simple effectue une rotation des caractères de l'alphabet (et ne touche
pas aux autres caractères, comme la ponctuation ou les espaces).

## Mise en place de l'environnement de travail

Ouvrez le dépôt dans un Codespace&nbsp;: sur GitHub, **Code** > **Codespaces** >
**Create codespace on main**, ou [ce
lien](https://codespaces.new/shuuchuu/caesar-cipher). Le Codespace installe les
dépendances à sa création, dans le `.venv` du projet.

Dans un clone local, installez
[uv](https://docs.astral.sh/uv/getting-started/installation/), puis lancez `uv sync` à
la racine du dépôt.

Les commandes ci-dessous se lancent dans un terminal à la racine du dépôt (**Terminal** >
**Nouveau terminal** dans le Codespace), avec `uv run`, qui les exécute dans
l'environnement du projet. Les fichiers s'écrivent dans l'éditeur. Les solutions sont
aussi sur la [branche
`solution`](https://github.com/shuuchuu/caesar-cipher/tree/solution) du dépôt.

## Tests à partir de la spécification

Sans regarder le fichier `src/caesar_cipher/caesar_cipher.py`, et d'après la description
du chiffre de César sur Wikipédia (en particulier les exemples donnés), écrivez quelques
tests simples de la fonction `rotate(text, key)` fournie&nbsp;: des fonctions qui
vérifient avec `assert` le chiffrement d'une chaîne. Appelez-les ensuite.

Pensez aux cas limites&nbsp;: la fin de l'alphabet, les majuscules, les caractères qui
ne sont pas des lettres, une clé négative.

Écrivez-les dans un nouveau fichier `exercises.py` à la racine du dépôt, qui commence
par&nbsp;:

```python
from caesar_cipher.caesar_cipher import rotate
```

et exécutez-le avec `uv run python exercises.py`.

<details>
<summary>Conseils supplémentaires</summary>

Un test est une fonction sans argument, dont le nom commence par `test_`, qui compare
avec `assert` le résultat de `rotate` à la valeur attendue, calculée à la main. Avec une
clé de 3, `a` devient `d`, et `x` revient au début de l'alphabet. Une clé négative
décale vers la gauche. Un test qui passe n'affiche rien, un test qui échoue lève une
`AssertionError`.

```python
def test_rotate_shifts_letters():
    assert rotate("abc", 3) == ...


def test_rotate_wraps_around():
    assert rotate("xyz", 3) == ...


test_rotate_shifts_letters()
test_rotate_wraps_around()
```

</details>

<details>
<summary>Solution</summary>

```python
def test_rotate_shifts_letters():
    assert rotate("abc", 3) == "def"


def test_rotate_wraps_around():
    assert rotate("xyz", 3) == "abc"


def test_rotate_keeps_other_characters():
    assert rotate("Ave, César !", 3) == "Dyh, Févdu !"


def test_rotate_with_negative_key():
    assert (
        rotate("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG", -3)
        == "QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD"
    )


test_rotate_shifts_letters()
test_rotate_wraps_around()
test_rotate_keeps_other_characters()
test_rotate_with_negative_key()
```

</details>

## Utilisation de `pytest`

Écrivez un fichier `tests/test_caesar_cipher.py` (le dossier `tests/` existe déjà) qui
regroupe vos exemples de `rotate` en un seul test, paramétré avec
`@pytest.mark.parametrize`. Donnez un nom à chaque cas, et couvrez au moins&nbsp;:

- la fin de l'alphabet (`z` devient `a`)&nbsp;;
- les majuscules&nbsp;;
- la ponctuation et les lettres accentuées, qui ne changent pas&nbsp;;
- une clé négative&nbsp;;
- une clé supérieure ou égale à 26.

Lancez ensuite les tests avec `uv run pytest -v`, qui affiche chaque cas sous son nom.

**Documentation utile**

- https://docs.pytest.org/en/stable/reference/reference.html#pytest-param

<details>
<summary>Conseils supplémentaires</summary>

`@pytest.mark.parametrize` prend les noms des paramètres du test, puis la liste des cas.
`pytest.param("xyz", 3, "abc", id="wrap-z-to-a")` est un cas nommé `wrap-z-to-a`, que
`-v` affiche `test_rotate[wrap-z-to-a]`&nbsp;: sans accents, que `pytest` échappe dans
les noms.

```python
import pytest

from caesar_cipher.caesar_cipher import rotate


@pytest.mark.parametrize(
    ("text", "key", "expected"),
    [
        pytest.param("xyz", 3, "abc", id="wrap-z-to-a"),
        pytest.param(..., id="uppercase"),
        ...,
    ],
)
def test_rotate(text, key, expected):
    assert ...
```

</details>

<details>
<summary>Solution</summary>

`tests/test_caesar_cipher.py`&nbsp;:

```python
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
```

```console
uv run pytest -v
```

</details>

## Démarche TDD (Test Driven Development)

On veut ajouter au module `src/caesar_cipher/caesar_cipher.py` une fonction
`crack(ciphertext, known_word)` qui retrouve la clé d'un message chiffré dont on connaît
un mot. Développez-la en suivant le cycle du TDD, avec ses tests dans un nouveau fichier
`tests/test_crack.py`&nbsp;:

1. Écrivez un test qui vérifie que `crack(rotate("attaque à l'aube", 3), "aube")` vaut
   `3`, et lancez `pytest`&nbsp;: il doit échouer, puisque `crack` n'existe pas encore.
2. Écrivez dans le module le code minimal qui le fait passer.
3. Ajoutez un test qui vérifie que `crack` lève une `ValueError` dont le message cite le
   mot, quand aucune clé ne le fait apparaître. Voyez-le échouer, puis faites-le passer.
4. Remaniez votre code si besoin, en vérifiant que les tests passent toujours.

<details>
<summary>Conseils supplémentaires</summary>

`uv run pytest -v tests/test_crack.py` ne lance que les tests de ce fichier. À l'étape
1, l'import de `crack` échoue&nbsp;: c'est l'échec attendu. Pour retrouver la clé,
essayez les 26 clés possibles&nbsp;: `rotate(ciphertext, -key)` déchiffre avec la clé
`key`. `pytest.raises(ValueError, match="xyz")` vérifie que le bloc lève une
`ValueError` dont le message contient `xyz`.

```python
import pytest

from caesar_cipher.caesar_cipher import crack, rotate


def test_crack_finds_key():
    assert crack(rotate("attaque à l'aube", 3), "aube") == 3


def test_crack_without_key():
    with pytest.raises(...):
        crack("bonjour", "xyz")
```

```python
def crack(ciphertext: str, known_word: str) -> int:
    for key in range(26):
        if ...:
            return key
    msg = f"no key reveals {known_word!r}"
    raise ValueError(msg)
```

</details>

<details>
<summary>Solution</summary>

`tests/test_crack.py`&nbsp;:

```python
import pytest

from caesar_cipher.caesar_cipher import crack, rotate


def test_crack_finds_key():
    assert crack(rotate("attaque à l'aube", 3), "aube") == 3


def test_crack_without_key():
    with pytest.raises(ValueError, match="xyz"):
        crack("bonjour", "xyz")
```

`src/caesar_cipher/caesar_cipher.py`&nbsp;:

```python
from string import ascii_lowercase, ascii_uppercase


def make_table(characters: str, key: int) -> dict[int, int]:
    key %= 26
    return str.maketrans(characters, characters[key:] + characters[:key])


def rotate(text: str, key: int) -> str:
    table = {**make_table(ascii_lowercase, key), **make_table(ascii_uppercase, key)}
    return text.translate(table)


def crack(ciphertext: str, known_word: str) -> int:
    for key in range(26):
        if known_word in rotate(ciphertext, -key):
            return key
    msg = f"no key reveals {known_word!r}"
    raise ValueError(msg)
```

```console
uv run pytest -v tests/test_crack.py
```

</details>

## Utilisation de `unittest`

Écrivez cette fois des tests de `crack` avec `unittest`, dans un fichier
`tests/test_crack_unittest.py`&nbsp;: une classe qui hérite de `unittest.TestCase`, dont
la méthode `setUp` prépare un message, une clé et le message chiffré avec cette clé, et
trois tests qui les utilisent&nbsp;:

- `crack` retrouve la clé à partir d'un mot du message&nbsp;;
- la clé trouvée déchiffre le message&nbsp;;
- `crack` lève une `ValueError` pour un mot absent du message.

Lancez-les avec `uv run python -m unittest discover -v`, puis avec `uv run pytest -v`.
Combien de fois `setUp` est-elle appelée&nbsp;?

**Documentation utile**

- https://docs.python.org/fr/3/library/unittest.html#unittest.TestCase.setUp
- https://docs.python.org/fr/3/library/unittest.html#unittest.TestCase.assertRaises

<details>
<summary>Conseils supplémentaires</summary>

Les attributs que `setUp` pose sur `self` (`self.message`, `self.key`,
`self.ciphertext`) sont visibles dans chaque test. `self.assertEqual(a, b)` compare deux
valeurs, et `with self.assertRaises(ValueError):` vérifie que le bloc lève l'exception.
`unittest discover` trouve les fichiers `test*.py` du paquet `tests` (c'est pour lui que
le dossier contient un `__init__.py`), et `pytest` lance aussi les tests écrits avec
`unittest`.

```python
import unittest

from caesar_cipher.caesar_cipher import crack, rotate


class CrackTest(unittest.TestCase):
    def setUp(self):
        self.message = "rendez-vous à la gare à midi"
        self.key = 7
        self.ciphertext = ...

    def test_finds_key(self):
        self.assertEqual(..., self.key)

    ...
```

</details>

<details>
<summary>Solution</summary>

`tests/test_crack_unittest.py`&nbsp;:

```python
import unittest

from caesar_cipher.caesar_cipher import crack, rotate


class CrackTest(unittest.TestCase):
    def setUp(self):
        self.message = "rendez-vous à la gare à midi"
        self.key = 7
        self.ciphertext = rotate(self.message, self.key)

    def test_finds_key(self):
        self.assertEqual(crack(self.ciphertext, "gare"), self.key)

    def test_decrypts_message(self):
        key = crack(self.ciphertext, "midi")
        self.assertEqual(rotate(self.ciphertext, -key), self.message)

    def test_unknown_word(self):
        with self.assertRaises(ValueError):
            crack(self.ciphertext, "train")
```

`setUp` est appelée trois fois&nbsp;: avant chacun des trois tests.

```console
uv run python -m unittest discover -v
uv run pytest -v
```

</details>

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
avec `unittest.mock.patch`, puis qui vérifie le texte chiffré et la clé renvoyés, et que
`random.randint` a été appelée une seule fois, avec les arguments `(1, 25)`.

**Documentation utile**

- https://docs.python.org/fr/3/library/unittest.mock.html#unittest.mock.patch

<details>
<summary>Conseils supplémentaires</summary>

`mock.patch("random.randint", return_value=3)` remplace `random.randint`, le temps du
bloc `with`, par un simulacre qui renvoie toujours `3`. `as randint` nomme ce simulacre,
qui enregistre ses appels. `encrypt_with_random_key` appelle `randint` à travers le
module `random`&nbsp;: c'est là qu'on le remplace. Appelez la fonction de test&nbsp;:
elle n'affiche rien si elle passe.

```python
from unittest import mock


def test_encrypt_with_random_key():
    with mock.patch(...) as randint:
        assert encrypt_with_random_key("abc") == ...
    randint.assert_called_once_with(...)


test_encrypt_with_random_key()
```

</details>

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

## Couverture de code

L'extension `pytest-cov`, installée avec les dépendances du dépôt, mesure les lignes du
paquet que les tests exécutent. Lancez vos tests en mesurant la couverture du paquet
`caesar_cipher`, avec la liste des lignes manquées. Quelles lignes vos tests
n'exécutent-ils pas&nbsp;? Ajoutez les tests qui manquent, jusqu'à 100&nbsp;%.

Vos tests vérifient-ils alors tout ce que font `rotate` et `crack`&nbsp;?

<details>
<summary>Conseils supplémentaires</summary>

`--cov=caesar_cipher` mesure la couverture du paquet, `--cov-report=term-missing`
l'affiche avec, pour chaque fichier, ses instructions (`Stmts`), celles qu'aucun test
n'a exécutées (`Miss`), le pourcentage couvert (`Cover`) et les numéros des lignes
manquées (`Missing`). Dans `crack`, la ligne souvent manquée est le `raise`&nbsp;: il
faut un test où aucune clé ne fait apparaître le mot.

```console
uv run pytest --cov=caesar_cipher --cov-report=term-missing
```

</details>

<details>
<summary>Solution</summary>

Avec les tests des solutions précédentes, la couverture est de 100&nbsp;%. Elle dit
quelles lignes les tests exécutent, pas ce qu'ils vérifient&nbsp;: un test sans `assert`
couvre autant de lignes. Les tests par mutations, plus bas, mesurent ce qui est vérifié.

</details>

## Pour aller plus loin

### Tests par génération

Avec `hypothesis`, écrivez dans un fichier `tests/test_properties.py` des tests de trois
propriétés de `rotate`, vraies pour tout texte et toute clé&nbsp;:

- le texte chiffré a la même longueur que le texte&nbsp;;
- chiffrer avec `key1` puis avec `key2` revient à chiffrer avec `key1 + key2`&nbsp;;
- un texte sans lettres ASCII ne change pas.

**Documentation utile**

- https://hypothesis.readthedocs.io/en/latest/reference/strategies.html#hypothesis.strategies.text
- https://hypothesis.readthedocs.io/en/latest/reference/strategies.html#hypothesis.strategies.characters

<details>
<summary>Conseils supplémentaires</summary>

`@given(st.text(), st.integers())` appelle le test avec des centaines de textes et de
clés générés, passés à ses paramètres. `st.text(alphabet)` génère des textes faits des
caractères d'`alphabet`, qui peut être une stratégie&nbsp;:
`st.characters(exclude_characters=ascii_letters)` génère tous les caractères sauf les
lettres ASCII.

```python
from string import ascii_letters

from hypothesis import given
from hypothesis import strategies as st

from caesar_cipher.caesar_cipher import rotate


@given(st.text(), st.integers())
def test_rotate_keeps_length(text, key):
    assert ...


@given(st.text(), st.integers(), st.integers())
def test_rotate_composes_keys(text, key1, key2):
    assert ...


@given(st.text(...), st.integers())
def test_rotate_keeps_non_letters(text, key):
    assert ...
```

</details>

<details>
<summary>Solution</summary>

`tests/test_properties.py`&nbsp;:

```python
from string import ascii_letters

from hypothesis import given
from hypothesis import strategies as st

from caesar_cipher.caesar_cipher import rotate


@given(st.text(), st.integers())
def test_rotate_keeps_length(text, key):
    assert len(rotate(text, key)) == len(text)


@given(st.text(), st.integers(), st.integers())
def test_rotate_composes_keys(text, key1, key2):
    assert rotate(rotate(text, key1), key2) == rotate(text, key1 + key2)


@given(st.text(st.characters(exclude_characters=ascii_letters)), st.integers())
def test_rotate_keeps_non_letters(text, key):
    assert rotate(text, key) == text
```

```console
uv run pytest -v tests/test_properties.py
```

</details>

### Tests par mutations

Utilisez `mutmut` pour trouver les comportements que vos tests ne vérifient pas&nbsp;:
chaque mutation qui passe votre suite de tests en révèle un. `mutmut run` crée et teste
les mutations, `mutmut results` liste celles qui ont survécu, et `mutmut show <nom>`
affiche le changement fait par l'une d'elles&nbsp;:

```console
uv run mutmut run
uv run mutmut results
```

Itérez pour réduire le nombre de mutations qui passent votre suite de tests. Une
mutation qui survit révèle-t-elle toujours un test manquant&nbsp;?

**Documentation utile**

- https://mutmut.readthedocs.io/

<details>
<summary>Conseils supplémentaires</summary>

Une mutation qui survit est une modification du code que vos tests laissent
passer&nbsp;: `mutmut show` montre la ligne changée. Écrivez un test qui échoue sur la
version modifiée et passe sur l'originale, puis relancez `mutmut run`. Une mutation qui
ne change pas ce que fait la fonction (une mutation *équivalente*) survit à tous les
tests&nbsp;: il n'y a alors rien à ajouter.

```console
uv run mutmut show caesar_cipher.caesar_cipher.x_crack__mutmut_2
```

</details>

<details>
<summary>Solution</summary>

Avec les tests des solutions précédentes, une seule mutation survit&nbsp;: `range(26)`
devenu `range(27)`. La clé 26 revient à la clé 0, déjà essayée&nbsp;: cette mutation ne
change pas ce que renvoie `crack`, et aucun test ne peut la détecter (mutation
équivalente).

```console
uv run mutmut results
uv run mutmut show caesar_cipher.caesar_cipher.x_crack__mutmut_2
```

</details>
