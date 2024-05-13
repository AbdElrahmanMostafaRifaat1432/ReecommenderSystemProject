import dash
from dash import html, dcc, callback, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import os
from utils.helper_func import *
from src.movie_rec import *
import numpy as np

movies_df = pd.read_csv('data/movies_links.csv')
ratings_df = pd.read_csv('data/ratings.csv')
unique_genres = get_unique_genres(movies_df, 'genres')
unique_years = get_unique_raw(movies_df, 'year')

userid = get_random_userid(ratings_df)
user_ratings = get_user_ratings(ratings_df, userid)
user_ratings = user_ratings.merge(movies_df, on='movieId')
user_ratings = user_ratings[['userId', 'title', 'rating']]

final_dataset, sample, sparsity, movies = data_prep()
csr_data, knn = create_model(sample, final_dataset)

dash.register_page(
    __name__,
    path="/Recommend",
    name="Recommend",
)

layout = html.Div([
    dbc.Row([
            dbc.Col([
                html.H2("Hello User" + str(userid)),
                html.H3("User Ratings"),
                html.Div([
                    html.H5("User Ratings"),
                    html.Table([
                        html.Thead([
                            html.Tr([html.Th("Title"), html.Th("Rating")])
                        ]),
                        html.Tbody([
                            html.Tr([html.Td(user_ratings.iloc[i]['title']),
                                     html.Td(user_ratings.iloc[i]['rating'])])
                            for i in range(user_ratings.shape[0])
                        ])
                    ])
                ])
            ], width=2),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.H4("Recommend",
                                style={
                                    "padding": "10px",
                                    "borderRadius": "10px",
                                    "color": "white",
                                    "textAlign": "center",
                                    "marginBottom": "10px",
                                    "marginTop": "10px"}
                                ),
                    ],
                        width=2,
                    ),
                    dbc.Col([
                        dbc.Input(
                            id="search",
                            type="text",
                            placeholder="Search for a movie",
                            style={"width": "100%",
                                   "height": "100%",
                                   "borderRadius": "40px", }
                        ),
                    ],
                        width=8,

                    ),
                    dbc.Col([
                        dbc.Button(
                            "'mend it!",
                            id="search-button",
                            className="coins-navbar-expand",
                            style={"width": "100%",
                                   "height": "80%",
                                   "textAlign": "center",
                                   "fontSize": "1.5em",
                                   "borderRadius": "10px",
                                   }
                        ),
                    ],
                        width=2,
                        style={"display": "flex",
                               "alignItems": "center",
                               "justifyContent": "center"}
                    ),

                ],),
                html.Div(html.H1("Your search bar is feeling cinematic! Type in a movie!", style={"textAlign": "center", "marginTop": "150px"}), id="movie-recommend-cards",
                         style={"display": "flex",
                                "flexWrap": "wrap",
                                            "justifyContent": "center"}
                         ),
                html.Div(html.H1("Your search bar is feeling cinematic! Type in a movie!", style={"textAlign": "center", "marginTop": "150px"}), id="user-recommend-cards",
                         style={"display": "flex",
                                "flexWrap": "wrap",
                                "justifyContent": "center"}
                         ),
            ], width=10)

            ],

            style={"marginBottom": "10px",
                   "marginTop": "10px"},),
],
)
