# Testing an Encryption Algorithm

*[Version française](https://github.com/shuuchuu/caesar-cipher)*

The project of the *Testing an encryption algorithm* lab. Its instructions are below, to
run the lab in a GitHub Codespace or a local clone; they are the same as the lab's
notebook, in
[English](https://colab.research.google.com/github/shuuchuu/labs/blob/main/testing-hands-on-en.ipynb)
or in
[French](https://colab.research.google.com/github/shuuchuu/labs/blob/main/testing-hands-on-fr.ipynb),
which runs it in Colab.

We are going to focus on implementing the
[Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher).

This simple encryption method involves rotating characters in the alphabet (and does not
affect other characters like punctuation or spaces).

## Setting up the Working Environment

This English version of the lab is the repository's `main-en` branch. Open it in a
Codespace: on GitHub, on the `main-en` branch, **Code** > **Codespaces** > **Create
codespace on main-en**, or [this link](https://codespaces.new/shuuchuu/caesar-cipher/tree/main-en).
The Codespace installs the dependencies when it is created, in the project's `.venv`.

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
environment.

## Tests from the Specification

Without looking at the `src/caesar_cipher/caesar_cipher.py` file, and based on the
description of the Caesar cipher on Wikipedia (especially the examples given), write some
simple tests (as functions) that check the encryption of a string by the provided
`rotate` function, then run them.

Write them in a new `exercises.py` file at the root of the repository, which starts with:

```python
from caesar_cipher.caesar_cipher import rotate
```

and run it with `uv run python exercises.py`.

## TDD Approach (Test Driven Development)

We want to add a function `crack(ciphertext, known_word)` that recovers the key of an
encrypted message when one of its words is known. Develop it in `exercises.py`, following
the TDD cycle:

1. Write a test that checks that `crack(rotate("attaque à l'aube", 3), "aube")` is `3`,
   and run it: it must fail, since `crack` does not exist yet.
2. Write the minimal code that makes it pass.
3. Add a test that checks that `crack` raises a `ValueError` when no key reveals the
   word, see it fail, then make it pass.
4. Refactor your code if needed, checking that the tests still pass.

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

## Using `pytest`

Create a `tests/test_caesar_cipher.py` file and adapt the functions that test `rotate` to
make them compatible with `pytest`, grouping the examples in a single test with
`@pytest.mark.parametrize`.

Then use `pytest` to run the tests:

```console
uv run pytest
```

Finally, complete your test file to achieve 5 test cases.

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
[`unittest.mock.patch`](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch),
then checks the returned encrypted text and key, and that `random.randint` was called
once, with the arguments `(1, 25)`.

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

## Going Further

### Property-based Testing

Use [`hypothesis`](https://hypothesis.readthedocs.io/en/latest/) to test the `rotate`
function with random data.

### Contracts

Finally, integrate a pre-condition contract into the `src/caesar_cipher/caesar_cipher.py`
code. Use the [`deal`](https://deal.readthedocs.io/) library for this purpose.

### Mutation Testing

Use [`mutmut`](https://mutmut.readthedocs.io/) to find the behaviors your tests do not
check: each mutation that passes your test suite reveals one.

Iterate to reduce the number of mutations that pass your test suite:

```console
uv run mutmut run
uv run mutmut results
```

## Solution

The solutions of the exercises that create test files are on the repository's
[`solution` branch](https://github.com/shuuchuu/caesar-cipher/tree/solution).
