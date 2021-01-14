from dataclasses import dataclass
from datetime import datetime
from typing import List

from ecoindex.models import Ecoindex


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
    url: str
    date: datetime
    resolution: str

    def list_attributes(self):
        print(self)
