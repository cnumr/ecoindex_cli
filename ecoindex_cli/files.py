from csv import DictWriter
from os import makedirs
from os.path import exists
from typing import List

from ecoindex.models import Result


def create_folder(path: str) -> None:
    if not exists(path):
        makedirs(path)


def write_results_to_file(filename: str, results: List[Result]) -> None:
    headers = results[0].__dict__

    with open(filename, "w") as fp:
        writer = DictWriter(fp, fieldnames=headers)

        writer.writeheader()
        for ecoindex in results:
            writer.writerow(ecoindex.__dict__)


def write_urls_to_file(file_prefix: str, urls: List[str]) -> None:
    tmp_input_folder = "/tmp/ecoindex-cli/input"
    create_folder(tmp_input_folder)
    with open(
        file=f"{tmp_input_folder}/{file_prefix}.csv", mode="w"
    ) as input_urls_file:
        for url in urls:
            input_urls_file.write(f"{url.strip()}\n")
