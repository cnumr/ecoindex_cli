from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from ecoindex.models import Ecoindex


@dataclass
class Page:
    logs: str
    outer_html: str
    nodes: List


@dataclass
class PageMetrics:
    size: Optional[float] = None
    nodes: Optional[int] = None
    requests: Optional[int] = None


@dataclass
class Result(Ecoindex, PageMetrics):
    url: str = ""
    date: datetime = datetime.now()
    resolution: str = ""

    def list_attributes(self):
        print(self)
