from asyncio import run

from ecoindex.models import Result, WindowSize
from ecoindex_scraper.scrap import EcoindexScraper


def run_page_analysis(
    url: str, window_size: WindowSize, chrome_version: int | None = None
) -> Result:
    return run(
        EcoindexScraper(
            url=url, window_size=window_size, chrome_version_main=chrome_version
        )
        .init_chromedriver()
        .get_page_analysis()
    )
