from click.exceptions import BadParameter
from pytest import raises

from ecoindex_cli.arguments_handler import get_url_from_args


def test_urls_all_valid_from_args():
    urls = ("http://test.com", "https://test.com", "https://www.dummy.com/page/")
    valid_urls = get_url_from_args(urls_arg=urls)
    assert len(valid_urls) == 3
    for url in valid_urls:
        assert url in urls


def test_urls_invalid_from_args():
    urls = "test.com"
    with raises(BadParameter):
        get_url_from_args(urls)
