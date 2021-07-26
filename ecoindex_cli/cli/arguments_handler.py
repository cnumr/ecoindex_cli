from tempfile import NamedTemporaryFile
from typing import List, Set, Tuple
from urllib.parse import urlparse

from click.exceptions import BadParameter
from ecoindex_cli.crawl import EcoindexSpider
from ecoindex_cli.models import WindowSize
from pydantic import validate_arguments
from pydantic.networks import HttpUrl
from scrapy.crawler import CrawlerProcess


def get_urls_from_file(urls_file: str) -> List[HttpUrl]:
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


@validate_arguments
def get_url_from_args(urls_arg: Tuple[HttpUrl]) -> Set[HttpUrl]:
    urls_from_args = set()
    for url in urls_arg:
        urls_from_args.add(url)

    return urls_from_args


def get_window_sizes(window_sizes: Tuple[str]) -> List[WindowSize]:
    result = []
    error = ""
    for window_size in window_sizes:
        try:
            width, height = window_size.split(",")
            result.append(WindowSize(width=int(width), height=int(height)))
        except ValueError:
            error += f"🔥 {window_size} is not a valid window size. Must be of type `1920,1080`\n"
            raise BadParameter(
                message=f"🔥 {window_size} is not a valid window size. Must be of type 1920,1080"
            )
    if error:
        raise BadParameter(message=error)

    return result
