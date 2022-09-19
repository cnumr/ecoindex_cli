from enum import Enum


class ExportFormat(Enum):
    csv = "csv"
    json = "json"


class Language(Enum):
    fr = "fr"
    en = "en"


class Target(Enum):
    nodes = 600
    requests = 40
    size = 1024


class GlobalMedian(Enum):
    nodes = 693
    requests = 78
    size = 2410
