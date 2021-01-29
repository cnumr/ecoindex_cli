from datetime import datetime
from typing import List, Optional

from ecoindex.models import Ecoindex
from pydantic import BaseModel, Field, HttpUrl
from starlette.routing import request_response

PageType = str


class WindowSize(BaseModel):
    height: int = Field(
        default=...,
        title="Window height",
        description="Height of the simulated window in pixel",
    )
    width: int = Field(
        default=...,
        title="Window width",
        description="Width of the simulated window in pixel",
    )

    def __str__(self) -> str:
        return f"{self.width},{self.height}"


class Page(BaseModel):
    logs: List
    outer_html: str
    nodes: List


class PageMetrics(BaseModel):
    size: float = Field(
        default=...,
        title="Page size",
        description="Is the size of the page and of the downloaded elements of the page in KB",
        ge=0,
    )
    nodes: int = Field(
        default=...,
        title="Page nodes",
        description="Is the number of the DOM elements in the page",
        ge=0,
    )
    requests: int = Field(
        default=...,
        title="Page requests",
        description="Is the number of external requests made by the page",
        ge=0,
    )


class WebPage(BaseModel):
    resolution: Optional[WindowSize] = Field(
        default=None,
        title="Page resolution",
        description="Resolution of the simulated window in pixel",
    )
    url: Optional[HttpUrl] = Field(
        default=None, title="Page url", description="Url of the analysed page"
    )


class Result(Ecoindex, PageMetrics, WebPage):
    date: Optional[datetime] = Field(
        default=None, title="Analysis datetime", description="Date of the analysis"
    )
    page_type: Optional[PageType] = Field(
        default=None,
        title="Page type",
        description="Is the type of the page, based ton the [opengraph type tag](https://ogp.me/#types)",
    )
