from click.exceptions import BadParameter
from ecoindex_cli.cli.arguments_handler import (
    get_url_from_args,
    get_window_sizes_from_args,
)
from ecoindex_cli.models import WindowSize
from pydantic import ValidationError
from pytest import raises


def test_urls_all_valid_from_args():
    urls = ("http://test.com", "https://test.com", "https://www.dummy.com/page/")
    valid_urls = get_url_from_args(urls_arg=urls)
    assert len(valid_urls) == 3
    for url in valid_urls:
        assert url in urls


def test_urls_invalid_from_args():
    urls = "test.com"
    with raises(ValidationError):
        get_url_from_args(urls)


def test_validate_valid_window_size():
    assert get_window_sizes_from_args(["1024,768"]) == [
        WindowSize(width=1024, height=768)
    ]


def test_validate_invalid_window_size():
    with raises(ValidationError):
        get_window_sizes_from_args(("800x600",))

    with raises(ValidationError):
        get_window_sizes_from_args(("width,600",))

    with raises(ValidationError):
        get_window_sizes_from_args(("600",))
