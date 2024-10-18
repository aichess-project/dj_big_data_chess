from typing import Tuple

def next_year_month(year: int, month: int) -> Tuple[int, int]:
    """
    Compute the next year and month given the current year and month.

    :param year: Current year (int8)
    :param month: Current month (int8)
    :return: A tuple containing the next year and month
    """
    # Ensure month is between 1 and 12
    if not (1 <= month <= 12):
        raise ValueError("Month must be between 1 and 12")

    # Handle month transition
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    return next_year, next_month

def str_replace_year_month(string, year, month) -> str:
    file_name = f"{string}".replace("<YEAR>", str(year)).replace("<MONTH>", f"{month:02}")
    return file_name
