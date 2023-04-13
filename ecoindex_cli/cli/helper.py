from asyncio import run

from ecoindex.models import Result, WindowSize
from ecoindex_scraper.scrap import EcoindexScraper


def run_page_analysis(
    url: str,
    window_size: WindowSize,
    chrome_version: int | None = None,
    driver_executable_path: str = "",
) -> Result:
    scraper = EcoindexScraper(
        url=url,
        window_size=window_size,
        chrome_version_main=chrome_version,
        driver_executable_path=driver_executable_path,
    )

    scraper.init_chromedriver()

    return run(scraper.get_page_analysis())
