    dbc.NavbarToggler(id="filter-toggler", className="home-link", n_clicks=0, children=[
        dbc.NavLink("Filter",  href="/filter", active="exact",
                    className="coins-navbar-expand", id="home-link"),
    ]),
    dbc.Collapse([
        dbc.Checklist(
            options=[
                {"label": genre, "value": genre} for genre in unique_genres
            ],
            value=[],
            id="genre-checklist",
            inline=True
        ),
    ],
        id="filter-collapse",
        is_open=False,
        navbar=True,
        # margin left
        style={"marginLeft": "15px", "marginTop": "10px"}
    ),
