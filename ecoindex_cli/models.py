from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from ecoindex.models import Ecoindex

PageType = str


@dataclass
class Page:
    logs: str
    outer_html: str
    nodes: List


@dataclass
class PageMetrics:
    size: float
    nodes: int
    requests: int


@dataclass
class Result(Ecoindex, PageMetrics):
    url: Optional[str] = None
    date: Optional[datetime] = None
    resolution: Optional[str] = None
    page_type: Optional[PageType] = None

    def list_attributes(self):
        print(self)
