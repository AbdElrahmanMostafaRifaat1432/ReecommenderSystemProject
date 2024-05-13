import dash
from dash import html, dcc, callback, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import os
from utils.helper_func import *

movies_df = pd.read_csv('data/movies_links.csv')
unique_genres = get_unique_genres(movies_df, 'genres')
unique_years = get_unique_raw(movies_df, 'year')


dash.register_page(
    __name__,
    path="/",
    name="Home",
)

layout = html.Div(
    [
        html.Div([
            dbc.Row([
                html.H4("Find new movies!", className="main-sub-title"),
            ],),
            dbc.Row([

                dbc.Col([
                    html.Div(id='movie-carousel'),
                ],
                    width=12,
                ),
            ]),
        ],
            style={"height": "300px"}
        ),
        html.Div([
            dbc.Row([
                html.H4("Top popular movies!", className="sub-title"),
            ],),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        create_smaller_movie_card(
                            movie, with_description=False)
                        for movie in get_n_top_movies(movies_df, 'ratings_count', 12).to_dict(orient='records')
                    ],
                        style={"margin": "10px",
                               "justify-content": "center",
                               "height": "100px"
                               }
                    ),
                ],
                    width=12,
                ),
            ]),
        ],
            style={"marginTop": "340px"}
        ),
        html.Div([
            dbc.Row([
                html.H4("Top rated movies!", className="sub-title"),
            ],),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        create_smaller_movie_card(
                            movie, with_description=False)
                        for movie in get_n_top_movies(movies_df, 'average_rating', 12).to_dict(orient='records')
                    ],
                        style={"margin": "10px",
                               "justify-content": "center",
                               }
                    ),
                ],
                    width=12,
                ),
            ],
            ),
        ],
            style={"marginTop": "1000px"}
        ),

        dcc.Interval(
            id='interval-component',
            interval=3000,  # in milliseconds
            n_intervals=0
        ),

    ],

)


@callback(
    Output("movie-carousel", "children"),
    Input("interval-component", "n_intervals")
)
def update_cards(n):
    # if n is more than the number of movies, reset n
    if n+7 > len(movies_df):
        n = 0

    return dbc.Row([
        create_smaller_movie_card(movie, with_description=False)
        for movie in movies_df.iloc[n:n+7].to_dict(orient='records')
    ],
        style={"margin": "10px",
               "justify-content": "center",
               "height": "100px"
               }
    )
