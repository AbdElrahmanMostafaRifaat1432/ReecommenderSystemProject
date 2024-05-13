import difflib
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html


def __get_closest_titles(title: str, titles: list, num_matches: int = 10) -> list:
    """
    Get the closest titles to the given title from the list of titles.
    """
    titles = [t.lower() for t in titles]

    closest_titles = difflib.get_close_matches(
        title.lower(), titles, n=num_matches)
    print(closest_titles)
    return closest_titles


def get_closest_matches(title: str, df: pd.DataFrame, column: str, num_matches: int = 10) -> pd.DataFrame:
    """
    Get the closest matches to the given title from the given column of the dataframe.
    """
    closest_titles = __get_closest_titles(
        title, df[column].tolist(), num_matches)
    closest_matches = pd.DataFrame()
    for closest_title in closest_titles:
        closest_matches = pd.concat(
            [closest_matches, df[df[column].str.lower() == closest_title]])
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


def get_n_top_movies(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
    """
    Get the n top popular movies from the given dataframe.
    """
    top_movies = df.sort_values(by=column, ascending=False).head(n)
    return top_movies


def get_random_userid(df: pd.DataFrame) -> int:
    """
    Get a random userId from the unique userIds in the dataframe.
    """
    userId = df['userId'].sample().values[0]
    return userId


def get_user_ratings(df: pd.DataFrame, user_id: int, n: int = 10) -> pd.DataFrame:
    """
    Get the n ratings of the given user from the dataframe.
    """
    user_ratings = df[df['userId'] == user_id].head(n)
    return user_ratings

# function to get movies from id list


def get_movies_from_id_list(df: pd.DataFrame, id_list: list) -> pd.DataFrame:
    """
    Get the movies from the given list of ids from the dataframe.
    """
    # add each movie to a pandas dataframe, with the same sequence as the id_list
    movies = pd.DataFrame()
    for movie_id in id_list:
        movie = df[df['movieId'] == movie_id]
        movies = pd.concat([movies, movie])
    return movies


def create_smaller_movie_card(movie, with_description: bool = True):
    if with_description:
        desc = f"Description: {movie['description']}"
    else:
        desc = ""
    return dbc.Card([
        dbc.CardImg(src=movie['image'],
                    top=True,
                    style={"height": "50%",
                           "width": "100%",
                           #    "objectFit": "cover",
                           "padding": "10",
                           "marginTop": "10px",
                           }),
        dbc.CardBody([
            html.H5(movie['title'], className="card-title"),
            html.P(
                ([dbc.Badge(genre, color="primary", className="mr-1", style={"margin": "2px",
                                                                             "fontSize": "0.8em"})
                 for genre in get_genres(movie)]),
                className="card-text"
            ),
            html.P(
                desc, className="card-text"),
            # dbc.Button("See more", id=str(movie['movieId']),
            #            className="see-more-button", n_clicks=0),
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
        className="movie-card-main",
        style={
        "width": "16rem",
        "margin": "6px",
    }
    )


def create_movie_card(movie, with_description: bool = True):
    if with_description:
        desc = f"Description: {movie['description']}"
    else:
        desc = ""
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
            html.P(f"Year: {int(movie['year'])}", className="card-text"),
            html.P(
                desc, className="card-text"),
            # dbc.Button("See more", id=str(movie['movieId']),
            #            className="see-more-button", n_clicks=0),
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
        className="movie-card-main",
        style={
        "width": "20rem",
        "margin": "6px",
    }
    )


# # create a modal based on the movie clicked
# def create_movie_modal(movie):
#     return dbc.Modal([
#         dbc.ModalHeader(movie['title']),
#         dbc.ModalBody([
#             html.Img(src=movie['image'],
#                      style={"height": "50%",
#                             "width": "100%",
#                             "objectFit": "cover",
#                             "padding": "10",
#                             "marginTop": "10px",
#                             }),
#             html.H4("Description", className="modal-title"),
#             html.P(movie['description'], className="modal-text"),
#             html.H4("Genres", className="modal-title"),
#             html.P(
#                 ([dbc.Badge(genre, color="primary", className="mr-1", style={"margin": "2px",  # make it bigger
#                                                                              "fontSize": "1.2em"})
#                   for genre in get_genres(movie)]),
#                 className="modal-text"
#             ),
#             html.H4("Year", className="modal-title"),
#             html.P(movie['year'], className="modal-text"),
#         ]
#         ),
#         dbc.ModalFooter(
#             dbc.Button("Close", id="close", className="ml-auto")
#         )
#     ],
#         id="modal",
#         size="lg",
#         is_open=False
#     )
