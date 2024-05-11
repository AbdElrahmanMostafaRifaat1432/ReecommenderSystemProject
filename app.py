import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State


# create the app with the slate theme

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.CYBORG, 'assets/styles/main_app.css'], use_pages=True)


sidebar = dbc.Nav([
    dbc.NavLink("Home", href="/", active="exact", className="home-link"),
    dbc.NavLink("Recommend", href="/exchanges",
                active="exact", className="home-link"),
    dbc.NavbarToggler(id="filter-toggler", className="home-link", n_clicks=0, children=[
        dbc.NavLink("Filter",  href="/filter", active="exact",
                    className="coins-navbar-expand", id="home-link"),
    ]),
],
    horizontal=True,
    pills=True,
    style={
    "justify-content": "center",
    "marginLeft": "25px",
    "marginRight": "10px"}
)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("CineScribe", className="main-title")
        ],
        )
    ],
    ),

    html.Hr(),

    dbc.Row([
        dbc.Col([
            sidebar
        ],
            width=12

        ),

        dbc.Col([
            dash.page_container
        ],
            # width=10
        )
    ])
],
    fluid=True
)


if __name__ == '__main__':
    app.run_server(debug=True)
