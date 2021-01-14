from csv import DictWriter
from typing import List

from ecoindex_cli.models import Result


def write_results_to_csv(filename: str, results: List[Result]) -> None:
    headers = results[0].__dict__

    with open(filename, "w") as fp:
        writer = DictWriter(fp, fieldnames=headers)

        writer.writeheader()
        for ecoindex in results:
            writer.writerow(ecoindex.__dict__)
