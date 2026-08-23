"""A module containing common functions used throughout the app."""


def _clean_number_string(value: str) -> str:
    """Helper function to clean up different variations of number strings.

    This function removes leading and trailing whitespace from the specified
    number string, checks for a range of numbers and keeps only the upper bound,
    and then strips out any commas appearing in the number string.

    Returns:
        A string that should be able to cast to an int or float.
    """
    # Remove all leading and trailing whitespace
    value = value.strip()

    # If the value is a range (e.g., "20-30"), take the upper bound
    splits = value.split("-", maxsplit=1)
    if len(splits) == 2:
        value = splits[1]

    # Collapse any commas in the value (e.g., "1,000" becomes "1000")
    value = value.replace(",", "")

    return value


def parse_int(value: str) -> int:
    """Return the integer value of a string or 0 if the string is not a valid integer."""
    try:
        return int(_clean_number_string(value))
    except ValueError:
        return 0


def parse_float(value: str) -> float:
    """Return the float value of a string or 0 if the string is not a valid float."""
    try:
        return float(_clean_number_string(value))
    except ValueError:
        return 0.0
