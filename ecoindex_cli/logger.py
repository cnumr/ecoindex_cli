import logging

from ecoindex_cli.files import create_folder


class Logger:
    def __init__(self, filename: str) -> None:
        self.path = "/tmp/ecoindex-cli/logs"
        self.file_name = filename
        create_folder(path=self.path)

        logging.basicConfig(
            filemode="w+",
            filename=self.path + "/" + filename,
            format="%(asctime)s %(message)s",
        )

    def error(self, msg: str) -> None:
        logging.error(msg)
