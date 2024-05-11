import dash
from dash import html, dcc, callback, Input, Output, State
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
    name="Filter",
)


layout = html.Div(
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Button(
                    "Filter By Genre",
                    id="filter-toggler",
                    className="coins-navbar-expand",
                    n_clicks=0,
                    style={
                        "width": "100%",
                        "marginBottom": "10px",
                    }
                ),
                dbc.Collapse(
                    dbc.Checklist(
                        options=[
                            {"label": genre, "value": genre}
                            for genre in unique_genres
                        ],
                        value=[],
                        id="genre-filter",
                    ),
                    id="filter-collapse",
                    is_open=False,
                ),
            ],
                style={
                "marginLeft": "10px",
            }
            ),
            html.Div([
                dbc.Button(
                    "Filter By Year",
                    id="year-toggler",
                    className="coins-navbar-expand",
                    n_clicks=0,
                    style={
                        "width": "100%",
                        "marginBottom": "10px",
                    }
                ),
                # collapse the filter, and add checkboxes for years
                dbc.Collapse(
                    [
                        dcc.RangeSlider(
                            id="year-filter",
                            min=min(unique_years),
                            max=max(unique_years),
                            step=1,
                            value=[min(unique_years), max(unique_years)],
                            pushable=1,
                            # make marks color white
                            marks={
                                year: {"label": str(year), "style": {
                                    "color": "white"}}
                                for year in range(int(min(unique_years)), int(max(unique_years)) + 1, 30)
                            },
                            tooltip={"placement": "bottom",
                                     "always_visible": True},

                        ),

                        dbc.Row([
                            # add two text boxes to select min and max years
                            dbc.Col([
                                dbc.Input(
                                    id="min-year",
                                    type="number",
                                    placeholder="Min Year",
                                    min=min(unique_years),
                                    max=max(unique_years),
                                    style={"width": "100%"},
                                ),
                            ]),
                            dbc.Col([
                                dbc.Input(
                                    id="max-year",
                                    type="number",
                                    min=min(unique_years),
                                    max=max(unique_years),
                                    placeholder="Max Year",
                                    style={"width": "100%"},
                                ),
                            ]),

                        ],),

                        dbc.Button(
                            "Apply",
                            id="apply-year",
                            className="coins-navbar-expand",
                            style={
                                "width": "50%",
                                "marginTop": "10px",
                                # move it to the center
                                "marginLeft": "25%"
                            }
                        ),

                    ],

                    id="year-collapse",
                    is_open=False,
                ),
            ],
                style={
                "marginLeft": "10px",
            }
            ),
        ],
            width=2
        ),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.H4("Explore",
                            style={"backgroundColor": "#212121",
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
                               "height": "100%"},
                    ),
                ],
                    width=8,

                ),
                dbc.Col([
                    dbc.Button(
                        "Search",
                        id="search-button",
                        className="coins-navbar-expand",
                        style={"width": "100%",
                               "height": "80%"},
                    ),
                ],
                    width=2,
                    style={"display": "flex",
                           "alignItems": "center",
                           "justifyContent": "center"}
                ),
            ],
                style={"marginBottom": "10px",
                       "marginTop": "10px"},
            ),

            html.Div(id="movie-cards",
                        style={"display": "flex",
                               "flexWrap": "wrap",
                               "justifyContent": "center"}
                     ),
        ],
            width=10,
            style={"marginTop": "10px",
                   "marginBottom": "10px"},
        ),
    ],
    )
)


@ callback(
    Output("filter-collapse", "is_open"),
    [Input("filter-toggler", "n_clicks")],
    [State("filter-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@ callback(
    Output("year-collapse", "is_open"),
    [Input("year-toggler", "n_clicks")],
    [State("year-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@ callback(
    Output("year-filter", "value"),
    [Input("apply-year", "n_clicks")],
    [State("min-year", "value"),
     State("max-year", "value")]
)
def apply_year_filter(n, min_year, max_year):
    # make sure the min year is less than the max year, if it is not, don't change the slider
    if min_year > max_year:
        return dash.no_update
    if n:
        return [min_year, max_year]
    return [min(unique_years), max(unique_years)]


# call back to add the movie cards based on the search, filters, make it 4 cards per row
# apply only when the search button is clicked, or when enter is pressed on the search bar
@ callback(
    Output("movie-cards", "children"),
    [Input("search-button", "n_clicks"),
     Input("search", "n_submit"),
     Input("genre-filter", "value"),
     Input("year-filter", "value"),
     State("search", "value")]
)
def add_movie_cards(n, n_submit, genres, years, search_value):
    # if the search button is not clicked, and enter is not pressed, return no update
    if not n and not n_submit:
        return dash.no_update

    # get the search value
    search_value = dash.callback_context.states['search.value']

    # get the movies that match the search value
    closest_movies = get_closest_matches(search_value, movies_df, 'title', 20)

    # filter the movies based on the genres
    if genres:
        closest_movies = closest_movies[closest_movies['genres'].str.contains(
            '|'.join(genres))]

    # filter the movies based on the years
    if years:
        closest_movies = closest_movies[(closest_movies['year'] >= years[0]) & (
            closest_movies['year'] <= years[1])]

    # create the movie cards
    movie_cards = [create_movie_card(movie)
                   for _, movie in closest_movies.iterrows()]

    rows = []
    for i in range(0, len(movie_cards), 5):
        rows.append(dbc.Row(movie_cards[i:i + 5]))

    if not rows:
        return html.Div([html.H1("No Movies Found", style={"textAlign": "center", "marginTop": "30px"}),
                         html.H4("Try a different search term or filter", style={"textAlign": "center"})])

    return rows
