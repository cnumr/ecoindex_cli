from datetime import datetime
from json import loads
from os import getenv
from sys import getsizeof
from time import sleep
from typing import List, Optional

from ecoindex.ecoindex import get_ecoindex
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from ecoindex_cli.models import Page, PageMetrics, Result


def get_page_analysis(
    url: str, window_size: Optional[str] = "1920,1080"
) -> List[Result]:
    page = scrap_page(url=url, window_size=window_size)
    metrics = get_page_metrics(page=page)
    ecoindex = get_ecoindex(
        dom=metrics.nodes, size=metrics.size, requests=metrics.requests
    )

    return Result(
        score=ecoindex.score,
        ges=ecoindex.ges,
        water=ecoindex.ges,
        grade=ecoindex.grade,
        url=url,
        date=datetime.now(),
        resolution=window_size,
        nodes=metrics.nodes,
        size=metrics.size,
        requests=metrics.requests,
    )


def scrap_page(url: str, window_size: str) -> Page:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"--window-size={window_size}")

    capbs = webdriver.DesiredCapabilities.CHROME.copy()
    capbs["goog:loggingPrefs"] = {"performance": "ALL"}

    driver = webdriver.Chrome(
        desired_capabilities=capbs,
        executable_path=getenv("CHROMEDRIVER_PATH"),
        chrome_options=chrome_options,
    )
    driver.set_script_timeout(10)
    driver.get(url)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    # TODO : Find a way to wait for all elements downloaded after scrolling to bottom
    sleep(1)

    page = Page(
        logs=driver.get_log("performance"),
        outer_html=driver.execute_script("return document.documentElement.outerHTML"),
        nodes=driver.find_elements_by_xpath("//*"),
    )
    driver.quit()

    return page


def get_page_metrics(page: Page) -> PageMetrics:
    downloaded_data = [
        loads(log["message"])["message"]["params"]["encodedDataLength"]
        for log in page.logs
        if "INFO" == log["level"] and "Network.loadingFinished" in log["message"]
    ]

    return PageMetrics(
        size=(sum(downloaded_data) + getsizeof(page.outer_html)) / (10 ** 3),
        nodes=len(page.nodes),
        requests=len(downloaded_data),
    )
