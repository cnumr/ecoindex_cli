from enum import Enum


class ExportFormat(Enum):
    csv = "csv"
    json = "json"


class Language(Enum):
    fr = "fr"
    en = "en"


class Target(Enum):
    nodes = 500
    requests = 27
    size = 900


class GlobalMedian(Enum):
    nodes = 693
    requests = 78
    size = 2410
