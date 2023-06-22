import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, callback
from dash_bootstrap_components._components.Container import Container
import dash

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)


navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row( children = [
            dbc.Col(dbc.NavItem(dbc.NavLink("Home", href="/"))),
            dbc.Col(dbc.NavItem(dbc.NavLink("Github Charts", href="github"))),
            dbc.Col(dbc.NavItem(dbc.NavLink("Stack Overflow", href="stack-overflow"))),
            dbc.Col(dbc.NavItem(dbc.NavLink("Pracuj", href="pracuj"))),
            
            ],
            className="ml-5"),
            
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
)


# add callback for toggling the collapse on small screens
@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open