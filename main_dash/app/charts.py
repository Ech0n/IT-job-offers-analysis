from app import app
import pandas as pd
from dash import html, dcc, callback, Output, Input
import plotly.express as px


def create_chart():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

    layout = [
        html.H1(children='Title of Dash App', style={'textAlign':'center'}),
        dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
        dcc.Graph(id='graph-content')
    ]

    
    @callback(
        Output('graph-content', 'figure'),
        Input('dropdown-selection', 'value')
    )
    def update_graph(value):
        dff = df[df.country==value]
        return px.line(dff, x='year', y='pop')

    return layout