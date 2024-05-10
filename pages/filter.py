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
    # create a search bar
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
                # collapse the filter, and add checkboxes for genres
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

        dbc.Col(
            dbc.Input(
                id="search",
                type="search",
                placeholder="Search...",
                style={"width": "100%"},
            ),
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
