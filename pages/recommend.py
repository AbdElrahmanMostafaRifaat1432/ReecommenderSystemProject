import dash
from dash import html, dcc, callback, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import os
from utils.helper_func import *
from src.movie_rec import *
from src.user_rec import *
import numpy as np

movies_df = pd.read_csv('data/movies_links.csv')
ratings_df = pd.read_csv('data/ratings.csv')
data_df = pd.read_csv('data/data.csv')


k = 10
user_id = get_random_userid(ratings_df)
user_ratings = get_user_ratings(ratings_df, user_id, 30)
user_ratings = user_ratings.merge(movies_df, on='movieId')
user_ratings = user_ratings[['userId', 'title', 'rating']]

movie_final_dataset, movie_sample, movie_sparsity, movie_movies = data_prep()
movie_csr_data, movie_knn = create_model(movie_sample, movie_final_dataset)

user_genres_list, user_concatenated_tags_list, user_data, model = init()
user_reccomendations = user_recomm(user_id, user_genres_list,
                                   user_concatenated_tags_list, user_data, model, k)

# user_reccomendations = [461, 659, 895, 314, 46, 913, 921, 1733, 2224, 6693]
user_reccomendations = get_movies_from_id_list(movies_df, user_reccomendations)

user_movie_cards = [create_movie_card(movie)
                    for _, movie in user_reccomendations.iterrows()]

dash.register_page(
    __name__,
    path="/Recommend",
    name="Recommend",
)

layout = html.Div([
    dbc.Row([
            dbc.Col([
                html.H2("Hello User " + str(user_id)),
                html.Div([
                    html.H5("User Ratings"),

                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H5("Title"),
                                ],),
                                dbc.Col([
                                    html.H5("Rating"),
                                ],
                                    style={"textAlign": "right"}
                                ),
                            ]),
                            html.Hr(),
                            html.Div([
                                dbc.Row([
                                    dbc.Col(
                                        movie['title'],
                                        width=9
                                    ),
                                    dbc.Col([
                                        dbc.Badge(
                                            movie['rating'], color="primary"),
                                    ],
                                        width=3
                                    ),
                                ],
                                    style={"marginBottom": "8px"}

                                ) for _, movie in user_ratings.iterrows()
                            ]),

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
                dbc.Row([
                    html.H3("Based on the movie you searched for!",
                            className="sub-title"),
                ],),
                html.Div("", id="searched-movie-title"),
                html.Div(html.H1("Your search bar is feeling cinematic! Type in a movie!", style={"textAlign": "center", "marginTop": "150px"}), id="movie-recommend-cards",
                         style={"display": "flex",
                                "flexWrap": "wrap",
                                            "justifyContent": "center"}
                         ),


                dbc.Row([
                        html.H3("Based on the movies you have watched!",
                                className="sub-title"),
                        ],),
                html.Div([

                    dbc.Row(
                        user_movie_cards[i:i+5]
                    ) for i in range(0, len(user_movie_cards), 5)


                ], id="user-recommend-cards",
                    style={"display": "flex",
                           "flexWrap": "wrap",
                           "justifyContent": "center"}
                )



            ], width=10)

            ],

            style={"marginBottom": "10px",
                   "marginTop": "10px"},),
],
)


@callback(
    Output("movie-recommend-cards", "children"),
    Output("searched-movie-title", "children"),
    Input("search-button", "n_clicks"),
    Input("search", "n_submit"),

    State("search", "value")

)
def add_movie_cards(n_clicks, n_submit, search):
    if search is None:
        return [html.H1("Your search bar is feeling cinematic! Type in a movie!", style={"textAlign": "center", "marginTop": "150px"})], ""
    else:
        movie = get_movie_recommendation(search, movie_final_dataset,
                                         movie_movies, movie_csr_data, movie_knn)
        if movie is None:
            return [html.H1("Movie not found! Try again!", style={"textAlign": "center", "marginTop": "150px"})], ""
        else:
            movie = [int(float(i)) for i in movie]
            movie = get_movies_from_id_list(movies_df, movie)
            rows = []
            movie_movie_cards = [create_movie_card(movie)
                                 for _, movie in movie.iterrows()]
            for i in range(0, len(movie_movie_cards), 5):
                rows.append(dbc.Row(movie_movie_cards[i:i+5]))

            title = get_movie(search, movies_df).iloc[0]['title']
            searched_movie_title = html.H4(
                "You have searched for: " + title)

            return rows, searched_movie_title
