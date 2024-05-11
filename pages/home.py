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
        html.Div(id='movie-carousel'),

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
    # based on n, get the next 3 movies, and create the cards and put them in a single row
    # return the row
    return dbc.Row([
        create_movie_card(movie, with_description=False)
        for movie in movies_df.iloc[n:n+3].to_dict(orient='records')
    ],
        style={"margin": "10px",
               "justify-content": "center",
               "height": "300px"
               }
    )
