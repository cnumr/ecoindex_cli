import logging


class logger:
    def __init__(self, f_name):
        logging.basicConfig(
            filemode="w", filename=f_name, format="%(asctime)s %(message)s"
        )

    def error(self, msg):
        logging.error(msg)
