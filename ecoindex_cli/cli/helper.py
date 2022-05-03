from asyncio import run

from ecoindex_scraper import get_page_analysis
from ecoindex_scraper.models import Result, WindowSize


def run_page_analysis(url: str, window_size: WindowSize) -> Result:
    return run(get_page_analysis(url=url, window_size=window_size))
