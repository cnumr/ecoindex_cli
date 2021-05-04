from ecoindex_cli.validators import validate_url


def test_validate_valid_url():
    assert validate_url(url="https://www.test.fr")
    assert validate_url(url="http://www.test.fr")
    assert validate_url(url="http://test.fr")
    assert validate_url(url="http://test.fr/")
    assert validate_url(url="http://www.test.fr/index")
    assert validate_url(url="http://www.test.fr/index.html")
    assert validate_url(url="http://www.test.fr/index?param=value")
