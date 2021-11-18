from ecoindex.models import WindowSize
from ecoindex_cli.cli.arguments_handler import (
    get_file_prefix_input_file_logger_file,
    get_url_from_args,
    get_window_sizes_from_args,
)
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


def test_get_file_prefix_input_file_logger_file():
    urls = ("http://test.com", "https://test.com", "https://www.dummy.com/page/")
    assert get_file_prefix_input_file_logger_file(urls=urls) == (
        "test.com",
        "/tmp/ecoindex-cli/input/test.com.csv",
        "test.com.log",
    )

    assert get_file_prefix_input_file_logger_file(
        urls=urls, urls_file="/home/user/my_urls.csv"
    ) == (
        "my_urls.csv",
        "/home/user/my_urls.csv",
        "my_urls.csv.log",
    )
