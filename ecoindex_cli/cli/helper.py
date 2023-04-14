from asyncio import run

from ecoindex.models import Result, WindowSize
from ecoindex_scraper.scrap import EcoindexScraper


def run_page_analysis(
    url: str,
    window_size: WindowSize,
    chrome_version: int | None = None,
    driver_executable_path: str = "",
    wait_after_scroll: int = 3,
    wait_before_scroll: int = 3,
) -> Result:
    scraper = EcoindexScraper(
        url=url,
        window_size=window_size,
        chrome_version_main=chrome_version,
        driver_executable_path=driver_executable_path,
        wait_after_scroll=wait_after_scroll,
        wait_before_scroll=wait_before_scroll,
    )

    scraper.init_chromedriver()

    return run(scraper.get_page_analysis())
