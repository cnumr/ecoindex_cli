from typing import List

from ecoindex_cli.models import Result, WebPage, WindowSize
from ecoindex_cli.scrap import get_page_analysis
from fastapi import Body, FastAPI
from fastapi.datastructures import Default
from pydantic import HttpUrl

app = FastAPI(
    title="Ecoindex API",
    description="This is the implementation of the [`ecoindex_cli`](https://github.com/cnumr/ecoindex_cli) for an API use.",
    version="1.0.0",
)


@app.post(
    "/analysis",
    response_model=List[Result],
    description="Make an ecoindex analysis on given urls",
    tags=["ecoindex"],
)
async def analyze_websites(
    webpages: List[WebPage] = Body(
        default=...,
        title="List of webpages",
        description="Array of urls and window resolution you want to analyze",
        example=[
            WebPage(
                url="http://ecoindex.fr",
                resolution=WindowSize(width=1920, height=1080),
            ),
            WebPage(
                url="https://www.greenit.fr/",
                resolution=WindowSize(width=800, height=600),
            ),
        ],
    ),
) -> List[Result]:
    return [
        get_page_analysis(url=webpage.url.strip(), window_size=webpage.resolution)
        for webpage in webpages
    ]
