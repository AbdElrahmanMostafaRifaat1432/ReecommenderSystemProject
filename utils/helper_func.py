import difflib
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html


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


def get_unique_raw(df: pd.DataFrame, column: str = 'year') -> list:
    """
    Get the unique of a column that has raw python type from the given column of the dataframe.
    """
    unique_years = df[column].unique()
    unique_years = [year for year in unique_years if pd.notnull(year)]
    return unique_years


def get_unique_genres(df: pd.DataFrame, column: str) -> list:
    """
    Get the unique genres from the given column of the dataframe.
    """
    unique_genres = df[column].str.split('|').explode().str.strip().unique()
    unique_genres = [
        genre for genre in unique_genres if genre != '(no genres listed)']
    return unique_genres


def get_genres(row: pd.Series) -> list:
    """
    Get the genres from the given row.
    """
    genres = row['genres'].split('|')
    genres = [genre.strip() for genre in genres]
    return genres


def create_movie_card(movie):
    return dbc.Card([
        dbc.CardImg(src=movie['image'],
                    top=True,
                    style={"height": "50%",
                           "width": "100%",
                           "objectFit": "cover",
                           "padding": "10",
                           "marginTop": "10px",
                           }),
        dbc.CardBody([
            html.H4(movie['title'], className="card-title"),
            html.P(
                ([dbc.Badge(genre, color="primary", className="mr-1", style={"margin": "2px",  # make it bigger
                                                                             "fontSize": "1.2em"})
                  for genre in get_genres(movie)]),
                className="card-text"
            ),
            html.P(f"Year: {movie['year']}", className="card-text"),
            html.P(
                f"Description: {movie['description']}", className="card-text"),
        ],
            style={
            "backgroundColor": "black",
            "color": "white",
            "marginTop": "10px",
            "marginBottom": "10px",
            "borderRadius": "10px",
        }
        ),
    ],
        style={
        "width": "20rem",
        "margin": "6px",
    }
    )
