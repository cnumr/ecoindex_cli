from typing import List, Optional
from urllib.request import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class Crawler:
    ignored_suffix = (".pdf", ".jpg")

    def __init__(self, max_urls: Optional[int] = 50) -> None:
        super().__init__()
        self.internal_urls = set()
        self.total_url_visited = 0
        self.max_urls = max_urls

    def is_valid(self, url: str) -> bool:
        """
        Checks whether `url` is a valid URL.
        """
        parsed = urlparse(url)
        return (
            bool(parsed.netloc)
            and bool(parsed.scheme)
            and bool(not url.lower().endswith(self.ignored_suffix))
        )

    def get_recursive_urls(self, url: str) -> List[str]:
        """
        Returns all URLs that is found on `url` in which it belongs to the same website
        """
        urls = set()
        domain_name = urlparse(url).netloc

        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue

            href = urljoin(url, href)
            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

            if not self.is_valid(href):
                continue

            if href in self.internal_urls:
                continue

            if domain_name not in href:
                continue

            urls.add(href)
            self.internal_urls.add(href)
        return urls

    def crawl(self, url: Optional[str] = None) -> None:
        """
        Crawls a web page and extracts all links.
        You'll find all links in `external_urls` and `internal_urls` global set variables.
        """
        self.total_url_visited += 1
        links = self.get_recursive_urls(url)

        if not links:
            return

        for link in links:
            if self.total_url_visited > self.max_urls:
                break
            self.crawl(link)

        return self.internal_urls
