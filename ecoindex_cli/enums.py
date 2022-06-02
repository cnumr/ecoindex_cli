from enum import Enum


class ExportFormat(Enum):
    csv = "csv"
    json = "json"


class Language(Enum):
    fr = "fr"
    en = "en"


class Target(Enum):
    nodes = 878
    requests = 54
    size = 2131
