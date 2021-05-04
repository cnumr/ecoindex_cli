from typing import Set, Tuple
from urllib.parse import urlparse

from click.exceptions import BadParameter

from ecoindex_cli.recursive import Crawler
from ecoindex_cli.validators import validate_url


def get_urls_from_file(urls_file: str) -> Set[str]:
    try:
        with open(urls_file) as fp:
            urls_from_file = set()
            for url in fp.readlines():
                url = url.replace("\n", "")
                if validate_url(url):
                    urls_from_file.add(url)

            return urls_from_file

    except FileNotFoundError:
        raise BadParameter(message=f"🔥 File {urls_file} is not valid")


def get_urls_recursive(main_url: str) -> Tuple[str]:
    parsed_url = urlparse(main_url)
    main_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    crawler = Crawler()
    urls = crawler.crawl(url=main_url)

    return urls


def get_url_from_args(urls_arg: Tuple[str]) -> Set[str]:
    urls_from_args = set()
    for url in urls_arg:
        if validate_url(url):
            urls_from_args.add(url)

    return urls_from_args
