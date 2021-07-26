from datetime import datetime
from typing import List, Optional

from ecoindex.models import Ecoindex
from pydantic import BaseModel, HttpUrl

PageType = str


class WindowSize(BaseModel):
    height: int
    width: int

    def __str__(self) -> str:
        return f"{self.width},{self.height}"


class Page(BaseModel):
    logs: List
    outer_html: str
    nodes: List


class PageMetrics(BaseModel):
    size: float
    nodes: int
    requests: int


class Result(Ecoindex, PageMetrics):
    url: Optional[HttpUrl] = None
    date: Optional[datetime] = None
    resolution: Optional[str] = None
    page_type: Optional[PageType] = None
