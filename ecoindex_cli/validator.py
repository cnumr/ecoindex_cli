from validators import validator


@validator
def window_size(values: str) -> bool:
    for value in values:
        try:
            width, height = value.split(",")
            int(width)
            int(height)
        except ValueError:
            return False

    return True
