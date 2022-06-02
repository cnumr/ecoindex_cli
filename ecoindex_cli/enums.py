from enum import Enum


class ExportFormat(Enum):
    csv = "csv"
    json = "json"


class Language(Enum):
    fr = "fr"
    en = "en"


class Target(Enum):
    nodes = 878  # Arbitrary value, must be evaluated later
    requests = 69  # Based on https://almanac.httparchive.org/en/2021/page-weight#requests (Mobile)
    size = 1923  # Based on https://almanac.httparchive.org/en/2021/page-weight#page-weight-by-the-numbers (Mobile)
