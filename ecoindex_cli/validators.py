from logging import error
from typing import Tuple

from click.exceptions import BadParameter


def validate_window_size(window_sizes: Tuple[str]) -> bool:
    for window_size in window_sizes:
        try:
            width, height = window_size.split(",")
            int(width)
            int(height)
        except ValueError:
            raise BadParameter(
                message=f"🔥 {window_size} is not a valid window size. Must be of type 1920,1080"
            )

    return True
