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

Sans regarder le fichier `src/chiffre_cesar/chiffre_cesar.py`, et d'après la description
du chiffre de César sur Wikipédia (en particulier les exemples donnés), écrivez quelques
tests simples de la fonction `decale(texte, cle)` fournie&nbsp;: des fonctions qui
vérifient avec `assert` le chiffrement d'une chaîne. Appelez-les ensuite.

Pensez aux cas limites&nbsp;: la fin de l'alphabet, les majuscules, les caractères qui
ne sont pas des lettres, une clef négative.

Écrivez-les dans un nouveau fichier `exercices.py` à la racine du dépôt, qui commence
par&nbsp;:

```python
from chiffre_cesar.chiffre_cesar import decale
```

et exécutez-le avec `uv run python exercices.py`.

<details>
<summary>Conseils supplémentaires</summary>

Un test est une fonction sans argument, dont le nom commence par `test_`, qui compare
avec `assert` le résultat de `decale` à la valeur attendue, calculée à la main. Avec une
clef de 3, `a` devient `d`, et `x` revient au début de l'alphabet. Une clef négative
décale vers la gauche. Un test qui passe n'affiche rien, un test qui échoue lève une
`AssertionError`.

```python
def test_decale_les_lettres():
    assert decale("abc", 3) == ...


def test_decale_reboucle():
    assert decale("xyz", 3) == ...


test_decale_les_lettres()
test_decale_reboucle()
```

</details>

<details>
<summary>Solution</summary>

```python
def test_decale_les_lettres():
    assert decale("abc", 3) == "def"


def test_decale_reboucle():
    assert decale("xyz", 3) == "abc"


def test_decale_garde_les_autres_caracteres():
    assert decale("Ave, César !", 3) == "Dyh, Févdu !"


def test_decale_avec_cle_negative():
    assert (
        decale("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG", -3)
        == "QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD"
    )


test_decale_les_lettres()
test_decale_reboucle()
test_decale_garde_les_autres_caracteres()
test_decale_avec_cle_negative()
```

</details>

## Utilisation de `pytest`

Écrivez un fichier `tests/test_chiffre_cesar.py` (le dossier `tests/` existe déjà) qui
regroupe vos exemples de `decale` en un seul test, paramétré avec
`@pytest.mark.parametrize`. Donnez un nom à chaque cas, et couvrez au moins&nbsp;:

- la fin de l'alphabet (`z` devient `a`)&nbsp;;
- les majuscules&nbsp;;
- la ponctuation et les lettres accentuées, qui ne changent pas&nbsp;;
- une clef négative&nbsp;;
- une clef supérieure ou égale à 26.

Lancez ensuite les tests avec `uv run pytest -v`, qui affiche chaque cas sous son nom.

**Documentation utile**

- https://docs.pytest.org/en/stable/reference/reference.html#pytest-param

<details>
<summary>Conseils supplémentaires</summary>

`@pytest.mark.parametrize` prend les noms des paramètres du test, puis la liste des cas.
`pytest.param("xyz", 3, "abc", id="z-reboucle-sur-a")` est un cas nommé `z-reboucle-sur-a`, que
`-v` affiche `test_decale[z-reboucle-sur-a]`&nbsp;: sans accents, que `pytest` échappe dans
les noms.

```python
import pytest

from chiffre_cesar.chiffre_cesar import decale


@pytest.mark.parametrize(
    ("texte", "cle", "attendu"),
    [
        pytest.param("xyz", 3, "abc", id="z-reboucle-sur-a"),
        pytest.param(..., id="majuscules"),
        ...,
    ],
)
def test_decale(texte, cle, attendu):
    assert ...
```

</details>

<details>
<summary>Solution</summary>

`tests/test_chiffre_cesar.py`&nbsp;:

```python
import pytest

from chiffre_cesar.chiffre_cesar import decale


@pytest.mark.parametrize(
    ("texte", "cle", "attendu"),
    [
        pytest.param("abc", 3, "def", id="decalage"),
        pytest.param("xyz", 3, "abc", id="z-reboucle-sur-a"),
        pytest.param("VENI VIDI VICI", 3, "YHQL YLGL YLFL", id="majuscules"),
        pytest.param("à l'aube, 6 h !", 1, "à m'bvcf, 6 i !", id="ponctuation-accents"),
        pytest.param("def", -3, "abc", id="cle-negative"),
        pytest.param("abc", 29, "def", id="cle-au-dela-de-25"),
    ],
)
def test_decale(texte, cle, attendu):
    assert decale(texte, cle) == attendu
```

```console
uv run pytest -v
```

</details>

## Démarche TDD (Test Driven Development)

On veut ajouter au module `src/chiffre_cesar/chiffre_cesar.py` une fonction
`trouve_cle(texte_chiffre, mot_connu)` qui retrouve la clef d'un message chiffré dont on connaît
un mot. Développez-la en suivant le cycle du TDD, avec ses tests dans un nouveau fichier
`tests/test_trouve_cle.py`&nbsp;:

1. Écrivez un test qui vérifie que `trouve_cle(decale("attaque à l'aube", 3), "aube")` vaut
   `3`, et lancez `pytest`&nbsp;: il doit échouer, puisque `trouve_cle` n'existe pas encore.
2. Écrivez dans le module le code minimal qui le fait passer, aussi naïf soit-il.
3. Ajoutez un test qui vérifie que `trouve_cle(decale("attaque à l'aube", 11), "aube")` vaut
   `11`. Voyez-le échouer, puis généralisez le code pour que les deux tests passent.
4. Ajoutez un test qui vérifie que `trouve_cle` lève une `ValueError` dont le message cite le
   mot, quand aucune clef ne le fait apparaître. Voyez-le échouer, puis faites-le passer.
5. Remaniez votre code si besoin, en vérifiant que les tests passent toujours.

<details>
<summary>Conseils supplémentaires</summary>

`uv run pytest -v tests/test_trouve_cle.py` ne lance que les tests de ce fichier. À l'étape
1, l'import de `trouve_cle` échoue&nbsp;: c'est l'échec attendu. À l'étape 2, `return 3`
suffit&nbsp;: c'est le code minimal, et le test de l'étape 3 le fait échouer. Pour
retrouver n'importe quelle clef, essayez les 26 clefs possibles&nbsp;:
`decale(texte_chiffre, -cle)` déchiffre avec la clef `cle`.
`pytest.raises(ValueError, match="xyz")` vérifie que le bloc lève une `ValueError` dont
le message contient `xyz`.

```python
import pytest

from chiffre_cesar.chiffre_cesar import decale, trouve_cle


def test_trouve_la_cle():
    assert trouve_cle(decale("attaque à l'aube", 3), "aube") == 3


def test_trouve_une_autre_cle():
    assert trouve_cle(decale("attaque à l'aube", 11), "aube") == ...


def test_sans_cle_possible():
    with pytest.raises(...):
        trouve_cle("bonjour", "xyz")
```

```python
def trouve_cle(texte_chiffre: str, mot_connu: str) -> int:
    for cle in range(26):
        if ...:
            return cle
    message = f"aucune clef ne fait apparaître {mot_connu!r}"
    raise ValueError(message)
```

</details>

<details>
<summary>Solution</summary>

`tests/test_trouve_cle.py`&nbsp;:

```python
import pytest

from chiffre_cesar.chiffre_cesar import decale, trouve_cle


def test_trouve_la_cle():
    assert trouve_cle(decale("attaque à l'aube", 3), "aube") == 3


def test_trouve_une_autre_cle():
    assert trouve_cle(decale("attaque à l'aube", 11), "aube") == 11


def test_sans_cle_possible():
    with pytest.raises(ValueError, match="xyz"):
        trouve_cle("bonjour", "xyz")
```

`src/chiffre_cesar/chiffre_cesar.py`&nbsp;:

```python
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
```

```console
uv run pytest -v tests/test_trouve_cle.py
```

</details>

## Utilisation de `unittest`

Écrivez cette fois des tests de `trouve_cle` avec `unittest`, dans un fichier
`tests/test_trouve_cle_unittest.py`&nbsp;: une classe qui hérite de `unittest.TestCase`, dont
la méthode `setUp` prépare un message, une clef et le message chiffré avec cette clef, et
trois tests qui les utilisent&nbsp;:

- `trouve_cle` retrouve la clef à partir d'un mot du message&nbsp;;
- la clef trouvée déchiffre le message&nbsp;;
- `trouve_cle` lève une `ValueError` pour un mot absent du message.

Lancez-les avec `uv run python -m unittest discover -v`, puis avec `uv run pytest -v`.
Combien de fois `setUp` est-elle appelée&nbsp;?

**Documentation utile**

- https://docs.python.org/fr/3/library/unittest.html#unittest.TestCase.setUp
- https://docs.python.org/fr/3/library/unittest.html#unittest.TestCase.assertRaises

<details>
<summary>Conseils supplémentaires</summary>

Les attributs que `setUp` pose sur `self` (`self.message`, `self.cle`,
`self.texte_chiffre`) sont visibles dans chaque test. `self.assertEqual(a, b)` compare deux
valeurs, et `with self.assertRaises(ValueError):` vérifie que le bloc lève l'exception.
`unittest discover` trouve les fichiers `test*.py` du paquet `tests` (c'est pour lui que
le dossier contient un `__init__.py`), et `pytest` lance aussi les tests écrits avec
`unittest`.

```python
import unittest

from chiffre_cesar.chiffre_cesar import decale, trouve_cle


class TrouveCleTest(unittest.TestCase):
    def setUp(self):
        self.message = "rendez-vous à la gare à midi"
        self.cle = 7
        self.texte_chiffre = ...

    def test_trouve_la_cle(self):
        self.assertEqual(..., self.cle)

    ...
```

</details>

<details>
<summary>Solution</summary>

`tests/test_trouve_cle_unittest.py`&nbsp;:

```python
import unittest

from chiffre_cesar.chiffre_cesar import decale, trouve_cle


class TrouveCleTest(unittest.TestCase):
    def setUp(self):
        self.message = "rendez-vous à la gare à midi"
        self.cle = 7
        self.texte_chiffre = decale(self.message, self.cle)

    def test_trouve_la_cle(self):
        self.assertEqual(trouve_cle(self.texte_chiffre, "gare"), self.cle)

    def test_dechiffre_le_message(self):
        cle = trouve_cle(self.texte_chiffre, "midi")
        self.assertEqual(decale(self.texte_chiffre, -cle), self.message)

    def test_mot_absent(self):
        with self.assertRaises(ValueError):
            trouve_cle(self.texte_chiffre, "train")
```

`setUp` est appelée trois fois&nbsp;: avant chacun des trois tests.

```console
uv run python -m unittest discover -v
uv run pytest -v
```

</details>

## Fixtures de `pytest`

Réécrivez maintenant vos tests `unittest` de `trouve_cle` à la manière de `pytest`, dans
`tests/test_trouve_cle.py`, sous les tests de la démarche TDD&nbsp;: la préparation de
`setUp` devient une fixture `secret` qui renvoie le message, la clef et le message
chiffré, et chaque test devient une fonction qui la demande.

Lancez `uv run pytest -v tests/test_trouve_cle.py`. Comparez avec `setUp`&nbsp;: combien de
fois la fixture est-elle calculée&nbsp;? Et pour les tests qui ne la demandent pas&nbsp;?

**Documentation utile**

- https://docs.pytest.org/en/stable/how-to/fixtures.html

<details>
<summary>Conseils supplémentaires</summary>

Une fixture est une fonction décorée par `@pytest.fixture`&nbsp;; un test la reçoit en
nommant l'un de ses paramètres comme elle. Elle peut renvoyer un n-uplet, que le test
décompose&nbsp;: `message, cle, texte_chiffre = secret` (un `_` en tête de nom marque une
valeur inutilisée).

```python
import pytest

from chiffre_cesar.chiffre_cesar import decale, trouve_cle

# Les tests de la démarche TDD
...


@pytest.fixture
def secret():
    message = "rendez-vous à la gare à midi"
    cle = 7
    return message, cle, ...


def test_trouve_la_cle_du_secret(secret):
    _message, cle, texte_chiffre = secret
    assert ...


...
```

</details>

<details>
<summary>Solution</summary>

`tests/test_trouve_cle.py`&nbsp;:

```python
import pytest

from chiffre_cesar.chiffre_cesar import decale, trouve_cle


def test_trouve_la_cle():
    assert trouve_cle(decale("attaque à l'aube", 3), "aube") == 3


def test_trouve_une_autre_cle():
    assert trouve_cle(decale("attaque à l'aube", 11), "aube") == 11


def test_sans_cle_possible():
    with pytest.raises(ValueError, match="xyz"):
        trouve_cle("bonjour", "xyz")


@pytest.fixture
def secret():
    message = "rendez-vous à la gare à midi"
    cle = 7
    return message, cle, decale(message, cle)


def test_trouve_la_cle_du_secret(secret):
    _message, cle, texte_chiffre = secret
    assert trouve_cle(texte_chiffre, "gare") == cle


def test_dechiffre_le_secret(secret):
    message, _cle, texte_chiffre = secret
    cle = trouve_cle(texte_chiffre, "midi")
    assert decale(texte_chiffre, -cle) == message


def test_mot_absent_du_secret(secret):
    _message, _cle, texte_chiffre = secret
    with pytest.raises(ValueError):
        trouve_cle(texte_chiffre, "train")
```

La fixture est calculée avant chacun des trois tests qui la demandent (portée
«&nbsp;function&nbsp;», par défaut), comme `setUp`. Les tests de la démarche TDD, qui ne
la demandent pas, ne la calculent pas&nbsp;: `setUp`, lui, tourne avant chaque test de
sa classe.

```console
uv run pytest -v tests/test_trouve_cle.py
```

</details>

## Simulacres avec `unittest.mock`

La fonction `chiffre_avec_cle_aleatoire` chiffre un texte avec une clef tirée au
hasard&nbsp;: son résultat change à chaque appel, ce qui la rend difficile à tester. Elle
est fournie dans un autre module du paquet, `src/chiffre_cesar/cles.py`&nbsp;:

```python
from random import randint

from chiffre_cesar.chiffre_cesar import decale


def chiffre_avec_cle_aleatoire(texte: str) -> tuple[str, int]:
    cle = randint(1, 25)
    return decale(texte, cle), cle
```

Écrivez dans `tests/test_cles.py` un test qui remplace `randint` par un simulacre qui
renvoie toujours `3`, avec `unittest.mock.patch`, puis qui vérifie le texte chiffré et
la clef renvoyés, et que le simulacre a été appelé une seule fois, avec les arguments
`(1, 25)`. Essayez d'abord la cible `"random.randint"`&nbsp;: pourquoi le test
échoue-t-il&nbsp;?

Si vous avez le temps, écrivez une seconde version du test avec la fixture
`monkeypatch` de `pytest`.

**Documentation utile**

- https://docs.python.org/fr/3/library/unittest.mock.html#unittest.mock.patch
- https://docs.python.org/fr/3/library/unittest.mock.html#where-to-patch

<details>
<summary>Conseils supplémentaires</summary>

`mock.patch("…", return_value=3)` remplace un nom, le temps du bloc `with`, par un
simulacre qui renvoie toujours `3`&nbsp;; `as randint` nomme ce simulacre, qui
enregistre ses appels. `cles.py` fait `from random import randint`&nbsp;: le module a sa
propre référence à la fonction, que remplacer `random.randint` ne touche pas. La cible
est le nom là où le code testé le cherche&nbsp;: `"chiffre_cesar.cles.randint"`. Avec la
fixture `monkeypatch`, `monkeypatch.setattr(cles, "randint", lambda a, b: 3)` remplace
le même nom, sans enregistrer les appels.

```python
from unittest import mock

from chiffre_cesar.cles import chiffre_avec_cle_aleatoire


def test_chiffre_avec_cle_aleatoire():
    with mock.patch(..., return_value=3) as randint:
        assert chiffre_avec_cle_aleatoire("abc") == ...
    randint.assert_called_once_with(...)
```

```console
uv run pytest -v tests/test_cles.py
```

</details>

<details>
<summary>Solution</summary>

`tests/test_cles.py`&nbsp;:

```python
from unittest import mock

from chiffre_cesar import cles
from chiffre_cesar.cles import chiffre_avec_cle_aleatoire


def test_chiffre_avec_cle_aleatoire():
    # Avec mock.patch("random.randint"), cles.randint resterait la vraie fonction :
    # la clef serait aléatoire, et le simulacre ne serait jamais appelé.
    with mock.patch("chiffre_cesar.cles.randint", return_value=3) as randint:
        assert chiffre_avec_cle_aleatoire("abc") == ("def", 3)
    randint.assert_called_once_with(1, 25)


def test_chiffre_avec_cle_aleatoire_monkeypatch(monkeypatch):
    monkeypatch.setattr(cles, "randint", lambda a, b: 3)
    assert chiffre_avec_cle_aleatoire("abc") == ("def", 3)
```

```console
uv run pytest -v tests/test_cles.py
```

</details>

## Couverture de code

L'extension `pytest-cov`, installée avec les dépendances du dépôt, mesure les lignes du
paquet que les tests exécutent.

1. Mesurez la couverture du paquet `chiffre_cesar` par les seuls tests de
   `tests/test_chiffre_cesar.py`, avec la liste des lignes manquées&nbsp;: quelles
   fonctions ces tests n'exécutent-ils pas&nbsp;?
2. Mesurez-la pour toute la suite de tests.
3. Écrivez dans `tests/test_sans_assert.py` un test qui appelle `trouve_cle` sans rien
   vérifier&nbsp;: une fois avec un mot du message, une fois avec un mot absent. Mesurez
   la couverture par `tests/test_chiffre_cesar.py` et ce seul fichier, et comparez la
   ligne de `chiffre_cesar.py` à celle de la question 2. Vos tests vérifient-ils tout ce
   que font `decale` et `trouve_cle`&nbsp;?

Supprimez ensuite `tests/test_sans_assert.py` (`rm tests/test_sans_assert.py`)&nbsp;: un test
qui ne vérifie rien n'a pas sa place dans la suite.

<details>
<summary>Conseils supplémentaires</summary>

`--cov=chiffre_cesar` mesure la couverture du paquet, `--cov-report=term-missing`
l'affiche avec, pour chaque fichier, ses instructions (`Stmts`), celles qu'aucun test
n'a exécutées (`Miss`), le pourcentage couvert (`Cover`) et les numéros des lignes
manquées (`Missing`). `pytest` ne lance que les fichiers de tests nommés sur la ligne de
commande, et tous si on n'en nomme aucun. Un appel à `trouve_cle` avec un mot absent lève une
`ValueError`&nbsp;: sans `pytest.raises`, qui vérifierait l'exception, entourez-le d'un
`try`/`except ValueError: pass`.

```console
uv run pytest tests/test_chiffre_cesar.py --cov=chiffre_cesar --cov-report=term-missing
```

```python
from chiffre_cesar.chiffre_cesar import decale, trouve_cle


def test_trouve_cle_sans_verifier():
    trouve_cle(...)
    try:
        trouve_cle(...)
    except ValueError:
        pass
```

</details>

<details>
<summary>Solution</summary>

`trouve_cle` (lignes 15 à 19 de `chiffre_cesar.py`) et `cles.py` ne sont exécutés par aucun
test de `tests/test_chiffre_cesar.py`&nbsp;:

```console
uv run pytest tests/test_chiffre_cesar.py --cov=chiffre_cesar --cov-report=term-missing
```

Toute la suite exécute 100&nbsp;% des lignes&nbsp;:

```console
uv run pytest --cov=chiffre_cesar --cov-report=term-missing
```

`tests/test_sans_assert.py`&nbsp;:

```python
from chiffre_cesar.chiffre_cesar import decale, trouve_cle


def test_trouve_cle_sans_verifier():
    trouve_cle(decale("attaque à l'aube", 3), "aube")
    try:
        trouve_cle("bonjour", "xyz")
    except ValueError:
        pass
```

`chiffre_cesar.py` est couvert à 100&nbsp;%, comme par toute la suite, alors que
`test_sans_assert.py` ne vérifie rien&nbsp;: la couverture dit quelles lignes les tests
exécutent, pas ce qu'ils vérifient. Les tests par mutations, plus bas, mesurent ce qui
est vérifié.

```console
uv run pytest tests/test_chiffre_cesar.py tests/test_sans_assert.py --cov=chiffre_cesar --cov-report=term-missing
rm tests/test_sans_assert.py
```

</details>

## Débogage post-mortem

`pdb` attend des commandes au clavier&nbsp;: cet exercice se fait dans un terminal à la
racine du dépôt.

1. Introduisez un bug dans `trouve_cle`&nbsp;: remplacez `range(26)` par `range(10)`.
2. Lancez `uv run pytest --pdb tests/test_trouve_cle.py`&nbsp;: au premier test en échec,
   `pytest` ouvre `pdb` là où l'exception a été levée.
3. Avec `ll` (le code de la fonction), `p cle` et `p mot_connu` (des valeurs), `w` et
   `u` (la pile d'appels, jusqu'au test), trouvez pourquoi aucune clef ne convient.
4. Quittez avec `q`, rétablissez `range(26)` et relancez les tests.

**Documentation utile**

- https://docs.pytest.org/en/stable/how-to/failures.html#using-python-library-pdb-with-pytest
- https://docs.python.org/fr/3/library/pdb.html#debugger-commands

## Pour aller plus loin

### Tests par génération

Avec `hypothesis`, écrivez dans un fichier `tests/test_proprietes.py` des tests de trois
propriétés de `decale`, vraies pour tout texte et toute clef&nbsp;:

- le texte chiffré a la même longueur que le texte&nbsp;;
- chiffrer avec `cle1` puis avec `cle2` revient à chiffrer avec `cle1 + cle2`&nbsp;;
- un texte sans lettres ASCII ne change pas.

**Documentation utile**

- https://hypothesis.readthedocs.io/en/latest/reference/strategies.html#hypothesis.strategies.text
- https://hypothesis.readthedocs.io/en/latest/reference/strategies.html#hypothesis.strategies.characters

<details>
<summary>Conseils supplémentaires</summary>

`@given(st.text(), st.integers())` appelle le test avec des centaines de textes et de
clefs générés, passés à ses paramètres. `st.text(alphabet)` génère des textes faits des
caractères d'`alphabet`, qui peut être une stratégie&nbsp;:
`st.characters(exclude_characters=ascii_letters)` génère tous les caractères sauf les
lettres ASCII.

```python
from string import ascii_letters

from hypothesis import given
from hypothesis import strategies as st

from chiffre_cesar.chiffre_cesar import decale


@given(st.text(), st.integers())
def test_decale_garde_la_longueur(texte, cle):
    assert ...


@given(st.text(), st.integers(), st.integers())
def test_decale_compose_cles(texte, cle1, cle2):
    assert ...


@given(st.text(...), st.integers())
def test_decale_garde_les_non_lettres(texte, cle):
    assert ...
```

</details>

<details>
<summary>Solution</summary>

`tests/test_proprietes.py`&nbsp;:

```python
from string import ascii_letters

from hypothesis import given
from hypothesis import strategies as st

from chiffre_cesar.chiffre_cesar import decale


@given(st.text(), st.integers())
def test_decale_garde_la_longueur(texte, cle):
    assert len(decale(texte, cle)) == len(texte)


@given(st.text(), st.integers(), st.integers())
def test_decale_compose_cles(texte, cle1, cle2):
    assert decale(decale(texte, cle1), cle2) == decale(texte, cle1 + cle2)


@given(st.text(st.characters(exclude_characters=ascii_letters)), st.integers())
def test_decale_garde_les_non_lettres(texte, cle):
    assert decale(texte, cle) == texte
```

```console
uv run pytest -v tests/test_proprietes.py
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
uv run mutmut show chiffre_cesar.chiffre_cesar.x_trouve_cle__mutmut_2
```

</details>

<details>
<summary>Solution</summary>

Avec les tests des solutions précédentes, une seule mutation survit&nbsp;: `range(26)`
devenu `range(27)`. La clef 26 revient à la clef 0, déjà essayée&nbsp;: cette mutation ne
change pas ce que renvoie `trouve_cle`, et aucun test ne peut la détecter (mutation
équivalente).

```console
uv run mutmut results
uv run mutmut show chiffre_cesar.chiffre_cesar.x_trouve_cle__mutmut_2
```

</details>
