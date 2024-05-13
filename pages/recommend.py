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
        ], width=3),
        dbc.Col([
            html.H2("Recommendations"),
            html.H3("Search for a movie"),
            dcc.Input(id='movie_name', type='text',
                      placeholder='Enter a movie name'),
            html.Button('Search', id='search_button'),
            html.Div(id='search_results')
        ], width=9)
    ])

]
)
