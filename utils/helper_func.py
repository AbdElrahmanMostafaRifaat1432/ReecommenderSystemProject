import difflib
import pandas as pd


def __get_closest_titles(title: str, titles: list, num_matches: int = 10) -> list:
    """
    Get the closest titles to the given title from the list of titles.
    """
    closest_titles = difflib.get_close_matches(title, titles, num_matches)
    return closest_titles


def get_closest_matches(title: str, df: pd.DataFrame, column: str, num_matches: int = 10) -> pd.DataFrame:
    """
    Get the closest matches to the given title from the given column of the dataframe.
    """
    closest_titles = __get_closest_titles(
        title, df[column].tolist(), num_matches)
    closest_matches = df[df[column].isin(closest_titles)]
    return closest_matches
