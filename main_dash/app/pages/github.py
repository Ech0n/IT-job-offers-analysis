import dash
from dash import html, dcc
from app import tree_chart_github


dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children=''),

    html.Div(children=tree_chart_github.create_chart()),

])