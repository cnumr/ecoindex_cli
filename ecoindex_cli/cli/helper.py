from asyncio import run

from ecoindex_scraper.models import Result, WindowSize
from ecoindex_scraper.scrap import EcoindexScraper


def run_page_analysis(url: str, window_size: WindowSize) -> Result:
    return run(
        EcoindexScraper(url=url, window_size=window_size)
        .init_chromedriver()
        .get_page_analysis()
    )
