from tempfile import NamedTemporaryFile
from typing import Set, Tuple
from urllib.parse import urlparse

from click.exceptions import BadParameter
from scrapy.crawler import CrawlerProcess

from ecoindex_cli.crawl import EcoindexSpider
from ecoindex_cli.validators import validate_url


def get_urls_from_file(urls_file: str) -> Set[str]:
    try:
        with open(urls_file) as fp:
            urls_from_file = set()
            for url in fp.readlines():
                url = url.strip()
                if validate_url(url):
                    urls_from_file.add(url)

            return urls_from_file

    except FileNotFoundError:
        raise BadParameter(message=f"🔥 File {urls_file} is not valid")


def get_urls_recursive(main_url: str) -> Tuple[str]:
    parsed_url = urlparse(main_url)
    domain = parsed_url.netloc
    main_url = f"{parsed_url.scheme}://{domain}"
    process = CrawlerProcess()

    with NamedTemporaryFile(mode="w+t") as temp_file:
        process.crawl(
            crawler_or_spidercls=EcoindexSpider,
            allowed_domains=[domain],
            start_urls=[main_url],
            temp_file=temp_file,
        )
        process.start()
        temp_file.seek(0)
        urls = temp_file.readlines()

    return urls


def get_url_from_args(urls_arg: Tuple[str]) -> Set[str]:
    urls_from_args = set()
    for url in urls_arg:
        if validate_url(url):
            urls_from_args.add(url)

    return urls_from_args
