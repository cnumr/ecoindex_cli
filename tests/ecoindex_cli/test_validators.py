from click.exceptions import BadArgumentUsage, BadParameter
from pytest import raises

from ecoindex_cli.validators import validate_url, validate_window_size


def test_validate_valid_url():
    assert validate_url(url="https://www.test.fr")
    assert validate_url(url="http://www.test.fr")
    assert validate_url(url="http://test.fr")
    assert validate_url(url="http://test.fr/")
    assert validate_url(url="http://www.test.fr/index")
    assert validate_url(url="http://www.test.fr/index.html")
    assert validate_url(url="http://www.test.fr/index?param=value")


def test_validate_invalid_url():
    with raises(BadParameter):
        validate_url("test.fr")


def test_validate_valid_window_size():
    assert validate_window_size(("800,600", "1024,768"))


def test_validate_invalid_window_size():
    with raises(BadParameter):
        validate_window_size(("800x600",))

    with raises(BadParameter):
        validate_window_size(("width,600",))

    with raises(BadParameter):
        validate_window_size(("600",))
