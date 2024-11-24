from lclib import lichess

def test_year_month():
    year, month = lichess.get_year_month_from_filename("lichess_db_standard_rated_2024-10.pgn")
    print(year, month)

test_year_month()