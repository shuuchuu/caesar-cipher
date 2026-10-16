import deal
import pytest

from caesar_cipher.caesar_cipher import crack


def test_crack_rejects_empty_word():
    with pytest.raises(deal.PreContractError):
        crack("bonjour", "")
