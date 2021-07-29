from csv import DictWriter
from typing import List

from ecoindex.models import Result


def write_results_to_file(filename: str, results: List[Result]) -> None:
    headers = results[0].__dict__

    with open(filename, "w") as fp:
        writer = DictWriter(fp, fieldnames=headers)

        writer.writeheader()
        for ecoindex in results:
            writer.writerow(ecoindex.__dict__)


def write_urls_to_file(domain: str, urls: List[str]) -> None:
    with open(file=f"input/{domain}.csv", mode="w") as input_urls_file:
        for url in urls:
            input_urls_file.write(f"{url.strip()}\n")
