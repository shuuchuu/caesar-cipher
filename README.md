# Testing an Encryption Algorithm

*[Version française](https://github.com/shuuchuu/caesar-cipher)*

The project of the *Testing an encryption algorithm* lab. Its instructions are below, to
run the lab in a GitHub Codespace or a local clone; they are the same as the lab's
notebook, in
[English](https://colab.research.google.com/github/shuuchuu/labs/blob/main/testing-hands-on-en.ipynb)
or in
[French](https://colab.research.google.com/github/shuuchuu/labs/blob/main/testing-hands-on-fr.ipynb),
which runs it in Colab.

We are going to focus on implementing the [Caesar
cipher](https://en.wikipedia.org/wiki/Caesar_cipher).

This simple encryption method involves rotating characters in the alphabet (and does not
affect other characters like punctuation or spaces).

## Setting up the Working Environment

This English version of the lab is the repository's `main-en` branch. Open it in a
Codespace: on GitHub, on the `main-en` branch, **Code** > **Codespaces** > **Create
codespace on main-en**, or [this
link](https://codespaces.new/shuuchuu/caesar-cipher/tree/main-en). The Codespace
installs the dependencies when it is created, in the project's `.venv`.

In a local clone of that branch, install
[uv](https://docs.astral.sh/uv/getting-started/installation/), then run `uv sync` at the
root of the repository:

```console
git clone -b main-en https://github.com/shuuchuu/caesar-cipher.git
cd caesar-cipher
uv sync
```

The commands below run in a terminal at the root of the repository (**Terminal** > **New
Terminal** in the Codespace), through `uv run`, which runs them in the project's
environment. The files are written in the editor. The solutions are also on the
repository's [`solution-en`
branch](https://github.com/shuuchuu/caesar-cipher/tree/solution-en).

## Tests from the Specification

Without looking at the `src/caesar_cipher/caesar_cipher.py` file, and based on the
description of the Caesar cipher on Wikipedia (especially the examples given), write a
few simple tests of the provided `rotate(text, key)` function: functions that check the
encryption of a string with `assert`. Then call them.

Think of the edge cases: the end of the alphabet, capital letters, characters that are
not letters, a negative key.

Write them in a new `exercises.py` file at the root of the repository, which starts
with:

```python
from caesar_cipher.caesar_cipher import rotate
```

and run it with `uv run python exercises.py`.

<details>
<summary>Additional hints</summary>

A test is a function with no argument, whose name starts with `test_`, that compares
with `assert` the result of `rotate` to the expected value, computed by hand. With a key
of 3, `a` becomes `d`, and `x` wraps around to the start of the alphabet. A negative key
shifts to the left. A test that passes prints nothing, a test that fails raises an
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

## Using `pytest`

Write a `tests/test_caesar_cipher.py` file (the `tests/` folder already exists) that
groups your examples of `rotate` into a single test, parametrized with
`@pytest.mark.parametrize`. Give each case a name, and cover at least:

- the end of the alphabet (`z` becomes `a`);
- capital letters;
- punctuation and accented letters, which do not change;
- a negative key;
- a key greater than or equal to 26.

Then run the tests with `uv run pytest -v`, which shows each case under its name.

**Useful documentation**

- https://docs.pytest.org/en/stable/reference/reference.html#pytest-param

<details>
<summary>Additional hints</summary>

`@pytest.mark.parametrize` takes the names of the test's parameters, then the list of
cases. `pytest.param("xyz", 3, "abc", id="wrap-z-to-a")` is a case named `wrap-z-to-a`,
which `-v` shows as `test_rotate[wrap-z-to-a]`: no accents, which `pytest` escapes in
names.

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

`tests/test_caesar_cipher.py`:

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

## TDD Approach (Test Driven Development)

We want to add to the `src/caesar_cipher/caesar_cipher.py` module a `crack(ciphertext,
known_word)` function that recovers the key of an encrypted message when one of its
words is known. Develop it following the TDD cycle, with its tests in a new
`tests/test_crack.py` file:

1. Write a test that checks that `crack(rotate("attaque à l'aube", 3), "aube")` is `3`,
   and run `pytest`: it must fail, since `crack` does not exist yet.
2. Write in the module the minimal code that makes it pass.
3. Add a test that checks that `crack` raises a `ValueError` whose message quotes the
   word, when no key reveals it. See it fail, then make it pass.
4. Refactor your code if needed, checking that the tests still pass.

<details>
<summary>Additional hints</summary>

`uv run pytest -v tests/test_crack.py` runs only that file's tests. At step 1, importing
`crack` fails: that is the expected failure. To recover the key, try the 26 possible
keys: `rotate(ciphertext, -key)` decrypts with the key `key`. `pytest.raises(ValueError,
match="xyz")` checks that the block raises a `ValueError` whose message contains `xyz`.

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

`tests/test_crack.py`:

```python
import pytest

from caesar_cipher.caesar_cipher import crack, rotate


def test_crack_finds_key():
    assert crack(rotate("attaque à l'aube", 3), "aube") == 3


def test_crack_without_key():
    with pytest.raises(ValueError, match="xyz"):
        crack("bonjour", "xyz")
```

`src/caesar_cipher/caesar_cipher.py`:

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

## Using `unittest`

This time, write tests of `crack` with `unittest`, in a `tests/test_crack_unittest.py`
file: a class that inherits from `unittest.TestCase`, whose `setUp` method prepares a
message, a key and the message encrypted with that key, and three tests that use them:

- `crack` recovers the key from a word of the message;
- the key found decrypts the message;
- `crack` raises a `ValueError` for a word that is not in the message.

Run them with `uv run python -m unittest discover -v`, then with `uv run pytest -v`. How
many times is `setUp` called?

**Useful documentation**

- https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp
- https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises

<details>
<summary>Additional hints</summary>

The attributes that `setUp` sets on `self` (`self.message`, `self.key`,
`self.ciphertext`) are visible in every test. `self.assertEqual(a, b)` compares two
values, and `with self.assertRaises(ValueError):` checks that the block raises the
exception. `unittest discover` finds the `test*.py` files of the `tests` package (that
is why the folder holds an `__init__.py`), and `pytest` also runs the tests written with
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

`tests/test_crack_unittest.py`:

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

`setUp` is called three times: before each of the three tests.

```console
uv run python -m unittest discover -v
uv run pytest -v
```

</details>

## Mocking with `unittest.mock`

The `encrypt_with_random_key` function below encrypts a text with a randomly drawn key:
its result changes on every call, which makes it hard to test. Copy it into
`exercises.py`:

```python
import random

from caesar_cipher.caesar_cipher import rotate


def encrypt_with_random_key(text: str) -> tuple[str, int]:
    key = random.randint(1, 25)
    return rotate(text, key), key
```

Write a test that replaces `random.randint` with a mock that always returns `3`, with
`unittest.mock.patch`, then checks the returned encrypted text and key, and that
`random.randint` was called once, with the arguments `(1, 25)`.

**Useful documentation**

- https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

<details>
<summary>Additional hints</summary>

`mock.patch("random.randint", return_value=3)` replaces `random.randint`, for the
duration of the `with` block, with a mock that always returns `3`. `as randint` names
that mock, which records its calls. `encrypt_with_random_key` calls `randint` through
the `random` module: that is where it is replaced. Call the test function: it prints
nothing if it passes.

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

## Code Coverage

The `pytest-cov` plugin, installed with the repository's dependencies, measures the
lines of the package that the tests run. Run your tests while measuring the coverage of
the `caesar_cipher` package, with the list of missed lines. Which lines do your tests
not run? Add the missing tests, up to 100%.

Do your tests then check everything `rotate` and `crack` do?

<details>
<summary>Additional hints</summary>

`--cov=caesar_cipher` measures the package's coverage, `--cov-report=term-missing` shows
it with, for each file, its statements (`Stmts`), those no test ran (`Miss`), the
percentage covered (`Cover`) and the numbers of the missed lines (`Missing`). In
`crack`, the line often missed is the `raise`: it takes a test where no key reveals the
word.

```console
uv run pytest --cov=caesar_cipher --cov-report=term-missing
```

</details>

<details>
<summary>Solution</summary>

With the tests of the previous solutions, the coverage is 100%. It tells which lines the
tests run, not what they check: a test without an `assert` covers as many lines.
Mutation testing, below, measures what is checked.

</details>

## Going Further

### Property-based Testing

With `hypothesis`, write in a `tests/test_properties.py` file tests of three properties
of `rotate`, true for any text and any key:

- the encrypted text has the same length as the text;
- encrypting with `key1` then with `key2` amounts to encrypting with `key1 + key2`;
- a text without ASCII letters does not change.

**Useful documentation**

- https://hypothesis.readthedocs.io/en/latest/reference/strategies.html#hypothesis.strategies.text
- https://hypothesis.readthedocs.io/en/latest/reference/strategies.html#hypothesis.strategies.characters

<details>
<summary>Additional hints</summary>

`@given(st.text(), st.integers())` calls the test with hundreds of generated texts and
keys, passed to its parameters. `st.text(alphabet)` generates texts made of the
characters of `alphabet`, which can be a strategy:
`st.characters(exclude_characters=ascii_letters)` generates every character but the
ASCII letters.

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

`tests/test_properties.py`:

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

### Mutation Testing

Use `mutmut` to find the behaviors your tests do not check: each mutation that passes
your test suite reveals one. `mutmut run` creates and tests the mutations, `mutmut
results` lists those that survived, and `mutmut show <name>` shows the change one of
them makes:

```console
uv run mutmut run
uv run mutmut results
```

Iterate to reduce the number of mutations that pass your test suite. Does a surviving
mutation always reveal a missing test?

**Useful documentation**

- https://mutmut.readthedocs.io/

<details>
<summary>Additional hints</summary>

A surviving mutation is a change of the code that your tests let pass: `mutmut show`
shows the changed line. Write a test that fails on the changed version and passes on the
original one, then run `mutmut run` again. A mutation that does not change what the
function does (an *equivalent* mutation) survives every test: there is then nothing to
add.

```console
uv run mutmut show caesar_cipher.caesar_cipher.x_crack__mutmut_2
```

</details>

<details>
<summary>Solution</summary>

With the tests of the previous solutions, a single mutation survives: `range(26)` turned
into `range(27)`. Key 26 amounts to key 0, already tried: this mutation does not change
what `crack` returns, and no test can detect it (equivalent mutation).

```console
uv run mutmut results
uv run mutmut show caesar_cipher.caesar_cipher.x_crack__mutmut_2
```

</details>

### Contracts

With the `deal` library, add a pre-condition to `crack`: the known word is not empty (an
empty word appears in any text, and `crack` would return the key 0). Check it with a
test, in a `tests/test_contracts.py` file.

**Useful documentation**

- https://deal.readthedocs.io/details/api.html#deal.pre
- https://deal.readthedocs.io/details/api.html#deal.PreContractError

<details>
<summary>Additional hints</summary>

`@deal.pre(condition)` checks `condition` before each call of the decorated function: it
takes the same arguments as the function and returns a boolean. When it is false, `deal`
raises a `deal.PreContractError`.

```python
import deal


@deal.pre(lambda ciphertext, known_word: ...)
def crack(ciphertext: str, known_word: str) -> int:
    for key in range(26):
        ...
```

```python
import deal
import pytest

from caesar_cipher.caesar_cipher import crack


def test_crack_rejects_empty_word():
    with pytest.raises(...):
        crack("bonjour", "")
```

</details>

<details>
<summary>Solution</summary>

`src/caesar_cipher/caesar_cipher.py`:

```python
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
    msg = f"no key reveals {known_word!r}"
    raise ValueError(msg)
```

`tests/test_contracts.py`:

```python
import deal
import pytest

from caesar_cipher.caesar_cipher import crack


def test_crack_rejects_empty_word():
    with pytest.raises(deal.PreContractError):
        crack("bonjour", "")
```

`mutmut` creates no mutation in a decorated function: with its contract, `crack` has
none anymore.

```console
uv run pytest -v
```

</details>
