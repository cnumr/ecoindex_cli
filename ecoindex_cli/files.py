from abc import ABC, abstractmethod
from csv import DictWriter
from json import dump
from os import makedirs
from os.path import exists
from typing import List, Optional

from ecoindex_scraper.models import Result

from ecoindex_cli.enums import ExportFormat


def create_folder(path: str) -> None:
    if not exists(path):
        makedirs(path)


class File(ABC):
    def __init__(
        self,
        filename: str,
        results: List[Result],
        export_format: Optional[ExportFormat] = ExportFormat.csv,
    ):
        self.filename = filename
        self.results = results
        self.export_format = export_format

    @abstractmethod
    def write(self) -> None:
        pass


class CsvFile(File):
    def write(self) -> None:
        headers = self.results[0].__dict__

        with open(self.filename, "w") as fp:
            writer = DictWriter(fp, fieldnames=headers)

            writer.writeheader()
            for ecoindex in self.results:
                writer.writerow(ecoindex.__dict__)


class JsonFile(File):
    def write(self) -> None:
        with open(self.filename, "w") as fp:
            dump(
                obj=[ecoindex.__dict__ for ecoindex in self.results],
                fp=fp,
                indent=4,
                default=str,
            )


def write_results_to_file(
    filename: str,
    results: List[Result],
    export_format: Optional[ExportFormat] = ExportFormat.csv,
) -> None:
    print(export_format)
    if export_format == ExportFormat.csv:
        file = CsvFile(filename=filename, results=results, export_format=export_format)
    elif export_format == ExportFormat.json:
        file = JsonFile(filename=filename, results=results, export_format=export_format)

    file.write()


def write_urls_to_file(file_prefix: str, urls: List[str]) -> None:
    tmp_input_folder = "/tmp/ecoindex-cli/input"
    create_folder(tmp_input_folder)
    with open(
        file=f"{tmp_input_folder}/{file_prefix}.csv", mode="w"
    ) as input_urls_file:
        for url in urls:
            input_urls_file.write(f"{url.strip()}\n")
